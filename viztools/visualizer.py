#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=E1101
#
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
The visualizer is the remote rendering resource in charge of rendering datasets
"""

import base64
import io

from viztools.application import Application
from viztools.utils import HTTP_STATUS_OK, in_notebook
from PIL import Image

import atexit
import gc

visualizers = list()


@atexit.register
def clean_all():
    """
    Cleans up the resources allocated by the visualizer and forces garbage collection
    """
    for visualizer in visualizers:
        visualizer.free()
        visualizers.remove(visualizer)
    gc.enable()
    gc.collect()


def camelcase_to_snake_case(name):
    """
    Convert CamelCase to snake_case
    :param name: CamelCase to convert
    :return: converted snake_case
    """
    import re
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class Visualizer(Application):
    """
    The visualizer class provides specialization like widgets, image display and image streaming
    for applications that expose according APIs.
    """

    def __init__(self, resource=None):
        """
        Create a new visualizer instance by connecting to the given resource
        :param resource: can be a string 'hostname:port' to connect to a known application, a
                         ResourceAllocator instance or None for default allocation.
        """

        visualizers.append(self)

        super(Visualizer, self).__init__(resource)

        if in_notebook():
            self._add_widgets()

    def image(self, size=None, quality=None):
        """
        Requests a new rendering from the application and returns a PIL image
        :param size: tuple (width,height) for the resulting image
        :param quality: JPEG compression quality between 1 (worst) and 100 (best)
        :return: the PIL image of the current rendering, None on error obtaining the image
        """

        if size or quality:
            print("Size and/or quality change is not implemented")

        if self.image_jpeg.request() \
                and self.image_jpeg.data:  # TODO: remove after
            # https://github.com/HBPVIS/Servus/issues/65
            return Image.open(io.BytesIO(base64.b64decode(self.image_jpeg.data)))
        return None

    def _add_widgets(self):
        """ Add functions to the visualizer to provide widgets for appropriate properties """

        if self._allocator.session_streaming_url().code == HTTP_STATUS_OK:
            self._add_show_function()

        if hasattr(self, 'frame'):
            self._add_simulation_slider()

    def _add_show_function(self):
        """ Add show() function for live streaming """

        def function_builder():
            """ Wrapper for returning the visualizer.show() function """

            def show():
                """ Shows the live rendering of the application """

                import time
                s = self._allocator.session_streaming_url()
                if s.code != HTTP_STATUS_OK:
                    print('Could not connect to streaming URL')
                    return

                # pylint: disable=F0401
                import ipywidgets as widgets
                from IPython.display import display
                w = widgets.HTML(value='<img src="{0}?{1}"/>'.format(
                    s.contents['uri'], str(int(time.time()))))
                display(w)

            return show

        setattr(self, 'show', function_builder())

    def _add_simulation_slider(self):
        """ Add simulation_slider() function for lexis/render/frame control """

        def function_builder():
            """ Wrapper for returning the visualizer.simulation_slider() function """

            def simulation_slider():
                """ Show slider to control simulation """

                # pylint: disable=F0401
                import ipywidgets as widgets
                from IPython.display import display
                self.frame.request()
                play = widgets.Play(
                    value=self.frame.current,
                    min=self.frame.start,
                    max=self.frame.end,
                    step=1,
                    description="Simulation playback"
                )
                play.observe(lambda change: self.set_frame(current=change['new']), names='value')

                slider = widgets.IntSlider(min=self.frame.start,
                                           max=self.frame.end,
                                           value=self.frame.current)
                widgets.jslink((play, 'value'), (slider, 'value'))
                w = widgets.HBox([play, slider])
                display(w)

            return simulation_slider

        setattr(self, 'simulation_slider', function_builder())
