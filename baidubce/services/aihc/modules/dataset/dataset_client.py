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
AIHC dataset client module.
"""
import json
from typing import Optional, List, Dict

from baidubce.bce_response import BceResponse
from baidubce.http import http_methods
from baidubce.services.aihc.base.aihc_base_client import AIHCBaseClient


class DatasetClient(AIHCBaseClient):
    """数据集相关接口客户端"""
    def DescribeDatasets(
        self,
        keyword: Optional[str] = None,
        storageType: Optional[str] = None,
        storageInstances: Optional[str] = None,
        importFormat: Optional[str] = None,
        pageNumber: int = 1,
        pageSize: Optional[int] = 10
    ) -> 'BceResponse':
        """
        获取数据集列表。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Emc099va4

        Args:
            keyword: 名称关键字（可选，Query参数）
            storageType: 存储类型（可选，Query参数）
            storageInstances: 存储实例列表，英文逗号分隔（可选，Query参数）
            importFormat: 导入格式（可选，Query参数）
            pageNumber: 页码，默认1（可选，Query参数）
            pageSize: 每页数量，不传递该参数默认返回全部（可选，Query参数）

        Returns:
            baidubce.bce_response.BceResponse: 数据集列表及总数
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

    def DescribeDataset(self, datasetId: str) -> 'BceResponse':
        """
        获取数据集详情。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Umc0988jj

        Args:
            datasetId: 数据集ID（必填，Query参数）

        Returns:
            baidubce.bce_response.BceResponse: 数据集详情
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

    def ModifyDataset(
            self,
            datasetId: str,
            name: Optional[str] = None,
            description: Optional[str] = None,
            visibilityScope: Optional[str] = None,
            visibilityUser: List[Dict] = None,
            visibilityGroup: List[Dict] = None
    ):
        """
        修改数据集。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Imc095v8z

        Args:
            datasetId: 数据集ID（必填，Query参数）
            name: 数据集名称（可选，Body参数）
            description: 数据集描述（可选，Body参数）
            visibilityScope: 可见范围（可选，Body参数）
            visibilityUser: 用户权限列表（可选，Body参数，List[dict]）
            visibilityGroup: 用户组权限列表（可选，Body参数，List[dict]）

        Returns:
            baidubce.bce_response.BceResponse: 修改结果

        Raises:
            ValueError: 当必填参数为空时
            TypeError: 当参数类型不匹配时
        """
        path = b'/'
        params = {
            'action': 'ModifyDataset',
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

    def DeleteDataset(self, datasetId: str):
        """
        删除数据集，同时删除所有版本。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/wmc09407x

        Args:
            datasetId: 数据集ID（必填，Query参数）

        Returns:
            baidubce.bce_response.BceResponse: 删除结果

        Raises:
            ValueError: 当必填参数为空时
            TypeError: 当参数类型不匹配时
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

    def CreateDataset(
            self,
            name: str,
            storageType: str,
            storageInstance: str,
            importFormat: str,
            visibilityScope: str,
            initVersionEntry: str,
            description: Optional[str] = None,
            owner: Optional[str] = None,
            visibilityUser: List[Dict] = None,
            visibilityGroup: List[Dict] = None
    ):
        """
        创建数据集。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Dmc091fap

        Args:
            name: 数据集名称（必填，Body参数）
            storageType: 存储类型（必填，Body参数）
            storageInstance: 存储实例ID（必填，Body参数）
            importFormat: 导入格式（必填，Body参数）
            visibilityScope: 可见范围（必填，Body参数）
            initVersionEntry: 初始版本信息（必填，Body参数，dict）
            description: 数据集描述（可选，Body参数）
            owner: 拥有者ID（可选，Body参数）
            visibilityUser: 用户权限列表（可选，Body参数，List[dict]）
            visibilityGroup: 用户组权限列表（可选，Body参数，List[dict]）

        Returns:
            baidubce.bce_response.BceResponse: 创建结果

        Raises:
            ValueError: 当必填参数为空时
            TypeError: 当参数类型不匹配时
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
            'visibilityScope': visibilityScope,
            'initVersionEntry': initVersionEntry,
        }
        if description is not None:
            body['description'] = description
        if owner is not None:
            body['owner'] = owner
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

    def DescribeDatasetVersion(self, datasetId: str, versionId: str) -> 'BceResponse':
        """
        获取数据集版本详情。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Dmc09bpj1

        Args:
            datasetId: 数据集ID（必填，Query参数）
            versionId: 数据集版本ID（必填，Query参数）

        Returns:
            baidubce.bce_response.BceResponse: 数据集版本详情
        """
        path = b'/'
        params = {
            'action': 'DescribeDatasetVersion',
            'datasetId': datasetId,
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
