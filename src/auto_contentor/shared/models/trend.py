"""Trend analysis data models for AutoContentor."""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class TrendDirection(str, Enum):
    """Trend direction classification."""
    
    RISING = "rising"
    DECLINING = "declining"
    STABLE = "stable"
    VOLATILE = "volatile"


class TrendTimeframe(str, Enum):
    """Trend timeframe classification."""
    
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


class TrendSource(str, Enum):
    """Trend data source."""
    
    GOOGLE_TRENDS = "google_trends"
    TWITTER = "twitter"
    REDDIT = "reddit"
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    NEWS = "news"
    INDUSTRY_REPORTS = "industry_reports"


class TrendCategory(str, Enum):
    """Trend category classification."""
    
    TECHNOLOGY = "technology"
    MARKETING = "marketing"
    SOCIAL_MEDIA = "social_media"
    BUSINESS = "business"
    LIFESTYLE = "lifestyle"
    ENTERTAINMENT = "entertainment"
    HEALTH = "health"
    FINANCE = "finance"
    EDUCATION = "education"
    OTHER = "other"


class TrendDataPoint(BaseModel):
    """Individual trend data point."""
    
    date: datetime = Field(..., description="Data point date")
    value: float = Field(..., description="Trend value/score")
    volume: Optional[int] = Field(None, description="Search/mention volume", ge=0)
    normalized_value: Optional[float] = Field(None, description="Normalized value 0-100", ge=0, le=100)


class RelatedTopic(BaseModel):
    """Related topic or keyword."""
    
    topic: str = Field(..., description="Topic or keyword")
    relevance_score: float = Field(..., description="Relevance score 0-1", ge=0, le=1)
    growth_rate: Optional[float] = Field(None, description="Growth rate percentage")
    search_volume: Optional[int] = Field(None, description="Search volume", ge=0)


class TrendInsight(BaseModel):
    """Trend insight or observation."""
    
    title: str = Field(..., description="Insight title")
    description: str = Field(..., description="Insight description")
    confidence_score: float = Field(..., description="Confidence in insight", ge=0, le=1)
    impact_level: str = Field(..., description="Impact level: low, medium, high")
    actionable_recommendation: Optional[str] = Field(None, description="Actionable recommendation")


class Trend(BaseModel):
    """Individual trend analysis."""
    
    id: UUID = Field(default_factory=uuid4, description="Trend identifier")
    keyword: str = Field(..., description="Trend keyword or topic")
    category: TrendCategory = Field(..., description="Trend category")
    
    # Trend characteristics
    direction: TrendDirection = Field(..., description="Trend direction")
    timeframe: TrendTimeframe = Field(..., description="Analysis timeframe")
    current_score: float = Field(..., description="Current trend score", ge=0, le=100)
    peak_score: float = Field(..., description="Peak trend score", ge=0, le=100)
    growth_rate: Optional[float] = Field(None, description="Growth rate percentage")
    
    # Historical data
    data_points: List[TrendDataPoint] = Field(default_factory=list, description="Historical trend data")
    
    # Context and insights
    related_topics: List[RelatedTopic] = Field(default_factory=list, description="Related topics")
    insights: List[TrendInsight] = Field(default_factory=list, description="Trend insights")
    
    # Geographic data
    top_regions: List[str] = Field(default_factory=list, description="Top regions for this trend")
    regional_scores: Dict[str, float] = Field(default_factory=dict, description="Regional trend scores")
    
    # Metadata
    data_sources: List[TrendSource] = Field(default_factory=list, description="Data sources used")
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    confidence_score: float = Field(default=0.0, description="Overall confidence in trend data", ge=0, le=1)
    
    @property
    def is_trending_up(self) -> bool:
        """Check if trend is rising."""
        return self.direction == TrendDirection.RISING
    
    @property
    def is_trending_down(self) -> bool:
        """Check if trend is declining."""
        return self.direction == TrendDirection.DECLINING
    
    @property
    def momentum_score(self) -> float:
        """Calculate momentum score based on recent data points."""
        if len(self.data_points) < 2:
            return 0.0
        
        # Calculate momentum from last 5 data points
        recent_points = sorted(self.data_points, key=lambda x: x.date)[-5:]
        if len(recent_points) < 2:
            return 0.0
        
        # Simple momentum calculation
        start_value = recent_points[0].value
        end_value = recent_points[-1].value
        
        if start_value == 0:
            return 0.0
        
        return ((end_value - start_value) / start_value) * 100


class SeasonalPattern(BaseModel):
    """Seasonal trend pattern."""
    
    season: str = Field(..., description="Season name (e.g., 'Q1', 'Summer', 'Holiday')")
    months: List[int] = Field(..., description="Months included (1-12)")
    avg_score: float = Field(..., description="Average trend score for this season", ge=0, le=100)
    peak_month: int = Field(..., description="Peak month in season", ge=1, le=12)
    description: Optional[str] = Field(None, description="Pattern description")


