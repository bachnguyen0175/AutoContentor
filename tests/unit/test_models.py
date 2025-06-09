"""Unit tests for data models."""

import pytest
from datetime import datetime
from uuid import uuid4

from src.auto_contentor.shared.models import (
    Campaign,
    CampaignRequest,
    CampaignStatus,
    CampaignPriority,
    KeywordMetrics,
    KeywordDifficulty,
    KeywordIntent,
    BuyerPersona,
    AgeGroup,
    Gender
)


class TestCampaignModels:
    """Test campaign-related models."""
    
    def test_campaign_request_creation(self):
        """Test creating a campaign request."""
        request = CampaignRequest(
            name="Test Campaign",
            description="A test campaign",
            seed_keywords=["test", "keyword"],
            competitor_urls=["https://example.com"],
            target_region="US",
            target_language="en",
            industry="Technology",
            priority=CampaignPriority.HIGH
        )
        
        assert request.name == "Test Campaign"
        assert len(request.seed_keywords) == 2
        assert request.priority == CampaignPriority.HIGH
    
    def test_campaign_creation(self):
        """Test creating a campaign."""
        campaign = Campaign(
            name="Test Campaign",
            seed_keywords=["test", "keyword"],
            target_region="US"
        )
        
        assert campaign.name == "Test Campaign"
        assert campaign.status == CampaignStatus.PENDING
        assert campaign.total_tasks == 4
        assert campaign.completed_tasks == 0
        assert isinstance(campaign.created_at, datetime)
    
    def test_campaign_progress_calculation(self):
        """Test campaign progress calculation."""
        campaign = Campaign(
            name="Test Campaign",
            seed_keywords=["test"],
            total_tasks=4,
            completed_tasks=2
        )
        
        assert campaign.progress_percentage == 50.0
    
    def test_campaign_status_update(self):
        """Test campaign status updates."""
        campaign = Campaign(
            name="Test Campaign",
            seed_keywords=["test"]
        )
        
        # Test starting campaign
        campaign.update_status(CampaignStatus.RUNNING)
        assert campaign.status == CampaignStatus.RUNNING
        assert campaign.started_at is not None
        
        # Test completing campaign
        campaign.update_status(CampaignStatus.COMPLETED)
        assert campaign.status == CampaignStatus.COMPLETED
        assert campaign.completed_at is not None
    
    def test_campaign_task_completion(self):
        """Test task completion logic."""
        campaign = Campaign(
            name="Test Campaign",
            seed_keywords=["test"],
            total_tasks=4
        )
        
        # Complete tasks one by one
        campaign.increment_completed_tasks()
        assert campaign.completed_tasks == 1
        assert campaign.status == CampaignStatus.PENDING
        
        campaign.increment_completed_tasks()
        campaign.increment_completed_tasks()
        campaign.increment_completed_tasks()
        
        # Should auto-complete when all tasks done
        assert campaign.completed_tasks == 4
        assert campaign.status == CampaignStatus.COMPLETED


class TestKeywordModels:
    """Test keyword-related models."""
    
    def test_keyword_metrics_creation(self):
        """Test creating keyword metrics."""
        metrics = KeywordMetrics(
            keyword="test keyword",
            search_volume=1000,
            competition=0.7,
            cpc=2.5,
            difficulty=KeywordDifficulty.MEDIUM,
            intent=KeywordIntent.INFORMATIONAL
        )
        
        assert metrics.keyword == "test keyword"
        assert metrics.search_volume == 1000
        assert metrics.difficulty == KeywordDifficulty.MEDIUM
    
    def test_keyword_difficulty_score(self):
        """Test keyword difficulty score calculation."""
        metrics = KeywordMetrics(
            keyword="test",
            difficulty=KeywordDifficulty.MEDIUM
        )
        
        assert metrics.difficulty_score == 0.6
    
    def test_keyword_opportunity_score(self):
        """Test keyword opportunity score calculation."""
        metrics = KeywordMetrics(
            keyword="test",
            search_volume=10000,
            competition=0.3,
            difficulty=KeywordDifficulty.EASY
        )
        
        score = metrics.opportunity_score
        assert 0 <= score <= 1
        assert score > 0  # Should have some opportunity


class TestAudienceModels:
    """Test audience-related models."""
    
    def test_buyer_persona_creation(self):
        """Test creating a buyer persona."""
        persona = BuyerPersona(
            name="Marketing Manager",
            description="A marketing professional",
            confidence_score=0.8
        )
        
        assert persona.name == "Marketing Manager"
        assert persona.confidence_score == 0.8
        assert isinstance(persona.id, type(uuid4()))
    
    def test_demographics_dominant_age_group(self):
        """Test demographics dominant age group calculation."""
        from src.auto_contentor.shared.models.audience import Demographics
        
        demographics = Demographics(
            age_groups={
                AgeGroup.MILLENNIAL: 45.0,
                AgeGroup.GEN_Z: 30.0,
                AgeGroup.GEN_X: 25.0
            }
        )
        
        assert demographics.dominant_age_group == AgeGroup.MILLENNIAL


class TestModelValidation:
    """Test model validation."""
    
    def test_campaign_request_validation(self):
        """Test campaign request validation."""
        # Valid request should not raise
        request = CampaignRequest(
            name="Valid Campaign",
            seed_keywords=["keyword1", "keyword2"]
        )
        assert request.name == "Valid Campaign"
    
    def test_invalid_campaign_request(self):
        """Test invalid campaign request."""
        with pytest.raises(ValueError):
            # Empty name should fail
            CampaignRequest(
                name="",
                seed_keywords=["keyword"]
            )
    
    def test_keyword_metrics_validation(self):
        """Test keyword metrics validation."""
        # Valid metrics
        metrics = KeywordMetrics(
            keyword="valid keyword",
            search_volume=1000,
            competition=0.5
        )
        assert metrics.keyword == "valid keyword"
        
        # Invalid competition score should fail
        with pytest.raises(ValueError):
            KeywordMetrics(
                keyword="test",
                competition=1.5  # Should be 0-1
            )


class TestModelSerialization:
    """Test model serialization."""
    
    def test_campaign_serialization(self):
        """Test campaign serialization to dict."""
        campaign = Campaign(
            name="Test Campaign",
            seed_keywords=["test"]
        )
        
        data = campaign.dict()
        assert data["name"] == "Test Campaign"
        assert "id" in data
        assert "created_at" in data
    
    def test_campaign_json_encoding(self):
        """Test campaign JSON encoding."""
        campaign = Campaign(
            name="Test Campaign",
            seed_keywords=["test"]
        )
        
        # Should be able to convert to JSON
        json_data = campaign.json()
        assert isinstance(json_data, str)
        assert "Test Campaign" in json_data
