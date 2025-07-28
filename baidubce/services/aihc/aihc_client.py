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
This module provides a client class for AIHC V2.
"""
import inspect
from functools import wraps
from typing import Any, Dict, Optional, Union, List

from baidubce.services.aihc.modules.job.job_client import JobClient
from baidubce.services.aihc.modules.dataset.dataset_client import DatasetClient
from baidubce.services.aihc.modules.model.model_client import ModelClient
from baidubce.services.aihc.modules.service.service_client import ServiceClient
from baidubce.services.aihc.modules.dev_instance.dev_instance_client import DevInstanceClient


def _create_proxy_method(target_client, method_name):
    """创建代理方法，保持原始文档字符串和签名"""
    original_method = getattr(target_client, method_name)
    
    @wraps(original_method)
    def proxy_method(*args, **kwargs):
        return original_method(*args, **kwargs)
    
    return proxy_method


class AihcClient:
    """
    AIHC主客户端，适配V2版本OpenAPI
    
    该客户端提供了对AIHC各个模块功能的统一访问接口，
    包括任务管理、数据集管理、模型管理、在线服务和开发机管理等功能。
    
    使用示例:
        >>> from baidubce.services.aihc.aihc_client import AihcClient
        >>> client = AihcClient(config)
        >>> jobs = client.DescribeJobs(resourcePoolId="xxx")
    """

    def __init__(self, config=None):
        """
        初始化AIHC V2客户端
        
        Args:
            config: 配置对象
                baidubce.bce_client_configuration.BceClientConfiguration实例
        """
        self.job_client = JobClient(config)
        self.dataset_client = DatasetClient(config)
        self.model_client = ModelClient(config)
        self.service_client = ServiceClient(config)
        self.dev_instance_client = DevInstanceClient(config)
        
        # 动态创建代理方法
        self._setup_proxy_methods()

    def _setup_proxy_methods(self):
        """设置代理方法"""
        # 任务相关接口
        job_methods = [
            'DescribeJobs', 'DescribeJob', 'DeleteJob', 'ModifyJob', 
            'DescribeJobEvents', 'DescribeJobLogs', 'DescribeJobPodEvents',
            'StopJob', 'DescribeJobNodeNames', 'GetJobWebTerminalUrl', 'CreateJob'
        ]
        
        # 数据集相关接口
        dataset_methods = [
            'DescribeDatasets', 'DescribeDataset', 'ModifyDataset', 'DeleteDataset',
            'CreateDataset', 'DescribeDatasetVersions', 'DescribeDatasetVersion',
            'DeleteDatasetVersion', 'CreateDatasetVersion'
        ]
        
        # 模型相关接口
        model_methods = [
            'DescribeModels', 'CreateModel', 'DeleteModel', 'ModifyModel',
            'DescribeModel', 'DescribeModelVersions', 'DescribeModelVersion',
            'CreateModelVersion', 'DeleteModelVersion'
        ]
        
        # 在线服务相关接口
        service_methods = [
            'DescribeServices', 'DescribeService', 'DescribeServiceStatus'
        ]
        
        # 开发机相关接口
        dev_instance_methods = [
            'DescribeDevInstances', 'DescribeDevInstance', 'StartDevInstance', 'StopDevInstance'
        ]
        
        # 为每个方法创建代理
        for method_name in job_methods:
            setattr(self, method_name, _create_proxy_method(self.job_client, method_name))
        
        for method_name in dataset_methods:
            setattr(self, method_name, _create_proxy_method(self.dataset_client, method_name))
        
        for method_name in model_methods:
            setattr(self, method_name, _create_proxy_method(self.model_client, method_name))
        
        for method_name in service_methods:
            setattr(self, method_name, _create_proxy_method(self.service_client, method_name))
        
        for method_name in dev_instance_methods:
            setattr(self, method_name, _create_proxy_method(self.dev_instance_client, method_name)) 