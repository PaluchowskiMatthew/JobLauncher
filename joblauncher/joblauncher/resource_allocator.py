#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=R0801, R0913

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
The resource allocator manages sessions and jobs on the cluster
"""


from joblauncher.utils import http_request, HTTP_METHOD_GET, HTTP_METHOD_PUT, \
    HTTP_METHOD_DELETE, HTTP_METHOD_POST, HTTP_STATUS_OK, Status
import joblauncher.settings as settings
import time

SESSION_STATUS_STOPPED = 0
SESSION_STATUS_SCHEDULING = 1
SESSION_STATUS_SCHEDULED = 2
SESSION_STATUS_GETTING_HOSTNAME = 3
SESSION_STATUS_STARTING = 4
SESSION_STATUS_RUNNING = 5
SESSION_STATUS_STOPPING = 6
SESSION_STATUS_FAILED = 7


class ResourceAllocator(object):
    """
    The resource allocator manages sessions and jobs on the cluster
    """

    def __init__(self,
                 service_url=settings.DEFAULT_ALLOCATOR_URI,
                 service_api_version=settings.DEFAULT_ALLOCATOR_API_VERSION,
                 resource_url=None,
                 renderer=settings.DEFAULT_RENDERER,
                 exclusive_allocation=settings.DEFAULT_ALLOCATOR_EXCLUSIVE,
                 nb_nodes=settings.DEFAULT_ALLOCATOR_NB_NODES,
                 nb_cpus=settings.DEFAULT_ALLOCATOR_NB_CPUS,
                 nb_gpus=settings.DEFAULT_ALLOCATOR_NB_GPUS,
                 allocation_time=settings.DEFAULT_ALLOCATOR_TIME,
                 reservation=''):
        self._cookies = None
        self._renderer = renderer
        self._exclusive_allocation = exclusive_allocation
        self._nb_nodes = nb_nodes
        self._nb_cpus = nb_cpus
        self._nb_gpus = nb_gpus
        self._allocation_time = allocation_time
        self._reservation = reservation
        if resource_url is None:
            self._url_service = service_url + '/' + \
                                settings.DEFAULT_ALLOCATOR_NAME + '/' + service_api_version
            self._url_session = self._url_service + '/' + \
                                settings.DEFAULT_ALLOCATOR_SESSION_PREFIX + '/'
            self._url_config = self._url_service + '/' + \
                               settings.DEFAULT_ALLOCATOR_CONFIG_PREFIX + '/'
            self._resource_url = resource_url
        else:
            self._resource_url = 'http://' + resource_url
            self._url_service = self._resource_url + '/'
            self._url_session = self._url_service
            self._url_config = self._url_service

    def free(self):
        """ Frees remote resources """
        if self._cookies is not None:
            self.session_delete()

    def resource_url(self):
        """ Return the URL of the resources' http server """
        try:
            if self._resource_url is not None:
                return self._resource_url

            payload = {
                "renderer_id": self._renderer,
                "owner": "joblauncher"
            }
            status = self.session_create(payload)
            if status.code != 201:
                raise Exception(status.contents)
            self._cookies = status.cookies

            # TODO Get the json info from visualizer
            payload = {
                "params": "",
                "environment": "",
                "reservation": self._reservation,
                "exclusive_allocation": self._exclusive_allocation,
                "nb_nodes": self._nb_nodes,
                "nb_cpus": self._nb_cpus,
                "nb_gpus": self._nb_gpus,
                "allocation_time": self._allocation_time
            }
            status = self.session_schedule(payload)
            if status.code != HTTP_STATUS_OK:
                raise Exception(status.contents)

            running = False
            attempt = 0
            while attempt < settings.SESSION_MAX_CONNECTION_ATTEMPTS and not running:
                status = self.session_status()
                if status.code == HTTP_STATUS_OK and \
                   status.contents['code'] != SESSION_STATUS_RUNNING:
                    time.sleep(1)
                else:
                    running = True
                attempt = attempt + 1

            if not running:
                raise Exception('Failed to get rendering resource running')

            return self._url_session
        except Exception:
            status = self.session_delete()
            raise
        return None

    def session_create(self, payload):
        """
        Create a session
        """
        self._cookies = None
        return http_request(HTTP_METHOD_POST, self._url_session, payload, None, self._cookies)

    def session_list(self):
        """
        List existing sessions
        """
        return self._status_check(http_request(
                HTTP_METHOD_POST, self._url_session, None, None, self._cookies))

    def session_delete(self):
        """
        Delete a session
        """
        return http_request(
            HTTP_METHOD_DELETE, self._url_session, None, None, self._cookies)

    def session_command(self, method, command, payload=None):
        """
        Execute a custom command
        """
        return self._status_check(http_request(
                method, self._url_session, payload, command, self._cookies))

    def session_schedule(self, payload):
        """
        Schedule a job
        """
        return self._status_check(http_request(
            HTTP_METHOD_PUT, self._url_session, payload, 'schedule', self._cookies))

    def session_status(self):
        """
        Request for session status
        """
        return self._status_check(http_request(
            HTTP_METHOD_GET, self._url_session, None, 'status', self._cookies))

    def session_log(self):
        """
        Request for session log
        """
        return self._status_check(http_request(
            HTTP_METHOD_GET, self._url_session, None, 'log', self._cookies))

    def session_job(self):
        """
        Request for job information
        """
        return self._status_check(http_request(
            HTTP_METHOD_GET, self._url_session, None, 'job', self._cookies))

    def session_streaming_url(self):
        """
        Request for streaming url
        """
        if self._cookies is None:
            payload = {'uri': settings.DEFAULT_STREAMER_URI}
            return Status(HTTP_STATUS_OK, payload, None)
        else:
            return self._status_check(http_request(
                HTTP_METHOD_GET, self._url_session, None, 'imagefeed', self._cookies))

    def config_create(self, payload):
        """
        Create configuration
        """
        return self._status_check(http_request(
            HTTP_METHOD_POST, self._url_config, payload, None, self._cookies))

    def config_update(self, payload):
        """
        Update configuration
        """
        return self._status_check(http_request(
            HTTP_METHOD_PUT, self._url_config, payload, None, self._cookies))

    def config_list(self):
        """
        List existing configurations
        """
        return self._status_check(http_request(
            HTTP_METHOD_GET, self._url_config, None, None, self._cookies))

    def config_delete(self, payload):
        """
        Delete configuration
        """
        return self._status_check(http_request(
            HTTP_METHOD_DELETE, self._url_config, payload, None, self._cookies))

    def _status_check(self, status):
        """
        Handles the result of an executed statement
        :param status Status of the executed statement
        """
        if status.code != HTTP_STATUS_OK:
            if status.code >= 500:
                # if the rendering resource is unreachable, then the session should
                # be destroyed
                self.session_delete()
                raise Exception(status.contents)
        return status
