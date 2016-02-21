# -*-  coding: utf-8 -*-
"""
"""
from __future__ import print_function, absolute_import

import uuid
from functools import wraps
from pycnic.core import WSGI, Handler
from pycnic.errors import HTTP_401, HTTP_400, HTTP_404
from pyoko.exceptions import ObjectDoesNotExist

from bilgic.lib.cache import Session
from bilgic.models import *


def get_user(request):
    """ Lookup a user session or return None if one doesn't exist """

    sess = get_session(request)
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
            if not get_user(args[0].request):
                raise HTTP_401("I can't let you do that")
            return f(*args, **kwargs)

        return wrapped

    return wrapper


class ListGames(Handler):
    def get(self):
        return [[g.key, g.data]
                for g in
                Game.objects.data().filter(active=True)]


class ListLevels(Handler):
    def get(self, game_id):
        return [{"name": l.data['name'],
                 'key': l.key}
                for l in
                Level.objects.data().filter(game_id=game_id)]


class ListElements(Handler):
    def get(self, level_id):
        level = Level.objects.data().get(level_id)
        return {"level": level.data,
                'key': level.key}


#
# class Home(Handler):
#     """ Handler for a message with the user's name """
#
#     @requires_login()
#     def get(self):
#         user = get_user(self)
#         return {"message": "Hello, %s" % (user.get("username"))}
#
#     @requires_login()
#     def post(self):
#         return self.get()


class Login(Handler):
    """ Create a session for a user """

    def post(self):

        username = self.request.data.get("username")
        password = self.request.data.get("password")

        if not username or not password:
            raise HTTP_400("Please specify username and password")

        # See if a user exists with those params
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            raise HTTP_404("Invalid username")
        user.check_password(password)

        # Create a new session
        sess = get_session(self)
        sess.set(user=user.clean_value())
        return {"message": "Logged in", "session_id": sess.session_id}


class Logout(Handler):
    """ Clears a user's session """

    def post(self):
        sess = get_session(self)
        sess.set('user', None)
        return {"message": "logged out"}


class app(WSGI):
    routes = [
        # ('/home', Home()),
        ('/levels_of/([\w]+', ListElements()),
        ('/elements_of/([\w]+', ListLevels()),
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
