# -*-  coding: utf-8 -*-
"""project settings"""
__author__ = 'Evren Esat Ozkan'
from pyoko.settings import *
import os.path

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


REDIS_SERVER = '127.0.0.1:6379'

DEFAULT_BUCKET_TYPE = os.environ.get('DEFAULT_BUCKET_TYPE', 'bilgic_models')
