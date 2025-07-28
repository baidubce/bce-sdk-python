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
AIHC common utilities module.
"""
import json


def build_request_params(action, **kwargs):
    """
    构建请求参数的通用方法
    
    :param action: API动作名称
    :type action: str
    :param kwargs: 其他参数
    :return: 请求参数字典
    :rtype: dict
    """
    params = {'action': action}
    for key, value in kwargs.items():
        if value is not None:
            params[key] = value
    return params


def build_request_body(**kwargs):
    """
    构建请求体的通用方法
    
    :param kwargs: 请求体参数
    :return: JSON格式的请求体字符串
    :rtype: str
    """
    body = {}
    for key, value in kwargs.items():
        if value is not None:
            body[key] = value
    return json.dumps(body) if body else None 