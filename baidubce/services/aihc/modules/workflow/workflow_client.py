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
AIHC workflow client module.
"""
import json

from baidubce.http import http_methods
from baidubce.services.aihc.base.aihc_base_client import AIHCBaseClient


class WorkflowClient(AIHCBaseClient):
    """工作流模板相关接口客户端"""

    def CreatePipeline(
        self,
        name,
        manifest,
        description=None,
        pipelineType=None,
        cronExpression=None,
        disabled=None,
        resourcePoolId=None,
        concurrencyPolicy=None,
    ):
        """
        创建一个工作流模版（Pipeline）。

        Args:
            name: Pipeline 名称，1～255 字符（必填，Body参数）
            manifest: Pipeline 定义的 Base64 字符串（必填，Body参数）
            description: 描述（可选）
            pipelineType: Pipeline 类型，支持 normal、cron，默认值：normal（可选）
            cronExpression: 五段式 Cron 表达式，pipelineType=cron 时必选（可选）
            disabled: 是否禁用，取值 true/false（可选）
            resourcePoolId: 资源池 ID（可选）
            concurrencyPolicy: 并发策略，支持 Allow、Forbid、Replace（可选）

        Returns:
            baidubce.bce_response.BceResponse: 返回创建的 Pipeline 信息，包含 pipelineId、name、status 等

        Raises:
            ValueError: 当必填参数为空时
        """
        path = b'/'
        params = {
            'action': 'CreatePipeline',
        }
        body = {
            'name': name,
            'manifest': manifest,
        }
        if description is not None:
            body['description'] = description
        if pipelineType is not None:
            body['pipelineType'] = pipelineType
        if cronExpression is not None:
            body['cronExpression'] = cronExpression
        if disabled is not None:
            body['disabled'] = disabled
        if resourcePoolId is not None:
            body['resourcePoolId'] = resourcePoolId
        if concurrencyPolicy is not None:
            body['concurrencyPolicy'] = concurrencyPolicy
        return self._send_job_request(
            http_methods.POST,
            path,
            body=json.dumps(body),
            params=params
        )

    def UpdatePipeline(
        self,
        pipelineId,
        name=None,
        description=None,
        manifest=None,
        pipelineType=None,
        cronExpression=None,
        disabled=None,
        resourcePoolId=None,
        concurrencyPolicy=None,
    ):
        """
        更新一个已有的工作流模版（Pipeline）。

        Args:
            pipelineId: 待更新的 Pipeline ID（必填，Query参数）
            name: Pipeline 名称，1～255 字符（可选）
            description: 描述（可选）
            manifest: Pipeline 定义的 Base64 字符串（可选）
            pipelineType: Pipeline 类型，支持 normal、cron（可选）
            cronExpression: 五段式 Cron 表达式（可选）
            disabled: 是否禁用，取值 true/false（可选）
            resourcePoolId: 资源池 ID（可选）
            concurrencyPolicy: 并发策略，支持 Allow、Forbid、Replace（可选）

        Returns:
            baidubce.bce_response.BceResponse: 返回更新后的 Pipeline 信息

        Raises:
            ValueError: 当必填参数为空时
        """
        path = b'/'
        params = {
            'action': 'UpdatePipeline',
            'pipelineId': pipelineId,
        }
        body = {}
        if name is not None:
            body['name'] = name
        if description is not None:
            body['description'] = description
        if manifest is not None:
            body['manifest'] = manifest
        if pipelineType is not None:
            body['pipelineType'] = pipelineType
        if cronExpression is not None:
            body['cronExpression'] = cronExpression
        if disabled is not None:
            body['disabled'] = disabled
        if resourcePoolId is not None:
            body['resourcePoolId'] = resourcePoolId
        if concurrencyPolicy is not None:
            body['concurrencyPolicy'] = concurrencyPolicy
        return self._send_job_request(
            http_methods.POST,
            path,
            body=json.dumps(body),
            params=params
        )

    def StopPipelineRun(
        self,
        runId,
        terminate=None,
        message=None,
    ):
        """
        停止指定的工作流运行。

        Args:
            runId: 运行 ID（必填，Query参数）
            terminate: 强制终止标志。true 强制终止（kill Pod），false 优雅停止，默认 false（可选）
            message: 停止原因或备注信息（可选）

        Returns:
            baidubce.bce_response.BceResponse: 返回 requestId 和 runId

        Raises:
            ValueError: 当必填参数为空时
        """
        path = b'/'
        params = {
            'action': 'StopPipelineRun',
            'runId': runId,
        }
        body = {}
        if terminate is not None:
            body['terminate'] = terminate
        if message is not None:
            body['message'] = message
        return self._send_job_request(
            http_methods.POST,
            path,
            body=json.dumps(body),
            params=params
        )

    def DescribePipelineRunNodes(
        self,
        runId,
    ):
        """
        查询指定工作流运行的节点列表，返回各节点的执行状态、类型、时间戳等信息。

        Args:
            runId: 运行 ID（必填，Query参数）

        Returns:
            baidubce.bce_response.BceResponse: 返回 requestId、runId 和 nodes 节点列表

        Raises:
            ValueError: 当必填参数为空时
        """
        path = b'/'
        params = {
            'action': 'DescribePipelineRunNodes',
            'runId': runId,
        }
        return self._send_job_request(
            http_methods.GET,
            path,
            body=json.dumps({}),
            params=params
        )

    def CreatePipelineRun(
        self,
        pipelineId,
        isCronRunOnce=None,
    ):
        """
        基于已有的工作流模版（Pipeline）提交一次运行实例。

        Args:
            pipelineId: Pipeline ID（必填，Body参数）
            isCronRunOnce: Cron Pipeline 立即运行一次（可选）

        Returns:
            baidubce.bce_response.BceResponse: 返回 requestId、runId 和 argoWorkflowUid

        Raises:
            ValueError: 当必填参数为空时
        """
        path = b'/'
        params = {
            'action': 'CreatePipelineRun',
        }
        body = {
            'pipelineId': pipelineId,
        }
        if isCronRunOnce is not None:
            body['isCronRunOnce'] = isCronRunOnce
        return self._send_job_request(
            http_methods.POST,
            path,
            body=json.dumps(body),
            params=params
        )

    def DeletePipeline(
        self,
        pipelineId,
    ):
        """
        删除指定的工作流模版（Pipeline）。

        Args:
            pipelineId: Pipeline ID（必填，Query参数）

        Returns:
            baidubce.bce_response.BceResponse: 返回 requestId、deleted 和 pipelineId

        Raises:
            ValueError: 当必填参数为空时
        """
        path = b'/'
        params = {
            'action': 'DeletePipeline',
            'pipelineId': pipelineId,
        }
        return self._send_job_request(
            http_methods.POST,
            path,
            body=json.dumps({}),
            params=params
        )

    def DeletePipelineRun(
        self,
        runId,
    ):
        """
        删除指定的工作流运行实例（PipelineRun）。

        Args:
            runId: 运行 ID（必填，Query参数）

        Returns:
            baidubce.bce_response.BceResponse: 返回 requestId 和 runId

        Raises:
            ValueError: 当必填参数为空时
        """
        path = b'/'
        params = {
            'action': 'DeletePipelineRun',
            'runId': runId,
        }
        return self._send_job_request(
            http_methods.POST,
            path,
            body=json.dumps({}),
            params=params
        )

    def DescribePipelines(
        self,
        pageNumber=None,
        pageSize=None,
        keyword=None,
        pipelineId=None,
        name=None,
        pipelineType=None,
        resourcePoolId=None,
    ):
        """
        查询当前账号下的工作流模版（Pipeline）列表，支持关键字搜索、分页等过滤条件。

        Args:
            pageNumber: 页码，从 1 开始，默认 1（可选，Query参数）
            pageSize: 每页条数，默认 10（可选，Query参数）
            keyword: 关键字搜索（模糊匹配名称）（可选，Query参数）
            pipelineId: 按 Pipeline ID 过滤（可选，Query参数）
            name: 按名称过滤（可选，Query参数）
            pipelineType: 按 Pipeline 类型过滤（可选，Query参数）
            resourcePoolId: 按资源池 ID 过滤（可选，Query参数）

        Returns:
            baidubce.bce_response.BceResponse: 返回 items 列表、total、pageNumber、pageSize

        Raises:
            ValueError: 当必填参数为空时
        """
        path = b'/'
        params = {
            'action': 'DescribePipelines',
        }
        if pageNumber is not None:
            params['pageNumber'] = pageNumber
        if pageSize is not None:
            params['pageSize'] = pageSize
        if keyword is not None:
            params['keyword'] = keyword
        if pipelineId is not None:
            params['pipelineId'] = pipelineId
        if name is not None:
            params['name'] = name
        if pipelineType is not None:
            params['pipelineType'] = pipelineType
        if resourcePoolId is not None:
            params['resourcePoolId'] = resourcePoolId
        return self._send_job_request(
            http_methods.GET,
            path,
            body=json.dumps({}),
            params=params
        )

    def DescribePipeline(
        self,
        pipelineId,
    ):
        """
        查询指定工作流模版（Pipeline）的详细信息。

        Args:
            pipelineId: Pipeline ID（必填，Query参数）

        Returns:
            baidubce.bce_response.BceResponse: 返回 Pipeline 详细信息，包含 pipelineId、name、pipelineType 等

        Raises:
            ValueError: 当必填参数为空时
        """
        path = b'/'
        params = {
            'action': 'DescribePipeline',
            'pipelineId': pipelineId,
        }
        return self._send_job_request(
            http_methods.GET,
            path,
            body=json.dumps({}),
            params=params
        )

    def DescribePipelineRuns(
        self,
        pipelineId,
        status=None,
        startTime=None,
        endTime=None,
        pageNumber=None,
        pageSize=None,
    ):
        """
        查询指定工作流模版（Pipeline）下的运行实例（PipelineRun）列表，支持状态、时间范围、分页等过滤条件。

        Args:
            pipelineId: Pipeline ID（必填，Query参数）
            status: 运行状态过滤，如 running、succeeded、failed（可选，Query参数）
            startTime: 运行开始时间下限（ISO 8601 格式）（可选，Query参数）
            endTime: 运行开始时间上限（ISO 8601 格式）（可选，Query参数）
            pageNumber: 页码，从 1 开始，默认 1（可选，Query参数）
            pageSize: 每页条数，默认 10（可选，Query参数）

        Returns:
            baidubce.bce_response.BceResponse: 返回 items 列表、total、pageNumber、pageSize

        Raises:
            ValueError: 当必填参数为空时
        """
        path = b'/'
        params = {
            'action': 'DescribePipelineRuns',
            'pipelineId': pipelineId,
        }
        if status is not None:
            params['status'] = status
        if startTime is not None:
            params['startTime'] = startTime
        if endTime is not None:
            params['endTime'] = endTime
        if pageNumber is not None:
            params['pageNumber'] = pageNumber
        if pageSize is not None:
            params['pageSize'] = pageSize
        return self._send_job_request(
            http_methods.GET,
            path,
            body=json.dumps({}),
            params=params
        )

    def RetryPipelineRun(
        self,
        runId,
        mode=None,
    ):
        """
        重试指定的工作流运行实例（PipelineRun）。

        Args:
            runId: 运行 ID（必填，Query参数）
            mode: 重试模式，full 从头全量重跑，breakpoint 从失败节点断点续跑，默认 full（可选，Body参数）

        Returns:
            baidubce.bce_response.BceResponse: 返回 requestId、runId、argoWorkflowName、argoWorkflowUid

        Raises:
            ValueError: 当必填参数为空时
        """
        path = b'/'
        params = {
            'action': 'RetryPipelineRun',
            'runId': runId,
        }
        body = {}
        if mode is not None:
            body['mode'] = mode
        return self._send_job_request(
            http_methods.POST,
            path,
            body=json.dumps(body),
            params=params
        )

    def DescribePipelineRun(
        self,
        runId,
    ):
        """
        查询指定工作流运行实例（PipelineRun）的详细信息。

        Args:
            runId: 运行 ID（必填，Query参数）

        Returns:
            baidubce.bce_response.BceResponse: 返回运行实例详情，包含 runId、pipelineId、status、startedAt、finishedAt 等

        Raises:
            ValueError: 当必填参数为空时
        """
        path = b'/'
        params = {
            'action': 'DescribePipelineRun',
            'runId': runId,
        }
        return self._send_job_request(
            http_methods.GET,
            path,
            body=json.dumps({}),
            params=params
        )
