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

from AccessControl import ClassSecurityInfo
from bika.lims import api
from bika.lims.interfaces import IDeactivable
from plone.dexterity.content import Container
from plone.supermodel import model
from Products.CMFCore import permissions
from senaite.core import PloneMessageFactory as _p
from senaite.core.catalog import SETUP_CATALOG
from senaite.diagnosis import messageFactory as _
from senaite.diagnosis.interfaces import IDisease
from senaite.diagnosis.utils import check_code
from zope import schema
from zope.interface import implementer
from zope.interface import Invalid
from zope.interface import invariant


class IDiseaseSchema(model.Schema):
    """Schema interface
    """

    code = schema.TextLine(
        title=_(
            "label_disease_code",
            default="Code"
        ),
        description=_(
            "description_disease_code",
            default="Unique code of this disease"
        ),
        required=True,
    )

    title = schema.TextLine(
        title=_p("Title"),
        required=False,
    )

    description = schema.Text(
        title=_p("Description"),
        required=False,
    )

    @invariant
    def validate_code(data):
        """Checks if the code for this disease is unique
        """
        code = data.code

        # https://community.plone.org/t/dexterity-unique-field-validation
        context = getattr(data, "__context__", None)
        if context is not None:
            if context.code == code:
                # nothing changed
                return

        check_code(code, context, portal_type="Disease")


@implementer(IDisease, IDiseaseSchema, IDeactivable)
class Disease(Container):
    """Disease content. A disease is a particular abnormal condition that
    negatively affects the structure or function of all or part of an organism,
    and that is not immediately due to any external injury. Often known to be
    medical conditions that are associated with specific signs and symptoms.
    Disease is often used more broadly to refer to any condition that causes
    pain, dysfunction, distress, social problems, or death to the person
    afflicted, or similar problems for those in contact with the person.
    In this broader sense, it sometimes includes injuries, disabilities,
    disorders, syndromes, infections, isolated symptoms, deviant behaviors,
    and atypical variations of structure and function, while in other contexts
    and for other purposes these may be considered distinguishable categories.
    """

    # Catalogs where this type will be catalogued
    _catalogs = [SETUP_CATALOG]

    security = ClassSecurityInfo()
    exclude_from_nav = True

    @security.private
    def accessor(self, fieldname):
        """Return the field accessor for the fieldname
        """
        schema = api.get_schema(self)
        if fieldname not in schema:
            return None
        return schema[fieldname].get

    @security.private
    def mutator(self, fieldname):
        """Return the field mutator for the fieldname
        """
        schema = api.get_schema(self)
        if fieldname not in schema:
            return None
        return schema[fieldname].set

    @security.protected(permissions.View)
    def getCode(self):
        accessor = self.accessor("code")
        return accessor(self)

    @security.protected(permissions.ModifyPortalContent)
    def setCode(self, value):
        if value == self.code:
            # Nothing changed
            return

        try:
            check_code(value, self)
        except Invalid as ex:
            raise ValueError(ex.message)

        mutator = self.mutator("code")
        mutator(self, value)
