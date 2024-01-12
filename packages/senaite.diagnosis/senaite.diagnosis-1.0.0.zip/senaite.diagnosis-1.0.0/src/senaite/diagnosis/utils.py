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

import re
from bika.lims import api
from bika.lims.utils import t as _t
from bika.lims.utils import to_utf8
from senaite.core.catalog import SETUP_CATALOG
from senaite.diagnosis import messageFactory as _
from zope.interface import Invalid


def translate(i18n_message, mapping=None):
    """Translates a message and handles mapping
    """
    return to_utf8(_t(_(i18n_message, mapping=mapping)))


def is_valid_code(value):
    """Return whether the value can be used as code, without special characters
    except '-' and without empties
    """
    if not value:
        return False
    regex = r'^[a-zA-Z0-9\-]*$'
    if re.match(regex, value):
        return True
    return False


def check_code(code, context, portal_type=None, catalog=SETUP_CATALOG):
    """Raises an Invalid exception if the symptom code passed-in is not valid
    or not unique
    """
    if not is_valid_code(code):
        raise Invalid(_("Code cannot contain special characters or spaces"))

    if not portal_type:
        portal_type = api.get_portal_type(context)

    query = {"portal_type": portal_type}
    for brain in api.search(query, catalog):
        obj = api.get_object(brain)
        if obj.code == code:
            if obj != context:
                raise Invalid(_("Code must be unique"))
