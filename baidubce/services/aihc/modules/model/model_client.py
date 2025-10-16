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
AIHC model client module.
"""
import json
from typing import Optional

from baidubce.http import http_methods
from baidubce.services.aihc.base.aihc_base_client import AIHCBaseClient


class ModelClient(AIHCBaseClient):
    """模型相关接口客户端"""

    def DescribeModels(self, keyword=None, pageNumber=1, pageSize=10):
        """
        获取模型列表。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/amc1fmz95

        :param keyword: 模型名称，用于筛选模糊匹配（可选，Query参数）
        :type keyword: str
        :param pageNumber: 分页参数，没传默认1（可选，Query参数）
        :type pageNumber: int
        :param pageSize: 分页大小，没传默认返回全部（可选，Query参数）
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

    def DescribeModelVersion(self, modelId, versionId):
        """
        获取模型版本详情。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/wmc1focnv

        :param modelId: 模型ID（必填，Query参数）
        :type modelId: str
        :param versionId: 模型版本ID（必填，Query参数）
        :type versionId: str
        :return: 模型版本详情
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'DescribeModelVersion',
            'modelId': modelId,
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

