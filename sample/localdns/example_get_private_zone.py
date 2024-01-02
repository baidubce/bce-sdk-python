# !/usr/bin/env python
# coding=utf-8
"""
Samples for private zone.
"""

import uuid

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.localdns import ld_client

if __name__ == '__main__':
    ak = "Your Ak"  # 账号的Ak
    sk = "Your Sk"  # 账号的Sk
    endpoint = "bcc.bj.baidubce.com"  # 服务对应的Region域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    ld_client = ld_client.LdClient(config)  # client 初始化

    try:
        zone_id = 'zone-7ssiavcjqi90'  # zone id
        client_token = str(uuid.uuid4())  # 幂等性Token
        resp = ld_client.get_private_zone(
            zone_id=zone_id,
        )
        resp_zone_id = resp.zone_id
        print("[example] get private zone id: %s" % resp_zone_id)
        print("[example] get private zone response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)