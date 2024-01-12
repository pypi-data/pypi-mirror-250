# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.DIAGNOSIS.
#
# SENAITE.DIAGNOSIS is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2022-2024 by it's authors.
# Some rights reserved, see README and LICENSE.

from bika.lims.api import get_portal
from senaite.diagnosis import is_installed
from senaite.diagnosis import logger
from senaite.diagnosis.setuphandlers import add_setup_folders
from senaite.diagnosis.setuphandlers import setup_navigation_types
from senaite.diagnosis.setuphandlers import setup_workflows


def afterUpgradeStepHandler(event):
    """Event handler that is executed after running an upgrade step of senaite.core
    """
    if not is_installed():
        return

    logger.info("Run senaite.diagnosis.afterUpgradeStepHandler ...")

    portal = get_portal()
    add_setup_folders(portal)
    setup_navigation_types(portal)
    setup_workflows(portal)

    logger.info("Run senaite.diagnosis.afterUpgradeStepHandler [DONE]")
