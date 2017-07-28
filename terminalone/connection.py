# -*- coding: utf-8 -*-
"""Provides connection object for T1."""

from __future__ import absolute_import
from requests import Session, post
from requests.utils import default_user_agent
from requests_oauthlib import OAuth2Session
from .config import ACCEPT_HEADERS, API_BASES, SERVICE_BASE_PATHS, AUTH_BASES
from .errors import ClientError, T1Error
from .metadata import __version__
from .xmlparser import XMLParser, ParseError
from .jsonparser import JSONParser
import json
import jwt


def _generate_user_agent(name='t1-python'):
    return '{name}/{version} {ua}'.format(name=name, version=__version__,
                                          ua=default_user_agent())


class Connection(object):
    """Base connection object for TerminalOne session"""
    user_agent = _generate_user_agent()

    def __init__(self,
                 environment='production',
                 api_base=None,
                 json=False,
                 auth_params=None,
                 _create_session=False):
        """Sets up Requests Session to be used for all connections to T1.

        :param environment: str to look up API Base to use. e.g. 'production'
            for https://api.mediamath.com/api/v2.0
        :param api_base: str API domain. should be the qualified domain name
            without trailing slash. e.g. "api.mediamath.com".
        :param json: bool use JSON header for serialization. Currently
            for internal experimentation, JSON will become the default in a
            future version.
        :param auth_params: dict set of auth parameters:
            "method" required argument. Determines session handler.
            "oauth2" => "client_id", "client_secret", "redirect_uri", "token_updater"
            "oauth2-ro" => "client_id", "client_secret", "username", "password"
            "cookie" => "username", "password", "api_key"
        :param _create_session: bool flag to create a Requests Session.
            Should only be used for initial T1 instantiation.
        """
        if api_base is not None:
            Connection.__setattr__(self, 'api_base', api_base)
        else:
            try:
                Connection.__setattr__(self, 'api_base',
                                       API_BASES[environment])
            except KeyError:
                raise ClientError("Environment: {!r}, does not exist."
                                  .format(environment))

        try:
            Connection.__setattr__(self, 'auth_base',
                                   AUTH_BASES[environment])
        except KeyError:
            raise ClientError("Auth URL for environment: {!r} does not exist."
                              .format(environment))

        Connection.__setattr__(self, 'json', json)
        Connection.__setattr__(self, 'auth_params', auth_params)
        if _create_session:
            self._create_session()

    def _oauth2_session(self, **kwargs):
        refresh_url = '/'.join(['https:/', self.api_base,
                                SERVICE_BASE_PATHS['oauth2'], 'token'])
        refresh_kwargs = {'client_id': self.auth_params['api_key'],
                          'client_secret': self.auth_params['client_secret']}
        session = OAuth2Session(
            client_id=self.auth_params['api_key'],
            auto_refresh_url=refresh_url,
            auto_refresh_kwargs=refresh_kwargs,
            token=self.auth_params['token'],
            token_updater=self.auth_params['token_updater'],
            **kwargs
        )
        session.headers['User-Agent'] = self.user_agent
        session.params = {'api_key': self.auth_params['api_key']}
        if self.json:
            self.session.headers['Accept'] = ACCEPT_HEADERS['json']
        return session

    def _create_session(self):
        method = self.auth_params['method']
        if method == 'oauth2':
            session = self._oauth2_session()
        else:
            session = Session()
            session.headers['User-Agent'] = self.user_agent
            if method != 'oauth2-resourceowner':
                session.params = {'api_key': self.auth_params['api_key']}
            if self.json:
                session.headers['Accept'] = ACCEPT_HEADERS['json']

        Connection.__setattr__(self, 'session', session)

    def _auth_cookie(self, username, password, api_key):
        """Authenticate by generating a session cookie.

        The traditional way of authenticating by making a POST request to /login
        endpoint and storing the returned session cookie.
        """
        user, _ = self._post(SERVICE_BASE_PATHS['mgmt'], 'login', data={
            'user': username,
            'password': password,
            'api_key': api_key,
        })
        self._check_session(user=user)

    def _auth_session_id(self, session_id, api_key, expires=None):
        """Authenticate using a passed-in session ID.

        This is the only real method for apps not doing their own login; for
        instance, apps in T1 are expected to take in a passed sesssion ID and
        authenticate using that. Hopefully with OAuth2 this should fade away.
        """
        from time import time
        self.session.cookies.set(
            name='adama_session',
            value=session_id,
            domain=self.api_base,
            expires=(expires or int(time() + 86400)),
        )
        self._check_session()

    # these should be stored as instance vars, because they aren't specific
    # to the user. Except for redirect_uri, because that gets saved as an
    # instance var for the session
    def authorization_url(self, redirect_uri=None):
        """Authenticate using OAuth2"""
        auth_url = '/'.join(['https:/', self.api_base,
                             SERVICE_BASE_PATHS['oauth2'], 'authorize'])
        if redirect_uri is None:
            try:
                redirect_uri = self.auth_params['redirect_uri']
            except KeyError:
                raise ClientError('Redirect URI not provided!')

        session = self._oauth2_session(redirect_uri=redirect_uri)
        return session.authorization_url(auth_url)

    def fetch_token(self, state=None, code=None,
                    authorization_response_url=None, set_session=False):
        token_url = '/'.join(['https:/',
                              self.api_base,
                              SERVICE_BASE_PATHS['oauth2'],
                              'token'])
        session = self._oauth2_session(state=state)
        token = session.fetch_token(
            token_url,
            code=code,
            authorization_response=authorization_response_url,
            client_secret=self.auth_params['client_secret']
        )
        if set_session:
            Connection.__setattr__(self, 'session', session)
        return token

    def fetch_resource_owner_password_token(self, username, password, client_id, client_secret):
        payload = {
            'grant_type': 'password',
            'username': username,
            'password': password,
            'client_id': client_id,
            'client_secret': client_secret,
            'scope': 'openid'
        }

        token_url = '/'.join(['https:/',
                              self.auth_base,
                              'oauth',
                              'token'])
        response = post(
            token_url, json=payload, stream=True)
        if response.status_code != 200:
            raise ClientError(
                'Failed to get OAuth2 token. Error: ' + response.text)
        id_token = json.loads(response.text)['id_token']
        user = jwt.decode(id_token, verify=False)
        Connection.__setattr__(self, 'user_id',
                               user['name'])
        Connection.__setattr__(self, 'username',
                               user['nickname'])
        self.session.headers['Authorization'] = 'Bearer ' + id_token
        return id_token, user

    def _check_session(self, user=None):
        """Set session parameters username, user_id, session_id.

        Call after posting auth. If given a session ID (and no auth is called),
        check session
        """
        if user is None:
            user, _ = self._get(SERVICE_BASE_PATHS['mgmt'], 'session')

        Connection.__setattr__(self, 'user_id',
                               int(user['id']))
        Connection.__setattr__(self, 'username',
                               user['name'])
        Connection.__setattr__(self, 'session_id',
                               self.session.cookies['adama_session'])

    def _get(self, path, rest, params=None):
        """Base method for subclasses to call.
        :param path: str API path (can be from terminalone.utils.PATHS)
        :param rest: str rest of url (module-specific path, )
        :param params: dict query string params
        """
        url = '/'.join(['https:/', self.api_base, path, rest])
        response = self.session.get(url, params=params, stream=True)
        return self._parse_response(response)

    def _post(self, path, rest, data=None, json=None):
        """Base method for subclasses to call.
        :param url: str API URL
        :param data: dict POST data for formdata posts
        :param json: dict POST data for json posts
        """
        if data is None and json is None:
            raise ClientError('No POST data.')
        if data and json:
            raise ClientError('Cannot specify both data and json POST data.')

        url = '/'.join(['https:/', self.api_base, path, rest])
        response = self.session.post(url, data=data, json=json, stream=True)
        return self._parse_response(response)

    def _parse_response(self, response):
        content_type = response.headers.get('Content-type')
        if content_type is None:
            raise T1Error(None, 'No content type header returned')

        parser, response_body = self._get_parser(content_type, response)

        try:
            result = parser(response_body)
        except ParseError as exc:
            Connection.__setattr__(self, 'response', response)
            raise T1Error(
                None, 'Could not parse response: {!r}'.format(exc.caught))
        except Exception:
            Connection.__setattr__(self, 'response', response)
            raise
        return result.entities, result.entity_count

    @staticmethod
    def _get_parser(content_type, response):
        if 'xml' in content_type:
            parser = XMLParser
            response_body = response.content
        elif 'json' in content_type:
            parser = JSONParser
            response_body = response.text
        else:
            raise T1Error(
                None, 'Cannot handle content type: {}'.format(content_type))
        return parser, response_body

    def _get_service_path(self, entity_name=None):
        if not entity_name:
            entity_name = self.collection
        return SERVICE_BASE_PATHS.get(entity_name, SERVICE_BASE_PATHS['mgmt'])
