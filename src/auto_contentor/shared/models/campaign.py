"""Campaign data models for AutoContentor."""

from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class CampaignStatus(str, Enum):
    """Campaign status enumeration."""
    
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class CampaignPriority(str, Enum):
    """Campaign priority levels."""
    
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class CampaignRequest(BaseModel):
    """Request model for creating a new campaign."""
    
    name: str = Field(..., description="Campaign name", min_length=1, max_length=255)
    description: Optional[str] = Field(None, description="Campaign description", max_length=1000)
    seed_keywords: List[str] = Field(..., description="Initial keywords to research", min_items=1)
    competitor_urls: List[str] = Field(default_factory=list, description="Competitor websites to analyze")
    target_region: str = Field(default="US", description="Target geographic region")
    target_language: str = Field(default="en", description="Target language code")
    industry: Optional[str] = Field(None, description="Industry or niche")
    priority: CampaignPriority = Field(default=CampaignPriority.MEDIUM, description="Campaign priority")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Q1 Content Strategy",
                "description": "Research for Q1 content marketing strategy",
                "seed_keywords": ["digital marketing", "content strategy", "SEO"],
                "competitor_urls": ["https://competitor1.com", "https://competitor2.com"],
                "target_region": "US",
                "target_language": "en",
                "industry": "Digital Marketing",
                "priority": "medium"
            }
        }


class Campaign(BaseModel):
    """Campaign data model."""
    
    id: UUID = Field(default_factory=uuid4, description="Unique campaign identifier")
    name: str = Field(..., description="Campaign name")
    description: Optional[str] = Field(None, description="Campaign description")
    seed_keywords: List[str] = Field(..., description="Initial keywords to research")
    competitor_urls: List[str] = Field(default_factory=list, description="Competitor websites")
    target_region: str = Field(default="US", description="Target geographic region")
    target_language: str = Field(default="en", description="Target language code")
    industry: Optional[str] = Field(None, description="Industry or niche")
    priority: CampaignPriority = Field(default=CampaignPriority.MEDIUM, description="Campaign priority")
    
    # Status and timing
    status: CampaignStatus = Field(default=CampaignStatus.PENDING, description="Campaign status")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    started_at: Optional[datetime] = Field(None, description="Start timestamp")
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp")
    
    # Progress tracking
    total_tasks: int = Field(default=4, description="Total number of tasks (agents)")
    completed_tasks: int = Field(default=0, description="Number of completed tasks")
    failed_tasks: int = Field(default=0, description="Number of failed tasks")
    
    # Results
    keyword_agent_result_id: Optional[str] = Field(None, description="Keyword analysis result ID")
    audience_agent_result_id: Optional[str] = Field(None, description="Audience analysis result ID")
    competitor_agent_result_id: Optional[str] = Field(None, description="Competitor analysis result ID")
    trend_agent_result_id: Optional[str] = Field(None, description="Trend analysis result ID")
    final_report_id: Optional[str] = Field(None, description="Final aggregated report ID")
    
    # Metadata
    created_by: Optional[str] = Field(None, description="User who created the campaign")
    tags: List[str] = Field(default_factory=list, description="Campaign tags")
    
    def update_status(self, new_status: CampaignStatus) -> None:
        """Update campaign status and timestamp."""
        self.status = new_status
        self.updated_at = datetime.utcnow()
        
        if new_status == CampaignStatus.RUNNING and not self.started_at:
            self.started_at = datetime.utcnow()
        elif new_status in [CampaignStatus.COMPLETED, CampaignStatus.FAILED, CampaignStatus.CANCELLED]:
            self.completed_at = datetime.utcnow()
    
    def increment_completed_tasks(self) -> None:
        """Increment completed tasks counter."""
        self.completed_tasks += 1
        self.updated_at = datetime.utcnow()
        
        # Auto-complete if all tasks are done
        if self.completed_tasks >= self.total_tasks:
            self.update_status(CampaignStatus.COMPLETED)
    
    def increment_failed_tasks(self) -> None:
        """Increment failed tasks counter."""
        self.failed_tasks += 1
        self.updated_at = datetime.utcnow()
        
        # Auto-fail if too many tasks failed
        if self.failed_tasks >= self.total_tasks // 2:  # Fail if more than half tasks failed
            self.update_status(CampaignStatus.FAILED)
    
    @property
    def progress_percentage(self) -> float:
        """Calculate completion percentage."""
        if self.total_tasks == 0:
            return 0.0
        return (self.completed_tasks / self.total_tasks) * 100.0
    
    @property
    def is_active(self) -> bool:
        """Check if campaign is currently active."""
        return self.status in [CampaignStatus.PENDING, CampaignStatus.RUNNING]
    
    @property
    def is_finished(self) -> bool:
        """Check if campaign is finished (completed, failed, or cancelled)."""
        return self.status in [CampaignStatus.COMPLETED, CampaignStatus.FAILED, CampaignStatus.CANCELLED]
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class CampaignSummary(BaseModel):
    """Lightweight campaign summary for listings."""
    
    id: UUID
    name: str
    status: CampaignStatus
    priority: CampaignPriority
    progress_percentage: float
    created_at: datetime
    updated_at: datetime
    seed_keywords_count: int
    competitor_urls_count: int
    
    @classmethod
    def from_campaign(cls, campaign: Campaign) -> "CampaignSummary":
        """Create summary from full campaign object."""
        return cls(
            id=campaign.id,
            name=campaign.name,
            status=campaign.status,
            priority=campaign.priority,
            progress_percentage=campaign.progress_percentage,
            created_at=campaign.created_at,
            updated_at=campaign.updated_at,
            seed_keywords_count=len(campaign.seed_keywords),
            competitor_urls_count=len(campaign.competitor_urls)
        )
