# -*-  coding: utf-8 -*-
"""
"""
from __future__ import print_function, absolute_import

import uuid
from functools import wraps

from pycnic.core import Handler

from bilgic.lib.cache import Session
from bilgic.models import *


class Api(Handler):
    """ Clears a user's session """

    def get(self):
        from bilgic.api import app
        self.response.set_header("Content-Type", "text/plain")
        return "API Docs\n\n   -  " + " \n   -  ".join(dict(app.routes).keys())


def get_user(handler):
    """ Lookup a user session or return None if one doesn't exist """

    sess = get_session(handler)
    if not sess:
        return None
    user_dict = sess.get('user')
    if not user_dict:
        return None
    user = User._load_data(user_dict)
    user.key = sess.get("user_id")
    return user


def get_session(handler):
    sess_id = handler.request.cookies.get("session_id")
    if not sess_id:
        sess_id = uuid.uuid4().hex
        handler.response.cookies.set("session_id", sess_id)
    return Session(sess_id)


def requires_login():
    """ Wrapper for methods that require login """

    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not get_user(args[0]):
                raise HTTP_401("I can't let you do that")
            return f(*args, **kwargs)

        return wrapped

    return wrapper
