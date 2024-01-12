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

from bika.lims.interfaces import IDoNotSupportSnapshots
from senaite.core.interfaces import IHideActionsMenu
from senaite.lims.interfaces import ISenaiteLIMS
from senaite.patient.interfaces import ISenaitePatientLayer
from zope.interface import Interface


class ISenaiteDiagnosisLayer(ISenaiteLIMS, ISenaitePatientLayer):
    """Zope 3 browser Layer interface specific for senaite.diagnosis
    This interface is referred in profiles/default/browserlayer.xml.
    All views and viewlets register against this layer will appear in the site
    only when the add-on installer has been run.
    """


class IContentFolder(IHideActionsMenu, IDoNotSupportSnapshots):
    """Marker interface for basic containers
    """


class IEtiologicAgents(IContentFolder):
    """Marker interface for container of Etiologic Agents
    """


class IEtiologicAgent(Interface):
    """Marker interface for Etiologic Agent objects
    """


class IDiseases(IContentFolder):
    """Marker interface for container of Diseases
    """


class IDisease(Interface):
    """Marker interface for Disease objects
    """


class ISymptoms(IContentFolder):
    """Marker interface for container of Symptoms
    """


class ISymptom(Interface):
    """Marker interface for Symptom objects
    """
