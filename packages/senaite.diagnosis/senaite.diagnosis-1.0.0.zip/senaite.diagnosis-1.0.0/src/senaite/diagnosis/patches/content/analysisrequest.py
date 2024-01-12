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

def getRawSymptoms(self):  # noqa camelcase
    """Returns the UIDs of the Symptom objects assigned to the Sample
    """
    return self.getField("Symptoms").getRaw(self)


def getSymptoms(self):  # noqa camelcase
    """Returns the symptom objects assigned to the Sample
    """
    return self.getField("Symptoms").get(self)


def setSymptoms(self, value):  # noqa camelcase
    """Sets the symptoms to the sample
    """
    self.getField("Symptoms").set(self, value)


def getDateOfOnset(self):  # noqa camelcase
    """Returns the date of onset, when the signs and symptoms were first noted
    """
    return self.getField("DateOfOnset").get(self)


def setDateOfOnset(self, value):  # noqa camelcase
    """Sets the date of onset, when the signs and symptoms were first noted
    """
    self.getField("DateOfOnset").set(self, value)


def getDateOfDiagnosis(self):  # noqa camelcase
    """Returns the date of diagnosis, when the diagnosis was/were determined
    """
    return self.getField("DateOfDiagnosis").get(self)


def setDateOfDiagnosis(self, value):  # noqa camelcase
    """Sets the date of diagnosis, when the diagnosis was/were determined
    """
    self.getField("DateOfDiagnosis").set(self, value)


def getRawDiseases(self):  # noqa camelcase
    """Returns the UIDs of the Disease objects assigned to the Sample
    """
    return self.getField("Diseases").getRaw(self)


def getDiseases(self):  # noqa camelcase
    """Returns the Disease objects assigned to the sample
    """
    return self.getField("Diseases").get(self)


def setDiseases(self, value):  # noqa camelcase
    """Sets the diseases to the sample
    """
    self.getField("Diseases").set(self, value)


def getRawEtiologicAgents(self):  # noqa camelcase
    """Returns the UIDs of the EtiologicAgent objects assigned to the Sample
    """
    return self.getField("EtiologicAgents").getRaw(self)


def getEtiologicAgents(self):  # noqa camelcase
    """Returns the EtiologicAgent objects assigned to the sample
    """
    return self.getField("EtiologicAgents").get(self)


def setEtiologicAgents(self, value):  # noqa camelcase
    """Sets the etiologic agents to the sample
    """
    self.getField("EtiologicAgents").set(self, value)
