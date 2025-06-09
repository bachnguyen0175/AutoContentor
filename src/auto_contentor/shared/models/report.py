"""Report generation data models for AutoContentor."""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ReportFormat(str, Enum):
    """Report output format."""
    
    PDF = "pdf"
    HTML = "html"
    JSON = "json"
    MARKDOWN = "markdown"


class ReportStatus(str, Enum):
    """Report generation status."""
    
    PENDING = "pending"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


class ReportSection(str, Enum):
    """Report section types."""
    
    EXECUTIVE_SUMMARY = "executive_summary"
    KEYWORD_ANALYSIS = "keyword_analysis"
    AUDIENCE_ANALYSIS = "audience_analysis"
    COMPETITOR_ANALYSIS = "competitor_analysis"
    TREND_ANALYSIS = "trend_analysis"
    STRATEGIC_RECOMMENDATIONS = "strategic_recommendations"
    CONTENT_CALENDAR = "content_calendar"
    APPENDIX = "appendix"


class ContentRecommendation(BaseModel):
    """Individual content recommendation."""
    
    title: str = Field(..., description="Content title")
    content_type: str = Field(..., description="Content type (blog, video, etc.)")
    target_keywords: List[str] = Field(..., description="Target keywords")
    target_audience: str = Field(..., description="Target audience segment")
    priority: str = Field(..., description="Priority level: low, medium, high")
    estimated_effort: str = Field(..., description="Estimated effort: low, medium, high")
    expected_impact: str = Field(..., description="Expected impact: low, medium, high")
    optimal_timing: Optional[str] = Field(None, description="Optimal publishing timing")
    distribution_channels: List[str] = Field(default_factory=list, description="Recommended distribution channels")
    success_metrics: List[str] = Field(default_factory=list, description="Success metrics to track")


class StrategicInsight(BaseModel):
    """Strategic insight or recommendation."""
    
    category: str = Field(..., description="Insight category")
    title: str = Field(..., description="Insight title")
    description: str = Field(..., description="Detailed description")
    impact_level: str = Field(..., description="Impact level: low, medium, high")
    implementation_difficulty: str = Field(..., description="Implementation difficulty: easy, medium, hard")
    timeline: str = Field(..., description="Recommended timeline")
    success_indicators: List[str] = Field(default_factory=list, description="Success indicators")
    action_items: List[str] = Field(default_factory=list, description="Specific action items")


class ContentCalendarEntry(BaseModel):
    """Content calendar entry."""
    
    date: datetime = Field(..., description="Scheduled date")
    content_title: str = Field(..., description="Content title")
    content_type: str = Field(..., description="Content type")
    target_keywords: List[str] = Field(..., description="Target keywords")
    target_audience: str = Field(..., description="Target audience")
    platform: str = Field(..., description="Publishing platform")
    status: str = Field(default="planned", description="Content status")
    notes: Optional[str] = Field(None, description="Additional notes")


class ValidationResult(BaseModel):
    """Data validation result."""
    
    section: ReportSection = Field(..., description="Report section")
    is_valid: bool = Field(..., description="Validation status")
    quality_score: float = Field(..., description="Quality score 0-1", ge=0, le=1)
    issues: List[str] = Field(default_factory=list, description="Validation issues found")
    recommendations: List[str] = Field(default_factory=list, description="Improvement recommendations")


class ReportMetadata(BaseModel):
    """Report metadata and generation info."""
    
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Generation timestamp")
    generated_by: str = Field(default="AutoContentor", description="Generator system")
    version: str = Field(default="1.0", description="Report version")
    template_version: str = Field(default="1.0", description="Template version")
    generation_duration_seconds: Optional[float] = Field(None, description="Generation duration")
    data_freshness: Dict[str, datetime] = Field(default_factory=dict, description="Data freshness by source")
    total_pages: Optional[int] = Field(None, description="Total pages in report", ge=1)
    file_size_bytes: Optional[int] = Field(None, description="File size in bytes", ge=0)


