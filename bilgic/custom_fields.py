# -*-  coding: utf-8 -*-
"""
"""
from __future__ import print_function, absolute_import
from json import loads, dumps
import six
from pyoko.fields import BaseField


class JSONField(BaseField):
    solr_type = 'string'
    # TODO: serialization can be lazy


    def __get__(self, instance, cls=None):
        if cls is None or instance is None:
            return six.text_type(self.__class__)
        return loads(instance._field_values.get(self.name, '[]'))


    def __set__(self, instance, value):
        if value and isinstance(value, (dict, list)):
            instance._field_values[self.name] = dumps(value)

