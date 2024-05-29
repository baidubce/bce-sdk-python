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
This module provides a client class for openApi rds backup.
"""

import json

from baidubce.utils import required
from baidubce.http import http_methods
from baidubce.services.rds import rds_http
from baidubce.services.rds.models import rds_backup_policy_model
from baidubce.services.rds.custom.requestparam import rds_request_param_object as request_param


class RdsBackupManager(rds_http.HttpRequest):

    """
      this is openApi rds backup manager sdk client
     :param rds_http.HttpRequest:
    """

    def __init__(self, config):
        """
        :param config:
        :type config: baidubce.BceClientConfiguration
        """
        rds_http.HttpRequest.__init__(self, config)

    @required(instance_id=(str), backup_id=(str))
    def backup_detail(self, instance_id, backup_id, config=None):
        """
         this is  open api backup detail
        :param instance_id:
            The Specify the instance short id,for example: rds-rWLm6n4e
        :type instance_id: str

        :param backup_id:
            The Specify the backup id,for example: 1702325499881950802
        :param config:  config

        :type config: baidubce.BceClientConfiguration
        :return:

        """
        return rds_backup_policy_model.BackUpDetail(
            self._send_request(http_method=http_methods.GET,
                               function_name='instance',
                               key=instance_id + '/backup/' + backup_id,
                               body=None,
                               config=config,
                               api_version=1))

    @required(instance_id=(str))
    def backup_list(self, instance_id, marker=None, max_keys=None, config=None):
        """
         this is open api backup list
        :param instance_id:
             The Specify the instance short id,for example: rds-rWLm6n4e
        :type instance_id: str

        :param marker:
            The backup snapshot ID that needs to be searched，
        :type marker: str or None

        :param max_keys:
            Number of entries per page, default to 10
        :type max_keys: int

        :param config:config
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype rds_backup_policy_model.BackUpList
        """

        if marker is None:
            marker = '-1'

        if max_keys is None:
            max_keys = 1000

        params = {
            "marker": marker,
            "maxKeys": max_keys
        }

        return rds_backup_policy_model.BackUpList(
            self._send_request(http_method=http_methods.GET,
                               function_name='instance',
                               key=instance_id + '/backup',
                               params=params,
                               config=config,
                               api_version=1))

    @required(instance_id=(str), backup_days=(str),
              backup_time=(str), persistent=(bool))
    def modify_backup_policy(self, instance_id, backup_days, backup_time, persistent, expire_in_days=None,
                             config=None):
        """
          this is open api modify backup policy

         :param instance_id:
            The Specify the instance short id,for example: rds-rWLm6n4e
         :type instance_id: str

         :param backup_days:
            Backup time day separated by a comma in English,
            with Sunday as the first day, with a value of 0，
            Example: "0,1,2,3,5,6"(mandatory)
         :type backup_days: str

         :param backup_time:
            Backup start time, the time here is in UTC yyyy-mm-ddThh:mmZ format,
         :type backup_time: str
         :param persistent:
            Is backup data persistence enabled,ture or false
         :type persistent: bool

         :param expire_in_days:
            Persistence days, ranging from 1-730 days;
            If not enabled, it is 0 or left blank
         :type expire_in_days: int

         :param config:config
         :type config: baidubce.BceClientConfiguration

         :return: void
        """

        data = {
            "backupDays": backup_days,
            "backupTime": backup_time,
            "persistent": persistent
        }

        if expire_in_days is not None:
            data['expireInDays'] = int(expire_in_days)

        return self._send_request(http_method=http_methods.PUT,
                                  function_name='instance',
                                  key=instance_id,
                                  params={"modifyBackupPolicy": ""},
                                  body=json.dumps(data),
                                  config=config,
                                  api_version=1)

    @required(instance_id=(str), effective_time=(str), data_backup_type=(str),
              data_backup_objects=(list))
    def full_backup(self, instance_id, effective_time=None, data_backup_type=None,
                    data_backup_objects=None, config=None):
        """
         Fully backup the database and data tables on the backup instance

        :param instance_id:
            The Specify the instance short id,for example: rds-rWLm6n4e
        :type  instance_id: str

        :param effective_time:
            Window field. The operation execution method has two values:
            timewindow and immediate. Among them, timewindow represents
            execution within the time window,and immediate represents
            immediate execution.The default is immediate. The default
            time window for the instance is from 05:00 to 06:00
        ：type effective_time: str

        :param data_backup_type:
            Backup type, supports physical/snapshot, with a value of snapshot.
            If the disk type is SSD, snapshot backup is not supported
        ：type data_backup_type: str

        :param data_backup_objects:
            Tables/tables that require backup or restoring library/table objects
        :type data_backup_objects: list

        :param config:config
        :type config: baidubce.BceClientConfiguration

        :return:
       """

        data = {}
        if effective_time is not None:
            data['effectiveTime'] = effective_time
        elif data_backup_type is not None:
            data['dataBackupType'] = data_backup_type
        elif data_backup_objects is not None:
            data['dataBackupObjects'] = data_backup_objects

        return self._send_request(http_method=http_methods.POST,
                                  function_name='instance',
                                  key=instance_id + '/backup',
                                  body=json.dumps(data),
                                  config=config,
                                  api_version=1)

    @required(instance_id=(str), snapsho_id=(str))
    def delete_specified_backup(self, instance_id, snapshot_id, config=None):
        """
          delete specified backup  sdk client
         :param instance_id:
             The Specify the instance short id,for example: rds-rWLm6n4e
         :type  instance_id: str

         :param snapshot_id:
             Delete the specified backup snapshot id, for example: 1701950306675099301
         :type  snapshot_id: str

         :param config: config
         :type  config: baidubce.BceClientConfiguration

         :return:
        """

        return self._send_request(http_method=http_methods.DELETE,
                                  function_name='instance',
                                  key=instance_id + '/backup/' + snapshot_id,
                                  config=config,
                                  api_version=1)

    @required(instance_id=(str), date_time=(str))
    def binlog_list(self, instance_id, date_time, config=None):
        """
         Get the binlog list on the instance  sdk client

        :param instance_id:
            The Specify the instance short id,for example: rds-rWLm6n4e
        :type  instance_id: str

        :param date_time:
            The time to obtain the binglog list, here is UTC time. Users need to
            calculate the UTC time themselves and fill it in，The time to obtain
            the binglog list, here is UTC time. Users need to calculate the UTC
            time themselves and fill it in,The format is YYYY-MM-DDThh:mm:ss:z
        :type date_time: str

        :param config: config
        :type  config: baidubce.BceClientConfiguration

        :return:
        """

        return rds_backup_policy_model.BinlogList(
            self._send_request(http_method=http_methods.GET,
                               function_name='instance',
                               key=instance_id + '/binlogs/' + date_time,
                               config=config,
                               api_version=1))

    @required(instance_id=(str), binlog_id=(str),
              download_valid_time_in_sec=(str))
    def binlog_detail(self, instance_id, binlog_id, download_valid_time_in_sec, config=None):
        """
         obtain bean log details based on instance id

        :param instance_id:
            The Specify the instance short id,for example: rds-rWLm6n4e
        :type binlog_id: str

        :param download_valid_time_in_sec:
            download effective time/S
        :type download_valid_time_in_sec: int

        :param config: config
        :type  config: baidubce.BceClientConfiguration

        :return: BinlogDetail
        :return: string
       """

        return rds_backup_policy_model.BinlogDetail(
            self._send_request(http_method=http_methods.GET,
                               function_name='instance',
                               key=instance_id +
                               '/binlogs/' +
                               binlog_id +
                               "/" +
                               download_valid_time_in_sec,
                               config=config,
                               api_version=1))

    @required(instance_id=(str), date_time=(str), data=(list))
    def restore_at_backup_in_time(self, instance_id, date_time, data, target_instance_id=None,
                                  config=None):
        """
        Restore the backup database, specified database, specified table,
         and backup table at the backup point in time. Please refer to the
         official website of RDS Open API for details

         :param instance_id:
            The Specify the instance short id,for example: rds-rWLm6n4e
         :type  instance_id: str

         :param date_time:
            Execution time point of instance logical backup
         :type  date_time: str

         :param data:
            Need to restore the library/table on the instance object
         :type  data: list

         :param target_instance_id:
            Specify the instance short id,for example: rds-fOtDrTd6
         :type  target_instance_id: str or None

         :param config: config
         :type  config: baidubce.BceClientConfiguration

         :return: BinlogDetail
         :return: json string
        """

        param_body = {"datetime": date_time, "data": data}

        if target_instance_id is not None:
            param_body['targetInstanceId'] = target_instance_id

        return self._send_request(http_method=http_methods.PUT,
                                  function_name='instance',
                                  key=instance_id +
                                  "/recoveryToSourceInstanceByDatetime",
                                  body=json.dumps(param_body, cls=request_param.JsonWrapper),
                                  config=config,
                                  api_version=1)

    @required(instance_id=str, snapshot_id=str, data=list)
    def restore_at_backup_in_snap_short(self, instance_id, snapshot_id, data, target_instance_id=None,
                                        config=None):
        """
         The instance that needs to be restored for backup should be
         restored according to the ID of the backup snapshot

        :param instance_id:
            Backup instance ID
        :type instance_id: str

        :param snapshot_id:
            The backup snapshot ID on the corresponding instance
        :type snapshot_id: str

        :param data:
            Need to restore the library/table on the instance object
        :type data: list

        :param target_instance_id:
        :type  target_instance_id: str or None

        :param config:
        :type  config: baidubce.BceClientConfiguration

        :return:
        :rtype:
        """

        param_body = {
            "snapshotId": snapshot_id,
            'data': data
        }

        if target_instance_id is not None:
            param_body['targetInstanceId'] = target_instance_id

        return self._send_request(http_method=http_methods.PUT,
                                  function_name='instance',
                                  key=instance_id +
                                  "/recoveryToSourceInstanceBySnapshot",
                                  body=json.dumps(param_body, cls=request_param.JsonWrapper),
                                  config=config,
                                  api_version=1)
