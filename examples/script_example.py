#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=R0801,E1101,W0201

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
Examples on how to start a remote visualizer
"""

import viztools
from pprint import pprint

# direct connection to a resource
#tide = viztools.Visualizer(viztools.DISPLAYWALLS.FLOOR_0)
#print(tide.options)
#print(tide.size)

# using a local resource allocator
resource_allocator = viztools.ResourceAllocator(resource_url='localhost:8080')

# using a distant resource allocator
#resource_allocator = viztools.ResourceAllocator(
#    renderer='livre', nb_cpus=1, nb_gpus=1,
#    exclusive_allocation=False, allocation_time='0:02:00')

visualizer = viztools.Visualizer(resource_allocator)
print(visualizer)

visualizer.reset_camera()

visualizer.set_settings(shading=visualizer.SHADING_DIFFUSE)

#visualizer.stream_to(viztools.DISPLAYWALLS.FLOOR_0)

visualizer.set_camera(origin=[0.5, 0.5, -1], look_at=[0.5, 0.5, 0.5])

pprint(visualizer.camera)

visualizer.image().show()

pprint(resource_allocator.session_streaming_url().contents)

resource_allocator.free()
