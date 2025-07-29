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
AIHC dataset model module: Dataset, DatasetVersion
"""


class Dataset(dict):
    """
    数据集信息结构体，对应数据集详情、数据集列表接口。
    :param id: 数据集ID
    :param name: 数据集名称
    :param storageType: 存储类型（如 PFS、BOS）
    :param storageInstance: 存储实例ID
    :param importFormat: 导入格式（如 FILE、FOLDER）
    :param owner: 拥有者ID
    :param ownerName: 拥有者名称
    :param visibilityScope: 可见范围（如 ALL_PEOPLE）
    :param permission: 权限（如 rw）
    :param latestVersionId: 最新版本ID
    :param latestVersion: 最新版本号
    :param latestVersionEntry: 最新版本详情（DatasetVersion 类型或 dict，可选）
    :param createdAt: 创建时间（ISO8601字符串）
    :param updatedAt: 更新时间（ISO8601字符串）
    """
    def __init__(self, id, name, storageType, storageInstance, importFormat, owner, 
                 ownerName, visibilityScope, permission, latestVersionId, latestVersion, 
                 createdAt, updatedAt, latestVersionEntry=None):
        """
        初始化数据集信息
        
        Args:
            id: 数据集ID
            name: 数据集名称
            storageType: 存储类型（如 PFS、BOS）
            storageInstance: 存储实例ID
            importFormat: 导入格式（如 FILE、FOLDER）
            owner: 拥有者ID
            ownerName: 拥有者名称
            visibilityScope: 可见范围（如 ALL_PEOPLE）
            permission: 权限（如 rw）
            latestVersionId: 最新版本ID
            latestVersion: 最新版本号
            createdAt: 创建时间（ISO8601字符串）
            updatedAt: 更新时间（ISO8601字符串）
            latestVersionEntry: 最新版本详情（DatasetVersion 类型或 dict，可选）
        """
        super(Dataset, self).__init__()
        self["id"] = id
        self["name"] = name
        self["storageType"] = storageType
        self["storageInstance"] = storageInstance
        self["importFormat"] = importFormat
        self["owner"] = owner
        self["ownerName"] = ownerName
        self["visibilityScope"] = visibilityScope
        self["permission"] = permission
        self["latestVersionId"] = latestVersionId
        self["latestVersion"] = latestVersion
        self["createdAt"] = createdAt
        self["updatedAt"] = updatedAt
        if latestVersionEntry is not None:
            self["latestVersionEntry"] = latestVersionEntry


class DatasetVersion(dict):
    """
    数据集版本信息结构体，对应数据集版本详情、版本列表接口。
    :param id: 版本ID
    :param version: 版本号
    :param description: 版本描述
    :param storagePath: 存储路径
    :param mountPath: 挂载路径
    :param createUser: 创建人ID
    :param createUserName: 创建人名称
    :param createdAt: 创建时间（ISO8601字符串）
    :param updatedAt: 更新时间（ISO8601字符串）
    """
    def __init__(self, id, version, description, storagePath, mountPath, createUser, 
                 createUserName, createdAt, updatedAt):
        """
        初始化数据集版本信息
        
        Args:
            id: 版本ID
            version: 版本号
            description: 版本描述
            storagePath: 存储路径
            mountPath: 挂载路径
            createUser: 创建人ID
            createUserName: 创建人名称
            createdAt: 创建时间（ISO8601字符串）
            updatedAt: 更新时间（ISO8601字符串）
        """
        super(DatasetVersion, self).__init__()
        self["id"] = id
        self["version"] = version
        self["description"] = description
        self["storagePath"] = storagePath
        self["mountPath"] = mountPath
        self["createUser"] = createUser
        self["createUserName"] = createUserName
        self["createdAt"] = createdAt
        self["updatedAt"] = updatedAt 