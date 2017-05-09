#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=R0801,E1101,R0912

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

import requests
import pprint
import sys
from collections import OrderedDict


HTTP_METHOD_PUT = 'PUT'
HTTP_METHOD_GET = 'GET'
HTTP_METHOD_DELETE = 'DELETE'
HTTP_METHOD_POST = 'POST'
HTTP_STATUS_OK = 200


class Status(object):
    """
    Holds the execution status of an HTTP request
    """
    def __init__(self, code, contents, cookies):
        self.code = code
        self.contents = contents
        self.cookies = cookies

    def show_response(self):
        pprint.pprint('HTTP status code: ' + str(self.code))
        pprint.pprint('Contents: ' + str(self.contents))
        pprint.pprint('Cookies:' + str(self.cookies))


def http_request(method, url, body=None, command=None, cookies=None):
    """
    Perform http requests to the given URL and return the applications' response
    :param method: the type of HTTP request, PUT or GET are supported
    :param url: the URL of the applications' http server
    :param body: optional body for PUT requests
    :param command: the type of HTTP command to be executed on the target app
    :param cookies: the cookies to add to the request header
    :return: JSON-encoded response of the request
    """
    full_url = url
    request = None
    if command is not None:
        full_url = full_url + command
    try:
        if method == HTTP_METHOD_POST:
            if body == '':
                request = requests.post(full_url, cookies=cookies)
            else:
                request = requests.post(full_url, data=body, cookies=cookies)
        elif method == HTTP_METHOD_PUT:
            if body == '':
                request = requests.put(full_url, cookies=cookies)
            else:
                request = requests.put(full_url, data=body, cookies=cookies)
        elif method == HTTP_METHOD_GET:
            request = requests.get(full_url, cookies=cookies)
            if request.status_code == 502:
                raise requests.exceptions.ConnectionError('Bad Gateway 502')
        elif method == HTTP_METHOD_DELETE:
            if body == '':
                request = requests.delete(full_url, cookies=cookies)
            else:
                request = requests.delete(full_url, data=body, cookies=cookies)
        js = ''
        if request.content:
            if request.status_code == 200:
                js = request.json(object_pairs_hook=OrderedDict)
            else:
                js = request.text
        response = Status(request.status_code, js, request.cookies)
        request.close()
    except requests.exceptions.ConnectionError:
        raise Exception('ERROR: Failed to connect to Application, did you start it with the '
                        '--zeroeq-http-server command line option?')
    return response


def in_notebook():
    """
    Returns ``True`` if the module is running in IPython kernel,
    ``False`` if in IPython shell or other Python shell.
    """
    return 'ipykernel' in sys.modules


def inherit_docstring_from(cls):
    """
    Provide a decorator for inheriting docstring of overridden functions.
    :param cls: The class where to inherit the docstring from
    :return: The decorator function
    """
    def docstring_inheriting_decorator(fn):
        """
        :param fn: the function to decorate
        :return: the decorated function with inherited docstring
        """
        fn.__doc__ = getattr(cls, fn.__name__).__doc__
        return fn
    return docstring_inheriting_decorator
