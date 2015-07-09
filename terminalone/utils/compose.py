# -*- coding: utf-8 -*-
"""Compose functions like you're using functional programming"""

from functools import reduce

def compose(*functions):
    """Compose functions like you're using functional programming"""
    return reduce(lambda f, g: lambda x: f(g(x)), functions)
