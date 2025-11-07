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
AIHC service model module.
"""

from typing import List, Optional


class ResourcePoolConf(dict):
    """
    资源池配置信息
    Attributes:
        resourcePoolId (str): 资源池ID，托管资源池固定为'aihc-serverless'
        queueName (str): 队列名称
        resourcePoolType (str): 资源池类型，可选值：
            - "" (空字符串): 自运维资源池
            - "serverless": 全托管资源池
            - "public": 预留字段（暂未使用）
        resourcePoolName (str): 资源池名称（托管资源池可不填）
    """

    def __init__(
        self,
        resourcePoolId,  # type: str
        queueName,  # type: str
        resourcePoolType,  # type: str
        resourcePoolName  # type: str
    ):
        super().__init__()
        self["resourcePoolId"] = resourcePoolId
        self["queueName"] = queueName
        self["resourcePoolType"] = resourcePoolType
        self["resourcePoolName"] = resourcePoolName


class PFSConfig(dict):
    """
    PFS存储配置（专用文件存储服务）
    Attributes:
        sourcePath (str): PFS中的源路径（如"/dataset/images"）
        InstanceId (str): PFS实例ID（如"pfs-12345"）
    """

    def __init__(self, sourcePath, InstanceId):
        super().__init__()
        self["sourcePath"] = sourcePath
        self["InstanceId"] = InstanceId


class VolumnConf(dict):
    """
    存储卷配置
    Attributes:
        volumeType (str): 存储类型，可选值：
            - "pfs": PFS存储
            - "hostpath": 主机路径
            - "emptydir": 临时目录
        volumnName (str): 卷名称（需满足^[a-z][a-z0-9-]*[a-z0-9]$）
        pfs (Optional[dict]): 当volumeType为pfs时必填（PFSConfig转换的字典）
    """

    def __init__(
            self,
            volumeType,  # type: str
            volumnName,  # type: str
            pfs,  # type: Optional[dict] = None
    ):
        super().__init__()
        self["volumeType"] = volumeType
        self["volumnName"] = volumnName
        if pfs is not None:
            self["pfs"] = pfs


class StorageConf(dict):
    """存储资源配置
    Attributes:
        shmSize (Optional[int]): 共享内存大小（单位GiB），不配置默认为0
        volumns (Optional[List[dict]]): 存储卷配置列表（VolumnConf转换的字典）
    """

    def __init__(
            self,
            shmSize, # type: Optional[int] = None,
            volumns # type: Optional[List[dict]] = None
    ):
        super().__init__()
        if shmSize is not None:
            self["shmSize"] = shmSize
        if volumns is not None:
            self["volumns"] = volumns


class ImageConf(dict):
    """容器镜像配置
    Attributes:
        imageType (int): 镜像类型：
            - 0: 预置镜像
            - 1: CCR镜像
            - 2: 其他镜像
        imageUrl (str): 镜像地址（如"registry.example.com/image:v1.0"）
        username (Optional[str]): 私有仓库用户名（非必填）
        password (Optional[str]): 私有仓库密码（非必填）
    """

    def __init__(
            self,
            imageType,  # type: int
            imageUrl,  # type: str
            username,  # type: Optional[str]
            password   # type: Optional[str]
    ):
        super().__init__()
        self["imageType"] = imageType
        self["imageUrl"] = imageUrl
        if username is not None:
            self["username"] = username
        if password is not None:
            self["password"] = password


class ExecAction(dict):
    """执行命令探针配置（通过在容器内执行命令检查健康状态）
    Attributes:
        command (list): 要执行的命令数组（如["/bin/sh", "-c", "echo ready"]）
    """

    def __init__(self, command):  # type: list
        super().__init__()
        self["command"] = command


class HTTPGetAction(dict):
    """HTTP请求探针配置（通过HTTP请求检查健康状态）
    Attributes:
        path (str): 请求路径（如"/healthz"）
        port (int): 请求端口号（如8080）
    """

    def __init__(self, path, port):  # type: (str, int)
        super().__init__()
        self["path"] = path
        self["port"] = port


class TCPSocketAction(dict):
    """TCP端口探针配置（通过TCP连接检查健康状态）
    Attributes:
        port (int): 要检查的端口号
    """

    def __init__(self, port):  # type: int
        super().__init__()
        self["port"] = port


class ProbeHandlerConf(dict):
    """健康检查处理器配置（三种检查方式三选一）
    Attributes:
        exec (Optional[dict]): 命令执行方式（ExecAction转换的字典）
        httpGet (Optional[dict]): HTTP请求方式（HTTPGetAction转换的字典）
        tcpSocketAction (Optional[dict]): TCP连接方式（TCPSocketAction转换的字典）
    Note:
        三种检查方式只能选择其中一种配置
    """

    def __init__(
            self,
            _exec,  # type: Optional[dict]
            httpGet,  # type: Optional[dict]
            tcpSocketAction  # type: Optional[dict]
    ):
        super().__init__()
        if _exec is not None:
            self["exec"] = _exec
        if httpGet is not None:
            self["httpGet"] = httpGet
        if tcpSocketAction is not None:
            self["tcpSocketAction"] = tcpSocketAction


class ProbeConf(dict):
    """健康检查探针配置
    Attributes:
        initialDelaySeconds (int): 初始化延迟时间（容器启动后等待多少秒开始检查）
        timeoutSeconds (int): 检查超时时间（每次检查等待的超时秒数）
        periodSeconds (int): 检查间隔时间（两次检查之间的间隔秒数）
        successThreshold (int): 成功阈值（连续成功多少次视为健康）
        failureThreshold (int): 失败阈值（连续失败多少次视为不健康）
        handler (dict): 检查处理器配置（ProbeHandlerConf转换的字典）
    """

    def __init__(
            self,
            initialDelaySeconds,  # type: int
            timeoutSeconds,       # type: int
            periodSeconds,        # type: int
            successThreshold,     # type: int
            failureThreshold,     # type: int
            handler               # type: dict
    ):
        super().__init__()
        self["initialDelaySeconds"] = initialDelaySeconds
        self["timeoutSeconds"] = timeoutSeconds
        self["periodSeconds"] = periodSeconds
        self["successThreshold"] = successThreshold
        self["failureThreshold"] = failureThreshold
        self["handler"] = handler


class ContainerConf(dict):
    """
    容器运行配置
    Attributes:
        name (str): 容器名称（需满足^a-z0-9?$，长度<=63）
        cpus (int): CPU核数（必须>0）
        memory (int): 内存大小（单位GiB，必须>0）
        acceleratorCount (int): 加速卡数量（>=0）
        image (dict): 镜像配置（ImageConf转换的字典）
        command (Optional[list]): 容器启动命令（如["python", "app.py"]）
        runArgs (Optional[list]): 容器启动参数（如["--port=8080"]）
        ports (Optional[list]): 端口映射列表（如[{"name": "http", "containerPort": 80}]）
        envs (Optional[dict]): 环境变量（如{"LOG_LEVEL": "debug"}）
        volumeMounts (Optional[list]): 存储挂载配置
        readinessProbe (Optional[dict]): 就绪探针（ProbeConf转换的字典）
        startupsProbe (Optional[dict]): 启动探针（ProbeConf转换的字典）
        livenessProbe (Optional[dict]): 存活探针（ProbeConf转换的字典）
    """

    def __init__(
            self,
            name,  # type: str
            cpus,  # type: int
            memory,  # type: int
            acceleratorCount,  # type: int
            image,  # type: dict
            command,  # type: Optional[list]
            runArgs,  # type: Optional[list]
            ports,  # type: Optional[list]
            envs,  # type: Optional[dict]
            volumeMounts,  # type: Optional[list]
            readinessProbe,  # type: Optional[dict]
            startupsProbe,  # type: Optional[dict]
            livenessProbe   # type: Optional[dict]
    ):
        super().__init__()
        self["name"] = name
        self["cpus"] = cpus
        self["memory"] = memory
        self["acceleratorCount"] = acceleratorCount
        self["image"] = image

        if command is not None:
            self["command"] = command
        if runArgs is not None:
            self["runArgs"] = runArgs
        if ports is not None:
            self["ports"] = ports
        if envs is not None:
            self["envs"] = envs
        if volumeMounts is not None:
            self["volumeMounts"] = volumeMounts
        if readinessProbe is not None:
            self["readinessProbe"] = readinessProbe
        if startupsProbe is not None:
            self["startupsProbe"] = startupsProbe
        if livenessProbe is not None:
            self["livenessProbe"] = livenessProbe


class AiGatewayConf(dict):
    """
    AI网关配置（用于分布式推理服务）
    Attributes:
        enableAuth (bool): 是否开启鉴权（True/False）
    """

    def __init__(self, enableAuth):  # type: bool
        super().__init__()
        self["enableAuth"] = enableAuth


class AccessConf(dict):
    """
    服务访问配置
    Attributes:
        publicAccess (Optional[bool]): 是否开启公网访问（默认False）
        eip (Optional[str]): 公网IP地址（开启公网且networkType为空时必填）
        aiGateway (Optional[dict]): 网关配置（AiGatewayConf转换的字典）
        networkType (Optional[str]): 网络类型（""或"aiGateway"）
    """

    def __init__(
            self,
            publicAccess,  # type: Optional[bool]
            eip,           # type: Optional[str]
            aiGateway,     # type: Optional[dict]
            networkType    # type: Optional[str]
    ):
        super().__init__()
        if publicAccess is not None:
            self["publicAccess"] = publicAccess
        if eip is not None:
            self["eip"] = eip
        if aiGateway is not None:
            self["aiGateway"] = aiGateway
        if networkType is not None:
            self["networkType"] = networkType


class LogConf(dict):
    """
    日志配置
    Attributes:
        persistent (Optional[bool]): 是否持久化容器标准输出日志（默认False）
    """

    def __init__(self, persistent=None):  # type: Optional[bool]
        super().__init__()
        if persistent is not None:  # 日志持久化开关
            self["persistent"] = persistent


class CanaryStrategyConf(dict):
    """
    金丝雀发布策略配置
    Attributes:
        maxSurge (Optional[int]): 最大超量百分比（如25表示25%）
        maxUnavailable (Optional[int]): 最大不可用百分比
    Note:
        maxSurge和maxUnavailable不能同时为0
    """

    def __init__(
            self,
            maxSurge,       # type: Optional[int]
            maxUnavailable  # type: Optional[int]
    ):
        super().__init__()
        if maxSurge is not None:
            self["maxSurge"] = maxSurge
        if maxUnavailable is not None:
            self["maxUnavailable"] = maxUnavailable


class ScheduleConf(dict):
    """
    调度优先级配置
    Attributes:
        priority (str): 优先级（"high"/"normal"/"low"）
    """

    def __init__(self, priority):  # type: str
        super().__init__()
        self["priority"] = priority


class DeployConf(dict):
    """
    部署策略配置
    Attributes:
        canaryStrategy (Optional[dict]): 金丝雀策略（CanaryStrategyConf转换的字典）
        schedule (Optional[dict]): 调度配置（ScheduleConf转换的字典）
    """

    def __init__(
            self,
            canaryStrategy,  # type: Optional[dict]
            schedule  # type: Optional[dict]
    ):
        super().__init__()
        if canaryStrategy is not None:
            self["canaryStrategy"] = canaryStrategy
        if schedule is not None:
            self["schedule"] = schedule


class Misc(dict):
    """
    Pod元数据配置
    Attributes:
        podLabels (Optional[dict]): Kubernetes Pod标签（如{"env":"prod"}）
        podAnnotations (Optional[dict]): Kubernetes Pod注解
        gracePeriodSec (Optional[int]): 优雅终止宽限期（秒）
        fedPodsPerIns (Optional[int]): 分布式部署时每组Pod实例数（>1）
        enableRDMA (Optional[bool]): 是否启用RDMA（远程直接内存访问）
    """

    def __init__(
            self,
            podLabels,      # type: Optional[dict]
            podAnnotations, # type: Optional[dict]
            gracePeriodSec, # type: Optional[int]
            fedPodsPerIns,  # type: Optional[int]
            enableRDMA      # type: Optional[bool]
    ):
        super().__init__()
        if podLabels is not None:
            self["podLabels"] = podLabels
        if podAnnotations is not None:
            self["podAnnotations"] = podAnnotations
        if gracePeriodSec is not None:
            self["gracePeriodSec"] = gracePeriodSec
        if fedPodsPerIns is not None:
            self["fedPodsPerIns"] = fedPodsPerIns
        if enableRDMA is not None:
            self["enableRDMA"] = enableRDMA


class ServiceConf(dict):
    """
    服务部署配置（顶级配置）
    Attributes:
        name (str): 服务名称（需满足^[a-z][a-z0-9-]*[a-z0-9]$，长度<=50）
        acceleratorType (str): 加速芯片类型（如"A100"）
        workloadType (str): 工作负载类型（"fed"表示分布式，""表示单机）
        instanceCount (int): 实例数量（>=0）
        resourcePool (dict): 资源池配置（ResourcePoolConf转换的字典）
        containers (List[dict]): 容器配置列表（ContainerConf转换的字典，1-10个）
        storage (Optional[dict]): 存储配置（StorageConf转换的字典）
        access (Optional[dict]): 访问配置（AccessConf转换的字典）
        log (Optional[dict]): 日志配置（LogConf转换的字典）
        deploy (Optional[dict]): 部署策略（DeployConf转换的字典）
        misc (Optional[dict]): 元数据配置（Misc转换的字典）
    """

    def __init__(
            self,
            name,            # type: str
            acceleratorType, # type: str
            workloadType,    # type: str
            instanceCount,   # type: int
            resourcePool,    # type: dict
            containers,      # type: List[dict]
            storage,    # type: Optional[dict]
            access,     # type: Optional[dict]
            log,        # type: Optional[dict]
            deploy,     # type: Optional[dict]
            misc        # type: Optional[dict]
    ):
        super().__init__()
        self["name"] = name
        self["acceleratorType"] = acceleratorType
        self["workloadType"] = workloadType
        self["instanceCount"] = instanceCount
        self["resourcePool"] = resourcePool
        self["containers"] = containers

        if storage is not None:
            self["storage"] = storage
        if access is not None:
            self["access"] = access
        if log is not None:
            self["log"] = log
        if deploy is not None:
            self["deploy"] = deploy
        if misc is not None:
            self["misc"] = misc


class ModifyServiceConf(dict):
    """
    服务修改配置（用于ModifyService接口）
    Attributes:
        name (str): 服务名称（必填）
        acceleratorType (str): 加速芯片类型（必填）
        instanceCount (int): 部署实例数，取值>=0（必填）
        storage (Optional[dict]): 存储卷、共享内存配置（可选）
        containers (List[dict]): 服务容器信息，最少需要1个，最多10个（必填）
        log (Optional[dict]): 日志配置（可选）
        deploy (Optional[dict]): 部署配置，默认为最大超量和最大不可用均为25%（可选）
        misc (Optional[dict]): 实例label、annotations配置（可选）
    """

    def __init__(
            self,
            name,            # type: str
            acceleratorType, # type: str
            instanceCount,   # type: int
            resourcePool,    # type: dict
            containers,      # type: List[dict]
            storage,    # type: Optional[dict]
            log,        # type: Optional[dict]
            deploy,     # type: Optional[dict]
            misc     # type: Optional[dict]
    ):
        super().__init__()
        self["name"] = name
        self["acceleratorType"] = acceleratorType
        self["instanceCount"] = instanceCount
        self["resourcePool"] = resourcePool
        self["containers"] = containers

        if storage is not None:
            self["storage"] = storage
        if log is not None:
            self["log"] = log
        if deploy is not None:
            self["deploy"] = deploy
        if misc is not None:
            self["misc"] = misc
