#!/usr/bin/env python3
"""

"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import logging
from pathlib import Path

# 
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.common.middleware.logging import setup_logging


class TestLoggingMiddleware(unittest.TestCase):
    """"""
    
    def test_setup_logging_default(self):
        """"""
        logger = setup_logging()
        
        self.assertIsNotNone(logger)
        self.assertEqual(logger.level, logging.INFO)
        self.assertTrue(len(logger.handlers) > 0)
    
    def test_setup_logging_debug_level(self):
        """DEBUG"""
        logger = setup_logging(level="DEBUG")
        
        self.assertIsNotNone(logger)
        self.assertEqual(logger.level, logging.DEBUG)
    
    def test_setup_logging_custom_format(self):
        """"""
        custom_format = "%(levelname)s - %(message)s"
        logger = setup_logging(format_string=custom_format)
        
        self.assertIsNotNone(logger)
        # handlerformatter
        if logger.handlers:
            formatter = logger.handlers[0].formatter
            self.assertIsNotNone(formatter)
    
    def test_setup_logging_invalid_level(self):
        """"""
        # INFO
        logger = setup_logging(level="INVALID_LEVEL")
        self.assertEqual(logger.level, logging.INFO)
    
    def test_logger_output(self):
        """"""
        logger = setup_logging(level="INFO")
        
        # 
        with self.assertLogs(logger, level='INFO') as log_context:
            logger.info("Test info message")
            logger.warning("Test warning message")
        
        self.assertEqual(len(log_context.records), 2)
        self.assertIn("Test info message", log_context.output[0])
        self.assertIn("Test warning message", log_context.output[1])
    
    def test_logger_filtering(self):
        """"""
        logger = setup_logging(level="WARNING")
        
        with self.assertLogs(logger, level='WARNING') as log_context:
            logger.debug("Debug message")  # 
            logger.info("Info message")    # 
            logger.warning("Warning message")  # 
            logger.error("Error message")   # 
        
        # WARNINGERROR
        self.assertEqual(len(log_context.records), 2)
        self.assertIn("Warning message", str(log_context.output))
        self.assertIn("Error message", str(log_context.output))


if __name__ == '__main__':
    unittest.main()
