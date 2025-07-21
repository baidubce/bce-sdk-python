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
import copy
import json
import sys
import uuid

from baidubce import bce_base_client, utils, compat
from baidubce.auth import bce_v1_signer
from baidubce.http import handler, bce_http_client, http_methods
from baidubce.services.aihc import aihc_model
from baidubce.services.aihc import aihc_handler
from baidubce.utils import required

class AIHCV2Client(bce_base_client.BceBaseClient):
    """
    AIHC V2 base sdk client
    """

    version = b'v2'

    def __init__(self, config=None):
        bce_base_client.BceBaseClient.__init__(self, config)

    def _merge_config(self, config=None):
        if config is None:
            return self.config
        else:
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    def _send_request(self, http_method, path,
                      body=None, headers=None, params=None,
                      config=None, body_parser=None):
        config = self._merge_config(config)
        if body_parser is None:
            body_parser = aihc_handler.parse_json
        
        if headers is None:
            headers = {
                b'version': AIHCV2Client.version
            }
        else:
            headers[b'version'] = AIHCV2Client.version

        return bce_http_client.send_request(
            config, bce_v1_signer.sign, [handler.parse_error, body_parser],
            http_method, path, body, headers, params)
    
    def _send_job_request(self, http_method, path,
                      body=None, headers=None, params=None,
                      config=None, body_parser=None):
        config = self._merge_config(config)
        if body_parser is None:
            body_parser = aihc_handler.parse_json
        
        if headers is None:
            headers = {
                b'X-API-Version': AIHCV2Client.version
            }
        else:
            headers[b'X-API-Version'] = AIHCV2Client.version

        return bce_http_client.send_request(
            config, bce_v1_signer.sign, [handler.parse_error, body_parser],
            http_method, path, body, headers, params)

# ============任务相关接口============
    @required(pageNumber=int, pageSize=int)
    def DescribeJobs(
        self,
        resourcePoolId,
        queueID=None,
        queue=None,
        status=None,
        keywordType=None,
        keywork=None,
        orderBy=None,
        order=None,
        pageNumber=1,
        pageSize=10
    ):
        """
        查询训练任务列表。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/xmayvctia

        :param resourcePoolId:
            资源池唯一标识符（必填）
        :type resourcePoolId: string

        :param queueID:
            托管资源池需传入该参数，为队列Id（可选，Query参数）
        :type queueID: string

        :param queue:
            训练任务所属队列，通用资源池须填入队列名称，不填时返回所有。托管资源池须填入队列Id（可选，Body参数）
        :type queue: string

        :param status:
            基于状态筛选任务（可选，Body参数）
        :type status: string

        :param keywordType:
            筛选关键字类型（可选，Body参数）
        :type keywordType: string

        :param keywork:
            关键字值，当前仅支持name/queueName（可选，Body参数）
        :type keywork: string

        :param orderBy:
            排序字段，支持createdAt，finishedAt，默认为createdAt（可选，Body参数）
        :type orderBy: string

        :param order:
            排序方式，可选 [asc, desc]，asc为升序，desc为降序，默认desc（可选，Body参数）
        :type order: string

        :param pageNumber:
            请求分页参数，表示第几页（可选，Body参数）
        :type pageNumber: int

        :param pageSize:
            单页结果数，默认值为10（可选，Body参数）
        :type pageSize: int

        :return:
            返回训练任务列表
        :rtype: baidubce.bce_response.BceResponse
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
    
    @required(needDetail=bool)
    def DescribeJob(self, resourcePoolId, jobId, needDetail=None):
        """
        查询训练任务详情。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Kmayvejf0

        :param resourcePoolId:
            资源池唯一标识符（必填，Query参数）
        :type resourcePoolId: string

        :param jobId:
            训练任务ID（必填，Body参数）
        :type jobId: string

        :param needDetail:
            是否需要详细信息，true时返回Pod及历史Pod列表（可选，Body参数）
        :type needDetail: bool

        :return:
            返回训练任务详情
        :rtype: baidubce.bce_response.BceResponse
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

    def UpdateJob(self, resourcePoolId, jobId, priority):
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
            'action': 'UpdateJob',
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

    @required(podName=str, logType=str, startTime=str, endTime=str, chunkSize=int, marker=str)
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

    @required(handshakeTimeoutSecond=int, pingTimeoutSecond=int)
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

    @required(jobConfig=aihc_model.JobConfig)
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

