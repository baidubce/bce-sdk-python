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


class Dimension(dict):
    """
    This class define dimension.
    """
    def __init__(self, name, value):
        """
        :param name: dimension name.
        :type name: string

        :param value: dimension value.
        :type value: string
        """
        super(Dimension, self).__init__()
        self["name"] = name
        self["value"] = value


class KV(dict):
    """
    This class define kv.
    """
    def __init__(self, key, value):
        """
        :param key: key.
        :type key: string

        :param value: dimension value.
        :type value: string
        """
        super(KV, self).__init__()
        self["key"] = key
        self["value"] = value


class PolicyResource(dict):
    """
    This class define policy resource.
    """
    def __init__(self, identifiers, metric_dimensions=None):
        """
        :param identifiers: identifiers.
        :type identifiers: Dimension array

        :param metric_dimensions: metric dimensions.
        :type metric_dimensions: Dimension array
        """
        super(PolicyResource, self).__init__()
        if metric_dimensions is None:
            metric_dimensions = []
        self["identifiers"] = identifiers
        self["metricDimensions"] = metric_dimensions


class MonitorObject(dict):
    """
    This class define monitor object.
    """
    def __init__(self, object_type, names, resources=None, type_name="Instance"):
        """
        :param object_type: monitor object type.
        :type object_type: string

        :param names: monitor object names.
        :type names: string array

        :param resources: monitor object resources.
        :type resources: PolicyResource array

        :param type_name: monitor object typename.
        :type type_name: string
        """
        super(MonitorObject, self).__init__()
        if resources is None:
            resources = []
        self["type"] = object_type
        self["names"] = names
        self["resources"] = resources
        self["typeName"] = type_name


class AlarmRule(dict):
    """

    private Long index;
    private String metric;
    private Long periodInSecond;
    private String statistics;
    private String threshold;
    private String comparisonOperator;
    private Integer evaluationPeriodCount;
    private List<Dimension> metricDimensions;

    This class define alarm rule.
    """
    def __init__(self, index, metric, period, statistics, threshold, operator, evaluation_count,
                 metric_dimensions=None):
        """
        :param index: alarm rule index.
        :type index: int

        :param metric: metric name.
        :type metric: string

        :param period: period in second.
        :type period: int

        :param statistics: statistics.
        :type statistics: string

        :param threshold: threshold.
        :type threshold: string

        :param operator: comparison operator.
        :type operator: string

        :param evaluation_count: evaluation period count.
        :type evaluation_count: int

        :param metric_dimensions: metric dimensions.
        :type metric_dimensions: Dimension array
        """
        super(AlarmRule, self).__init__()
        if metric_dimensions is None:
            metric_dimensions = []
        self["index"] = index
        self["metric"] = metric
        self["periodInSecond"] = period
        self["statistics"] = statistics
        self["threshold"] = threshold
        self["comparisonOperator"] = operator
        self["evaluationPeriodCount"] = evaluation_count
        self["metricDimensions"] = metric_dimensions


class AlarmAction(dict):
    """
    This class define alarm action.
    """
    def __init__(self, name, action_id=""):
        """
        :param name: action name.
        :type name: string

        :param id: action id.
        :type id: string
        """
        super(AlarmAction, self).__init__()
        self["name"] = name
        self["id"] = action_id


class AlarmConfigRule(dict):
    """
    This class define alarm config rule.
    """
    def __init__(self, metric_name, operator, statistics, threshold, window=60, metric_dimensions=None):
        """
        :param metric_name: metric name.
        :type metric_name: string

        :param operator: operator.
        :type operator: string

        :param statistics: statistics.
        :type statistics: string

        :param threshold: threshold.
        :type threshold: float

        :param window: window.
        :type window: int

        :param metric_dimensions: metric dimensions.
        :type metric_dimensions: KV array
        """
        super(AlarmConfigRule, self).__init__()
        if metric_dimensions is None:
            metric_dimensions = []
        self["metricName"] = metric_name
        self["operator"] = operator
        self["statistics"] = statistics
        self["threshold"] = threshold
        self["window"] = window
        self["metricDimensions"] = metric_dimensions


class AlarmConfigPolicy(dict):
    """
    This class define alarm config policy.
    """
    def __init__(self, rules, alarm_pending_count):
        """
        :param rules: alarm config rules.
        :type rules: AlarmConfigRule array

        :param alarm_pending_count: alarm pending period count.
        :type alarm_pending_count: int
        """
        super(AlarmConfigPolicy, self).__init__()
        self["rules"] = rules
        self["alarmPendingPeriodCount"] = alarm_pending_count


class TargetInstance(dict):
    """
    This class define alarm config policy target instance.
    """
    def __init__(self, region, identifiers, metric_dimensions=None):
        """
        :param region: region.
        :type region: string

        :param identifiers: identifiers.
        :type identifiers: KV array

        :param metric_dimensions: metric dimensions.
        :type metric_dimensions: KV array
        """
        super(TargetInstance, self).__init__()
        if metric_dimensions is None:
            metric_dimensions = []
        self["region"] = region
        self["identifiers"] = identifiers
        self["metricDimensions"] = metric_dimensions


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

