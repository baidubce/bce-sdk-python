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
AIHC service client module.
"""
from baidubce.http import http_methods
from baidubce.services.aihc.base.aihc_base_client import AIHCBaseClient


class ServiceClient(AIHCBaseClient):
    """在线服务相关接口客户端"""

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