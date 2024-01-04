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
    member_list = [
        {
            "ip": "10.100.0.136",
            "port": 80,
            "weight": 100
        }
    ]

    try:
        # create ip group
        resp = app_blb_client.create_app_ip_group(blb_id, name, desc, member_list)
        print("[example] create ip group response :%s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)
