# !/usr/bin/env python
# coding=utf-8
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
            access_key_id='your-ak',  # 用户的ak
            secret_access_key='your-sk'  # 用户的sk
        ),
        endpoint='host'  # 请求的域名信息

    )

    # create an app blb client
    app_blb_client = AppBlbClient(config)

    blb_id = "lb-a889d7d4"
    ip_group_id = "ip_group-21475a51"
    protocol_type = "TCP"
    health_check = "TCP"
    health_check_down_retry = 4

    # create ip group port
    try:
        app_blb_client.create_app_ip_group_port(blb_id, ip_group_id, protocol_type, health_check,
                                                health_check_down_retry=health_check_down_retry)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)
