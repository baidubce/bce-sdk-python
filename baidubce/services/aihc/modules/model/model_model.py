# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the
# License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.

"""
AIHC model module: ModelVersion
"""


class ModelVersion(dict):
    """
    模型版本信息结构体，对应模型管理相关接口。
    :param id: 模型版本ID（可选，新建时无需指定）
    :param version: 版本号（可选，新建时无需指定）
    :param source: 该版本模型的来源（必填，如 UserUpload）
    :param storageBucket: 模型存储的BOS桶（必填）
    :param storagePath: BOS桶中的存储路径（必填）
    :param modelMetrics: 模型指标，JSON格式字符串（可选）
    :param description: 版本描述（可选）
    """
    def __init__(self, source, storageBucket, storagePath, id=None, version=None, 
                 modelMetrics=None, description=None):
        """
        初始化模型版本信息
        
        Args:
            source: 该版本模型的来源（必填，如 UserUpload）
            storageBucket: 模型存储的BOS桶（必填）
            storagePath: BOS桶中的存储路径（必填）
            id: 模型版本ID（可选，新建时无需指定）
            version: 版本号（可选，新建时无需指定）
            modelMetrics: 模型指标，JSON格式字符串（可选）
            description: 版本描述（可选）
        """
        super(ModelVersion, self).__init__()
        if id is not None:
            self["id"] = id
        if version is not None:
            self["version"] = version
        self["source"] = source
        self["storageBucket"] = storageBucket
        self["storagePath"] = storagePath
        if modelMetrics is not None:
            self["modelMetrics"] = modelMetrics
        if description is not None:
            self["description"] = description 