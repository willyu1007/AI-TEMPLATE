#!/usr/bin/env python3
"""
日志中间件测试用例
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import logging
from pathlib import Path

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.common.middleware.logging import setup_logging


class TestLoggingMiddleware(unittest.TestCase):
    """日志中间件测试类"""
    
    def test_setup_logging_default(self):
        """测试默认日志设置"""
        logger = setup_logging()
        
        self.assertIsNotNone(logger)
        self.assertEqual(logger.level, logging.INFO)
        self.assertTrue(len(logger.handlers) > 0)
    
    def test_setup_logging_debug_level(self):
        """测试DEBUG级别日志设置"""
        logger = setup_logging(level="DEBUG")
        
        self.assertIsNotNone(logger)
        self.assertEqual(logger.level, logging.DEBUG)
    
    def test_setup_logging_custom_format(self):
        """测试自定义日志格式"""
        custom_format = "%(levelname)s - %(message)s"
        logger = setup_logging(format_string=custom_format)
        
        self.assertIsNotNone(logger)
        # 检查handler的formatter
        if logger.handlers:
            formatter = logger.handlers[0].formatter
            self.assertIsNotNone(formatter)
    
    def test_setup_logging_invalid_level(self):
        """测试无效日志级别"""
        # 应该使用默认级别INFO
        logger = setup_logging(level="INVALID_LEVEL")
        self.assertEqual(logger.level, logging.INFO)
    
    def test_logger_output(self):
        """测试日志输出"""
        logger = setup_logging(level="INFO")
        
        # 模拟日志输出
        with self.assertLogs(logger, level='INFO') as log_context:
            logger.info("Test info message")
            logger.warning("Test warning message")
        
        self.assertEqual(len(log_context.records), 2)
        self.assertIn("Test info message", log_context.output[0])
        self.assertIn("Test warning message", log_context.output[1])
    
    def test_logger_filtering(self):
        """测试日志级别过滤"""
        logger = setup_logging(level="WARNING")
        
        with self.assertLogs(logger, level='WARNING') as log_context:
            logger.debug("Debug message")  # 不应该被记录
            logger.info("Info message")    # 不应该被记录
            logger.warning("Warning message")  # 应该被记录
            logger.error("Error message")   # 应该被记录
        
        # 只有WARNING和ERROR应该被记录
        self.assertEqual(len(log_context.records), 2)
        self.assertIn("Warning message", str(log_context.output))
        self.assertIn("Error message", str(log_context.output))


if __name__ == '__main__':
    unittest.main()
