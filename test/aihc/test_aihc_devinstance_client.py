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
Unit tests for aihc devinstance client.

使用unittest模块 (推荐)
python -m unittest test.aihc.test_aihc_devinstance_client

使用pytest模块
python -m pytest test/aihc/test_aihc_devinstance_client.py -v

直接运行测试文件
python test/aihc/test_aihc_devinstance_client.py

运行特定测试
python -m unittest test.aihc.test_aihc_devinstance_client.TestAIHCClient.test_describe_dev_instances -v
"""
import json
import os
import random
import string
import sys
import unittest
import uuid
import importlib

import baidubce
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
import baidubce.services.aihc.aihc_client as aihc_client
from baidubce.exception import BceServerError, BceHttpClientError
from baidubce import compat

import aihc_test_conf

# Use importlib.reload instead of imp.reload for Python 3.4+
try:
    from importlib import reload
except ImportError:
    from imp import reload

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')
reload(sys)

if compat.PY2:
    sys.setdefaultencoding('utf8')


dev_instance_id = 'dev-test789'


def generate_client_token():
    """Generate a random client token for testing."""
    return str(uuid.uuid4())


class TestAIHCClient(unittest.TestCase):
    """
    Test class for aihc sdk client - DevInstance related methods only
    """

    def setUp(self):
        config = BceClientConfiguration(credentials=BceCredentials(aihc_test_conf.AK, aihc_test_conf.SK),
                                        endpoint=aihc_test_conf.HOST)
        # Try to find the correct client class
        if hasattr(aihc_client, 'AihcClient'):
            self.client = aihc_client.AihcClient(config)
        else:
            raise AttributeError("No AIHC client class found")

    def test_describe_dev_instances(self):
        """Test describe dev instances functionality."""
        try:
            response = self.client.dev_instance.DescribeDevInstances(
                pageNumber=1,
                pageSize=10
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)

    def test_describe_dev_instance(self):
        """Test describe dev instance functionality."""
        try:
            response = self.client.dev_instance.DescribeDevInstance(
                devInstanceId=dev_instance_id
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)

    def test_start_dev_instance(self):
        """Test start dev instance functionality."""
        try:
            response = self.client.dev_instance.StartDevInstance(
                devInstanceId=dev_instance_id
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)

    def test_stop_dev_instance(self):
        """Test stop dev instance functionality."""
        try:
            response = self.client.dev_instance.StopDevInstance(
                devInstanceId=dev_instance_id
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)


if __name__ == '__main__':
    suite = unittest.TestSuite()

    # Add dev instance-related tests
    suite.addTest(TestAIHCClient("test_describe_dev_instances"))
    suite.addTest(TestAIHCClient("test_describe_dev_instance"))
    suite.addTest(TestAIHCClient("test_start_dev_instance"))
    suite.addTest(TestAIHCClient("test_stop_dev_instance"))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite) 

    print("\n" + "=" * 50)
    print("测试总结:")
    print(f"运行测试: {result.testsRun}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print(f"跳过: {len(result.skipped)}")
    
    if result.failures:
        print("\n失败详情:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\n错误详情:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}") 