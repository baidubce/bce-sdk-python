#!/usr/bin/env python
# coding=utf8

import logging
import os
import sys
import unittest

import baidubce.services.scs.scs_client as scs
import baidubce.services.scs.model as model
from QaConf import config1
from QaConf import config2
from baidubce.exception import BceHttpClientError

if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')

logging.basicConfig(level=logging.DEBUG, filename='./scs_sample.log', filemode='w')
LOG = logging.getLogger(__name__)


class TestScsClient(unittest.TestCase):

    def setUp(self):
        self.instance_id = 'scs-bj-hlfcrrmeggfj'
        self.scs_client1 = scs.ScsClient(config1)
        self.scs_client2 = scs.ScsClient(config2)

    def tearDown(self):
        pass

    def test_create_instance(self):
        # 创建实例
        instance_name = 'redis-py-create'
        billing = model.Billing(pay_method='Postpaid')
        node_type = 'cache.n1.micro'
        shard_num = 1
        proxy_num = 0
        cluster_type = 'master_slave'
        replication_num = 2
        port = 7001
        engine_version = '3.2'
        vpc_id = 'vpc-sqq7nuryepat'
        subnets = [
            model.SubnetMap(u'cn-bj-d', u'sbn-p5xq05kxfhsp'),
            model.SubnetMap(u'cn-bj-a', u'sbn-w1tw0787su6d')
        ]
        resp = self.scs_client1.create_instance(instance_name=instance_name, billing=billing, node_type=node_type,
                                                shard_num=shard_num, proxy_num=proxy_num, cluster_type=cluster_type,
                                                replication_num=2, port=port, engine_version=engine_version,
                                                vpc_id=vpc_id, subnets=subnets)
        self.assertIsNotNone(resp.instance_ids)

        # 获取实例详情
        instance = self.scs_client1.get_instance_detail(instance_id=str(resp.instance_ids[0]))
        self.assertEqual(str(port), instance.port)
        self.assertEqual(instance_name, instance.instance_name)

    def test_resize_instance(self):
        resp = self.scs_client1.resize_instance(self.instance_id, 'cache.n1.small')

    def test_instance(self):
        # 获取实例列表
        resp = self.scs_client1.list_instances()
        self.assertEqual(False, resp.is_truncated)
        self.assert_(len(resp.instances) > 0)

        resp = self.scs_client1.list_instances(max_keys=2)
        self.assertEqual(True, resp.is_truncated)
        self.assertEqual(2, resp.max_keys)
        self.assertEqual(2, len(resp.instances))

        # 修改实例名称
        self.scs_client1.rename_instance(instance_id=self.instance_id, instance_name='redis-py')

        # 获取实例详情
        instance = self.scs_client1.get_instance_detail(instance_id=str(self.instance_id))
        self.assertEqual("Postpaid", instance.payment_timing)
        self.assertEqual("redis-py", instance.instance_name)

        # 获取可用区列表
        resp = self.scs_client1.list_available_zones()
        self.assertEqual(15, len(resp.zones))

        # 获取子网列表
        resp = self.scs_client1.list_subnets()
        self.assertEqual(24, len(resp.subnets))

        # 获取节点规格列表
        resp = self.scs_client1.list_nodetypes()
        self.assert_(len(resp.cluster_node_type_list) > 0)
        self.assert_(len(resp.default_node_type_list) > 0)
        self.assert_(len(resp.hsdb_node_type_list) > 0)

    def test_clear_instance(self):
        # 清空实例
        resp = self.scs_client1.flush_instance(self.instance_id)

    def test_tags(self):

        # 绑定标签
        resp = self.scs_client1.bind_tags(
            self.instance_id, [model.Tag(u'用途', u'测试'), model.Tag(u'测试人', u'你猜')]
        )

        # 解绑标签
        resp = self.scs_client1.unbind_tags(
            self.instance_id, [model.Tag('用途', '测试')]
        )

    def test_network(self):

        # 增加IP白名单
        resp = self.scs_client1.add_security_ips(self.instance_id, ['192.168.1.3'])

        # 删除IP白名单
        resp = self.scs_client1.delete_security_ips(self.instance_id, ['192.168.1.2'])

        # 查询IP白名单
        resp = self.scs_client1.list_security_ip(self.instance_id)
        print(resp.security_ips)
        self.assertIsNotNone(resp.security_ips)

        # 修改访问密码
        resp = self.scs_client1.modify_password(self.instance_id, 'password')

    def test_parameter(self):

        # 获取参数列表
        resp = self.scs_client1.list_parameters(self.instance_id)
        print(resp.parameters)
        self.assertIsNotNone(resp.parameters)

        # 修改参数
        try:
            self.scs_client1.modify_parameter(self.instance_id, 'appendonly', 'yes')
            resp = self.scs_client1.list_parameters(self.instance_id)
            self.assertEqual('yes', model.Parameter(resp.parameters[0]).value)
        except BceHttpClientError as e:
            pass

    def test_backup(self):
        # 获取备份列表
        resp = self.scs_client1.list_backups(self.instance_id)
        self.assertEqual(1, len(resp.total_count))

        # 获取备份详情
        if len(resp.backups) > 0:
            backup_record_id = model.BackupRecord(model.Backup(resp.backups[0]).records[0]).backup_record_id
            resp = self.scs_client1.get_backup(self.instance_id, backup_record_id)
            print(resp)
            self.assertEqual("1800", resp.url_expiration)
            self.assert_(resp.url.startswith("http://bj.bcebos.com/scs-backup-rdb-bucket-bj"))

        # 修改备份策略
        resp = self.scs_client1.modify_backup_policy(self.instance_id, 'Mon,Thu',
                                                     '01:05:00', 5)
        pass

    def test_disaster_recovery(self):
        # 设置集群为热活主地域
        resp = self.scs_client1.set_as_master(
            self.instance_id
        )
        # 设置集群为热活从地域
        resp = self.scs_client1.set_as_slave(
            'scs-bj-aixanaiajitc',
            'redis.nacgbwtlxguv.scs.bj.baidubce.com',
            master_port=6379
        )

    def test_delete_instance(self):
        resp = self.scs_client1.delete_instance('scs-bj-pqgqxjjphfhr')


if __name__ == '__main__':
    unittest.main()
