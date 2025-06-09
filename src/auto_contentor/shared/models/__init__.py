"""Shared data models for AutoContentor."""

# Campaign models
from .campaign import (
    Campaign,
    CampaignPriority,
    CampaignRequest,
    CampaignStatus,
    CampaignSummary,
)

# Keyword models
from .keyword import (
    KeywordAnalysisResult,
    KeywordCluster,
    KeywordDifficulty,
    KeywordIntent,
    KeywordMetrics,
    KeywordTrend,
    RelatedKeyword,
)

# Audience models
from .audience import (
    AgeGroup,
    AudienceAnalysisResult,
    AudienceSegment,
    BuyerPersona,
    Demographics,
    Gender,
    Interest,
    PainPoint,
)

# Competitor models
from .competitor import (
    CompetitorAnalysisResult,
    CompetitorProfile,
    CompetitorTier,
    ContentPiece,
    ContentType,
    SocialMetrics,
    SWOTCategory,
    SWOTItem,
)

# Trend models
from .trend import (
    ContentOpportunity,
    RelatedTopic,
    SeasonalPattern,
    Trend,
    TrendAnalysisResult,
    TrendCategory,
    TrendDataPoint,
    TrendDirection,
    TrendInsight,
    TrendSource,
    TrendTimeframe,
)

# Report models
from .report import (
    ContentCalendarEntry,
    ContentRecommendation,
    FinalReport,
    ReportFormat,
    ReportMetadata,
    ReportSection,
    ReportStatus,
    StrategicInsight,
    ValidationResult,
)

__all__ = [
    # Campaign
    "Campaign",
    "CampaignPriority",
    "CampaignRequest",
    "CampaignStatus",
    "CampaignSummary",
    # Keyword
    "KeywordAnalysisResult",
    "KeywordCluster",
    "KeywordDifficulty",
    "KeywordIntent",
    "KeywordMetrics",
    "KeywordTrend",
    "RelatedKeyword",
    # Audience
    "AgeGroup",
    "AudienceAnalysisResult",
    "AudienceSegment",
    "BuyerPersona",
    "Demographics",
    "Gender",
    "Interest",
    "PainPoint",
    # Competitor
    "CompetitorAnalysisResult",
    "CompetitorProfile",
    "CompetitorTier",
    "ContentPiece",
    "ContentType",
    "SocialMetrics",
    "SWOTCategory",
    "SWOTItem",
    # Trend
    "ContentOpportunity",
    "RelatedTopic",
    "SeasonalPattern",
    "Trend",
    "TrendAnalysisResult",
    "TrendCategory",
    "TrendDataPoint",
    "TrendDirection",
    "TrendInsight",
    "TrendSource",
    "TrendTimeframe",
    # Report
    "ContentCalendarEntry",
    "ContentRecommendation",
    "FinalReport",
    "ReportFormat",
    "ReportMetadata",
    "ReportSection",
    "ReportStatus",
    "StrategicInsight",
    "ValidationResult",
]