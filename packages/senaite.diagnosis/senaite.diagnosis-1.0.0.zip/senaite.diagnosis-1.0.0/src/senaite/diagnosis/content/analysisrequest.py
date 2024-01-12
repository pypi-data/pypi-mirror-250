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

from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaExtender
from bika.lims.interfaces import IAnalysisRequest
from Products.CMFCore.permissions import View
from senaite.core.browser.widgets import DateTimeWidget
from senaite.core.browser.widgets import ReferenceWidget
from senaite.core.catalog import SETUP_CATALOG
from senaite.diagnosis import messageFactory as _
from senaite.diagnosis import permissions
from senaite.diagnosis.content.fields import ExtDateTimeField
from senaite.diagnosis.content.fields import ExtUIDReferenceField
from senaite.diagnosis.interfaces import ISenaiteDiagnosisLayer
from zope.component import adapter
from zope.interface import implementer

NEW_FIELDS = [

    ExtUIDReferenceField(
        "Symptoms",
        allowed_types=("Symptom", ),
        multiValued=True,
        read_permission=View,
        write_permission=permissions.FieldEditSymptoms,
        widget=ReferenceWidget(
            label=_(
                "label_sample_symptoms",
                default="Signs and Symptoms"
            ),
            description=_(
                "description_sample_symptoms",
                default="Observed or detectable signs, and experienced "
                        "symptoms of an illness, injury, or condition"
            ),
            render_own_label=True,
            visible={
                "add": "edit",
            },
            catalog_name=SETUP_CATALOG,
            base_query={
                "is_active": True,
                "sort_on": "sortable_title",
                "sort_order": "ascending",
            },
        )
    ),

    ExtDateTimeField(
        "DateOfOnset",
        required=False,
        read_permission=View,
        write_permission=permissions.FieldEditDateOfOnset,
        widget=DateTimeWidget(
            render_own_label=True,
            label=_(
                "label_sample_dateofonset",
                default="Date of Onset"
            ),
            description=_(
                "description_sample_dateofonset",
                default="Date when the signs and symptoms were first noted"
            ),
            show_time=False,
            visible={
                "add": "edit"
            },
        ),
    ),

    ExtUIDReferenceField(
        "Diseases",
        allowed_types=("Disease", ),
        multiValued=True,
        read_permission=View,
        write_permission=permissions.FieldEditDiseases,
        widget=ReferenceWidget(
            label=_(
                "label_sample_diseases",
                default="Diseases or conditions"
            ),
            description=_(
                "description_sample_diseases",
                default="Particular abnormal conditions that negatively "
                        "affect the structure or function of all or part of "
                        "an organism. Often known to be medical conditions "
                        "that are associated with specific signs and symptoms"
            ),
            render_own_label=True,
            visible={
                "add": "edit",
            },
            catalog_name=SETUP_CATALOG,
            base_query={
                "is_active": True,
                "sort_on": "sortable_title",
                "sort_order": "ascending",
            },
        )
    ),

    ExtDateTimeField(
        "DateOfDiagnosis",
        required=False,
        read_permission=View,
        write_permission=permissions.FieldEditDateOfDiagnosis,
        widget=DateTimeWidget(
            render_own_label=True,
            label=_(
                "label_sample_dateofdiagnosis",
                default="Date of Diagnosis"
            ),
            description=_(
                "description_sample_dateofdiagnosis",
                default="Date when the diagnosis, as the process of "
                        "identifying a disease, condition or injure from its "
                        "signs and symptoms, was determined"
            ),
            show_time=False,
            visible={
                "add": "edit"
            },
        ),
    ),

    ExtUIDReferenceField(
        "EtiologicAgents",
        allowed_types=("EtiologicAgent", ),
        multiValued=True,
        read_permission=View,
        write_permission=permissions.FieldEditEtiologicAgents,
        widget=ReferenceWidget(
            label=_(
                "label_sample_etiologicagents",
                default="Etiologic agents"
            ),
            description=_(
                "description_sample_etiologicagents",
                default="Infectious agents (microorganisms or toxins) that "
                        "cause or may cause the disease or diseases"
            ),
            render_own_label=True,
            visible={
                "add": "edit",
            },
            catalog_name=SETUP_CATALOG,
            base_query={
                "is_active": True,
                "sort_on": "sortable_title",
                "sort_order": "ascending",
            },
        )
    ),

]


@adapter(IAnalysisRequest)
@implementer(ISchemaExtender, IBrowserLayerAwareExtender)
class AnalysisRequestSchemaExtender(object):
    """Extends the Sample (aka AnalysisRequest) with additional fields
    """
    layer = ISenaiteDiagnosisLayer

    def __init__(self, context):
        self.context = context

    def getFields(self):  # noqa CamelCase
        return NEW_FIELDS
