#!/usr/bin/env python
# coding=utf8

import logging
import os
import sys
import unittest

import baidubce.services.rds.rds_client as rds
import baidubce.services.rds.model as model
from QaConf import config1
from QaConf import config2
from baidubce.exception import BceHttpClientError

if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')

logging.basicConfig(level=logging.DEBUG, filename='./rds_sample.log', filemode='w')
LOG = logging.getLogger(__name__)


class TestRdsClient(unittest.TestCase):

    def setUp(self):
        self.instance_id = 'rds-9jV9lLI9'
        self.vpc_id = 'vpc-ph7237ym686c'
        self.subnets = [
            model.SubnetMap(u'cn-bj-d', u'sbn-p1va817v3qn0')
        ]
        self.post_billing = model.Billing(pay_method='Postpaid')
        self.engine = 'MySql'
        self.engine_version = '5.7'
        self.category = 'Standard'
        self.cpu_count = 1
        self.memory_capacity = 2
        self.volume_capacity = 100
        self.disk_io_type = 'cloud_enha'
        self.rds_client1 = rds.RdsClient(config1)
        self.rds_client2 = rds.RdsClient(config2)

    def tearDown(self):
        pass

    def test_create_instance(self):
        # 创建实例
        instance_name = 'rds-py-create'
        billing = self.post_billing
        purchase_count = 1
        engine = self.engine
        engine_version = self.engine_version
        category = self.category
        cpu_count = self.cpu_count
        memory_capacity = self.memory_capacity
        volume_capacity = self.volume_capacity
        disk_io_type = self.disk_io_type
        vpc_id = self.vpc_id
        is_direct_pay = bool(1)
        subnets = self.subnets
        #tags = [
        #    model.Tag(u'key', u'value'),
        #    model.Tag(u'zyh', u'haha')
        #]
        #parameter_template_id = "167"
        #initial_data_reference = model.InitialDataReference(instance_id='rds-gvQDRheI', reference_type='snapshot', snapshot_id='1681225244867371501')
        #data = [
        #    model.RecoveryToSourceInstanceModel(db_name='test2', new_dbname='test22', restore_mode='table',
        #                                        tables=[
        #                                            model.Tables(table_name='table1', new_tablename='table11')
        #                                        ]
        #                                        )
        #]
        response = self.rds_client1.create_instance(instance_name=instance_name, billing=billing,
                                              purchase_count=purchase_count, engine=engine,
                                              engine_version=engine_version, category=category,
                                              cpu_count=cpu_count, memory_capacity=memory_capacity,
                                              volume_capacity=volume_capacity,disk_io_type=disk_io_type,
                                              vpc_id=vpc_id, subnets=subnets,
                                              is_direct_pay=is_direct_pay)
        LOG.debug('\n%s', response)
        self.instance_id = response.instance_ids[0]

    def test_create_read_instance(self):
        # 创建只读实例
        instance_name = 'rds-py-create-read'
        source_instance_id = self.instance_id
        billing = self.post_billing
        cpu_count = self.cpu_count
        memory_capacity = self.memory_capacity
        volume_capacity = self.volume_capacity
        vpc_id = self.vpc_id
        is_direct_pay = bool(1)
        subnets = self.subnets
        response = self.rds_client1.create_read_instance(instance_name=instance_name, source_instance_id=source_instance_id,
                                                   billing=billing, vpc_id=vpc_id, is_direct_pay=is_direct_pay,
                                                   subnets=subnets,
                                                   cpu_count=cpu_count, memory_capacity=memory_capacity,
                                                   volume_capacity=volume_capacity)
        instance_read_id = response.instance_ids[0]
        LOG.debug('\n%s', response)

    def test_create_proxy_instance(self):
        # 创建代理实例
        instance_name = 'rds-py-create-proxy'
        source_instance_id = self.instance_id
        billing = self.post_billing
        node_amount = 2
        vpc_id = self.vpc_id
        is_direct_pay = bool(1)
        subnets = self.subnets
        response = self.rds_client1.create_proxy_instance(instance_name=instance_name, source_instance_id=source_instance_id,
                                                    billing=billing, vpc_id=vpc_id, is_direct_pay=is_direct_pay,
                                                    subnets=subnets, node_amount=node_amount)
        LOG.debug('\n%s', response)
        instance_proxy_id = response.instance_ids[0]

    def test_instance_detail(self):
        # 实例详情
        response = self.rds_client1.get_instance_detail(self.instance_id)
        LOG.debug('\n%s', response)

    def test_instance(self):
        # 实例列表
        response = self.rds_client1.list_instances(max_keys=10)
        LOG.debug('\n%s', response)

    def test_resize_instance(self):
        # 变配实例
        instance_id = self.instance_id
        cpu_count = 1
        memory_capacity = 4
        volume_capacity = 100
        #node_amount = 4
        is_direct_pay = bool(1)

        response = self.rds_client1.resize_instance(instance_id=instance_id, cpu_count=cpu_count,
                                              memory_capacity=memory_capacity, volume_capacity=volume_capacity,
                                              is_direct_pay=is_direct_pay)
        LOG.debug('\n%s', response)

    def test_reboot_instance(self):
        # 重启实例
        response = self.rds_client1.reboot_instance(self.instance_id)

    def test_rename_instance(self):
        # 更新实例名称
        instance_id = self.instance_id
        instance_name = "py-test"
        response = self.rds_client1.rename_instance(instance_id=instance_id, instance_name=instance_name)

    def test_modif_sync_mode_instance(self):
        # 更新实例同步模式
        instance_id = self.instance_id
        sync_mode = "Semi_sync"
        response = self.rds_client1.modify_sync_mode_instance(instance_id=instance_id, sync_mode=sync_mode)
        LOG.debug('\n%s', response)

    def test_modify_endpoint_instance(self):
        # 更新实例连接信息
        instance_id = self.instance_id
        address = "python"
        response = self.rds_client1.modify_endpoint_instance(instance_id=instance_id, address=address)

    def test_modify_public_access_instance(self):
        # 更新实例公网访问状态
        instance_id = self.instance_id
        public_access = bool(1)
        response = self.rds_client1.modify_public_access_instance(instance_id=instance_id, public_access=public_access)

    def test_auto_renew_instance(self):
        # 实例开启自动续费
        instance_ids = [self.instance_id]
        auto_renew_time_unit = "month"
        auto_renew_time = 1

        response = self.rds_client1.auto_renew_instance(instance_ids=instance_ids, auto_renew_time_unit=auto_renew_time_unit,
                                                  auto_renew_time=auto_renew_time)
        LOG.debug('\n%s', response)

    def test_zone_list(self):
        # 查询可用区列表
        response = self.rds_client1.zone()

    def test_subnet_list(self):
        # 查询查询子网列表
        response = self.rds_client1.subnet()

    def test_price_instance(self):
        # 获取价格
        instance = model.Instance(engine='sqlserver', engine_version='2016', cpu_count=2, allocated_memory_in_g_b=8,
                                  allocated_storage_in_g_b=50, category='Singleton', disk_io_type='cloud_enha')
        duration = 1
        number = 1
        product_type = "prepay"
        response = self.rds_client1.price_instance(instance=instance, duration=duration, number=number,
                                             product_type=product_type)

    def test_suspend_instance(self):
        # 暂停实例
        instance_id = self.instance_id
        response = self.rds_client1.suspend_instance(instance_id=instance_id)

    def test_start_instance(self):
        # 启动实例
        instance_id = self.instance_id
        response = self.rds_client1.start_instance(instance_id=instance_id)

    def test_delete_instance(self):
        # 释放实例
        resp = self.rds_client1.delete_instance(self.instance_id)

    def test_recycler_list(self):
        # 回收站列表
        response = self.rds_client1.recycler_list()

    def test_recycler_recover(self):
        # 从回收站恢复实例（单个、批量均通过同一个接口）
        instance_ids = [self.instance_id]
        response = self.rds_client1.recycler_recover(instance_ids)

    def test_delete_recycler(self):
        # 从回收站中释放单个实例
        response = self.rds_client1.delete_recycler(self.instance_id)

    def test_delete_recycler_batch(self):
        # 从回收站中释放批量实例
        response = self.rds_client1.delete_recycler_batch(self.instance_id)


if __name__ == '__main__':
    unittest.main()
