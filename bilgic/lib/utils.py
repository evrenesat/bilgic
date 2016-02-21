# -*-  coding: utf-8 -*-
"""
"""

def clean_value(obj):
    cv = obj.clean_value()
    cv['key'] = obj.key
    return cv
