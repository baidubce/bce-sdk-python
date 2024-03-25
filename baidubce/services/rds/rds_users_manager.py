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
This module defines RdsUsersManager  interface
"""

import json

from baidubce.utils import required
from baidubce.http import http_methods
from baidubce.services.rds import rds_http
from baidubce.services.rds.models import rds_user_model
from baidubce.services.rds.custom.requestparam import rds_request_param_object as request_param


class RdsUsersManager(rds_http.HttpRequest):
    """
      this is RdsUsersManager open api interface
     :param rds_http.HttpRequest:
    """

    def __init__(self, config):
        """
        :param config:
        :type config: baidubce.BceClientConfiguration
        """

        rds_http.HttpRequest.__init__(self, config)

    @required(access_key=(object), instance_id=(str), ccount_name=(str), password=(str))
    def create_account(self, access_key, instance_id, account_name, password,
                       account_type=None, database_privileges=None, desc=None,
                       type=None, config=None):
        """
        create database account

        :param access_key:
            Request the required accessKey parameter
        :type account_type: object

        :param instance_id:
            The specified instance ID
        :type instance_id : str

        :param account_name:
            Account name created
        :type account_name: str

        :param password:
            The password for the account consists of letters,
            numbers, or underscores, with a length of 6-32 digits.

            Passwords need to be encrypted for transmission,
            and plaintext transmission is prohibited.
            For details, please refer to the definition
            of password encryption transmission specifications
        :type password: str

        :param account_type:
            Account permission type
            Common: regular account, Super: super account
        :type account_type: str or None

        :param database_privileges:
            Database Privilege object,
            which can be set for MySQL and SQL Server instances
        :type database_privileges: list or None

        :param desc:
            Account description information
        :type desc: str or None
        :param type:
            OnlyMaster: The account used on the primary instance,
            RdsProxy: The account used on the proxy instance
            corresponding to the primary instance,
            defaulting to the OnlyMaster account
        :type type: str or None

        :param config:
        :type config : baidubce.BceClientConfiguration

        :return:
        """

        data = {"accountName": account_name, "password": password}
        if account_type is not None:
            data["accountType"] = account_type
        if database_privileges is not None:
            data["databasePrivileges"] = database_privileges
        if desc is not None:
            data["desc"] = desc
        if type is not None:
            data["type"] = type

        return self._send_request(http_method=http_methods.POST,
                                  function_name='instance',
                                  key='/' + instance_id + '/account',
                                  headers={b"X-Bce-Accesskey": access_key},
                                  body=json.dumps(data, cls=request_param.JsonWrapper),
                                  config=config,
                                  api_version=1)

    @required(instance_id=(str))
    def query_account(self, instance_id, config=None):
        """
         Query account based on specified  instance ID

        :param instance_id:
            the specified instance ID
        :type instance_id:str

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        return rds_user_model.AccountList(
            self._send_request(http_method=http_methods.GET,
                               function_name='instance',
                               key='/' + instance_id + '/account',
                               config=config,
                               api_version=1))

    @required(instance_id=(str), account_name=(str))
    def query_account_detail(self, instance_id, account_name, config=None):
        """
         Query account detail

        :param instance_id:
            the specified  instance ID
        :type instance_id: str

        :param account_name:
            The account name of the database
        :type instance_id: str

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        return rds_user_model.AccountList(
            self._send_request(http_method=http_methods.GET,
                               function_name='instance',
                               key='/' + instance_id + '/account/' + account_name,
                               config=config,
                               api_version=1))

    @required(access_key=(object), instance_id=(str), account_name=(str), password=(str))
    def modify_account_password(self, access_key, instance_id, account_name, password,
                                config=None):
        """
         Modify account password

        :param access_key:
            Request the required accessKey parameter
        :type access_key: str

        :param instance_id:
            The specified  instance ID
        :type instance_id: str

        :param account_name:
            Modified database account name
        :type account_name: str

        :param password:
            Modified database account password
        :type password: str

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        data = {"password": password}

        return self._send_request(http_method=http_methods.PUT,
                                  function_name='instance',
                                  key='/' + instance_id + '/account/' + account_name +
                                      '/password',
                                  headers={b"X-Bce-Accesskey": access_key},
                                  body=json.dumps(data),
                                  config=config,
                                  api_version=1)

    @required(access_key=(object), e_tag=(str), instance_id=(str),
              account_name=(str), privileges_arrays=(list))
    def modify_account_privileges(self, access_key, e_tag, instance_id,
                                  account_name, privileges_arrays, config=None):
        """
         Modify account privileges

        :param access_key:
             Request the required accessKey parameter
        :type access_key: str

        :param e_tag:
            Obtain e_tag from query account details
        :type e_tag: str

        :param instance_id:
            The specified  instance ID
        :type instance_id: str

        :param account_name:
            The database account name
        :type account_name: str

        :param privileges_arrays:
            The Specific database permissions,
            adding permissions to a specific library.
            MySQL and SQL Server instances can set this option.
        :type privileges_arrays: list

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        """
        data = {}
        data["databasePrivileges"] = privileges_arrays
        return self._send_request(http_method=http_methods.PUT,
                                  function_name='instance',
                                  key='/' + instance_id + '/account/' + account_name +
                                      '/privileges',
                                  headers={b"X-Bce-Accesskey": access_key, b"x-bce-if-match": e_tag},
                                  body=json.dumps(data),
                                  config=config,
                                  api_version=1)

    @required(instance_id=(str), account_name=(str), remark=(str))
    def modify_account_remark(self, instance_id, account_name, remark, config=None):
        """

        modify account remark

        :param instance_id:
            The specified  instance ID
        :type instance_id: str

        :param account_name:
            The database account name
        :type account_name: str

        :param remark:
            Modify database notes
        :type remark: str

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        data = {"remark": remark}
        return self._send_request(http_method=http_methods.PUT,
                                  function_name='instance',
                                  key='/' + instance_id + '/account/' + account_name +
                                      "/desc",
                                  body=json.dumps(data),
                                  config=config,
                                  api_version=1)

    @required(instance_id=(str), account_name=(str))
    def delete_account(self, instance_id, account_name, config=None):
        """
         delete account

        :param instance_id:
            The specified  instance ID
        :type instance_id: str

        :param account_name:
            The database account name
        :type account_name: str

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        return self._send_request(http_method=http_methods.DELETE,
                                  function_name='instance',
                                  key='/' + instance_id + '/account/' + account_name,
                                  config=config,
                                  api_version=1)
