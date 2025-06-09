"""Competitor analysis data models for AutoContentor."""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class CompetitorTier(str, Enum):
    """Competitor tier classification."""
    
    DIRECT = "direct"  # Direct competitors
    INDIRECT = "indirect"  # Indirect competitors
    SUBSTITUTE = "substitute"  # Substitute products/services


class ContentType(str, Enum):
    """Content type classification."""
    
    BLOG_POST = "blog_post"
    VIDEO = "video"
    SOCIAL_POST = "social_post"
    INFOGRAPHIC = "infographic"
    PODCAST = "podcast"
    EBOOK = "ebook"
    WEBINAR = "webinar"
    CASE_STUDY = "case_study"


class SWOTCategory(str, Enum):
    """SWOT analysis categories."""
    
    STRENGTH = "strength"
    WEAKNESS = "weakness"
    OPPORTUNITY = "opportunity"
    THREAT = "threat"


class SocialMetrics(BaseModel):
    """Social media metrics for a competitor."""
    
    platform: str = Field(..., description="Social media platform")
    followers: Optional[int] = Field(None, description="Number of followers", ge=0)
    following: Optional[int] = Field(None, description="Number of following", ge=0)
    posts_count: Optional[int] = Field(None, description="Total posts", ge=0)
    avg_engagement_rate: Optional[float] = Field(None, description="Average engagement rate", ge=0, le=1)
    avg_likes: Optional[int] = Field(None, description="Average likes per post", ge=0)
    avg_comments: Optional[int] = Field(None, description="Average comments per post", ge=0)
    avg_shares: Optional[int] = Field(None, description="Average shares per post", ge=0)
    posting_frequency: Optional[str] = Field(None, description="Posting frequency pattern")


class ContentPiece(BaseModel):
    """Individual content piece analysis."""
    
    title: str = Field(..., description="Content title")
    url: Optional[str] = Field(None, description="Content URL")
    content_type: ContentType = Field(..., description="Type of content")
    publish_date: Optional[datetime] = Field(None, description="Publication date")
    
    # Performance metrics
    views: Optional[int] = Field(None, description="Number of views", ge=0)
    shares: Optional[int] = Field(None, description="Number of shares", ge=0)
    comments: Optional[int] = Field(None, description="Number of comments", ge=0)
    engagement_score: Optional[float] = Field(None, description="Overall engagement score", ge=0)
    
    # SEO metrics
    target_keywords: List[str] = Field(default_factory=list, description="Target keywords")
    search_ranking: Optional[int] = Field(None, description="Search ranking position", ge=1)
    backlinks: Optional[int] = Field(None, description="Number of backlinks", ge=0)
    
    # Content analysis
    word_count: Optional[int] = Field(None, description="Word count", ge=0)
    readability_score: Optional[float] = Field(None, description="Readability score", ge=0, le=100)
    sentiment_score: Optional[float] = Field(None, description="Sentiment score", ge=-1, le=1)
    topics: List[str] = Field(default_factory=list, description="Main topics covered")


class SWOTItem(BaseModel):
    """Individual SWOT analysis item."""
    
    category: SWOTCategory = Field(..., description="SWOT category")
    description: str = Field(..., description="Item description")
    impact_score: float = Field(..., description="Impact score 1-10", ge=1, le=10)
    evidence: List[str] = Field(default_factory=list, description="Supporting evidence")
    source: Optional[str] = Field(None, description="Data source")


class CompetitorProfile(BaseModel):
    """Comprehensive competitor profile."""
    
    id: UUID = Field(default_factory=uuid4, description="Competitor identifier")
    name: str = Field(..., description="Competitor name")
    website_url: str = Field(..., description="Main website URL")
    tier: CompetitorTier = Field(..., description="Competitor tier")
    
    # Basic info
    description: Optional[str] = Field(None, description="Company description")
    industry: Optional[str] = Field(None, description="Industry/niche")
    founded_year: Optional[int] = Field(None, description="Year founded", ge=1800)
    company_size: Optional[str] = Field(None, description="Company size category")
    headquarters: Optional[str] = Field(None, description="Headquarters location")
    
    # Digital presence
    domain_authority: Optional[float] = Field(None, description="Domain authority score", ge=0, le=100)
    monthly_traffic: Optional[int] = Field(None, description="Estimated monthly traffic", ge=0)
    top_keywords: List[str] = Field(default_factory=list, description="Top ranking keywords")
    social_metrics: List[SocialMetrics] = Field(default_factory=list, description="Social media metrics")
    
    # Content strategy
    content_pieces: List[ContentPiece] = Field(default_factory=list, description="Analyzed content pieces")
    content_themes: List[str] = Field(default_factory=list, description="Main content themes")
    posting_frequency: Dict[str, int] = Field(default_factory=dict, description="Posting frequency by platform")
    avg_content_performance: Dict[str, float] = Field(default_factory=dict, description="Average performance metrics")
    
    # SWOT analysis
    swot_items: List[SWOTItem] = Field(default_factory=list, description="SWOT analysis items")
    
    # Competitive metrics
    market_share: Optional[float] = Field(None, description="Estimated market share", ge=0, le=100)
    brand_mentions: Optional[int] = Field(None, description="Monthly brand mentions", ge=0)
    sentiment_score: Optional[float] = Field(None, description="Overall brand sentiment", ge=-1, le=1)
    
    def get_swot_by_category(self, category: SWOTCategory) -> List[SWOTItem]:
        """Get SWOT items by category."""
        return [item for item in self.swot_items if item.category == category]
    
    def get_top_content_by_engagement(self, limit: int = 10) -> List[ContentPiece]:
        """Get top content pieces by engagement."""
        return sorted(
            [c for c in self.content_pieces if c.engagement_score],
            key=lambda x: x.engagement_score or 0,
            reverse=True
        )[:limit]
    
    def get_social_metrics_by_platform(self, platform: str) -> Optional[SocialMetrics]:
        """Get social metrics for specific platform."""
        for metrics in self.social_metrics:
            if metrics.platform.lower() == platform.lower():
                return metrics
        return None
    
    @property
    def strengths(self) -> List[SWOTItem]:
        """Get strengths from SWOT analysis."""
        return self.get_swot_by_category(SWOTCategory.STRENGTH)
    
    @property
    def weaknesses(self) -> List[SWOTItem]:
        """Get weaknesses from SWOT analysis."""
        return self.get_swot_by_category(SWOTCategory.WEAKNESS)
    
    @property
    def opportunities(self) -> List[SWOTItem]:
        """Get opportunities from SWOT analysis."""
        return self.get_swot_by_category(SWOTCategory.OPPORTUNITY)
    
    @property
    def threats(self) -> List[SWOTItem]:
        """Get threats from SWOT analysis."""
        return self.get_swot_by_category(SWOTCategory.THREAT)


