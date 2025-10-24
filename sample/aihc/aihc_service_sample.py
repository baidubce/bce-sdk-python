# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
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
AIHC客户端示例模块。

本模块提供了百度云AIHC服务的完整使用示例，包括：
- 服务管理：查询服务列表、服务详情、创建、更新、删除服务
- 错误处理：演示如何处理BCE客户端和服务器错误

主要功能：
1. 演示AihcClient的基本使用方法
2. 展示各种API调用的正确方式
3. 提供完整的错误处理示例
4. 展示响应数据的处理方式

使用前请确保：
- 已正确配置aihc_sample_conf.py中的认证信息
- 有相应的AIHC服务权限
- 网络连接正常

示例：
    python aihc_service_sample.py

    python -m sample.aihc.aihc_service_sample -v
"""

# !/usr/bin/env python
# coding=utf-8
import json
import logging

from baidubce.exception import BceHttpClientError, BceServerError
from baidubce.services.aihc.aihc_client import AihcClient
from baidubce.services.aihc.modules.service.service_model import ResourcePoolConf, ImageConf, ContainerConf, ServiceConf
from baidubce.services.aihc.modules.service.service_model import ModifyServiceConf

import sample.aihc.aihc_sample_conf as aihc_sample_conf

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', force=True)
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("baidubce").setLevel(logging.INFO)
__logger = logging.getLogger(__name__)
__logger.setLevel(logging.INFO)


def to_dict(obj):
    """
    将对象转换为字典格式。
    
    递归地将Python对象（包括自定义对象、字典、列表）转换为纯字典格式，
    便于JSON序列化和调试输出。
    
    Args:
        obj: 要转换的对象，可以是字典、列表、自定义对象或基本类型
        
    Returns:
        dict/list/基本类型: 转换后的字典、列表或基本类型值
        
    Examples:
        >>> obj = SomeClass()
        >>> obj.name = "test"
        >>> result = to_dict(obj)
        >>> print(result)
        {'name': 'test'}
    """
    if isinstance(obj, dict):
        return {k: to_dict(v) for k, v in obj.items()}
    elif hasattr(obj, '__dict__'):
        return {k: to_dict(v) for k, v in obj.__dict__.items()}
    elif isinstance(obj, list):
        return [to_dict(i) for i in obj]
    else:
        return obj


def main():
    """
    主函数，演示AIHC服务的各种操作。
    
    本函数展示了AihcClient的完整使用流程，包括：
    1. 创建AIHC客户端实例
    2. 查询任务列表和详情
    3. 查询各种资源列表（数据集、模型、服务、开发机）
    4. 完整的错误处理机制
    
    注意：
    - 部分功能（如创建、升级、删除服务等）被注释掉，避免误操作
    - 所有API调用都包含完整的异常处理
    - 响应数据会被转换为JSON格式输出
    
    Raises:
        BceHttpClientError: 当API调用失败时抛出
        BceServerError: 当服务器返回错误时抛出
    """
    # create a aihc client
    aihc_client = AihcClient(aihc_sample_conf.config)
    
    # 初始化变量
    service_id = None

    # 查询服务列表
    try:
        __logger.info('--------------------------------DescribeServices start...--------------------------------')
        response = aihc_client.service.DescribeServices()
        print(json.dumps(to_dict(response), ensure_ascii=False))
        __logger.info('DescribeServices: %s', response.__dict__.keys())

        # 获取第一个服务ID用于后续操作
        if hasattr(response, 'services') and response.services is not None and len(response.services) > 0:
            service_id = response.services[0].id

    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # 查询服务详情
    if service_id:
        try:
            __logger.info('--------------------------------DescribeService start...--------------------------------')
            response = aihc_client.service.DescribeService(serviceId=service_id)
            print(json.dumps(to_dict(response), ensure_ascii=False))
            __logger.info('DescribeService: %s', response.__dict__.keys())
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                __logger.error('send request failed. Response %s, code: %s, msg: %s'
                               % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
            else:
                __logger.error('send request failed. Unknown exception: %s' % e)

    # 查询服务状态
    if service_id:
        try:
            __logger.info('--------------------------------DescribeServiceStatus start...--------------------------------')
            response = aihc_client.service.DescribeServiceStatus(serviceId=service_id)
            print(json.dumps(to_dict(response), ensure_ascii=False))
            __logger.info('DescribeServiceStatus: %s', response.__dict__.keys())
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                __logger.error('send request failed. Response %s, code: %s, msg: %s'
                               % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
            else:
                __logger.error('send request failed. Unknown exception: %s' % e)

    # 查询服务Pod列表
    if service_id:
        try:
            __logger.info('--------------------------DescribeServicePods start...--------------------------------')
            response = aihc_client.service.DescribeServicePods(serviceId=service_id)
            print(json.dumps(to_dict(response), ensure_ascii=False))
            __logger.info('DescribeServicePods: %s', response.__dict__.keys())
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                __logger.error('send request failed. Response %s, code: %s, msg: %s'
                               % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
            else:
                __logger.error('send request failed. Unknown exception: %s' % e)

    # 获取实例组列表
    if service_id:
        try:
            __logger.info('-------------------DescribeServicePodGroups start...--------------------------------')
            response = aihc_client.service.DescribeServicePodGroups(serviceId=service_id)
            print(json.dumps(to_dict(response), ensure_ascii=False))
            __logger.info('DescribeServicePodGroups: %s', response.__dict__.keys())
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                __logger.error('send request failed. Response %s, code: %s, msg: %s'
                               % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
            else:
                __logger.error('send request failed. Unknown exception: %s' % e)

    # 查询服务变更记录
    if service_id:
        try:
            __logger.info('----------------------DescribeServiceChangelogs start...--------------------------------')
            response = aihc_client.service.DescribeServiceChangelogs(serviceId=service_id)
            print(json.dumps(to_dict(response), ensure_ascii=False))
            __logger.info('DescribeServiceChangelogs: %s', response.__dict__.keys())
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                __logger.error('send request failed. Response %s, code: %s, msg: %s'
                               % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
            else:
                __logger.error('send request failed. Unknown exception: %s' % e)

    # # 创建服务
    # try:
    #     __logger.info('--------------------------------CreateService start...--------------------------------')
    #     resource_pool_conf = ResourcePoolConf(
    #         resourcePoolId="cce-xxx",
    #         queueName='default',
    #         resourcePoolType="",
    #         resourcePoolName="pool-xxx"
    #     )
    #     image_conf = ImageConf(
    #         imageType=1,
    #         imageUrl="registry.baidubce.com/csm-online/sglang-router:0.2.0",
    #     )
    #     containers = [ContainerConf(
    #             name="container-test",
    #             cpus=16,
    #             memory=64,
    #             acceleratorCount=1,
    #             image=image_conf,
    #             command=[
    #                 "python",
    #                 "-m",
    #                 "sglang_router.launch_router",
    #                 "--enable-igw",
    #                 "--pd-disaggregation",
    #                 "--service-discovery",
    #                 "--prefill-selector",
    #                 "pom.aihc.baidubce.com/app-name=sglang-p-test",
    #                 "--decode-selector",
    #                 "pom.aihc.baidubce.com/app-name=sglang-d-test",
    #                 "--service-discovery-namespace",
    #                 "aihc-pom",
    #                 "--service-discovery-port",
    #                 "9000",
    #                 "--prefill-policy",
    #                 "cache_aware",
    #                 "--decode-policy",
    #                 "round_robin",
    #                 "--host",
    #                 "0.0.0.0",
    #                 "--port",
    #                 "30000"
    #             ],
    #         )]
    #     response = aihc_client.service.CreateService(
    #         serviceConf={
    #             "name": "pythonsdk-aihc-service-test-xxx",
    #             "acceleratorType": "NVIDIA H20-3e",
    #             "workloadType": "",
    #             "instanceCount": 1,
    #             "resourcePool": resource_pool_conf,
    #             "containers": containers
    #         }
    #     )
    #     print(json.dumps(to_dict(response), ensure_ascii=False))
    #     __logger.info('CreateService: %s', response.__dict__.keys())
    # except BceHttpClientError as e:
    #     if isinstance(e.last_error, BceServerError):
    #         __logger.error('send request failed. Response %s, code: %s, msg: %s'
    #                        % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
    #     else:
    #         __logger.error('send request failed. Unknown exception: %s' % e)
    #
    # # 升级在线服务
    # try:
    #     __logger.info('--------------------------------ModifyService start...--------------------------------')
    #     resource_pool_conf = ResourcePoolConf(
    #         resourcePoolId="cce-xxx",
    #         queueName='default',
    #         resourcePoolType="",
    #         resourcePoolName="xxxx"
    #     )
    #     service_conf = ModifyServiceConf(
    #         name="service-xxx-test-20251027",
    #         acceleratorType="NVIDIA H20-3e",
    #         instanceCount=3,
    #         resourcePool=resource_pool_conf,
    #         containers=[ContainerConf(
    #             name="custom-container",
    #             cpus=16,
    #             memory=64,
    #             acceleratorCount=1,
    #             image= ImageConf(
    #                 imageType=1,
    #                 imageUrl="registry.baidubce.com/csm-online/sglang-router:0.2.0",
    #             ),
    #             command=[
    #                 "python",
    #                 "-m",
    #                 "sglang_router.launch_router",
    #                 "--enable-igw",
    #                 "--pd-disaggregation",
    #                 "--service-discovery",
    #                 "--prefill-selector",
    #                 "pom.aihc.baidubce.com/app-name=sglang-p-test",
    #                 "--decode-selector",
    #                 "pom.aihc.baidubce.com/app-name=sglang-d-test",
    #                 "--service-discovery-namespace",
    #                 "aihc-pom",
    #                 "--service-discovery-port",
    #                 "9000",
    #                 "--prefill-policy",
    #                 "cache_aware",
    #                 "--decode-policy",
    #                 "round_robin",
    #                 "--host",
    #                 "0.0.0.0",
    #                 "--port",
    #                 "30000"
    #             ],
    #         )]
    #     )
    #     response = aihc_client.service.ModifyService(serviceId=service_id, serviceConf=service_conf)
    #     print(json.dumps(to_dict(response), ensure_ascii=False))
    #     __logger.info('ModifyService: %s', response.__dict__.keys())
    # except BceHttpClientError as e:
    #     if isinstance(e.last_error, BceServerError):
    #         __logger.error('send request failed. Response %s, code: %s, msg: %s'
    #                        % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
    #     else:
    #         __logger.error('send request failed. Unknown exception: %s' % e)

    # 查询服务变更详情
    try:
        __logger.info('--------------------------DescribeServiceChangelog start...-----------------------------')
        change_id = "ch-48a51f1fc896"
        response = aihc_client.service.DescribeServiceChangelog(changeId=change_id)
        print(json.dumps(to_dict(response), ensure_ascii=False))
        __logger.info('DescribeServiceChangelog: %s', response.__dict__.keys())
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # # 摘除pod流量
    # try:
    #     __logger.info('--------------------------------DisableServicePod start...--------------------------------')
    #     service_id = "s-xxx"
    #     instance_id = "s-xxx-xxx-xx"
    #     block = False
    #     response = aihc_client.service.DisableServicePod(serviceId=service_id, instanceId=instance_id, block=block)
    #     print(json.dumps(to_dict(response), ensure_ascii=False))
    #     __logger.info('DisableServicePod: %s', response.__dict__.keys())
    # except BceHttpClientError as e:
    #     if isinstance(e.last_error, BceServerError):
    #         __logger.error('send request failed. Response %s, code: %s, msg: %s'
    #                        % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
    #     else:
    #         __logger.error('send request failed. Unknown exception: %s' % e)

    # # 删除pod并重建
    # try:
    #     __logger.info('--------------------------------DeleteServicePod start...--------------------------------')
    #     service_id = "s-xxx"
    #     instance_id = "s-xxx-xxx-xx"
    #     response = aihc_client.service.DeleteServicePod(serviceId=service_id, instanceId=instance_id)
    #     print(json.dumps(to_dict(response), ensure_ascii=False))
    #     __logger.info('DeleteServicePod: %s', response.__dict__.keys())
    # except BceHttpClientError as e:
    #     if isinstance(e.last_error, BceServerError):
    #         __logger.error('send request failed. Response %s, code: %s, msg: %s'
    #                        % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
    #     else:
    #         __logger.error('send request failed. Unknown exception: %s' % e)

    # # 删除服务
    # try:
    #     __logger.info('----------------DeleteService start...-----------------------------')
    #     service_id = "s-xxx"
    #     response = aihc_client.service.DeleteService(serviceId=service_id)
    #     print(json.dumps(to_dict(response), ensure_ascii=False))
    #     __logger.info('DeleteService: %s', response.__dict__.keys())
    # except BceHttpClientError as e:
    #     if isinstance(e.last_error, BceServerError):
    #         __logger.error('send request failed. Response %s, code: %s, msg: %s'
    #                        % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
    #     else:
    #         __logger.error('send request failed. Unknown exception: %s' % e)

if __name__ == '__main__':
    main()
