"""Validation utilities for AutoContentor."""

import re
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse

from pydantic import ValidationError

from ..config.constants import SUPPORTED_LANGUAGES, SUPPORTED_REGIONS, VALIDATION_RULES
from ..models import Campaign, CampaignRequest
from .logger import get_logger

logger = get_logger(__name__)


class ValidationResult:
    """Result of a validation operation."""
    
    def __init__(self, is_valid: bool = True, errors: List[str] = None, warnings: List[str] = None):
        self.is_valid = is_valid
        self.errors = errors or []
        self.warnings = warnings or []
    
    def add_error(self, error: str) -> None:
        """Add an error message."""
        self.errors.append(error)
        self.is_valid = False
    
    def add_warning(self, warning: str) -> None:
        """Add a warning message."""
        self.warnings.append(warning)
    
    def merge(self, other: "ValidationResult") -> None:
        """Merge another validation result."""
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)
        if not other.is_valid:
            self.is_valid = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "is_valid": self.is_valid,
            "errors": self.errors,
            "warnings": self.warnings
        }


class CampaignValidator:
    """Validator for campaign data."""
    
    @staticmethod
    def validate_campaign_request(request: CampaignRequest) -> ValidationResult:
        """Validate campaign request."""
        result = ValidationResult()
        
        # Validate name
        if not request.name or len(request.name.strip()) == 0:
            result.add_error("Campaign name is required")
        elif len(request.name) > VALIDATION_RULES["MAX_CAMPAIGN_NAME_LENGTH"]:
            result.add_error(f"Campaign name must be less than {VALIDATION_RULES['MAX_CAMPAIGN_NAME_LENGTH']} characters")
        
        # Validate description
        if request.description and len(request.description) > VALIDATION_RULES["MAX_DESCRIPTION_LENGTH"]:
            result.add_error(f"Description must be less than {VALIDATION_RULES['MAX_DESCRIPTION_LENGTH']} characters")
        
        # Validate keywords
        if not request.seed_keywords:
            result.add_error("At least one seed keyword is required")
        elif len(request.seed_keywords) < VALIDATION_RULES["MIN_KEYWORDS"]:
            result.add_error(f"At least {VALIDATION_RULES['MIN_KEYWORDS']} keyword is required")
        elif len(request.seed_keywords) > VALIDATION_RULES["MAX_KEYWORDS"]:
            result.add_error(f"Maximum {VALIDATION_RULES['MAX_KEYWORDS']} keywords allowed")
        
        # Validate keyword content
        for keyword in request.seed_keywords:
            if not keyword or len(keyword.strip()) == 0:
                result.add_error("Empty keywords are not allowed")
            elif len(keyword) > 100:
                result.add_error(f"Keyword '{keyword}' is too long (max 100 characters)")
        
        # Validate competitor URLs
        if len(request.competitor_urls) > VALIDATION_RULES["MAX_COMPETITORS"]:
            result.add_error(f"Maximum {VALIDATION_RULES['MAX_COMPETITORS']} competitor URLs allowed")
        
        for url in request.competitor_urls:
            if not URLValidator.is_valid_url(url):
                result.add_error(f"Invalid competitor URL: {url}")
        
        # Validate region
        if request.target_region not in SUPPORTED_REGIONS:
            result.add_warning(f"Unsupported region: {request.target_region}")
        
        # Validate language
        if request.target_language not in SUPPORTED_LANGUAGES:
            result.add_warning(f"Unsupported language: {request.target_language}")
        
        return result
    
    @staticmethod
    def validate_campaign(campaign: Campaign) -> ValidationResult:
        """Validate campaign object."""
        result = ValidationResult()
        
        # Basic validation
        try:
            # This will raise ValidationError if the model is invalid
            campaign.dict()
        except ValidationError as e:
            for error in e.errors():
                result.add_error(f"Field {error['loc']}: {error['msg']}")
        
        # Business logic validation
        if campaign.completed_tasks > campaign.total_tasks:
            result.add_error("Completed tasks cannot exceed total tasks")
        
        if campaign.failed_tasks > campaign.total_tasks:
            result.add_error("Failed tasks cannot exceed total tasks")
        
        return result


class URLValidator:
    """Validator for URLs."""
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if URL is valid."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    @staticmethod
    def is_valid_domain(domain: str) -> bool:
        """Check if domain is valid."""
        domain_pattern = re.compile(
            r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$'
        )
        return bool(domain_pattern.match(domain))
    
    @staticmethod
    def validate_urls(urls: List[str]) -> ValidationResult:
        """Validate a list of URLs."""
        result = ValidationResult()
        
        for url in urls:
            if not URLValidator.is_valid_url(url):
                result.add_error(f"Invalid URL: {url}")
        
        return result


