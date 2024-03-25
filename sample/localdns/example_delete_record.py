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
        record_id='rc-v9nc88nm0te2'  # record id
        client_token = str(uuid.uuid4())  # 幂等性Token
        resp = ld_client.delete_record(
            record_id=record_id,
            client_token=client_token
        )
        print("[example] delete record response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)