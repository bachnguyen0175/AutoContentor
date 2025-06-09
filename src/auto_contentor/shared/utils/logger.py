"""Centralized logging configuration for AutoContentor."""

import sys
from pathlib import Path
from typing import Optional

from loguru import logger

from ..config.settings import get_settings


class LoggerConfig:
    """Logger configuration and setup."""
    
    def __init__(self):
        self.settings = get_settings()
        self._configured = False
    
    def configure(self, service_name: Optional[str] = None) -> None:
        """Configure logger with appropriate settings."""
        if self._configured:
            return
        
        # Remove default handler
        logger.remove()
        
        # Console handler
        self._add_console_handler()
        
        # File handler
        self._add_file_handler(service_name)
        
        # Error file handler
        self._add_error_file_handler(service_name)
        
        self._configured = True
    
    def _add_console_handler(self) -> None:
        """Add console logging handler."""
        log_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )
        
        if self.settings.is_development:
            # More verbose format for development
            log_format = (
                "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                "<level>{message}</level>"
            )
        
        logger.add(
            sys.stdout,
            format=log_format,
            level=self.settings.app.log_level,
            colorize=True,
            backtrace=self.settings.is_development,
            diagnose=self.settings.is_development
        )
    
    def _add_file_handler(self, service_name: Optional[str] = None) -> None:
        """Add file logging handler."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        service_prefix = f"{service_name}_" if service_name else ""
        log_file = log_dir / f"{service_prefix}app.log"
        
        log_format = (
            "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
            "{level: <8} | "
            "{name}:{function}:{line} | "
            "{message}"
        )
        
        logger.add(
            log_file,
            format=log_format,
            level=self.settings.app.log_level,
            rotation="10 MB",
            retention="30 days",
            compression="gz",
            backtrace=True,
            diagnose=True
        )
    
    def _add_error_file_handler(self, service_name: Optional[str] = None) -> None:
        """Add error-only file logging handler."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        service_prefix = f"{service_name}_" if service_name else ""
        error_log_file = log_dir / f"{service_prefix}error.log"
        
        log_format = (
            "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
            "{level: <8} | "
            "{name}:{function}:{line} | "
            "{message} | "
            "{exception}"
        )
        
        logger.add(
            error_log_file,
            format=log_format,
            level="ERROR",
            rotation="5 MB",
            retention="60 days",
            compression="gz",
            backtrace=True,
            diagnose=True
        )


# Global logger configuration instance
_logger_config = LoggerConfig()


def setup_logger(service_name: Optional[str] = None) -> None:
    """Setup logger for a service."""
    _logger_config.configure(service_name)


def get_logger(name: str) -> "logger":
    """Get a logger instance with the given name."""
    return logger.bind(service=name)


# Convenience functions for different log levels
def log_info(message: str, **kwargs) -> None:
    """Log info message."""
    logger.info(message, **kwargs)


def log_warning(message: str, **kwargs) -> None:
    """Log warning message."""
    logger.warning(message, **kwargs)


def log_error(message: str, **kwargs) -> None:
    """Log error message."""
    logger.error(message, **kwargs)


def log_debug(message: str, **kwargs) -> None:
    """Log debug message."""
    logger.debug(message, **kwargs)


def log_critical(message: str, **kwargs) -> None:
    """Log critical message."""
    logger.critical(message, **kwargs)


# Context managers for structured logging
class LogContext:
    """Context manager for structured logging."""
    
    def __init__(self, operation: str, **context):
        self.operation = operation
        self.context = context
        self.start_time = None
    
    def __enter__(self):
        import time
        self.start_time = time.time()
        logger.info(f"Starting {self.operation}", **self.context)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        duration = time.time() - self.start_time if self.start_time else 0
        
        if exc_type is None:
            logger.info(
                f"Completed {self.operation}",
                duration_seconds=duration,
                **self.context
            )
        else:
            logger.error(
                f"Failed {self.operation}",
                duration_seconds=duration,
                error_type=exc_type.__name__ if exc_type else None,
                error_message=str(exc_val) if exc_val else None,
                **self.context
            )


def log_operation(operation: str, **context):
    """Create a log context for an operation."""
    return LogContext(operation, **context)


# Decorators for automatic logging
def log_function_call(func):
    """Decorator to automatically log function calls."""
    from functools import wraps
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = f"{func.__module__}.{func.__name__}"
        
        with log_operation(f"function_call: {func_name}"):
            try:
                result = func(*args, **kwargs)
                logger.debug(f"Function {func_name} completed successfully")
                return result
            except Exception as e:
                logger.error(f"Function {func_name} failed: {str(e)}")
                raise
    
    return wrapper


def log_async_function_call(func):
    """Decorator to automatically log async function calls."""
    from functools import wraps
    
    @wraps(func)
    async def wrapper(*args, **kwargs):
        func_name = f"{func.__module__}.{func.__name__}"
        
        with log_operation(f"async_function_call: {func_name}"):
            try:
                result = await func(*args, **kwargs)
                logger.debug(f"Async function {func_name} completed successfully")
                return result
            except Exception as e:
                logger.error(f"Async function {func_name} failed: {str(e)}")
                raise
    
    return wrapper


# Performance logging
class PerformanceLogger:
    """Logger for performance metrics."""
    
    @staticmethod
    def log_api_call(api_name: str, endpoint: str, duration: float, status_code: int = None):
        """Log API call performance."""
        logger.info(
            "API call completed",
            api_name=api_name,
            endpoint=endpoint,
            duration_seconds=duration,
            status_code=status_code
        )
    
    @staticmethod
    def log_database_query(collection: str, operation: str, duration: float, count: int = None):
        """Log database query performance."""
        logger.info(
            "Database query completed",
            collection=collection,
            operation=operation,
            duration_seconds=duration,
            record_count=count
        )
    
    @staticmethod
    def log_agent_task(agent_type: str, task_type: str, duration: float, success: bool = True):
        """Log agent task performance."""
        logger.info(
            "Agent task completed",
            agent_type=agent_type,
            task_type=task_type,
            duration_seconds=duration,
            success=success
        )


# Initialize performance logger instance
perf_logger = PerformanceLogger()
