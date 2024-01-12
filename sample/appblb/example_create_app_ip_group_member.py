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
    ip_group_id = "Your Ipgroupid"  # ip组id
    memberList = [
        {
            "ip": "10.100.0.136",  # ip地址
            "weight": 100,  # 权重
            "port": 80  # 端口
        }
    ]

    try:
        # create ip group member
        resp = app_blb_client.create_app_ip_group_member(blb_id, ip_group_id, memberList)
        print("[example] create ip group member response :%s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)
