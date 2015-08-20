# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import

import unittest
import responses
import requests

from terminalone import T1
from terminalone import errors

API_BASE = 'api.mediamath.com'


def patched_extract_cookies_to_jar(jar, request, response):
    """Patched version to support mocked HTTPResponses from Responses.

    :param jar: cookielib.CookieJar (not necessarily a RequestsCookieJar)
    :param request: our own requests.Request object
    :param response: urllib3.HTTPResponse object
    """
    if not (hasattr(response, '_original_response') and
                response._original_response):
        # just grab the headers from the mocked response object
        res = requests.cookies.MockResponse(response.headers)
    else:
        # the _original_response field is the wrapped httplib.HTTPResponse object
        # pull out the HTTPMessage with the headers and put it in the mock:
        res = requests.cookies.MockResponse(response._original_response.msg)

    req = requests.cookies.MockRequest(request)
    jar.extract_cookies(res, req)


requests.sessions.extract_cookies_to_jar = patched_extract_cookies_to_jar
requests.adapters.extract_cookies_to_jar = patched_extract_cookies_to_jar


class TestT1Login(unittest.TestCase):
    """docstring for TestT1Login"""

    @responses.activate
    def test_correct_login_works(self):
        expected_session = 'd24f41277ae4c202dda876676b0006585b20f64f'
        expected_user = 'user'
        expected_user_id = 1

        def login_callback(_):
            body = open('fixtures/session.xml').read()
            response_headers = {
                'Set-Cookie': 'adama_session=' + expected_session,
            }
            return 200, response_headers, body

        mock_credentials = {
            'username': expected_user,
            'password': 'password',
            'api_key': 'api_key',
        }
        responses.add_callback(
            responses.POST, 'https://api.mediamath.com/api/v2.0/login',
            callback=login_callback,
            content_type='application/xml')

        t1 = T1(auth_method='cookie',
                api_base=API_BASE,
                **mock_credentials)

        assert hasattr(t1, 'user_id'), 'No user ID present'
        assert (t1.user_id == expected_user_id), 'incorrect user ID returned'
        assert (t1.username == expected_user), 'user name is incorrect'
        assert (t1.session_id == expected_session), 'session id not correct'

    @responses.activate
    def test_incorrect_login_raises_error(self):
        def login_callback(_):
            body = open('fixtures/auth_error.xml').read()
            return 401, {}, body

        mock_credentials = {
            'username': 'bad_user',
            'password': 'bad_pass',
            'api_key': 'api_key',
        }
        responses.add_callback(responses.POST, 'https://api.mediamath.com/api/v2.0/login',
                               callback=login_callback)

        with self.assertRaises(errors.AuthRequiredError) as cm:
            T1(auth_method='cookie',
               api_base=API_BASE,
               **mock_credentials)

        exc = cm.exception
        self.assertEqual(exc.message, 'Authentication error')

    @responses.activate
    def test_no_key_fails(self):
        def login_callback(_):
            body = open('fixtures/login_no_key.xml').read()
            return 403, {}, body

        mock_credentials = {
            'username': 'user',
            'password': 'pass',
        }
        responses.add_callback(responses.POST, 'https://api.mediamath.com/api/v2.0/login',
                               callback=login_callback)

        with self.assertRaises(errors.T1Error) as cm:
            T1(auth_method='cookie',
               api_base=API_BASE,
               **mock_credentials)

        exc = cm.exception
        self.assertEqual('<h1>Developer Inactive</h1>', exc.message)

    @responses.activate
    def test_no_user_fails(self):
        def login_callback(_):
            body = open('fixtures/login_badrequest.xml').read()
            return 400, {}, body

        mock_credentials = {
            'password': 'pass',
            'api_key': 'api_key',
        }
        responses.add_callback(responses.POST, 'https://api.mediamath.com/api/v2.0/login',
                               callback=login_callback)

        with self.assertRaises(errors.ValidationError) as cm:
            T1(auth_method='cookie',
               api_base=API_BASE,
               **mock_credentials)

        exc = cm.exception
        self.assertEqual('invalid', exc.message)
