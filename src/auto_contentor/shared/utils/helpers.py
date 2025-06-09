"""Utility helper functions for AutoContentor."""

import asyncio
import hashlib
import json
import re
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse

import httpx
from pydantic import BaseModel

from ..config.constants import RETRY_SETTINGS
from .logger import get_logger, log_operation

logger = get_logger(__name__)


def generate_id(prefix: str = "", length: int = 8) -> str:
    """Generate a unique ID with optional prefix."""
    import uuid
    unique_id = str(uuid.uuid4()).replace("-", "")[:length]
    return f"{prefix}{unique_id}" if prefix else unique_id


def hash_string(text: str, algorithm: str = "md5") -> str:
    """Generate hash of a string."""
    if algorithm == "md5":
        return hashlib.md5(text.encode()).hexdigest()
    elif algorithm == "sha256":
        return hashlib.sha256(text.encode()).hexdigest()
    else:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")


def clean_text(text: str) -> str:
    """Clean and normalize text."""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\-.,!?;:]', '', text)
    
    return text


def extract_domain(url: str) -> Optional[str]:
    """Extract domain from URL."""
    try:
        parsed = urlparse(url)
        return parsed.netloc.lower()
    except Exception:
        return None


def is_valid_url(url: str) -> bool:
    """Check if URL is valid."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def normalize_keyword(keyword: str) -> str:
    """Normalize keyword for consistent processing."""
    return keyword.lower().strip()


def extract_keywords_from_text(text: str, min_length: int = 2) -> List[str]:
    """Extract potential keywords from text."""
    # Simple keyword extraction - can be enhanced with NLP
    words = re.findall(r'\b[a-zA-Z]{' + str(min_length) + ',}\b', text.lower())
    return list(set(words))


def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate similarity between two texts (simple Jaccard similarity)."""
    if not text1 or not text2:
        return 0.0
    
    set1 = set(text1.lower().split())
    set2 = set(text2.lower().split())
    
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    
    return intersection / union if union > 0 else 0.0


def format_number(number: Union[int, float], precision: int = 2) -> str:
    """Format number with appropriate units (K, M, B)."""
    if number < 1000:
        return str(int(number))
    elif number < 1000000:
        return f"{number/1000:.{precision}f}K"
    elif number < 1000000000:
        return f"{number/1000000:.{precision}f}M"
    else:
        return f"{number/1000000000:.{precision}f}B"


