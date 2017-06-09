#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#
# Code related to EPFL Master Semester Project:
# "A job management web service for cluster-based processing in Brain Atlasing"
#
# Version 1.0, 02 June 2017
#
# Copyright (c) 2017, Blue Brain Project
#                     Mateusz Paluchowski <mateusz.paluchowski@epfl.ch>
#                     Christian Tresch <christian.tresch@epfl.ch>
#
# This file is part of ClusterTools, fork of VizTools
# <https://github.com/BlueBrain/VizTools>
#
###############################################################################

import pprint
import logging
from tqdm import tqdm
import time
import requests


from .resource_allocator import ResourceAllocator
from .utils import Status

logger = logging.getLogger(__name__)

class JobLauncher(ResourceAllocator):
    """
    Simple wrapper around ResourceAllocator for extending and simplifying process of connecting to JobManager
    """
    def __init__(self, resource=None):

        if isinstance(resource, basestring):
            super(JobLauncher, self).__init__(resource_url = resource)
        else:
            super(JobLauncher, self).__init__()

        self.launched_job_url = None


    def get_allocation_settings(self):
        """
        :return: dict representation of ResourceAllocator settings
        """
        attributes = vars(self)
        return attributes

    def edit_allocation_settings(self, **kwargs):
        """
        Updates settings of ResourceAllocator
        :return: dict representation of updated allocation settings
        """
        for key, value in kwargs.iteritems():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                print('Attribute ' + key + ' not found in ResourceAllocator. Skipping.')
                logger.info('Attribute ' + key + ' not found in ResourceAllocator. Skipping.')
        return self.get_allocation_settings()

    def create_job_renderer(self, payload=None):
        """
        Creates new renderer basing either on payload provided or default renderer if one is not provided
        :return: dict representation of renderer settings payload
        """
        if not payload:
            payload = self.create_renderer_payload()
        return self.config_create(payload)

    def create_renderer_payload(self, **kwargs):
        """
        Creates
        default_renderer_payload = {
            "id": "bbic_wrapper",
            "command_line": "pip install flask --user; python /gpfs/bbp.cscs.ch/apps/viz/bbp/dev/wrapper/wrapper.py",
            "environment_variables": "",
            "modules": "BBP/viz/latest BBP/viz/hdf5/1.8.15 BBP/viz/python/3.4.3",
            "process_rest_parameters_format": "",
            "scheduler_rest_parameters_format": "--script-command \"bbic_stack.py /gpfs/bbp.cscs.ch/project/proj39/rrm_test/out_vm.h5 --create-from /gpfs/bbp.cscs.ch/home/tresch/bigbrain600/list.txt --orientation coronal --all-stacks\" --host \"${rest_hostname}\" --port \"${rest_port}\"",
            "project": "proj39",
            "queue": "test",
            "exclusive": False,
            "nb_nodes": 1,
            "nb_cpus": 1,
            "nb_gpus": 0,
            "graceful_exit": False,
            "wait_until_running": False,
            "name": "bbic",
            "description": "wrapper for bbic"
        }
        and modifies values if proper kwargs were provided
        :param kwargs: id, command_line, environment_variables, modules, process_rest_parameters_format,
        scheduler_rest_parameters_format, project, queue, exclusive, nb_nodes, nb_cpus, nb_gpus, graceful_exit, wait_until_running
        :return: dict representation of renderer settings payload
        """
        default_renderer_payload = {
            "id": "bbic_wrapper",
            "command_line": "pip3 install flask --user; python3 /gpfs/bbp.cscs.ch/apps/viz/bbp/dev/Wrapper/wrapper.py",
            "environment_variables": "",
            "modules": "BBP/viz/latest BBP/viz/hdf5/1.8.15 BBP/viz/python/3.4.3",
            "process_rest_parameters_format": "",
            "scheduler_rest_parameters_format": '--script-command "python3 -u /gpfs/bbp.cscs.ch/apps/viz/bbp/dev/wrapper/bbic_stack.py /gpfs/bbp.cscs.ch/project/proj39/rrm_test/out_vm.h5 --create-from /gpfs/bbp.cscs.ch/home/tresch/bigbrain600/list.txt --orientation coronal --all-stacks" --host "${rest_hostname}" --port "${rest_port}"',
            "project": "proj39",
            "queue": "prod",
            "exclusive": False,
            "nb_nodes": 1,
            "nb_cpus": 1,
            "nb_gpus": 0,
            "graceful_exit": False,
            "wait_until_running": False,
            "name": "bbic",
            "description": "wrapper for bbic"
        }
        for key, value in kwargs.iteritems():
            if key in default_renderer_payload:
                default_renderer_payload[key] = value
        return default_renderer_payload

    def get_job_settings(self, renderer_id):
        """
        Returns the settings of selected job identified by renderer_id
        :param renderer_id: Job identifier
        :return: None or dict representation of selected job settings
        """
        renderers = self.config_list().contents
        if renderers:
            renderer = next((rend for rend in renderers if rend["id"] == renderer_id), None)

        if renderer:
            return dict(renderer)
        else:
            pprint.pprint('Renderer not found.')
            return


    def edit_job_settings(self, renderer_id, **kwargs):
        """
        Updates the settings of selected job identified by renderer_id.
        :param renderer_id: Job identifier
        :param kwargs: key-value pairs with new settings of job identified
        :return: Status object holding execution status of an HTTP request
        """
        renderers = self.config_list().contents
        if renderers:
            renderer = next((rend for rend in renderers if rend["id"] == renderer_id), None)

        if renderer:
            renderer = dict(renderer)
            for key, value in kwargs.iteritems():
                if key in renderer:
                    renderer[key] = value
            renderer["id"] = renderer_id
            return self.config_update(renderer)
        else:
            return Status(400, 'Renderer not found.', '')


    def delete_job_settings(self, renderer_id):
        """
        Deletes job settings from RenderingResourceManager
        :param renderer_id: Job identifier
        :return: Status object holding execution status of an HTTP request
        """
        return self.config_delete({"id": renderer_id})


    def schedule_and_launch_job(self, renderer_id=None):
        """
        Method used for scheduling required resources and launching specific job
        :param renderer_id: Job identifier
        :return: Status object holding execution status of an HTTP request
        """

        if renderer_id is not None:
            self._renderer = renderer_id

        # This calls session_schedule() with payload containing allocation settings and schedules a job run given the renderer_id
        resource = self.resource_url()
        if resource is not None:
            self.launched_job_url = resource
            print('Job scheduled and launched!')
            logger.info('Job scheduled and launched!')
            return Status(200, 'Job scheduled and launched!', '')
        else:
            print('Failed to schedule and launch the job!')
            logger.info('Failed to schedule and launch the job!')
            return Status(400, 'Failed to schedule and launch the job!', '')

    def deallocate_and_cancel_job(self):
        """
        Delete session which results in job cancel and deallocation of the resources on the cluster via JobManager.
        :return: Status object holding execution status of an HTTP request
        """
        # TODO verify that is enough to deallocate resources and then get the new job running.
        self.launched_job_url = None
        self._resource_url = None
        response = self.session_delete()
        if response.code == 200:
            print('Resources deallocated and job canceled successfully!')
            logger.info('Resources deallocated and job canceled successfully!')
        else:
            print('Failed to deallocate resources and cancel the job.')
            logger.info('Failed to deallocate resources and cancel the job.')
        return response

    def get_single_job_status(self):
        """
        Single API call to check what is the status of scheduled and launched job
        :return: Progress in percents
        """
        if not self.launched_job_url:
            print('Job was not scheduled and launched!')
            logger.info('Job was not scheduled and launched!')
            return -1
        try:
            response = requests.get(self.launched_job_url + '/resourceconnector/v1/status')
            data = response.json()
            progress = int(data['progress'])
            return progress
        except Exception:
            print('Exception caught.')
            raise

    def get_continuous_job_status(self):
        """
        Prints progress bar indicating the status of scheduled and launched job
        """
        max_ = 100
        with tqdm(total=max_) as pbar:
            while True:
                try:
                    response = requests.get(self.launched_job_url + '/resourceconnector/v1/status')
                    data = response.json()
                    progress = int(data['progress'])
                    pbar.update(progress - pbar.n)
                except Exception:
                    print('Exception caught.')
                    raise

                if progress >= 100:
                    print('Job completed!')
                    logger.info('Job scheduled and launched!')
                    break
                time.sleep(.5)