#!/usr/bin/env python
# -*-  coding: utf-8 -*-
"""
"""

# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.
from pyoko.manage import ManagementCommands, environ

environ['PYOKO_SETTINGS'] = 'bilgic.settings'

if __name__ == '__main__':
    ManagementCommands()
