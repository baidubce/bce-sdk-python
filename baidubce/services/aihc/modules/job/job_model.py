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
AIHC job model module.
"""

from typing import Optional


class Label(dict):
    """
    训练任务标签
    """
    def __init__(self, key: str, value: str):
        """
        初始化训练任务标签

        Args:
            key: 标签键
            value: 标签值
        """
        super(Label, self).__init__()
        self["key"] = key
        self["value"] = value


class Option(dict):
    """
    数据卷挂载选项信息
    """

    def __init__(self, readOnly: str):
        """
        初始化数据卷挂载选项

        Args:
            readOnly: 是否以只读模式挂载到容器中
        """
        super(Option, self).__init__()
        self["readOnly"] = readOnly


class Datasource(dict):
    """
    训练任务数据源配置
    支持类型：pfs/hostPath/dataset/bos
    """

    def __init__(
        self,
        type: str,
        name: str,
        mountPath: str,
        sourcePath: Optional[str] = None,
        options: Optional[dict] = None
    ):
        """
        初始化数据源配置

        Args:
            type: 数据源类型，枚举值：pfs/hostPath/dataset/bos
            name: 数据源名称（pfs类型时为实例id，bos类型可为空）
            mountPath: 容器内挂载路径
            sourcePath: 源路径（pfs时为存储路径，hostpath时为宿主机路径）(可选)
            options: 数据源参数（可选）
        """
        super(Datasource, self).__init__()
        self["type"] = type
        self["name"] = name
        self["mountPath"] = mountPath
        if sourcePath is not None:
            self["sourcePath"] = sourcePath
        if options is not None:
            self["options"] = options


class TensorboardConfig(dict):
    """
    tensorboard相关配置
    """
    def __init__(self, enable: Optional[bool] = None, logPqth: Optional[str] = None):
        """
        初始化tensorboard配置

        Args:
            enable: 是否开启Tensorboard（可选）
            logPqth: 训练任务Tensorboard日志（可选）
        """
        super(TensorboardConfig, self).__init__()
        if enable is not None:
            self["enable"] = enable
        if logPqth is not None:
            self["logPath"] = logPqth


class AlertConfig(dict):
    """
    告警相关配置
    """

    def __init__(
        self,
        alertIds: Optional[str] = None,
        instanceId: Optional[str] = None,
        alertName: Optional[str] = None,
        alertItems: Optional[str] = None,
        for_: Optional[str] = None,  # 使用for_避免关键字冲突
        description: Optional[str] = None,
        notifyRuleId: Optional[str] = None,
        severity: Optional[str] = None,
    ):
        """
        初始化告警配置
        """
        super().__init__()
        if alertIds is not None:
            self["alertIds"] = alertIds
        if instanceId is not None:
            self["instanceId"] = instanceId
        if alertName is not None:
            self["alertName"] = alertName
        if alertItems is not None:
            self["alertItems"] = alertItems
        if for_ is not None:
            self["for"] = for_  # 映射到保留字"for"
        if description is not None:
            self["description"] = description
        if notifyRuleId is not None:
            self["notifyRuleId"] = notifyRuleId
        if severity is not None:
            self["severity"] = severity


class JobSpec(dict):
    """
    创建训练任务配置
    """
    def __init__(
        self,
        image,
        replicas,
        imageConfig: Optional[dict] = None,
        resources: Optional[list] = None,
        envs: Optional[list] = None,
        enableRDMA: Optional[bool] = None,
        hostNetwork: Optional[bool] = None
    ):
        """
        初始化训练任务配置

        Args:
            image: 镜像名称
            replicas: 副本数量
            imageConfig: 镜像配置（可选）
            resources: 资源配置（可选）
            envs: 环境变量（可选）
            enableRDMA: 是否启用RDMA（可选）
            hostNetwork: 是否使用主机网络（可选）
        """
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


class ImageConfig(dict):
    """
    任务镜像配置，仅私有镜像时需要配置。
    被创建训练任务接口引用。
    :param username: 私有镜像仓库用户名
    :param password: 私有镜像仓库密码
    """
    def __init__(self, username, password):
        """
        初始化镜像配置

        Args:
            username: 私有镜像仓库用户名
            password: 私有镜像仓库密码
        """
        super(ImageConfig, self).__init__()
        self["username"] = username
        self["password"] = password


class Resource(dict):
    """
    任务资源配置
    被如下接口引用：创建训练任务

    资源名称示例（具体以平台最新文档为准）：
    - baidu.com/a800_80g_cgpu：GPU型号（需按百度资源描述符填写）
    - cpu：CPU配额，单位核
    - memory：内存配额，单位GB
    - sharedMemory：共享内存配额，单位GB
    """

    def __init__(self, name: str, quantity: str):
        """
        初始化资源配置

        Args:
            name: 资源名称，示例值：
                - baidu.com/a800_80g_cgpu：GPU型号
                - cpu：CPU配额
                - memory：内存配额
                - sharedMemory：共享内存配额
            quantity: 资源量，字符串类型
                示例："8"（表示8核CPU/8GB内存等）
        """
        super(Resource, self).__init__()
        self["name"] = name
        self["quantity"] = quantity


class Env(dict):
    """
    环境变量信息，被创建训练任务、查询训练任务详情接口引用。
    Attributes:
        name: 标签名（可选）
        value: 标签值（可选）
    """
    def __init__(self, name=None, value=None):
        """
        初始化环境变量

        Args:
            name: 环境变量名（可选）
            value: 环境变量值（可选）
        """
        super(Env, self).__init__()
        if name is not None:
            self["name"] = name
        if value is not None:
            self["value"] = value
