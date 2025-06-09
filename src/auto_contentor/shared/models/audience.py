"""Audience research data models for AutoContentor."""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class AgeGroup(str, Enum):
    """Age group classifications."""
    
    GEN_Z = "gen_z"  # 18-24
    MILLENNIAL = "millennial"  # 25-40
    GEN_X = "gen_x"  # 41-56
    BOOMER = "boomer"  # 57+


class Gender(str, Enum):
    """Gender classifications."""
    
    MALE = "male"
    FEMALE = "female"
    NON_BINARY = "non_binary"
    OTHER = "other"


class IncomeLevel(str, Enum):
    """Income level classifications."""
    
    LOW = "low"  # <$30k
    LOWER_MIDDLE = "lower_middle"  # $30k-$50k
    MIDDLE = "middle"  # $50k-$80k
    UPPER_MIDDLE = "upper_middle"  # $80k-$120k
    HIGH = "high"  # $120k+


class EducationLevel(str, Enum):
    """Education level classifications."""
    
    HIGH_SCHOOL = "high_school"
    SOME_COLLEGE = "some_college"
    BACHELORS = "bachelors"
    MASTERS = "masters"
    DOCTORATE = "doctorate"


class Demographics(BaseModel):
    """Demographic information for audience segment."""
    
    age_groups: Dict[AgeGroup, float] = Field(default_factory=dict, description="Age group distribution (percentages)")
    gender_distribution: Dict[Gender, float] = Field(default_factory=dict, description="Gender distribution (percentages)")
    income_levels: Dict[IncomeLevel, float] = Field(default_factory=dict, description="Income level distribution (percentages)")
    education_levels: Dict[EducationLevel, float] = Field(default_factory=dict, description="Education level distribution (percentages)")
    
    # Geographic data
    top_countries: List[str] = Field(default_factory=list, description="Top countries by audience")
    top_cities: List[str] = Field(default_factory=list, description="Top cities by audience")
    urban_vs_rural: Dict[str, float] = Field(default_factory=dict, description="Urban vs rural distribution")
    
    @property
    def dominant_age_group(self) -> Optional[AgeGroup]:
        """Get the dominant age group."""
        if not self.age_groups:
            return None
        return max(self.age_groups.items(), key=lambda x: x[1])[0]
    
    @property
    def dominant_gender(self) -> Optional[Gender]:
        """Get the dominant gender."""
        if not self.gender_distribution:
            return None
        return max(self.gender_distribution.items(), key=lambda x: x[1])[0]


class Interest(BaseModel):
    """Interest or hobby category."""
    
    name: str = Field(..., description="Interest name")
    category: str = Field(..., description="Interest category")
    relevance_score: float = Field(..., description="Relevance score 0-1", ge=0, le=1)
    engagement_level: str = Field(..., description="Engagement level: low, medium, high")


class PainPoint(BaseModel):
    """Audience pain point or challenge."""
    
    description: str = Field(..., description="Pain point description")
    severity: str = Field(..., description="Severity level: low, medium, high")
    frequency: str = Field(..., description="How often this occurs: rare, occasional, frequent")
    category: str = Field(..., description="Pain point category")


class ContentPreference(BaseModel):
    """Content consumption preferences."""
    
    content_types: Dict[str, float] = Field(default_factory=dict, description="Preferred content types with scores")
    content_lengths: Dict[str, float] = Field(default_factory=dict, description="Preferred content lengths")
    platforms: Dict[str, float] = Field(default_factory=dict, description="Preferred platforms with engagement scores")
    posting_times: Dict[str, float] = Field(default_factory=dict, description="Best posting times")
    content_themes: List[str] = Field(default_factory=list, description="Popular content themes")


class BuyerPersona(BaseModel):
    """Detailed buyer persona."""
    
    id: UUID = Field(default_factory=uuid4, description="Persona identifier")
    name: str = Field(..., description="Persona name")
    description: str = Field(..., description="Persona description")
    
    # Core demographics
    demographics: Demographics = Field(default_factory=Demographics, description="Demographic information")
    
    # Psychographics
    interests: List[Interest] = Field(default_factory=list, description="Interests and hobbies")
    values: List[str] = Field(default_factory=list, description="Core values")
    lifestyle: List[str] = Field(default_factory=list, description="Lifestyle characteristics")
    personality_traits: List[str] = Field(default_factory=list, description="Personality traits")
    
    # Behavioral data
    pain_points: List[PainPoint] = Field(default_factory=list, description="Pain points and challenges")
    goals: List[str] = Field(default_factory=list, description="Goals and aspirations")
    motivations: List[str] = Field(default_factory=list, description="Key motivations")
    
    # Content preferences
    content_preferences: ContentPreference = Field(default_factory=ContentPreference, description="Content preferences")
    
    # Buying behavior
    buying_triggers: List[str] = Field(default_factory=list, description="What triggers purchase decisions")
    decision_factors: List[str] = Field(default_factory=list, description="Key decision factors")
    purchase_journey_stages: Dict[str, str] = Field(default_factory=dict, description="Behavior at each journey stage")
    
    # Communication preferences
    preferred_channels: List[str] = Field(default_factory=list, description="Preferred communication channels")
    communication_style: str = Field(default="", description="Preferred communication style")
    
    # Metadata
    confidence_score: float = Field(default=0.0, description="Confidence in persona accuracy", ge=0, le=1)
    data_sources: List[str] = Field(default_factory=list, description="Data sources used to build persona")
    
    @property
    def primary_age_group(self) -> Optional[str]:
        """Get primary age group as string."""
        dominant = self.demographics.dominant_age_group
        return dominant.value if dominant else None
    
    @property
    def primary_gender(self) -> Optional[str]:
        """Get primary gender as string."""
        dominant = self.demographics.dominant_gender
        return dominant.value if dominant else None