class MetricDatum(dict):
    """
    This class metric datum.
    """
    def __init__(self, metric_name, dimensions, value, timestamp):

        """
        :param metric_name: metric_name
        :type  metric_name: string
        :param dimensions: dimensions
        :type  dimensions: list
        :param value: value
        :type value: double
        :param timestamp: timestamp
        :type  timestamp: string
        """

        super(MetricDatum, self).__init__()
        self["metricName"] = metric_name
        self["dimensions"] = dimensions
        self["value"] = value
        self["timestamp"] = timestamp


class SiteAlarmRule(dict):
    """
    This class define site alarm policy config
    """

    def __init__(self, metric, metric_alias, cycle, statistics, threshold, comparison_operator, count,
                 function, act_on_idcs, act_on_isps, version_site):
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
        :param function:
        :type function: string
        :param act_on_idcs:
        :type act_on_idcs: list
        :param act_on_isps:
        :type act_on_isps: list
        :param version_site:
        :type version_site: string
        """
        super(SiteAlarmRule, self).__init__()
        self["metric"] = metric
        self["metricAlias"] = metric_alias
        self["cycle"] = cycle
        self["statistics"] = statistics
        self["threshold"] = threshold
        self["function"] = "THRESHOLD"
        self["comparisonOperator"] = comparison_operator
        self["count"] = count
        self["actOnIdcs"] = act_on_idcs
        self["actOnIsps"] = act_on_isps
        self["versionSite"] = version_site


class CustomAlarmRule(dict):
    """
    This class define custom alarm policy config
    """

    def __init__(self, metric, cycle, statistics, threshold, comparison_operator, count,
                 index, metric_dimensions):
        """

        :param metric: metric identifier
        :type metric: string
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
        :param index: rule's sequence, begin with 0
        :type index: int
        :param metric_dimensions: dimensions
        :type metric_dimensions: list
        """
        super(CustomAlarmRule, self).__init__()
        self["metricName"] = metric
        self["cycle"] = cycle
        self["statistics"] = statistics
        self["threshold"] = threshold
        self["function"] = "THRESHOLD"
        self["comparisonOperator"] = comparison_operator
        self["count"] = count
        self["index"] = index
        self["metricDimensions"] = metric_dimensions


class SiteOnceConfig(dict):
    """
    This class define site once config
    """

    def __init__(self, anonymous_login=None, method=None, post_content=None, kidnap_white=None, resolve_type=None,
                 server=None, packet_count=None, port=None, input_type=None, input_data=None, output_type=None,
                 expected_output=None, username=None, password=None):
        """

        :param anonymous_login: anonymous login
        :type anonymous_login: bool
        :param method: method, enum: get, post, put, delete, patch
        :type method: string
        :param post_content: post content
        :type post_content: string
        :param kidnap_white: kidnap white
        :type kidnap_white: bool
        :param resolve_type: resolve type
        :type resolve_type: string
        :param server: server
        :type server: string
        :param packet_count: packet count
        :type packet_count: int
        :param port: port
        :type port: int
        :param input_type: input type
        :type input_type: string
        :param input_data: input data
        :type input_data: string
        :param output_type: output type
        :type output_type: string
        :param expected_output: expected output
        :type expected_output: string
        :param username: username
        :type username: string
        :param password: password
        :type password: string
        """
        super(SiteOnceConfig, self).__init__()
        self["anonymousLogin"] = anonymous_login
        self["method"] = method
        self["postContent"] = post_content
        self["kidnapWhite"] = kidnap_white
        self["resolveType"] = resolve_type
        self["server"] = server
        self["packetCount"] = packet_count
        self["port"] = port
        self["inputType"] = input_type
        self["input"] = input_data
        self["outputType"] = output_type
        self["expectedOutput"] = expected_output
        self["username"] = username
        self["password"] = password


class AdvancedConfig(dict):
    """
    This class define advanced site once config
    """

    def __init__(self, cookies=None, user_agent=None, host=None, response_code=None,
                 response_check=None, username=None, password=None, input_type=None,
                 input_data=None, output_type=None, expected_output=None):
        """
       :param cookies: cookies
       :type cookies: string
       :param user_agent: user agent
       :type user_agent: string
       :param host: host
       :type host: string
       :param response_code: response code
       :type response_code: int
       :param response_check: response check
       :type response_check: bool
       :param username: username
       :type username: string
       :param password: password
       :type password: string
       :param input_type: input type
       :type input_type: string
       :param input_data: input data
       :type input_data: string
       :param output_type: output type
       :type output_type: string
       :param expected_output: expected output
       :type expected_output: string
       """
        super(AdvancedConfig, self).__init__()
        self["cookies"] = cookies
        self["userAgent"] = user_agent
        self["host"] = host
        self["responseCode"] = response_code
        self["responseCheck"] = response_check
        self["username"] = username
        self["password"] = password
        self["inputType"] = input_type
        self["input"] = input_data
        self["outputType"] = output_type
        self["expectedOutput"] = expected_output