class CompetitorAnalysisResult(BaseModel):
    """Complete competitor analysis result."""
    
    id: UUID = Field(default_factory=uuid4, description="Analysis result identifier")
    campaign_id: UUID = Field(..., description="Associated campaign ID")
    
    # Input data
    competitor_urls: List[str] = Field(..., description="Competitor URLs analyzed")
    target_keywords: List[str] = Field(..., description="Keywords used for analysis")
    analysis_scope: List[str] = Field(default_factory=list, description="Scope of analysis")
    
    # Analysis results
    competitor_profiles: List[CompetitorProfile] = Field(default_factory=list, description="Detailed competitor profiles")
    
    # Competitive landscape insights
    market_leaders: List[str] = Field(default_factory=list, description="Identified market leaders")
    content_gaps: List[str] = Field(default_factory=list, description="Identified content gaps")
    keyword_opportunities: List[str] = Field(default_factory=list, description="Keyword opportunities")
    
    # Strategic insights
    common_strengths: List[str] = Field(default_factory=list, description="Common competitor strengths")
    common_weaknesses: List[str] = Field(default_factory=list, description="Common competitor weaknesses")
    market_opportunities: List[str] = Field(default_factory=list, description="Market opportunities")
    competitive_threats: List[str] = Field(default_factory=list, description="Competitive threats")
    
    # Content strategy insights
    trending_content_types: List[str] = Field(default_factory=list, description="Trending content types")
    optimal_content_length: Dict[str, int] = Field(default_factory=dict, description="Optimal content length by type")
    best_performing_topics: List[str] = Field(default_factory=list, description="Best performing topics")
    content_frequency_recommendations: Dict[str, str] = Field(default_factory=dict, description="Recommended posting frequency")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Analysis timestamp")
    data_sources: List[str] = Field(default_factory=list, description="Data sources used")
    analysis_duration_seconds: Optional[float] = Field(None, description="Analysis duration")
    
    def get_competitor_by_name(self, name: str) -> Optional[CompetitorProfile]:
        """Get competitor profile by name."""
        for competitor in self.competitor_profiles:
            if competitor.name.lower() == name.lower():
                return competitor
        return None
    
    def get_competitors_by_tier(self, tier: CompetitorTier) -> List[CompetitorProfile]:
        """Get competitors filtered by tier."""
        return [c for c in self.competitor_profiles if c.tier == tier]
    
    def get_top_competitors_by_traffic(self, limit: int = 5) -> List[CompetitorProfile]:
        """Get top competitors by monthly traffic."""
        return sorted(
            [c for c in self.competitor_profiles if c.monthly_traffic],
            key=lambda x: x.monthly_traffic or 0,
            reverse=True
        )[:limit]
    
    @property
    def summary_stats(self) -> Dict[str, any]:
        """Generate summary statistics."""
        if not self.competitor_profiles:
            return {}
        
        traffic_data = [c.monthly_traffic for c in self.competitor_profiles if c.monthly_traffic]
        da_data = [c.domain_authority for c in self.competitor_profiles if c.domain_authority]
        
        return {
            "total_competitors": len(self.competitor_profiles),
            "direct_competitors": len(self.get_competitors_by_tier(CompetitorTier.DIRECT)),
            "indirect_competitors": len(self.get_competitors_by_tier(CompetitorTier.INDIRECT)),
            "avg_monthly_traffic": sum(traffic_data) / len(traffic_data) if traffic_data else 0,
            "avg_domain_authority": sum(da_data) / len(da_data) if da_data else 0,
            "total_content_pieces": sum(len(c.content_pieces) for c in self.competitor_profiles),
            "total_swot_items": sum(len(c.swot_items) for c in self.competitor_profiles)
        }
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }
