# -*-  coding: utf-8 -*-
"""
"""
from pycnic.core import WSGI, Handler

from bilgic.api.base import Api
from bilgic.api.images import GetLevel, ListLevels, ListGames, SetLevel, SearchImages
from bilgic.api.user import Login, Register, Logout



class app(WSGI):
    debug = True

    def before(self):
        self.response.set_header("Access-Control-Allow-Origin", "*")

    routes = [
        ('/search_image/([\w\s]+)', SearchImages()),  # /keyword
        ('/search_image/([\w\s]+)/(\d+)', SearchImages()),  # /keyword/page
        ('/search_image/([\w\s]+)/(\d+)/(\d+)', SearchImages()),  # /keyword/page/per_page
        ('/get_level/([\w]+)', GetLevel()),  # /level_key
        ('/set_level', SetLevel()),
        ('/game_levels/([\w]+)', ListLevels()),
        ('/games', ListGames()),
        ('/login', Login()),
        ('/logout', Logout()),
        ('/register', Register()),
        ('/api', Api()),
    ]


if __name__ == "__main__":

    from wsgiref.simple_server import make_server

    try:
        print("Serving on 0.0.0.0:8080...")
        make_server('0.0.0.0', 8080, app).serve_forever()
    except KeyboardInterrupt:
        pass
    print("Done")
