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
example for delete app ip group port.
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
    ip_group_id = "ip_group-xxxxxxx"  # IP组ID
    port_list = [  # 端口列表
        "ip_group_policy-xxxxxx"
    ]

    # delete ip group port
    try:
        app_blb_client.delete_app_ip_group_port(blb_id, ip_group_id, port_list)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)
