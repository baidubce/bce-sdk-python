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
This module defines some Response classes for BTS
"""
from baidubce.bce_response import BceResponse
from json import JSONEncoder


class Billing(object):
    """
	This class define billing.
	param: pay_method:
		The pay time of the payment,
	param: reservationLength:
		The duration to buy in specified time unit,
	param: reservationTimeUnit:
		The time unit to specify the duration ,only "Month" can be used now.
	"""

    def __init__(self, pay_method='Prepaid', reservationLength=1, reservationTimeUnit='Month'):
        self.paymentTiming = pay_method
        self.reservation = {
            'reservationLength': reservationLength,
            'reservationTimeUnit': reservationTimeUnit
        }

    def get_pay_method(self):
        """
            get instance current pay_method:Prepaid/Postpaid
        """
        return self.paymentTiming


class SubnetMap(object):
    """
    SubnetMap:contains zoneName and subnetId
    """

    def __init__(self, zone_name, subnet_id):
        super(SubnetMap, self).__init__()
        self.zone_name = str(zone_name)
        self.subnet_id = str(subnet_id)


class Tag(object):
    """
    Tag model
    """

    def __init__(self, key, value):
        super(Tag, self).__init__()
        self.tag_key = str(key)
        self.tag_value = str(value)

    def __repr__(self):
        return repr((self.tag_key, self.tag_value))


class InitialDataReference(object):
    """
        Initial Data Reference
    """

    def __init__(self, instance_id, reference_type, datetime=None, snapshot_id=None):
        super(InitialDataReference, self).__init__()
        self.instance_id = instance_id
        self.reference_type = reference_type
        self.datetime = datetime
        self.snapshot_id = snapshot_id


class RecoveryToSourceInstanceModel(object):
    """
        RecoveryToSourceInstance model
    """

    def __init__(self, restore_mode, db_name, new_dbname, tables=None):
        super(RecoveryToSourceInstanceModel, self).__init__()
        self.restore_mode = restore_mode
        self.db_name = db_name
        self.new_dbname = new_dbname
        self.tables = tables


class Tables(object):
    """
        Tables
    """

    def __init__(self, table_name, new_tablename):
        super(Tables, self).__init__()
        self.table_name = table_name
        self.new_tablename = new_tablename


class CreateInstanceResponse(BceResponse):
    """
    Create Instance Response
    """

    def __init__(self, bce_response):
        super(CreateInstanceResponse, self).__init__()
        self.instance_ids = bce_response.instance_ids
        self.order_id = bce_response.order_id


class GetInstanceResponse(BceResponse):
    """
        Get Instance Response
    """

    def __init__(self, bce_response):
        super(GetInstanceResponse, self).__init__()
        self.instance_id = bce_response.instance_id
        self.instance_name = bce_response.instance_name
        self.engine = bce_response.engine
        self.engine_version = bce_response.engine_version
        self.category = bce_response.category
        self.instance_status = bce_response.instance_status
        self.cpu_count = bce_response.cpu_count
        self.memory_capacity = bce_response.memory_capacity
        self.volume_capacity = bce_response.volume_capacity
        self.node_amount = bce_response.node_amount
        self.used_storage = bce_response.used_storage
        self.instance_create_time = bce_response.instance_create_time
        self.instance_expire_time = bce_response.instance_expire_time
        self.endpoint = bce_response.endpoint
        self.public_access_status = bce_response.public_access_status
        self.sync_mode = bce_response.sync_mode
        self.backup_policy = bce_response.backup_policy
        self.region = bce_response.region
        self.instance_type = bce_response.instance_type
        self.source_instance_id = bce_response.source_instance_id
        self.source_region = bce_response.source_region
        self.zone_names = bce_response.zone_names
        self.vpc_id = bce_response.vpc_id
        self.subnets = bce_response.subnets
        self.topology = bce_response.topology
        self.payment_timing = bce_response.payment_timing
        self.character_set_name = bce_response.character_set_name


class ListInstanceResponse(BceResponse):
    """
    List Instance Response
    """

    def __init__(self, bce_response):
        super(ListInstanceResponse, self).__init__()
        self.max_keys = bce_response.max_keys
        self.marker = str(bce_response.marker)
        self.next_marker = str(bce_response.next_marker)
        self.is_truncated = bce_response.is_truncated
        self.instances = bce_response.instances


class ListZoneResponse(BceResponse):
    """
    List zone.
    """

    def __init__(self, bce_response):
        super(ListZoneResponse, self).__init__()
        self.zones = bce_response.zones


class ListSubnetResponse(BceResponse):
    """
    List zone.
    """

    def __init__(self, bce_response):
        super(ListSubnetResponse, self).__init__()
        self.subnets = bce_response.subnets


class Instance(object):
    """
    instance.
    """

    def __init__(self, engine, engine_version, cpu_count, allocated_memory_in_g_b, allocated_storage_in_g_b,
                 category, disk_io_type):
        super(Instance, self).__init__()
        self.engine = engine
        self.engineVersion = engine_version
        self.cpuCount = cpu_count
        self.allocatedMemoryInGB = allocated_memory_in_g_b
        self.allocatedStorageInGB = allocated_storage_in_g_b
        self.category = category
        self.diskIoType = disk_io_type


class PriceResponse(BceResponse):
    """
    price response.
    """

    def __init__(self, bce_response):
        super(PriceResponse, self).__init__()
        self.price = bce_response.price


class OrderStatusResponse(BceResponse):
    """
    order status response.
    """
    def __init__(self, bce_response):
        super(OrderStatusResponse, self).__init__()
        self.orderId = bce_response.orderId
        self.status = bce_response.status


class TaskResponse(BceResponse):
    """
    task response.
    """
    def __init__(self, bce_response):
        super(TaskResponse, self).__init__()
        self.tasks = bce_response.tasks


class ForceChangeResponse(BceResponse):
    """
    ForceChange response.
    """
    def __init__(self, bce_response):
        super(ForceChangeResponse, self).__init__()
        self.behindMaster = bce_response.behindMaster

class GroupResponse(BceResponse):
    """
    grop response.
    """

    def __init__(self, bce_response):
        super(GroupResponse, self).__init__()
        self.group_id = bce_response.group_id
        self.name = bce_response.name
        self.count = bce_response.count
        self.leader = bce_response.leader


class GroupDetailResponse(BceResponse):
    """
    grop detail response.
    """

    def __init__(self, bce_response):
        super(GroupDetailResponse, self).__init__()
        self.group_id = bce_response.group_id
        self.name = bce_response.name
        self.count = bce_response.count
        self.leader = bce_response.leader
        self.followers = bce_response.followers


class GroupCheckGtidResponse(BceResponse):
    """
    grop checkGtid response.
    """

    def __init__(self, bce_response):
        super(GroupCheckGtidResponse, self).__init__()
        self.result = bce_response.result


class JsonWrapper(JSONEncoder):
    """
        custom json encoder for class
    """

    def default(self, obj):  # pylint: disable=E0202
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        if isinstance(obj, SubnetMap):
            return {
                'zoneName': obj.zone_name,
                'subnetId': obj.subnet_id
            }
        if isinstance(obj, Tag):
            return {
                'tagKey': obj.tag_key,
                'tagValue': obj.tag_value
            }
        if isinstance(obj, InitialDataReference):
            return {
                'instanceId': obj.instance_id,
                'referenceType': obj.reference_type,
                'datetime': obj.datetime,
                'snapshotId': obj.snapshot_id
            }
        if isinstance(obj, RecoveryToSourceInstanceModel):
            return {
                'restoreMode': obj.restore_mode,
                'dbName': obj.db_name,
                'newDbname': obj.new_dbname,
                'tables': obj.tables
            }
        if isinstance(obj, Tables):
            return {
                'tableName': obj.table_name,
                'newTablename': obj.new_tablename
            }
        return JSONEncoder.default(self, obj)
