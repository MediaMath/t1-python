# -*- coding: utf-8 -*-
"""Compose functions like you're using functional programming.

See: https://mathieularose.com/function-composition-in-python/
"""

from functools import reduce


def compose(*functions):
    """Compose functions like you're using functional programming.

    >>> import operator
    >>> negative_sum = compose(operator.neg, sum)
    >>> negative_sum(range(5))
    -10
    >>> unique_sorted = compose(sorted, set)
    >>> unique_sorted('hello')
    ['e', 'h', 'l', 'o']

    :param functions: functions to compose.
    :return: function
    """
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)
