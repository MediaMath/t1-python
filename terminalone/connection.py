# -*- coding: utf-8 -*-
"""Provides connection object for T1."""

from __future__ import absolute_import
from requests import Session
from .errors import ClientError
from .utils import PATHS
from .xmlparser import XMLParser, ParseError


class Connection(object):
    """Base connection object for TerminalOne session"""
    VALID_ENVS = frozenset(['production', 'qa'])
    API_BASES = {
        'production': 'api.mediamath.com',
    }
    def __init__(self,
                 environment='production',
                 api_base=None,
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
                                       Connection.API_BASES[environment])
            except KeyError:
                raise ClientError("Environment: {!r}, does not exist."
                                  .format(environment))
        else:
            Connection.__setattr__(self, 'api_base', api_base)
        if _create_session:
            Connection.__setattr__(self, 'session', Session())

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

        try:
            result = XMLParser(response)
        except ParseError as exc:
            Connection.__setattr__(self, 'response', response)
            raise ClientError('Could not parse XML response: {!r}'.format(exc))
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

        try:
            result = XMLParser(response)
        except ParseError as exc:
            Connection.__setattr__(self, 'response', response)
            raise ClientError('Could not parse XML response: {!r}'.format(exc))
        except Exception:
            Connection.__setattr__(self, 'response', response)
            raise
        return iter(result.entities), result.entity_count