class ContentOpportunity(BaseModel):
    """Content opportunity based on trends."""
    
    title: str = Field(..., description="Opportunity title")
    description: str = Field(..., description="Opportunity description")
    target_keywords: List[str] = Field(..., description="Target keywords")
    content_type: str = Field(..., description="Recommended content type")
    urgency_level: str = Field(..., description="Urgency level: low, medium, high")
    estimated_reach: Optional[int] = Field(None, description="Estimated potential reach", ge=0)
    competition_level: str = Field(default="medium", description="Competition level: low, medium, high")
    
    # Timing recommendations
    optimal_publish_date: Optional[datetime] = Field(None, description="Optimal publish date")
    content_lifespan: Optional[str] = Field(None, description="Expected content lifespan")


class TrendAnalysisResult(BaseModel):
    """Complete trend analysis result."""
    
    id: UUID = Field(default_factory=uuid4, description="Analysis result identifier")
    campaign_id: UUID = Field(..., description="Associated campaign ID")
    
    # Input data
    target_keywords: List[str] = Field(..., description="Keywords analyzed for trends")
    target_region: str = Field(..., description="Target region")
    analysis_period: str = Field(..., description="Analysis time period")
    
    # Analysis results
    trends: List[Trend] = Field(default_factory=list, description="Identified trends")
    seasonal_patterns: List[SeasonalPattern] = Field(default_factory=list, description="Seasonal patterns")
    content_opportunities: List[ContentOpportunity] = Field(default_factory=list, description="Content opportunities")
    
    # Summary insights
    top_rising_trends: List[str] = Field(default_factory=list, description="Top rising trends")
    declining_trends: List[str] = Field(default_factory=list, description="Declining trends")
    stable_trends: List[str] = Field(default_factory=list, description="Stable trends")
    
    # Strategic recommendations
    immediate_opportunities: List[str] = Field(default_factory=list, description="Immediate content opportunities")
    long_term_trends: List[str] = Field(default_factory=list, description="Long-term trends to watch")
    content_calendar_suggestions: List[str] = Field(default_factory=list, description="Content calendar suggestions")
    
    # Competitive insights
    competitor_trend_gaps: List[str] = Field(default_factory=list, description="Trends competitors are missing")
    oversaturated_trends: List[str] = Field(default_factory=list, description="Oversaturated trend topics")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Analysis timestamp")
    data_sources: List[TrendSource] = Field(default_factory=list, description="Data sources used")
    analysis_duration_seconds: Optional[float] = Field(None, description="Analysis duration")
    overall_confidence: float = Field(default=0.0, description="Overall confidence in analysis", ge=0, le=1)
    
    def get_trend_by_keyword(self, keyword: str) -> Optional[Trend]:
        """Get trend by keyword."""
        for trend in self.trends:
            if trend.keyword.lower() == keyword.lower():
                return trend
        return None
    
    def get_trends_by_category(self, category: TrendCategory) -> List[Trend]:
        """Get trends filtered by category."""
        return [t for t in self.trends if t.category == category]
    
    def get_trends_by_direction(self, direction: TrendDirection) -> List[Trend]:
        """Get trends filtered by direction."""
        return [t for t in self.trends if t.direction == direction]
    
    def get_high_opportunity_content(self, limit: int = 10) -> List[ContentOpportunity]:
        """Get high opportunity content suggestions."""
        return sorted(
            [c for c in self.content_opportunities if c.urgency_level == "high"],
            key=lambda x: x.estimated_reach or 0,
            reverse=True
        )[:limit]
    
    def get_trending_keywords(self, min_score: float = 50.0) -> List[str]:
        """Get keywords with high trend scores."""
        return [
            t.keyword for t in self.trends 
            if t.current_score >= min_score and t.is_trending_up
        ]
    
    @property
    def summary_stats(self) -> Dict[str, any]:
        """Generate summary statistics."""
        if not self.trends:
            return {}
        
        rising_count = len(self.get_trends_by_direction(TrendDirection.RISING))
        declining_count = len(self.get_trends_by_direction(TrendDirection.DECLINING))
        stable_count = len(self.get_trends_by_direction(TrendDirection.STABLE))
        
        avg_score = sum(t.current_score for t in self.trends) / len(self.trends)
        avg_confidence = sum(t.confidence_score for t in self.trends) / len(self.trends)
        
        return {
            "total_trends": len(self.trends),
            "rising_trends": rising_count,
            "declining_trends": declining_count,
            "stable_trends": stable_count,
            "avg_trend_score": avg_score,
            "avg_confidence": avg_confidence,
            "total_opportunities": len(self.content_opportunities),
            "high_urgency_opportunities": len([c for c in self.content_opportunities if c.urgency_level == "high"]),
            "seasonal_patterns": len(self.seasonal_patterns)
        }
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }
