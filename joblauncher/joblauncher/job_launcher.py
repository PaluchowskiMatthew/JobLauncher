import pprint
import logging
import sys
from time import sleep
import json


from .resource_allocator import ResourceAllocator
from .utils import Status

logger = logging.getLogger(__name__)

class JobLauncher(ResourceAllocator):
    """
    Simple wrapper around ResourceAllocator for extending and simplifying process of connecting to Rendering Resource Manager
    """

    def __init__(self, resource=None):

        if isinstance(resource, basestring):
            super(JobLauncher, self).__init__(resource_url = resource)
        else:
            super(JobLauncher, self).__init__()


    def get_allocation_settings(self):
        """
        Prints settings of ResourceAllocator
        """
        attributes = vars(self)
        return attributes

    def edit_allocation_settings(self, **kwargs):
        """
        Updates settings of ResourceAllocator
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
        :return:
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
        :return: payload as json
        """
        default_renderer_payload = {
            "id": "bbic_wrapper",
            "command_line": "pip install flask --user; python /gpfs/bbp.cscs.ch/apps/viz/bbp/dev/wrapper/wrapper.py",
            "environment_variables": "",
            "modules": "BBP/viz/latest BBP/viz/hdf5/1.8.15 BBP/viz/python/3.4.3",
            "process_rest_parameters_format": "",
            "scheduler_rest_parameters_format": '--script-command "bbic_stack.py /gpfs/bbp.cscs.ch/project/proj39/rrm_test/out_vm.h5 --create-from /gpfs/bbp.cscs.ch/home/tresch/bigbrain600/list.txt --orientation coronal --all-stacks" --host "${rest_hostname}" --port "${rest_port}"',
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
        for key, value in kwargs.iteritems():
            if key in default_renderer_payload:
                default_renderer_payload[key] = value
        return default_renderer_payload

    def get_job_settings(self, renderer_id):
        """
        Prints the settings of selected job identified by renderer_id
        :param renderer_id: Job identifier
        :return:
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
        :param renderer_id:
        :param kwargs:
        :return:
        """
        renderers = self.config_list().contents
        if renderers:
            renderer = next((rend for rend in renderers if rend["id"] == renderer_id), None)

        if renderer:
            renderer = dict(renderer)
            for key, value in kwargs.iteritems():
                if key in renderer:
                    renderer[key] = value

            return self.config_update(renderer)
        else:
            return Status(400, 'Renderer not found.', '')


    def delete_job_settings(self, renderer_id):
        """

        TODO: FIX. NOT WORKING.

        :param renderer_id:
        :return:
        """
        return self.config_delete({"id": renderer_id})


    def schedule_and_launch_job(self, renderer_id=None):
        """
        :param renderer_id:
        :return:
        """

        if renderer_id is not None:
            self._renderer = renderer_id

        # This calls session_schedule() with payload containing allocation settings and schedules a job run given the renderer_id
        resource = self.resource_url()
        if resource is not None:
            print('Job scheduled and launched!')
            logger.info('Job scheduled and launched!')


    def get_job_status(self):
        """

        :return:
        """

        # This is just a plain progressbar
        for i in range(21):
            sys.stdout.write('\r')
            # the exact output you're looking for:
            sys.stdout.write("[%-20s] %d%%" % ('=' * i, 5 * i))
            sys.stdout.flush()
            sleep(0.25)