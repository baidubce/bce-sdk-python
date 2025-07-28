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

from typing import List, Optional


class Label(dict):
    """
    训练任务标签
    """
    def __init__(self, key, value):
        """
        初始化训练任务标签
        
        Args:
            key: 标签键
            value: 标签值
        """
        super(Label, self).__init__()
        self["key"] = key
        self["value"] = value


class Datasource(dict):
    """
    数据源配置，当前支持PFS
    """
    def __init__(self, type, name, mountPath):
        """
        初始化数据源配置
        
        Args:
            type: 数据源类型
            name: 数据源名称
            mountPath: 挂载路径
        """
        super(Datasource, self).__init__()
        self["type"] = type
        self["name"] = name
        self["mountPath"] = mountPath


class TensorboardConfig(dict):
    """
    tensorboard相关配置
    """
    def __init__(self, logDir, image=None, resources=None):
        """
        初始化tensorboard配置
        
        Args:
            logDir: 日志目录
            image: 镜像配置（可选）
            resources: 资源配置（可选）
        """
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
        """
        初始化告警配置
        
        Args:
            alertType: 告警类型
            receivers: 接收者列表
        """
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


class JobConfig(dict):
    """
    创建训练任务请求参数

    :param name: 名称（必填，Body参数）
    :type name: str
    :param queue: 训练任务所属队列（必填，Body参数，通用资源池须填入队列名称，
                 托管资源池须填入队列Id）
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
    def __init__(self, name: str, queue: str, jobSpec: JobSpec, command: str, resourcePoolId: str,
        jobType: str = "PyTorchJob", labels: Optional[List['Label']] = None, priority: str = "normal",
        dataSources: Optional[List['Datasource']] = None, enableBccl: Optional[bool] = None,
        faultTolerance: Optional[bool] = None, faultToleranceArgs: Optional[str] = None,
        tensorboardConfig: Optional['TensorboardConfig'] = None, alertConfig: Optional['AlertConfig'] = None
    ):
        """
        初始化训练任务配置
        
        Args:
            name: 名称（必填，Body参数）
            queue: 训练任务所属队列（必填，Body参数，通用资源池须填入队列名称，托管资源池须填入队列Id）
            jobSpec: 训练任务配置（必填，Body参数，JobSpec类型）
            command: 启动命令（必填，Body参数）
            resourcePoolId: 资源池唯一标识符（必填，Query参数）
            jobType: 分布式框架（可选，Body参数，只支持 PyTorchJob，默认值：PyTorchJob）
            labels: 训练任务标签（可选，Body参数，List[Label]，默认包含系统标签）
            priority: 调度优先级（可选，Body参数，支持high/normal/low，默认normal）
            dataSources: 数据源配置（可选，Body参数，List[Datasource]，当前支持PFS）
            enableBccl: 是否开启BCCL自动注入（可选，Body参数，bool，默认关闭）
            faultTolerance: 是否开启容错（可选，Body参数，bool，默认关闭）
            faultToleranceArgs: 容错配置（可选，Body参数，str）
            tensorboardConfig: tensorboard相关配置（可选，Body参数，TensorboardConfig类型）
            alertConfig: 告警相关配置（可选，Body参数，AlertConfig类型）
        """
        super(JobConfig, self).__init__()
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
    任务资源配置，被创建训练任务接口引用。
    :param name: 资源名称，支持GPU/CPU/内存/共享内存等，枚举值：
        - baidu.com/a800_80g_cgpu：gpu型号（需按百度资源描述符填写）
        - cpu：cpu配额，单位核
        - memory：内存配额，单位GB
        - sharedMemory：共享内存配额，单位GB
    :param quantity: 资源量，字符串类型
    """
    def __init__(self, name, quantity):
        """
        初始化资源配置
        
        Args:
            name: 资源名称，支持GPU/CPU/内存/共享内存等
            quantity: 资源量，字符串类型
        """
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