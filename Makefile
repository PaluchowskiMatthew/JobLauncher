#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=R0801

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

#modules that have tests
TEST_MODULES=viztools

#modules that are installable (ie: ones w/ setup.py)
INSTALL_MODULES=.

#packages to cover
COVER_PACKAGES=viztools

#documented modules
DOC_MODULES=

#no need to do coverage on the mock objects
IGNORE_LINT=

#need a later version than 1.4.1 to install ipywidgets and ipython
#we choose 9.0.1 here to match the pip version in collab notebooks
PYTHON_PIP_VERSION=pip==9.0.1

##### DO NOT MODIFY BELOW #####################

ifndef CI_DIR
CI_REPO?=ssh://bbpcode.epfl.ch/platform/ContinuousIntegration.git
CI_DIR?=ContinuousIntegration

FETCH_CI := $(shell \
		if [ ! -d $(CI_DIR) ]; then \
			git clone $(CI_REPO) $(CI_DIR) > /dev/null ;\
		fi;\
		echo $(CI_DIR) )
endif

include $(CI_DIR)/python/common_makefile
