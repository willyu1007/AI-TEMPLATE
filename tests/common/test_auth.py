#!/usr/bin/env python3
"""


"""

import unittest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# 
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.common.middleware.auth import AuthMiddleware


class TestAuthMiddleware(unittest.TestCase):
    """"""
    
    def setUp(self):
        """"""
        self.auth = AuthMiddleware()
    
    def test_validate_token_valid(self):
        """token"""
        # token
        valid_token = "Bearer valid_token_123"
        result = self.auth.validate_token(valid_token)
        
        self.assertTrue(result)
        self.assertEqual(self.auth.last_validated, valid_token)
    
    def test_validate_token_invalid(self):
        """token"""
        # token
        self.assertFalse(self.auth.validate_token(""))
        
        # token
        self.assertFalse(self.auth.validate_token("invalid_format"))
        
        # token
        expired_token = "Bearer expired_token"
        self.assertFalse(self.auth.validate_token(expired_token))
    
    def test_extract_user_from_token(self):
        """token"""
        token = "Bearer user123_token"
        user_info = self.auth.extract_user(token)
        
        self.assertIsNotNone(user_info)
        self.assertIn('user_id', user_info)
        self.assertIn('permissions', user_info)
    
    def test_check_permission(self):
        """"""
        # 
        self.auth.set_permissions(['read', 'write'])
        
        # 
        self.assertTrue(self.auth.check_permission('read'))
        self.assertTrue(self.auth.check_permission('write'))
        
        # 
        self.assertFalse(self.auth.check_permission('admin'))
        self.assertFalse(self.auth.check_permission('delete'))
    
    def test_refresh_token(self):
        """token"""
        old_token = "Bearer old_token_123"
        new_token = self.auth.refresh_token(old_token)
        
        self.assertIsNotNone(new_token)
        self.assertNotEqual(old_token, new_token)
        self.assertTrue(new_token.startswith("Bearer"))
    
    def tearDown(self):
        """"""
        self.auth = None


if __name__ == '__main__':
    unittest.main()
