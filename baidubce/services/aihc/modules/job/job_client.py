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
AIHC job client module.
"""
import json
from typing import Optional

from baidubce.http import http_methods
from baidubce.utils import required
from baidubce.services.aihc.modules.job.job_model import JobConfig
from baidubce.services.aihc.base.aihc_base_client import AIHCBaseClient


class JobClient(AIHCBaseClient):
    """任务相关接口客户端"""

    def DescribeJobs(
        self,
        resourcePoolId: str,
        queueID: Optional[str] = None,
        queue: Optional[str] = None,
        status: Optional[str] = None,
        keywordType: Optional[str] = None,
        keywork: Optional[str] = None,
        orderBy: Optional[str] = None,
        order: Optional[str] = None,
        pageNumber: int = 1,
        pageSize: int = 10
    ):
        """
        查询训练任务列表。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/xmayvctia

        Args:
            resourcePoolId: 资源池唯一标识符（必填）
            queueID: 托管资源池需传入该参数，为队列Id（可选，Query参数）
            queue: 训练任务所属队列，通用资源池须填入队列名称，不填时返回所有。托管资源池须填入队列Id（可选，Body参数）
            status: 基于状态筛选任务（可选，Body参数）
            keywordType: 筛选关键字类型（可选，Body参数）
            keywork: 关键字值，当前仅支持name/queueName（可选，Body参数）
            orderBy: 排序字段，支持createdAt，finishedAt，默认为createdAt（可选，Body参数）
            order: 排序方式，可选 [asc, desc]，asc为升序，desc为降序，默认desc（可选，Body参数）
            pageNumber: 请求分页参数，表示第几页（可选，Body参数）
            pageSize: 单页结果数，默认值为10（可选，Body参数）

        Returns:
            baidubce.bce_response.BceResponse: 返回训练任务列表

        Raises:
            ValueError: 当必填参数为空时
            TypeError: 当参数类型不匹配时
        """
        path = b'/'
        params = {
            'action': 'DescribeJobs',
            'resourcePoolId': resourcePoolId,
        }
        if queueID:
            params['queueID'] = queueID

        body = {}
        if queue is not None:
            body['queue'] = queue
        if status is not None:
            body['status'] = status
        if keywordType is not None:
            body['keywordType'] = keywordType
        if keywork is not None:
            body['keywork'] = keywork
        if orderBy is not None:
            body['orderBy'] = orderBy
        if order is not None:
            body['order'] = order
        if pageNumber is not None:
            body['pageNumber'] = pageNumber
        if pageSize is not None:
            body['pageSize'] = pageSize

        return self._send_job_request(
            http_methods.POST,
            path,
            body=json.dumps(body),
            params=params
        )
    
    def DescribeJob(self, resourcePoolId: str, jobId: str, needDetail: Optional[bool] = None):
        """
        查询训练任务详情。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Kmayvejf0

        Args:
            resourcePoolId: 资源池唯一标识符（必填）
            jobId: 任务ID（必填）
            needDetail: 是否需要详细信息（可选）

        Returns:
            baidubce.bce_response.BceResponse: 返回训练任务详情

        Raises:
            ValueError: 当必填参数为空时
            TypeError: 当参数类型不匹配时
        """
        path = b'/'
        params = {
            'action': 'DescribeJob',
            'resourcePoolId': resourcePoolId,
        }
        body = {
            'jobId': jobId,
        }
        if needDetail is not None:
            body['needDetail'] = needDetail

        return self._send_job_request(http_methods.POST, path, body=json.dumps(body), params=params)

    def DeleteJob(self, resourcePoolId, jobId):
        """
        删除训练任务。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/rmayvfzxj

        :param resourcePoolId: 资源池唯一标识符（必填，Query参数）
        :type resourcePoolId: string
        :param jobId: 训练任务ID（必填，Body参数）
        :type jobId: string
        :return: 删除结果
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'DeleteJob',
            'resourcePoolId': resourcePoolId,
        }
        body = {
            'jobId': jobId,
        }
        return self._send_job_request(http_methods.POST, path, body=json.dumps(body), params=params)

    def ModifyJob(self, resourcePoolId, jobId, priority):
        """
        更新训练任务。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Smayvhq0w

        :param resourcePoolId: 资源池唯一标识符（必填，Query参数）
        :type resourcePoolId: string
        :param jobId: 训练任务ID（必填，Body参数）
        :type jobId: string
        :param priority: 优先级（必填，Body参数），如 "normal"
        :type priority: string
        :return: 更新结果
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'ModifyJob',
            'resourcePoolId': resourcePoolId,
        }
        body = {
            'jobId': jobId,
            'priority': priority,
        }
        return self._send_job_request(http_methods.POST, path, body=json.dumps(body), params=params)

    def DescribeJobEvents(self, resourcePoolId, jobId):
        """
        查询训练任务事件。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/fmayvjaeq

        :param resourcePoolId: 资源池唯一标识符（必填，Query参数）
        :type resourcePoolId: string
        :param jobId: 训练任务ID（必填，Body参数）
        :type jobId: string
        :return: 事件列表
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'DescribeJobEvents',
            'resourcePoolId': resourcePoolId,
        }
        body = {
            'jobId': jobId,
        }
        return self._send_job_request(http_methods.POST, path, body=json.dumps(body), params=params)

    def DescribeJobLogs(self, resourcePoolId, jobId, podName=None, logType=None, 
                       startTime=None, endTime=None, chunkSize=None, marker=None):
        """
        查询训练任务日志。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Hmayvkw26

        :param resourcePoolId: 资源池唯一标识符（必填，Query参数）
        :type resourcePoolId: string
        :param jobId: 训练任务ID（必填，Body参数）
        :type jobId: string
        :param podName: Pod名称（可选，Body参数）
        :type podName: string
        :param logType: 日志类型，如"stdout"、"stderr"（可选，Body参数）
        :type logType: string
        :param startTime: 日志起始时间，格式"yyyy-MM-dd HH:mm:ss"（可选，Body参数）
        :type startTime: string
        :param endTime: 日志结束时间，格式"yyyy-MM-dd HH:mm:ss"（可选，Body参数）
        :type endTime: string
        :param chunkSize: 日志聚合条数，默认1（可选，Body参数）
        :type chunkSize: int
        :param marker: 日志查询标识符（可选，Body参数）
        :type marker: string
        :return: 日志查询结果
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'DescribeJobLogs',
            'resourcePoolId': resourcePoolId,
        }
        body = {
            'jobId': jobId,
        }
        if podName is not None:
            body['podName'] = podName
        if logType is not None:
            body['logType'] = logType
        if startTime is not None:
            body['startTime'] = startTime
        if endTime is not None:
            body['endTime'] = endTime
        if chunkSize is not None:
            body['chunkSize'] = chunkSize
        if marker is not None:
            body['marker'] = marker

        return self._send_job_request(
            http_methods.POST,
            path,
            body=json.dumps(body),
            params=params
        )

    def DescribeJobPodEvents(self, resourcePoolId, jobId, podName, startTime=None, endTime=None):
        """
        查询训练任务Pod事件。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/mmayvm8tb

        :param resourcePoolId: 资源池唯一标识符（必填，Query参数）
        :type resourcePoolId: string
        :param jobId: 训练任务ID（必填，Body参数）
        :type jobId: string
        :param podName: 训练任务节点名称（必填，Body参数）
        :type podName: string
        :param startTime: 事件起始时间（可选，Body参数）
        :type startTime: string
        :param endTime: 事件结束时间（可选，Body参数）
        :type endTime: string
        :return: Pod事件查询结果
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'DescribeJobPodEvents',
            'resourcePoolId': resourcePoolId,
        }
        body = {
            'jobId': jobId,
            'podName': podName,
        }
        if startTime is not None:
            body['startTime'] = startTime
        if endTime is not None:
            body['endTime'] = endTime

        return self._send_job_request(
            http_methods.POST,
            path,
            body=json.dumps(body),
            params=params
        )

    def StopJob(self, resourcePoolId, jobId):
        """
        停止训练任务。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/0mayvnkik

        :param resourcePoolId: 资源池唯一标识符（必填，Query参数）
        :type resourcePoolId: string
        :param jobId: 训练任务ID（必填，Body参数）
        :type jobId: string
        :return: 停止任务结果
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'StopJob',
            'resourcePoolId': resourcePoolId,
        }
        body = {
            'jobId': jobId,
        }
        return self._send_job_request(
            http_methods.POST,
            path,
            body=json.dumps(body),
            params=params
        )

    def DescribeJobNodeNames(self, resourcePoolId, jobId):
        """
        查询训练任务所在节点列表。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/2mayvq994

        :param resourcePoolId: 资源池唯一标识符（必填，Query参数）
        :type resourcePoolId: string
        :param jobId: 训练任务ID（必填，Body参数）
        :type jobId: string
        :return: 节点名称列表
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'DescribeJobNodeNames',
            'resourcePoolId': resourcePoolId,
        }
        body = {
            'jobId': jobId,
        }
        return self._send_job_request(
            http_methods.POST,
            path,
            body=json.dumps(body),
            params=params
        )

    def GetJobWebTerminalUrl(self, resourcePoolId, jobId, handshakeTimeoutSecond=None, pingTimeoutSecond=None):
        """
        获取训练任务WebTerminal地址。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/9mayvri1t

        :param resourcePoolId: 资源池唯一标识符（必填，Query参数）
        :type resourcePoolId: string
        :param jobId: 训练任务ID（必填，Body参数）
        :type jobId: string
        :param handshakeTimeoutSecond: 连接超时参数，单位秒（可选，Body参数）
        :type handshakeTimeoutSecond: int
        :param pingTimeoutSecond: 心跳超时参数，单位秒（可选，Body参数）
        :type pingTimeoutSecond: int
        :return: WebTerminal地址
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'GetJobWebTerminalUrl',
            'resourcePoolId': resourcePoolId,
        }
        body = {
            'jobId': jobId,
        }
        if handshakeTimeoutSecond is not None:
            body['handshakeTimeoutSecond'] = handshakeTimeoutSecond
        if pingTimeoutSecond is not None:
            body['pingTimeoutSecond'] = pingTimeoutSecond

        return self._send_job_request(
            http_methods.POST,
            path,
            body=json.dumps(body),
            params=params
        )

    def CreateJob(self, resourcePoolId, jobConfig):
        """
        创建训练任务。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Hmayv96tj

        :param resourcePoolId: 资源池唯一标识符（必填，Query参数）
        :type resourcePoolId: string
        :param jobConfig: 训练任务配置（必填，Body参数，dict类型，需包含jobName、image、resources等）
        :type jobConfig: dict
        :return: 创建任务结果
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'CreateJob',
            'resourcePoolId': resourcePoolId,
        }
        body = jobConfig
        return self._send_job_request(
            http_methods.POST,
            path,
            body=json.dumps(body),
            params=params
        ) 