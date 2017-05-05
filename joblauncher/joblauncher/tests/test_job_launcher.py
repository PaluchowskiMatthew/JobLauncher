import unittest
import joblauncher
import joblauncher.settings as settings
from joblauncher.job_launcher import ResourceAllocator


class JobLauncherTests(unittest.TestCase):

    def check_defaults(self,
                       job_launcher,
                       cookie=None,
                       renderer=settings.DEFAULT_RENDERER,
                       allocation=settings.DEFAULT_ALLOCATOR_EXCLUSIVE,
                       nodes=settings.DEFAULT_ALLOCATOR_NB_NODES,
                       cpus=settings.DEFAULT_ALLOCATOR_NB_CPUS,
                       gpus=settings.DEFAULT_ALLOCATOR_NB_GPUS,
                       time=settings.DEFAULT_ALLOCATOR_TIME,
                       reservation=''):
        # Test defaults
        self.assertEqual(job_launcher._cookies, cookie)
        self.assertEqual(job_launcher._renderer, renderer)
        self.assertEqual(job_launcher._exclusive_allocation, allocation)
        self.assertEqual(job_launcher._nb_nodes, nodes)
        self.assertEqual(job_launcher._nb_cpus, cpus)
        self.assertEqual(job_launcher._nb_gpus, gpus)
        self.assertEqual(job_launcher._allocation_time, time)
        self.assertEqual(job_launcher._reservation, reservation)

    def test_default_init(self):
        job_launcher = joblauncher.JobLauncher()

        self.check_defaults(job_launcher)

        self.assertEqual(job_launcher._resource_url, None)
        self.assertEqual(job_launcher._url_service, settings.DEFAULT_ALLOCATOR_URI + '/' + \
                            settings.DEFAULT_ALLOCATOR_NAME + '/' + settings.DEFAULT_ALLOCATOR_API_VERSION)
        self.assertEqual(job_launcher._url_session, job_launcher._url_service + '/' + \
                            settings.DEFAULT_ALLOCATOR_SESSION_PREFIX + '/')
        self.assertEqual(job_launcher._url_config, job_launcher._url_service + '/' + \
                           settings.DEFAULT_ALLOCATOR_CONFIG_PREFIX + '/')

    def test_url_init(self):
        resource_url = 'www.test_resource_url.com'
        job_launcher = joblauncher.JobLauncher(resource_url)

        self.check_defaults(job_launcher)

        self.assertEqual(job_launcher._resource_url, 'http://' + resource_url)
        self.assertEqual(job_launcher._url_service, job_launcher._resource_url + '/')
        self.assertEqual(job_launcher._url_session, job_launcher._url_service)
        self.assertEqual(job_launcher._url_config, job_launcher._url_service)

    def test_edit_allocation_settings(self):
        job_launcher = joblauncher.JobLauncher()

        new_time = '5:00:00'
        new_cookie = 'tasty'
        new_allocation = True
        new_cpus = 10
        new_gpus = 2
        new_nodes = 1
        new_render = 'wrapper'
        new_reservation = 'reserve'
        new_resource = 'resource'
        new_config = 'www.config.com'
        new_service = 'www.service.com'
        new_session = 'www.session.com'
        new_not_existing_attribute = 'something new'

        job_launcher.edit_allocation_settings(_allocation_time=new_time,
                                              _cookies=new_cookie,
                                              _exclusive_allocation=new_allocation,
                                              _nb_cpus=new_cpus,
                                              _nb_gpus=new_gpus,
                                              _nb_nodes=new_nodes,
                                              _renderer=new_render,
                                              _reservation=new_reservation,
                                              _resource_url=new_resource,
                                              _url_config=new_config,
                                              _url_service=new_service,
                                              _url_session=new_session,
                                              _new_attribute=new_not_existing_attribute
                                              )

        self.check_defaults(job_launcher, new_cookie, new_render, new_allocation, new_nodes, new_cpus, new_gpus, new_time, new_reservation)

        self.assertEqual(job_launcher._url_service, new_service)
        self.assertEqual(job_launcher._url_session, new_session)
        self.assertEqual(job_launcher._url_config, new_config)
        self.assertFalse(hasattr(job_launcher, '_new_attribute'))