class FinalReport(BaseModel):
    """Complete final report."""
    
    id: UUID = Field(default_factory=uuid4, description="Report identifier")
    campaign_id: UUID = Field(..., description="Associated campaign ID")
    
    # Report configuration
    title: str = Field(..., description="Report title")
    format: ReportFormat = Field(default=ReportFormat.PDF, description="Report format")
    status: ReportStatus = Field(default=ReportStatus.PENDING, description="Report status")
    
    # Input data references
    keyword_analysis_id: Optional[UUID] = Field(None, description="Keyword analysis result ID")
    audience_analysis_id: Optional[UUID] = Field(None, description="Audience analysis result ID")
    competitor_analysis_id: Optional[UUID] = Field(None, description="Competitor analysis result ID")
    trend_analysis_id: Optional[UUID] = Field(None, description="Trend analysis result ID")
    
    # Executive Summary
    executive_summary: str = Field(default="", description="Executive summary")
    key_findings: List[str] = Field(default_factory=list, description="Key findings")
    critical_insights: List[str] = Field(default_factory=list, description="Critical insights")
    
    # Strategic Recommendations
    strategic_insights: List[StrategicInsight] = Field(default_factory=list, description="Strategic insights")
    content_recommendations: List[ContentRecommendation] = Field(default_factory=list, description="Content recommendations")
    
    # Content Strategy
    content_calendar: List[ContentCalendarEntry] = Field(default_factory=list, description="Content calendar")
    content_themes: List[str] = Field(default_factory=list, description="Recommended content themes")
    content_distribution_strategy: Dict[str, str] = Field(default_factory=dict, description="Distribution strategy by platform")
    
    # Performance Projections
    projected_metrics: Dict[str, float] = Field(default_factory=dict, description="Projected performance metrics")
    success_kpis: List[str] = Field(default_factory=list, description="Success KPIs to track")
    
    # Quality Assurance
    validation_results: List[ValidationResult] = Field(default_factory=list, description="Validation results")
    overall_quality_score: float = Field(default=0.0, description="Overall report quality score", ge=0, le=1)
    
    # File information
    file_path: Optional[str] = Field(None, description="Generated file path")
    file_url: Optional[str] = Field(None, description="File download URL")
    
    # Metadata
    metadata: ReportMetadata = Field(default_factory=ReportMetadata, description="Report metadata")
    
    def add_strategic_insight(self, insight: StrategicInsight) -> None:
        """Add a strategic insight to the report."""
        self.strategic_insights.append(insight)
    
    def add_content_recommendation(self, recommendation: ContentRecommendation) -> None:
        """Add a content recommendation to the report."""
        self.content_recommendations.append(recommendation)
    
    def add_calendar_entry(self, entry: ContentCalendarEntry) -> None:
        """Add an entry to the content calendar."""
        self.content_calendar.append(entry)
    
    def get_high_priority_recommendations(self) -> List[ContentRecommendation]:
        """Get high priority content recommendations."""
        return [r for r in self.content_recommendations if r.priority == "high"]
    
    def get_recommendations_by_type(self, content_type: str) -> List[ContentRecommendation]:
        """Get recommendations filtered by content type."""
        return [r for r in self.content_recommendations if r.content_type.lower() == content_type.lower()]
    
    def get_calendar_entries_by_month(self, year: int, month: int) -> List[ContentCalendarEntry]:
        """Get calendar entries for a specific month."""
        return [
            entry for entry in self.content_calendar
            if entry.date.year == year and entry.date.month == month
        ]
    
    def update_status(self, new_status: ReportStatus) -> None:
        """Update report status."""
        self.status = new_status
        if new_status == ReportStatus.COMPLETED:
            self.metadata.generated_at = datetime.utcnow()
    
    def calculate_quality_score(self) -> float:
        """Calculate overall quality score based on validation results."""
        if not self.validation_results:
            return 0.0
        
        valid_sections = sum(1 for v in self.validation_results if v.is_valid)
        total_sections = len(self.validation_results)
        
        if total_sections == 0:
            return 0.0
        
        # Base score from validation
        validation_score = valid_sections / total_sections
        
        # Quality score from individual sections
        avg_quality = sum(v.quality_score for v in self.validation_results) / total_sections
        
        # Combined score
        self.overall_quality_score = (validation_score * 0.6 + avg_quality * 0.4)
        return self.overall_quality_score
    
    @property
    def is_complete(self) -> bool:
        """Check if report is complete."""
        return self.status == ReportStatus.COMPLETED
    
    @property
    def has_high_quality(self) -> bool:
        """Check if report meets high quality standards."""
        return self.overall_quality_score >= 0.8
    
    @property
    def summary_stats(self) -> Dict[str, any]:
        """Generate summary statistics."""
        return {
            "total_insights": len(self.strategic_insights),
            "total_recommendations": len(self.content_recommendations),
            "high_priority_recommendations": len(self.get_high_priority_recommendations()),
            "calendar_entries": len(self.content_calendar),
            "quality_score": self.overall_quality_score,
            "validation_passed": sum(1 for v in self.validation_results if v.is_valid),
            "total_validations": len(self.validation_results),
            "key_findings_count": len(self.key_findings),
            "content_themes_count": len(self.content_themes)
        }
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }
