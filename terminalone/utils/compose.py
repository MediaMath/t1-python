# -*- coding: utf-8 -*-

from functools import reduce

def compose(*functions):
	return reduce(lambda f, g: lambda x: f(g(x)), functions)
