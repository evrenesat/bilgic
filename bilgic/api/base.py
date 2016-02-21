# -*-  coding: utf-8 -*-
"""
"""
from __future__ import print_function, absolute_import

import uuid
from functools import wraps
from pycnic.core import WSGI, Handler
from bilgic.api.images import ListElements, ListLevels, ListGames
from bilgic.api.images import SearchImages
from bilgic.api.user import Login
from bilgic.api.user import Logout
from bilgic.lib.cache import Session
from bilgic.models import *


def get_user(handler):
    """ Lookup a user session or return None if one doesn't exist """

    sess = get_session(handler)
    if not sess:
        return None
    user_dict = sess.get('user')
    if not user_dict:
        return None
    return User._load_data(user_dict)


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



class app(WSGI):
    debug = True
    routes = [
        # ('/home', Home()),
        ('/levels_of/([\w]+)', ListElements()),
        ('/search_image/([\w]+)', SearchImages()),
        ('/search_image/([\w]+)/(\d+)', SearchImages()),
        ('/search_image/([\w]+)/(\d+)/(\d+)', SearchImages()),
        ('/elements_of/([\w]+)', ListLevels()),
        ('/games', ListGames()),
        ('/login', Login()),
        ('/logout', Logout())
    ]


if __name__ == "__main__":

    from wsgiref.simple_server import make_server

    try:
        print("Serving on 0.0.0.0:8080...")
        make_server('0.0.0.0', 8080, app).serve_forever()
    except KeyboardInterrupt:
        pass
    print("Done")
