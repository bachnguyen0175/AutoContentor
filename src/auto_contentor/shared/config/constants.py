"""Application constants."""

from typing import Dict, List

# Agent Types
AGENT_TYPES = {
    "ORCHESTRATOR": "orchestrator",
    "KEYWORD": "keyword",
    "AUDIENCE": "audience", 
    "COMPETITOR": "competitor",
    "TREND": "trend",
    "AGGREGATOR": "aggregator"
}

# Task Types
TASK_TYPES = {
    "KEYWORD_RESEARCH": "keyword_research",
    "AUDIENCE_RESEARCH": "audience_research",
    "COMPETITOR_ANALYSIS": "competitor_analysis",
    "TREND_ANALYSIS": "trend_analysis",
    "REPORT_GENERATION": "report_generation"
}

# Queue Names
QUEUE_NAMES = {
    "KEYWORD_TASKS": "keyword_tasks",
    "AUDIENCE_TASKS": "audience_tasks",
    "COMPETITOR_TASKS": "competitor_tasks",
    "TREND_TASKS": "trend_tasks",
    "AGGREGATOR_TASKS": "aggregator_tasks",
    "NOTIFICATIONS": "notifications"
}

# Database Collections
COLLECTIONS = {
    "CAMPAIGNS": "campaigns",
    "KEYWORD_RESULTS": "keyword_results",
    "AUDIENCE_RESULTS": "audience_results",
    "COMPETITOR_RESULTS": "competitor_results",
    "TREND_RESULTS": "trend_results",
    "FINAL_REPORTS": "final_reports",
    "TASKS": "tasks",
    "LOGS": "logs"
}

# Cache Keys
CACHE_KEYS = {
    "CAMPAIGN": "campaign:{campaign_id}",
    "KEYWORD_RESULT": "keyword_result:{result_id}",
    "AUDIENCE_RESULT": "audience_result:{result_id}",
    "COMPETITOR_RESULT": "competitor_result:{result_id}",
    "TREND_RESULT": "trend_result:{result_id}",
    "REPORT": "report:{report_id}",
    "AGENT_STATUS": "agent_status:{agent_type}",
    "API_RATE_LIMIT": "rate_limit:{api_name}:{key}"
}

# Cache TTL (Time To Live) in seconds
CACHE_TTL = {
    "CAMPAIGN": 3600,  # 1 hour
    "RESULTS": 7200,   # 2 hours
    "REPORTS": 86400,  # 24 hours
    "AGENT_STATUS": 300,  # 5 minutes
    "API_RATE_LIMIT": 3600  # 1 hour
}

# API Rate Limits (requests per hour)
API_RATE_LIMITS = {
    "GOOGLE_TRENDS": 100,
    "SERPAPI": 100,
    "TWITTER": 300,
    "REDDIT": 60,
    "OPENAI": 3000,
    "GEMINI": 1000
}

# Content Types
CONTENT_TYPES = {
    "BLOG_POST": "blog_post",
    "VIDEO": "video",
    "SOCIAL_POST": "social_post",
    "INFOGRAPHIC": "infographic",
    "PODCAST": "podcast",
    "EBOOK": "ebook",
    "WEBINAR": "webinar",
    "CASE_STUDY": "case_study",
    "WHITEPAPER": "whitepaper",
    "EMAIL": "email"
}

# Social Media Platforms
SOCIAL_PLATFORMS = {
    "FACEBOOK": "facebook",
    "TWITTER": "twitter",
    "INSTAGRAM": "instagram",
    "LINKEDIN": "linkedin",
    "TIKTOK": "tiktok",
    "YOUTUBE": "youtube",
    "PINTEREST": "pinterest",
    "REDDIT": "reddit"
}

# Supported Languages
SUPPORTED_LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ja": "Japanese",
    "ko": "Korean",
    "zh": "Chinese",
    "ar": "Arabic"
}

# Supported Regions
SUPPORTED_REGIONS = {
    "US": "United States",
    "GB": "United Kingdom",
    "CA": "Canada",
    "AU": "Australia",
    "DE": "Germany",
    "FR": "France",
    "ES": "Spain",
    "IT": "Italy",
    "JP": "Japan",
    "KR": "South Korea",
    "CN": "China",
    "BR": "Brazil",
    "MX": "Mexico",
    "IN": "India"
}

# Industry Categories
INDUSTRY_CATEGORIES = [
    "Technology",
    "Healthcare",
    "Finance",
    "Education",
    "Retail",
    "Manufacturing",
    "Real Estate",
    "Travel",
    "Food & Beverage",
    "Fashion",
    "Automotive",
    "Entertainment",
    "Sports",
    "Non-profit",
    "Government",
    "Consulting",
    "Marketing",
    "Legal",
    "Other"
]

