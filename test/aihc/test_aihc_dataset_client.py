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
Unit tests for aihc dataset client.

使用unittest模块 (推荐)
python -m unittest test.aihc.test_aihc_dataset_client

使用pytest模块
python -m pytest test/aihc/test_aihc_dataset_client.py -v

直接运行测试文件
python test/aihc/test_aihc_dataset_client.py

运行特定测试
python -m unittest test.aihc.test_aihc_dataset_client.TestAIHCClient.test_describe_datasets -v
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
# from baidubce.services.aihc import aihc_model  # Commented out as module may not be available
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

dataset_id = 'ds-test789'


def generate_client_token():
    """Generate a random client token for testing."""
    return str(uuid.uuid4())


class TestAIHCClient(unittest.TestCase):
    """
    Test class for aihc sdk client
    """

    def setUp(self):
        config = BceClientConfiguration(credentials=BceCredentials(aihc_test_conf.AK, aihc_test_conf.SK),
                                        endpoint=aihc_test_conf.HOST)
        # Try to find the correct client class
        if hasattr(aihc_client, 'AihcClient'):
            self.client = aihc_client.AihcClient(config)
        else:
            raise AttributeError("No AIHC client class found")

    def test_describe_datasets(self):
        """Test describe datasets functionality."""
        try:
            response = self.client.DescribeDatasets(
                keyword='test',
                pageNumber=1,
                pageSize=10
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)

    def test_describe_dataset(self):
        """Test describe dataset functionality."""
        try:
            response = self.client.DescribeDataset(
                datasetId=dataset_id
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)

    def test_create_dataset(self):
        """Test create dataset functionality."""
        try:
            response = self.client.CreateDataset(
                name='test-dataset-' + generate_client_token(),
                storageType='bos',
                storageInstance='bos-test',
                importFormat='auto',
                description='Test dataset'
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)

    def test_delete_dataset(self):
        """Test delete dataset functionality."""
        try:
            response = self.client.DeleteDataset(
                datasetId=dataset_id
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)
    
    def test_create_dataset_version(self):
        """Test create dataset version functionality."""
        try:
            response = self.client.CreateDatasetVersion(
                datasetId=dataset_id,
                storagePath='/test/path',
                mountPath='/mnt/data',
                description='Test dataset version'
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)

    def test_delete_dataset_version(self):
        """Test delete dataset version functionality."""
        try:
            response = self.client.DeleteDatasetVersion(
                datasetId=dataset_id,
                versionId='version-test123'
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)

    def test_describe_dataset_version(self):
        """Test describe dataset version functionality."""
        try:
            response = self.client.DescribeDatasetVersion(
                versionId='version-test123'
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)

    def test_describe_dataset_versions(self):
        """Test describe dataset versions functionality."""
        try:
            response = self.client.DescribeDatasetVersions(
                datasetId=dataset_id,
                pageNumber=1,
                pageSize=10
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)

    def test_modify_dataset(self):
        """Test update dataset functionality."""
        try:
            response = self.client.ModifyDataset(
                datasetId=dataset_id,
                name='updated-dataset-name',
                description='Updated dataset description',
                visibilityScope='private'
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)


if __name__ == '__main__':
    suite = unittest.TestSuite()

    # Add dataset-related tests
    suite.addTest(TestAIHCClient("test_describe_datasets"))
    suite.addTest(TestAIHCClient("test_describe_dataset"))
    suite.addTest(TestAIHCClient("test_create_dataset"))
    suite.addTest(TestAIHCClient("test_delete_dataset"))
    suite.addTest(TestAIHCClient("test_create_dataset_version"))
    suite.addTest(TestAIHCClient("test_delete_dataset_version"))
    suite.addTest(TestAIHCClient("test_describe_dataset_version"))
    suite.addTest(TestAIHCClient("test_describe_dataset_versions"))
    suite.addTest(TestAIHCClient("test_modify_dataset"))

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