#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=R0801,E1101

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
Python package allowing remote control of visualization applications through HTTP REST API.
"""

__all__ = ['ResourceAllocator', 'Visualizer', 'DISPLAYWALLS', 'COLORMAP_SIMULATION',
           'SIMULATION_DEFAULT_RANGE', 'Tide', 'Brayns', 'Livre', 'RTNeuron', 'Application']
from .version import VERSION
from .resource_allocator import ResourceAllocator
from .application import Application
from .visualizer import Visualizer
from .settings import DISPLAYWALLS, COLORMAP_SIMULATION, SIMULATION_DEFAULT_RANGE
from .utils import inherit_docstring_from


class Brayns(Visualizer):
    """
    Visualizer for large-scale and interactive ray-tracing of neurons
    """

    @inherit_docstring_from(Visualizer)
    def image(self, size=None, quality=None):

        # make this generic with https://github.com/HBPVIS/ZeroEQ/issues/186
        if size:
            self.settings.jpeg_size = list(size)
        if quality:
            self.settings.jpeg_compression = quality
        self.settings.commit()

        return super(Brayns, self).image()


class Livre(Visualizer):
    """
    Large-scale Interactive Volume Rendering Engine
    """
    pass


class RTNeuron(Visualizer):
    """
    Scalable rendering tool for the visualization of Neuron simulation data
    """
    pass


class Tide(Visualizer):
    """
    A Tiled Interactive DisplayWall Environment
    """
    pass
