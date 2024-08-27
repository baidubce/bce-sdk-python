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
This module provides a client class for RDS.
"""

from __future__ import unicode_literals

import copy
import json
import logging
import random
import string
import uuid

from baidubce import bce_base_client
from baidubce.auth import bce_v1_signer
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce.http import http_methods
from baidubce.services.rds import rds_model
from baidubce.utils import aes128_encrypt_16char_key
from baidubce.utils import required
from baidubce import compat

_logger = logging.getLogger(__name__)

FETCH_MODE_SYNC = b"sync"
FETCH_MODE_ASYNC = b"async"

ENCRYPTION_ALGORITHM = "AES256"

default_billing_to_purchase_created = rds_model.Billing('Postpaid')
default_billing_to_purchase_reserved = rds_model.Billing()


class RDSClient(bce_base_client.BceBaseClient):
    """
    Rds base sdk client
    """

    prefix = b'/v1'
    prefix_v2 = b'/v2'

    def __init__(self, config=None):
        bce_base_client.BceBaseClient.__init__(self, config)

    def _merge_config(self, config=None):
        if config is None:
            return self.config
        else:
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    # 1. instance manager
    def _send_request(self, http_method, path,
                      body=None, headers=None, params=None,
                      config=None, body_parser=None, prefix=None):
        config = self._merge_config(config)
        if body_parser is None:
            body_parser = handler.parse_json
        if prefix is None:
            prefix = RDSClient.prefix

        return bce_http_client.send_request(
            config, bce_v1_signer.sign, [handler.parse_error, body_parser],
            http_method, prefix + path, body, headers, params)

    @required(engine=(str), engine_version=(str), category=(str),
              cpuCount=int, memory_capacity=int, volume_capacity=int, disk_io_type=(str),
              purchase_count=int, zone_names=list, vpc_id=(str),
              subnets=list)
    def create_instance(self, engine, engine_version, category, cpu_count, memory_capacity, volume_capacity,
                        disk_io_type, is_direct_pay=None, initial_data_reference=None, bgw_group_id=None,
                        bgw_group_exclusive=None, character_set_name=None, lower_case_table_names=None,
                        parameter_template_id=None, data=None, instance_name=None, vpc_id=None, subnets=None,
                        tags=None, purchase_count=1, zone_names=None, auto_renew_time_unit='month',
                        auto_renew_time=None, billing=None, config=None, client_token=None):
        """
         Create instance with specific config

        :param purchase_count:
            Instance count
        :type purchase_count: int

        :param instance_name:
            Instance name
        :type  instance_name: string

        :param engine:
            database engine
        :type  engine: string

        :param engine_version:
            database version
        :type  engine_version: string or unicode

        :param category: Singleton or Standard
        :type  category: string

        :param cpu_count: Number of CPUs
        :type  cpu_count: int

        :param memory_capacity:
            memory size，unit:GB
        :type  memory_capacity: int

        :param volume_capacity:
            disk size，unit:GB
        :type  volume_capacity: int

        :param disk_io_type:
            normal_io; cloud_high; cloud_nor; cloud_enha
        :type  disk_io_type: string

        :param zone_names:
            Subnet Name Collection
        :type  zone_names: list

        :param vpc_id:
            the vpc short id
        :type  vpc_id: string

        :param is_direct_pay:
            Whether to make direct payment, default to false.
            Variable configuration orders set to direct payment will
            be directly deducted without the need for payment logic
        :type  is_direct_pay: bool

        :param initial_data_reference:
        :type  initial_data_reference: rds_instance_model.InitialDataReference

        :param subnets:
             list of model.SubnetMap
        :type  subnets: list

        :param tags:
             tag object of collection
        :type  tags: list

        :param bgw_group_id:
             If bgwGroupExclusive is true,
             if a dedicated cluster ID is specified when creating an instance,
             BLB will be assigned to the specified dedicated cluster.
             If not passed, it will be assigned by default
        :type  bgw_group_id: string

        :param bgw_group_exclusive:
             Load balancing cluster attributes,
            true indicates specifying a dedicated cluster,
            false indicates using a shared cluster
        :type  bgw_group_exclusive: bool

        :param character_set_name:
            the Specify the instance character set,
            which includes options such as "utf8mb4",
            "latin1", "gbk", and "utf8". The default is "utf8"
            (currently only supports MySQL primary instances)
        :type  character_set_name: string

        :param lower_case_table_names:
            Is the table name case sensitive. The default is 0,
            indicating case sensitivity and case sensitivity;
            Pass 1 to indicate case insensitivity
        :type  lower_case_table_names: int

        :param parameter_template_id:
            parameter template id
        :type  parameter_template_id: string

        :param auto_renew_time_unit:
            Renew monthly or yearly,value in ['month','year]
        :type  auto_renew_time_unit: str

        :param auto_renew_time:
            If billing is Prepay, the automatic renewal time is 1-9
            when auto_renew_time_unit is 'month' and 1-3 when auto_renew_time_unit is 'year'
        :type  auto_renew_time: int

        :param initial_data_reference:
        :type  initial_data_reference: instance_model.InitialDataReference

        :param data:
            Parameter Object of lit
        :type  data: list

        :param billing: default billing is Prepay 1 month
        :type  billing: rds_instance_model.Billing

        :param config: None
        :type  config: BceClientConfiguration

        :return: Object
            {
                "instance_ids": ["rds-sgrw14145"]
            }

        :rtype: baidubce.bce_response.BceResponse
        """

        if billing is None:
            billing = rds_model.Billing()

        if zone_names is None:
            zone_names = []

        if subnets is None:
            subnets = []

        if tags is None:
            tags = []

        if data is None:
            data = []

        body = {
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
            'initialDataReference': initial_data_reference,
            'data': data
        }
        path = b'/instance'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        headers = {b'Content-Type': b'application/json'}
        return self._send_request(http_methods.POST, path, json.dumps(body),
                                  headers=headers, params=params, config=config)

    @required(instance_name=(str), source_instance_id=(str), zone_names=list, vpc_id=(str),
              is_direct_pay=bool, subnets=list, tags=list, billing=rds_model.Billing)
    def create_read_instance(self, source_instance_id, cpu_count, memory_capacity, volume_capacity,
                             instance_name=None, vpc_id=None, subnets=None, tags=None, zone_names=None,
                             disk_io_type=None, is_direct_pay=None, billing=None,
                             config=None):
        """
         Create instance with specific config

        :param source_instance_id:
           The Source instance count
        :type source_instance_id: string

        :param instance_name:
           The Instance name
        :type  instance_name: string

        :param cpu_count: cpu core number
        :type  cpu_count: int

        :param memory_capacity:
            The memory size ,unit:GB
        :type  memory_capacity: int

        :param volume_capacity:
            The disk size，unit:GB
        :type  volume_capacity: int

        :param disk_io_type:
            normal_io; cloud_high; cloud_nor; cloud_enha
        :type  disk_io_type: string

        :param zone_names:
            zone name of arraylist
        :type  zone_names: list

        :param vpc_id:
            VPC short ID
        :type  vpc_id: string

        :param is_direct_pay:

        :type  is_direct_pay: bool

        :param subnets:
            list of model.SubnetMap
        :type  subnets: list

        :param tags:
        :type  tags: list

        :param billing: default billing is Prepay 1 month
        :type  billing: rds_instance_model.Billing

        :param config: None
        :type  config: BceClientConfiguration

        :return: Object
            {
                "instance_ids": ["rds-sgrw14145"]
            }

        :rtype: baidubce.bce_response.BceResponse
        """
        if billing is None:
            billing = rds_model.Billing()

        if zone_names is None:
            zone_names = []

        if subnets is None:
            subnets = []

        if tags is None:
            tags = []

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
        path = b'/instance'
        headers = {b'Content-Type': b'application/json'}
        return self._send_request(http_methods.POST, path,
                               params={"clientToken": uuid.uuid4(), "readReplica": ""},
                               headers=headers,
                               body=json.dumps(data, cls=rds_model.JsonWrapper, indent=4),
                               config=config)

    @required(instance_name=(str), source_instance_id=(str), node_amount=int, zone_names=list,
              vpc_id=(str), is_direct_pay=bool, subnets=list, tags=list, billing=rds_model.Billing)
    def create_proxy_instance(self, source_instance_id, node_amount, instance_name=None,
                              vpc_id=None, subnets=None, tags=None, zone_names=None,
                              is_direct_pay=None, billing=None, config=None):
        """
         Create instance with specific config

        :param source_instance_id:
            Source instance count
        :type source_instance_id: string

        :param instance_name:
            Instance name
        :type  instance_name: string

        :param node_amount:
             number of node
        :type  node_amount: int

        :param zone_names:
          zone name of arraylist
        :type  zone_names: list

        :param vpc_id:
        :type  vpc_id: string

        :param is_direct_pay:
             Whether to make direct payment, default to false.
            Variable configuration orders set to direct payment will
            be directly deducted without the need for payment logic
        :type  is_direct_pay: bool

        :param subnets: list of model.SubnetMap
        :type  subnets: list

        :param tags:
            tag object of arraylist
        :type  tags: list

        :param billing: default billing is Prepay 1 month
        :type  billing: instance_model.Billing

        :param config: None
        :type  config: BceClientConfiguration

        :return: Object
            {
                "instance_ids": ["rds-sgrw14145"]
            }

        :rtype: baidubce.bce_response.BceResponse
        """

        if billing is None:
            billing = rds_model.Billing()

        if zone_names is None:
            zone_names = []

        if subnets is None:
            subnets = []

        if tags is None:
            tags = []

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
        headers = {b'Content-Type': b'application/json'}
        return self._send_request(http_methods.POST,
                               b'/instance',
                               params={"clientToken": uuid.uuid4(), "rdsproxy": ""}, headers=headers,
                               body=json.dumps(data, cls=rds_model.JsonWrapper, indent=4),
                               config=config)

    @required(instance_id=(str))
    def get_instance_detail(self, instance_id, config=None):
        """
         Get instance detail

        :param instance_id:
            The ID of instance
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
        template = b'/instance/{instance_id}'
        # 注意：由于模板是bytes类型，你需要将变量也转换为bytes类型以匹配
        formatted_url = template.decode().format(instance_id=instance_id).encode()
        return self._send_request(http_methods.GET,
                                  formatted_url,
                                  params=None,
                                  body=None,
                                  config=config)

    def list_instances(self, marker=None, max_keys=1000, config=None):
        """
         Get instances in current region

        :param marker:
            To search for the instance id, fill in -1 from the first page
        :type marker: str

        :param max_keys:
            max count per page,deafult is 1000
         :type marker: int

        :param config:
        :return:
        """
        params = {}
        if marker is not None:
            params[b'marker'] = marker
        if max_keys is not None:
            params[b'maxKeys'] = max_keys
        return self._send_request(http_methods.GET,
                               path=b'/instance',
                               params=params,
                               config=config)

    @required(instance_id=(str), cpu_count=int, memory_capacity=int, volume_capacity=int, node_amount=int,
              is_direct_pay=bool, is_enhanced=bool, effective_time=(str))
    def resize_instance(self, instance_id, cpu_count=None, memory_capacity=None, volume_capacity=None,
                        node_amount=None, is_direct_pay=None, is_enhanced=None, effective_time=None,
                        disk_io_type=None, force_hot_upgrade=None, master_azone=None, backup_azone=None,
                        subnet_id=None, edge_subnet_id=None, config=None):
        """
         Create instance with specific config

        :param cpu_count:
            CPU cores number,Unit:Pieces
        :type  cpu_count: int

        :param memory_capacity:
            memory size,Unit:GB
        :type  memory_capacity: int

        :param volume_capacity:
            disk size，Unit:GB
        :type  volume_capacity: int

        :param node_amount:
            number of nodes
        :type  node_amount: int

        :param is_direct_pay:
            Whether to make direct payment, default to false.
            Variable configuration orders set to direct payment will
            be directly deducted without the need for payment logic
        :type  is_direct_pay: bool

        :param effective_time:
            The operation execution method has two values: timewindow
            and immediate. Among them, timewindow represents execution
            within the time window, and immediate represents immediate
            execution. The default is immediate. The default time window
            for the instance is from 05:00 to 06:00. Please refer to the
            instance details for details
        :type  effective_time: string

        :param disk_io_type:
            normal_io; cloud_high; cloud_nor; cloud_enha
        :type  disk_io_type: string


        :param force_hot_upgrade:
        :type  force_hot_upgrade: int

        :param master_azone:
            When changing the configuration, it is necessary to change
            the available area of the main database. This parameter
            needs to be passed a value, such as cn-bj-a.
            Do not transfer default to the current main database az
        :type  master_azone: string

        :param subnet_id:
            Subnet ID, default to empty
        :type  subnet_id: string

        :param backup_azone:
            When changing the configuration, it is necessary to change
            the available area of the backup database. This parameter
            needs to be passed a value, such as cn-bj-a. Do not transfer,
            default to retrieve the current backup database az
        :type  backup_azone: string

        :param edge_subnet_id:
            Parameter Edge Subnet ID
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
        path = b'/instance/{instance_id}'
        formatted_url = path.decode().format(instance_id=instance_id).encode()
        headers = {b'Content-Type': b'application/json'}
        return rds_model.CreateInstanceResponse(
            self._send_request(http_methods.PUT,
                               path=formatted_url,
                               body=json.dumps(data),
                               headers=headers,
                               params={"resize": ""},
                               config=config))

    @required(instance_ids=(str))
    def delete_instance(self, instance_ids, config=None):
        """
         Delete instance

        :param instance_ids:
            The ID of instance
        :type  instance_ids: string or unicode

        :param config:
            None
        :type  config: BceClientConfiguration

        :return:
        """
        path = b'/instance'
        return self._send_request(http_method=http_methods.DELETE,
                                  path=path,
                                  params={"instanceIds": instance_ids},
                                  config=config)

    @required(instance_id=(str))
    def reboot_instance(self, instance_id, config=None):
        """
         Reboot instance

        :param instance_id:
            the ID of instance
        :type  instance_id: string

        :param config:
        :type  config: BceClientConfiguration

        :return:
        """
        template = b'/instance/{instance_id}'
        # 注意：由于模板是bytes类型，你需要将变量也转换为bytes类型以匹配
        formatted_url = template.decode().format(instance_id=instance_id).encode()
        headers = {b'Content-Type': b'application/json'}
        return self._send_request(http_method=http_methods.PUT,
                                  path=formatted_url,
                                  headers=headers,
                                  params={"reboot": ""},
                                  config=config)

    @required(instance_id=(str), instance_name=(str))
    def rename_instance(self, instance_id, instance_name, config=None):
        """
         Rename instance

        :param instance_id:
            the ID of instance
        :type  instance_id: str

        :param instance_name:
            name
        :type  instance_name: str

        :param config:
        :return:

        """
        data = {
            'instanceName': instance_name
        }
        template = b'/instance/{instance_id}'
        # 注意：由于模板是bytes类型，你需要将变量也转换为bytes类型以匹配
        formatted_url = template.decode().format(instance_id=instance_id).encode()
        headers = {b'Content-Type': b'application/json'}
        return self._send_request(http_method=http_methods.PUT,
                                  path=formatted_url,
                                  params={"rename": ""},
                                  headers=headers,
                                  body=json.dumps(data),
                                  config=config)

    @required(instance_id=(str), sync_mode=(str))
    def modify_sync_mode_instance(self, instance_id, sync_mode, config=None):
        """
         ModifySyncMode instance

        :param instance_id:
            the ID of instance
        :type  instance_id: str

        :param sync_mode:
            Async/Semi_sync
        :type  sync_mode: str

        :param config:
        :return:

        """
        data = {
            'syncMode': sync_mode
        }
        template = b'/instance/{instance_id}'
        # 注意：由于模板是bytes类型，你需要将变量也转换为bytes类型以匹配
        formatted_url = template.decode().format(instance_id=instance_id).encode()
        headers = {b'Content-Type': b'application/json'}
        return self._send_request(http_method=http_methods.PUT,
                                  path=formatted_url,
                                  params={"modifySyncMode": ""},
                                  headers=headers,
                                  body=json.dumps(data),
                                  config=config)

    @required(instance_id=(str), sync_mode=(str))
    def modify_endpoint_instance(self, instance_id, address, config=None):
        """
         ModifyEndpoint instance

        :param instance_id:
            the ID of instance
        :type  instance_id: string

        :param address:
            Fill in the domain name
        :type  address: string

        :param config:
        :type  config: BceClientConfiguration

        :return:
        """
        data = {
            'address': address
        }
        template = b'/instance/{instance_id}'
        # 注意：由于模板是bytes类型，你需要将变量也转换为bytes类型以匹配
        formatted_url = template.decode().format(instance_id=instance_id).encode()
        headers = {b'Content-Type': b'application/json'}
        return self._send_request(http_method=http_methods.PUT,
                                  path=formatted_url,
                                  params={"modifyEndpoint": ""},
                                  headers=headers,
                                  body=json.dumps(data),
                                  config=config)

    @required(instance_id=(str), public_access=bool)
    def modify_public_access_instance(self, instance_id, public_access, config=None):
        """
         ModifyPublicAccess instance

        :param instance_id:
            the ID of instance
        :type  instance_id: string

        :param public_access:
            ture/false
        :type  public_access: bool

        :param config:
        :type  config: BceClientConfiguration

        :return:
        """
        data = {
            'publicAccess': public_access
        }
        template = b'/instance/{instance_id}'
        # 注意：由于模板是bytes类型，你需要将变量也转换为bytes类型以匹配
        formatted_url = template.decode().format(instance_id=instance_id).encode()
        headers = {b'Content-Type': b'application/json'}
        return self._send_request(http_method=http_methods.PUT,
                                  path=formatted_url,
                                  params={"modifyPublicAccess": ""},
                                  headers=headers,
                                  body=json.dumps(data),
                                  config=config)

    @required(instance_ids=list, auto_renew_time_unit=(str), auto_renew_time=int)
    def auto_renew_instance(self, instance_ids=None, auto_renew_time_unit=None, auto_renew_time=None, config=None):
        """
         AutoRenew instance

        :param instance_ids:
            the ID of instance
        :type  instance_ids: list

        :param auto_renew_time_unit:
            Renewal period, in months
        :type  auto_renew_time_unit: str

        :param auto_renew_time:
            Renewal duration
        :type  auto_renew_time: int

        :param config:
        :return:
        """

        if instance_ids is None:
            instance_ids = []

        data = {
            'instanceIds': instance_ids,
            'autoRenewTimeUnit': auto_renew_time_unit,
            'autoRenewTime': auto_renew_time
        }
        headers = {b'Content-Type': b'application/json'}
        return self._send_request(http_method=http_methods.PUT,
                                  path=b'/instance',
                                  params={"autoRenew": ""},
                                  headers=headers,
                                  body=json.dumps(data),
                                  config=config)

    def zone(self, config=None):
        """
         Get zone list

        :param config:
        :type  config: BceClientConfiguration

        :return:
        """
        return self._send_request(
                http_method=http_methods.GET,
                path=b'/zone',
                config=config)

    def subnet(self, vpc_id=None, zone_name=None, config=None):
        """
         get Subnet list

        :param config:
        :type  config: BceClientConfiguration

        :return:
        """
        return self._send_request(http_method=http_methods.GET,
                               path=b'/subnet',
                               params={"vpcId": vpc_id, "zoneName": zone_name},
                               config=config)

    def price_instance(self, duration, number, product_type, instance=None, config=None):
        """
         Gets the specified instance price

        :param duration:
            The purchase duration does not need to be set  when the payment
            method is post-payment, but must be set when pre-payment.
            The default time unit is month.
        :type  duration: int

        :param number:
            Number of purchases. The default value is 1.
        :type  number: int

        :param product_type:
            prepay/postpay
        :type  product_type: string

        :param instance: Inquiry parameter object
        :type  instance: rds_instance_model.Instance

        :param config:
        :type  config: BceClientConfiguration

        :return:
        """
        data = {
            'instance': instance.__dict__,
            'duration': duration,
            'number': number,
            'productType': product_type
        }
        headers = {b'Content-Type': b'application/json'}
        return self._send_request(http_methods.POST,
                               path=b'/instance/price',
                               headers=headers,
                               body=json.dumps(data, cls=rds_model.JsonWrapper, indent=4),
                               config=config)

    @required(order_id=(str))
    def order_status(self, order_id, config=None):
        """
         Get order status

        :param order_id:
            the ID of order
        :type  order_id: string

        :param config:
        :type  config: BceClientConfiguration

        :return:
        """
        template = b'/instance/order/{order_id}'
        # 注意：由于模板是bytes类型，你需要将变量也转换为bytes类型以匹配
        formatted_url = template.decode().format(order_id=order_id).encode()
        return self._send_request(http_method=http_methods.GET,
                                  path=formatted_url,
                                  config=config)

    @required(duration=int, instance_ids=list)
    def renew_instance(self, duration, instance_ids, config=None):
        """
         Used to renew existing prepaid instances.
         If the prepaid instance is in the recycle bin,
         it will be restored from the recycle bin after renewal.

        :param duration:
            Renewal period, unit is month
        :type  duration: int

        :param instance_ids:
            An instance array of renewal instances
        :type  instance_ids: list of string

        :param config:
        :return:
        """
        data = {
            "duration": duration,
            "instanceIds": instance_ids
        }
        headers = {b'Content-Type': b'application/json'}
        return self._send_request(http_method=http_methods.POST,
                               path=b'/instance/renew',
                               headers=headers,
                               body=json.dumps(data),
                               config=config)

    @required(instance_id=(str), maintain_start_time=(str), maintain_duration=int)
    def maintaintime_instance(self, instance_id, maintain_start_time, maintain_duration, config=None):
        """
         Update the time window of the instance.
         The default time window of the instance is 05:00 to 06:00

        :param instance_id:
            The ID of instance
        :type  instance_id: string

        :param maintain_start_time:
            Start time of the instance maintenance time window,
            local time, for example, 17:00:00
        :type  maintain_start_time: string

        :param maintain_duration:
            The duration of the instance maintenance time window,
            expressed in hours, for example,
            Each hour is a time range，The start time and duration cannot span one day
        :type  maintain_duration: int

        :param config:
        :type  config: BceClientConfiguration

        :return:
        """
        data = {
            "maintainDuration": maintain_duration,
            "maintainStartTime": maintain_start_time
        }
        template = b'/instance/{instance_id}/maintaintime'
        # 注意：由于模板是bytes类型，你需要将变量也转换为bytes类型以匹配
        formatted_url = template.decode().format(instance_id=instance_id).encode()
        headers={b'Content-Type': b'application/json'}
        return self._send_request(http_method=http_methods.PUT,
                                  path=formatted_url,
                                  headers=headers,
                                  body=json.dumps(data),
                                  config=config)
    # 2. database manager
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
        path = b'/instance/{instance_id}/databases'
        # 注意：由于模板是bytes类型，你需要将变量也转换为bytes类型以匹配
        formatted_url = path.decode().format(instance_id=instance_id).encode()
        headers = {b'Content-Type': b'application/json'}
        return self._send_request(http_method=http_methods.POST,
                                  path=formatted_url,
                                  headers=headers,
                                  body=json.dumps(data),
                                  config=config)

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
        path = b'/instance/{instance_id}/databases'
        # 注意：由于模板是bytes类型，你需要将变量也转换为bytes类型以匹配
        formatted_url = path.decode().format(instance_id=instance_id).encode()
        return self._send_request(http_method=http_methods.GET,
                                  path=formatted_url,
                                  config=config)

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
        headers = {b'Content-Type': b'application/json'}
        data = {"remark": remark}
        path = b'/instance/{instance_id}/databases/{db_name}/remark'
        formatted_url = path.decode().format(instance_id=instance_id, db_name=db_name).encode()
        return self._send_request(http_method=http_methods.PUT,
                                  path=formatted_url,
                                  headers=headers,
                                  body=json.dumps(data),
                                  config=config)

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
        headers = {b'Content-Type': b'application/json'}
        path = b'/instance/{instance_id}/port'
        formatted_url = path.decode().format(instance_id=instance_id).encode()
        return self._send_request(http_method=http_methods.PUT,
                                  path=formatted_url,
                                  body=json.dumps(data),
                                  headers=headers,
                                  config=config)

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
        path=b'/instance/{instance_id}/databases/{db_name}'
        # 注意：由于模板是bytes类型，你需要将变量也转换为bytes类型以匹配
        formatted_url = path.decode().format(instance_id=instance_id, db_name=db_name).encode()
        return self._send_request(http_method=http_methods.DELETE,
                                  path=formatted_url,
                                  config=config)

    # 3. backup manager
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
        path = b'/instance/{instanceId}/backup/{backupId}'
        formatted_url = path.decode().format(instanceId=instance_id, backupId=backup_id).encode()
        return self._send_request(http_method=http_methods.GET,
                               path=formatted_url,
                               body=None,
                               config=config)

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
        path = b'/instance/{instanceId}/backup'
        formatted_url = path.decode().format(instanceId=instance_id).encode()
        return self._send_request(http_method=http_methods.GET,
                               path=formatted_url,
                               params=params,
                               config=config)

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
        path = b'/instance/{instanceId}'
        formatted_url = path.decode().format(instanceId=instance_id).encode()
        data = {
            "backupDays": backup_days,
            "backupTime": backup_time,
            "persistent": persistent
        }

        if expire_in_days is not None:
            data['expireInDays'] = int(expire_in_days)
        headers = {b'Content-Type': b'application/json'}
        return self._send_request(http_method=http_methods.PUT,
                                  path=formatted_url,
                                  headers = headers,
                                  params={"modifyBackupPolicy": ""},
                                  body=json.dumps(data),
                                  config=config)

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
        path = b'/instance/{instanceId}/backup'
        formatted_url = path.decode().format(instanceId=instance_id).encode()
        headers = {b'Content-Type': b'application/json'}
        return self._send_request(http_method=http_methods.POST,
                                  path=formatted_url,
                                  headers=headers,
                                  body=json.dumps(data),
                                  config=config)

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
        path = b'/instance/{instanceId}/backup/{snapshotId}'
        formatted_url = path.decode().format(instanceId=instance_id, snapshotId=snapshot_id).encode()
        return self._send_request(http_method=http_methods.DELETE,
                                  path=formatted_url,
                                  config=config)

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
        path = b'/instance/{instanceId}/binlogs/{datetime}'
        formatted_url = path.decode().format(instanceId=instance_id, datetime=date_time).encode()
        return self._send_request(http_method=http_methods.GET,
                               path=formatted_url,
                               config=config)

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
        path = b'/instance/{instance_id}/binlogs/{binlog_id}/{downloadValidTimeInSec}'
        formatted_url = path.decode().format(instance_id=instance_id, binlog_id=binlog_id,
                                             downloadValidTimeInSec=download_valid_time_in_sec).encode()
        return self._send_request(http_method=http_methods.GET,
                                path=formatted_url, config=config)

    # 4. hot instance group manager
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
        path = b'/instance/group/{groupId}/forceChange'
        formatted_url = path.decode().format(groupId=group_id).encode()
        headers = {b'Content-Type': b'application/json'}
        return self._send_request(http_method=http_methods.PUT,
                               path=formatted_url,
                               body=json.dumps(data),
                               headers=headers,
                               config=config)

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
        headers = {b'Content-Type': b'application/json'}
        return self._send_request(http_method=http_methods.POST,
                                  path=b'/instance/group/batchjoin',
                                  headers=headers,
                                  body=json.dumps(data),
                                  config=config)

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
        headers = {b'Content-Type': b'application/json'}
        return self._send_request(http_method=http_methods.POST,
                                  path=b'/instance/group',
                                  headers=headers,
                                  body=json.dumps(data),
                                  config=config)

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

        params = {b"manner": b"page"}

        if order is not None:
            params[b"order"] = order
        if order_by is not None:
            params[b"orderBy"] = order_by
        if page_no is not None:
            params[b"pageNo"] = page_no
        if page_size is not None:
            params[b"pageSize"] = page_size
        if filter_map_str is not None:
            params[b"filterMapStr"] = filter_map_str
        if days_to_expiration is not None:
            params[b"daysToExpiration"] = days_to_expiration

        return self._send_request(http_method=http_methods.GET,
                               path=b'/instance/group',
                               params=params, config=config)

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
        path = b'/instance/group/{groupId}'
        formatted_url = path.decode().format(groupId=group_id).encode()
        return self._send_request(http_method=http_methods.GET,
                               path=formatted_url,
                               config=config)

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
        headers = {b'Content-Type': b'application/json'}
        return self._send_request(http_method=http_methods.POST,
                               path=b'/instance/group/checkGtid',
                               headers=headers,
                               body=json.dumps(data),
                               config=config)

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
        headers = {b'Content-Type': b'application/json'}
        return self._send_request(http_method=http_methods.POST,
                               path=b'/instance/group/checkPing',
                               headers=headers,
                               body=json.dumps(data),
                               config=config)

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
        headers = {b'Content-Type': b'application/json'}
        return self._send_request(http_method=http_methods.POST,
                               path=b'/instance/group/checkData',
                               headers=headers,
                               body=json.dumps(data),
                               config=config)

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
        path=b'/instance/group/{groupId}/instance'
        formatted_url = path.decode().format(groupId=group_id).encode()
        headers = {b'Content-Type': b'application/json'}
        return self._send_request(http_method=http_methods.POST,
                                  path=formatted_url,
                                  body=json.dumps(data),
                                  headers=headers,
                                  config=config)

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
        path = b'/instance/group/{groupId}/name'
        formatted_url = path.decode().format(groupId=group_id).encode()
        headers = {b'Content-Type': b'application/json'}
        return self._send_request(http_method=http_methods.POST,
                                  path=formatted_url,
                                  body=json.dumps(data),
                                  headers=headers,
                                  config=config)

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
        path=b'/instance/group/{groupId}'
        formatted_url = path.decode().format(groupId=group_id).encode()
        return self._send_request(http_method=http_methods.DELETE,
                                  path=formatted_url,
                                  config=config)

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
        path=b'/instance/group/{groupId}/instance'
        formatted_url = path.decode().format(groupId=group_id).encode()
        headers = {b'Content-Type': b'application/json'}
        return self._send_request(http_method=http_methods.PUT,
                                  path=formatted_url,
                                  body=json.dumps(data),
                                  headers=headers,
                                  config=config)

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
        path=b'/instance/group/{groupId}/instance/{instanceId}'
        formatted_url = path.decode().format(groupId=group_id, instanceId=instance_id).encode()
        return self._send_request(http_method=http_methods.DELETE,
                                  path=formatted_url,
                                  config=config)

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
        headers = {b'Content-Type': b'application/json'}
        return self._send_request(http_method=http_methods.POST,
                                  path=b'/instance/group/checkVersion',
                                  headers=headers,
                                  body=json.dumps(data),
                                  config=config)

    # 5. log manager
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
        path=b'/instance/{instanceId}/slowlogs/details'
        formatted_url = path.decode().format(instanceId=instance_id).encode()
        headers = {b'Content-Type': b'application/json'}
        return self._send_request(http_method=http_methods.POST,
                               path=formatted_url,
                               headers=headers,
                               body=json.dumps(data),
                               config=config)

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
        path=b'/instance/{instanceId}/errorlogs/details'
        formatted_url = path.decode().format(instanceId=instance_id).encode()
        headers = {b'Content-Type': b'application/json'}
        return self._send_request(http_method=http_methods.POST,
                               path=formatted_url,
                               body=json.dumps(data),
                               headers=headers,
                               config=config)

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
        path = b'/instance/{instanceId}/slowlogs/download_url/{logId}/{downloadValidTimeInSec}'
        formatted_url = path.decode().format(instanceId=instance_id, logId=log_id,
                                             downloadValidTimeInSec=download_valid_time_in_sec).encode()
        return self._send_request(http_method=http_methods.GET,
                               path=formatted_url,
                               config=config)

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
        path=b'/instance/{instanceId}/errorlogs/download_url/{logId}/{downloadValidTimeInSec}'
        formatted_url = path.decode().format(instanceId=instance_id, logId=log_id,
                                             downloadValidTimeInSec=download_valid_time_in_sec).encode()
        return self._send_request(http_method=http_methods.GET,
                               path=formatted_url,
                               config=config)

    # 6.recycle manager
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
        return self._send_request(http_methods.GET,
                               path=b'/instance/recycler/list',
                               params=params,
                               config=config)

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
        headers={b'Content-Type': b'application/json'}
        return self._send_request(http_method=http_methods.PUT,
                                  path=b'/instance/recycler/recover',
                                  body=json.dumps(data),
                                  headers=headers,
                                  config=config)

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
        path=b'/instance/recycler/{instanceId}'
        formatted_url = path.decode().format(instanceId=instance_id).encode()
        return self._send_request(http_method=http_methods.DELETE,
                                  path=formatted_url,
                                  config=config)

    # 7.task manager
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
        headers = {b'Content-Type': b'application/json'}
        return self._send_request(http_method=http_methods.POST,
                               path=b'/instance/task',
                               headers=headers,
                               body=json.dumps(data),
                               config=config)

    # 8.param manager
    @required(instance_id=str)
    def parameter_list(self, instance_id, keyword=None, config=None):
        """
         Gets a list of parameters for the specified instance

        :param instance_id:
            the specified instance id
        :type instance_id: str

        :param keyword:
            the keyword of parameter
        :type keyword: str or None

        :param config: config
        :type config: baidubce.BceClientConfiguration

        :return:
        """
        path=b'/instance/{instanceId}/parameter'
        formatted_url = path.decode().format(instanceId=instance_id).encode()
        return self._send_request(http_method=http_methods.GET,
                               path=formatted_url,
                               params={'keyword': keyword},
                               config=config)

    @required(instance_id=(str), e_tag=(str), effective_time=(str), parameters=(list))
    def modify_config_parameter(self, instance_id, e_tag, effective_time, parameters,
                                config=None):
        """
         Modifying config parameters for the specified instance

        :param instance_id:
            The specified instance id
        :type instance_id: str

        :param e_tag:
            The new version, for example, v1,
            is obtained from the details list
        :type e_tag: str

        :param effective_time:
            Actual validity mode: immediate or
            maintenance time (timewindow)
        :type effective_time: str

        :param parameters:
            Parameter list to be modified
        :type parameters: list

        :param config: config
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        headers = {b'Content-Type': b'application/json', b'x-bce-if-match': e_tag}
        data = {
            "effectiveTime": effective_time,
            "parameters": parameters
        }
        path=b'/instance/{instanceId}/parameter'
        formatted_url = path.decode().format(instanceId=instance_id).encode()
        return self._send_request(http_method=http_methods.PUT,
                                  path=formatted_url,
                                  body=json.dumps(data),
                                  headers=headers,
                                  config=config)

    @required(instance_id=(str))
    def query_modify_parameter_history_List(self, instance_id, config=None):
        """
         query modify parameter history list

        :param instance_id:
            The specified instance id
        :type instance_id: str

        :param config: config
        :type config: baidubce.BceClientConfiguration

        :return:
        """
        path=b'/instance/{instanceId}/parameter/history'
        formatted_url = path.decode().format(instanceId=instance_id).encode()
        return self._send_request(http_method=http_methods.GET,
                               path=formatted_url,
                               config=config)

    def query_parameter_template_list(self, page_no=None, page_size=None, template_type=None,
                                      db_type=None, db_version=None, config=None):
        """
         query parameter template

        :param page_no:
            The current page number,default is 1
        :type page_no: int

        :param page_size:
            The number of records per page,default is 10
        :type page_no: int

        :param template_type:
            The template type can be user or system.
            The default value is user. user: Returns
            a list of custom parameters. system:
            Returns the system parameter list.
        :type template_type: string

        :param db_type:
            Tthe Database type
        :type db_type: string

        :param db_version:
            The Database version
        :type db_version: string

        :param config:
        :type config: baidubce.BceClientConfiguration
        :return:
        """

        params = {}

        if page_no is not None:
            params['pageNo'] = page_no
        if page_size is not None:
            params['pageSize'] = page_size
        if template_type is not None:
            params['type'] = template_type
        if db_type is not None:
            params['dbType'] = db_type
        if db_version is not None:
            params['dbVersion'] = db_version

        return self._send_request(http_method=http_methods.GET,
                               path=b'/instance/paraTemplate',
                               params=params,
                               config=config)

    @required(template_id=(str))
    def query_parameter_template_detail(self, template_id, config=None):
        """
         query parameter template detail

        :param template_id:
            The id of parameter template
        :type template_id: str

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        """
        path=b'/instance/paraTemplate/template/detail/{templateId}'
        formatted_url = path.decode().format(templateId=template_id).encode()
        return self._send_request(http_method=http_methods.GET,
                                  path=formatted_url,
                                  config=config)

    @required(template_id=(str), name=(str), desc=(str))
    def copy_parameter_template(self, template_id, name, desc, config=None):
        """
         copy parameter template

        :param name:
            The name of parameter template
        :type name: str

        :param desc:
            The description of parameter template
        :type desc: str

        :param template_id:
            The id of parameter template
        :type template_id: str

        :param config:
        :type config: baidubce.BceClientConfiguration
        :return:

        """

        data = {
            'name': name,
            'desc': desc,
            "templateId": template_id
        }
        headers = {b'Content-Type': b'application/json'}
        return self._send_request(http_method=http_methods.POST,
                                  path=b'/instance/paraTemplate/duplicate/template',
                                  headers=headers,
                                  body=json.dumps(data),
                                  config=config)

    # security manager
    @required(instance_id=(str))
    def get_white_list(self, instance_id, config=None):
        """
         query whit list

        :param instance_id: the specified instance id
        :type instance_id: str

        :param config:
        :type config: baidubce.BceClientConfiguration
        :return:
        """
        path=b'/instance/{instanceId}/securityIp'
        formatted_url = path.decode().format(instanceId=instance_id).encode()
        return self._send_request(http_method=http_methods.GET,
                               path=formatted_url,
                               config=config)

    @required(instance_id=(str), security_ips=(list), e_tag=(str))
    def update_white_list(self, instance_id, security_ips, e_tag, config=None):
        """
         update whit list

        :param instance_id: the specified instance id
        :type instance_id: str

        :param security_ips:
            Set the IP addresses of the whitelist, separated by commas (,)
            for example:  [ "xx.xx.xx.xx","xx.xx.xx.xx" ]
        :type security_ips: list

        :param e_tag:
            The ETag value is obtained by querying the interface
        :type e_tag: str

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        """
        path=b'/instance/{instanceId}/securityIp'
        formatted_url = path.decode().format(instanceId=instance_id).encode()
        data = {"securityIps": security_ips}
        headers = {b'Content-Type': b'application/json', b'x-bce-if-match': e_tag}
        return self._send_request(http_method=http_methods.PUT,
                                  path=formatted_url,
                                  headers=headers,
                                  body=json.dumps(data),
                                  config=config)

    @required(instance_id=(str))
    def get_ssl_status(self, instance_id, config=None):
        """
         Enable and disable ssl

        :param instance_id:
            the specified instance id
        :type instance_id: str

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        path=b'/instance/ssl/{instanceId}'
        formatted_url = path.decode().format(instanceId=instance_id).encode()
        return self._send_request(http_method=http_methods.GET,
                                  path=formatted_url,
                                  config=config)

    def obtain_ssl_ca(self, config=None):
        """
         Obtaining a ca Certificate

        :param config:
        ：type config: baidubce.BceClientConfiguration
        :return:
        """

        return self._send_request(http_method=http_methods.GET,
                                  path=b'/instance/ssl/static/ca',
                                  config=config)

    # read only manager
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
        path = b'/rds/{sourceAppId}/rogroup'
        formatted_url = path.decode().format(sourceAppId=instance_id).encode()
        headers = {b'Content-Type': b'application/json'}
        return self._send_request(http_method=http_methods.POST,
                               path=formatted_url,
                               body=json.dumps(data),
                               headers=headers,
                               config=config)

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
        path = b'/rds/{sourceAppId}/rogroup/detail/{roGroupId}'
        formatted_url = path.decode().format(sourceAppId=instance_id, roGroupId=ro_group_id).encode()
        return self._send_request(http_method=http_methods.GET,
                               path=formatted_url,
                               config=config)

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
        path = b'/rds/{sourceAppId}/rogroup/list'
        formatted_url = path.decode().format(sourceAppId=instance_id).encode()
        headers = {b'Content-Type': b'application/json'}
        return self._send_request(http_method=http_methods.GET,
                               path=formatted_url,
                               config=config)

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
        path = b'/rds/{sourceAppId}/rogroup/{roGroupId}/join'
        formatted_url = path.decode().format(sourceAppId=instance_id, roGroupId=ro_group_id).encode()
        headers = {b'Content-Type': b'application/json'}
        self._send_request(http_method=http_methods.PUT,
                           path=formatted_url,
                           headers=headers,
                           body=json.dumps(data),
                           config=config)

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
        path = b'/rds/{sourceAppId}/rogroup/{roGroupId}/reload'
        formatted_url = path.decode().format(sourceAppId=source_app_id, roGroupId=ro_group_id).encode()
        headers = {b'Content-Type': b'application/json'}
        self._send_request(http_method=http_methods.PUT,
                           path=formatted_url,
                           headers=headers,
                           config=config)

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
        path = b'/rds/{sourceAppId}/rogroup/{roGroupId}/updateRoGroupProperty'
        formatted_url = path.decode().format(sourceAppId=source_app_id, roGroupId=ro_group_id).encode()
        headers = {b'Content-Type': b'application/json'}
        self._send_request(http_method=http_methods.PUT,
                           path=formatted_url,
                           body=json.dumps(data),
                           headers=headers,
                           config=config)

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
        path = b'/rds/{sourceAppId}/rogroup/{roGroupId}/updatePubliclyAccessible'
        formatted_url = path.decode().format(sourceAppId=source_app_id, roGroupId=ro_group_id).encode()
        headers = {b'Content-Type': b'application/json'}
        self._send_request(http_method=http_methods.PUT,
                           path=formatted_url,
                           body=json.dumps(data),
                           headers=headers,
                           config=config)

    @required(source_app_id=(str), ro_group_id=(str))
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
        path = b'/rds/{sourceAppId}/rogroup/{roGroupId}/updateEndpoint'
        formatted_url = path.decode().format(sourceAppId=source_app_id, roGroupId=ro_group_id).encode()
        headers = {b'Content-Type': b'application/json'}
        self._send_request(http_method=http_methods.PUT,
                           path=formatted_url,
                           headers=headers,
                           body=json.dumps(data),
                           config=config)

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
        path = b'/rds/{sourceAppId}/rogroup/{roGroupId}/leave'
        formatted_url = path.decode().format(sourceAppId=source_app_id, roGroupId=ro_group_id).encode()
        headers = {b'Content-Type': b'application/json'}
        self._send_request(http_method=http_methods.PUT,
                           path=formatted_url,
                           headers=headers,
                           body=json.dumps(data),
                           config=config)

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
        path = b'/rds/{sourceAppId}/rogroup/{roGroupId}'
        formatted_url = path.decode().format(sourceAppId=source_app_id, roGroupId=ro_group_id).encode()
        self._send_request(http_method=http_methods.DELETE,
                           path=formatted_url,
                           config=config)

def generate_client_token_by_uuid():
    """
    The default method to generate the random string for client_token
    if the optional parameter client_token is not specified by the user.
    :return:
    :rtype string
    """
    return str(uuid.uuid4())

generate_client_token = generate_client_token_by_uuid