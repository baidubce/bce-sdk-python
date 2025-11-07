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
AIHC resource pool client module.
"""

from baidubce.http import http_methods
from baidubce.services.aihc.base.aihc_base_client import AIHCBaseClient


class ResourcePoolClient(AIHCBaseClient):
    """资源池相关接口客户端"""

    def DescribeResourcePools(
            self,
            resourcePoolType,
            keywordType=None,
            keyword=None,
            orderBy=None,
            order=None,
            pageNumber=None,
            pageSize=None
    ):
        """
        查询资源池列表。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/dmgrw0t8l

        Args:
            resourcePoolType: 资源池类型：1、通用资源池：common，2、托管资源池：dedicatedV2
            keywordType: 资源池模糊查询字段，可选 [resourcePoolName, resourcePoolId]，默认值为 resourcePoolName
            keyword: 查询关键词，默认值为空字符串
            orderBy: 资源池查询排序字段，可选 [resourcePoolName, resourcePoolId, createdAt]，默认值为 resourcePoolName
            order: 排序方式，可选 [ASC, DESC]，默认值为 ASC
            pageNumber: 页码，默认值为1
            pageSize: 单页结果数，默认值为10

        Returns:
            baidubce.bce_response.BceResponse: 资源池列表

        Raises:
            ValueError: 当必填参数为空时
            TypeError: 当参数类型不匹配时
        """
        path = b'/'
        params = {
            'action': 'DescribeResourcePools',
            'resourcePoolType': resourcePoolType
        }
        if keywordType is not None:
            params['keywordType'] = keywordType
        if keyword is not None:
            params['keyword'] = keyword
        if orderBy is not None:
            params['orderBy'] = orderBy
        if order is not None:
            params['order'] = order
        if pageNumber is not None:
            params['pageNumber'] = pageNumber
        if pageSize is not None:
            params['pageSize'] = pageSize

        return self._send_resource_pool_request(
            http_methods.GET,
            path,
            params=params
        )

    def DescribeResourcePool(
        self,
        resourcePoolId
    ):
        """
        查询资源池详情。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Wmgrw36zt

        Args:
            resourcePoolId: 资源池ID（必填，Query参数）

        Returns:
            baidubce.bce_response.BceResponse: 资源池详情

        Raises:
            ValueError: 当必填参数为空时
            TypeError: 当参数类型不匹配时
        """
        path = b'/'
        params = {
            'action': 'DescribeResourcePool',
            'resourcePoolId': resourcePoolId,
        }

        return self._send_resource_pool_request(
            http_methods.GET,
            path,
            params=params
        )

    def DescribeResourcePoolOverview(self):
        """
        查询资源池概览。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Imgrw8356

        Returns:
            baidubce.bce_response.BceResponse: 资源池概览信息

        Raises:
            ValueError: 当必填参数为空时
            TypeError: 当参数类型不匹配时
        """
        path = b'/'
        params = {
            'action': 'DescribeResourcePoolOverview',
        }

        return self._send_resource_pool_request(
            http_methods.GET,
            path,
            params=params
        )

    def DescribeResourcePoolConfiguration(
        self,
        resourcePoolId
    ):
        """
        查询资源池配置。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/mmgrw76pp

        Args:
            resourcePoolId: 资源池ID（必填. Query参数）

        Returns:
            baidubce.bce_response.BceResponse: 资源池配置信息

        Raises:
            ValueError: 当必填参数为空时
            TypeError: 当参数类型不匹配时
        """
        path = b'/'
        params = {
            'action': 'DescribeResourcePoolConfiguration',
            'resourcePoolId': resourcePoolId,
        }

        return self._send_resource_pool_request(
            http_methods.GET,
            path,
            params=params
        )

    def DescribeQueues(
        self,
        resourcePoolId,
        keywordType=None,
        keyword=None,
        pageNumber=None,
        pageSize=None,
    ):
        """
        查询队列列表。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/vmfcjld9v

        Args:
            resourcePoolId: 资源池ID（必填，Query参数）
            keywordType: 关键字类型（可选，Query参数）
            keyword: 关键字（可选，Query参数）
            pageNumber: 分页参数（可选，Query参数）
            pageSize: 单页结果数（可选，Query参数）

        Returns:
            baidubce.bce_response.BceResponse: 队列列表

        Raises:
            ValueError: 当必填参数为空时
            TypeError: 当参数类型不匹配时
        """
        path = b'/'
        params = {
            'action': 'DescribeQueues',
            'resourcePoolId': resourcePoolId,
        }
        if keywordType is not None:
            params['keywordType'] = keywordType
        if keyword is not None:
            params['keyword'] = keyword
        if pageNumber is not None:
            params['pageNumber'] = pageNumber
        if pageSize is not None:
            params['pageSize'] = pageSize

        return self._send_resource_pool_request(
            http_methods.GET,
            path,
            params=params
        )

    def DescribeQueue(
        self,
        queueId
    ):
        """
        查询队列详情。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Jmfcjhru0

        Args:
            queueId: 队列ID（必填，Query参数）

        Returns:
            baidubce.bce_response.BceResponse: 队列详情

        Raises:
            ValueError: 当必填参数为空时
            TypeError: 当参数类型不匹配时
        """
        path = b'/'
        params = {
            'action': 'DescribeQueue',
            'queueId': queueId,
        }

        return self._send_resource_pool_request(
            http_methods.GET,
            path,
            params=params
        )