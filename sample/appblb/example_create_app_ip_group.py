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
example for create app ip group.
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

    blb_id = "lb-xxxxxxxx"  # 指定的BLB ID
    name = "exmaple"  # IP组名称
    desc = "example"  # IP组描述
    member_list = [   # IP成员列表
        {
            "ip": "10.10.10.10",  # 后端服务器IP
            "port": 80,  # 后端服务器端口
            "weight": 100  # 权重
        }
    ]

    try:
        # create ip group
        resp = app_blb_client.create_app_ip_group(blb_id, name, desc, member_list)
        print("[example] create ip group response :%s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)
