# -*-  coding: utf-8 -*-
"""
"""

# Copyright (C) 2015 Evren Esat Ozkan.

from __future__ import print_function, absolute_import
from pyoko import Model, ListNode, field
from pyoko.lib.utils import get_object_from_path

from .custom_fields import JSONField


class Game(Model):
    name = field.String()


class Elements(Model):
    name = field.String()
    text = field.String()
    url = field.String()
    tags = field.String()

    class Types(ListNode):
        type = field.String()


class Level(Model):
    name = field.String()
    game = Game()

    class Elements(ListNode):
        element = Elements()


class Provider(Model):
    name = field.String()
    module_name = field.String()
    active = field.Boolean()
    priority = field.Integer()
    credentials = JSONField()


    @classmethod
    def get_provider(cls, name=None):
        provider = cls.objects.get(name=name) if name \
            else cls.objects.set_params(sort='priority').filter()[0]
        api = get_object_from_path("providers.%s.api" % provider.module_name)
        api.set_credentials(**provider.credentials)
        return api

    def search(self, keywords):
        pass

    def set_credentials(self):
        self.api.set_credentials(**kwargs)
