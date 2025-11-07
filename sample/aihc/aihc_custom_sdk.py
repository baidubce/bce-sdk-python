# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

"""
AIHC客户端示例模块。
"""

import copy
import json
import os
import logging

import dotenv

from baidubce import bce_base_client
from baidubce.exception import BceHttpClientError, BceServerError
from baidubce.auth import bce_v1_signer
from baidubce.http import handler, bce_http_client, http_methods
from baidubce.utils import required, Expando
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', force=True)
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("baidubce").setLevel(logging.INFO)
__logger = logging.getLogger(__name__)
__logger.setLevel(logging.INFO)

dotenv.load_dotenv()


def parse_json(http_response, response):
    """
    解析HTTP响应中的JSON数据并更新response对象。

    :param http_response: HTTP响应对象
    :param response: 要更新的响应对象
    :return: 解析是否成功
    """
    body = http_response.read()
    if body:
        try:
            parsed_data = json.loads(body, object_hook=dict_to_python_object)
            response.__dict__.update(parsed_data.__dict__)
            # 移除metadata key（如果存在）
            if 'metadata' in response.__dict__:
                del response.__dict__['metadata']
        except json.JSONDecodeError as e:
            __logger.error('Failed to parse JSON response: %s', e)
            return False
    http_response.close()
    return True


def dict_to_python_object(d):
    """
    将字典转换为Expando对象，用于JSON解析时的对象钩子。
    :param d: 要转换的字典
    :return: Expando对象
    """
    attr = {}
    for k, v in list(d.items()):
        k = str(k)
        attr[k] = v
    return Expando(attr)


def to_dict(obj):
    """
    将对象转换为字典格式。

    递归地将Python对象（包括自定义对象、字典、列表）转换为纯字典格式，
    便于JSON序列化和调试输出。

    Args:
        obj: 要转换的对象，可以是字典、列表、自定义对象或基本类型

    Returns:
        dict/list/基本类型: 转换后的字典、列表或基本类型值

    Examples:
        >>> obj = SomeClass()
        >>> obj.name = "test"
        >>> result = to_dict(obj)
        >>> print(result)
        {'name': 'test'}
    """
    if isinstance(obj, dict):
        return {k: to_dict(v) for k, v in obj.items()}
    elif hasattr(obj, '__dict__'):
        return {k: to_dict(v) for k, v in obj.__dict__.items()}
    elif isinstance(obj, list):
        return [to_dict(i) for i in obj]
    else:
        return obj


