# -*- coding: utf-8 -*-
"""Get credentials from file or environment variables"""

import os
from functools import reduce
from dotenv import load_dotenv

dotenv_path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path)


def dpath(dict_, path):
    """Dig into dictionary by string path. e.g.

    dpath({'a': {'b': {'c': 'd'}}}, 'a.b') -> {'c': 'd'}
    """
    from operator import getitem
    paths = path.split('.')
    return reduce(
        getitem,
        paths,
        dict_
    )


def credentials(filename=None, root=None):
    """Get credentials from JSON file or environment variables.

    JSON file should have credentials in the form of:
    {
        "username": "myusername",
        "password": "supersecret",
        "api_key": "myapikey"
    }

    If filename not provided, fall back on environment variables:
    - T1_API_USERNAME
    - T1_API_PASSWORD
    - T1_API_KEY

    :param filename: str filename of JSON file containing credentials.
    :param root: str path to get to credentials object. For instance, in object:
        {
            "credentials": {
                "api": {
                    "username": "myusername",
                    "password": "supersecret",
                    "api_key": "myapikey"
                }
            }
        }
        "root" is "credentials.api"
    :return: dict[str]str
    :raise: TypeError: no JSON file or envvars
    """

    if filename is not None:
        import json
        with open(filename, 'rb') as f:
            conf = json.load(f)
        if root is not None:
            conf = dpath(conf, root)
    else:
        import os
        try:
            conf = {
                'username': os.environ.get('T1_API_USERNAME'),
                'password': os.environ.get('T1_API_PASSWORD'),
                'api_key': os.environ.get('T1_API_KEY'),
                'client_id': os.environ.get('T1_CLIENT_ID'),
                'client_secret': os.environ.get('T1_CLIENT_SECRET'),
            }
        except KeyError:
            raise TypeError('Must either supply JSON file of credentials'
                            ' or set environment variables '
                            'T1_API_{USERNAME,PASSWORD,KEY}')

    return conf
