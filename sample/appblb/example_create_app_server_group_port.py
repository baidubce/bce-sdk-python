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
example for app server group port.
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

    blb_id = "lb-xxxxxxx"  # 指定的BLB ID
    sg_id = "sg-xxxxxx"  # 服务器组ID
    port = 80  # 监听端口
    protocol_type = "TCP"  # 协议类型，支持 "TCP"/"UDP"/"HTTP"
    enable_health_check = True  # 是否启用健康检查，默认为true
    health_check = "TCP"  # 健康检查协议，支持 "HTTP"/"TCP"/"UDP"/"ICMP"
    health_check_port = 80  # 健康检查端口
    health_check_host = "localhost"  # 7层健康检查请求的Host头，仅当health_check为HTTP时有效
    health_check_urlpath = "/"  # 健康检查URI，仅当health_check为HTTP时有效
    health_check_timeout_insecond = 3  # 健康检查超时时间(秒)
    health_check_interval_insecond = 3  # 健康检查间隔(秒)
    health_check_down_retry = 3  # 不健康阈值，连续几次健康检查失败后屏蔽
    health_check_up_retry = 3  # 健康阈值，连续几次健康检查成功后恢复
    health_check_normal_status = "http_2xx|http_3xx"  # HTTP健康检查正常状态码

    # create server group port with TCP health check
    try:
        resp = app_blb_client.create_app_server_group_port(
            blb_id, sg_id, port, protocol_type,
            enable_health_check=enable_health_check,
            health_check=health_check,
            health_check_port=health_check_port,
            health_check_timeout_insecond=health_check_timeout_insecond,
            health_check_interval_insecond=health_check_interval_insecond,
            health_check_down_retry=health_check_down_retry,
            health_check_up_retry=health_check_up_retry
        )
        print("[example] create server group port response :%s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)

    # create server group port with HTTP health check (using health_check_host)
    try:
        resp = app_blb_client.create_app_server_group_port(
            blb_id, sg_id, 8080, "HTTP",
            enable_health_check=True,
            health_check="HTTP",
            health_check_port=8080,
            health_check_host="www.example.com",  # 指定健康检查Host头
            health_check_urlpath="/health",
            health_check_timeout_insecond=5,
            health_check_interval_insecond=5,
            health_check_down_retry=3,
            health_check_up_retry=3,
            health_check_normal_status="http_2xx"
        )
        print("[example] create server group port with HTTP health check response :%s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)
