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
- 任务管理：查询任务列表、任务详情、创建、更新、删除任务
- 资源管理：查询数据集、模型、服务、开发机列表
- 错误处理：演示如何处理BCE客户端和服务器错误

主要功能：
1. 演示AIHCV2Client的基本使用方法
2. 展示各种API调用的正确方式
3. 提供完整的错误处理示例
4. 展示响应数据的处理方式

使用前请确保：
- 已正确配置aihc_sample_conf.py中的认证信息
- 有相应的AIHC服务权限
- 网络连接正常

示例：
    python aihc_sample.py
"""

# !/usr/bin/env python
# coding=utf-8
from baidubce.exception import BceHttpClientError, BceServerError
from baidubce.services.aihc.aihc_model import JobConfig
from baidubce.services.aihc.aihc_client import AIHCV2Client, aihc_model

import sample.aihc.aihc_sample_conf as aihc_sample_conf
import json
import logging
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
    
    本函数展示了AIHCV2Client的完整使用流程，包括：
    1. 创建AIHC客户端实例
    2. 查询任务列表和详情
    3. 查询各种资源列表（数据集、模型、服务、开发机）
    4. 完整的错误处理机制
    
    注意：
    - 部分功能（如创建、更新、删除任务）被注释掉，避免误操作
    - 所有API调用都包含完整的异常处理
    - 响应数据会被转换为JSON格式输出
    
    Raises:
        BceHttpClientError: 当API调用失败时抛出
        BceServerError: 当服务器返回错误时抛出
    """
    resourcePoolId = "cce-hcuw9ybk"
    jobId = "job-1234567890"

    # create a aihc client
    aihc_client = AIHCV2Client(aihc_sample_conf.config)

    # 查询任务列表
    try:
        __logger.info('--------------------------------DescribeJobs start--------------------------------')
        response = aihc_client.job.DescribeJobs(resourcePoolId=resourcePoolId)
        # 将response转换为python对象
        print(json.dumps(to_dict(response), indent=4, ensure_ascii=False))

        # response对象的全部key
        __logger.info('response.__dict__.keys(): %s', response.__dict__.keys())
        jobId = response.jobs[0].jobId
        __logger.info('jobId: %s', jobId)
        
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # 查询任务详情
    try:
        __logger.info('--------------------------------DescribeJob start...--------------------------------')
        response = aihc_client.job.DescribeJob(resourcePoolId=resourcePoolId, jobId=jobId)
        print(json.dumps(to_dict(response), indent=4, ensure_ascii=False))

        __logger.info('response.__dict__.keys(): %s', response.__dict__.keys())
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # 删除任务
    # try:
    #     response = aihc_client.DeleteJob(resourcePoolId=resourcePoolId, jobId=jobId)
    #     print(response)
    # except BceHttpClientError as e:
    #     if isinstance(e.last_error, BceServerError):
    #         __logger.error('send request failed. Response %s, code: %s, msg: %s'
    #                        % (e.last_error.status_code, e.last_error.code, e.last_error.message))
    #     else:
    #         __logger.error('send request failed. Unknown exception: %s' % e)

    # 更新任务
    # try:
    #     response = aihc_client.UpdateJob(resourcePoolId=resourcePoolId, jobId=jobId, priority="normal")
    #     print(response)
    # except BceHttpClientError as e:
    #     if isinstance(e.last_error, BceServerError):
    #         __logger.error('send request failed. Response %s, code: %s, msg: %s'
    #                        % (e.last_error.status_code, e.last_error.code, e.last_error.message))
    #     else:
    #         __logger.error('send request failed. Unknown exception: %s' % e)

    # 创建任务
    # try:
    #     jobConfig = aihc_model.JobConfig(
    #         name="test-job",
    #         queue="test-queue",
    #         jobSpec=aihc_model.JobSpec(
    #             image="test-image",
    #             replicas=1
    #         ),
    #         command="python train.py"
    #     )
    #     response = aihc_client.CreateJob(resourcePoolId=resourcePoolId, jobConfig=jobConfig)
    #     print(response)
    # except BceHttpClientError as e:
    #     if isinstance(e.last_error, BceServerError):
    #         __logger.error('send request failed. Response %s, code: %s, msg: %s'
    #                        % (e.last_error.status_code, e.last_error.code, e.last_error.message))
    #     else:
    #         __logger.error('send request failed. Unknown exception: %s' % e)

    # 查询数据集列表
    try:
        __logger.info('--------------------------------DescribeDatasets start--------------------------------')
        response = aihc_client.dataset.DescribeDatasets()
        print(json.dumps(to_dict(response), indent=4, ensure_ascii=False))
        __logger.info('DescribeDatasets: %s', response.__dict__.keys())
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # 查询模型列表
    try:
        __logger.info('--------------------------------DescribeModels start...--------------------------------')
        response = aihc_client.model.DescribeModels()
        print(json.dumps(to_dict(response), indent=4, ensure_ascii=False))
        __logger.info('DescribeModels: %s', response.__dict__.keys())
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # 查询服务列表
    try:
        __logger.info('--------------------------------DescribeServices start...--------------------------------')
        response = aihc_client.service.DescribeServices()
        print(json.dumps(to_dict(response), indent=4, ensure_ascii=False))
        __logger.info('DescribeServices: %s', response.__dict__.keys())
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # 查询开发机列表
    try:
        __logger.info('--------------------------------DescribeDevInstances start...--------------------------------')
        response = aihc_client.dev_instance.DescribeDevInstances()
        print(json.dumps(to_dict(response), indent=4, ensure_ascii=False))
        __logger.info('DescribeDevInstances: %s', response.__dict__.keys())
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)


if __name__ == '__main__':
    main()