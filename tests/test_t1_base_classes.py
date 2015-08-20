# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import

import unittest
import responses
import requests

from terminalone import T1

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
        EXPECTED_SESSION = 'd24f41277ae4c202dda876676b0006585b20f64f'
        EXPECTED_USER = 'user'
        EXPECTED_USER_ID = 1

        def login_callback(request):
            body = open('fixtures/session.xml').read()
            response_headers = {
                'Set-Cookie': 'adama_session='+EXPECTED_SESSION,
            }
            return (200, response_headers, body)



        mock_credentials = {
            'username': EXPECTED_USER,
            'password': EXPECTED_USER_ID,
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
        assert (t1.user_id == EXPECTED_USER_ID), 'incorrect user ID returned'
        assert (t1.username == EXPECTED_USER), 'user name is incorrect'
        assert (t1.session_id == EXPECTED_SESSION), 'session id not correct'

    def test_incorrect_login_raises_error(self):
        pass

    def test_no_data_fails(self):
        pass


class TestXMLParsing(unittest.TestCase):
    """docstring for TestXMLParsing"""

    def test_auth_error(self):
        pass

    def test_invalid_login(self):
        pass

    def test_status_ok(self):
        pass

    def test_no_entities(self):
        pass

    def test_one_entity(self):
        pass

    def test_multiple_entities(self):
        pass

    def test_multiple_pages(self):
        pass
