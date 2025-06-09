"""Pytest configuration and fixtures for AutoContentor tests."""

import asyncio
import os
from typing import AsyncGenerator, Generator
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import AsyncClient

# Set test environment
os.environ["APP_ENVIRONMENT"] = "test"
os.environ["DEBUG"] = "true"
os.environ["MONGODB_DATABASE"] = "autocontentor_test"
os.environ["REDIS_DB"] = "1"

from src.auto_contentor.shared import get_mongo_client, get_redis_client, close_mongo_client, close_redis_client
from src.auto_contentor.shared.models import Campaign, CampaignRequest, CampaignPriority


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def mongo_client():
    """Provide MongoDB client for tests."""
    client = await get_mongo_client()
    yield client
    await close_mongo_client()


@pytest_asyncio.fixture(scope="session")
async def redis_client():
    """Provide Redis client for tests."""
    client = await get_redis_client()
    yield client
    await close_redis_client()


@pytest_asyncio.fixture
async def clean_database(mongo_client):
    """Clean database before each test."""
    # Clean test collections
    collections = [
        "campaigns",
        "keyword_results",
        "audience_results", 
        "competitor_results",
        "trend_results",
        "final_reports"
    ]
    
    for collection_name in collections:
        await mongo_client._database[collection_name].delete_many({})
    
    yield
    
    # Clean up after test
    for collection_name in collections:
        await mongo_client._database[collection_name].delete_many({})


@pytest_asyncio.fixture
async def clean_cache(redis_client):
    """Clean Redis cache before each test."""
    await redis_client.flushdb()
    yield
    await redis_client.flushdb()


@pytest.fixture
def sample_campaign_request() -> CampaignRequest:
    """Provide sample campaign request for testing."""
    return CampaignRequest(
        name="Test Campaign",
        description="A test campaign for unit testing",
        seed_keywords=["digital marketing", "content strategy", "SEO"],
        competitor_urls=["https://competitor1.com", "https://competitor2.com"],
        target_region="US",
        target_language="en",
        industry="Digital Marketing",
        priority=CampaignPriority.MEDIUM
    )


@pytest.fixture
def sample_campaign(sample_campaign_request) -> Campaign:
    """Provide sample campaign for testing."""
    return Campaign(
        id=uuid4(),
        name=sample_campaign_request.name,
        description=sample_campaign_request.description,
        seed_keywords=sample_campaign_request.seed_keywords,
        competitor_urls=sample_campaign_request.competitor_urls,
        target_region=sample_campaign_request.target_region,
        target_language=sample_campaign_request.target_language,
        industry=sample_campaign_request.industry,
        priority=sample_campaign_request.priority
    )


@pytest_asyncio.fixture
async def http_client() -> AsyncGenerator[AsyncClient, None]:
    """Provide HTTP client for API testing."""
    async with AsyncClient() as client:
        yield client


@pytest.fixture
def mock_api_responses():
    """Provide mock API responses for external services."""
    return {
        "google_trends": {
            "default": [
                {"date": "2024-01", "value": 75},
                {"date": "2024-02", "value": 80},
                {"date": "2024-03", "value": 85}
            ]
        },
        "serpapi": {
            "default": {
                "organic_results": [
                    {
                        "title": "Test Result 1",
                        "link": "https://example1.com",
                        "snippet": "Test snippet 1"
                    },
                    {
                        "title": "Test Result 2", 
                        "link": "https://example2.com",
                        "snippet": "Test snippet 2"
                    }
                ]
            }
        }
    }


@pytest.fixture
def mock_keyword_data():
    """Provide mock keyword analysis data."""
    return {
        "keywords": [
            {
                "keyword": "digital marketing",
                "search_volume": 50000,
                "competition": 0.7,
                "cpc": 2.5,
                "difficulty": "medium"
            },
            {
                "keyword": "content strategy",
                "search_volume": 25000,
                "competition": 0.5,
                "cpc": 1.8,
                "difficulty": "easy"
            }
        ]
    }


@pytest.fixture
def mock_audience_data():
    """Provide mock audience analysis data."""
    return {
        "personas": [
            {
                "name": "Marketing Manager",
                "age_group": "millennial",
                "interests": ["marketing", "analytics", "strategy"],
                "pain_points": ["limited budget", "measuring ROI"]
            }
        ]
    }


@pytest.fixture
def mock_competitor_data():
    """Provide mock competitor analysis data."""
    return {
        "competitors": [
            {
                "name": "Competitor 1",
                "website": "https://competitor1.com",
                "domain_authority": 75,
                "monthly_traffic": 100000,
                "top_keywords": ["marketing", "strategy"]
            }
        ]
    }


@pytest.fixture
def mock_trend_data():
    """Provide mock trend analysis data."""
    return {
        "trends": [
            {
                "keyword": "AI marketing",
                "trend_score": 85,
                "direction": "rising",
                "growth_rate": 25.5
            }
        ]
    }


# Markers for different test types
pytest.mark.unit = pytest.mark.unit
pytest.mark.integration = pytest.mark.integration
pytest.mark.e2e = pytest.mark.e2e
pytest.mark.slow = pytest.mark.slow


def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "slow: Slow running tests")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on file location."""
    for item in items:
        # Add unit marker to tests in unit/ directory
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        
        # Add integration marker to tests in integration/ directory
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        
        # Add e2e marker to tests in e2e/ directory
        elif "e2e" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)


# Skip tests if dependencies are not available
def pytest_runtest_setup(item):
    """Setup for individual test runs."""
    # Skip integration tests if databases are not available
    if "integration" in item.keywords:
        try:
            import pymongo
            import redis
        except ImportError:
            pytest.skip("Database dependencies not available for integration tests")
    
    # Skip e2e tests in CI unless explicitly enabled
    if "e2e" in item.keywords and os.getenv("SKIP_E2E_TESTS", "false").lower() == "true":
        pytest.skip("E2E tests skipped in CI environment")