# ============数据集相关接口============
    def DescribeDatasets(
        self,
        keyword=None,
        storageType=None,
        storageInstances=None,
        importFormat=None,
        pageNumber=1,
        pageSize=None
    ):
        """
        获取数据集列表。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Emc099va4

        :param keyword: 名称关键字（可选，Query参数）
        :type keyword: str
        :param storageType: 存储类型（可选，Query参数）
        :type storageType: str
        :param storageInstances: 存储实例列表，英文逗号分隔（可选，Query参数）
        :type storageInstances: str
        :param importFormat: 导入格式（可选，Query参数）
        :type importFormat: str
        :param pageNumber: 页码，默认1（可选，Query参数）
        :type pageNumber: int
        :param pageSize: 每页数量，不传递该参数默认返回全部（可选，Query参数）
        :type pageSize: int
        :return: 数据集列表及总数
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'DescribeDatasets',
            'pageNumber': pageNumber,
        }
        if keyword is not None:
            params['keyword'] = keyword
        if storageType is not None:
            params['storageType'] = storageType
        if storageInstances is not None:
            params['storageInstances'] = storageInstances
        if importFormat is not None:
            params['importFormat'] = importFormat
        if pageSize is not None:
            params['pageSize'] = pageSize

        return self._send_request(
            http_methods.GET,
            path,
            params=params
        )

    def DescribeDataset(self, datasetId):
        """
        获取数据集详情。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Umc0988jj

        :param datasetId: 数据集ID（必填，Query参数）
        :type datasetId: str
        :return: 数据集详情
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'DescribeDataset',
            'datasetId': datasetId,  # 必须为 datasetId
        }
        return self._send_request(
            http_methods.GET,
            path,
            params=params
        )

    def UpdateDataset(self, datasetId, name=None, description=None, visibilityScope=None, 
                    visibilityUser=None, visibilityGroup=None):
        """
        修改数据集。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Imc095v8z

        :param datasetId: 数据集ID（必填，Query参数）
        :type datasetId: str
        :param name: 数据集名称（可选，Body参数）
        :type name: str
        :param description: 数据集描述（可选，Body参数）
        :type description: str
        :param visibilityScope: 可见范围（可选，Body参数）
        :type visibilityScope: str
        :param visibilityUser: 用户权限列表（可选，Body参数，List[dict]）
        :type visibilityUser: list
        :param visibilityGroup: 用户组权限列表（可选，Body参数，List[dict]）
        :type visibilityGroup: list
        :return: 修改结果
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'UpdateDataset',
            'datasetId': datasetId,
        }
        body = {}
        if name is not None:
            body['name'] = name
        if description is not None:
            body['description'] = description
        if visibilityScope is not None:
            body['visibilityScope'] = visibilityScope
        if visibilityUser is not None:
            body['visibilityUser'] = visibilityUser
        if visibilityGroup is not None:
            body['visibilityGroup'] = visibilityGroup
        return self._send_request(
            http_methods.POST,
            path,
            body=json.dumps(body),
            params=params
        )

    def DeleteDataset(self, datasetId):
        """
        删除数据集，同时删除所有版本。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/wmc09407x

        :param datasetId: 数据集ID（必填，Query参数）
        :type datasetId: str
        :return: 删除结果
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'DeleteDataset',
            'datasetId': datasetId,
        }
        return self._send_request(
            http_methods.POST,
            path,
            params=params
        )

    def CreateDataset(self, name, storageType, storageInstance, importFormat, description=None, 
                    owner=None, visibilityScope=None, visibilityUser=None, visibilityGroup=None, 
                    initVersionEntry=None):
        """
        创建数据集。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Dmc091fap

        :param name: 数据集名称（必填，Body参数）
        :type name: str
        :param storageType: 存储类型（必填，Body参数）
        :type storageType: str
        :param storageInstance: 存储实例ID（必填，Body参数）
        :type storageInstance: str
        :param importFormat: 导入格式（必填，Body参数）
        :type importFormat: str
        :param description: 数据集描述（可选，Body参数）
        :type description: str
        :param owner: 拥有者ID（可选，Body参数）
        :type owner: str
        :param visibilityScope: 可见范围（可选，Body参数）
        :type visibilityScope: str
        :param visibilityUser: 用户权限列表（可选，Body参数，List[dict]）
        :type visibilityUser: list
        :param visibilityGroup: 用户组权限列表（可选，Body参数，List[dict]）
        :type visibilityGroup: list
        :param initVersionEntry: 初始版本信息（可选，Body参数，dict）
        :type initVersionEntry: dict
        :return: 创建结果
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'CreateDataset',
        }
        body = {
            'name': name,
            'storageType': storageType,
            'storageInstance': storageInstance,
            'importFormat': importFormat,
        }
        if description is not None:
            body['description'] = description
        if owner is not None:
            body['owner'] = owner
        if visibilityScope is not None:
            body['visibilityScope'] = visibilityScope
        if visibilityUser is not None:
            body['visibilityUser'] = visibilityUser
        if visibilityGroup is not None:
            body['visibilityGroup'] = visibilityGroup
        if initVersionEntry is not None:
            body['initVersionEntry'] = initVersionEntry
        return self._send_request(
            http_methods.POST,
            path,
            body=json.dumps(body),
            params=params
        )

    def DescribeDatasetVersions(self, datasetId, pageNumber=1, pageSize=10):
        """
        获取数据集版本列表。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Tmc09d4k0

        :param datasetId: 数据集ID（必填，Query参数）
        :type datasetId: str
        :param pageNumber: 页码，默认1（可选，Query参数）
        :type pageNumber: int
        :param pageSize: 每页数量，默认10（可选，Query参数）
        :type pageSize: int
        :return: 数据集版本列表及总数
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'DescribeDatasetVersions',
            'datasetId': datasetId,
            'pageNumber': pageNumber,
            'pageSize': pageSize,
        }
        return self._send_request(
            http_methods.GET,
            path,
            params=params
        )

    def DescribeDatasetVersion(self, versionId):
        """
        获取数据集版本详情。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Dmc09bpj1

        :param versionId: 数据集版本ID（必填，Query参数）
        :type versionId: str
        :return: 数据集版本详情
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'DescribeDatasetVersion',
            'versionId': versionId,
        }
        return self._send_request(
            http_methods.GET,
            path,
            params=params
        )

    def DeleteDatasetVersion(self, datasetId, versionId):
        """
        删除数据集版本。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Omc09gd0f

        :param datasetId: 数据集ID（必填，Query参数）
        :type datasetId: str
        :param versionId: 数据集版本ID（必填，Query参数）
        :type versionId: str
        :return: 删除结果
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'DeleteDatasetVersion',
            'datasetId': datasetId,
            'versionId': versionId,
        }
        return self._send_request(
            http_methods.POST,
            path,
            params=params
        )

    def CreateDatasetVersion(self, datasetId, storagePath, mountPath, description=None):
        """
        创建数据集版本。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/hmc09en7q

        :param datasetId: 数据集ID（必填，Query参数）
        :type datasetId: str
        :param storagePath: 存储路径（必填，Body参数）
        :type storagePath: str
        :param mountPath: 默认挂载路径（必填，Body参数）
        :type mountPath: str
        :param description: 版本描述（可选，Body参数）
        :type description: str
        :return: 创建结果
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'CreateDatasetVersion',
            'datasetId': datasetId,
        }
        body = {
            'storagePath': storagePath,
            'mountPath': mountPath,
        }
        if description is not None:
            body['description'] = description
        return self._send_request(
            http_methods.POST,
            path,
            body=json.dumps(body),
            params=params
        )

# ============模型相关接口============
    def DescribeModels(self, keyword=None, modelFormat=None, owner=None, visibilityScope=None, 
                     pageNumber=1, pageSize=None):
        """
        获取模型列表。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/amc1fmz95

        :param keyword: 名称关键字（可选，Query参数）
        :type keyword: str
        :param modelFormat: 模型格式（可选，Query参数）
        :type modelFormat: str
        :param owner: 拥有者ID（可选，Query参数）
        :type owner: str
        :param visibilityScope: 可见范围（可选，Query参数）
        :type visibilityScope: str
        :param pageNumber: 页码，默认1（可选，Query参数）
        :type pageNumber: int
        :param pageSize: 每页数量，不传递该参数默认返回全部（可选，Query参数）
        :type pageSize: int
        :return: 模型列表及总数
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'DescribeModels',
            'pageNumber': pageNumber,
        }
        if keyword is not None:
            params['keyword'] = keyword
        if modelFormat is not None:
            params['modelFormat'] = modelFormat
        if owner is not None:
            params['owner'] = owner
        if visibilityScope is not None:
            params['visibilityScope'] = visibilityScope
        if pageSize is not None:
            params['pageSize'] = pageSize
        return self._send_request(
            http_methods.GET,
            path,
            params=params
        )

    def CreateModel(self, name, modelFormat, description=None, owner=None, visibilityScope=None, initVersionEntry=None):
        """
        创建模型。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/2mc1f9d4p

        :param name: 模型名称（必填，Body参数）
        :type name: str
        :param modelFormat: 模型格式（必填，Body参数）
        :type modelFormat: str
        :param description: 模型描述（可选，Body参数）
        :type description: str
        :param owner: 拥有者ID（可选，Body参数）
        :type owner: str
        :param visibilityScope: 可见范围（可选，Body参数）
        :type visibilityScope: str
        :param initVersionEntry: 初始版本信息（可选，Body参数，dict）
        :type initVersionEntry: dict
        :return: 创建结果
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'CreateModel',
        }
        body = {
            'name': name,
            'modelFormat': modelFormat,
        }
        if description is not None:
            body['description'] = description
        if owner is not None:
            body['owner'] = owner
        if visibilityScope is not None:
            body['visibilityScope'] = visibilityScope
        if initVersionEntry is not None:
            body['initVersionEntry'] = initVersionEntry
        return self._send_request(
            http_methods.POST,
            path,
            body=json.dumps(body),
            params=params
        )

    def DeleteModel(self, modelId):
        """
        删除模型，同时删除所有版本。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Mmc1fikgf

        :param modelId: 模型ID（必填，Query参数）
        :type modelId: str
        :return: 删除结果
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'DeleteModel',
            'modelId': modelId,
        }
        return self._send_request(
            http_methods.POST,
            path,
            params=params
        )

    def ModifyModel(self, modelId, name, description):
        """
        修改模型。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/hmc1fk2zd

        :param modelId: 模型ID（必填，Query参数）
        :type modelId: str
        :param name: 模型名称（必填，Body参数）
        :type name: str
        :param description: 描述（必填，Body参数）
        :type description: str
        :return: 修改结果
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'ModifyModel',
            'modelId': modelId,
        }
        body = {
            'name': name,
            'description': description,
        }
        return self._send_request(
            http_methods.POST,
            path,
            body=json.dumps(body),
            params=params
        )

    def DescribeModel(self, modelId):
        """
        获取模型详情。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Xmc1flhmc

        :param modelId: 模型ID（必填，Query参数）
        :type modelId: str
        :return: 模型详情
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'DescribeModel',
            'modelId': modelId,
        }
        return self._send_request(
            http_methods.GET,
            path,
            params=params
        )

    def DescribeModelVersions(self, modelId, pageNumber=1, pageSize=10):
        """
        获取模型版本列表。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Lmc1fr4lc

        :param modelId: 模型ID（必填，Query参数）
        :type modelId: str
        :param pageNumber: 页码，默认1（可选，Query参数）
        :type pageNumber: int
        :param pageSize: 每页数量，默认10（可选，Query参数）
        :type pageSize: int
        :return: 模型版本列表及总数
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'DescribeModelVersions',
            'modelId': modelId,
            'pageNumber': pageNumber,
            'pageSize': pageSize,
        }
        return self._send_request(
            http_methods.GET,
            path,
            params=params
        )

    def DescribeModelVersion(self, versionId):
        """
        获取模型版本详情。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/wmc1focnv

        :param versionId: 模型版本ID（必填，Query参数）
        :type versionId: str
        :return: 模型版本详情
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'DescribeModelVersion',
            'versionId': versionId,
        }
        return self._send_request(
            http_methods.GET,
            path,
            params=params
        )

    def CreateModelVersion(self, modelId, storageBucket, storagePath, source, description=None, modelMetrics=None):
        """
        新建模型版本。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/imc1fsm39

        :param modelId: 模型ID（必填，Query参数）
        :type modelId: str
        :param storageBucket: 存储桶（必填，Body参数）
        :type storageBucket: str
        :param storagePath: 存储路径（必填，Body参数）
        :type storagePath: str
        :param source: 来源（必填，Body参数），如 UserUpload
        :type source: str
        :param description: 描述（可选，Body参数）
        :type description: str
        :param modelMetrics: 模型指标，JSON字符串（可选，Body参数）
        :type modelMetrics: str
        :return: 新建模型版本结果
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'CreateModelVersion',
            'modelId': modelId,
        }
        body = {
            'storageBucket': storageBucket,
            'storagePath': storagePath,
            'source': source,
        }
        if description is not None:
            body['description'] = description
        if modelMetrics is not None:
            body['modelMetrics'] = modelMetrics
        return self._send_request(
            http_methods.POST,
            path,
            body=json.dumps(body),
            params=params
        )

    def DeleteModelVersion(self, modelId, versionId):
        """
        删除模型版本。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/nmc1ftz7x

        :param modelId: 模型ID（必填，Query参数）
        :type modelId: str
        :param versionId: 模型版本ID（必填，Query参数）
        :type versionId: str
        :return: 删除结果
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'DeleteModelVersion',
            'modelId': modelId,
            'versionId': versionId,
        }
        return self._send_request(
            http_methods.POST,
            path,
            params=params
        )