def parse_date_string(date_str: str) -> Optional[datetime]:
    """Parse date string in various formats."""
    formats = [
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%SZ",
        "%d/%m/%Y",
        "%m/%d/%Y"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    return None


def get_date_range(period: str) -> tuple[datetime, datetime]:
    """Get date range for a given period."""
    end_date = datetime.utcnow()
    
    if period == "1week":
        start_date = end_date - timedelta(weeks=1)
    elif period == "1month":
        start_date = end_date - timedelta(days=30)
    elif period == "3months":
        start_date = end_date - timedelta(days=90)
    elif period == "6months":
        start_date = end_date - timedelta(days=180)
    elif period == "1year":
        start_date = end_date - timedelta(days=365)
    else:
        # Default to 3 months
        start_date = end_date - timedelta(days=90)
    
    return start_date, end_date


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """Split list into chunks of specified size."""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def flatten_list(nested_list: List[List[Any]]) -> List[Any]:
    """Flatten a nested list."""
    return [item for sublist in nested_list for item in sublist]


def safe_get(dictionary: Dict, key: str, default: Any = None) -> Any:
    """Safely get value from dictionary with dot notation support."""
    keys = key.split('.')
    value = dictionary
    
    try:
        for k in keys:
            value = value[k]
        return value
    except (KeyError, TypeError):
        return default


def merge_dicts(*dicts: Dict) -> Dict:
    """Merge multiple dictionaries."""
    result = {}
    for d in dicts:
        if d:
            result.update(d)
    return result


def filter_dict(dictionary: Dict, keys: List[str]) -> Dict:
    """Filter dictionary to only include specified keys."""
    return {k: v for k, v in dictionary.items() if k in keys}


def serialize_model(model: BaseModel) -> Dict:
    """Serialize Pydantic model to dictionary."""
    return model.dict()


def deserialize_model(data: Dict, model_class: type) -> BaseModel:
    """Deserialize dictionary to Pydantic model."""
    return model_class(**data)


class RetryableError(Exception):
    """Exception that indicates an operation should be retried."""
    pass


async def retry_async(
    func,
    *args,
    max_retries: int = None,
    initial_delay: float = None,
    max_delay: float = None,
    backoff_factor: float = None,
    retryable_exceptions: tuple = (Exception,),
    **kwargs
):
    """Retry an async function with exponential backoff."""
    max_retries = max_retries or RETRY_SETTINGS["MAX_RETRIES"]
    initial_delay = initial_delay or RETRY_SETTINGS["INITIAL_DELAY"]
    max_delay = max_delay or RETRY_SETTINGS["MAX_DELAY"]
    backoff_factor = backoff_factor or RETRY_SETTINGS["BACKOFF_FACTOR"]
    
    last_exception = None
    delay = initial_delay
    
    for attempt in range(max_retries + 1):
        try:
            return await func(*args, **kwargs)
        except retryable_exceptions as e:
            last_exception = e
            
            if attempt == max_retries:
                logger.error(f"Function {func.__name__} failed after {max_retries} retries: {str(e)}")
                raise e
            
            logger.warning(f"Function {func.__name__} failed (attempt {attempt + 1}/{max_retries + 1}): {str(e)}")
            
            await asyncio.sleep(delay)
            delay = min(delay * backoff_factor, max_delay)
    
    raise last_exception


def retry_sync(
    func,
    *args,
    max_retries: int = None,
    initial_delay: float = None,
    max_delay: float = None,
    backoff_factor: float = None,
    retryable_exceptions: tuple = (Exception,),
    **kwargs
):
    """Retry a sync function with exponential backoff."""
    max_retries = max_retries or RETRY_SETTINGS["MAX_RETRIES"]
    initial_delay = initial_delay or RETRY_SETTINGS["INITIAL_DELAY"]
    max_delay = max_delay or RETRY_SETTINGS["MAX_DELAY"]
    backoff_factor = backoff_factor or RETRY_SETTINGS["BACKOFF_FACTOR"]
    
    last_exception = None
    delay = initial_delay
    
    for attempt in range(max_retries + 1):
        try:
            return func(*args, **kwargs)
        except retryable_exceptions as e:
            last_exception = e
            
            if attempt == max_retries:
                logger.error(f"Function {func.__name__} failed after {max_retries} retries: {str(e)}")
                raise e
            
            logger.warning(f"Function {func.__name__} failed (attempt {attempt + 1}/{max_retries + 1}): {str(e)}")
            
            time.sleep(delay)
            delay = min(delay * backoff_factor, max_delay)
    
    raise last_exception


async def make_http_request(
    url: str,
    method: str = "GET",
    headers: Optional[Dict] = None,
    params: Optional[Dict] = None,
    json_data: Optional[Dict] = None,
    timeout: int = 30
) -> Dict:
    """Make HTTP request with error handling and retries."""
    
    async def _make_request():
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json_data
            )
            response.raise_for_status()
            return response.json()
    
    with log_operation(f"http_request: {method} {url}"):
        return await retry_async(
            _make_request,
            retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException)
        )


def validate_email(email: str) -> bool:
    """Validate email address format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to maximum length with suffix."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def get_file_extension(filename: str) -> str:
    """Get file extension from filename."""
    return filename.split('.')[-1].lower() if '.' in filename else ""


def is_valid_file_type(filename: str, allowed_extensions: List[str]) -> bool:
    """Check if file type is allowed."""
    extension = get_file_extension(filename)
    return extension in [ext.lower() for ext in allowed_extensions]


def calculate_percentage(part: float, total: float) -> float:
    """Calculate percentage with zero division protection."""
    return (part / total * 100) if total > 0 else 0.0


def round_to_nearest(number: float, nearest: float = 0.1) -> float:
    """Round number to nearest specified value."""
    return round(number / nearest) * nearest
