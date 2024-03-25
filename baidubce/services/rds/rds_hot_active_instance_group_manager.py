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
This module defines RdsHotActiveInstanceGroupManager interface,
"""

import json

from baidubce.http import http_methods
from baidubce.services.rds import rds_http
from baidubce.services.rds.models import rds_hot_active_instance_group_model as\
    rds_hot_active_instance_group_model


class RdsHotActiveInstanceGroupManager(rds_http.HttpRequest):
    """
      this is RdsHotActiveInstanceGroupManager openApi interface
     :param rds_http.HttpRequest:
    """

    def __init__(self, config):
        """
        :param config:config
        :type config: baidubce.BceClientConfiguration
        """

        rds_http.HttpRequest.__init__(self, config)

    def force_change_instance(self, group_id, leader_id, force=None, max_behind=None, config=None):
        """
          Specify a hot active instance to forcibly switch to the main role

         :param group_id:
            The instance group id
            to the primary role
         :type group_id: str

         :param leader_id:
            The instance ID in the instance group that needs to switch
            to the primary role
         :type leader_id: str or None

         :param force:
            Used in fault state,0- Non fault (used in non fault state) 1-
            Fault
         :type force: int or None

         :param max_behind:
            Maximum allowable backup behind_Master value (0 indicates
            that the data from the backup database and the faulty main
            database must be completely consistent. It is recommended
            that the business gradually  increase from 0 until the
            maximum tolerance value is reached.When force=0, this
            parameter does not take effect)
         :type force: int or None

         :param config:config
         :type config: baidubce.BceClientConfiguration or None

         :return: json str
         :type: josn
        """

        data = {
            "leaderId": leader_id,
            "force": force,
            "maxBehind": max_behind
        }

        return rds_hot_active_instance_group_model.ForceChangeResponse(
            self._send_request(http_method=http_methods.PUT,
                               function_name='instance',
                               key="/group/" + group_id + '/forceChange',
                               body=json.dumps(data),
                               config=config,
                               api_version=1))

    def group_batch_join(self, follower_ids, name, leader_id, config=None):
        """
         Interface Description
             1.This interface is used to batch add instances to the hot instance
             group sdk client.

         matters needing attention
            1.To join a hot instance group, the following prerequisites must be met

            2.The active instance group only supports MYSQL version 5.6/5.7

            3.The synchronization mode of the main instance must be asynchronous
              synchronization

            4.The primary instance must have GTID enabled

            5.The location of the primary instance ID must be consistent with the
              current requested location

            6.Batch added leader nodes cannot be within the current instance group

        :param follower_ids:
            slave instance short ID array
        :type follower_ids: list

        :param name:
            Name of joining the instance group
        :type name: str

        :param leader_id:
            Leader instance short ID
        :type leader_id: str

        :param config: config
        :type config: baidubce.BceClientConfiguration

        :return: void
        :type:  void
        """

        data = {
            "followerIds": follower_ids,
            "name": name,
            "leaderId": leader_id
        }

        return self._send_request(http_method=http_methods.POST,
                                  function_name='instance',
                                  key='/group/batchjoin',
                                  body=json.dumps(data),
                                  config=config,
                                  api_version=1)

    def create_group(self, name, leader_id, config=None):
        """
         Create a hot instance group

        :param name:
            Instance Group Name
        :type name: str

        :param leader_id:
            Need to create an instance ID as a leader node
        :type leader_id: str

        :param config: config
        :type config: baidubce.BceClientConfiguration

        :return: void
        :type:  void
        """

        data = {
            "name": name,
            "leaderId": leader_id
        }

        return self._send_request(http_method=http_methods.POST,
                                  function_name='instance',
                                  key='/group',
                                  body=json.dumps(data),
                                  config=config,
                                  api_version=1)

    def group_list(self, order=None, order_by=None, page_no=None, page_size=None, filter_map_str=None,
                   days_to_expiration=None, config=None):
        """
         Get a list of hot instance groups

        :param order: asc/desc
        :type order: str

        :param order_by: sort field
        :type order_by: str

        :param page_no:
            Current number of pages,
        :type page_no: int

        :param page_size:
            Number of entries per page
        :type page_size: int

        :param filter_map_str:
            Filtering that includes，three aspects: groupId, groupName, and instanceStatus
              # filter_map_str = "{\"groupId\":\"rdcqzga9i4s\"}"
              # filter_map_str = "{\"groupName\":\"acount-test\"}"
              # filter_map_str = "{\"instanceStatus\":\"topoModifying\"}"

        :param days_to_expiration:
            Deadline, default to -1
        :type days_to_expiration: int

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        params = {"manner": "page"}

        if order is not None:
            params["order"] = order
        if order_by is not None:
            params["orderBy"] = order_by
        if page_no is not None:
            params["pageNo"] = page_no
        if page_size is not None:
            params["pageSize"] = page_size
        if filter_map_str is not None:
            params["filterMapStr"] = filter_map_str
        if days_to_expiration is not None:
            params["daysToExpiration"] = days_to_expiration

        return rds_hot_active_instance_group_model.GroupResponse(
            self._send_request(http_method=http_methods.GET,
                               function_name='instance',
                               key='/group', params=params,
                               config=config,
                               api_version=1))

    def detail_group(self, group_id, config=None):
        """
         Query details of hot instance groups

        :param group_id:
            ID of the hot instance group
        :type group_id: str

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:json str
        :GroupDetailResponse
        """

        return rds_hot_active_instance_group_model.GroupDetailResponse(
            self._send_request(http_method=http_methods.GET,
                               function_name='instance',
                               key='/group/' + group_id,
                               config=config,
                               api_version=1))

    def check_gtid_group(self, instance_id, config=None):
        """
         This interface is used for instance group pre-check (GTID check).

        :param instance_id:
            the Specifies the instance ID
        :type instance_id: str

        :param config:config
        :type config: baidubce.BceClientConfiguration

        :return result: true or false
        :rtype result: rds_hot_active_instance_group_model.GroupCheckGtidResponse
        """

        data = {
            "instanceId": instance_id
        }

        return rds_hot_active_instance_group_model.GroupCheckGtidResponse(
            self._send_request(http_method=http_methods.POST,
                               function_name='instance',
                               key='/group/checkGtid',
                               body=json.dumps(data),
                               config=config,
                               api_version=1))

    def check_ping_group(self, source_id, target_id, config=None):
        """
         This interface is used for instance group pre-check
         (instance connectivity check). The region of the
         current request must be the same as the region
         where the sourceId resides.

        :param source_id:
            Source instance id
        :type source_id: str

        :param target_id:
            Target instance id
        :type source_id: str

        :param config: config
        :type config: baidubce.BceClientConfiguration

        :return result: true or false
        :rtype result: rds_hot_active_instance_group_model.GroupCheckPingResponse
        """

        data = {
            "sourceId": source_id,
            "targetId": target_id
        }

        return rds_hot_active_instance_group_model.GroupCheckPingResponse(
            self._send_request(http_method=http_methods.POST,
                               function_name='instance',
                               key='/group/checkPing',
                               body=json.dumps(data),
                               config=config,
                               api_version=1))

    def check_data_group(self, instance_id, config=None):
        """
         this interface is used for instance group pre-check
         (data check). The region of the incoming instance
         instanceId must be the same as that of the current
         request.

        :param instance_id:
            the Specifies the instance ID
        :type instance_id: str

        :param config: config
        :type config: baidubce.BceClientConfiguration

        :return result : true or false
        :rtype result: rds_hot_active_instance_group_model.GroupCheckDataResponse

        """

        data = {
            "instanceId": instance_id
        }

        return rds_hot_active_instance_group_model.GroupCheckDataResponse(
            self._send_request(http_method=http_methods.POST,
                               function_name='instance',
                               key='/group/checkData',
                               body=json.dumps(data),
                               config=config,
                               api_version=1))

    def add_instance_to_group(self, group_id, follower_id, config=None):
        """
         adding an instance group refers to adding an existing
         instance group. The instance to be added cannot be
         an existing hot live instance group

        :param group_id:
            The Specify the ID of the created Heat instance group
        :type group_id: str

        :param follower_id:
            The ID of the instance to be added
        :type follower_id: str

        :param config:config
        :type config: baidubce.BceClientConfiguration

        :return result:true or false
        :rtype result :bool
        """

        data = {
            "followerId": follower_id
        }

        return self._send_request(http_method=http_methods.POST,
                                  function_name='instance',
                                  key='/group/' + group_id + '/instance',
                                  body=json.dumps(data),
                                  config=config,
                                  api_version=1)

    def modify_instances_group_name(self, group_id, group_name, config=None):
        """
         modify instances group name

        :param group_id:
            The Specifies the ID of the hot instance group
        :type group_id: str

        :param group_name:
            Name of the Heat instance group that you want to modify
        :type group_name: str

        :param config: config
        :type config: baidubce.BceClientConfiguration
        :return:
    """

        data = {
            "name": group_name
        }

        return self._send_request(http_method=http_methods.POST,
                                  function_name='instance',
                                  key='/group/' + group_id + '/name',
                                  body=json.dumps(data),
                                  config=config,
                                  api_version=1)

    def delete_instances_group(self, group_id, config=None):
        """
         delete a specified instance group. Only one leader instance can be deleted

        :param group_id:
            id of the instance group to be deleted
        :type group_id: str

        :param config: config
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        return self._send_request(http_method=http_methods.DELETE,
                                  function_name='instance',
                                  key='/group/' + group_id,
                                  config=config,
                                  api_version=1)

    def master_role_change(self, group_id, leader_id, config=None):
        """
         To switch the instance of the instance group to the primary role

        :param group_id:
            The Specifies the ID of the hot instance group
        : type group_id: str

        :param leader_id:
            Switch the instance of the master role
        ：type leader_id: str

        :param config: config
        ：type config: baidubce.BceClientConfiguration

        :return:
        :rtype:
        """

        data = {
            "leaderId": leader_id
        }

        return self._send_request(http_method=http_methods.PUT,
                                  function_name='instance',
                                  key='/group/' + group_id + '/instance',
                                  body=json.dumps(data),
                                  config=config,
                                  api_version=1)

    def quit_instances_group(self, group_id, instance_id, config=None):
        """
         To exit the hot instance group, the region of the incoming
         instance instanceId must be the same as that of the current
         request

        :param group_id:
            id of the group from which you want to exit the
            hot instance group
        :type group_id: str

        :param instance_id:
            id of the hot instance group from which you want
            to exit
        :type instance_id: str

        :param config: config
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype:
        """

        data = {
            "groupId": group_id,
            "instanceId": instance_id
        }

        return self._send_request(http_method=http_methods.DELETE,
                                  function_name='instance',
                                  key='/group/' + group_id + '/instance/' + instance_id,
                                  config=config,
                                  api_version=1)

    def check_min_version(self, leader_id, follower_id, config=None):
        """
         pre-check the minor version of the instance added to the
         hot live group

        :param leader_id:
            The specifies the id of the leader instance
        :type leader_id: str

        :param follower_id:
            The specifies the follower instance id
        :type follower_id: str

        :param config:config
        :type config: baidubce.BceClientConfiguration

        :return result: true or false
        :rtype result: bool
        """

        data = {
            "leaderId": leader_id,
            "followerId": follower_id
        }

        return self._send_request(http_method=http_methods.POST,
                                  function_name='instance',
                                  key='/group/checkVersion',
                                  body=json.dumps(data),
                                  config=config,
                                  api_version=1)
