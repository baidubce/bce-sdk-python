#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions
# and limitations under the License.

"""
This module defines RdsTaskManager interface
"""

import json

from baidubce.http import http_methods
from baidubce.services.rds import rds_http
from baidubce.services.rds.models import rds_task_model


class RdsTaskManager(rds_http.HttpRequest):
    """
     this is RdsTaskManager openApi interface
    :param rds_http.HttpRequest:
    """

    def __init__(self, config):
        """
        :param config:
        :type config: baidubce.BceClientConfiguration
        """

        rds_http.HttpRequest.__init__(self, config)

    def task_instance(self, page_size=None, page_no=None, end_time=None, instance_id=None,
                      instance_name=None, task_id=None, task_type=None, task_status=None,
                      start_time=None, config=None):
        """
         task list
        :param instance_id: the specified instance id
        :type instance_id: string

        :param page_size: the number of items per page
        :type page_size: int or None

        :param page_no:   the current page no
        :type page_no: int or None

        :param end_time:  the task executor  end time
        :type end_time: string or None

        :param instance_name: the specified instance name
        :type instance_name: string or None

        :param task_id:   the specified task id
        :type task_id: string or None

        :param task_type:  Task type, value: resize/switch/reboot/changeAzone
        :type task_type: string or None

        :param task_status: Task status, value, created/running/success/failed/cancelled
        :type task_status: string or None

        :param start_time:  Task  executor start time
        :type start_time: string or None

        :param config:
        :return:
        """

        data = {}

        if page_no is not None:
            data['pageNo'] = page_no
        if page_size is not None:
            data['pageSize'] = page_size
        if end_time is not None:
            data['endTime'] = end_time
        if instance_id is not None:
            data['instanceId'] = instance_id
        if instance_name is not None:
            data['instanceName'] = instance_name
        if task_id is not None:
            data['taskId'] = task_id
        if task_type is not None:
            data['taskType'] = task_type
        if task_status is not None:
            data['taskStatus'] = task_status
        if start_time is not None:
            data['startTime'] = start_time

        return rds_task_model.TaskResponse(
            self._send_request(http_method=http_methods.POST,
                               function_name='instance',
                               key='/task',
                               body=json.dumps(data),
                               config=config,
                               api_version=1))
