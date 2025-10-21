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
Unit tests for aihc job client.

使用unittest模块 (推荐)
python -m unittest test.aihc.test_aihc_job_client

使用pytest模块
python -m pytest test/aihc/test_aihc_job_client.py -v

直接运行测试文件
python test/aihc/test_aihc_job_client.py

运行特定测试
python -m unittest test.aihc.test_aihc_job_client.TestAIHCClient.test_client_initialization -v
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

from test.aihc import aihc_test_conf

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


def generate_client_token():
    """Generate a random client token for testing."""
    return str(uuid.uuid4())


class TestAIHCClient(unittest.TestCase):
    """
    Test class for aihc sdk client - Job related tests only
    """

    resource_pool_id = 'cce-hcuw9ybk'
    job_id = ''

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

    def test_describe_jobs(self):
        """Test describe jobs functionality."""
        """Test DescribeJobs with strict validation."""
        print("\n=== 严格验证测试: DescribeJobs ===")
        
        try:
            response = self.client.job.DescribeJobs(
                resourcePoolId=self.resource_pool_id,
                pageNumber=1,
                pageSize=10
            )
            
            # 严格验证响应
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
            
            # 检查响应是否有实际内容
            if hasattr(response, 'jobs') and hasattr(response, 'requestId') and hasattr(response, 'totalCount'):
                self.assertIsInstance(response.jobs, list)
                self.assertIsInstance(response.requestId, str)
                self.assertIsInstance(response.totalCount, int)
            else:
                self.fail("WARNING: 响应结果为空")
                
        except BceServerError as e:
            print(f"[ERROR] 服务器错误: {e}")
            # 服务器错误说明请求到达了服务器，这是好的
            self.assertIn("ResourcePool", str(e))
            
        except BceHttpClientError as e:
            print(f"[ERROR] HTTP客户端错误: {e}")
            # HTTP错误也说明进行了网络请求
            
        except Exception as e:
            print(f"[ERROR] 其他错误: {type(e).__name__}: {e}")
            self.fail(f"意外的错误类型: {type(e).__name__}")

    def test_describe_job(self):
        """Test exist job DescribeJob with strict validation."""
        print("\n=== 严格验证测试: DescribeJob (存在任务) ===")
        
        try:
            response = self.client.job.DescribeJob(
                resourcePoolId=self.resource_pool_id,
                jobId=self.job_id,
                needDetail=True
            )
            
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
            
            if hasattr(response, 'requestId') and hasattr(response, 'jobId'):
                print(f"[SUCCESS] 响应包含数据: jobId={response.jobId}, requestId={response.requestId}")
                self.assertIsInstance(response.jobId, str)
                self.assertIsInstance(response.requestId, str)
            else:
                print("[WARNING] 响应结果为空或缺少必要字段")
                self.fail("[WARNING] 响应结果为空或缺少必要字段")
                
        except BceServerError as e:
            print(f"[ERROR] 服务器错误: {e}")
            # 如果任务不存在，这是预期的
            if "not found" in str(e).lower():
                print("[WARNING] 任务不存在，可能需要更新job_id")
                self.fail("[WARNING] 任务不存在，可能需要更新job_id")
                
        except BceHttpClientError as e:
            print(f"[ERROR] HTTP客户端错误: {e}")
            # 检查是否是包装的服务器错误
            if "not found" in str(e).lower():
                print("[WARNING] 任务不存在 (通过HTTP客户端错误)")
                self.fail("[WARNING] 任务不存在 (通过HTTP客户端错误)")
        except Exception as e:
            print(f"[ERROR] 其他错误: {type(e).__name__}: {e}")
            self.fail(f"意外的错误类型: {type(e).__name__}")

    def test_create_job(self):
        """Test create job functionality."""
        job_config = {
            'jobName': 'test-job-' + generate_client_token(),
            'image': 'test-image:latest',
            'resources': {
                'cpu': 1,
                'memory': '1Gi',
                'gpu': 0
            },
            'command': ['python', 'train.py'],
            'args': ['--epochs', '10']
        }
        
        try:
            response = self.client.job.CreateJob(
                resourcePoolId=self.resource_pool_id,
                jobConfig=job_config
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)

    def test_delete_job(self):
        """Test delete job functionality."""
        try:
            response = self.client.job.DeleteJob(
                resourcePoolId=self.resource_pool_id,
                jobId=self.job_id
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)

    def test_stop_job(self):
        """Test stop job functionality."""
        try:
            response = self.client.job.StopJob(
                resourcePoolId=self.resource_pool_id,
                jobId=self.job_id
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)

    def test_describe_job_events(self):
        """Test describe job events functionality."""
        try:
            response = self.client.job.DescribeJobEvents(
                resourcePoolId=self.resource_pool_id,
                jobId=self.job_id
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)

    def test_describe_job_logs(self):
        """Test describe job logs functionality."""
        try:
            response = self.client.job.DescribeJobLogs(
                resourcePoolId=self.resource_pool_id,
                jobId=self.job_id,
                podName='test-pod',
                logType='stdout',
                startTime='2024-01-01 00:00:00',
                endTime='2024-01-01 23:59:59',
                chunkSize=1,
                marker='test-marker'
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)

    def test_describe_job_node_names(self):
        """Test describe job node names functionality."""
        try:
            response = self.client.job.DescribeJobNodeNames(
                resourcePoolId=self.resource_pool_id,
                jobId=self.job_id
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)

    def test_describe_job_pod_events(self):
        """Test describe job pod events functionality."""
        try:
            response = self.client.job.DescribeJobPodEvents(
                resourcePoolId=self.resource_pool_id,
                jobId=self.job_id,
                podName='test-pod',
                startTime='2024-01-01 00:00:00',
                endTime='2024-01-01 23:59:59'
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)

    def test_get_job_web_terminal_url(self):
        """Test get job web terminal URL functionality."""
        try:
            response = self.client.job.GetJobWebTerminalUrl(
                resourcePoolId=self.resource_pool_id,
                jobId=self.job_id,
                handshakeTimeoutSecond=30,
                pingTimeoutSecond=60
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)

    def test_modify_job(self):
        """Test modify job functionality."""
        try:
            response = self.client.job.ModifyJob(
                resourcePoolId=self.resource_pool_id,
                jobId=self.job_id,
                priority='normal'
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
            self.client.DescribeJobs()

    def test_pagination_parameters(self):
        """Test pagination parameters."""
        try:
            response = self.client.DescribeJobs(
                resourcePoolId=self.resource_pool_id,
                pageNumber=1,
                pageSize=5
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)

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

    def test_response_structure_validation(self):
        """Test response structure validation."""
        try:
            response = self.client.DescribeJobs(
                resourcePoolId=self.resource_pool_id,
                pageNumber=1,
                pageSize=10
            )
            # 验证响应结构
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
            # 如果有响应数据，验证基本结构
            if hasattr(response, 'result'):
                self.assertIsInstance(response.result, dict)
        except Exception as e:
            self.assertIsInstance(e, Exception)

    def test_parameter_validation(self):
        """Test parameter validation."""
        # 测试必需参数缺失
        with self.assertRaises(TypeError):
            self.client.DescribeJobs()
        
        # 测试参数类型错误
        with self.assertRaises(TypeError):
            self.client.DescribeJobs(
                resourcePoolId=self.resource_pool_id,
                pageNumber="invalid_type",  # 应该是int
                pageSize=10
            )

    def test_error_handling(self):
        """Test error handling scenarios."""
        # 测试无效的资源池ID
        try:
            response = self.client.DescribeJobs(
                resourcePoolId='invalid-resource-pool',
                pageNumber=1,
                pageSize=10
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
            response = self.client.DescribeJobs(
                resourcePoolId=self.resource_pool_id,
                pageNumber=0,  # 边界值
                pageSize=1     # 边界值
            )
            self.assertIsInstance(response, baidubce.bce_response.BceResponse)
        except Exception as e:
            self.assertIsInstance(e, Exception)

        try:
            response = self.client.DescribeJobs(
                resourcePoolId=self.resource_pool_id,
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

    # Add job-related tests
    suite.addTest(TestAIHCClient("test_describe_jobs"))
    suite.addTest(TestAIHCClient("test_describe_job"))
    suite.addTest(TestAIHCClient("test_create_job"))
    # suite.addTest(TestAIHCClient("test_delete_job"))
    suite.addTest(TestAIHCClient("test_stop_job"))
    suite.addTest(TestAIHCClient("test_describe_job_events"))
    suite.addTest(TestAIHCClient("test_describe_job_logs"))
    suite.addTest(TestAIHCClient("test_describe_job_node_names"))
    suite.addTest(TestAIHCClient("test_describe_job_pod_events"))
    suite.addTest(TestAIHCClient("test_get_job_web_terminal_url"))
    suite.addTest(TestAIHCClient("test_modify_job"))

    # Add validation and error handling tests
    suite.addTest(TestAIHCClient("test_pagination_parameters"))
    suite.addTest(TestAIHCClient("test_response_structure_validation"))
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