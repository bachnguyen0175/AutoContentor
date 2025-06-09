"""Redis client for AutoContentor."""

import json
from typing import Any, Dict, List, Optional, Union

import redis.asyncio as redis
from redis.exceptions import RedisError

from ..config.constants import CACHE_TTL
from ..config.settings import get_settings
from ..utils.logger import get_logger, log_operation, perf_logger

logger = get_logger(__name__)


class RedisClient:
    """Redis client wrapper with async support."""
    
    def __init__(self):
        self.settings = get_settings()
        self._client: Optional[redis.Redis] = None
        self._connected = False
    
    async def connect(self) -> None:
        """Connect to Redis."""
        if self._connected:
            return
        
        try:
            with log_operation("redis_connection"):
                self._client = redis.from_url(
                    self.settings.redis_connection_string,
                    encoding="utf-8",
                    decode_responses=True,
                    socket_connect_timeout=5,
                    socket_timeout=5
                )
                
                # Test connection
                await self._client.ping()
                
                self._connected = True
                logger.info("Connected to Redis successfully")
                
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {str(e)}")
            raise
    
    async def disconnect(self) -> None:
        """Disconnect from Redis."""
        if self._client:
            await self._client.close()
            self._connected = False
            logger.info("Disconnected from Redis")
    
    def _ensure_connected(self) -> None:
        """Ensure Redis is connected."""
        if not self._connected or not self._client:
            raise RuntimeError("Redis not connected. Call connect() first.")
    
    def _serialize_value(self, value: Any) -> str:
        """Serialize value for Redis storage."""
        if isinstance(value, (dict, list)):
            return json.dumps(value, default=str)
        return str(value)
    
    def _deserialize_value(self, value: str) -> Any:
        """Deserialize value from Redis."""
        if not value:
            return None
        
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value
    
    async def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """Set a key-value pair with optional TTL."""
        self._ensure_connected()
        
        try:
            with log_operation(f"redis_set: {key}"):
                serialized_value = self._serialize_value(value)
                
                if ttl:
                    result = await self._client.setex(key, ttl, serialized_value)
                else:
                    result = await self._client.set(key, serialized_value)
                
                logger.debug(f"Set Redis key: {key}")
                return bool(result)
                
        except RedisError as e:
            logger.error(f"Redis error in set for key {key}: {str(e)}")
            raise
    
    async def get(self, key: str) -> Any:
        """Get value by key."""
        self._ensure_connected()
        
        try:
            with log_operation(f"redis_get: {key}"):
                value = await self._client.get(key)
                
                if value is None:
                    return None
                
                return self._deserialize_value(value)
                
        except RedisError as e:
            logger.error(f"Redis error in get for key {key}: {str(e)}")
            raise
    
    async def delete(self, key: str) -> bool:
        """Delete a key."""
        self._ensure_connected()
        
        try:
            with log_operation(f"redis_delete: {key}"):
                result = await self._client.delete(key)
                logger.debug(f"Deleted Redis key: {key}")
                return bool(result)
                
        except RedisError as e:
            logger.error(f"Redis error in delete for key {key}: {str(e)}")
            raise
    
    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        self._ensure_connected()
        
        try:
            result = await self._client.exists(key)
            return bool(result)
            
        except RedisError as e:
            logger.error(f"Redis error in exists for key {key}: {str(e)}")
            raise
    
    async def expire(self, key: str, ttl: int) -> bool:
        """Set TTL for existing key."""
        self._ensure_connected()
        
        try:
            result = await self._client.expire(key, ttl)
            return bool(result)
            
        except RedisError as e:
            logger.error(f"Redis error in expire for key {key}: {str(e)}")
            raise
    
    async def ttl(self, key: str) -> int:
        """Get TTL for key."""
        self._ensure_connected()
        
        try:
            return await self._client.ttl(key)
            
        except RedisError as e:
            logger.error(f"Redis error in ttl for key {key}: {str(e)}")
            raise
    
    async def increment(self, key: str, amount: int = 1) -> int:
        """Increment a key's value."""
        self._ensure_connected()
        
        try:
            result = await self._client.incrby(key, amount)
            return result
            
        except RedisError as e:
            logger.error(f"Redis error in increment for key {key}: {str(e)}")
            raise
    
    async def decrement(self, key: str, amount: int = 1) -> int:
        """Decrement a key's value."""
        self._ensure_connected()
        
        try:
            result = await self._client.decrby(key, amount)
            return result
            
        except RedisError as e:
            logger.error(f"Redis error in decrement for key {key}: {str(e)}")
            raise
    
    # List operations
    async def lpush(self, key: str, *values: Any) -> int:
        """Push values to the left of a list."""
        self._ensure_connected()
        
        try:
            serialized_values = [self._serialize_value(v) for v in values]
            result = await self._client.lpush(key, *serialized_values)
            return result
            
        except RedisError as e:
            logger.error(f"Redis error in lpush for key {key}: {str(e)}")
            raise
    
    async def rpush(self, key: str, *values: Any) -> int:
        """Push values to the right of a list."""
        self._ensure_connected()
        
        try:
            serialized_values = [self._serialize_value(v) for v in values]
            result = await self._client.rpush(key, *serialized_values)
            return result
            
        except RedisError as e:
            logger.error(f"Redis error in rpush for key {key}: {str(e)}")
            raise
    
    async def lpop(self, key: str) -> Any:
        """Pop value from the left of a list."""
        self._ensure_connected()
        
        try:
            value = await self._client.lpop(key)
            return self._deserialize_value(value) if value else None
            
        except RedisError as e:
            logger.error(f"Redis error in lpop for key {key}: {str(e)}")
            raise
    
    async def rpop(self, key: str) -> Any:
        """Pop value from the right of a list."""
        self._ensure_connected()
        
        try:
            value = await self._client.rpop(key)
            return self._deserialize_value(value) if value else None
            
        except RedisError as e:
            logger.error(f"Redis error in rpop for key {key}: {str(e)}")
            raise
    
    async def llen(self, key: str) -> int:
        """Get length of a list."""
        self._ensure_connected()
        
        try:
            return await self._client.llen(key)
            
        except RedisError as e:
            logger.error(f"Redis error in llen for key {key}: {str(e)}")
            raise
    
    async def lrange(self, key: str, start: int = 0, end: int = -1) -> List[Any]:
        """Get range of values from a list."""
        self._ensure_connected()
        
        try:
            values = await self._client.lrange(key, start, end)
            return [self._deserialize_value(v) for v in values]
            
        except RedisError as e:
            logger.error(f"Redis error in lrange for key {key}: {str(e)}")
            raise
    
    # Hash operations
    async def hset(self, key: str, field: str, value: Any) -> bool:
        """Set field in hash."""
        self._ensure_connected()
        
        try:
            serialized_value = self._serialize_value(value)
            result = await self._client.hset(key, field, serialized_value)
            return bool(result)
            
        except RedisError as e:
            logger.error(f"Redis error in hset for key {key}, field {field}: {str(e)}")
            raise
    
    async def hget(self, key: str, field: str) -> Any:
        """Get field from hash."""
        self._ensure_connected()
        
        try:
            value = await self._client.hget(key, field)
            return self._deserialize_value(value) if value else None
            
        except RedisError as e:
            logger.error(f"Redis error in hget for key {key}, field {field}: {str(e)}")
            raise
    
    async def hgetall(self, key: str) -> Dict[str, Any]:
        """Get all fields from hash."""
        self._ensure_connected()
        
        try:
            hash_data = await self._client.hgetall(key)
            return {k: self._deserialize_value(v) for k, v in hash_data.items()}
            
        except RedisError as e:
            logger.error(f"Redis error in hgetall for key {key}: {str(e)}")
            raise
    
    async def hdel(self, key: str, *fields: str) -> int:
        """Delete fields from hash."""
        self._ensure_connected()
        
        try:
            result = await self._client.hdel(key, *fields)
            return result
            
        except RedisError as e:
            logger.error(f"Redis error in hdel for key {key}: {str(e)}")
            raise
    
    # Utility methods
    async def keys(self, pattern: str = "*") -> List[str]:
        """Get keys matching pattern."""
        self._ensure_connected()
        
        try:
            return await self._client.keys(pattern)
            
        except RedisError as e:
            logger.error(f"Redis error in keys for pattern {pattern}: {str(e)}")
            raise
    
    async def flushdb(self) -> bool:
        """Flush current database."""
        self._ensure_connected()
        
        try:
            result = await self._client.flushdb()
            logger.warning("Redis database flushed")
            return bool(result)
            
        except RedisError as e:
            logger.error(f"Redis error in flushdb: {str(e)}")
            raise
    
    async def health_check(self) -> bool:
        """Check Redis health."""
        try:
            if not self._connected:
                return False
            
            await self._client.ping()
            return True
            
        except Exception as e:
            logger.error(f"Redis health check failed: {str(e)}")
            return False


# Global Redis client instance
_redis_client: Optional[RedisClient] = None


async def get_redis_client() -> RedisClient:
    """Get Redis client instance."""
    global _redis_client
    
    if _redis_client is None:
        _redis_client = RedisClient()
        await _redis_client.connect()
    
    return _redis_client


async def close_redis_client() -> None:
    """Close Redis client connection."""
    global _redis_client
    
    if _redis_client:
        await _redis_client.disconnect()
        _redis_client = None
