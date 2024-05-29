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
this model defines RdsInstanceManager  interface
"""

import uuid
import json
import logging

from baidubce.utils import required
from baidubce.http import http_methods
from baidubce.services.rds import rds_http
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.rds.models import rds_instance_model as rds_instance_model


_logger = logging.getLogger(__name__)


class RdsInstanceManager(rds_http.HttpRequest):
    """
         this is RdsInstanceManager openApi interface
        :param HttpRequest:
       """

    def __init__(self, config=None):
        """
        :param config:

        """
        rds_http.HttpRequest.__init__(self, config)

    @required(config=BceClientConfiguration)
    def _check_config_type(self, config):
        return True

    @required(instance_name=(str), engine=(str), engine_version=(str), category=(str),
              cpuCount=int, memory_capacity=int, volume_capacity=int, disk_io_type=(str),
              purchase_count=int, zone_names=list, vpc_id=(str), is_direct_pay=bool,
              subnets=list, tags=list, bgw_group_id=(str), bgw_group_exclusive=bool,
              character_set_name=(str), lower_case_table_names=int, parameter_template_id=(str),
              auto_renew_time_unit=(str), auto_renew_time=int,
              initial_data_reference=rds_instance_model.InitialDataReference, data=list,
              billing=rds_instance_model.Billing)
    def create_instance(self, engine, engine_version, category, cpu_count, memory_capacity, volume_capacity,
                        disk_io_type, is_direct_pay=None, initial_data_reference=None, bgw_group_id=None,
                        bgw_group_exclusive=None, character_set_name=None, lower_case_table_names=None,
                        parameter_template_id=None, data=None, instance_name=None, vpc_id=None, subnets=None,
                        tags=None, purchase_count=1, zone_names=None, auto_renew_time_unit='month',
                        auto_renew_time=None, billing=None, config=None):
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
            billing = rds_instance_model.Billing()

        if zone_names is None:
            zone_names = []

        if subnets is None:
            subnets = []

        if tags is None:
            tags = []

        if data is None:
            data = []

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

        return rds_instance_model.CreateInstanceResponse(
            self._send_request(http_methods.POST,
                               'instance',
                               params={"clientToken": uuid.uuid4()},
                               body=json.dumps(data, cls=rds_instance_model.JsonWrapper, indent=4),
                               config=config,
                               api_version=1))

    @required(instance_name=(str), source_instance_id=(str), zone_names=list, vpc_id=(str),
              is_direct_pay=bool, subnets=list, tags=list, billing=rds_instance_model.Billing)
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
            billing = rds_instance_model.Billing()

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
        return rds_instance_model.CreateInstanceResponse(
            self._send_request(http_methods.POST,
                               'instance',
                               params={"clientToken": uuid.uuid4(), "readReplica": ""},
                               body=json.dumps(data, cls=rds_instance_model.JsonWrapper, indent=4),
                               config=config,
                               api_version=1))

    @required(instance_name=(str), source_instance_id=(str), node_amount=int, zone_names=list,
              vpc_id=(str), is_direct_pay=bool, subnets=list, tags=list, billing=rds_instance_model.Billing)
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
            billing = rds_instance_model.Billing()

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
        return rds_instance_model.CreateInstanceResponse(
            self._send_request(http_methods.POST,
                               'instance',
                               params={"clientToken": uuid.uuid4(), "rdsproxy": ""},
                               body=json.dumps(data, cls=rds_instance_model.JsonWrapper, indent=4),
                               config=config,
                               api_version=1))

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
        return rds_instance_model.GetInstanceResponse(
            self._send_request(http_methods.GET,
                               function_name='instance',
                               key=instance_id,
                               config=config,
                               api_version=1))

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
        return rds_instance_model.ListInstanceResponse(
            self._send_request(http_methods.GET,
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
        return rds_instance_model.CreateInstanceResponse(
            self._send_request(http_methods.PUT,
                               'instance',
                               key=instance_id,
                               params={"resize": ""},
                               body=json.dumps(data),
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
        return self._send_request(http_method=http_methods.DELETE,
                                  function_name='instance',
                                  params={"instanceIds": instance_ids},
                                  config=config,
                                  api_version=1)

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

        return self._send_request(http_method=http_methods.PUT,
                                  function_name='instance',
                                  key=instance_id,
                                  params={"reboot": ""},
                                  config=config,
                                  api_version=1)

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
        return self._send_request(http_method=http_methods.PUT,
                                  function_name='instance',
                                  key=instance_id,
                                  params={"rename": ""},
                                  body=json.dumps(data),
                                  config=config,
                                  api_version=1)

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
        return self._send_request(http_method=http_methods.PUT,
                                  function_name='instance',
                                  key=instance_id,
                                  params={"modifySyncMode": ""},
                                  body=json.dumps(data),
                                  config=config,
                                  api_version=1)

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
        return self._send_request(http_method=http_methods.PUT,
                                  function_name='instance',
                                  key=instance_id,
                                  params={"modifyEndpoint": ""},
                                  body=json.dumps(data),
                                  config=config,
                                  api_version=1)

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
        return self._send_request(http_method=http_methods.PUT,
                                  function_name='instance',
                                  key=instance_id,
                                  params={"modifyPublicAccess": ""},
                                  body=json.dumps(data),
                                  config=config,
                                  api_version=1)

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
        return self._send_request(http_method=http_methods.PUT,
                                  function_name='instance',
                                  params={"autoRenew": ""},
                                  body=json.dumps(data),
                                  config=config,
                                  api_version=1)

    def zone(self, config=None):
        """
         Get zone list

        :param config:
        :type  config: BceClientConfiguration

        :return:
        """
        return rds_instance_model.ListZoneResponse(
            self._send_request(
                http_method=http_methods.GET,
                function_name='zone',
                config=config,
                api_version=1))

    def subnet(self, vpc_id=None, zone_name=None, config=None):
        """
         get Subnet list

        :param config:
        :type  config: BceClientConfiguration

        :return:
        """
        return rds_instance_model.ListSubnetResponse(
            self._send_request(http_method=http_methods.GET,
                               function_name='subnet',
                               params={"vpcId": vpc_id, "zoneName": zone_name},
                               config=config,
                               api_version=1))

    @required(instance_id=(str))
    def start_instance(self, instance_id, config=None):
        """
         Start the current instance

        :param instance_id:
            the ID of instance
        :type  instance_id: str

        :param config:
        :type  config: BceClientConfiguration

        :return:
        """

        return self._send_request(http_method=http_methods.PUT,
                                  function_name='instance',
                                  key=instance_id + '/start',
                                  config=config,
                                  api_version=1)

    @required(instance_id=(str))
    def suspend_instance(self, instance_id, config=None):
        """
         Pause the current instance

        :param instance_id:
            the ID of instance
        :type  instance_id: string

        :param config:
        :type  config: BceClientConfiguration

        :return:
        """

        return self._send_request(http_method=http_methods.PUT,
                                  function_name='instance',
                                  key=instance_id + '/suspend',
                                  config=config,
                                  api_version=1)

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

        return rds_instance_model.PriceResponse(
            self._send_request(http_methods.POST,
                               'instance/price',
                               body=json.dumps(data, cls=rds_instance_model.JsonWrapper, indent=4),
                               config=config,
                               api_version=1))

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

        return self._send_request(http_method=http_methods.GET,
                                  function_name='instance',
                                  key='/order/' + order_id,
                                  config=config,
                                  api_version=1)

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

        return rds_instance_model.CreateInstanceResponse(
            self._send_request(http_method=http_methods.POST,
                               function_name='instance',
                               key='/renew',
                               body=json.dumps(data),
                               config=config,
                               api_version=1))

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

        return self._send_request(http_method=http_methods.PUT,
                                  function_name='instance',
                                  key=instance_id + '/maintaintime',
                                  body=json.dumps(data),
                                  config=config,
                                  api_version=1)