# Report Templates
REPORT_TEMPLATES = {
    "STANDARD": "standard_report.html",
    "EXECUTIVE": "executive_summary.html",
    "DETAILED": "detailed_analysis.html",
    "PRESENTATION": "presentation.html"
}

# File Size Limits (in bytes)
FILE_SIZE_LIMITS = {
    "REPORT_PDF": 50 * 1024 * 1024,  # 50MB
    "REPORT_HTML": 10 * 1024 * 1024,  # 10MB
    "UPLOAD_FILE": 5 * 1024 * 1024,   # 5MB
    "LOG_FILE": 100 * 1024 * 1024     # 100MB
}

# Timeout Settings (in seconds)
TIMEOUTS = {
    "API_REQUEST": 30,
    "DATABASE_QUERY": 10,
    "AGENT_TASK": 300,  # 5 minutes
    "REPORT_GENERATION": 600,  # 10 minutes
    "FILE_UPLOAD": 60
}

# Retry Settings
RETRY_SETTINGS = {
    "MAX_RETRIES": 3,
    "INITIAL_DELAY": 1,
    "MAX_DELAY": 60,
    "BACKOFF_FACTOR": 2
}

# Validation Rules
VALIDATION_RULES = {
    "MIN_KEYWORDS": 1,
    "MAX_KEYWORDS": 50,
    "MIN_COMPETITORS": 0,
    "MAX_COMPETITORS": 10,
    "MIN_CAMPAIGN_NAME_LENGTH": 1,
    "MAX_CAMPAIGN_NAME_LENGTH": 255,
    "MAX_DESCRIPTION_LENGTH": 1000
}

# Quality Thresholds
QUALITY_THRESHOLDS = {
    "MIN_CONFIDENCE_SCORE": 0.6,
    "MIN_DATA_FRESHNESS_HOURS": 24,
    "MIN_KEYWORD_VOLUME": 10,
    "MIN_TREND_SCORE": 30,
    "MIN_REPORT_QUALITY": 0.7
}

# Default Values
DEFAULTS = {
    "CAMPAIGN_PRIORITY": "medium",
    "TARGET_REGION": "US",
    "TARGET_LANGUAGE": "en",
    "ANALYSIS_PERIOD": "3months",
    "CONTENT_CALENDAR_DAYS": 30,
    "TOP_KEYWORDS_LIMIT": 20,
    "TOP_COMPETITORS_LIMIT": 5,
    "TOP_TRENDS_LIMIT": 10
}

# Error Messages
ERROR_MESSAGES = {
    "INVALID_API_KEY": "Invalid API key provided",
    "RATE_LIMIT_EXCEEDED": "API rate limit exceeded",
    "INSUFFICIENT_DATA": "Insufficient data for analysis",
    "ANALYSIS_FAILED": "Analysis failed to complete",
    "REPORT_GENERATION_FAILED": "Report generation failed",
    "DATABASE_CONNECTION_ERROR": "Database connection error",
    "INVALID_INPUT": "Invalid input parameters",
    "AGENT_UNAVAILABLE": "Agent service unavailable",
    "TIMEOUT_ERROR": "Request timeout",
    "UNKNOWN_ERROR": "An unknown error occurred"
}

# Success Messages
SUCCESS_MESSAGES = {
    "CAMPAIGN_CREATED": "Campaign created successfully",
    "ANALYSIS_COMPLETED": "Analysis completed successfully",
    "REPORT_GENERATED": "Report generated successfully",
    "DATA_UPDATED": "Data updated successfully",
    "TASK_COMPLETED": "Task completed successfully"
}

# Log Levels
LOG_LEVELS = {
    "DEBUG": "DEBUG",
    "INFO": "INFO",
    "WARNING": "WARNING",
    "ERROR": "ERROR",
    "CRITICAL": "CRITICAL"
}

# Health Check Endpoints
HEALTH_CHECK_ENDPOINTS = {
    "ORCHESTRATOR": "/health",
    "KEYWORD_AGENT": "/health",
    "AUDIENCE_AGENT": "/health",
    "COMPETITOR_AGENT": "/health",
    "TREND_AGENT": "/health",
    "AGGREGATOR_AGENT": "/health"
}

# Metrics and KPIs
DEFAULT_KPIS = [
    "organic_traffic_growth",
    "keyword_ranking_improvement",
    "content_engagement_rate",
    "social_media_reach",
    "lead_generation",
    "conversion_rate",
    "brand_awareness",
    "competitor_gap_closure"
]
