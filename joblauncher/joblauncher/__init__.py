#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=R0801,E1101
import logging

from .job_launcher import JobLauncher
from .utils import inherit_docstring_from

logger = logging.getLogger(__name__)

logger.addHandler(logging.NullHandler())

def init():
    return JobLauncher()
