# -*- coding: utf-8 -*-
"""Provides configuration data"""

VALID_ENVS = frozenset(['production', 'qa'])

API_BASES = {
    'production': 'api.mediamath.com',
}

ACCEPT_HEADERS = {
    'json': 'application/vnd.mediamath.v1+json',
}

PATHS = {
    'mgmt': 'api/v2.0',
    'reports': 'reporting/v1/std',
    'uniques': 'uniques/v1',
    'oauth2': 'oauth2/v1.0',
}
