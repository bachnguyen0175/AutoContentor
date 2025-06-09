"""Keyword research data models for AutoContentor."""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class KeywordDifficulty(str, Enum):
    """Keyword difficulty levels."""
    
    VERY_EASY = "very_easy"
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    VERY_HARD = "very_hard"


class KeywordIntent(str, Enum):
    """Search intent classification."""
    
    INFORMATIONAL = "informational"
    NAVIGATIONAL = "navigational"
    TRANSACTIONAL = "transactional"
    COMMERCIAL = "commercial"


class KeywordTrend(BaseModel):
    """Keyword trend data point."""
    
    date: str = Field(..., description="Date in YYYY-MM format")
    value: int = Field(..., description="Search volume or trend value", ge=0)


class RelatedKeyword(BaseModel):
    """Related keyword suggestion."""
    
    keyword: str = Field(..., description="Related keyword phrase")
    relevance_score: float = Field(..., description="Relevance score 0-1", ge=0, le=1)
    search_volume: Optional[int] = Field(None, description="Monthly search volume", ge=0)


class KeywordMetrics(BaseModel):
    """Comprehensive keyword metrics."""
    
    keyword: str = Field(..., description="Keyword phrase")
    search_volume: Optional[int] = Field(None, description="Monthly search volume", ge=0)
    competition: Optional[float] = Field(None, description="Competition score 0-1", ge=0, le=1)
    cpc: Optional[float] = Field(None, description="Cost per click in USD", ge=0)
    difficulty: Optional[KeywordDifficulty] = Field(None, description="SEO difficulty level")
    intent: Optional[KeywordIntent] = Field(None, description="Search intent classification")
    
    # Trend data
    trend_data: List[KeywordTrend] = Field(default_factory=list, description="Historical trend data")
    trend_direction: Optional[str] = Field(None, description="Trend direction: up, down, stable")
    
    # Related keywords
    related_keywords: List[RelatedKeyword] = Field(default_factory=list, description="Related keyword suggestions")
    
    # Additional metrics
    seasonal_trends: Dict[str, float] = Field(default_factory=dict, description="Seasonal trend patterns")
    top_ranking_pages: List[str] = Field(default_factory=list, description="Top ranking page URLs")
    
    @property
    def difficulty_score(self) -> Optional[float]:
        """Convert difficulty enum to numeric score."""
        if not self.difficulty:
            return None
        
        difficulty_map = {
            KeywordDifficulty.VERY_EASY: 0.2,
            KeywordDifficulty.EASY: 0.4,
            KeywordDifficulty.MEDIUM: 0.6,
            KeywordDifficulty.HARD: 0.8,
            KeywordDifficulty.VERY_HARD: 1.0
        }
        return difficulty_map.get(self.difficulty)
    
    @property
    def opportunity_score(self) -> float:
        """Calculate opportunity score based on volume, competition, and difficulty."""
        if not self.search_volume:
            return 0.0
        
        # Normalize search volume (log scale)
        import math
        volume_score = min(math.log10(self.search_volume + 1) / 6, 1.0)  # Max at 1M searches
        
        # Lower competition and difficulty = higher opportunity
        competition_score = 1.0 - (self.competition or 0.5)
        difficulty_score = 1.0 - (self.difficulty_score or 0.5)
        
        # Weighted average
        return (volume_score * 0.4 + competition_score * 0.3 + difficulty_score * 0.3)


class KeywordCluster(BaseModel):
    """Group of related keywords."""
    
    id: UUID = Field(default_factory=uuid4, description="Cluster identifier")
    name: str = Field(..., description="Cluster name/theme")
    primary_keyword: str = Field(..., description="Main keyword for this cluster")
    keywords: List[str] = Field(..., description="Keywords in this cluster")
    total_search_volume: int = Field(default=0, description="Combined search volume")
    avg_difficulty: Optional[float] = Field(None, description="Average difficulty score")
    dominant_intent: Optional[KeywordIntent] = Field(None, description="Most common intent in cluster")


class KeywordAnalysisResult(BaseModel):
    """Complete keyword analysis result."""
    
    id: UUID = Field(default_factory=uuid4, description="Analysis result identifier")
    campaign_id: UUID = Field(..., description="Associated campaign ID")
    
    # Input data
    seed_keywords: List[str] = Field(..., description="Original seed keywords")
    target_region: str = Field(..., description="Target region")
    target_language: str = Field(..., description="Target language")
    
    # Analysis results
    keyword_metrics: List[KeywordMetrics] = Field(default_factory=list, description="Detailed keyword metrics")
    keyword_clusters: List[KeywordCluster] = Field(default_factory=list, description="Keyword clusters")
    
    # Summary statistics
    total_keywords_analyzed: int = Field(default=0, description="Total keywords analyzed")
    high_opportunity_keywords: List[str] = Field(default_factory=list, description="Top opportunity keywords")
    recommended_keywords: List[str] = Field(default_factory=list, description="Recommended keywords to target")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Analysis timestamp")
    data_sources: List[str] = Field(default_factory=list, description="Data sources used")
    analysis_duration_seconds: Optional[float] = Field(None, description="Analysis duration")
    
    def get_keyword_metrics(self, keyword: str) -> Optional[KeywordMetrics]:
        """Get metrics for a specific keyword."""
        for metrics in self.keyword_metrics:
            if metrics.keyword.lower() == keyword.lower():
                return metrics
        return None
    
    def get_top_keywords_by_volume(self, limit: int = 10) -> List[KeywordMetrics]:
        """Get top keywords by search volume."""
        return sorted(
            [k for k in self.keyword_metrics if k.search_volume],
            key=lambda x: x.search_volume or 0,
            reverse=True
        )[:limit]
    
    def get_top_keywords_by_opportunity(self, limit: int = 10) -> List[KeywordMetrics]:
        """Get top keywords by opportunity score."""
        return sorted(
            self.keyword_metrics,
            key=lambda x: x.opportunity_score,
            reverse=True
        )[:limit]
    
    def get_keywords_by_intent(self, intent: KeywordIntent) -> List[KeywordMetrics]:
        """Get keywords filtered by search intent."""
        return [k for k in self.keyword_metrics if k.intent == intent]
    
    def get_keywords_by_difficulty(self, difficulty: KeywordDifficulty) -> List[KeywordMetrics]:
        """Get keywords filtered by difficulty level."""
        return [k for k in self.keyword_metrics if k.difficulty == difficulty]
    
    @property
    def summary_stats(self) -> Dict[str, any]:
        """Generate summary statistics."""
        if not self.keyword_metrics:
            return {}
        
        volumes = [k.search_volume for k in self.keyword_metrics if k.search_volume]
        difficulties = [k.difficulty_score for k in self.keyword_metrics if k.difficulty_score]
        
        return {
            "total_keywords": len(self.keyword_metrics),
            "avg_search_volume": sum(volumes) / len(volumes) if volumes else 0,
            "total_search_volume": sum(volumes) if volumes else 0,
            "avg_difficulty": sum(difficulties) / len(difficulties) if difficulties else 0,
            "intent_distribution": {
                intent.value: len(self.get_keywords_by_intent(intent))
                for intent in KeywordIntent
            },
            "difficulty_distribution": {
                difficulty.value: len(self.get_keywords_by_difficulty(difficulty))
                for difficulty in KeywordDifficulty
            }
        }
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }
