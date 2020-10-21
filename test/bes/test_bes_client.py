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
Unit tests for bes client.
"""

import sys
import time
import unittest

import baidubce
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.bes.bes_client import BesClient
from baidubce.services.bes.bes_model import Billing
from baidubce.services.bes.bes_model import Module

PY2 = sys.version_info[0] == 2
if PY2:
    reload(sys)
    sys.setdefaultencoding('utf8')

# client config
HOST = b'host'
AK = b'ak'
SK = b'sk'
REGION = b'region'

# operation params
pre_name = 'test'
name = 'test'
password = '123456aA'
modules = [Module(type='es_node', instance_num=1), Module(type='kibana', instance_num=1)]
version = '7.4.2'
modules_resize = [
    Module(type='es_node', slot_type='calculate_v1', version=version, desire_instance_num=2),
    Module(type='kibana', slot_type='calculate_v1', version=version, desire_instance_num=1)]

slot_type = 'calculate_v1'
is_open_service = False
available_zone = 'zoneA'
security_group_id = '3742b538-039b-41fc-999b-b15d3bfb381b'
subnet_uuid = '20d48ab8-22d4-4e13-a762-e806fb9a0e19'
vpcId = '0e4e00bc-4bf1-49bd-bdf6-854676922a1d'
# billing = Billing(payment='prepay', time=3)
billing = Billing(payment='postpay', time=0)
region = 'bj'
product_type = 'postpay'


class TestBesClient(unittest.TestCase):
    """
    Test class for bes sdk client
    """

    def setUp(self):
        print("---init begin")
        config = BceClientConfiguration(credentials=BceCredentials(AK, SK), endpoint=HOST, region=REGION)
        self.client = BesClient(config)
        # self.clean_data()
        # time.sleep(20)
        # self.init_data()
        # time.sleep(5)
        print("---init end")

    def tearDown(self):
        print("---clean begin")
        time.sleep(5)
        # self.clean_data()
        print("---clean end")

    def test_create_cluster(self):
        """
        test create bes cluster
        """
        # clean data before create cluster
        print("---test_create_cluster")
        # self.clean_data()
        # time.sleep(5)
        response = self.client.create_cluster(name,
                                              password,
                                              modules,
                                              version,
                                              slot_type,
                                              is_open_service,
                                              available_zone,
                                              security_group_id,
                                              subnet_uuid,
                                              vpcId,
                                              billing)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_resize_cluster(self):
        """
        test resize cluster
        """
        print("---test_resize_cluster")
        response = self.client.get_cluster_list(page_no=1, page_size=2)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        page = response.page
        if page is None:
            return
        for cluster in (page.result or []):
            if cluster.cluster_id != '439335249076424704':
                continue
            print('cluster_id:' + cluster.cluster_id)
            self.assertEqual(type(response), baidubce.bce_response.BceResponse)
            response = self.client.resize_cluster(name,
                                                  product_type,
                                                  cluster.cluster_id,
                                                  region,
                                                  modules_resize)
            self.assertEqual(type(response), baidubce.bce_response.BceResponse)
            print(response)

    def test_get_cluster_list(self):
        """
        test list cluster
        """
        print("---test_list_cluster")
        response = self.client.get_cluster_list(page_no=1, page_size=2)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_cluster_detail(self):
        """
        test detail bes cluster
        """
        print("---test_detail_cluster")
        response = self.client.get_cluster_list(page_no=1, page_size=100)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        page = response.page
        if page is None:
            return
        for cluster in (page.result or []):
            print(cluster.cluster_id)
            response = self.client.get_cluster_detail(cluster_id=cluster.cluster_id)
            self.assertEqual(type(response), baidubce.bce_response.BceResponse)
            print(response)

    def test_start_cluster(self):
        """
        start start bes cluster
        """
        print("---test_start_cluster")
        response = self.client.get_cluster_list(page_no=1, page_size=100)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        # print(response)
        page = response.page
        if page is None:
            return
        for cluster in (page.result or []):
            print('clusterId:' + cluster.cluster_id)
            response = self.client.start_cluster(cluster_id=cluster.cluster_id)
            self.assertEqual(type(response), baidubce.bce_response.BceResponse)
            print(response)

    def test_stop_cluster(self):
        """
        stop stop bes cluster
        """
        print("---test_stop_cluster")
        response = self.client.get_cluster_list(page_no=1, page_size=100)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)
        page = response.page
        if page is None:
            return
        for cluster in (page.result or []):
            print(cluster.cluster_id)
            response = self.client.stop_cluster(cluster_id=cluster.cluster_id)
            self.assertEqual(type(response), baidubce.bce_response.BceResponse)
            print(response)

    def test_delete_cluster(self):
        """
        test delete bes cluster
        """
        print("---test_delete_cluster")
        response = self.client.get_cluster_list(page_no=1, page_size=100)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)
        page = response.pagedelete
        if page is None:
            return
        for cluster in (page.result or []):
            if cluster.cluster_id != '439305389729779712':
                continue
            print(cluster.cluster_id)
            response = self.client._cluster(cluster_id=cluster.cluster_id)
            self.assertEqual(type(response), baidubce.bce_response.BceResponse)
            print(response)

    def test_start_instance(self):
        """
        start instance
        """
        print("---test_start_instance")
        response = self.client.get_cluster_list(page_no=1, page_size=2)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        # print(response)
        page = response.page
        if page is None:
            return
        for cluster in (page.result or []):
            print('cluster.cluster_id:' + cluster.cluster_id)
            response = self.client.get_cluster_detail(cluster_id=cluster.cluster_id)
            self.assertEqual(type(response), baidubce.bce_response.BceResponse)
            result = response.result
            if result is None:
                return
            for instance in (result.instances or []):
                print('instance.instanceId:' + instance.instance_id)
                response = self.client.start_instance(cluster_id=cluster.cluster_id, instance_id=instance.instance_id)
                self.assertEqual(type(response), baidubce.bce_response.BceResponse)
                print(response)

    def test_stop_instance(self):
        """
        stop instance
        """
        print("---test_start_instance")
        response = self.client.get_cluster_list(page_no=1, page_size=2)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        # print(response)
        page = response.page
        if page is None:
            return
        for cluster in (page.result or []):
            print('cluster.cluster_id:' + cluster.cluster_id)
            response = self.client.get_cluster_detail(cluster_id=cluster.cluster_id)
            self.assertEqual(type(response), baidubce.bce_response.BceResponse)
            result = response.result
            if result is None:
                return
            for instance in (result.instances or []):
                print('instance.instanceId:' + instance.instance_id)
                response = self.client.stop_instance(cluster_id=cluster.cluster_id, instance_id=instance.instance_id)
                self.assertEqual(type(response), baidubce.bce_response.BceResponse)
                print(response)

    def init_data(self):
        """
        init_data
        """
        response = self.client.create_cluster(name,
                                              password,
                                              modules,
                                              version,
                                              slot_type,
                                              is_open_service,
                                              available_zone,
                                              security_group_id,
                                              subnet_uuid,
                                              vpcId,
                                              billing)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def clean_data(self):
        """
        clean_data
        """
        response = self.client.get_cluster_list(page_no=1, page_size=100)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        page = response.page
        if page is None:
            return
        for cluster in (page.result or []):
            print(cluster.cluster_id)
            response = self.client.delete_cluster(cluster_id=cluster.cluster_id)
            self.assertEqual(type(response), baidubce.bce_response.BceResponse)
            print(response)
