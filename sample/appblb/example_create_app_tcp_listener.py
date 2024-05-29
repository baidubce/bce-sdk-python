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
example for create app tcp listener.
"""
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError

from baidubce.services.blb import app_blb_client

if __name__ == '__main__':
    ak = "Your Ak"  # 账号的Ak
    sk = "Your Sk"  # 账号的Sk
    endpoint = "Your Endpoint"  # 服务对应的Region域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    app_blb_client = app_blb_client.AppBlbClient(config)  # client 初始化
    try:
        blb_id = 'Your Blbid'  # 指定的BLB ID
        listener_port = 80  # 监听器的监听端口
        scheduler = 'Your Scheduler'  # 负载均衡算法
        resp = app_blb_client.create_app_tcp_listener(blb_id=blb_id, listener_port=listener_port,
                                                      scheduler=scheduler, config=config)
        print("[example] create app tcp listener response :%s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)
