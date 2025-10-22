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
    python aihc_job_sample.py

    python -m sample.aihc.aihc_job_sample -v
"""

# !/usr/bin/env python
# coding=utf-8

import json
import logging

from baidubce.exception import BceHttpClientError, BceServerError
from baidubce.services.aihc.aihc_client import AihcClient
from baidubce.services.aihc.modules.job.job_model import Datasource, Env, JobSpec

from sample.aihc import aihc_sample_conf

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
    - 部分功能（如创建、更新、删除任务）被注释掉，避免误操作
    - 所有API调用都包含完整的异常处理
    - 响应数据会被转换为JSON格式输出

    Raises:
        BceHttpClientError: 当API调用失败时抛出
        BceServerError: 当服务器返回错误时抛出
    """

    # 创建 aihc client
    aihc_client = AihcClient(aihc_sample_conf.config)

    # 查询训练任务列表
    try:
        __logger.info('--------------------------------DescribeJobs start--------------------------------')
        resource_pool_id = "cce-xxx"
        keyword = ""
        response = aihc_client.job.DescribeJobs(resourcePoolId=resource_pool_id, keyword=keyword)
        print(json.dumps(to_dict(response), ensure_ascii=False))
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # 查询训练任务详情
    try:
        __logger.info('--------------------------------DescribeJob start--------------------------------')
        resource_pool_id = "cce-xxx"
        queue_id = "default"
        job_id = "job-xxx"
        need_detail = True
        response = aihc_client.job.DescribeJob(resourcePoolId=resource_pool_id, queueID=queue_id, jobId=job_id,
                                               needDetail=need_detail)
        print(json.dumps(to_dict(response), ensure_ascii=False))
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # 查询训练任务监控
    try:
        __logger.info('--------------------------------DescribeJobMetrics start--------------------------------')
        resource_pool_id = "cce-xxx"
        job_id = "job-xxx"
        start_time = "1758359060"
        end_time = "1758445563"
        time_step = "5m"
        metric_type = "GpuUsage"
        rate_interval = "5m"
        response = aihc_client.job.DescribeJobMetrics(
                                        resourcePoolId=resource_pool_id, jobId=job_id,
                                        metricType=metric_type, startTime=start_time,
                                        endTime=end_time, timeStep=time_step,
                                        rateInterval=rate_interval
        )
        print(json.dumps(to_dict(response), ensure_ascii=False))
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # 查询训练任务事件
    try:
        __logger.info('--------------------------DescribeJobEvents start-----------------------------------')
        resource_pool_id = "cce-xxx"
        job_id = "job-xxx"
        start_time = "1758532230"
        end_time = "1758618650"
        response = aihc_client.job.DescribeJobEvents(resourcePoolId=resource_pool_id, jobId=job_id,
                                                     startTime=start_time, endTime=end_time)
        print(json.dumps(to_dict(response), ensure_ascii=False))
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # 查询训练任务日志
    try:
        __logger.info('--------------------------DescribeJobLogs start---------------------------------')
        resource_pool_id = "cce-xxx"
        job_id = "job-xxx"
        pod_name = "xxx-test-copy2-master-0"
        keywords = "xxx"
        response = aihc_client.job.DescribeJobLogs(resourcePoolId=resource_pool_id,
                                                   jobId=job_id,
                                                   keywords=keywords,
                                                   podName=pod_name)
        print(json.dumps(to_dict(response), ensure_ascii=False))
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # 查询训练任务Pod事件
    try:
        __logger.info('---------------DescribeJobPodEvents start---------------------------')
        resource_pool_id = "cce-xxx"
        pod_name = "job-xxx-master-0"
        job_id = "job-xxx"
        response = aihc_client.job.DescribeJobPodEvents(resourcePoolId=resource_pool_id,
                                                        jobId=job_id,
                                                        podName=pod_name,
                                                        )
        print(json.dumps(to_dict(response), ensure_ascii=False))
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # 查询训练任务监控
    try:
        __logger.info('--------------------DescribeJobMetrics start------------------------')
        resource_pool_id = "cce-xxx"
        job_id = "job-xxx"
        start_time = "1758359060"
        end_time = "1758445563"
        time_step = "5m"
        metric_type = "GpuUsage"
        rate_interval = "5m"
        response = aihc_client.job.DescribeJobMetrics(resourcePoolId=resource_pool_id,
                                                      jobId=job_id,
                                                      metricType=metric_type,
                                                      startTime=start_time,
                                                      endTime=end_time,
                                                      timeStep=time_step,
                                                      rateInterval=rate_interval)
        print(json.dumps(to_dict(response), ensure_ascii=False))
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # 查询训练任务所在节点列表
    try:
        __logger.info('-------------------DescribeJobNodes start--------------------------')
        resource_pool_id = "cce-xxx"
        job_id = "job-xxx"
        response = aihc_client.job.DescribeJobNodes(resourcePoolId=resource_pool_id, jobId=job_id)
        print(json.dumps(to_dict(response), ensure_ascii=False))
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # 获取训练任务WebTerminal地址
    try:
        __logger.info('-------------------DescribeJobWebterminal start--------------------------')
        resource_pool_id = "cce-xxx"
        job_id = "job-xxx"
        podName = "xxx-test-bb1-rerun1-master-0"
        handshake_timeout_second = "30"
        ping_timeout_second = "900"
        response = aihc_client.job.DescribeJobWebterminal(
            resourcePoolId=resource_pool_id,
            jobId=job_id,
            podName=podName,
            pingTimeoutSecond=ping_timeout_second,
            handshakeTimeoutSecond=handshake_timeout_second,
        )
        print(json.dumps(to_dict(response), ensure_ascii=False))
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # # 删除训练任务
    # try:
    #     __logger.info('----------------------------------DeleteJob start-----------------------------------')
    #     resource_pool_id = "cce-xxx"
    #     job_id = "job-xxx"
    #     response = aihc_client.job.DeleteJob(resourcePoolId=resource_pool_id, jobId=job_id)
    #     print(json.dumps(to_dict(response), ensure_ascii=False))
    # except BceHttpClientError as e:
    #     if isinstance(e.last_error, BceServerError):
    #         __logger.error('send request failed. Response %s, code: %s, msg: %s'
    #                        % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
    #     else:
    #         __logger.error('send request failed. Unknown exception: %s' % e)
    #
    # # 更新训练任务
    # try:
    #     __logger.info('---------------------------------ModifyJob start----------------------------------')
    #     resource_pool_id = ("cce-xxx")
    #     job_id = "job-xxx"
    #     priority = "high"
    #     response = aihc_client.job.ModifyJob(resourcePoolId=resource_pool_id, jobId=job_id, priority=priority)
    #     print(json.dumps(to_dict(response), ensure_ascii=False))
    # except BceHttpClientError as e:
    #     if isinstance(e.last_error, BceServerError):
    #         __logger.error('send request failed. Response %s, code: %s, msg: %s'
    #                        % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
    #     else:
    #         __logger.error('send request failed. Unknown exception: %s' % e)
    #
    # # 创建训练任务
    # try:
    #     __logger.info('---------------------------------CreateJob start------------------------------')
    #     resource_pool_id = "cce-xxx"
    #     queue_id = "default"
    #     name = ("python-sdk-test-xxx")
    #     command = "sleep 5m"
    #     envs = [Env(name="NCCL_DEBUG", value="DEBUG"), Env(name="NCCL_IB_DISABLE", value="0")]
    #     data_source = Datasource(type="pfs", name="pfs-pxE6jz", mountPath="/mnt/cluster")
    #     job_spec = JobSpec(
    #         image="registry.baidubce.com/aihc-aiak/aiak-megatron:ubuntu20.04"
    #               "-cu11.8-torch1.14.0-py38_v1.2.7.12_release",
    #         replicas=1,
    #         resources=[],
    #         envs=envs,
    #         enableRDMA=False
    #     )
    #     job_type = "PyTorchJob"
    #     labels = []
    #     priority = "normal"
    #     dataSources = [
    #         data_source,
    #     ]
    #     enable_bccl = False
    #     fault_tolerance = False
    #     fault_tolerance_args = {}
    #     tensorboard_config = {}
    #     retention_period = "5m"
    #     response = aihc_client.job.CreateJob(
    #         resourcePoolId=resource_pool_id,
    #         queueID=queue_id,
    #         name=name,
    #         command=command,
    #         jobSpec=job_spec,
    #         jobType=job_type,
    #         labels=labels,
    #         priority=priority,
    #         dataSources=dataSources,
    #         enableBccl=enable_bccl,
    #         faultTolerance=fault_tolerance,
    #         faultToleranceArgs=fault_tolerance_args,
    #         tensorboardConfig=tensorboard_config,
    #         retentionPeriod=retention_period,
    #     )
    #     print(json.dumps(to_dict(response), ensure_ascii=False))
    # except BceHttpClientError as e:
    #     if isinstance(e.last_error, BceServerError):
    #         __logger.error('send request failed. Response %s, code: %s, msg: %s'
    #                        % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
    #     else:
    #         __logger.error('send request failed. Unknown exception: %s' % e)
    #
    # # 停止训练任务
    # try:
    #     __logger.info('stop job')
    #     resource_pool_id = "cce-xxx"
    #     job_id = "job-xxx"
    #     response = aihc_client.job.StopJob(resourcePoolId=resource_pool_id, jobId=job_id)
    #     print(json.dumps(to_dict(response), ensure_ascii=False))
    # except BceHttpClientError as e:
    #     if isinstance(e.last_error, BceServerError):
    #         __logger.error('send request failed. Response %s, code: %s, msg: %s'
    #                        % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
    #     else:
    #         __logger.error('send request failed. Unknown exception: %s' % e)


if __name__ == '__main__':
    main()
