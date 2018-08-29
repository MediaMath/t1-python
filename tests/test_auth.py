from __future__ import absolute_import
import unittest
from terminalone import service


class TestDetectAuthMethod(unittest.TestCase):
    """Tests for auth method detection in service.py."""

    def test_credentials_returns_cookie_auth_method(self):
        """Test."""
        m = service._detect_auth_method("u", "pass", None, "key", None, None, None)
        self.assertEqual(m, 'cookie')

    def test_session_id_returns_cookie_auth_method(self):
        """Test."""
        m = service._detect_auth_method(None, None, "session", "key", None, None, None)
        self.assertEqual(m, 'cookie')

    def test_secret_returns_oauth2_resource_owner_auth_method(self):
        """Test."""
        m = service._detect_auth_method(None, None, None, "key", "client_id", "secret", None)
        self.assertEqual(m, 'oauth2-resourceowner')
