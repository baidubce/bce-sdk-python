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
This module defines RdsRecyclerManager interface
"""

import json

from baidubce.utils import required
from baidubce.http import http_methods
from baidubce.services.rds import rds_http
from baidubce.services.rds.models import rds_recycler_model


class RdsRecyclerManager(rds_http.HttpRequest):
    """
      this is RdsRecyclerManager openApi interface
     :param rds_http.HttpRequest:
    """

    def __init__(self, config):
        """
        :param config:
        :type config: baidubce.BceClientConfiguration
        """

        rds_http.HttpRequest.__init__(self, config)

    def recycler_list(self, marker=None, max_keys=None, config=None):
        """
         Get instances recycler list

        :param marker: Find the instance id in the recycle bin list
        :type marker: str or None

        :param max_keys: the current number
        :type max_keys: int or None

        :param config:
        :type config: baidubce.BceClientConfiguration
        :return:
        """

        params = {}
        if marker is not None:
            params[b'marker'] = marker
        if max_keys is not None:
            params[b'maxKeys'] = max_keys
        return rds_recycler_model.RecyclerList(
            self._send_request(http_methods.GET,
                               function_name='instance/recycler/list',
                               params=params,
                               config=config))

    @required(instance_ids=list)
    def recycler_recover(self, instance_ids, config=None):
        """
         Get instances recycler recover

        :param instance_ids:
            List of instance ids in the recycle bin
        :type instance_ids: list

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        data = {
            'instanceIds': instance_ids
        }
        return self._send_request(http_method=http_methods.PUT,
                                  function_name='instance/recycler/recover',
                                  body=json.dumps(data),
                                  config=config,
                                  api_version=1)

    @required(instance_id=(str))
    def delete_recycler(self, instance_id, config=None):
        """
         Delete the instance from the recycle bin

        :param instance_id: the instance id in recycle bin
        :type instance_id: str

        :param config:
        :type config: baidubce.BceClientConfiguration
        :return:
        """

        return self._send_request(http_method=http_methods.DELETE,
                                  function_name='instance/recycler',
                                  key=instance_id,
                                  config=config,
                                  api_version=1)

    @required(instance_ids=(str))
    def delete_recycler_batch(self, instance_ids, config=None):
        """
         Batch delete instances from Recycle bin

        :param instance_ids: the instance id in recycle bin
        :type instance_ids: str

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        return self._send_request(http_method=http_methods.DELETE,
                                  function_name='instance/recycler/batch',
                                  params={"instanceIds": instance_ids},
                                  config=config,
                                  api_version=1)
