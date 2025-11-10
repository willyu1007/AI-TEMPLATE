#!/usr/bin/env python3
"""
Auth middleware tests.
"""

import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

os.environ["TEMPLATEAI_AUTH_SECRET"] = "unit-test-secret"

from modules.common.middleware.auth import AuthConfig, AuthMiddleware, AuthError


class TestAuthMiddleware(unittest.TestCase):
    def setUp(self):
        self.config = AuthConfig(secret_key="unit-test-secret", token_ttl_seconds=1, leeway_seconds=0)
        self.auth = AuthMiddleware(self.config)
        self.valid_token = self.auth.issue_token(
            user_id="user123",
            username="tester",
            role="user",
            permissions=["read"],
        )
    
    def test_validate_token_valid(self):
        self.assertTrue(self.auth.validate_token(self.valid_token))
        self.assertEqual(self.auth.last_validated, self.valid_token)
    
    def test_validate_token_invalid_format(self):
        self.assertFalse(self.auth.validate_token("invalid_format"))
        expired = self.auth.issue_token(user_id="user123", username="x", role="user", permissions=[], ttl_seconds=-10)
        self.assertFalse(self.auth.validate_token(expired))
    
    def test_extract_user_from_token(self):
        user_info = self.auth.extract_user(self.valid_token)
        self.assertIsNotNone(user_info)
        self.assertEqual(user_info["user_id"], "user123")
        self.assertIn("read", user_info["permissions"])
    
    def test_check_permission(self):
        self.auth.set_permissions(["read", "write"])
        self.assertTrue(self.auth.check_permission("read"))
        self.assertFalse(self.auth.check_permission("admin"))
    
    def test_refresh_token(self):
        refreshed = self.auth.refresh_token(self.valid_token)
        self.assertIsNotNone(refreshed)
        self.assertNotEqual(refreshed, self.valid_token)
        self.assertTrue(self.auth.validate_token(refreshed))
    
    def test_require_auth_helper(self):
        from modules.common.middleware.auth import require_auth
        
        @require_auth
        def protected_endpoint(*, current_user=None):
            return current_user
        
        result = protected_endpoint(token=self.valid_token)
        self.assertEqual(result["user_id"], "user123")
        
        with self.assertRaises(AuthError):
            protected_endpoint(token="Bearer invalid")


if __name__ == "__main__":
    unittest.main()
