"""Application settings and configuration."""

import os
from typing import List, Optional

from pydantic import BaseSettings, Field


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""
    
    mongodb_url: str = Field(default="mongodb://localhost:27017", env="MONGODB_URL")
    mongodb_database: str = Field(default="autocontentor", env="MONGODB_DATABASE")
    mongodb_username: Optional[str] = Field(default=None, env="MONGODB_USERNAME")
    mongodb_password: Optional[str] = Field(default=None, env="MONGODB_PASSWORD")
    
    redis_url: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    redis_password: Optional[str] = Field(default=None, env="REDIS_PASSWORD")
    redis_db: int = Field(default=0, env="REDIS_DB")
    
    class Config:
        env_file = ".env"


class APISettings(BaseSettings):
    """External API configuration settings."""
    
    # Google APIs
    google_api_key: Optional[str] = Field(default=None, env="GOOGLE_API_KEY")
    google_search_engine_id: Optional[str] = Field(default=None, env="GOOGLE_SEARCH_ENGINE_ID")
    
    # AI/LLM APIs
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    gemini_api_key: Optional[str] = Field(default=None, env="GEMINI_API_KEY")
    
    # Search APIs
    serpapi_key: Optional[str] = Field(default=None, env="SERPAPI_KEY")
    
    # Social Media APIs
    twitter_bearer_token: Optional[str] = Field(default=None, env="TWITTER_BEARER_TOKEN")
    reddit_client_id: Optional[str] = Field(default=None, env="REDDIT_CLIENT_ID")
    reddit_client_secret: Optional[str] = Field(default=None, env="REDDIT_CLIENT_SECRET")
    reddit_user_agent: str = Field(default="AutoContentor/1.0", env="REDDIT_USER_AGENT")
    
    class Config:
        env_file = ".env"


class ServiceSettings(BaseSettings):
    """Service configuration settings."""
    
    # Orchestrator
    orchestrator_host: str = Field(default="0.0.0.0", env="ORCHESTRATOR_HOST")
    orchestrator_port: int = Field(default=8000, env="ORCHESTRATOR_PORT")
    orchestrator_workers: int = Field(default=1, env="ORCHESTRATOR_WORKERS")
    
    # Agents
    keyword_agent_host: str = Field(default="0.0.0.0", env="KEYWORD_AGENT_HOST")
    keyword_agent_port: int = Field(default=8001, env="KEYWORD_AGENT_PORT")
    
    audience_agent_host: str = Field(default="0.0.0.0", env="AUDIENCE_AGENT_HOST")
    audience_agent_port: int = Field(default=8002, env="AUDIENCE_AGENT_PORT")
    
    competitor_agent_host: str = Field(default="0.0.0.0", env="COMPETITOR_AGENT_HOST")
    competitor_agent_port: int = Field(default=8003, env="COMPETITOR_AGENT_PORT")
    
    trend_agent_host: str = Field(default="0.0.0.0", env="TREND_AGENT_HOST")
    trend_agent_port: int = Field(default=8004, env="TREND_AGENT_PORT")
    
    aggregator_agent_host: str = Field(default="0.0.0.0", env="AGGREGATOR_AGENT_HOST")
    aggregator_agent_port: int = Field(default=8005, env="AGGREGATOR_AGENT_PORT")
    
    class Config:
        env_file = ".env"


class SecuritySettings(BaseSettings):
    """Security configuration settings."""
    
    secret_key: str = Field(default="your_secret_key_here_change_in_production", env="SECRET_KEY")
    jwt_secret_key: str = Field(default="your_jwt_secret_key_here", env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_expiration_hours: int = Field(default=24, env="JWT_EXPIRATION_HOURS")
    
    class Config:
        env_file = ".env"


class ApplicationSettings(BaseSettings):
    """Main application settings."""
    
    app_name: str = Field(default="AutoContentor", env="APP_NAME")
    app_version: str = Field(default="0.1.0", env="APP_VERSION")
    app_environment: str = Field(default="development", env="APP_ENVIRONMENT")
    debug: bool = Field(default=True, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Rate limiting
    api_rate_limit: int = Field(default=100, env="API_RATE_LIMIT")
    request_timeout: int = Field(default=30, env="REQUEST_TIMEOUT")
    max_retries: int = Field(default=3, env="MAX_RETRIES")
    retry_delay: int = Field(default=1, env="RETRY_DELAY")
    
    # Report settings
    report_output_dir: str = Field(default="./reports", env="REPORT_OUTPUT_DIR")
    report_template_dir: str = Field(default="./templates", env="REPORT_TEMPLATE_DIR")
    max_report_size_mb: int = Field(default=50, env="MAX_REPORT_SIZE_MB")
    
    # Development settings
    dev_mode: bool = Field(default=True, env="DEV_MODE")
    enable_cors: bool = Field(default=True, env="ENABLE_CORS")
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        env="CORS_ORIGINS"
    )
    
    class Config:
        env_file = ".env"


class Settings:
    """Combined settings class."""
    
    def __init__(self):
        self.app = ApplicationSettings()
        self.database = DatabaseSettings()
        self.api = APISettings()
        self.service = ServiceSettings()
        self.security = SecuritySettings()
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.app.app_environment.lower() in ["development", "dev"]
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.app.app_environment.lower() in ["production", "prod"]
    
    @property
    def mongodb_connection_string(self) -> str:
        """Get MongoDB connection string."""
        if self.database.mongodb_username and self.database.mongodb_password:
            # Replace localhost with credentials
            url = self.database.mongodb_url.replace(
                "mongodb://",
                f"mongodb://{self.database.mongodb_username}:{self.database.mongodb_password}@"
            )
            return f"{url}/{self.database.mongodb_database}"
        return f"{self.database.mongodb_url}/{self.database.mongodb_database}"
    
    @property
    def redis_connection_string(self) -> str:
        """Get Redis connection string."""
        if self.database.redis_password:
            return f"{self.database.redis_url}?password={self.database.redis_password}&db={self.database.redis_db}"
        return f"{self.database.redis_url}/{self.database.redis_db}"


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings."""
    return settings


def reload_settings() -> Settings:
    """Reload settings from environment."""
    global settings
    settings = Settings()
    return settings
