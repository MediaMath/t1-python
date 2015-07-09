# -*- coding: utf-8 -*-
"""Filters for use with T1.find"""

IN = '()'
NULL = ':'
NOT_NULL = ':!'
# Equals operator is *different* between M&E (==) and Picard (=)
EQUALS = '=='
NOT_EQUALS = '!='
GREATER = '>'
GREATER_OR_EQUAL = '>='
LESS = '<'
LESS_OR_EQUAL = '<='
CASE_INS_STRING = '=:'
# Following are not available in M&E API
# CASE_INS_NOT_STRING = '!:'
# CASE_SENS_STRING = '=~'
# CASE_SENS_NOT_STRING = '!~'
