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
import json
from typing import Optional

from baidubce.http import http_methods
from baidubce.services.aihc.base.aihc_base_client import AIHCBaseClient


class ResourcePoolClient(AIHCBaseClient):
    """资源池相关接口客户端"""

    def DescribeResourcePools(
        self,
        keyword: Optional[str] = None,
        pageNumber: int = 1,
        pageSize: Optional[int] = None
    ):
        """
        查询资源池列表。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/xxxxx

        Args:
            keyword: 关键字（可选）
            pageNumber: 页码，默认1（可选）
            pageSize: 每页数量（可选）

        Returns:
            baidubce.bce_response.BceResponse: 资源池列表
        """
        path = b'/'
        params = {
            'action': 'DescribeResourcePools',
            'pageNumber': pageNumber,
        }
        if keyword is not None:
            params['keyword'] = keyword
        if pageSize is not None:
            params['pageSize'] = pageSize

        return self._send_request(
            http_methods.GET,
            path,
            params=params
        )

    def DescribeResourcePool(
        self,
        resourcePoolId: str
    ):
        """
        查询资源池详情。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/xxxxx

        Args:
            resourcePoolId: 资源池ID（必填）

        Returns:
            baidubce.bce_response.BceResponse: 资源池详情
        """
        path = b'/'
        params = {
            'action': 'DescribeResourcePool',
            'resourcePoolId': resourcePoolId,
        }

        return self._send_request(
            http_methods.GET,
            path,
            params=params
        )

    def DescribeResourcePoolOverview(
        self,
        resourcePoolId: str
    ):
        """
        查询资源池概览。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/xxxxx

        Args:
            resourcePoolId: 资源池ID（必填）

        Returns:
            baidubce.bce_response.BceResponse: 资源池概览信息
        """
        path = b'/'
        params = {
            'action': 'DescribeResourcePoolOverview',
            'resourcePoolId': resourcePoolId,
        }

        return self._send_request(
            http_methods.GET,
            path,
            params=params
        )

    def DescribeResourcePoolConfiguration(
        self,
        resourcePoolId: str
    ):
        """
        查询资源池配置。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/xxxxx

        Args:
            resourcePoolId: 资源池ID（必填）

        Returns:
            baidubce.bce_response.BceResponse: 资源池配置信息
        """
        path = b'/'
        params = {
            'action': 'DescribeResourcePoolConfiguration',
            'resourcePoolId': resourcePoolId,
        }

        return self._send_request(
            http_methods.GET,
            path,
            params=params
        )

    def DescribeQueues(
        self,
        resourcePoolId: str
    ):
        """
        查询队列列表。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/xxxxx

        Args:
            resourcePoolId: 资源池ID（必填）

        Returns:
            baidubce.bce_response.BceResponse: 队列列表
        """
        path = b'/'
        params = {
            'action': 'DescribeQueues',
            'resourcePoolId': resourcePoolId,
        }

        return self._send_request(
            http_methods.GET,
            path,
            params=params
        )

    def DescribeQueue(
        self,
        resourcePoolId: str,
        queueId: str
    ):
        """
        查询队列详情。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/xxxxx

        Args:
            resourcePoolId: 资源池ID（必填）
            queueId: 队列ID（必填）

        Returns:
            baidubce.bce_response.BceResponse: 队列详情
        """
        path = b'/'
        params = {
            'action': 'DescribeQueue',
            'resourcePoolId': resourcePoolId,
            'queueId': queueId,
        }

        return self._send_request(
            http_methods.GET,
            path,
            params=params
        )