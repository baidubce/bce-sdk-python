# -*- coding: utf-8 -*-
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
example for create app server group.
"""

from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.services.blb.app_blb_client import AppBlbClient
from baidubce.exception import BceHttpClientError

if __name__ == "__main__":

    config = BceClientConfiguration(
        credentials=BceCredentials(
            access_key_id='your-ak',  # 用户的ak
            secret_access_key='your-sk'  # 用户的sk
        ),
        endpoint='host'  # 请求的域名信息

    )

    # create an app blb client
    app_blb_client = AppBlbClient(config)

    blb_id = "lb-xxxxxx"  # 指定的BLB ID
    name = "exmaple"  # 服务器组名称
    desc = "example"  # 服务器组描述
    backend_server_list = [  # 后端服务器列表
        {
            "instanceId": "i-xxxxxx",  # 后端服务器ID
            "weight": 100,  # 权重
            "portList": [  # 端口列表
                {
                    "listenerPort": 80,  # 监听端口
                    "backendPort": 80,  # 后端服务器端口
                    "portType": "TCP"  # 后端协议
                }
            ]
        }
    ]

    try:
        # create server group
        resp = app_blb_client.create_app_server_group(blb_id, name, desc, backend_server_list)
        print("[example] create server group response :%s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)