class KeywordValidator:
    """Validator for keywords."""
    
    @staticmethod
    def is_valid_keyword(keyword: str) -> bool:
        """Check if keyword is valid."""
        if not keyword or len(keyword.strip()) == 0:
            return False
        
        # Check length
        if len(keyword) > 100:
            return False
        
        # Check for invalid characters (basic check)
        if re.search(r'[<>{}[\]\\]', keyword):
            return False
        
        return True
    
    @staticmethod
    def validate_keywords(keywords: List[str]) -> ValidationResult:
        """Validate a list of keywords."""
        result = ValidationResult()
        
        if not keywords:
            result.add_error("Keywords list cannot be empty")
            return result
        
        # Check for duplicates
        unique_keywords = set()
        for keyword in keywords:
            normalized = keyword.lower().strip()
            if normalized in unique_keywords:
                result.add_warning(f"Duplicate keyword: {keyword}")
            unique_keywords.add(normalized)
        
        # Validate individual keywords
        for keyword in keywords:
            if not KeywordValidator.is_valid_keyword(keyword):
                result.add_error(f"Invalid keyword: {keyword}")
        
        return result


class DataQualityValidator:
    """Validator for data quality."""
    
    @staticmethod
    def validate_confidence_score(score: float) -> ValidationResult:
        """Validate confidence score."""
        result = ValidationResult()
        
        if not 0 <= score <= 1:
            result.add_error(f"Confidence score must be between 0 and 1, got {score}")
        elif score < 0.6:
            result.add_warning(f"Low confidence score: {score}")
        
        return result
    
    @staticmethod
    def validate_search_volume(volume: Optional[int]) -> ValidationResult:
        """Validate search volume."""
        result = ValidationResult()
        
        if volume is not None:
            if volume < 0:
                result.add_error(f"Search volume cannot be negative: {volume}")
            elif volume == 0:
                result.add_warning("Search volume is zero")
        
        return result
    
    @staticmethod
    def validate_percentage(value: float, field_name: str) -> ValidationResult:
        """Validate percentage value."""
        result = ValidationResult()
        
        if not 0 <= value <= 100:
            result.add_error(f"{field_name} must be between 0 and 100, got {value}")
        
        return result


class APIKeyValidator:
    """Validator for API keys."""
    
    @staticmethod
    def validate_api_key(api_key: Optional[str], api_name: str) -> ValidationResult:
        """Validate API key format."""
        result = ValidationResult()
        
        if not api_key:
            result.add_warning(f"No API key provided for {api_name}")
            return result
        
        # Basic format validation
        if len(api_key) < 10:
            result.add_error(f"API key for {api_name} appears to be too short")
        elif len(api_key) > 200:
            result.add_error(f"API key for {api_name} appears to be too long")
        
        # Check for common patterns
        if api_key.startswith('sk-') and api_name.lower() == 'openai':
            # OpenAI key format
            if len(api_key) != 51:
                result.add_warning(f"OpenAI API key may have incorrect length")
        
        return result


class ContentValidator:
    """Validator for content data."""
    
    @staticmethod
    def validate_content_length(content: str, min_length: int = 10, max_length: int = 10000) -> ValidationResult:
        """Validate content length."""
        result = ValidationResult()
        
        if len(content) < min_length:
            result.add_error(f"Content too short (minimum {min_length} characters)")
        elif len(content) > max_length:
            result.add_error(f"Content too long (maximum {max_length} characters)")
        
        return result
    
    @staticmethod
    def validate_html_content(html: str) -> ValidationResult:
        """Basic HTML content validation."""
        result = ValidationResult()
        
        # Check for balanced tags (basic check)
        open_tags = re.findall(r'<([^/][^>]*)>', html)
        close_tags = re.findall(r'</([^>]+)>', html)
        
        # Extract tag names
        open_tag_names = [tag.split()[0] for tag in open_tags]
        close_tag_names = close_tags
        
        # Check for unmatched tags
        for tag in open_tag_names:
            if tag not in ['br', 'hr', 'img', 'input', 'meta', 'link']:  # Self-closing tags
                if tag not in close_tag_names:
                    result.add_warning(f"Unmatched opening tag: {tag}")
        
        return result


def validate_model_data(model_instance: Any) -> ValidationResult:
    """Validate Pydantic model instance."""
    result = ValidationResult()
    
    try:
        # This will trigger validation
        model_instance.dict()
    except ValidationError as e:
        for error in e.errors():
            field_path = " -> ".join(str(loc) for loc in error['loc'])
            result.add_error(f"Field '{field_path}': {error['msg']}")
    except Exception as e:
        result.add_error(f"Validation error: {str(e)}")
    
    return result


def validate_json_data(data: Dict[str, Any], required_fields: List[str] = None) -> ValidationResult:
    """Validate JSON data structure."""
    result = ValidationResult()
    
    if required_fields:
        for field in required_fields:
            if field not in data:
                result.add_error(f"Required field missing: {field}")
            elif data[field] is None:
                result.add_error(f"Required field cannot be null: {field}")
    
    return result
