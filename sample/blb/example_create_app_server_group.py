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
    name = "exmaple"
    desc = "example"
    backend_server_list = [
        {
            "instanceId": "i-FKhltG7y",
            "weight": 100,
            "portList": [
                {
                    "listenerPort": 80,
                    "backendPort": 80,
                    "portType": "TCP"
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
