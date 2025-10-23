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
AIHC service client module.
"""
import json
from typing import Optional

from baidubce.http import http_methods
from baidubce.services.aihc.base.aihc_base_client import AIHCBaseClient


class ServiceClient(AIHCBaseClient):
    """在线服务相关接口客户端"""

    def DescribeServices(self, resourcePoolId=None, queueName=None, name=None, region=None, pageNumber=1, pageSize=10):
        """
        拉取服务列表。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Imb4v5905

        :param resourcePoolId: 资源池ID（可选，Query参数）
        :type resourcePoolId: str
        :param queueName: 队列名称（可选，Query参数）
        :type queueName: str
        :param name: 服务名称（可选，Query参数）
        :type name: str
        :param region: 区域（可选，Query参数）
        :type region: str
        :param pageNumber: 页码，默认1（可选，Query参数）
        :type pageNumber: int
        :param pageSize: 每页数量，默认10（可选，Query参数）
        :type pageSize: int
        :return: 服务列表及总数
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'DescribeServices',
            'pageNumber': pageNumber,
            'pageSize': pageSize,
        }
        if resourcePoolId is not None:
            params['resourcePoolId'] = resourcePoolId
        if queueName is not None:
            params['queueName'] = queueName
        if name is not None:
            params['name'] = name
        if region is not None:
            params['region'] = region
        return self._send_request(
            http_methods.GET,
            path,
            params=params
        )

    def DescribeService(self, serviceId: str):
        """
        查询服务详情。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/4mb4v7wn5

        serviceId: 服务ID（必填，Query参数）

        Returns:
            baidubce.bce_response.BceResponse: 服务详情

        Raises:
            ValueError: 当必填参数为空时
            TypeError: 当参数类型不匹配时
        """
        path = b'/'
        params = {
            'action': 'DescribeService',
            'serviceId': serviceId,
        }
        return self._send_request(
            http_methods.GET,
            path,
            params=params
        )

    def DescribeServiceStatus(self, serviceId):
        """
        获取服务状态。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/dmb4v6oh0

        :param serviceId: 服务ID（必填，Query参数）
        :type serviceId: str
        :return: 服务状态信息
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'DescribeServiceStatus',
            'serviceId': serviceId,
        }
        return self._send_request(
            http_methods.GET,
            path,
            params=params
        )

    def CreateService(
        self,
        serviceConf: dict,
        clientToken: Optional[str] = None
    ):
        """
        创建在线服务。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Imb4uf20u

        Args:
            clientToken: clientToken保证请求的幂等性（可选，Query参数）
            serviceConf: 服务配置（必填，Body参数，详见ServiceConf结构），包含：
                - name: 服务名称（必填）
                - acceleratorType: 加速芯片类型（必填）
                - workloadType: 负载类型（必填）
                - instanceCount: 部署实例数（必填）
                - resourcePool: 资源池描述（必填，ResourcePoolConf结构）
                - containers: 服务容器信息（必填，Array of ContainerConf）
                - storage: 存储卷、共享内存配置（可选，StorageConf结构）
                - access: 服务访问配置信息（可选，AccessConf结构）
                - log: 日志配置（可选，LogConf结构）
                - deploy: 部署配置（可选，DeployConf结构）
                - misc: 实例label、annotations配置（可选，Misc结构）

        Returns:
            baidubce.bce_response.BceResponse: 创建结果

        Raises:
            ValueError: 当必填参数为空时
            TypeError: 当参数类型不匹配时
        """
        path = b'/'
        params = {
            'action': 'CreateService',
        }
        if clientToken is not None:
            params['clientToken'] = clientToken

        return self._send_request(
            http_methods.POST,
            path,
            body=json.dumps(serviceConf),
            params=params
        )

    def DeleteService(
        self,
        serviceId: str
    ):
        """
        删除在线服务。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/xxxxx

        Args:
            serviceId: 服务ID（必填）

        Returns:
            baidubce.bce_response.BceResponse: 删除结果

        Raises:
            ValueError: 当必填参数为空时
            TypeError: 当参数类型不匹配时
        """
        path = b'/'
        params = {
            'action': 'DeleteService',
            'serviceId': serviceId,
        }

        return self._send_request(
            http_methods.POST,
            path,
            params=params
        )

    def ModifyService(
        self,
        serviceId: str,
        serviceConf: dict,
        description: Optional[str] = None,
    ):
        """
        升级在线服务。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Zmb4v974k

        Args:
            serviceId: 服务ID（必填，Query参数）
            serviceConf: 与创建参数一致，但不允许修改网络配置，当前支持修改的字段如下：（可选，Body参数）
            - acceleratorType: 加速芯片类型（必填）
            - instanceCount: 部署实例数，取值>=0（必填）
            - storage: 存储卷、共享内存配置（可选）
            - containers: 服务容器信息，最少需要1个，最多10个（必填）
            - log: 日志配置（可选）
            - deploy: 部署配置，默认为最大超量和最大不可用均为25%（可选）
            - misc: 实例label、annotations配置（可选）
            description: 描述（可选，Query参数）

        Returns:
            baidubce.bce_response.BceResponse: 修改结果

        Raises:
            ValueError: 当必填参数为空时
            TypeError: 当参数类型不匹配时
        """
        path = b'/'
        params = {
            'action': 'ModifyService',
            'serviceId': serviceId,
        }
        if params is not None:
            params['description'] = description

        return self._send_request(
            http_methods.POST,
            path,
            body=json.dumps(serviceConf),
            params=params
        )

    def ModifyServiceReplicas(
        self,
        serviceId: str,
        instanceCount: int
    ):
        """
        扩缩容在线服务。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Omb4vbjhh

        Args:
            serviceId: 服务ID（必填）
            instanceCount: 实例数量（必填）

        Returns:
            baidubce.bce_response.BceResponse: 扩缩容结果
        """
        path = b'/'
        params = {
            'action': 'ModifyServiceReplicas',
            'serviceId': serviceId,
        }

        body = {
            'instanceCount': instanceCount,
        }

        return self._send_request(
            http_methods.POST,
            path,
            body=json.dumps(body),
            params=params
        )

    def UpgradeService(
        self,
        serviceId: str,
        versionId: str,
        **kwargs
    ):
        """
        升级服务。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/xxxxx

        Args:
            serviceId: 服务ID（必填）
            versionId: 版本ID（必填）
            **kwargs: 其他升级参数

        Returns:
            baidubce.bce_response.BceResponse: 升级结果
        """
        path = b'/'
        params = {
            'action': 'UpgradeService',
            'serviceId': serviceId,
        }

        body = {
            'versionId': versionId,
            **kwargs
        }

        return self._send_request(
            http_methods.POST,
            path,
            body=json.dumps(body),
            params=params
        )

    def DescribeServicePods(
        self,
        serviceId: str
    ):
        """
        拉取服务pod列表。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/xxxxx

        Args:
            serviceId: 服务ID（必填）

        Returns:
            baidubce.bce_response.BceResponse: 服务pod列表
        """
        path = b'/'
        params = {
            'action': 'DescribeServicePods',
            'serviceId': serviceId,
        }

        return self._send_request(
            http_methods.GET,
            path,
            params=params
        )

    def DeleteServicePod(
        self,
        serviceId: str,
        instanceId: str
    ):
        """
        删除Pod并重建。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Hmb4vjh24

        Args:
            serviceId: 服务ID（必填，Query参数）
            instanceId: Pod实例ID（必填，Query参数）

        Returns:
            baidubce.bce_response.BceResponse: Pod删除结果

        Raises:
            ValueError: 当必填参数为空时
            TypeError: 当参数类型不匹配时
        """
        path = b'/'
        params = {
            'action': 'DeleteServicePod',
            'serviceId': serviceId,
            'instanceId': instanceId,
        }

        return self._send_request(
            http_methods.POST,
            path,
            params=params
        )

    def DisableServicePod(
        self,
        serviceId: str,
        instanceId: str,
        block: bool
    ):
        """
        摘除Pod流量。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/5mb4vhz0a

        Args:
            serviceId: 服务ID（必填，Query参数）
            instanceId: Pod实例ID（必填，Query参数）
            block: 是否阻塞等待（必填，Query参数）

        Returns:
            baidubce.bce_response.BceResponse: Pod流量摘除结果

        Raises:
            ValueError: 当必填参数为空时
            TypeError: 当参数类型不匹配时
        """
        path = b'/'
        params = {
            'action': 'DisableServicePod',
            'serviceId': serviceId,
            'instanceId': instanceId,
            'block': block,
        }

        return self._send_request(
            http_methods.POST,
            path,
            params=params
        )

    def ModifyServiceNetConfig(
        self,
        serviceId: str,
        publicAccess: bool,
        eip: str = None
    ):
        """
        配置公网访问。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Gmb4vgurj

        Args:
            serviceId: 服务ID（必填）
            publicAccess: 是否开启公网访问（必填）
            eip: 弹性公网IP（可选）

        Returns:
            baidubce.bce_response.BceResponse: 公网访问配置结果
        """
        path = b'/'
        params = {
            'action': 'ModifyServiceNetConfig',
            'serviceId': serviceId,
            'publicAccess': publicAccess,
        }
        if eip is not None:
            params['eip'] = eip

        return self._send_request(
            http_methods.POST,
            path,
            params=params
        )

    def DescribeServicePodGroups(
        self,
        serviceId: str
    ):
        """
        获取实例组列表。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Emb4va9nm

        Args:
            serviceId: 服务ID（必填）

        Returns:
            baidubce.bce_response.BceResponse: 实例组列表
        """
        path = b'/'
        params = {
            'action': 'DescribeServicePodGroups',
            'serviceId': serviceId,
        }

        return self._send_request(
            http_methods.GET,
            path,
            params=params
        )

    def DescribeServiceChangelogs(
        self,
        serviceId: str,
        pageNumber: int = 1,
        pageSize: int = 10
    ):
        """
        拉取服务变更记录。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Zmb4v9gvl

        Args:
            serviceId: 服务ID（必填）
            pageNumber: 页码，默认1（可选）
            pageSize: 每页数量，默认10（可选）

        Returns:
            baidubce.bce_response.BceResponse: 服务变更记录列表
        """
        path = b'/'
        params = {
            'action': 'DescribeServiceChangelogs',
            'serviceId': serviceId,
            'pageNumber': pageNumber,
            'pageSize': pageSize,
        }

        return self._send_request(
            http_methods.GET,
            path,
            params=params
        )

    def DescribeServiceChangelog(
        self,
        changeId: str
    ):
        """
        查询服务变更详情。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/vmb4vam48

        Args:
            changeId: 变更记录ID（必填）

        Returns:
            baidubce.bce_response.BceResponse: 服务变更详情
        """
        path = b'/'
        params = {
            'action': 'DescribeServiceChangelog',
            'changeId': changeId,
        }

        return self._send_request(
            http_methods.GET,
            path,
            params=params
        )
