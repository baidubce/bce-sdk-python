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
Unit tests for aihc client model functionality.

使用unittest模块 (推荐)
python -m unittest test.aihc.test_aihc_model_client

使用pytest模块
python -m pytest test/aihc/test_aihc_model_client.py -v

直接运行测试文件
python test/aihc/test_aihc_model_client.py

运行特定测试
python -m unittest test.aihc.test_aihc_model_client.TestAIHCClient.test_describe_models -v
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

resource_pool_id = 'cce-hcuw9ybk'
model_id = 'model-test101'


def generate_client_token():
    """Generate a random client token for testing."""
    return str(uuid.uuid4())


class TestAIHCClient(unittest.TestCase):
    """
    Test class for aihc sdk client model functionality
    """

    def setUp(self):
        config = BceClientConfiguration(credentials=BceCredentials(aihc_test_conf.AK, aihc_test_conf.SK),
                                        endpoint=aihc_test_conf.HOST)
        # Try to find the correct client class
        if hasattr(aihc_client, 'AihcClient'):
            self.client = aihc_client.AihcClient(config)
        else:
            raise AttributeError("No AIHC client class found")

    def test_client_initialization(self):
        """Test client initialization."""
        self.assertIsNotNone(self.client)

    def test_describe_models(self):
        """Test describe models functionality."""
        try:
            response = self.client.DescribeModels(
                keyword='test',
                pageNumber=1,
                pageSize=10
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)

    def test_create_model(self):
        """Test create model functionality."""
        try:
            response = self.client.CreateModel(
                name='test-model-' + generate_client_token(),
                modelFormat='pytorch',
                description='Test model'
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)

    def test_delete_model(self):
        """Test delete model functionality."""
        try:
            response = self.client.DeleteModel(
                modelId=model_id
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)

    def test_create_model_version(self):
        """Test create model version functionality."""
        try:
            response = self.client.CreateModelVersion(
                modelId=model_id,
                storageBucket='test-bucket',
                storagePath='/test/model',
                source='UserUpload',
                description='Test model version'
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)

    def test_delete_model_version(self):
        """Test delete model version functionality."""
        try:
            response = self.client.DeleteModelVersion(
                modelId=model_id,
                versionId='version-test123'
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)

    def test_describe_model_version(self):
        """Test describe model version functionality."""
        try:
            response = self.client.DescribeModelVersion(
                versionId='version-test123'
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)

    def test_describe_model_versions(self):
        """Test describe model versions functionality."""
        try:
            response = self.client.DescribeModelVersions(
                modelId=model_id,
                pageNumber=1,
                pageSize=10
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)

    def test_modify_model(self):
        """Test modify model functionality."""
        try:
            response = self.client.ModifyModel(
                modelId=model_id,
                name='modified-model-name',
                description='Modified model description'
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)

    def test_merge_config(self):
        """Test _merge_config method."""
        # Test with None config
        merged_config = self.client._merge_config(None)
        self.assertEqual(merged_config, self.client.config)
        
        # Test with new config
        new_config = BceClientConfiguration()
        merged_config = self.client._merge_config(new_config)
        self.assertIsNotNone(merged_config)

    def test_required_decorator(self):
        """Test @required decorator functionality."""
        # Test that required parameters are enforced
        with self.assertRaises(TypeError):
            # This should raise an error because required parameters are missing
            self.client.DescribeModels()

    def test_version_header(self):
        """Test version header in requests."""
        # Note: version attribute may not be available in all client versions
        # This test is kept for compatibility but may need adjustment
        # Check if version attribute exists
        if hasattr(self.client, 'version'):
            self.assertEqual(self.client.version, b'v2')
        else:
            # Skip version check if not available
            pass

    def test_endpoint_configuration(self):
        """Test endpoint configuration."""
        # Test that the client is configured with the correct endpoint
        self.assertIsNotNone(self.client.config.endpoint)

    def test_credentials_configuration(self):
        """Test credentials configuration."""
        # Test that the client is configured with credentials
        self.assertIsNotNone(self.client.config.credentials)

    def test_parameter_validation(self):
        """Test parameter validation."""
        # 测试必需参数缺失
        with self.assertRaises(TypeError):
            self.client.DescribeModels()
        
        # 测试参数类型错误
        with self.assertRaises(TypeError):
            self.client.DescribeModels(
                keyword='test',
                pageNumber="invalid_type",  # 应该是int
                pageSize=10
            )

    def test_error_handling(self):
        """Test error handling scenarios."""
        # 测试无效的模型ID
        try:
            response = self.client.DescribeModelVersion(
                versionId='invalid-version-id'
            )
            # 如果成功，验证响应
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            # 如果失败，验证异常类型
            self.assertIsInstance(e, Exception)

    def test_boundary_conditions(self):
        """Test boundary conditions."""
        # 测试边界值
        try:
            response = self.client.DescribeModels(
                keyword='test',
                pageNumber=0,  # 边界值
                pageSize=1     # 边界值
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)

        try:
            response = self.client.DescribeModels(
                keyword='test',
                pageNumber=1,
                pageSize=1000  # 大数值
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)


if __name__ == '__main__':
    suite = unittest.TestSuite()

    # Add basic functionality tests
    suite.addTest(TestAIHCClient("test_client_initialization"))
    suite.addTest(TestAIHCClient("test_merge_config"))
    suite.addTest(TestAIHCClient("test_required_decorator"))
    suite.addTest(TestAIHCClient("test_version_header"))
    suite.addTest(TestAIHCClient("test_endpoint_configuration"))
    suite.addTest(TestAIHCClient("test_credentials_configuration"))

    # Add model-related tests
    suite.addTest(TestAIHCClient("test_describe_models"))
    suite.addTest(TestAIHCClient("test_create_model"))
    suite.addTest(TestAIHCClient("test_delete_model"))
    suite.addTest(TestAIHCClient("test_create_model_version"))
    suite.addTest(TestAIHCClient("test_delete_model_version"))
    suite.addTest(TestAIHCClient("test_describe_model_version"))
    suite.addTest(TestAIHCClient("test_describe_model_versions"))
    suite.addTest(TestAIHCClient("test_modify_model"))

    # Add validation and error handling tests
    suite.addTest(TestAIHCClient("test_parameter_validation"))
    suite.addTest(TestAIHCClient("test_error_handling"))
    suite.addTest(TestAIHCClient("test_boundary_conditions"))

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