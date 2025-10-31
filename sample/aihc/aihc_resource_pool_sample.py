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
- 资源池管理：查询资源池列表、资源池详情、资源池概览、资源池配置、队列列表、队列详情
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
    python aihc_resource_pool_sample.py

    python -m sample.aihc.aihc_resource_pool_sample -v
"""

# !/usr/bin/env python
# coding=utf-8

import json
import logging

from baidubce.exception import BceHttpClientError, BceServerError
from baidubce.services.aihc.aihc_client import AihcClient

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
    主函数，演示AIHC服务的资源池相关操作。

    本函数展示了AihcClient的资源池相关接口使用流程，包括：
    1. 创建AIHC客户端实例
    2. 查询资源池列表和详情
    3. 查询资源池概览和配置信息
    4. 查询队列列表和详情
    5. 完整的错误处理机制

    注意：
    - 所有API调用都包含完整的异常处理
    - 响应数据会被转换为JSON格式输出

    Raises:
        BceHttpClientError: 当API调用失败时抛出
        BceServerError: 当服务器返回错误时抛出
    """
    # create a aihc client
    aihc_client = AihcClient(aihc_sample_conf.config)

    # 初始化变量
    resource_pool_id = None
    queue_id = None

    # 查询资源池列表
    try:
        __logger.info('--------------------------------DescribeResourcePools start--------------------------------')
        response = aihc_client.resource_pool.DescribeResourcePools(resourcePoolType='common')
        print(json.dumps(to_dict(response), ensure_ascii=False, indent=2))
        __logger.info('response.__dict__.keys(): %s', response.__dict__.keys())

        # 如果有资源池，获取第一个资源池ID用于后续查询
        if hasattr(response, 'resourcePools') and len(response.resourcePools) > 0:
            resource_pool_id = response.resourcePools[0].resourcePoolId
            __logger.info('resource_pool_id: %s', resource_pool_id)

    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # 查询资源池概览
    try:
        __logger.info(
            '--------------------------------DescribeResourcePoolOverview start--------------------------------')
        response = aihc_client.resource_pool.DescribeResourcePoolOverview()
        print(json.dumps(to_dict(response), ensure_ascii=False, indent=2))
        __logger.info('response.__dict__.keys(): %s', response.__dict__.keys())
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # 如果获取到资源池ID，继续查询详情
    if resource_pool_id:
        # 查询资源池详情
        try:
            __logger.info('-------------------------DescribeResourcePool start--------------------------------')
            response = aihc_client.resource_pool.DescribeResourcePool(resourcePoolId=resource_pool_id)
            print(json.dumps(to_dict(response), ensure_ascii=False, indent=2))
            __logger.info('response.__dict__.keys(): %s', response.__dict__.keys())
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                __logger.error('send request failed. Response %s, code: %s, msg: %s'
                               % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
            else:
                __logger.error('send request failed. Unknown exception: %s' % e)

        # 查询资源池配置
        try:
            __logger.info('-----------------DescribeResourcePoolConfiguration start--------------------------------')
            response = aihc_client.resource_pool.DescribeResourcePoolConfiguration(resourcePoolId=resource_pool_id)
            print(json.dumps(to_dict(response), ensure_ascii=False, indent=2))
            __logger.info('response.__dict__.keys(): %s', response.__dict__.keys())
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                __logger.error('send request failed. Response %s, code: %s, msg: %s'
                               % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
            else:
                __logger.error('send request failed. Unknown exception: %s' % e)

        # 查询队列列表
        try:
            __logger.info('--------------------------------DescribeQueues start--------------------------------')
            response = aihc_client.resource_pool.DescribeQueues(resourcePoolId=resource_pool_id)
            print(json.dumps(to_dict(response), ensure_ascii=False, indent=2))
            __logger.info('response.__dict__.keys(): %s', response.__dict__.keys())
            # 如果有队列，获取第一个队列ID用于后续查询
            if hasattr(response, 'queues') and len(response.queues) > 0:
                queue_id = response.queues[0].queueId
                __logger.info('queue_id: %s', queue_id)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                __logger.error('send request failed. Response %s, code: %s, msg: %s'
                               % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
            else:
                __logger.error('send request failed. Unknown exception: %s' % e)

        # 如果获取到队列ID，查询队列详情
        if queue_id:
            try:
                __logger.info('--------------------------------DescribeQueue start--------------------------------')
                response = aihc_client.resource_pool.DescribeQueue(queueId=queue_id)
                print(json.dumps(to_dict(response), ensure_ascii=False, indent=2))
                __logger.info('response.__dict__.keys(): %s', response.__dict__.keys())
            except BceHttpClientError as e:
                if isinstance(e.last_error, BceServerError):
                    __logger.error('send request failed. Response %s, code: %s, msg: %s'
                                   % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
                else:
                    __logger.error('send request failed. Unknown exception: %s' % e)


if __name__ == '__main__':
    main()
