# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the
# License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.

"""
This module provides a model class for BCM.
"""


class CustomDimensionModel(dict):
    """
    This class define custom dimension.
    """
    def __init__(self, name, order, alias=""):
        """
        :param name:
            custom dimension name.
        :type name: string

        :param alias:
            custom dimension alias.
        :type alias: string

        :param order:
            custom dimension order.
        :type order: int
        """
        super(CustomDimensionModel, self).__init__()
        self["name"] = name
        self["order"] = order
        self["alias"] = alias


class EventLevel(object):
    """
    This class define event level.
    """
    NOTICE = "NOTICE"
    WARNING = "WARNING"
    MAJOR = "MAJOR"
    CRITICAL = "CRITICAL"
    __all_members = (NOTICE, WARNING, MAJOR, CRITICAL)

    @classmethod
    def contains(cls, event_level):
        """
        whether event_level is valid

        :param event_level:
            event level
        :type event_level: string

        :return:
        :rtype true/false
        """
        if event_level in cls.__all_members:
            return True
        return False

    @classmethod
    def all_event_levels(cls):
        """
        get all event levels

        :return:
        :rtype tuple
        """
        return cls.__all_members