class AudienceSegment(BaseModel):
    """Audience segment with shared characteristics."""
    
    id: UUID = Field(default_factory=uuid4, description="Segment identifier")
    name: str = Field(..., description="Segment name")
    description: str = Field(..., description="Segment description")
    size_percentage: float = Field(..., description="Percentage of total audience", ge=0, le=100)
    
    # Segment characteristics
    defining_characteristics: List[str] = Field(default_factory=list, description="Key defining characteristics")
    demographics: Demographics = Field(default_factory=Demographics, description="Segment demographics")
    interests: List[Interest] = Field(default_factory=list, description="Common interests")
    pain_points: List[PainPoint] = Field(default_factory=list, description="Common pain points")
    
    # Engagement metrics
    engagement_rate: Optional[float] = Field(None, description="Average engagement rate", ge=0, le=1)
    conversion_rate: Optional[float] = Field(None, description="Average conversion rate", ge=0, le=1)
    lifetime_value: Optional[float] = Field(None, description="Average customer lifetime value", ge=0)


class AudienceAnalysisResult(BaseModel):
    """Complete audience analysis result."""
    
    id: UUID = Field(default_factory=uuid4, description="Analysis result identifier")
    campaign_id: UUID = Field(..., description="Associated campaign ID")
    
    # Input data
    target_keywords: List[str] = Field(..., description="Keywords used for audience research")
    target_region: str = Field(..., description="Target region")
    competitor_urls: List[str] = Field(default_factory=list, description="Competitor URLs analyzed")
    
    # Analysis results
    buyer_personas: List[BuyerPersona] = Field(default_factory=list, description="Identified buyer personas")
    audience_segments: List[AudienceSegment] = Field(default_factory=list, description="Audience segments")
    
    # Overall insights
    total_addressable_audience: Optional[int] = Field(None, description="Estimated total audience size")
    primary_demographics: Demographics = Field(default_factory=Demographics, description="Overall demographics")
    top_interests: List[Interest] = Field(default_factory=list, description="Top interests across all segments")
    common_pain_points: List[PainPoint] = Field(default_factory=list, description="Most common pain points")
    
    # Content strategy insights
    recommended_content_types: List[str] = Field(default_factory=list, description="Recommended content types")
    optimal_posting_times: Dict[str, str] = Field(default_factory=dict, description="Optimal posting times by platform")
    key_messaging_themes: List[str] = Field(default_factory=list, description="Key messaging themes")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Analysis timestamp")
    data_sources: List[str] = Field(default_factory=list, description="Data sources used")
    analysis_duration_seconds: Optional[float] = Field(None, description="Analysis duration")
    confidence_score: float = Field(default=0.0, description="Overall confidence in analysis", ge=0, le=1)
    
    def get_persona_by_name(self, name: str) -> Optional[BuyerPersona]:
        """Get persona by name."""
        for persona in self.buyer_personas:
            if persona.name.lower() == name.lower():
                return persona
        return None
    
    def get_primary_persona(self) -> Optional[BuyerPersona]:
        """Get the primary (highest confidence) persona."""
        if not self.buyer_personas:
            return None
        return max(self.buyer_personas, key=lambda x: x.confidence_score)
    
    def get_largest_segment(self) -> Optional[AudienceSegment]:
        """Get the largest audience segment."""
        if not self.audience_segments:
            return None
        return max(self.audience_segments, key=lambda x: x.size_percentage)
    
    @property
    def summary_stats(self) -> Dict[str, any]:
        """Generate summary statistics."""
        return {
            "total_personas": len(self.buyer_personas),
            "total_segments": len(self.audience_segments),
            "avg_persona_confidence": sum(p.confidence_score for p in self.buyer_personas) / len(self.buyer_personas) if self.buyer_personas else 0,
            "primary_age_group": self.primary_demographics.dominant_age_group.value if self.primary_demographics.dominant_age_group else None,
            "primary_gender": self.primary_demographics.dominant_gender.value if self.primary_demographics.dominant_gender else None,
            "total_interests": len(self.top_interests),
            "total_pain_points": len(self.common_pain_points)
        }
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }
