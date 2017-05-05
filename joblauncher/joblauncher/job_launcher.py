import pprint
import logging

from .resource_allocator import ResourceAllocator

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


    def show_allocation_settings(self):
        """
        Prints settings of ResourceAllocator
        """
        attributes = vars(self)
        pprint.pprint(attributes)

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