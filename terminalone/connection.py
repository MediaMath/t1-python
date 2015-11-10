# -*- coding: utf-8 -*-
"""Provides connection object for T1."""

from __future__ import absolute_import
from requests import Session
from requests.utils import default_user_agent
from .config import ACCEPT_HEADERS, API_BASES, PATHS, VALID_ENVS
from .errors import ClientError, ParserException
from .metadata import __version__
from .xmlparser import XMLParser, ParseError
from .jsonparser import JSONParser


def _generate_user_agent(name='t1-python'):
    return '{name}/{version} {ua}'.format(name=name, version=__version__,
                                          ua=default_user_agent())


class Connection(object):
    """Base connection object for TerminalOne session"""

    def __init__(self,
                 environment='production',
                 api_base=None,
                 json=False,
                 _create_session=True):
        """Sets up Requests Session to be used for all connections to T1.

        :param environment: str to look up API Base to use. e.g. 'production'
        for https://api.mediamath.com/api/v2.0
        :param api_base: str API domain. should be the qualified domain name without
        trailing slash. e.g. "api.mediamath.com".
        :param _create_session: bool flag to create a Requests Session.
        Should only be used for initial T1 instantiation.
        """

        if api_base is None:
            try:
                Connection.__setattr__(self, 'api_base',
                                       API_BASES[environment])
            except KeyError:
                raise ClientError("Environment: {!r}, does not exist."
                                  .format(environment))
        else:
            Connection.__setattr__(self, 'api_base', api_base)

        Connection.__setattr__(self, 'json', json)

        if json:
            Connection.__setattr__(self, '_parser', JSONParser)
        else:
            Connection.__setattr__(self, '_parser', XMLParser)

        if _create_session:
            Connection.__setattr__(self, 'session', Session())
            self.session.headers['User-Agent'] = _generate_user_agent()
            if json:
                self.session.headers['Accept'] = ACCEPT_HEADERS['json']

    def _check_session(self, user=None):
        """Set session parameters username, user_id, session_id.

        Call after posting auth. If given a session ID (and no auth is called),
        check session
        """
        if user is None:
            user, _ = self._get(PATHS['mgmt'], 'session')

        user = next(user)
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

        if self.json:
            response_body = response.text
        else:
            response_body = response.content

        try:
            result = self._parser(response_body)
        except ParserException as exc:
            Connection.__setattr__(self, 'response', response)
            raise ClientError('Could not parse response: {!r}'.format(exc.caught))
        except Exception:
            Connection.__setattr__(self, 'response', response)
            raise
        return iter(result.entities), result.entity_count

    def _post(self, path, rest, data):
        """Base method for subclasses to call.
        :param url: str API URL
        :param data: dict POST data
        """
        if not data:
            raise ClientError('No POST data.')

        url = '/'.join(['https:/', self.api_base, path, rest])
        response = self.session.post(url, data=data, stream=True)

        if self.json:
            response_body = response.text
        else:
            response_body = response.content

        try:
            result = self._parser(response_body)
        except ParseError as exc:
            Connection.__setattr__(self, 'response', response)
            raise ClientError('Could not parse response: {!r}'.format(exc))
        except Exception:
            Connection.__setattr__(self, 'response', response)
            raise
        return iter(result.entities), result.entity_count
