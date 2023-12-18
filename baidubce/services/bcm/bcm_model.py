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


class DisableTime(dict):
    """
    This class define disable time
    """

    def __init__(self, from_time, to_time):
        """

        :param from_time: disable start time, such as 08:00:00
        :type from_time: string
        :param to_time: disable end time, such as 08:00:00
        :type to_time: string
        """
        super(DisableTime, self).__init__()
        self["from"] = from_time
        self["to"] = to_time


class Notification(dict):
    """
    This class define notification
    """

    def __init__(self, type, receiver=""):
        """

        :param type: enum, EMAIL, SMS, PHONE
        :type type: string
        :param receiver: receiver id
        :type receiver string
        """
        super(Notification, self).__init__()
        self["type"] = type
        self["receiver"] = receiver


class Member(dict):
    """
    This class define member
    """

    def __init__(self, type, id, name):
        """

        :param type: enum, notifyParty or notifyGroup
        :type type: string
        :param id: receiver id
        :type id string
        :param name: receiver's name
        :type name: string
        """
        super(Member, self).__init__()
        self["type"] = type
        self["id"] = id
        self["name"] = name


class ApplicationAlarmRule(dict):
    """
    This class define application alarm policy config
    """

    def __init__(self, metric, metric_alias, cycle, statistics, threshold, comparison_operator, count,
                 sequence, metric_dimensions):
        """

        :param metric: metric identifier
        :type metric: string
        :param metric_alias: metric name
        :type metric_alias: string
        :param cycle: period, second
        :type cycle: int
        :param statistics: statistics, enum: average, minimum, maximum, sum
        :type statistics: string
        :param threshold:
        :type threshold: float
        :param comparison_operator: operator, enum: ">", "<", ">=", "<="
        :type: string
        :param count:
        :type count: int
        :param sequence: rule's sequence, begin with 0
        :type sequence: int
        :param metric_dimensions: dimensions
        :type metric_dimensions: list
        """
        super(ApplicationAlarmRule, self).__init__()
        self["metric"] = metric
        self["metricAlias"] = metric_alias
        self["cycle"] = cycle
        self["statistics"] = statistics
        self["threshold"] = threshold
        self["function"] = "THRESHOLD"
        self["comparisonOperator"] = comparison_operator
        self["count"] = count
        self["sequence"] = sequence
        self["metricDimensions"] = metric_dimensions


class ApplicationObjectView(dict):
    """
    This class define the monitorObjectView in application monitor alarm
    """

    def __init__(self, monitor_object_name, monitor_object_name_view="", metric_dimension_view=""):
        """

        :param monitor_object_name: taskName
        :type monitor_object_name: string
        :param monitor_object_name_view: displayed name
        :type monitor_object_name_view: string
        :param metric_dimension_view:
        :type string
        """
        super(ApplicationObjectView, self).__init__()
        self["monitorObjectName"] = monitor_object_name
        self["monitorObjectNameView"] = monitor_object_name_view
        self["metricDimensionView"] = metric_dimension_view


class ApplicationMonitorObject(dict):
    """
    This class define application monitor object
    """

    def __init__(self, monitor_object_type, monitor_object_view):
        """

        :param monitor_object_type: enum: APP, SERVICE
        :type monitor_object_type: string
        :param monitor_object_view: monitor object
        :type monitor_object_view: list
        """
        super(ApplicationMonitorObject, self).__init__()
        self["monitorObjectType"] = monitor_object_type
        self["monitorObjectView"] = monitor_object_view


class EventFilter(dict):
    """
    This class define event filter
    """

    def __init__(self, event_level, event_type_list, eventAliasNames):
        """
        :param event_level: event level, enum: NOTICE, WARNING, MAJOR, CRITICAL, * means all
        :type event_level: string
        :param event_type_list: event type list, * means all
        :type event_type_list: list
        :param eventAliasNames: event alias name list, * means all
        :type eventAliasNames: list
        """
        super(EventFilter, self).__init__()
        self["eventLevel"] = event_level
        self["eventTypeList"] = event_type_list
        self["eventAliasNames"] = eventAliasNames


class EventResourceFilter(dict):
    """
    This class define event resource filter
    """

    def __init__(self, region, type, monitor_object_type, resources):
        """

        :param region: region
        :type region: string
        :param type: resource type, enum: APP, SERVICE
        :type type: string
        :param monitor_object_type: monitor object type, enum: ALL, TAG
        :type monitor_object_type: string
        :param resources: resource list of EventResource
        :type resources: list of EventResource
        """
        super(EventResourceFilter, self).__init__()
        self["region"] = region
        self["type"] = type
        self["monitorObjectType"] = monitor_object_type
        self["resources"] = resources


class EventResource(dict):
    """
    This class define event resource
    """

    def __init__(self, identifiers):
        """
        :param identifiers: resource identifiers
        :type identifiers: list of Dimension
        """
        super(EventResource, self).__init__()
        self["identifiers"] = identifiers


class Dimension(dict):
    """
    This class define dimension
    """

    def __init__(self, name, value):
        """
        :param name: dimension name
        :type name: string
        :param value: dimension value
        :type value: string
        """
        super(Dimension, self).__init__()
        self["name"] = name
        self["value"] = value


class MonitorResource(dict):
    """
    This class define monitor resource
    """

    def __init__(self, user_id, region, service_name, type_name, resource_id, identifiers=None,
                 properties=None, tags=None):
        """
        :param user_id: user id
        :type user_id: string
        :param region: region
        :type region: string
        :param service_name: service name
        :type service_name: string
        :param type_name: type name
        :type type_name: string
        :param resource_id: resource id
        :type resource_id: string
        :param identifiers: identifier list
        :type identifiers: list of Dimension
        :param properties: property list
        :type properties: list of Dimension
        :param tags: tag list
        :type tags: list of Dimension
        """
        super(MonitorResource, self).__init__()
        self["userId"] = user_id
        self["region"] = region
        self["serviceName"] = service_name
        self["typeName"] = type_name
        self["resourceId"] = resource_id
        self["identifiers"] = identifiers
        self["properties"] = properties
        self["tags"] = tags
