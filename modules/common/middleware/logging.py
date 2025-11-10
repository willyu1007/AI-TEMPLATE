"""


/
"""

import logging
import sys
from typing import Optional, Dict, Any
from datetime import datetime, timezone


def setup_logging(
    level: str = "INFO",
    format_string: Optional[str] = None,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    
    
    Args:
        level: DEBUG, INFO, WARNING, ERROR, CRITICAL
        format_string: 
        log_file: 
        
    Returns:
         logger 
        
    Examples:
        >>> logger = setup_logging(level="DEBUG")
        >>> logger.info("Test message")
    """
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, level.upper()))
    
    # 
    logger.handlers.clear()
    
    # 
    formatter = logging.Formatter(format_string)
    
    # 
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def log_request(
    method: str,
    path: str,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    logger: Optional[logging.Logger] = None
):
    """
    
    
    Args:
        method: HTTP GET, POST 
        path: 
        headers: 
        params: 
        logger: logger  logger
        
    Examples:
        >>> log_request("GET", "/api/users", params={"page": 1})
    """
    if logger is None:
        logger = logging.getLogger()
    
    logger.info(
        f"Request: {method} {path} | "
        f"Params: {params or {}} | "
        f"Time: {datetime.now(timezone.utc).isoformat()}"
    )


def log_response(
    status_code: int,
    path: str,
    duration_ms: float,
    logger: Optional[logging.Logger] = None
):
    """
    
    
    Args:
        status_code: HTTP 
        path: 
        duration_ms: 
        logger: logger  logger
        
    Examples:
        >>> log_response(200, "/api/users", 150.5)
    """
    if logger is None:
        logger = logging.getLogger()
    
    level = logging.ERROR if status_code >= 400 else logging.INFO
    logger.log(
        level,
        f"Response: {status_code} {path} | "
        f"Duration: {duration_ms:.2f}ms | "
        f"Time: {datetime.now(timezone.utc).isoformat()}"
    )

