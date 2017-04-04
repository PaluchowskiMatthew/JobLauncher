#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=E1101,W0122
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
The application class exposes a dynamic generated API from ZeroEQ HTTP server exposed registry.
"""

import json
import python_jsonschema_objects as pjs

from viztools.utils import HTTP_METHOD_GET, HTTP_METHOD_PUT, HTTP_STATUS_OK
from viztools.resource_allocator import ResourceAllocator
from viztools.settings import DISPLAYWALLS, DISPLAYWALL_PORT


def camelcase_to_snake_case(name):
    """
    Convert CamelCase to snake_case
    :param name: CamelCase to convert
    :return: converted snake_case
    """
    import re
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def make_allocator(url):
    """
    Create an allocator referencing an existing resource
    :param url: a DisplayWall preset or the "hostname:port" of an existing application
    :return: the allocator
    """
    if url in DISPLAYWALLS:
        url += DISPLAYWALL_PORT
    return ResourceAllocator(resource_url=url)


class Application(object):
    """
    The application class exposes a dynamic generated API from ZeroEQ HTTP server exposed registry.
    """

    def __init__(self, resource=None):
        """
        Create a new application instance by connecting to the given resource
        :param resource: can be a string 'hostname:port' to connect to a known application, a
                         ResourceAllocator instance or None for default allocation.
        """

        if isinstance(resource, ResourceAllocator):
            self._allocator = resource
        elif isinstance(resource, basestring):
            self._allocator = make_allocator(resource)
        else:
            self._allocator = ResourceAllocator()

        self._url = self._allocator.resource_url()
        self._registry, ret_code = self._obtain_registry()
        if ret_code != HTTP_STATUS_OK:
            raise Exception('Failed to obtain registry from application')

        self._create_all_properties()

        if not hasattr(self, 'version'):
            type(self).version = None

    def __str__(self):
        session = self._allocator.session_status()
        if session.code == HTTP_STATUS_OK:
            url = 'http://' + ':'.join([session.contents['hostname'], session.contents['port']])
        else:
            url = self._url

        if self.version:
            version = '.'.join(str(x) for x in [self.version.major, self.version.minor,
                                                self.version.patch, self.version.revision])
        else:
            version = 'unknown'
        return "Application version {0} running on {1}".format(version, url)

    def free(self):
        """
        Frees resources allocated by the application
        """
        self._allocator.free()

    def log(self):
        """
        Show the application log output
        """
        log = self._allocator.session_log()
        if log.code == HTTP_STATUS_OK:
            return log.contents['contents']
        return "Can only provide log output from applications launched with ResourceAllocator"

    def _create_all_properties(self):
        """
        Add all exposed objects and types from the application as properties to the Application.
        """

        for i in self._registry.keys():
            schema, ret_code = self._schema(i)
            if ret_code != HTTP_STATUS_OK:
                continue

            classes = pjs.ObjectBuilder(schema).build_classes()
            class_names = dir(classes)

            # find the generated class name that matches our schema root title
            for c in class_names:
                if c.lower() == schema['title'].lower():
                    class_name = c
                    break

            class_type = getattr(classes, class_name)
            success, value = self._create_member(class_type, i, schema['type'])
            if not success:
                continue

            is_object = schema['type'] == 'object'
            if is_object:
                self._add_enums(value)
                self._add_request(class_type, i)
                self._add_commit(class_type, i)

            # add member to Application
            member = '_' + schema['title']
            setattr(self, member, value)

            put_only = HTTP_METHOD_PUT in self._registry[i] and len(self._registry[i]) == 1
            if put_only and is_object:
                self._add_method(schema, i)
            else:
                self._add_property(schema, member, i, schema['type'])
                if HTTP_METHOD_PUT in self._registry[i]:
                    self._add_method(schema, i, 'set_')

    def _create_member(self, class_type, object_name, object_type):
        """
        Create a new object from the given class type and initialize it from the application state.
        :param class_type: class type of the new object
        :param object_name: name of the new object
        :param object_type: type as string of the new object
        :return: tuple(success, object)
        """

        # initialize object from application state with GET if applicable
        if HTTP_METHOD_GET in self._registry[object_name]:
            status = self._allocator.session_command(HTTP_METHOD_GET, object_name)
            if status.code != HTTP_STATUS_OK:
                print('Error getting data for {0}: {1}'.format(object_name, status.code))
                return False, None
            if object_type in ['array', 'object']:
                value = class_type.from_json(json.dumps(status.contents))
            else:
                value = class_type(status.contents)
        else:
            value = class_type()
        return True, value

    def _add_enums(self, value):
        """
        Look for enums in the given object to create string constants <ENUM_CLASSNAME>_<ENUM_VALUE>
        """

        for i in value.keys():
            enum = None
            if 'enum' in value.propinfo(i):
                enum = value.propinfo(i)
            if value.propinfo(i)['type'] == 'array':
                if 'enum' in value.propinfo(i)['items']:
                    enum = value.propinfo(i)['items']
            if not enum:
                continue

            enum_class = str(camelcase_to_snake_case(enum['title'])).upper() + "_"
            for val in enum['enum']:
                setattr(self, enum_class + val.upper(), val)

    def _add_request(self, class_type, object_name):
        """ Add request() for given property """

        if HTTP_METHOD_GET in self._registry[object_name]:
            def request_builder(url):
                """ Wrapper for returning the property.request() function """

                def request(prop):
                    """
                    Initialize the property from the application
                     :return: True if request was successful (not working yet, needs
                              https://github.com/HBPVIS/Servus/issues/65)
                    """

                    status = self._allocator.session_command(HTTP_METHOD_GET, url)
                    if status.code == HTTP_STATUS_OK:
                        prop.__init__(**status.contents)
                        return True
                    return False

                return request

            setattr(class_type, 'request', request_builder(object_name))

    def _add_commit(self, class_type, object_name):
        """ Add commit() for given property """

        if HTTP_METHOD_PUT in self._registry[object_name]:
            def commit_builder(url):
                """ Wrapper for returning the property.commit() function """

                def commit(prop):
                    """ Update the property in the application """
                    self._allocator.session_command(HTTP_METHOD_PUT, url, prop.serialize())

                return commit

            setattr(class_type, 'commit', commit_builder(object_name))

    def _add_property(self, schema, member, object_name, property_type):
        """ Add property to Application for object """

        def getter_builder(member):
            """ Wrapper for returning the property state """

            def function(self):
                """ Returns the current state for the property """
                value = getattr(self, member)
                if property_type == 'array':
                    return value.data
                return value

            return function

        def setter_builder(member, object_name):
            """ Wrapper for updating the property state """

            def function(self, prop):
                """ Update the current state of the property locally and in the application """
                if property_type == 'object':
                    setattr(self, member, prop)
                    self._allocator.session_command(HTTP_METHOD_PUT, object_name, prop.serialize())
                    return

                if property_type == 'array':
                    value = getattr(self, member)
                    value.data = prop
                else:
                    setattr(self, member, prop)
                self._allocator.session_command(HTTP_METHOD_PUT, object_name, json.dumps(prop))

            return function if HTTP_METHOD_PUT in self._registry[object_name] else None

        import os
        snake_case_name = os.path.basename(object_name).replace('-', '_')
        setattr(type(self), snake_case_name,
                property(fget=getter_builder(member), fset=setter_builder(member, object_name),
                         doc='Access to the {0} property'.format(schema['title'])))

    def _add_method(self, schema, object_name, prefix=''):
        """
        Add a setter method for the property with all the properties' fields as positional
        arguments.
        """

        if 'properties' in schema:
            code = '''
                def function(self, {0}):
                    args = locals()
                    var = getattr(self, "{1}")
                    for i in args.keys():
                        if i != 'self' and args[i] != None:
                            try:
                                setattr(var, i, args[i])
                            except Exception as e:
                                print(e.message)
                    self._allocator.session_command('PUT', '{2}', var.serialize())
                '''.format(', '.join([s + '=None' for s in schema['properties'].keys()]),
                           '_' + schema['title'], object_name)
        else:
            code = '''
                def function(self):
                    self._allocator.session_command('PUT', '{0}')
                '''.format(object_name)

        d = {}
        exec(code.strip(), d)
        function = d['function']

        import os
        func_name = str(os.path.basename(object_name).replace('-', '_'))
        function.__doc__ = 'Update the {0} property'.format(schema['title'])
        function.__name__ = prefix + func_name

        setattr(self.__class__, function.__name__, function)

    def _obtain_registry(self):
        """ Returns the registry of PUT and GET objects of the application """
        status = self._allocator.session_command(HTTP_METHOD_GET, 'registry')
        return status.contents, status.code

    def _schema(self, object_name):
        """ Returns the JSON schema for the given object """
        status = self._allocator.session_command(HTTP_METHOD_GET, object_name + '/schema')
        return status.contents, status.code
