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

from typing import Optional


class PermissionEntry(dict):
    """
    权限条目结构体，用于表示用户或用户组的权限信息
    """

    def __init__(self, id: str, name: str, permission: str):
        """
        初始化权限条目

        Args:
            id: 用户或用户组ID
            name: 用户或用户组名
            permission: 权限，枚举值：r：只读，rw：读写
        """
        super().__init__()
        self["id"] = id
        self["name"] = name
        self["permission"] = permission


class DatasetVersionEntry(dict):
    """
    数据集版本条目结构体，用于表示数据集版本信息
    """

    def __init__(
            self,
            storagePath: str,
            mountPath: str,
            id: Optional[str] = None,
            version: Optional[str] = None,
            description: Optional[str] = None,
            createUser: Optional[str] = None
    ):
        """
        初始化数据集版本条目

        Args:
            storagePath: 存储路径（必须）
            mountPath: 默认挂载路径（必须）
            id: 数据集版本ID（可选）
            version: 版本号（可选）
            description: 版本描述（可选）
            createUser: 创建用户（可选）
        """
        super().__init__()
        self["storagePath"] = storagePath
        self["mountPath"] = mountPath
        if id is not None:
            self["id"] = id
        if version is not None:
            self["version"] = version
        if description is not None:
            self["description"] = description
        if createUser is not None:
            self["createUser"] = createUser
