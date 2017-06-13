from __future__ import absolute_import
from time import time
import unittest
import responses
from terminalone import T1
from terminalone.vendor import six

mock_credentials = {
    'api_key': 'api_key',
    'client_secret': 'secret',
    'redirect_uri': 'https://www.mediamath.com/',
}

API_BASE = 'api.mediamath.com'

expected_token = {
    'access_token': 'accesstoken',
    'expires_in': 3600,
    'refresh_token': 'refreshtoken',
    'token_type': 'Bearer',
}


def to_nearest_hundred(number):
    return round(float(number) / 100) * 100


def mock_saver(_):
    pass


class TestOauth2ResourceOwnerLogin(unittest.TestCase):
  """ Tests for OAuth2 Resource Owner Login"""
  def setUp(self):
        self.t1 = T1(**mock_credentials)
        with open('tests/fixtures/json/access_token.json') as f:
            self.token = f.read()

    def test_minimum_creds_for_oauth2(self):
        self.assertEqual(self.t1.auth_params['method'], 'oauth2')

class TestOAuth2Login(unittest.TestCase):
    """Tests for OAuth2 Authentication"""
    def setUp(self):
        self.t1 = T1(**mock_credentials)
        with open('tests/fixtures/json/access_token.json') as f:
            self.token = f.read()

    def test_minimum_creds_for_oauth2(self):
        self.assertEqual(self.t1.auth_params['method'], 'oauth2')

    def test_authorization_url(self):
        url, state = self.t1.authorization_url()
        url_prefix = ('https://api.mediamath.com/oauth2/v1.0/authorize?response'
                      '_type=code&client_id=api_key&redirect_uri=https%3A%2F%2F')
        self.assertIn(url_prefix, url)
        self.assertIn(state, url)

    @responses.activate
    def test_fetch_token_from_explicit_state_and_code(self):
        responses.add(responses.POST,
                      'https://api.mediamath.com/oauth2/v1.0/token',
                      body=self.token,
                      content_type='application/json')
        token = self.t1.fetch_token(state='state', code='code')
        for field, val in six.iteritems(expected_token):
            self.assertIn(field, token,
                          'Expected {} in token. Token received: {}'
                          .format(field, token))
            self.assertEqual(val, token[field],
                             'Bad value in token. Expected: {}, got: {}'
                             .format(val, token[field]))

    @responses.activate
    def test_fetch_token_from_authorization_response_url(self):
        responses.add(responses.POST,
                      'https://api.mediamath.com/oauth2/v1.0/token',
                      body=self.token,
                      content_type='application/json')
        url = 'https://www.mediamath.com/?code=code&state=state'
        token = self.t1.fetch_token(authorization_response_url=url)
        for field, val in six.iteritems(expected_token):
            self.assertIn(field, token,
                          'Expected {} in token. Token received: {}'
                          .format(field, token))
            self.assertEqual(val, token[field],
                             'Bad value in token. Expected: {}, got: {}'
                             .format(val, token[field]))

    @responses.activate
    def test_read_expiration_from_token(self):
        responses.add(responses.POST,
                      'https://api.mediamath.com/oauth2/v1.0/token',
                      body=self.token,
                      content_type='application/json')
        token = self.t1.fetch_token(state='state', code='code')
        now = time()
        calculated_ttl = to_nearest_hundred(token['expires_at'] - now)
        self.assertEqual(calculated_ttl, 3600)

    @responses.activate
    def test_new_session_with_token(self):
        responses.add(responses.POST,
                      'https://api.mediamath.com/oauth2/v1.0/token',
                      body=self.token,
                      content_type='application/json')
        token = self.t1.fetch_token(state='state', code='code')
        with open('tests/fixtures/xml/advertiser.xml') as f:
            responses.add(responses.GET,
                          'https://api.mediamath.com/api/v2.0/advertisers/1',
                          body=f.read(),
                          content_type='application/xml')

        new_t1 = T1(token=token, token_updater=mock_saver, **mock_credentials)
        adv = new_t1.get('advertisers', 1)
        self.assertEqual(adv.id, 1)

    @responses.activate
    def test_refresh_after_expiration(self):
        def token_callback(request):
            if 'grant_type=authorization_code' in request.body:
                filename = 'access_token.json'
            elif 'grant_type=refresh_token' in request.body:
                filename = 'access_token_refreshed.json'
            else:
                raise ValueError('What is your grant type?')
            with open('tests/fixtures/json/' + filename) as f:
                return 200, {}, f.read()

        responses.add_callback(
            responses.POST,
            'https://api.mediamath.com/oauth2/v1.0/token',
            callback=token_callback,
            content_type='application/json'
        )

        token = self.t1.fetch_token(state='state', code='code')
        now = time()
        token.update({
            'expiration_time': int(now) - 1,
            'expires_at': now - 1,
        })

        with open('tests/fixtures/xml/advertiser.xml') as f:
            responses.add(responses.GET,
                          'https://api.mediamath.com/api/v2.0/advertisers/1',
                          body=f.read(),
                          content_type='application/xml')

        new_t1 = T1(token=token, token_updater=mock_saver, **mock_credentials)
        _ = new_t1.get('advertisers', 1)
        self.assertEqual(new_t1.session.token['access_token'], 'newaccesstoken')
        self.assertEqual(new_t1.session.token['refresh_token'], 'newrefreshtoken')
