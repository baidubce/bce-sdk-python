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
This module defines RdsDataBaseManager interface
"""

import json

from baidubce.utils import required
from baidubce.http import http_methods
from baidubce.services.rds import rds_http
from baidubce.services.rds.custom.requestparam import rds_request_param_object as request_param


class RdsDataBaseManager(rds_http.HttpRequest):
    """
      this is RdsDataBaseManager openApi sdk client
     :param rds_http.HttpRequest:
    """

    def __init__(self, config):
        """
        :param config:
        :type config: baidubce.BceClientConfiguration
        """

        rds_http.HttpRequest.__init__(self, config)

    @required(instance_id=(str), data=(dict))
    def create_database(self, instance_id, data, config=None):
        """
         create a database on the specified instance

        :param instance_id:
            The specified instance ID
        :type instance_id: str

        :param data:
            This data is an AccountPrivilege array object
        :type data: list

        :param config: baidubce.BceClientConfiguration
        :type config: baidubce.BceClientConfiguration

        :return: void
        :@rtype: void
        """

        return self._send_request(http_method=http_methods.POST,
                                  function_name='instance',
                                  key='/' + instance_id + '/databases',
                                  body=json.dumps(data, cls=request_param.JsonWrapper),
                                  config=config,
                                  api_version=1)

    @required(instance_id=(str))
    def query_database_list(self, instance_id, config=None):
        """
          query database information to return as a list

         :param instance_id:
            The instance id that needs to be queried
         :type  instance_id: str

         :param config: config
         :type config: baidubce.BceClientConfiguration

         :return: json
         :type: string
        """

        return self._send_request(http_method=http_methods.GET,
                                  function_name='instance',
                                  key='/' + instance_id + '/databases',
                                  config=config,
                                  api_version=1)

    @required(instance_id=(str), db_name=(str), remark=(str))
    def update_database_remark(self, instance_id, db_name=None, remark=None, config=None):
        """
         update the database remark on the specified instance

        :param instance_id:
            The specified instance ID
        :type  instance_id: str

        :param db_name:
            The specified database name
        :type  instance_id: str

        :param remark:
            need to update remark
        :type  instance_id: str

        :param config: config
        :type config: baidubce.BceClientConfiguration
        :return: void
        """

        data = {"remark": remark}

        return self._send_request(http_method=http_methods.PUT,
                                  function_name='instance',
                                  key='/' + instance_id + '/databases/' + db_name + '/remark',
                                  body=json.dumps(data, cls=request_param.JsonWrapper),
                                  config=config,
                                  api_version=1)

    @required(instance_id=(str), db_port=(int))
    def update_database_port(self, instance_id, db_port=None, config=None):
        """
         Update the database port on the specified instance

        :param instance_id:
            The specified instance ID
        :type instance_id: str

        :param db_port:
            need to update port
        :type db_port: int

        :param config: config
        :type config: baidubce.BceClientConfiguration
        :return: void
        :rtype: void
        """

        data = {"entryPort": db_port}

        return self._send_request(http_method=http_methods.PUT,
                                  function_name='instance',
                                  key='/' + instance_id + '/port',
                                  body=json.dumps(data, cls=request_param.JsonWrapper),
                                  config=config,
                                  api_version=1)

    @required(instance_id=(str), db_name=(str))
    def delete_database(self, instance_id, db_name=None, config=None):
        """
         Delete the database on the specified instance

        :param instance_id:
            The specified instance ID
        :rtype: str

        :param db_name:
            need to update db_name
        :rtype: str

        :param config: config
        :type config: baidubce.BceClientConfiguration
        :return: void
        :rtype: void
        """

        return self._send_request(http_method=http_methods.DELETE,
                                  function_name='instance',
                                  key='/' + instance_id + '/databases/' + db_name,
                                  config=config,
                                  api_version=1)
