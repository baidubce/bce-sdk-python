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
from typing import Any, Dict, Optional, Union, List, get_type_hints

from baidubce.services.aihc.modules.job.job_client import JobClient
from baidubce.services.aihc.modules.dataset.dataset_client import DatasetClient
from baidubce.services.aihc.modules.model.model_client import ModelClient
from baidubce.services.aihc.modules.service.service_client import ServiceClient
from baidubce.services.aihc.modules.dev_instance.dev_instance_client import DevInstanceClient
from baidubce.services.aihc.modules.resource_pool.resource_pool_client import ResourcePoolClient


def create_typed_proxy_method(target_client, method_name):
    """
    创建带有完整类型信息的代理方法
    
    这个函数会：
    1. 获取原始方法的完整签名和类型注解
    2. 创建一个新的代理方法，保持所有类型信息
    3. 确保IDE能够正确识别类型提示
    """
    original_method = getattr(target_client, method_name)
    
    # 获取原始方法的完整信息
    sig = inspect.signature(original_method)
    
    # 创建代理方法
    @wraps(original_method)
    def proxy_method(*args, **kwargs):
        """
        代理方法，用于调用原始目标方法并保持类型信息
        """
        return original_method(*args, **kwargs)
    
    # 设置完整的类型信息
    proxy_method.__signature__ = sig
    proxy_method.__annotations__ = original_method.__annotations__
    
    # 确保IDE能够识别类型信息
    if hasattr(original_method, '__module__'):
        proxy_method.__module__ = original_method.__module__
    if hasattr(original_method, '__qualname__'):
        proxy_method.__qualname__ = original_method.__qualname__
    if hasattr(original_method, '__name__'):
        proxy_method.__name__ = original_method.__name__
    
    # 使用 typing.get_type_hints 确保类型信息正确
    try:
        type_hints = get_type_hints(original_method)
        proxy_method.__annotations__ = type_hints
    except Exception:
        # 如果获取类型提示失败，使用原始注解
        proxy_method.__annotations__ = original_method.__annotations__
    
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
        self.job = JobClient(config)
        self.dataset = DatasetClient(config)
        self.model = ModelClient(config)
        self.service = ServiceClient(config)
        self.dev_instance = DevInstanceClient(config)
        self.resource_pool = ResourcePoolClient(config)
        
        # 动态创建代理方法
        self._setup_proxy_methods()

    def _setup_proxy_methods(self):
        """
        设置代理方法
        
        为各个子模块的方法创建代理，使主客户端可以直接调用子模块的方法
        """
        # 任务相关接口
        job_methods = [
            'DescribeJobs', 'DescribeJob', 'DeleteJob', 'ModifyJob',
            'DescribeJobEvents', 'DescribeJobLogs', 'DescribeJobPodEvents',
            'StopJob', 'DescribeJobNodes', 'DescribeJobWebterminal', 'CreateJob',
            'DescribeJobMetrics'
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
            'DescribeServices', 'DescribeService', 'DescribeServiceStatus',
            'CreateService', 'DeleteService', 'ModifyService', 'ModifyServiceReplicas', 'UpgradeService',
            'DescribeServicePods', 'DeleteServicePod', 'DisableServicePod', 'ModifyServiceNetConfig',
            'DescribeServicePodGroups', 'DescribeServiceChangelogs', 'DescribeServiceChangelog'
        ]
        
        # 开发机相关接口
        dev_instance_methods = [
            'DescribeDevInstances', 'DescribeDevInstance', 'StartDevInstance', 'StopDevInstance',
            'CreateDevInstance', 'DeleteDevInstance', 'ModifyDevInstance',
            'DescribeDevInstanceEvents', 'CreateDevInstanceImagePackJob', 
            'DescribeDevInstanceImagePackJob', 'TimedStopDevInstance'
        ]
        
        # 资源池相关接口
        resource_pool_methods = [
            'DescribeResourcePools', 'DescribeResourcePool', 'DescribeResourcePoolOverview',
            'DescribeResourcePoolConfiguration', 'DescribeQueues', 'DescribeQueue'
        ]
        
        # 为每个方法创建代理
        for method_name in job_methods:
            setattr(self, method_name, create_typed_proxy_method(self.job, method_name))
        
        for method_name in dataset_methods:
            setattr(self, method_name, create_typed_proxy_method(self.dataset, method_name))
        
        for method_name in model_methods:
            setattr(self, method_name, create_typed_proxy_method(self.model, method_name))
        
        for method_name in service_methods:
            setattr(self, method_name, create_typed_proxy_method(self.service, method_name))
        
        for method_name in dev_instance_methods:
            setattr(self, method_name, create_typed_proxy_method(self.dev_instance, method_name))
        
        for method_name in resource_pool_methods:
            setattr(self, method_name, create_typed_proxy_method(self.resource_pool, method_name))
