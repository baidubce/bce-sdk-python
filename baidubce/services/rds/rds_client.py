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
This module provides a client class for SCS.
"""
from __future__ import unicode_literals

import copy
import json
import logging
import uuid

import http.client

import baidubce.services.rds.model as model
from baidubce import utils
from baidubce.auth import bce_v1_signer
from baidubce.bce_base_client import BceBaseClient
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceClientError
from baidubce.exception import BceServerError
from baidubce.http import bce_http_client
from baidubce.http import http_headers
from baidubce.http import http_methods
from baidubce.services import scs, rds
from baidubce.utils import required

_logger = logging.getLogger(__name__)


def _parse_result(http_response, response):
    if http_response.status / 100 == http.client.CONTINUE / 100:
        raise BceClientError('Can not handle 1xx http status code')
    bse = None
    body = http_response.read()
    if body:
        d = json.loads(body)

        if http_response.status / 100 != http.client.OK / 100:
            r_code = d['code']
            # 1000 means success
            if r_code != '1000':
                bse = BceServerError(d['message'],
                                     code=d['code'],
                                     request_id=d['requestId'])
            else:
                response.__dict__.update(
                    json.loads(body, object_hook=utils.dict_to_python_object).__dict__)
                http_response.close()
                return True
        elif http_response.status / 100 == http.client.OK / 100:
            response.__dict__.update(
                json.loads(body, object_hook=utils.dict_to_python_object).__dict__)
            http_response.close()
            return True
    elif http_response.status / 100 == http.client.OK / 100:
        return True

    if bse is None:
        bse = BceServerError(http_response.reason, request_id=response.metadata.bce_request_id)
    bse.status_code = http_response.status
    raise bse  # pylint: disable-msg=E0702


class RdsClient(BceBaseClient):
    """
    Rds sdk client
    """

    def __init__(self, config=None):
        if config is not None:
            self._check_config_type(config)
        BceBaseClient.__init__(self, config)

    @required(config=BceClientConfiguration)
    def _check_config_type(self, config):
        return True

    @required(instance_name=(str), engine=(str), engine_version=(str), category=(str),
              cpuCount=int, memory_capacity=int, volume_capacity=int, disk_io_type=(str), purchase_count=int,
              zone_names=list, vpc_id=(str), is_direct_pay=bool, subnets=list, tags=list, bgw_group_id=(str),
              bgw_group_exclusive=bool, character_set_name=(str), lower_case_table_names=int,
              parameter_template_id=(str), auto_renew_time_unit=(str), auto_renew_time=int,
              initial_data_reference=model.InitialDataReference, data=list, billing=model.Billing)
    def create_instance(self, engine, engine_version, category, cpu_count, memory_capacity, volume_capacity,
                        disk_io_type, is_direct_pay=None, initial_data_reference=None, bgw_group_id=None,
                        bgw_group_exclusive=None, character_set_name=None, lower_case_table_names=None,
                        parameter_template_id=None, data=None, instance_name=None, vpc_id=None, subnets=None, tags=None,
                        purchase_count=1, zone_names=None, auto_renew_time_unit='month', auto_renew_time=None,
                        billing=model.Billing(), config=None):
        """
        Create instance with specific config

        :param purchase_count: Instance count
        :type purchase_count: int

        :param instance_name: Instance name
        :type  instance_name: string

        :param engine:
        :type  engine: string

        :param engine_version:
        :type  engine_version: string or unicode

        :param category: Singleton or Standard
        :type  category: string

        :param cpu_count:
        :type  cpu_count: int

        :param memory_capacity:
        :type  memory_capacity: int

        :param volume_capacity:
        :type  volume_capacity: int

        :param disk_io_type: normal_io; cloud_high; cloud_nor; cloud_enha
        :type  disk_io_type: string

        :param zone_names:
        :type  zone_names: list

        :param vpc_id:
        :type  vpc_id: string

        :param is_direct_pay:
        :type  is_direct_pay: bool

        :param subnets: list of model.SubnetMap
        :type  subnets: list

        :param tags:
        :type  tags: list

        :param bgw_group_id:
        :type  bgw_group_id: string

        :param bgw_group_exclusive:
        :type  bgw_group_exclusive: bool

        :param character_set_name:
        :type  character_set_name: string

        :param lower_case_table_names:
        :type  lower_case_table_names: int

        :param parameter_template_id:
        :type  parameter_template_id: string

        :param auto_renew_time_unit: Renew monthly or yearly,value in ['month','year]
        :type  auto_renew_time_unit: str

        :param auto_renew_time: If billing is Prepay, the automatic renewal time is 1-9
         when auto_renew_time_unit is 'month' and 1-3 when auto_renew_time_unit is 'year'
        :type  auto_renew_time: int

        :param initial_data_reference:
        :type  initial_data_reference: model.InitialDataReference

        :param data:
        :type  data: list

        :param billing: default billing is Prepay 1 month
        :type  billing: model.Billing

        :param config: None
        :type  config: BceClientConfiguration

        :return: Object
            {
                "instance_ids": ["rds-sgrw14145"]
            }

        :rtype: baidubce.bce_response.BceResponse
        """
        data = {
            'billing': billing.__dict__,
            'purchaseCount': purchase_count,
            'instanceName': instance_name,
            'engine': engine,
            'engineVersion': engine_version,
            'category': category,
            'cpuCount': cpu_count,
            'memoryCapacity': memory_capacity,
            'volumeCapacity': volume_capacity,
            'diskIoType': disk_io_type,
            'zoneNames': zone_names,
            'vpcId': vpc_id,
            'isDirectPay': is_direct_pay,
            'subnets': subnets,
            'tags': tags,
            'bgwGroupId': bgw_group_id,
            'bgwGroupExclusive': bgw_group_exclusive,
            'characterSetName': character_set_name,
            'lowerCaseTableNames': lower_case_table_names,
            'parameterTemplateId': parameter_template_id,
            'autoRenewTimeUnit': auto_renew_time_unit,
            'autoRenewTime': auto_renew_time,
            'initial_data_reference': initial_data_reference,
            'data': data
        }

        return model.CreateInstanceResponse(self._send_request(http_methods.POST, 'instance',
                                                               params={"clientToken": uuid.uuid4()},
                                                               body=json.dumps(data, cls=model.JsonWrapper, indent=4),
                                                               config=config,
                                                               api_version=1))

    @required(instance_name=(str), source_instance_id=(str), zone_names=list, vpc_id=(str), is_direct_pay=bool,
              subnets=list, tags=list, billing=model.Billing)
    def create_read_instance(self, source_instance_id, cpu_count, memory_capacity, volume_capacity,
                             instance_name=None, vpc_id=None, subnets=None, tags=None, zone_names=None,
                             disk_io_type=None, is_direct_pay=None, billing=model.Billing(), config=None):
        """
        Create instance with specific config

        :param source_instance_id: Source instance count
        :type source_instance_id: string

        :param instance_name: Instance name
        :type  instance_name: string

        :param cpu_count:
        :type  cpu_count: int

        :param memory_capacity:
        :type  memory_capacity: int

        :param volume_capacity:
        :type  volume_capacity: int

        :param disk_io_type: normal_io; cloud_high; cloud_nor; cloud_enha
        :type  disk_io_type: string

        :param zone_names:
        :type  zone_names: list

        :param vpc_id:
        :type  vpc_id: string

        :param is_direct_pay:
        :type  is_direct_pay: bool

        :param subnets: list of model.SubnetMap
        :type  subnets: list

        :param tags:
        :type  tags: list

        :param billing: default billing is Prepay 1 month
        :type  billing: model.Billing

        :param config: None
        :type  config: BceClientConfiguration

        :return: Object
            {
                "instance_ids": ["rds-sgrw14145"]
            }

        :rtype: baidubce.bce_response.BceResponse
        """
        data = {
            'billing': billing.__dict__,
            'sourceInstanceId': source_instance_id,
            'instanceName': instance_name,
            'cpuCount': cpu_count,
            'memoryCapacity': memory_capacity,
            'volumeCapacity': volume_capacity,
            'zoneNames': zone_names,
            'vpcId': vpc_id,
            'diskIoType': disk_io_type,
            'isDirectPay': is_direct_pay,
            'subnets': subnets,
            'tags': tags
        }
        return model.CreateInstanceResponse(self._send_request(http_methods.POST, 'instance',
                                                               params={"clientToken": uuid.uuid4(), "readReplica": ""},
                                                               body=json.dumps(data, cls=model.JsonWrapper, indent=4),
                                                               config=config,
                                                               api_version=1))

    @required(instance_name=(str), source_instance_id=(str), node_amount=int, zone_names=list, vpc_id=(str),
              is_direct_pay=bool, subnets=list, tags=list, billing=model.Billing)
    def create_proxy_instance(self, source_instance_id, node_amount, instance_name=None, vpc_id=None, subnets=None,
                              tags=None, zone_names=None, is_direct_pay=None,
                              billing=model.Billing(), config=None):

        """
        Create instance with specific config

        :param source_instance_id: Source instance count
        :type source_instance_id: string

        :param instance_name: Instance name
        :type  instance_name: string

        :param node_amount:
        :type  node_amount: int

        :param zone_names:
        :type  zone_names: list

        :param vpc_id:
        :type  vpc_id: string

        :param is_direct_pay:
        :type  is_direct_pay: bool

        :param subnets: list of model.SubnetMap
        :type  subnets: list

        :param tags:
        :type  tags: list

        :param billing: default billing is Prepay 1 month
        :type  billing: model.Billing

        :param config: None
        :type  config: BceClientConfiguration

        :return: Object
            {
                "instance_ids": ["rds-sgrw14145"]
            }

        :rtype: baidubce.bce_response.BceResponse
        """
        data = {
            'billing': billing.__dict__,
            'sourceInstanceId': source_instance_id,
            'instanceName': instance_name,
            'nodeAmount': node_amount,
            'zoneNames': zone_names,
            'vpcId': vpc_id,
            'isDirectPay': is_direct_pay,
            'subnets': subnets,
            'tags': tags
        }
        return model.CreateInstanceResponse(self._send_request(http_methods.POST, 'instance',
                                                               params={"clientToken": uuid.uuid4(), "rdsproxy": ""},
                                                               body=json.dumps(data, cls=model.JsonWrapper, indent=4),
                                                               config=config,
                                                               api_version=1))

    @required(instance_id=(str))
    def get_instance_detail(self, instance_id, config=None):
        """
        Get instance detail
        :param instance_id: The ID of instance
        :type  instance_id: string or unicode

        :param config: None
        :type  config: BceClientConfiguration

        :return:
            {
                "instanceId": "rds-mut9rhom8p3m",
                "instanceName": "mysql56",
                "memoryCapacity": 0.25,
                "volumeCapacity": 5,
                "nodeAmount": 2,
                "usedStorage": 0.5672,
                "engine": "mysql",
                "engineVersion": "5.6",
                "characterSetName": "utf8mb4",
                "instanceStatus": "Available",
                "publicAccessStatus": "Closed",
                "instanceCreateTime": "2016-04-26T06:46:30Z",
                "instanceExpireTime": "2016-05-26T06:46:11Z",
                "endpoint": {
                    "address": "<address>",
                    "port": 3306,
                    "vnetIp": "<vnetIp>",
                    "inetIp": "<inetIp>"
                },
                "instanceType": "Master",
                "zoneNames": ["cn-bj-a"],
                "vpcId": "v-kj3nc8fs",
                "backupPolicy": {
                    "backupDays": "0,1,2,3,4,5,6",
                    "backupTime": "17:00:00Z",
                    "persistent": false,
                    "expireInDays": 0,
                    "freeSpace": 5
                },
                "topology": {
                    "rdsproxy": [],
                    "master": [
                        "rds-mut9rhog"
                    ],
                    "readReplica": [
                        "rds-m2s2du6j",
                        "rds-m4bkxb0i"
                    ]
                },
               "syncMode": "Async",
               "paymentTiming": "Prepaid"
            }

        """
        return model.GetInstanceResponse(self._send_request(http_methods.GET, function_name='instance', key=instance_id,
                                                            config=config, api_version=1))

    def list_instances(self, marker=None, max_keys=1000, config=None):
        """
        Get instances in current region
        :param marker: start position
        :param max_keys: max count per page
        :param config:
        :return:
        """
        params = {}
        if marker is not None:
            params[b'marker'] = marker
        if max_keys is not None:
            params[b'maxKeys'] = max_keys
        return model.ListInstanceResponse(self._send_request(http_methods.GET,
                                                             function_name='instance',
                                                             params=params,
                                                             config=config))

    @required(instance_id=(str), cpu_count=int, memory_capacity=int, volume_capacity=int, node_amount=int,
              is_direct_pay=bool, is_enhanced=bool, effective_time=(str))
    def resize_instance(self, instance_id, cpu_count=None, memory_capacity=None, volume_capacity=None,
                        node_amount=None, is_direct_pay=None, is_enhanced=None, effective_time=None,
                        disk_io_type=None, force_hot_upgrade=None, master_azone=None, backup_azone=None,
                        subnet_id=None, edge_subnet_id=None, config=None):
        """
        Create instance with specific config

       :param cpu_count:
        :type  cpu_count: int

        :param memory_capacity:
        :type  memory_capacity: int

        :param volume_capacity:
        :type  volume_capacity: int

        :param node_amount:
        :type  node_amount: int

        :param is_direct_pay:
        :type  is_direct_pay: bool

        :param effective_time:
        :type  effective_time: string

        :param disk_io_type: normal_io; cloud_high; cloud_nor; cloud_enha
        :type  disk_io_type: string



        :param force_hot_upgrade:
        :type  force_hot_upgrade: int

        :param master_azone:
        :type  master_azone: string

        :param subnet_id:
        :type  subnet_id: string

        :param backup_azone:
        :type  backup_azone: string

        :param edge_subnet_id:
        :type  edge_subnet_id: string

        :param config: None
        :type  config: BceClientConfiguration

        :return: Object
            {
                "instance_ids": ["rds-sgrw14145"]
            }

        :rtype: baidubce.bce_response.BceResponse
        """
        data = {
            'cpuCount': cpu_count,
            'memoryCapacity': memory_capacity,
            'volumeCapacity': volume_capacity,
            'nodeAmount': node_amount,
            'isDirectPay': is_direct_pay,
            'isEnhanced': is_enhanced,
            'effectiveTime': effective_time,
            'diskIoType': disk_io_type,
            'forceHotUpgrade': force_hot_upgrade,
            'masterAzone': master_azone,
            'backupAzone': backup_azone,
            'subnetId': subnet_id,
            'edgeSubnetId': edge_subnet_id

        }
        return model.CreateInstanceResponse(self._send_request(http_methods.PUT, 'instance', key=instance_id,
                                                               params={"resize": ""},
                                                               body=json.dumps(data), config=config))

    @required(instance_ids=(str))
    def delete_instance(self, instance_ids, config=None):
        """
        Delete instance
        :param instance_ids: The ID of instance
        :type  instance_ids: string or unicode

        :param config: None
        :type  config: BceClientConfiguration

        :return:
        """
        return self._send_request(http_method=http_methods.DELETE, function_name='instance',
                                  params={"instanceIds": instance_ids},
                                  config=config, api_version=1)

    def recycler_list(self, marker=None, max_keys=None, config=None):
        """
        Get instances recycler list
        :param marker: start position
        :param max_keys: max count per page
        :param config:
        :return:
        """
        params = {}
        if marker is not None:
            params[b'marker'] = marker
        if max_keys is not None:
            params[b'maxKeys'] = max_keys
        return model.ListInstanceResponse(self._send_request(http_methods.GET,
                                                             function_name='instance/recycler/list',
                                                             params=params,
                                                             config=config))

    @required(instance_ids=list)
    def recycler_recover(self, instance_ids, config=None):
        """
        Get instances recycler recover
        :param instance_ids: the ID of instance
        :param config:
        :return:
        """
        data = {
            'instanceIds': instance_ids
        }
        return self._send_request(http_method=http_methods.PUT, function_name='instance/recycler/recover',
                                  body=json.dumps(data),
                                  config=config, api_version=1)

    @required(instance_id=(str))
    def delete_recycler(self, instance_id, config=None):

        """
        Delete recycler
        :param instance_id: the ID of instance
        :param config:
        :return:
        """

        return self._send_request(http_method=http_methods.DELETE, function_name='instance/recycler',
                                  key=instance_id,
                                  config=config, api_version=1)

    @required(instance_ids=(str))
    def delete_recycler_batch(self, instance_ids, config=None):

        """
        Delete recycler batch
        :param instance_ids: the ID of instance
        :param config:
        :return:
        """

        return self._send_request(http_method=http_methods.DELETE, function_name='instance/recycler/batch',
                                  params={"instanceIds": instance_ids},
                                  config=config, api_version=1)

    @required(instance_id=(str))
    def reboot_instance(self, instance_id, config=None):

        """
        Reboot instance
        :param instance_id: the ID of instance
        :param config:
        :return:
        """

        return self._send_request(http_method=http_methods.PUT, function_name='instance',
                                  key=instance_id,
                                  params={"reboot": ""},
                                  config=config, api_version=1)

    @required(instance_id=(str), instance_name=(str))
    def rename_instance(self, instance_id, instance_name, config=None):
        """
        Rename instance
        :param instance_id: the ID of instance
        :param instance_name: name
        :param config:
        :return:
        """
        data = {
            'instanceName': instance_name
        }
        return self._send_request(http_method=http_methods.PUT, function_name='instance',
                                  key=instance_id,
                                  params={"rename": ""},
                                  body=json.dumps(data),
                                  config=config, api_version=1)

    @required(instance_id=(str), sync_mode=(str))
    def modify_sync_mode_instance(self, instance_id, sync_mode, config=None):
        """
        ModifySyncMode instance
        :param instance_id: the ID of instance
        :param sync_mode:
        :param config:
        :return:
        """
        data = {
            'syncMode': sync_mode
        }
        return self._send_request(http_method=http_methods.PUT, function_name='instance',
                                  key=instance_id,
                                  params={"modifySyncMode": ""},
                                  body=json.dumps(data),
                                  config=config, api_version=1)

    @required(instance_id=(str), sync_mode=(str))
    def modify_endpoint_instance(self, instance_id, address, config=None):
        """
        ModifyEndpoint instance
        :param instance_id: the ID of instance
        :param address:
        :param config:
        :return:
        """
        data = {
            'address': address
        }
        return self._send_request(http_method=http_methods.PUT, function_name='instance',
                                  key=instance_id,
                                  params={"modifyEndpoint": ""},
                                  body=json.dumps(data),
                                  config=config, api_version=1)

    @required(instance_id=(str), public_access=bool)
    def modify_public_access_instance(self, instance_id, public_access, config=None):
        """
        ModifyPublicAccess instance
        :param instance_id: the ID of instance
        :param public_access:
        :param config:
        :return:
        """
        data = {
            'publicAccess': public_access
        }
        return self._send_request(http_method=http_methods.PUT, function_name='instance',
                                  key=instance_id,
                                  params={"modifyPublicAccess": ""},
                                  body=json.dumps(data),
                                  config=config, api_version=1)

    @required(instance_ids=list, auto_renew_time_unit=(str), auto_renew_time=int)
    def auto_renew_instance(self, instance_ids=None, auto_renew_time_unit=None, auto_renew_time=None, config=None):
        """
        AutRenew instance
        :param instance_ids: the ID of instance
        :param auto_renew_time_unit:
        :param auto_renew_time:
        :param config:
        :return:
        """
        data = {
            'instanceIds': instance_ids,
            'autoRenewTimeUnit': auto_renew_time_unit,
            'autoRenewTime': auto_renew_time
        }
        return self._send_request(http_method=http_methods.PUT, function_name='instance',
                                  params={"autoRenew": ""},
                                  body=json.dumps(data),
                                  config=config, api_version=1)

    def zone(self, config=None):
        """
        Zone list
        :param config:
        :return:
        """
        return model.ListZoneResponse(self._send_request(http_method=http_methods.GET, function_name='zone',
                                                         config=config, api_version=1))

    def subnet(self, vpc_id=None, zone_name=None, config=None):
        """
        Subnet list
        :param config:
        :return:
        """
        return model.ListSubnetResponse(self._send_request(http_method=http_methods.GET, function_name='subnet',
                                                           params={"vpcId": vpc_id, "zoneName": zone_name},
                                                           config=config, api_version=1))

    @required(instance_id=(str))
    def start_instance(self, instance_id, config=None):
        """
        Start instance
        :param instance_id: the ID of instance
        :param config:
        :return:
        """

        return self._send_request(http_method=http_methods.PUT, function_name='instance',
                                  key=instance_id + '/start',
                                  config=config, api_version=1)

    @required(instance_id=(str))
    def suspend_instance(self, instance_id, config=None):

        """
        Suspend instance
        :param instance_id: the ID of instance
        :param config:
        :return:
        """

        return self._send_request(http_method=http_methods.PUT, function_name='instance',
                                  key=instance_id + '/suspend',
                                  config=config, api_version=1)

    def price_instance(self, duration, number, product_type, instance=model.Instance, config=None):
        """
        Price instance
        :param duration:
        :param number:
        :param product_type:
        :param duration:
        :param instance:
        :return:
        """
        data = {
            'instance': instance.__dict__,
            'duration': duration,
            'number': number,
            'productType': product_type
        }

        return model.PriceResponse(self._send_request(http_methods.POST, 'instance/price',
                                                      body=json.dumps(data, cls=model.JsonWrapper, indent=4),
                                                      config=config,
                                                      api_version=1))

    @required(order_id=(str))
    def order_status(self, order_id, config=None):

        """
        order status
        :param order_id: the ID of order
        :param config:
        :return:
        """

        return self._send_request(http_method=http_methods.GET, function_name='instance',
                                  key='/order/' + order_id,
                                  config=config, api_version=1)

    @required(duration=int, instance_ids=list)
    def renew_instance(self, duration, instance_ids, config=None):

        """
        renew instance
        :param duration:
        :param instance_ids:
        :param config:
        :return:
        """
        data = {
            "duration": duration,
            "instanceIds": instance_ids
        }

        return model.CreateInstanceResponse(self._send_request(http_method=http_methods.POST, function_name='instance',
                                                               key='/renew',
                                                               body=json.dumps(data),
                                                               config=config, api_version=1))

    @required(instance_id=(str), maintain_start_time=(str), maintain_duration=int)
    def maintaintime_instance(self, instance_id, maintain_start_time, maintain_duration, config=None):

        """
        maintaintime instance
        :param instance_id: the ID of instance
        :param maintain_start_time:
        :param maintain_duration:
        :param config:
        :return:
        """
        data = {
            "maintainDuration": maintain_duration,
            "maintainStartTime": maintain_start_time
        }

        return self._send_request(http_method=http_methods.PUT, function_name='instance',
                                  key=instance_id + '/maintaintime',
                                  body=json.dumps(data),
                                  config=config, api_version=1)

    def task_instance(self, page_size=None, page_no=None, end_time=None, instance_id=None, instance_name=None,
                      task_id=None, task_type=None, task_status=None, start_time=None, config=None):

        """
        task list
        :param instance_id: the ID of instance
        :param page_size:
        :param page_no:
        :param end_time:
        :param instance_name:
        :param task_id:
        :param task_type:
        :param task_status:
        :param start_time:
        :param config:
        :return:
        """
        data = {
            "pageSize": page_size,
            "pageNo": page_no,
            "endTime": end_time,
            "instanceId": instance_id,
            "instanceName": instance_name,
            "taskId": task_id,
            "taskType": task_type,
            "taskStatus": task_status,
            "startTime": start_time
        }

        return model.TaskResponse(self._send_request(http_method=http_methods.POST, function_name='instance',
                                                     key='/task',
                                                     body=json.dumps(data),
                                                     config=config, api_version=1))

    def force_change_instance(self, group_id, leader_id, force=None, max_behind=None, config=None):
        """
        force changeinstance
        :param leader_id:
        :param force:
        :param max_behind:
        :param config:
        :return:
        """
        data = {
            "leaderId": leader_id,
            "force": force,
            "maxBehind": max_behind
        }

        return model.ForceChangeResponse(self._send_request(http_method=http_methods.PUT, function_name='instance',
                                                            key=group_id + '/forceChange',
                                                            body=json.dumps(data),
                                                            config=config, api_version=1))

    def group_batch_join(self, follower_ids, name, leader_id, config=None):
        """
        group batch join
        :param follower_ids:
        :param name:
        :param leader_id:
        :param config:
        :return:
        """
        data = {
            "followerIds": follower_ids,
            "name": name,
            "leaderId": leader_id
        }

        return self._send_request(http_method=http_methods.POST, function_name='instance',
                                  key='/group/batchjoin',
                                  body=json.dumps(data),
                                  config=config, api_version=1)

    def create_group(self, name, leader_id, config=None):
        """
        group create
        :param name:
        :param leader_id:
        :param config:
        :return:
        """
        data = {
            "name": name,
            "leaderId": leader_id
        }

        return self._send_request(http_method=http_methods.POST, function_name='instance',
                                  key='/group',
                                  body=json.dumps(data),
                                  config=config, api_version=1)

    def list_group(self, config=None):
        """
        group list
        :param config:
        :return:
        """

        return model.GroupResponse(self._send_request(http_method=http_methods.GET, function_name='instance',
                                  key='/group', params={"manner": "page"},
                                  config=config, api_version=1))

    def detail_group(self, group_id, config=None):
        """
        group detail
        :param group_id:
        :param config:
        :return:
        """

        return model.GroupDetailResponse(self._send_request(http_method=http_methods.GET, function_name='instance',
                                                      key='/group/' + group_id,
                                                      config=config, api_version=1))

    def check_gtid_group(self, instance_id, config=None):
        """
        group detail
        :param instance_id:
        :param config:
        :return:
        """
        data = {
            "instanceId": instance_id
        }

        return model.GroupCheckGtidResponse(self._send_request(http_method=http_methods.POST, function_name='instance',
                                                               key='/group/checkGtid',
                                                               body=json.dumps(data),
                                                               config=config, api_version=1))


    @staticmethod
    def _get_path_v1(config, function_name=None, key=None):
        return utils.append_uri(rds.URL_PREFIX_V1, function_name, key)

    @staticmethod
    def _get_path_v2(config, function_name=None, key=None):
        return utils.append_uri(rds.URL_PREFIX_V2, function_name, key)

    @staticmethod
    def _bce_scs_sign(credentials, http_method, path, headers, params,
                      timestamp=0, expiration_in_seconds=1800,
                      headers_to_sign=None):

        headers_to_sign_list = [b"host",
                                b"content-md5",
                                b"content-length",
                                b"content-type"]

        if headers_to_sign is None or len(headers_to_sign) == 0:
            headers_to_sign = []
            for k in headers:
                k_lower = k.strip().lower()
                if k_lower.startswith(http_headers.BCE_PREFIX) or k_lower in headers_to_sign_list:
                    headers_to_sign.append(k_lower)
            headers_to_sign.sort()
        else:
            for k in headers:
                k_lower = k.strip().lower()
                if k_lower.startswith(http_headers.BCE_PREFIX):
                    headers_to_sign.append(k_lower)
            headers_to_sign.sort()

        return bce_v1_signer.sign(credentials,
                                  http_method,
                                  path,
                                  headers,
                                  params,
                                  timestamp,
                                  expiration_in_seconds,
                                  headers_to_sign)

    def _merge_config(self, config):
        if config is None:
            return self.config
        else:
            self._check_config_type(config)
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    def _send_request(self, http_method, function_name=None, key=None, body=None, headers=None, params=None,
                      config=None, body_parser=None, api_version=1):
        if params is None:
            params = {"clientToken": uuid.uuid4()}
        config = self._merge_config(config)
        path = {
            1: RdsClient._get_path_v1,
            2: RdsClient._get_path_v2,
        }[api_version](config, function_name, key)

        if body_parser is None:
            body_parser = _parse_result

        if headers is None:
            headers = {b'Accept': b'*/*', b'Content-Type': b'application/json;charset=utf-8'}

        return bce_http_client.send_request(config, RdsClient._bce_scs_sign, [body_parser], http_method, path, body,
                                            headers, params)
