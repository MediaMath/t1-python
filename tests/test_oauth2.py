"""Test OAuth2 methods."""
import unittest
from terminalone import T1
import responses

mock_credentials = {
    'client_id': 'client_id',
    'client_secret': 'secret',
    'username': 'username',
    'password': 'asdf'
}


class TestOauth2ResourceOwnerLogin(unittest.TestCase):
    """Tests for OAuth2 Resource Owner Login."""

    @responses.activate
    def setUp(self):
        """Setup."""
        with open('tests/fixtures/json/access_token.json') as f:
            token = f.read()
        responses.add(responses.POST, 'https://auth.mediamath.com/oauth/token',
                      body=token,
                      adding_headers={
                          'Set-Cookie': 'adama_session=1',
                      },
                      content_type='application/json')

        self.t1 = T1(auth_method='oauth2-resourceowner',
                     **mock_credentials)

    @responses.activate
    def test_minimum_creds_for_oauth2(self):
        """Test Minimum Credentials."""
        self.assertEqual(self.t1.auth_params['method'], 'oauth2-resourceowner')

    @responses.activate
    def test_logout(self):
        """Test if logout removes credentials."""
        self.assertIsNotNone(self.t1.session.headers['Authorization'])
        self.t1.logout()
        self.assertIsNone(self.t1.session.headers['Authorization'])
