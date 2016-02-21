# -*-  coding: utf-8 -*-
"""
"""
from pycnic.core import Handler

from bilgic.api.base import get_user
from bilgic.lib.utils import clean_value
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
        return dict(games=[clean_value(g) for g in Game.objects.filter(active=True)],
                    status="success"
                    )


class ListLevels(Handler):
    def get(self, game_id):
        return dict(levels=[{"name": l.data['name'], 'key': l.key} for l in
                            Level.objects.data().filter(game_id=game_id)],
                    status="success")


class GetLevel(Handler):
    def get(self, level_id):
        level = Level.objects.get(level_id)
        return {
            "level": level.clean_value(),
            "elements": [clean_value(e.element) for e in level.Elements],
            "status": "success"}


class SetLevel(Handler):
    def post(self):
        level = Level(**self.data["level"]).save()
        for elm in self.data["elements"]:
            level.Elements(element=Element(**elm))
        user = get_user(self)
        if user:
            level.creator = user
        level.save()
        return {"message": "level_edit_saved",
                "new_level_id": level.key,
                "status": "success"}
