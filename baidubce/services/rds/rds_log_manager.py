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
this model defines RdsLogManager  interface
"""

import json

from baidubce.utils import required
from baidubce.http import http_methods
from baidubce.services.rds import rds_http
from baidubce.services.rds.models import rds_log_model


class RdsLogManager(rds_http.HttpRequest):
    """
     this is RdsLogManager openApi interface
    :param rds_http.HttpRequest:
    """

    def __init__(self, config):
        """
        :param config:
        :type config: baidubce.BceClientConfiguration
        """

        rds_http.HttpRequest.__init__(self, config)

    @required(instance_id=(str))
    def slow_log_detail(self, instance_id, start_time=None, end_time=None, page_no=None, page_size=None,
                        db_name=None, host_ip=None, user_name=None, sql=None, config=None):
        """
         get slow log detail

        :param instance_id:
            id of the slow log instance
        :type instance_id: str

        :param start_time:
            Slow log start time. The format is yyyy-mm-ddThh:mm:ssZ,
            for example,2014-07-30T15:06:00Z.
        :type start_time: str

        :param end_time:
            Slow log end time. The format is yyyy-mm-ddThh:mm:ssZ,
            for example,2014-08-20T18:06:00Z.
        :type end_time: str

        :param page_no:
            Current page count, not from the first page
        :type page_no: int

        :param page_size:
            Number of items per page. 10 items per page is recommended
        :type page_size: int

        :param db_name: database name list
        :type db_name: list

        :param host_ip: ip address list（ipv4）
        :type host_ip: list

        :param user_name: username list
        :type user_name: list

        :param sql: sql statement
        :type sql: str

        :param config:
        :return:
        """

        data = {}

        if start_time is not None:
            data['startTime'] = start_time
        if end_time is not None:
            data['endTime'] = end_time
        if page_no is not None:
            data['pageNo'] = page_no
        if page_size is not None:
            data['pageSize'] = page_size
        if db_name is not None:
            data['dbName'] = db_name
        if host_ip is not None:
            data['hostIp'] = host_ip
        if user_name is not None:
            data['userName'] = user_name
        if sql is not None:
            data['sql'] = sql

        return rds_log_model.SlowLogDetail(
            self._send_request(http_method=http_methods.POST,
                               function_name='instance',
                               key=instance_id + "/slowlogs/details",
                               body=json.dumps(data),
                               config=config,
                               api_version=1))

    @required(instance_id=(str))
    def error_log_detail(self, instance_id, start_time=None, end_time=None, page_no=None, page_size=None,
                         key_word=None, config=None):
        """
         get error log detail

        :param instance_id:
            id of the slow log instance
        :type instance_id: str

        :param start_time:
            Error log start time. The format is yyyy-mm-ddThh:mm:ssZ,
            for example,2014-07-30T15:06:00Z.
        :type start_time: str

        :param end_time:
            Error log end time. The format is yyyy-mm-ddThh:mm:ssZ,
            for example,2014-07-30T15:06:00Z.
        :type end_time: str

        :param page_no:
            Current page count, not from the first page
        :type page_no: int

        :param page_size:
            Number of items per page. 10 items per page is recommended
        :type page_size: int

        :param key_word:
            Search keywords
        :type key_word: str

        :param config:
        :type config: baidubce.BceClientConfiguration
        :return:
        :rtype: baidubce.services.rds.model.ErrorLogDetail
        """

        data = {}

        if start_time is not None:
            data['startTime'] = start_time
        if end_time is not None:
            data['endTime'] = end_time
        if page_no is not None:
            data['pageNo'] = page_no
        if page_size is not None:
            data['pageSize'] = page_size
        if key_word is not None:
            data['keyWord'] = key_word

        return rds_log_model.ErrorDetail(
            self._send_request(http_method=http_methods.POST,
                               function_name='instance',
                               key=instance_id + "/errorlogs/details",
                               body=json.dumps(data),
                               config=config,
                               api_version=1))

    @required(instance_id=(str), datetime=(str))
    def slow_log_list(self, instance_id, datetime, config=None):
        """
         get slow log list

        :param instance_id:
            The specify instance id
        :type instance_id: str

        :param datetime:
            The slow log time,The format is yyyy-mm-ddThh:mm:ssZ,
            For example,2014-07-30T15:06:00Z.
        :type datetime: str

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        return rds_log_model.SlowLogList(
            self._send_request(http_method=http_methods.GET,
                               function_name='instance',
                               key=instance_id + "/slowlogs/logList/" + datetime,
                               config=config,
                               api_version=1))

    @required(instance_id=(str), log_id=(str), download_valid_time_in_sec=(int))
    def slow_log_download_detail(self, instance_id, log_id, download_valid_time_in_sec, config=None):
        """
          slow log download detail

        :param instance_id:
            The specify instance id
        :type instance_id: str

        :param log_id:
            The slow log id

        :param download_valid_time_in_sec: 1800
        :type  download_valid_time_in_sec: int

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        return rds_log_model.DownLoadDetail(
            self._send_request(http_method=http_methods.GET,
                               function_name='instance',
                               key=instance_id + "/slowlogs/download_url/" +
                               log_id + "/" + download_valid_time_in_sec,
                               config=config,
                               api_version=1))

    @required(instance_id=(str), datetime=(str))
    def error_log_list(self, instance_id, datetime, config=None):
        """
         get error log list

        :param instance_id:
            The specify instance id
        :type instance_id: str

        :param datetime:
            The error log time,The format is yyyy-mm-ddThh:mm:ssZ,
            For example,2014-07-30T15:06:00Z.
        :type datetime: str

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.services.rds.model.ErrorLogList
        """

        return rds_log_model.ErrorLogList(
            self._send_request(http_method=http_methods.GET,
                               function_name='instance',
                               key=instance_id + "/errorlogs/logList/" + datetime,
                               config=config,
                               api_version=1))

    @required(instance_id=(str), log_id=(str), download_valid_time_in_sec=(str))
    def error_log_download_detail(self, instance_id, log_id, download_valid_time_in_sec, config=None):
        """
         error log download detail

        :param instance_id:
            The specify instance id
        :type instance_id: str

        :param log_id:
            The error log id
        :type log_id: str

        :param download_valid_time_in_sec: 1800
        :type  download_valid_time_in_sec: str

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :type: baidubce.services.rds.model.DownLoadDetail
        """

        return rds_log_model.DownLoadDetail(
            self._send_request(http_method=http_methods.GET,
                               function_name='instance',
                               key=instance_id + "/errorlogs/download_url/" + log_id + "/" +
                               download_valid_time_in_sec,
                               config=config,
                               api_version=1))
