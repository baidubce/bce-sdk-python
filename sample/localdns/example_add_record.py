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
        zone_id='zone-nqa0uqyse51z'  # zone id
        add_record_request = {
            'rr': 'www',
            'type': 'A',
            'value': '2.2.2.2'
        }
        client_token = str(uuid.uuid4())  # 幂等性Token
        resp = ld_client.add_record(
            zone_id=zone_id,
            add_record_request=add_record_request,
            client_token=client_token
        )
        resp_record_id = resp.record_id
        print("[example] add record id: %s" % resp_record_id)
        print("[example] add record response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)