#! usr/bin/python
# -*-coding:utf-8 -*-
# Copyright 2014 Baidu, Inc.
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
This module defines RdsReadOnlyGroupManager interface
"""

import json

from baidubce.utils import required
from baidubce.http import http_methods
from baidubce.services.rds import rds_http
from baidubce.services.rds.models import rds_readonly_group_model
from baidubce.services.rds.custom.requestparam import rds_request_param_object as request_param


class RdsReadOnlyGroupManager(rds_http.HttpRequest):
    """
      this is RdsReadOnlyGroupManager openApi interface
     :param rds_http.HttpRequest:
    """

    def __init__(self, config):
        """
        :param config:
        :type config: baidubce.BceClientConfiguration
        """

        rds_http.HttpRequest.__init__(self, config)

    @required(instance_id=(str), vpc_id=(str), subnet_id=(str))
    def create_readonly_group(self, instance_id, vpc_id, subnet_id, ro_group_name=None,
                              enable_delay_off=None, least_app_amount=None,
                              balance_reload=None, bgw_group_exclusive=None,
                              bgw_groupId=None, entry_port=None, vnet_ip=None,
                              delay_threshold=None, config=None):
        """
         create readonly group

        :param instance_id:
            the specified instance id
        :type instance_id: str

        :param vpc_id:
            the specified vpc id
        :type vpc_id: str

        :param subnet_id:
            the specified subnet id
        :type subnet_id: str

        :param ro_group_name:
            the created ro group name
        :type ro_group_name: str or None

        :param enable_delay_off:
            Whether to enable deferred culling.
            The default value is off. When enabled,
            read-only instances in a group that experience
            latency and reach a threshold are removed from
            the group if the minimum number of retained instances is met
        :type enable_delay_off: bool(True/False) or None

        :param least_app_amount:
            Minimum number of reserved instances in a group.
            The value is an integer ranging from 0 to 5. Default is 1
        :type least_app_amount: int or None

        :param balance_reload:
            Whether to enable the reload balancing switch.
            The default value is disabled. After this function
            is enabled, old connections are disconnected when
            the weight of read-only instances in a group is changed
        :type balance_reload: bool(True/False)

        :param bgw_group_exclusive:
            The value is assigned to a shared cluster or a dedicated
            cluster. The default value is false
        :type bgw_group_exclusive: bool(True/False) or None

        :param bgw_groupId:
            Cluster ID, if passed, to which cluster to assign the blb;
            If no dedicated cluster is transmitted, use the dedicated
            cluster with the least default configuration.
            If no dedicated cluster is transmitted, use the shared
            cluster with the least default configuration.
        :type bgw_groupId: str or None

        :param entry_port:
            Service port. The default value MySQL is 3306
        :type entry_port: int or None

        :param vnet_ip:
            The IP address of the virtual network, for example 10.254.38.96
        :type vnet_ip: str or None

        :param delay_threshold:
            The value is an integer greater than or equal to 0. Default is 10
        :type delay_threshold: int or None

        :param config:
        :type config: baidubce.BceClientConfiguration or None

        :return:
        """

        data = {"vpcId": vpc_id, "subnetId": subnet_id}

        if ro_group_name is not None:
            data["roGroupName"] = ro_group_name
        if enable_delay_off is not None:
            data["enableDelayOff"] = enable_delay_off
        if bgw_groupId is not None:
            data["bgwGroupId"] = bgw_groupId
        if entry_port is not None:
            data["entryPort"] = int(entry_port)
        if vnet_ip is not None:
            data["vnetIp"] = vnet_ip

        if least_app_amount is None:
            data["leastAppAmount"] = 1
        else:
            data["leastAppAmount"] = int(least_app_amount)

        if bgw_group_exclusive is None:
            data["bgwGroupExclusive"] = False
        else:
            data["bgwGroupExclusive"] = bgw_group_exclusive

        if delay_threshold is None:
            data["delayThreshold"] = 10
        else:
            data["delayThreshold"] = int(delay_threshold)

        if balance_reload is None:
            data["balanceReload"] = False
        else:
            data["balanceReload"] = bool(balance_reload)

        return rds_readonly_group_model.ReadOnlyGroupList(
            self._send_request(http_method=http_methods.POST,
                               function_name='rds',
                               key='/' + instance_id + "/rogroup",
                               body=json.dumps(data),
                               config=config,
                               api_version=1))

    @required(instance_id=(str), ro_group_id=(str))
    def readonly_group_detail(self, instance_id, ro_group_id, config=None):
        """
         get readonly group detail

        :param instance_id:
            the specified instance id
        :type instance_id: str

        :param ro_group_id:
            the specified ro group id
        :type ro_group_id: str

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        return rds_readonly_group_model.ReadOnlyGroupDetail(
            self._send_request(http_method=http_methods.GET,
                               function_name='rds',
                               key='/' + instance_id + "/rogroup/detail/" + ro_group_id,
                               config=config,
                               api_version=1))

    @required(instance_id=(str))
    def master_instance_associated_readonly_List(self, instance_id, config=None):
        """
         Displays the list of read-only groups associated
         with the primary instance.

        :param instance_id:
            the specified instance id
        :type instance_id: str

        :param config:
        :type config: baidubce.BceClientConfiguration

        @return:
        """

        return rds_readonly_group_model.MasterInstanceAssociatedReadOnlyList(
            self._send_request(http_method=http_methods.GET,
                               function_name='rds',
                               key='/' + instance_id + "/rogroup/list",
                               config=config,
                               api_version=1))

    @required(instance_id=(str), ro_group_id=(str), read_replica_list=(list))
    def join_readonly_group(self, instance_id, ro_group_id, read_replica_list, config=None):
        """
         You can add read-only instances to a read-only group
         individually or add a maximum of four word read groups in a batch.

        :param instance_id:
            the specified source isntance id
        :type instance_id: str

        :param ro_group_id:
            the specified ro group id
        :type ro_group_id: str

        :param read_replica_list:
            the specified read replica list include more read app
        :type read_replica_list: list

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        data = {"readReplicaList": read_replica_list}

        self._send_request(http_method=http_methods.PUT,
                           function_name='rds',
                           key=instance_id + '/rogroup/' + ro_group_id + "/join",
                           body=json.dumps(data),
                           config=config,
                           api_version=1)

    @required(instance_id=(str), ro_group_id=(str))
    def readonly_group_load_balance(self, source_app_id, ro_group_id, config=None):
        """
         Load balancing is restarted for the read-only group

        :param source_app_id:
            The specified source isntance id
        :type source_app_id: str

        :param ro_group_id:
            The specified ro group id
        :type ro_group_id: str

        :param config: config
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        self._send_request(http_method=http_methods.PUT,
                           function_name='rds',
                           key=source_app_id + '/rogroup/' + ro_group_id + "/reload",
                           config=config,
                           api_version=1)

    @required(source_app_id=(str), ro_group_id=(str))
    def batch_modify_readonly_group_properties(self, source_app_id, ro_group_id, ro_group_name=None,
                                               enable_delay_off=None, delay_threshold=None,
                                               balance_reload=None, least_app_amount=None,
                                               read_replica_list=None, config=None):
        """
         batch modify readonly group properties

        :param source_app_id:
            The specified source instance id
        :type source_app_id: str

        :param ro_group_id:
            The specified ro group id
        :type ro_group_id: str

        :param ro_group_name:
            Name of the read-only group that you want to change
        :type ro_group_name: str or None

        :param enable_delay_off:
            Delay auto-delete switch of read-only groups，true / false
        :type enable_delay_off: bool or None

        :param delay_threshold:
            Delay threshold. The value must be an integer greater than
            or equal to 0, ranging from 1 to 2147483646
        :type delay_threshold: int or None

        :param balance_reload:
            Re-load balancing switch of the read-only group, true / false
        :type balance_reload: bool or None

        :param least_app_amount:
            Minimum number of reserved instances in a group.
            The value is an integer ranging from 0 to 5. Default is 1
        :type least_app_amount: int or None

        :param read_replica_list:
            List of read-only instances for which you want to change the
            weight Recommended range: 1-100
         :type read_replica_list: list or None

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        data = {}
        if source_app_id is not None:
            data["sourceAppId"] = source_app_id
        if ro_group_id is not None:
            data["roGroupId"] = ro_group_id
        if ro_group_name is not None:
            data["roGroupName"] = ro_group_name
        if enable_delay_off is not None:
            data["enableDelayOff"] = enable_delay_off
        if delay_threshold is not None:
            data["delayThreshold"] = int(delay_threshold)
        if balance_reload is not None:
            data["balanceReload"] = bool(balance_reload)
        if least_app_amount is not None:
            data["leastAppAmount"] = int(least_app_amount)
        if read_replica_list is not None:
            data["readReplicaList"] = read_replica_list

        self._send_request(http_method=http_methods.PUT,
                           function_name='rds',
                           key=source_app_id + '/rogroup/' + ro_group_id +
                           "/updateRoGroupProperty",
                           body=json.dumps(data), config=config,
                           api_version=1)

    @required(source_app_id=(str), ro_group_id=(str), publicly_accessible=(bool))
    def update_publicly_accessible(self, source_app_id, ro_group_id, publicly_accessible, config=None):
        """
         Enable or disable a public network

        :param source_app_id:
            The specified source isntance id
        :type source_app_id: str

        :param ro_group_id:
            The specified readonly group id
        :type ro_group_id: str

        :param publicly_accessible:
            ture / false
        :type publicly_accessible: bool

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        data = {"publiclyAccessible": publicly_accessible}

        self._send_request(http_method=http_methods.PUT,
                           function_name='rds',
                           key=source_app_id + '/rogroup/' + ro_group_id +
                           "/updatePubliclyAccessible",
                           body=json.dumps(data),
                           config=config,
                           api_version=1)

    @required(source_app_id=(str), ro_group_id=(str), endpoint=(request_param.Endpoint))
    def update_endpoint(self, source_app_id, ro_group_id, endpoint, ro_group_name=None,
                        least_app_amount=None, delay_threshold=None, config=None):
        """
         update endpoint information

        :param source_app_id:
            The specified source isntance id
        :type source_app_id: str

        :param ro_group_id:
            The specified read-only group id
        :type ro_group_id: str

        :param endpoint:
            The specified endpoint object
        :type endpoint: baidubce.services.rds.request_param.Endpoint

        :param ro_group_name:
            The update readonly group name
        :type ro_group_name: str or None

        :param least_app_amount:
            Change the minimum number of reserved instances in a group
            update  ranging from 0 to 5. Default is 1
        :type least_app_amount: int or None

        :param delay_threshold:
            Enable or disable intra-group balance recovery
        :type delay_threshold: int or None

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        data = {"endpoint": endpoint.to_json()}

        if ro_group_name is not None:
            data["roGroupName"] = ro_group_name
        if least_app_amount is not None:
            data["leastAppAmount"] = int(least_app_amount)
        if delay_threshold is not None:
            data["delayThreshold"] = int(delay_threshold)

        self._send_request(http_method=http_methods.PUT,
                           function_name='rds',
                           key=source_app_id + '/rogroup/' + ro_group_id +
                           "/updateEndpoint",
                           body=json.dumps(data),
                           config=config,
                           api_version=1)

    @required(source_app_id=(str), ro_group_id=(str), read_replica_list=(list))
    def level_readonly_group(self, source_app_id, ro_group_id, read_replica_list, config=None):
        """
         level readonly group
        :param source_app_id:
            The specified source instance id
        :type source_app_id: str

        :param ro_group_id:
            The level read-only group id
        :type ro_group_id: str

        :param read_replica_list:
            The level read-only group  read-only instance list
        :type read_replica_list: list

        :param config: config
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        data = {"readReplicaList": read_replica_list}

        self._send_request(http_method=http_methods.PUT,
                           function_name='rds',
                           key=source_app_id + '/rogroup/' + ro_group_id + "/leave",
                           body=json.dumps(data),
                           config=config,
                           api_version=1)

    @required(source_app_id=(str), ro_group_id=(str))
    def delete_readonly_group(self, source_app_id, ro_group_id, config=None):
        """
         delete readonly group

        :param source_app_id:
            The specified source instance id
        :type source_app_id: str

        :param ro_group_id:
            The specified read-only group id
        :type ro_group_id: str

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        self._send_request(http_method=http_methods.DELETE,
                           function_name='rds',
                           key=source_app_id + '/rogroup/' + ro_group_id,
                           config=config,
                           api_version=1)