class AihcClient(bce_base_client.BceBaseClient):
    """
    AIHC V2 base sdk client
    """

    version = b'v2'

    def __init__(self, config=None):
        bce_base_client.BceBaseClient.__init__(self, config)
        self.version = self.version

    def _compute_service_id(self):
        return b'aihc'

    def _merge_config(self, config=None):
        if config is None:
            return self.config
        else:
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    def _send_request(self, http_method, path,
                      body=None, headers=None, params=None,
                      config=None, body_parser=None):
        config = self._merge_config(config)
        if body_parser is None:
            body_parser = parse_json
        if headers is None:
            headers = {
                b'version': self.version,
                b'Content-Type': b'application/json'
            }
        else:
            headers[b'version'] = self.version
            headers[b'Content-Type'] = b'application/json'

        return bce_http_client.send_request(
            config, bce_v1_signer.sign, [handler.parse_error, body_parser],
            http_method, path, body, headers, params)

    def _send_job_request(
        self,
        http_method,
        path,
        body=None,
        headers=None,
        params=None,
        config=None,
        body_parser=None
    ):
        config = self._merge_config(config)
        if body_parser is None:
            body_parser = parse_json
        if headers is None:
            headers = {
                b'X-API-Version': self.version
            }
        else:
            headers[b'X-API-Version'] = self.version

        return bce_http_client.send_request(
            config, bce_v1_signer.sign, [handler.parse_error, body_parser],
            http_method, path, body, headers, params)

    # ============任务相关接口============
    @required(pageNumber=int, pageSize=int)
    def DescribeJobs(
        self,
        resourcePoolId,
        queueID=None,
        queue=None,
        status=None,
        keywordType=None,
        keyword=None,
        orderBy=None,
        order=None,
        pageNumber=1,
        pageSize=10
    ):
        """
        查询训练任务列表。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/xmayvctia

        :param resourcePoolId:
            资源池唯一标识符（必填）
        :type resourcePoolId: string

        :param queueID:
            托管资源池需传入该参数，为队列Id（可选，Query参数）
        :type queueID: string

        :param queue:
            训练任务所属队列，通用资源池须填入队列名称，不填时返回所有。托管资源池须填入队列Id（可选，Body参数）
        :type queue: string

        :param status:
            基于状态筛选任务（可选，Body参数）
        :type status: string

        :param keywordType:
            筛选关键字类型（可选，Body参数）
        :type keywordType: string

        :param keyword:
            关键字值，当前仅支持name/queueName（可选，Body参数）
        :type keyword: string

        :param orderBy:
            排序字段，支持createdAt，finishedAt，默认为createdAt（可选，Body参数）
        :type orderBy: string

        :param order:
            排序方式，可选 [asc, desc]，asc为升序，desc为降序，默认desc（可选，Body参数）
        :type order: string

        :param pageNumber:
            请求分页参数，表示第几页（可选，Body参数）
        :type pageNumber: int

        :param pageSize:
            单页结果数，默认值为10（可选，Body参数）
        :type pageSize: int

        :return:
            返回训练任务列表
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/'
        params = {
            'action': 'DescribeJobs',
            'resourcePoolId': resourcePoolId,
        }
        if queueID:
            params['queueID'] = queueID

        body = {}
        if queue is not None:
            body['queue'] = queue
        if status is not None:
            body['status'] = status
        if keywordType is not None:
            body['keywordType'] = keywordType
        if keyword is not None:
            body['keyword'] = keyword
        if orderBy is not None:
            body['orderBy'] = orderBy
        if order is not None:
            body['order'] = order
        if pageNumber is not None:
            body['pageNumber'] = pageNumber
        if pageSize is not None:
            body['pageSize'] = pageSize

        return self._send_job_request(
            http_methods.POST,
            path,
            body=json.dumps(body),
            params=params
        )

    # ============数据集相关接口============
    @required(datasetId=str)
    def ModifyDataset(
        self,
        datasetId,
        name=None,
        description=None,
        visibilityScope=None,
        visibilityUser=None,
        visibilityGroup=None
    ):
        """
        修改数据集。

        参考文档：https://cloud.baidu.com/doc/AIHC/s/Imc095v8z

        :param datasetId: 数据集ID（必填，Query参数）
        :type datasetId: str
        :param name: 数据集名称（可选，Body参数）
        :type name: str
        :param description: 数据集描述（可选，Body参数）
        :type description: str
        :param visibilityScope: 可见范围（可选，Body参数）
            可选值：ALL_PEOPLE（所有人可见）、ONLY_OWNER（仅所有者可读写）、USER_GROUP（指定范围可用）
        :type visibilityScope: str
        :param visibilityUser: 用户权限列表（可选，Body参数）
            格式：[{"id": "xxx", "name": "xxx", "permission": "r"}, {"id": "yyy", "name": "xxx", "permission": "rw"}]
        :type visibilityUser: list
        :param visibilityGroup: 用户组权限列表（可选，Body参数）
            格式：[{"id": "xxx", "name": "xxx", "permission": "r"}, {"id": "yyy", "name": "xxx", "permission": "rw"}]
        :type visibilityGroup: list
        :return: 修改结果
        :rtype: baidubce.bce_response.BceResponse
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


def main():
    """
    main函数，程序入口
    """
    AK = os.getenv('AK') or 'your-access-key-id'  # 百度云access key
    SK = os.getenv('SK') or 'your-secret-access-key'  # 百度云secret key
    HOST = os.getenv('HOST') or 'https://aihc.bj.baidubce.com'  # AIHC服务地址

    resourcePoolId = ""  # 资源池ID
    datasetId = ""  # 数据集ID
    name = ""  # 数据集名称

    config = BceClientConfiguration(credentials=BceCredentials(AK, SK), endpoint=HOST)

    # create a aihc client
    aihc_client = AihcClient(config)

    # 查询任务列表
    try:
        __logger.info('-------------------DescribeJobs start--------------------------------')
        response = aihc_client.DescribeJobs(resourcePoolId=resourcePoolId)
        # 将response转换为python对象
        print(json.dumps(to_dict(response), ensure_ascii=False))

        # response对象的全部key
        __logger.info('response.__dict__.keys(): %s', response.__dict__.keys())
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # 修改数据集
    try:
        __logger.info('-------------------ModifyDataset start--------------------------------')
        # 示例1：仅修改数据集名称
        response = aihc_client.ModifyDataset(datasetId=datasetId, name=name)
        print("修改数据集名称结果:", response)
        print(json.dumps(to_dict(response), ensure_ascii=False, indent=2))
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)


if __name__ == '__main__':
    main()