# ============在线服务部署相关接口============

    def DescribeServices(self, resourcePoolId=None, queueName=None, name=None, region=None, pageNumber=1, pageSize=10):
        """
        拉取服务列表。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Imb4v5905

        :param resourcePoolId: 资源池ID（可选，Query参数）
        :type resourcePoolId: str
        :param queueName: 队列名称（可选，Query参数）
        :type queueName: str
        :param name: 服务名称（可选，Query参数）
        :type name: str
        :param region: 区域（可选，Query参数）
        :type region: str
        :param pageNumber: 页码，默认1（可选，Query参数）
        :type pageNumber: int
        :param pageSize: 每页数量，默认10（可选，Query参数）
        :type pageSize: int
        :return: 服务列表及总数
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'DescribeServices',
            'pageNumber': pageNumber,
            'pageSize': pageSize,
        }
        if resourcePoolId is not None:
            params['resourcePoolId'] = resourcePoolId
        if queueName is not None:
            params['queueName'] = queueName
        if name is not None:
            params['name'] = name
        if region is not None:
            params['region'] = region
        return self._send_request(
            http_methods.GET,
            path,
            params=params
        )

    def DescribeService(self, serviceId):
        """
        查询服务详情。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/4mb4v7wn5

        :param serviceId: 服务ID（必填，Query参数）
        :type serviceId: str
        :return: 服务详情
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'DescribeService',
            'serviceId': serviceId,
        }
        return self._send_request(
            http_methods.GET,
            path,
            params=params
        )

    def DescribeServiceStatus(self, serviceId):
        """
        获取服务状态。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/dmb4v6oh0

        :param serviceId: 服务ID（必填，Query参数）
        :type serviceId: str
        :return: 服务状态信息
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'DescribeServiceStatus',
            'serviceId': serviceId,
        }
        return self._send_request(
            http_methods.GET,
            path,
            params=params
        )

# ============开发机相关接口============
    def DescribeDevInstances(
        self,
        resourcePoolId=None,
        queueName=None,
        status=None,
        onlyMyDevs=None,
        queryKey=None,
        queryVal=None,
        pageNumber=1,
        pageSize=10
    ):
        """
        查询开发机列表。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Nmbkpgnrm

        :param resourcePoolId: 资源池ID（可选，Query参数）
        :type resourcePoolId: str
        :param queueName: 队列名称（可选，Query参数）
        :type queueName: str
        :param status: 开发机状态（可选，Query参数）
        :type status: str
        :param onlyMyDevs: 是否只看自己开发机（可选，Query参数，"true"/"false"）
        :type onlyMyDevs: str
        :param queryKey: 过滤key（可选，Query参数，devInstanceName/devInstanceId/creator）
        :type queryKey: str
        :param queryVal: 过滤value（可选，Query参数，和queryKey配套）
        :type queryVal: str
        :param pageNumber: 页码，默认1（可选，Query参数）
        :type pageNumber: int
        :param pageSize: 每页数量，默认10（可选，Query参数）
        :type pageSize: int
        :return: 开发机列表及总数
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'DescribeDevInstances',
            'pageNumber': pageNumber,
            'pageSize': pageSize,
        }
        if resourcePoolId is not None:
            params['resourcePoolId'] = resourcePoolId
        if queueName is not None:
            params['queueName'] = queueName
        if status is not None:
            params['status'] = status
        if onlyMyDevs is not None:
            params['onlyMyDevs'] = onlyMyDevs
        if queryKey is not None:
            params['queryKey'] = queryKey
        if queryVal is not None:
            params['queryVal'] = queryVal
        return self._send_request(
            http_methods.GET,
            path,
            params=params
        )

    def DescribeDevInstance(self, devInstanceId):
        """
        查询开发机详情。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/dmbkphznw

        :param devInstanceId: 开发机实例ID（必填，Query参数）
        :type devInstanceId: str
        :return: 开发机详情
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'DescribeDevInstance',
            'devInstanceId': devInstanceId,
        }
        return self._send_request(
            http_methods.GET,
            path,
            params=params
        )

    def StartDevInstance(self, devInstanceId):
        """
        开启开发机实例。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Fmbkovqsa

        :param devInstanceId: 开发机实例ID（必填，Query参数）
        :type devInstanceId: str
        :return: 开启结果
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'StartDevInstance',
            'devInstanceId': devInstanceId,
        }
        return self._send_request(
            http_methods.POST,
            path,
            params=params
        )

    def StopDevInstance(self, devInstanceId):
        """
        停止开发机实例。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Ymbkoethu

        :param devInstanceId: 开发机实例ID（必填，Query参数）
        :type devInstanceId: str
        :return: 停止结果
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'StopDevInstance',
            'devInstanceId': devInstanceId,
        }
        return self._send_request(
            http_methods.POST,
            path,
            params=params
        )