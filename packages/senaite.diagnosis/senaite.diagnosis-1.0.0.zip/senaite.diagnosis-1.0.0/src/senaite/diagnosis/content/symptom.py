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
from senaite.diagnosis.interfaces import ISymptom
from senaite.diagnosis.utils import check_code
from zope import schema
from zope.interface import implementer
from zope.interface import Invalid
from zope.interface import invariant


class ISymptomSchema(model.Schema):
    """Schema interface for Symptom content
    """

    code = schema.TextLine(
        title=_(
            "label_symptom_code",
            default="Code",
        ),
        description=_(
            "description_symptom_code",
            default="Unique code of this symptom"
        ),
        required=True,
    )

    title = schema.TextLine(
        title=_p("Title"),
        required=True,
    )

    description = schema.Text(
        title=_p("Description"),
        required=False,
    )

    gender = schema.Choice(
        title=_(
            "label_symptom_gender",
            default="Gender"
        ),
        description=_(
            "description_symptom_gender",
            default="Gender this symptom applies to"
        ),
        source="senaite.patient.vocabularies.gender",
        default="",
        required=False,
    )

    severity_levels = schema.Bool(
        title=_(
            "label_symptom_severity",
            default="Severity levels permitted"
        ),
        description=_(
            "description_symptom_severity",
            default="Select if patient can experience different stress levels "
                    "of this symptom (none, mild, moderate, severe)"
        ),
        required=False,
    )

    @invariant
    def validate_code(data):
        """Checks if the code for this symptom is unique
        """
        code = data.code

        # https://community.plone.org/t/dexterity-unique-field-validation
        context = getattr(data, "__context__", None)
        if context is not None:
            if context.code == code:
                # nothing changed
                return

        check_code(code, context, portal_type="Symptom")


@implementer(ISymptom, ISymptomSchema, IDeactivable)
class Symptom(Container):
    """Symptom content. Signs and symptoms are the observed or detectable
    signs, and experienced symptoms of an illness, injury, or condition. A sign
    for example may be a higher or lower temperature than normal, raised or
    lowered blood pressure or an abnormality showing on a medical scan. A
    symptom is something out of the ordinary that is experienced by an
    individual such as feeling feverish, a headache or other pain or pains in
    the body
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

    @security.protected(permissions.View)
    def getGender(self):
        accessor = self.accessor("gender")
        return accessor(self)

    @security.protected(permissions.ModifyPortalContent)
    def setGender(self, value):
        mutator = self.mutator("gender")
        mutator(self, value)

    @security.protected(permissions.View)
    def getSeverityLevels(self):
        accessor = self.accessor("severity_levels")
        return accessor(self)

    @security.protected(permissions.ModifyPortalContent)
    def setSeverityLevels(self, value):
        mutator = self.mutator("severity_levels")
        mutator(self, value)
