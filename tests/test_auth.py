from __future__ import absolute_import
import unittest
from terminalone import errors, service


class TestDetectAuthMethod(unittest.TestCase):
    """Tests for auth method detection in service.py"""
    def test_no_apikey_raises_auth_method(self):
        with self.assertRaises(errors.ClientError):
            service._detect_auth_method(None, None, None, None, None, None)

    def test_token_returns_oauth2_auth_method(self):
        m = service._detect_auth_method(None, None, None, "key", None, "token")
        self.assertEqual(m, 'oauth2')

    def test_credentials_returns_cookie_auth_method(self):
        m = service._detect_auth_method("u", "pass", None, "key", None, None)
        self.assertEqual(m, 'cookie')

    def test_session_id_returns_cookie_auth_method(self):
        m = service._detect_auth_method(None, None, "session", "key", None, None)
        self.assertEqual(m, 'cookie')

    def test_secret_returns_oauth2_auth_method(self):
        m = service._detect_auth_method(None, None, None, "key", "secret", None)
        self.assertEqual(m, 'oauth2')
