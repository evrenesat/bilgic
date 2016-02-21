# -*-  coding: utf-8 -*-
"""
"""
from pycnic.core import Handler

from bilgic.models import Provider, Game, Level, Element


class SearchImages(Handler):
    def get(self, keyword, page=1, per_page=10):
        return dict(results=Provider.get_provider_api().get_images(keyword,
                                                                   int(page),
                                                                   int(per_page)),
                    status="success"
                    )


class ListGames(Handler):
    def get(self):
        return dict(games=[[g.key, g.data] for g in
                           Game.objects.data().filter(active=True)],
                    status="success"
                    )


class ListLevels(Handler):
    def get(self, game_id):
        return dict(levels=[{"name": l.data['name'], 'key': l.key} for l in
                            Level.objects.data().filter(game_id=game_id)],
                    status="success")


class ListElements(Handler):
    def get(self, level_id):
        return {"elements": Level.objects.get(level_id).get_pairs(),
                "status": "success"}
