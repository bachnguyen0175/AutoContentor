"""MongoDB client for AutoContentor."""

from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import ASCENDING, DESCENDING
from pymongo.errors import DuplicateKeyError, PyMongoError

from ..config.constants import COLLECTIONS
from ..config.settings import get_settings
from ..utils.logger import get_logger, log_operation, perf_logger

logger = get_logger(__name__)


class MongoClient:
    """MongoDB client wrapper with async support."""
    
    def __init__(self):
        self.settings = get_settings()
        self._client: Optional[AsyncIOMotorClient] = None
        self._database: Optional[AsyncIOMotorDatabase] = None
        self._connected = False
    
    async def connect(self) -> None:
        """Connect to MongoDB."""
        if self._connected:
            return
        
        try:
            with log_operation("mongodb_connection"):
                self._client = AsyncIOMotorClient(
                    self.settings.mongodb_connection_string,
                    serverSelectionTimeoutMS=5000,
                    connectTimeoutMS=5000,
                    socketTimeoutMS=5000
                )
                
                # Test connection
                await self._client.admin.command('ping')
                
                self._database = self._client[self.settings.database.mongodb_database]
                self._connected = True
                
                logger.info("Connected to MongoDB successfully")
                
                # Create indexes
                await self._create_indexes()
                
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise
    
    async def disconnect(self) -> None:
        """Disconnect from MongoDB."""
        if self._client:
            self._client.close()
            self._connected = False
            logger.info("Disconnected from MongoDB")
    
    async def _create_indexes(self) -> None:
        """Create database indexes for better performance."""
        try:
            # Campaigns collection indexes
            campaigns = self._database[COLLECTIONS["CAMPAIGNS"]]
            await campaigns.create_index([("id", ASCENDING)], unique=True)
            await campaigns.create_index([("status", ASCENDING)])
            await campaigns.create_index([("created_at", DESCENDING)])
            await campaigns.create_index([("priority", ASCENDING)])
            
            # Results collections indexes
            for collection_name in [
                COLLECTIONS["KEYWORD_RESULTS"],
                COLLECTIONS["AUDIENCE_RESULTS"],
                COLLECTIONS["COMPETITOR_RESULTS"],
                COLLECTIONS["TREND_RESULTS"]
            ]:
                collection = self._database[collection_name]
                await collection.create_index([("id", ASCENDING)], unique=True)
                await collection.create_index([("campaign_id", ASCENDING)])
                await collection.create_index([("created_at", DESCENDING)])
            
            # Reports collection indexes
            reports = self._database[COLLECTIONS["FINAL_REPORTS"]]
            await reports.create_index([("id", ASCENDING)], unique=True)
            await reports.create_index([("campaign_id", ASCENDING)])
            await reports.create_index([("status", ASCENDING)])
            await reports.create_index([("created_at", DESCENDING)])
            
            logger.info("Database indexes created successfully")
            
        except Exception as e:
            logger.warning(f"Failed to create some indexes: {str(e)}")
    
    def _ensure_connected(self) -> None:
        """Ensure database is connected."""
        if not self._connected or not self._database:
            raise RuntimeError("Database not connected. Call connect() first.")
    
    def _serialize_document(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        """Serialize document for MongoDB storage."""
        if not doc:
            return doc
        
        # Convert UUID objects to strings
        for key, value in doc.items():
            if isinstance(value, UUID):
                doc[key] = str(value)
            elif isinstance(value, dict):
                doc[key] = self._serialize_document(value)
            elif isinstance(value, list):
                doc[key] = [
                    self._serialize_document(item) if isinstance(item, dict) else str(item) if isinstance(item, UUID) else item
                    for item in value
                ]
        
        return doc
    
    async def insert_one(self, collection_name: str, document: Dict[str, Any]) -> str:
        """Insert a single document."""
        self._ensure_connected()
        
        try:
            with log_operation(f"mongodb_insert_one: {collection_name}"):
                collection = self._database[collection_name]
                serialized_doc = self._serialize_document(document.copy())
                
                result = await collection.insert_one(serialized_doc)
                
                perf_logger.log_database_query(
                    collection=collection_name,
                    operation="insert_one",
                    duration=0,  # Would need timing logic
                    count=1
                )
                
                logger.debug(f"Inserted document in {collection_name}: {result.inserted_id}")
                return str(result.inserted_id)
                
        except DuplicateKeyError as e:
            logger.error(f"Duplicate key error in {collection_name}: {str(e)}")
            raise
        except PyMongoError as e:
            logger.error(f"MongoDB error in insert_one for {collection_name}: {str(e)}")
            raise
    
    async def find_one(self, collection_name: str, filter_dict: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find a single document."""
        self._ensure_connected()
        
        try:
            with log_operation(f"mongodb_find_one: {collection_name}"):
                collection = self._database[collection_name]
                serialized_filter = self._serialize_document(filter_dict.copy())
                
                result = await collection.find_one(serialized_filter)
                
                perf_logger.log_database_query(
                    collection=collection_name,
                    operation="find_one",
                    duration=0,
                    count=1 if result else 0
                )
                
                return result
                
        except PyMongoError as e:
            logger.error(f"MongoDB error in find_one for {collection_name}: {str(e)}")
            raise
    
    async def find_many(
        self,
        collection_name: str,
        filter_dict: Dict[str, Any] = None,
        limit: int = None,
        skip: int = None,
        sort: List[tuple] = None
    ) -> List[Dict[str, Any]]:
        """Find multiple documents."""
        self._ensure_connected()
        
        try:
            with log_operation(f"mongodb_find_many: {collection_name}"):
                collection = self._database[collection_name]
                filter_dict = filter_dict or {}
                serialized_filter = self._serialize_document(filter_dict.copy())
                
                cursor = collection.find(serialized_filter)
                
                if sort:
                    cursor = cursor.sort(sort)
                if skip:
                    cursor = cursor.skip(skip)
                if limit:
                    cursor = cursor.limit(limit)
                
                results = await cursor.to_list(length=limit)
                
                perf_logger.log_database_query(
                    collection=collection_name,
                    operation="find_many",
                    duration=0,
                    count=len(results)
                )
                
                return results
                
        except PyMongoError as e:
            logger.error(f"MongoDB error in find_many for {collection_name}: {str(e)}")
            raise
    
    async def update_one(
        self,
        collection_name: str,
        filter_dict: Dict[str, Any],
        update_dict: Dict[str, Any],
        upsert: bool = False
    ) -> bool:
        """Update a single document."""
        self._ensure_connected()
        
        try:
            with log_operation(f"mongodb_update_one: {collection_name}"):
                collection = self._database[collection_name]
                serialized_filter = self._serialize_document(filter_dict.copy())
                serialized_update = self._serialize_document(update_dict.copy())
                
                result = await collection.update_one(
                    serialized_filter,
                    {"$set": serialized_update},
                    upsert=upsert
                )
                
                perf_logger.log_database_query(
                    collection=collection_name,
                    operation="update_one",
                    duration=0,
                    count=result.modified_count
                )
                
                return result.modified_count > 0
                
        except PyMongoError as e:
            logger.error(f"MongoDB error in update_one for {collection_name}: {str(e)}")
            raise
    
    async def delete_one(self, collection_name: str, filter_dict: Dict[str, Any]) -> bool:
        """Delete a single document."""
        self._ensure_connected()
        
        try:
            with log_operation(f"mongodb_delete_one: {collection_name}"):
                collection = self._database[collection_name]
                serialized_filter = self._serialize_document(filter_dict.copy())
                
                result = await collection.delete_one(serialized_filter)
                
                perf_logger.log_database_query(
                    collection=collection_name,
                    operation="delete_one",
                    duration=0,
                    count=result.deleted_count
                )
                
                return result.deleted_count > 0
                
        except PyMongoError as e:
            logger.error(f"MongoDB error in delete_one for {collection_name}: {str(e)}")
            raise
    
    async def count_documents(self, collection_name: str, filter_dict: Dict[str, Any] = None) -> int:
        """Count documents in collection."""
        self._ensure_connected()
        
        try:
            collection = self._database[collection_name]
            filter_dict = filter_dict or {}
            serialized_filter = self._serialize_document(filter_dict.copy())
            
            count = await collection.count_documents(serialized_filter)
            return count
            
        except PyMongoError as e:
            logger.error(f"MongoDB error in count_documents for {collection_name}: {str(e)}")
            raise
    
    async def aggregate(self, collection_name: str, pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Execute aggregation pipeline."""
        self._ensure_connected()
        
        try:
            with log_operation(f"mongodb_aggregate: {collection_name}"):
                collection = self._database[collection_name]
                
                cursor = collection.aggregate(pipeline)
                results = await cursor.to_list(length=None)
                
                perf_logger.log_database_query(
                    collection=collection_name,
                    operation="aggregate",
                    duration=0,
                    count=len(results)
                )
                
                return results
                
        except PyMongoError as e:
            logger.error(f"MongoDB error in aggregate for {collection_name}: {str(e)}")
            raise
    
    async def health_check(self) -> bool:
        """Check database health."""
        try:
            if not self._connected:
                return False
            
            await self._client.admin.command('ping')
            return True
            
        except Exception as e:
            logger.error(f"MongoDB health check failed: {str(e)}")
            return False


# Global MongoDB client instance
_mongo_client: Optional[MongoClient] = None


async def get_mongo_client() -> MongoClient:
    """Get MongoDB client instance."""
    global _mongo_client
    
    if _mongo_client is None:
        _mongo_client = MongoClient()
        await _mongo_client.connect()
    
    return _mongo_client


async def close_mongo_client() -> None:
    """Close MongoDB client connection."""
    global _mongo_client
    
    if _mongo_client:
        await _mongo_client.disconnect()
        _mongo_client = None
