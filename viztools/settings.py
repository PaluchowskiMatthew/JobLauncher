#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=R0801

# Copyright (c) 2016, Blue Brain Project
#                     Raphael Dumusc <raphael.dumusc@epfl.ch>
#                     Daniel Nachbaur <daniel.nachbaur@epfl.ch>
#                     Cyrille Favreau <cyrille.favreau@epfl.ch>
#
# This file is part of VizTools
# <https://github.com/BlueBrain/VizTools>
#
# This library is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License version 3.0 as published
# by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# All rights reserved. Do not distribute without further notice.

"""
Settings and default values for the viztools
"""

from collections import namedtuple

DEFAULT_ALLOCATOR_URI = 'https://visualization-dev.humanbrainproject.eu/viz'
DEFAULT_ALLOCATOR_API_VERSION = 'v1'
DEFAULT_ALLOCATOR_NAME = 'rendering-resource-manager'
DEFAULT_ALLOCATOR_SESSION_PREFIX = 'session'
DEFAULT_ALLOCATOR_CONFIG_PREFIX = 'config'
DEFAULT_ALLOCATOR_NB_NODES = 1
DEFAULT_ALLOCATOR_NB_CPUS = 8
DEFAULT_ALLOCATOR_NB_GPUS = 1
DEFAULT_ALLOCATOR_TIME = '1:00:00'
DEFAULT_ALLOCATOR_EXCLUSIVE = False

DEFAULT_STREAMER_NAME = 'image-streaming-service'
DEFAULT_STREAMER_API = 'v1'
DEFAULT_STREAMER_URI = 'https://visualization-dev.humanbrainproject.eu/viz/' + \
                        DEFAULT_STREAMER_NAME + '/' + DEFAULT_STREAMER_API + \
                        '/image_streaming_feed/demo'

DEFAULT_RENDERER = 'brayns'

SESSION_MAX_CONNECTION_ATTEMPTS = 5

DisplayWalls = namedtuple('DisplayWalls', ['FLOOR_0', 'FLOOR_5', 'FLOOR_6'])
DISPLAYWALLS = DisplayWalls('bbpav02.bbp.epfl.ch', 'bbpav05.bbp.epfl.ch', 'bbpav06.bbp.epfl.ch')
DISPLAYWALL_PORT = ":8888"

COLORMAP_SIMULATION = 'AAAAAgAAAAcAAAANAAAAEgAAABcAAAAdAAAAIgAAACcAAAAtAAAAMgAAADcAAAA9AAAAQgAAA' \
                      'EgAAABNAAAAUgAAAFgAAABdAAAAYgAAAGgAAABtAAAAcgAAAHgAAAB9AQAAggEAAIgBAACNAQ' \
                      'AAkgEAAJgBAACdAQAAogEAAKgBAACtAQAAsgEAALgBAAC9AQAAwwEAAMgBAADNAQAA0wEAANg' \
                      'BAADdAQAA4wEAAOgBAADtAQAA8wEAAPgBAAD9AgAA/gIAAP0CAAD9AgAA/AIAAPwCAAD7AgEA' \
                      '+gIMAPoCFwD5AiIA+QItAPgCOAb3AkMS9xFOH/YhWSv2MGQ49T9vRPRPelH0XoVd826QavN9n' \
                      'HbyjaeD8Zyyj/GrvZzwu8io8MrTte/a3sHu6enO7vn02u31/uft5fTz7NTq/evE3/LrtNXn6K' \
                      'TL3N2UwdHRhLfGxnStu7pkorCuVJilo0SOmpczhI+MI3qEgBNveXUDZW5pAFtjXQBRWFIAR01' \
                      'GAD1COwAyNy8AKCwkAB4hGAAUFgwACgsBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' \
                      'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' \
                      'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' \
                      'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' \
                      'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAEAAAABAAAAAQAA' \
                      'AAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABA' \
                      'AAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAA' \
                      'EAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAA' \
                      'AAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAABAAAAAQAAAAEAAAACAAAHAgAAEwIA' \
                      'AB8CAAArAgAANwIAAEQCAABQAgAAXAIAAGgCAAB0AgAAgAIAAIwCAACYAgAApAIAALECAAC9A' \
                      'h4AyQJAANUCYgDhAoQA7QKmAPkCyADJAuoAiQLjAEgCnAAHAlYAEgIPEicCHzY8AkZaUQJuf2' \
                      'YElqN6D77Hjxrm7JMl7896MMemYjuffElGd1MxUU8pGFwnAABnAA=='

SIMULATION_DEFAULT_RANGE = [-92.0915, 49.5497]
