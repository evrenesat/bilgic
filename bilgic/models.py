# -*-  coding: utf-8 -*-
"""
"""

# Copyright (C) 2015 Evren Esat Ozkan.

from __future__ import print_function, absolute_import

from pycnic.errors import HTTP_401
from pyoko import Model, ListNode, field
from pyoko.fields import BaseField
from pyoko.lib.utils import get_object_from_path
from bilgic.lib.cache import SettingsCache
from passlib.hash import pbkdf2_sha512

CurrentProviderData = SettingsCache('current_provider_data')


class JSONField(BaseField):
    solr_type = 'string'


class User(Model):
    username = field.String(index=True)
    name = field.String(index=True)
    email = field.String(index=True)
    question = field.String(index=True)
    answer = field.String(index=True)
    password = field.String(index=True)

    def pre_save(self):
        # this is pre-save hook
        # encrypt password if not already encrypted

        if self.answer and not self.answer.startswith('pbkdf2'):
            self.answer = pbkdf2_sha512.encrypt(self.answer)
        if not self.password.startswith('pbkdf2'):
            self.password = pbkdf2_sha512.encrypt(self.password)

    def check_password(self, clean_password):
        # check password hash against given clean password input
        if not pbkdf2_sha512.verify(self.password, clean_password):
            raise HTTP_401("Invalid password")


class Provider(Model):
    name = field.String(index=True)
    module_name = field.String()
    active = field.Boolean(index=True, default=True)
    priority = field.Integer(index=True)
    credentials = JSONField()

    _api = None

    def __unicode__(self):
        return "%s API Provider (A:%s | P:%s)" % (self.name.upper(),
                                                  self.active,
                                                  self.priority)

    def post_save(self):
        Provider.api = None
        CurrentProviderData.delete()

    @classmethod
    def get_current_provider_dict(cls):
        riak_obj = cls.objects.set_params(sort='priority desc').data().filter(active=True)[0]
        provider_dict = riak_obj.data
        provider_dict['key'] = riak_obj.key
        return provider_dict

    @classmethod
    def get_provider_api(cls):
        if cls._api is None:
            try:
                cp = CurrentProviderData.get()
                if not cp:
                    cp = CurrentProviderData.set(cls.get_current_provider_dict())
                cls._api = get_object_from_path("bilgic.providers.%s.api" % cp['module_name'])
                cls._api.set_credentials(**cp['credentials'])
            except:
                # print(cp)
                raise
        return cls._api


class Game(Model):
    name = field.String(index=True)
    active = field.Boolean(index=True)


class Element(Model):
    name = field.String(index=True)
    text = field.String(index=True)
    content = field.Text()
    url = field.String(index=True)
    provider = Provider()
    tags = field.String(index=True)
    type = field.Integer(choices=((1, 'Image'), (2, 'Text')), default=1)


class Level(Model):
    name = field.String()
    game = Game()
    creator = User()

    class Pairs(ListNode):
        elm1 = Element()
        elm2 = Element()

    def get_pairs(self):
        return [(pair.elm1.clean_data(),
                 pair.elm2.clean_data())
                for pair in self.Pairs]


