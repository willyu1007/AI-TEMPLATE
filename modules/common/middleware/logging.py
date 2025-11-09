"""
日志中间件

提供统一的日志配置和请求/响应日志记录功能。
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
    设置日志配置
    
    Args:
        level: 日志级别（DEBUG, INFO, WARNING, ERROR, CRITICAL）
        format_string: 日志格式字符串
        log_file: 日志文件路径（可选，默认输出到控制台）
        
    Returns:
        配置好的 logger 对象
        
    Examples:
        >>> logger = setup_logging(level="DEBUG")
        >>> logger.info("Test message")
    """
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, level.upper()))
    
    # 清除现有的处理器
    logger.handlers.clear()
    
    # 创建格式化器
    formatter = logging.Formatter(format_string)
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器（如果指定）
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
    记录请求日志
    
    Args:
        method: HTTP 方法（GET, POST 等）
        path: 请求路径
        headers: 请求头（可选）
        params: 请求参数（可选）
        logger: logger 对象（可选，默认使用根 logger）
        
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
    记录响应日志
    
    Args:
        status_code: HTTP 状态码
        path: 请求路径
        duration_ms: 处理耗时（毫秒）
        logger: logger 对象（可选，默认使用根 logger）
        
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

