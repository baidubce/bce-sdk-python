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

from baidubce.http import http_methods
from baidubce.services.aihc.base.aihc_base_client import AIHCBaseClient


class JobClient(AIHCBaseClient):
    """任务相关接口客户端"""

    def DescribeJobs(
        self,
        resourcePoolId,
        queueID=None,
        queue=None,
        status=None,
        keywordType=None,
        keyword=None,
        orderBy=None,
        order=None,
        pageNumber=1,
        pageSize=10
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
            keyword: 关键字值，当前仅支持name/queueName（可选，Body参数）
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
        if keyword is not None:
            body['keyword'] = keyword
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

    def DescribeJob(
        self,
        resourcePoolId,
        queueID,
        jobId,
        needDetail=None
    ):
        """
        查询训练任务详情。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Kmayvejf0

        Args:
            resourcePoolId: 资源池唯一标识符（必填，Query参数）
            queueID: 训练任务所属队列，自运维资源池须填入队列名称，托管资源池须填入队列Id（必填，Query参数）
            jobId: 任务ID（必填，Body参数）
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
            'queueID': queueID,
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

        Args:
            resourcePoolId: 资源池唯一标识符（必填，Query参数）
            resourcePoolId: string
            jobId: 训练任务ID（必填，Body参数）
            jobId: string

        Returns:
            baidubce.bce_response.BceResponse: 删除任务结果

        Raises:
            ValueError: 当必填参数为空时
            TypeError: 当参数类型不匹配时
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

        Args:
            resourcePoolId: 资源池唯一标识符（必填，Query参数）
            jobId: 训练任务ID（必填，Body参数）
            priority: 优先级（必填，Body参数），如 "normal"

        Returns:
            baidubce.bce_response.BceResponse: 更新任务结果

        Raises:
            ValueError: 当必填参数为空时
            TypeError: 当参数类型不匹配时
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

    def DescribeJobEvents(
        self,
        resourcePoolId,
        jobId,
        startTime=None,
        endTime=None
    ):
        """
        查询训练任务事件。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/fmayvjaeq

        Args:
            resourcePoolId: 资源池唯一标识符（必填，Query参数）
            jobId: 训练任务ID（必填，Body参数）
            startTime: 获取任务事件的起始时间（可选，Body参数）
            endTime: 获取任务事件的结束时间（可选，Body参数）

        Returns:
            baidubce.bce_response.BceResponse: 训练任务事件结果

        Raises:
            ValueError: 当必填参数为空时
            TypeError: 当参数类型不匹配时
        """
        path = b'/'
        params = {
            'action': 'DescribeJobEvents',
            'resourcePoolId': resourcePoolId,
        }
        body = {
            'jobId': jobId,
        }
        if startTime is not None:
            body['startTime'] = startTime
        if endTime is not None:
            body['endTime'] = endTime
        return self._send_job_request(http_methods.POST, path, body=json.dumps(body), params=params)

    def DescribeJobLogs(
        self,
        resourcePoolId,
        jobId,
        podName,
        keywords=None,
        startTime=None,
        endTime=None,
        maxLines=None,
        chunkSize=None,
        marker=None
    ):
        """
        查询训练任务日志。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Hmayvkw26

        Args:
            resourcePoolId: 资源池唯一标识符（必填，Query参数）
            jobId: 训练任务ID（必填，Body参数）
            podName: Pod名称（必填，Body参数）
            keywords: 日志查询关键字（可选，Body参数）
            startTime: 日志起始时间，Unix时间格式（可选，Body参数）
            endTime: 日志结束时间，Unix时间格式（可选，Body参数）
            maxLines：日志的最大行数（可选，Body参数）
            chunkSize: 日志聚合条数，默认1（可选，Body参数）
            marker: 日志查询标识符（可选，Body参数）

        Returns:
            baidubce.bce_response.BceResponse: 日志查询结果

        Raises:
            ValueError: 当必填参数为空时
            TypeError: 当参数类型不匹配时
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
        if keywords is not None:
            body['keywords'] = keywords
        if startTime is not None:
            body['startTime'] = startTime
        if endTime is not None:
            body['endTime'] = endTime
        if maxLines is not None:
            body['maxLines'] = maxLines
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

    def DescribeJobPodEvents(
        self,
        resourcePoolId,
        jobId,
        podName,
        startTime=None,
        endTime=None,
    ):
        """
        查询训练任务Pod事件。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/mmayvm8tb

        Args:
            resourcePoolId: 资源池唯一标识符（必填，Query参数）
            jobId: 训练任务ID（必填，Body参数）
            podName: 训练任务节点名称（必填，Body参数）
            startTime: 事件起始时间，Unix时间格式（可选，Body参数）
            endTime: 事件结束时间，Unix时间格式（可选，Body参数）

        Returns:
            baidubce.bce_response.BceResponse: Pod事件查询结果

        Raises:
            ValueError: 当必填参数为空时
            TypeError: 当参数类型不匹配时
        """
        path = b'/'
        params = {
            'action': 'DescribePodEvents',
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

        Args:
            resourcePoolId: 资源池唯一标识符（必填，Query参数）
            jobId: 训练任务ID（必填，Body参数）

        Returns:
            baidubce.bce_response.BceResponse: 停止任务结果

        Raises:
            ValueError: 当必填参数为空时
            TypeError: 当参数类型不匹配时
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

    def DescribeJobNodes(self, resourcePoolId, jobId):
        """
        查询训练任务所在节点列表。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/2mayvq994

        Args:
            resourcePoolId: 资源池唯一标识符（必填，Query参数）
            jobId: 训练任务ID（必填，Body参数）

        Returns:
            baidubce.bce_response.BceResponse: 节点名称列表

        Raises:
            ValueError: 当必填参数为空时
            TypeError: 当参数类型不匹配时
        """
        path = b'/'
        params = {
            'action': 'DescribeJobNodes',
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

    def DescribeJobWebterminal(
        self,
        resourcePoolId,
        jobId,
        podName,
        handshakeTimeoutSecond=None,
        pingTimeoutSecond=None
    ):
        """
        获取训练任务WebTerminal地址。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/9mayvri1t

        Args:
            resourcePoolId: 资源池唯一标识符（必填，Query参数）
            jobId: 训练任务ID（必填，Body参数）
            podName: 训练任务节点名称（必填，Body参数）
            handshakeTimeoutSecond: 连接超时参数，单位秒（可选，Body参数）
            pingTimeoutSecond: 心跳超时参数，单位秒（可选，Body参数）

        Returns:
            baidubce.bce_response.BceResponse: WebTerminal地址

        Raises:
            ValueError: 当必填参数为空时
            TypeError: 当参数类型不匹配时
        """
        path = b'/'
        params = {
            'action': 'DescribeJobWebterminal',
            'resourcePoolId': resourcePoolId,
        }
        body = {
            'jobId': jobId,
            'podName': podName,
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

    def CreateJob(
            self,
            resourcePoolId,
            queueID,
            name,
            command,
            jobSpec,
            jobType=None,
            labels=None,
            priority=None,
            dataSources=None,
            enableBccl=None,
            faultTolerance=None,
            faultToleranceArgs=None,
            tensorboardConfig=None,
            alertConfig=None,
            retentionPeriod=None,
    ):
        """
        创建训练任务。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Hmayv96tj

        Args:
            resourcePoolId: 资源池唯一标识符（必填，Query参数）
            queueID: 训练任务所属队列，通用资源池须填入队列名称，托管资源池须填入队列Id（必填，Query参数）
            name: 训练任务名称（必填，Body参数）
            command: 启动命令（必填，Body参数）
            jobSpec: 训练任务配置（必填，Body参数）
            jobType: 分布式框架，只支持 PyTorchJob（可选，Body参数，默认："PyTorchJob"）
            labels: 训练任务标签（可选，Body参数）
            priority: 调度优先级，支持高（high）、中（normal）、低（low）（可选，Body参数，默认："normal"）
            dataSources: 数据源配置，当前支持PFS（可选，Body参数）
            enableBccl: 是否开启BCCL自动注入（可选，Body参数，默认：False）
            faultTolerance: 是否开启容错（可选，Body参数，默认：False）
            faultToleranceArgs: 容错配置（可选，Body参数）
            tensorboardConfig: tensorboard相关配置（可选，Body参数）
            alertConfig: 告警相关配置（可选，Body参数）
            retentionPeriod: 任务保留时间，格式1m、1h、1d，分别代表一分钟、一小时、一天（可选，Body参数）

        Returns:
            baidubce.bce_response.BceResponse: 创建任务结果

        Raises:
            ValueError: 当必填参数为空时
            TypeError: 当参数类型不匹配时
        """
        path = b'/'
        params = {
            'action': 'CreateJob',
            'resourcePoolId': resourcePoolId,
            'queueID': queueID,
        }
        body = {
            'name': name,
            'command': command,
            'jobSpec': jobSpec,
            'enableBccl': enableBccl,
            'faultTolerance': faultTolerance,
        }
        if jobType is not None:
            body['jobType'] = jobType
        if priority is not None:
            body['priority'] = priority
        if labels is not None:
            body['labels'] = labels
        if dataSources is not None:
            body['datasources'] = dataSources
        if faultToleranceArgs is not None:
            body['faultToleranceArgs'] = faultToleranceArgs
        if tensorboardConfig is not None:
            body['tensorboardConfig'] = tensorboardConfig
        if alertConfig is not None:
            body['alertConfig'] = alertConfig
        if retentionPeriod is not None:
            body['retentionPeriod'] = retentionPeriod
        return self._send_job_request(
            http_methods.POST,
            path,
            body=json.dumps(body),
            params=params
        )

    def DescribeJobMetrics(
        self,
        resourcePoolId,
        jobId,
        metricType,
        startTime=None,
        endTime=None,
        timeStep=None,
        rateInterval=None
    ):
        """
        查询训练任务监控。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/fmayvjaeq

        Args:
            resourcePoolId: 资源池唯一标识符（必填，Query参数）
            jobId: 任务ID（必填，Body参数）
            metricType: 查询监控数据的指标类型（必填，Body参数）
            startTime: 开始时间，Unix时间格式（可选，Body参数）
            endTime: 结束时间，Unix时间格式（可选，Body参数）
            timeStep: 返回监控数据的时间间隔（可选，Body参数）
            rateInterval: 指标变化周期频率，默认为5分钟（可选，Body参数）

        Returns:
            baidubce.bce_response.BceResponse: 返回训练任务指标数据

        Raises:
            ValueError: 当必填参数为空时
            TypeError: 当参数类型不匹配时
        """
        path = b'/'
        params = {
            'action': 'DescribeJobMetrics',
            'resourcePoolId': resourcePoolId,
        }

        body = {
            'jobId': jobId,
            'metricType': metricType,
        }
        optional_boy_params = {
            'startTime': startTime,
            'endTime': endTime,
            'timeStep': timeStep,
            'rateInterval': rateInterval
        }
        body.update({k: v for k, v in optional_boy_params.items() if v is not None})
        return self._send_job_request(
            http_methods.POST,
            path,
            body=json.dumps(body),
            params=params
        )