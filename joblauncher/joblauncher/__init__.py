#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=R0801,E1101

from .resource_allocator import ResourceAllocator
from .utils import inherit_docstring_from
# from .settings import *

def initResource():
    return ResourceAllocator()
