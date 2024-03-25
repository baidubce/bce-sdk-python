# -*- coding: utf-8 -*-
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the
# specific language governing permissions and limitations under the License.
"""
Samples for app blb client.
"""

from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.services.blb.app_blb_client import AppBlbClient
from baidubce.exception import BceHttpClientError

if __name__ == "__main__":

    config = BceClientConfiguration(
        credentials=BceCredentials(
            access_key_id='Your AK', # 用户的ak
            secret_access_key='Your SK' # 用户的sk
        ),
        endpoint='Your Endpoint' # 服务对应的Region域名
    )

    # create an app blb client
    app_blb_client = AppBlbClient(config)

    blb_id = "Your Blbid"  # LB实例ID
    sg_id = "Your Sgid"  # 服务器组ID
    backend_server_list = [
        {
            "instanceId": "Your Serverid",  # 云服务器ID
            "weight": 100  # 权重
        }
    ]

    try:
        # create server group rs
        resp = app_blb_client.create_app_blb_rs(blb_id, sg_id, backend_server_list)
        print("[example] create server group rs response :%s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)
