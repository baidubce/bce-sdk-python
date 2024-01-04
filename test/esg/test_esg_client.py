# !/usr/bin/env python
# coding=UTF-8
#
# Copyright 2023 Baidu, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
"""
This module for test.
"""
import baidubce
import unittest

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.esg import esg_client
from baidubce.services.esg import esg_model

esg_id = 'esg-zdeijr7gmjnh'
esg_rule_id = 'esgr-um5ggn03bqaj'

class TestEsgClient(unittest.TestCase):
    """
    unit test
    """

    def setUp(self):
        """
        set up
        """
        AK = "AK"  # 账号的Ak
        SK = "SK"  # 账号的Sk
        ENDPOINT = 'bcc.bj.baidubce.com'
        config = BceClientConfiguration(credentials=BceCredentials(AK, SK),
                                        endpoint=ENDPOINT)
        self.the_client = esg_client.EsgClient(config)
        self.rule = esg_model.EnterpriseSecurityGroupRuleModel(remark='test0',  # 规则备注
                                                               direction='ingress',  # 规则方向 ingress or egress
                                                               action='allow',  # 动作 allow or deny
                                                               protocol='udp',  # 协议 tcp or udp
                                                               portRange='78-98',  # 端口范围
                                                               priority=1000,  # 优先级
                                                               ethertype='IPv6',  # 协议类型
                                                               sourceIp='192.168.0.33',  # 源ip
                                                               destIp='10.0.0.1',  # 目的ip
                                                               sourcePortRange='10-19',  # 源端口范围
                                                               )
        self.rules = []  # 规则列表
        self.rules.append(self.rule)

    def tearDown(self):
        """
        tear down
        """
        self.the_client = None

    def test_create_enterprise_security_group(self):
        """
        test case for create_enterprise_securitygroup
        """
        res = self.the_client.create_enterprise_security_group(name='esg_unittest',
                                                               desc='esg_unittest desc',
                                                               rules=self.rules)
        print(res)
        self.assertEqual(type(res), baidubce.bce_response.BceResponse)

    def test_get_enterprise_securitygrouplist(self):
        """
        test case for get_enterprise_securitygrouplist
        """
        res = self.the_client.list_enterprise_security_groups()
        print(res)
        self.assertEqual(type(res), baidubce.bce_response.BceResponse)

    def test_authorize_enterprise_securitygroup_rule(self):
        """
        test case for authorize_enterprise_securitygroup_rule
        """
        res = self.the_client.authorize_enterprise_security_group_rule(enterprise_security_group_id=esg_id,
                                                                       rules=self.rules,
                                                                       client_token='test')
        print(res)
        self.assertEqual(type(res), baidubce.bce_response.BceResponse)

    def test_delete_enterprise_securitygroup_rule(self):
        """
        test case for delete_enterprise_securitygroup_rule
        """
        res = self.the_client.delete_enterprise_security_group_rule(enterprise_security_group_rule_id=esg_rule_id)
        print(res)
        self.assertEqual(type(res), baidubce.bce_response.BceResponse)

    def test_update_enterprise_securitygroup_rule(self):
        """
        test case for update_enterprise_securitygroup_rule
        """
        res = self.the_client.update_enterprise_security_group_rule(enterprise_security_group_rule_id=esg_rule_id,
                                                                    remark='test')
        print(res)
        self.assertEqual(type(res), baidubce.bce_response.BceResponse)

    def test_delete_enterprise_securitygroup(self):
        """
        test case for delete_enterprise_securitygroup
        """
        res = self.the_client.delete_enterprise_security_group(esg_id)
        print(res)
        self.assertEqual(type(res), baidubce.bce_response.BceResponse)

if __name__ == "__main__":
    suite = unittest.TestSuite()
    # suite.addTest(TestEsgClient("test_create_enterprise_securitygroup"))
    # suite.addTest(TestEsgClient("test_authorize_enterprise_securitygroup_rule"))
    # suite.addTest(TestEsgClient("test_delete_enterprise_securitygroup_rule"))
    # suite.addTest(TestEsgClient("test_update_enterprise_securitygroup_rule"))
    # suite.addTest(TestEsgClient("test_delete_enterprise_securitygroup"))
    suite.addTest(TestEsgClient("test_get_enterprise_securitygrouplist"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
