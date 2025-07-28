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
AIHC dev instance client module.
"""
from baidubce.http import http_methods
from baidubce.services.aihc.base.aihc_base_client import AIHCBaseClient


class DevInstanceClient(AIHCBaseClient):
    """开发机相关接口客户端"""

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