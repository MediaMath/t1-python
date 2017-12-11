# -*- coding: utf-8 -*-
"""Provides exception and error handling for T1 API calls."""

from __future__ import absolute_import
from .vendor import six


class T1Error(Exception):
    """Base exception class for the module. To catch all errors, catch this.

    T1Error encompasses errors that occur both from the client
    (bad request, bad formation of properties, etc), to errors returned by the
    server (validation errors, login errors, etc). Sets code and message attributes.
    """

    def __init__(self, code, content, body=None):
        self.code = code
        self.message = content
        self.body = body
        super(T1Error, self).__init__(content)

    def __str__(self):
        return repr('Unknown Error. Code: {code}. Message: {msg}'
                    .format(code=self.code, msg=self.message))


class ClientError(T1Error):
    """Used for improper usages of the module.

    Improper usage includes attempting to retrieve a collection not in T1,
    attempting to send data that doesn't match an API object, etc.
    """

    def __init__(self, content, code=None):
        super(ClientError, self).__init__(code, content)

    def __str__(self):
        return repr(self.message)


T1ClientError = ClientError


class APIError(T1Error):
    """Base class that includes error code and message."""

    def __str__(self):
        return repr('{code}: {msg}\n'.format(code=self.code, msg=self.message))


T1APIError = APIError


class AuthRequiredError(APIError):
    """Raised on no authentication information or improper authentication"""
    pass


class ValidationError(APIError):
    """Raised on validation error on POST"""

    def __init__(self, code, content, body=None):
        msg_list = ['{}: {}'.format(error, val['error'])
                    for (error, val) in six.iteritems(content)]
        messages = [code] + msg_list
        messages = '\n'.join(messages)
        super(ValidationError, self).__init__(code, messages, body)

    def __str__(self):
        return self.message


class NotFoundError(APIError):
    """Raised on item not found"""
    pass


class LoginError(T1Error):
    """Exception class for invalid T1 Logins. Returns details of invalid login.

    If you encounter this class, it's because there's an issue with your T1 login.
    Logins are defined in the config file, and need to be kept up-to-date.
    """

    def __init__(self, code, content, credentials):
        super(LoginError, self).__init__(code, content)
        self.credentials = credentials

    def __str__(self):
        return repr('{}: {} -- {}'.format(self.code, self.message,
                                          self.credentials))


class ParserException(Exception):
    def __init__(self, caught):
        self.caught = caught

# Map known status.code responses to Exceptions. 'ok' signifies no exception,
# so that is None. 'invalid' can have many errors and needs
# an additional level of parsing, while the others can be instantiated directly.
STATUS_CODES = {
    'ok': None,
    'invalid': True,
    'not_found': NotFoundError,
    'auth_required': AuthRequiredError,
    'auth_error': AuthRequiredError,
    'error': APIError,
    'bad_request': ClientError,
}
