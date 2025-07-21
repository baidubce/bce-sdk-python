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
This module provides a model class for AIHC V2.
"""

from typing import List, Optional

class Label(dict):
    """
    训练任务标签
    """
    def __init__(self, key, value):
        super(Label, self).__init__()
        self["key"] = key
        self["value"] = value

class Datasource(dict):
    """
    数据源配置，当前支持PFS
    """
    def __init__(self, type, name, mountPath):
        super(Datasource, self).__init__()
        self["type"] = type
        self["name"] = name
        self["mountPath"] = mountPath

class TensorboardConfig(dict):
    """
    tensorboard相关配置
    """
    def __init__(self, logDir, image=None, resources=None):
        super(TensorboardConfig, self).__init__()
        self["logDir"] = logDir
        if image is not None:
            self["image"] = image
        if resources is not None:
            self["resources"] = resources

class AlertConfig(dict):
    """
    告警相关配置
    """
    def __init__(self, alertType, receivers):
        super(AlertConfig, self).__init__()
        self["alertType"] = alertType
        self["receivers"] = receivers

class JobSpec(dict):
    """
    创建训练任务配置
    """
    def __init__(
        self,
        image,
        replicas,
        imageConfig=None,
        resources=None,
        envs=None,
        enableRDMA=None,
        hostNetwork=None
    ):
        super(JobSpec, self).__init__()
        self["image"] = image
        self["replicas"] = replicas
        if imageConfig is not None:
            self["imageConfig"] = imageConfig
        if resources is not None:
            self["resources"] = resources
        if envs is not None:
            self["envs"] = envs
        if enableRDMA is not None:
            self["enableRDMA"] = enableRDMA
        if hostNetwork is not None:
            self["hostNetwork"] = hostNetwork

class JobConfig(dict):
    """
    创建训练任务请求参数

    :param name: 名称（必填，Body参数）
    :type name: str
    :param queue: 训练任务所属队列（必填，Body参数，通用资源池须填入队列名称，托管资源池须填入队列Id）
    :type queue: str
    :param jobSpec: 训练任务配置（必填，Body参数，JobSpec类型）
    :type jobSpec: JobSpec
    :param command: 启动命令（必填，Body参数）
    :type command: str
    :param resourcePoolId: 资源池唯一标识符（必填，Query参数）
    :type resourcePoolId: str
    :param jobType: 分布式框架（可选，Body参数，只支持 PyTorchJob，默认值：PyTorchJob）
    :type jobType: str
    :param labels: 训练任务标签（可选，Body参数，List[Label]，默认包含系统标签）
    :type labels: List[Label]
    :param priority: 调度优先级（可选，Body参数，支持high/normal/low，默认normal）
    :type priority: str
    :param dataSources: 数据源配置（可选，Body参数，List[Datasource]，当前支持PFS）
    :type dataSources: List[Datasource]
    :param enableBccl: 是否开启BCCL自动注入（可选，Body参数，bool，默认关闭）
    :type enableBccl: bool
    :param faultTolerance: 是否开启容错（可选，Body参数，bool，默认关闭）
    :type faultTolerance: bool
    :param faultToleranceArgs: 容错配置（可选，Body参数，str）
    :type faultToleranceArgs: str
    :param tensorboardConfig: tensorboard相关配置（可选，Body参数，TensorboardConfig类型）
    :type tensorboardConfig: TensorboardConfig
    :param alertConfig: 告警相关配置（可选，Body参数，AlertConfig类型）
    :type alertConfig: AlertConfig
    """
    def __init__(
        self,
        name: str,
        queue: str,
        jobSpec: JobSpec,
        command: str,
        resourcePoolId: Optional[str] = None,
        jobType: str = "PyTorchJob",
        labels: Optional[List['Label']] = None,
        priority: str = "normal",
        dataSources: Optional[List['Datasource']] = None,
        enableBccl: Optional[bool] = None,
        faultTolerance: Optional[bool] = None,
        faultToleranceArgs: Optional[str] = None,
        tensorboardConfig: Optional['TensorboardConfig'] = None,
        alertConfig: Optional['AlertConfig'] = None
    ):
        super(JobConfig, self).__init__()
        if resourcePoolId is not None:
            self["resourcePoolId"] = resourcePoolId
        self["name"] = name
        self["queue"] = queue
        self["jobType"] = jobType
        self["jobSpec"] = jobSpec
        self["command"] = command
        if labels is not None:
            self["labels"] = labels
        self["priority"] = priority
        if dataSources is not None:
            self["dataSources"] = dataSources
        if enableBccl is not None:
            self["enableBccl"] = enableBccl
        if faultTolerance is not None:
            self["faultTolerance"] = faultTolerance
        if faultToleranceArgs is not None:
            self["faultToleranceArgs"] = faultToleranceArgs
        if tensorboardConfig is not None:
            self["tensorboardConfig"] = tensorboardConfig
        if alertConfig is not None:
            self["alertConfig"] = alertConfig

class ImageConfig(dict):
    """
    任务镜像配置，仅私有镜像时需要配置。
    被创建训练任务接口引用。
    :param username: 私有镜像仓库用户名
    :param password: 私有镜像仓库密码
    """
    def __init__(self, username, password):
        super(ImageConfig, self).__init__()
        self["username"] = username
        self["password"] = password

class Resource(dict):
    """
    任务资源配置，被创建训练任务接口引用。
    :param name: 资源名称，支持GPU/CPU/内存/共享内存等，枚举值：
        - baidu.com/a800_80g_cgpu：gpu型号（需按百度资源描述符填写）
        - cpu：cpu配额，单位核
        - memory：内存配额，单位GB
        - sharedMemory：共享内存配额，单位GB
    :param quantity: 资源量，字符串类型
    """
    def __init__(self, name, quantity):
        super(Resource, self).__init__()
        self["name"] = name
        self["quantity"] = quantity

class Env(dict):
    """
    环境变量信息，被创建训练任务、查询训练任务详情接口引用。
    :param name: 标签名（可选）
    :param value: 标签值（可选）
    """
    def __init__(self, name=None, value=None):
        super(Env, self).__init__()
        if name is not None:
            self["name"] = name
        if value is not None:
            self["value"] = value

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
    def __init__(self, source, storageBucket, storagePath, id=None, version=None, modelMetrics=None, description=None):
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
    def __init__(self, id, name, storageType, storageInstance, importFormat, owner, ownerName, visibilityScope, permission, latestVersionId, latestVersion, createdAt, updatedAt, latestVersionEntry=None):
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
    def __init__(self, id, version, description, storagePath, mountPath, createUser, createUserName, createdAt, updatedAt):
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
