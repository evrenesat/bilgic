#!/usr/bin/env python
# -*-  coding: utf-8 -*-
"""
"""

# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.
from pyoko.manage import ManagementCommands, environ, Command

environ['PYOKO_SETTINGS'] = 'bilgic.settings'


class CreateLevel(Command):
    CMD_NAME = 'create_level'
    HELP = 'Creates a new level with given keyword'
    PARAMS = [
        {'name': 'game_name', 'required': True, 'help': 'Code name of game'},
        {'name': 'level_name', 'required': True, 'help': 'Set level name'},
        {'name': 'keyword', 'required': True, 'help': 'Keyword for images'},
        {'name': 'rating', 'default': 10, 'help': 'Rating code'},
    ]

    def run(self):
        from models import Provider, Level, Game, User, Element
        keyword = self.manager.args.keyword
        api = Provider.get_provider_api()
        images = api.get_images(keyword)
        user = User.objects.filter(super=True)[0]
        game = Game.objects.get(code_name=self.manager.args.game_name)
        level = Level(name=self.manager.args.level_name, game=game, creator=user).save()
        for img in images:
            level.Elements(element=Element(content=img, tags=keyword, name=keyword).save())
        level.save()

if __name__ == '__main__':
    ManagementCommands()
