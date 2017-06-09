#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=R0801,W0122,E0602

import os
from setuptools import setup


BASEDIR = os.path.dirname(os.path.abspath(__file__))
REQS_PATH = (os.path.join(BASEDIR, "requirements.txt"))

with open(REQS_PATH) as f:
    requirements = f.read().splitlines()

setup(name='joblauncher',
      version='0.1',
      description='Simple python package for interaction with JobManager',
      author='Mateusz Paluchowski & Christian Tresch',
      license='GNU LGPL',
      packages=['joblauncher'],
      install_requires=requirements,
      test_suite='nose.collector',
      tests_require=['nose'],
      )