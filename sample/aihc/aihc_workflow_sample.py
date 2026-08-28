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
AIHC工作流模板客户端示例模块。
"""

# !/usr/bin/env python
# coding=utf-8

import json
import logging

from baidubce.exception import BceHttpClientError, BceServerError
from baidubce.services.aihc.aihc_client import AihcClient

from sample.aihc import aihc_sample_conf

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', force=True)
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("baidubce").setLevel(logging.INFO)
__logger = logging.getLogger(__name__)
__logger.setLevel(logging.INFO)


def to_dict(obj):
    """将对象转换为字典格式。"""
    if isinstance(obj, dict):
        return {k: to_dict(v) for k, v in obj.items()}
    elif hasattr(obj, '__dict__'):
        return {k: to_dict(v) for k, v in obj.__dict__.items()}
    elif isinstance(obj, list):
        return [to_dict(i) for i in obj]
    else:
        return obj


def main():
    """主函数，演示AIHC工作流模板服务的各种操作。"""
    aihc_client = AihcClient(aihc_sample_conf.config)

    # CreatePipeline - 创建工作流模版（危险操作，已注释）
    # try:
    #     __logger.info('--------------------------------CreatePipeline start--------------------------------')
    #     name = "my-pipeline"
    #     manifest = "version: v1\nkind: PipelineTemplate\n..."
    #     description = "示例 Pipeline"
    #     pipeline_type = "normal"
    #     resource_pool_id = "xxx"
    #     response = aihc_client.workflow.CreatePipeline(
    #         name=name,
    #         manifest=manifest,
    #         description=description,
    #         pipelineType=pipeline_type,
    #         resourcePoolId=resource_pool_id,
    #         concurrencyPolicy="Allow",
    #     )
    #     print(json.dumps(to_dict(response), ensure_ascii=False))
    # except BceHttpClientError as e:
    #     if isinstance(e.last_error, BceServerError):
    #         __logger.error('send request failed. Response %s, code: %s, msg: %s'
    #                        % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
    #     else:
    #         __logger.error('send request failed. Unknown exception: %s' % e)

    # UpdatePipeline - 更新工作流模版（危险操作，已注释）
    # try:
    #     __logger.info('--------------------------------UpdatePipeline start--------------------------------')
    #     pipeline_id = "pipe-xxx"
    #     response = aihc_client.workflow.UpdatePipeline(
    #         pipelineId=pipeline_id,
    #         name="updated-pipeline-name",
    #         description="更新后的描述",
    #         pipelineType="normal",
    #         concurrencyPolicy="Allow",
    #     )
    #     print(json.dumps(to_dict(response), ensure_ascii=False))
    # except BceHttpClientError as e:
    #     if isinstance(e.last_error, BceServerError):
    #         __logger.error('send request failed. Response %s, code: %s, msg: %s'
    #                        % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
    #     else:
    #         __logger.error('send request failed. Unknown exception: %s' % e)

    # StopPipelineRun - 停止工作流运行（危险操作，已注释）
    # try:
    #     __logger.info('--------------------------------StopPipelineRun start--------------------------------')
    #     run_id = "xxx"
    #     response = aihc_client.workflow.StopPipelineRun(
    #         runId=run_id,
    #         terminate=False,
    #         message="暂时停止",
    #     )
    #     print(json.dumps(to_dict(response), ensure_ascii=False))
    # except BceHttpClientError as e:
    #     if isinstance(e.last_error, BceServerError):
    #         __logger.error('send request failed. Response %s, code: %s, msg: %s'
    #                        % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
    #     else:
    #         __logger.error('send request failed. Unknown exception: %s' % e)

    # DescribePipelineRunNodes - 查询工作流运行节点列表
    try:
        __logger.info('--------------------------------DescribePipelineRunNodes start--------------------------------')
        run_id = "xxx"
        response = aihc_client.workflow.DescribePipelineRunNodes(
            runId=run_id,
        )
        print(json.dumps(to_dict(response), ensure_ascii=False))
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # CreatePipelineRun - 运行工作流（危险操作，已注释）
    # try:
    #     __logger.info('--------------------------------CreatePipelineRun start--------------------------------')
    #     pipeline_id = "pipe-xxx"
    #     response = aihc_client.workflow.CreatePipelineRun(
    #         pipelineId=pipeline_id,
    #         isCronRunOnce=False,
    #     )
    #     print(json.dumps(to_dict(response), ensure_ascii=False))
    # except BceHttpClientError as e:
    #     if isinstance(e.last_error, BceServerError):
    #         __logger.error('send request failed. Response %s, code: %s, msg: %s'
    #                        % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
    #     else:
    #         __logger.error('send request failed. Unknown exception: %s' % e)

    # DeletePipeline - 删除工作流模版（危险操作，已注释）
    # try:
    #     __logger.info('--------------------------------DeletePipeline start--------------------------------')
    #     pipeline_id = "pipe-xxx"
    #     response = aihc_client.workflow.DeletePipeline(
    #         pipelineId=pipeline_id,
    #     )
    #     print(json.dumps(to_dict(response), ensure_ascii=False))
    # except BceHttpClientError as e:
    #     if isinstance(e.last_error, BceServerError):
    #         __logger.error('send request failed. Response %s, code: %s, msg: %s'
    #                        % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
    #     else:
    #         __logger.error('send request failed. Unknown exception: %s' % e)

    # DeletePipelineRun - 删除工作流运行实例（危险操作，已注释）
    # try:
    #     __logger.info('--------------------------------DeletePipelineRun start--------------------------------')
    #     run_id = "xxx"
    #     response = aihc_client.workflow.DeletePipelineRun(
    #         runId=run_id,
    #     )
    #     print(json.dumps(to_dict(response), ensure_ascii=False))
    # except BceHttpClientError as e:
    #     if isinstance(e.last_error, BceServerError):
    #         __logger.error('send request failed. Response %s, code: %s, msg: %s'
    #                        % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
    #     else:
    #         __logger.error('send request failed. Unknown exception: %s' % e)

    # DescribePipelines - 查询工作流模版列表
    try:
        __logger.info('--------------------------------DescribePipelines start--------------------------------')
        response = aihc_client.workflow.DescribePipelines(
            pageNumber=1,
            pageSize=10,
        )
        print(json.dumps(to_dict(response), ensure_ascii=False))
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # DescribePipeline - 查询工作流模版详情
    try:
        __logger.info('--------------------------------DescribePipeline start--------------------------------')
        pipeline_id = "pipe-xxx"
        response = aihc_client.workflow.DescribePipeline(
            pipelineId=pipeline_id,
        )
        print(json.dumps(to_dict(response), ensure_ascii=False))
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # DescribePipelineRuns - 查询工作流运行列表
    try:
        __logger.info('--------------------------------DescribePipelineRuns start--------------------------------')
        pipeline_id = "pipe-xxx"
        response = aihc_client.workflow.DescribePipelineRuns(
            pipelineId=pipeline_id,
            pageNumber=1,
            pageSize=10,
        )
        print(json.dumps(to_dict(response), ensure_ascii=False))
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # DescribePipelineRun - 查询工作流运行详情
    try:
        __logger.info('--------------------------------DescribePipelineRun start--------------------------------')
        run_id = "xxx"
        response = aihc_client.workflow.DescribePipelineRun(
            runId=run_id,
        )
        print(json.dumps(to_dict(response), ensure_ascii=False))
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # RetryPipelineRun - 重试工作流运行（危险操作，已注释）
    # try:
    #     __logger.info('--------------------------------RetryPipelineRun start--------------------------------')
    #     run_id = "xxx"
    #     response = aihc_client.workflow.RetryPipelineRun(
    #         runId=run_id,
    #         mode="full",
    #     )
    #     print(json.dumps(to_dict(response), ensure_ascii=False))
    # except BceHttpClientError as e:
    #     if isinstance(e.last_error, BceServerError):
    #         __logger.error('send request failed. Response %s, code: %s, msg: %s'
    #                        % (e.last_error.status_code, e.last_error.code, str(e.last_error)))
    #     else:
    #         __logger.error('send request failed. Unknown exception: %s' % e)


if __name__ == '__main__':
    main()
