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
        zone_id = 'zone-nqa0uqyse51z'  # zone id
        marker = "rc-dhh8ajrtu89w"  # 分页查询的起点,默认值为None
        max_keys = 100  # 分页查询的最大返回结果数, 默认值为1000
        resp = ld_client.list_record(
            zone_id=zone_id,
            marker=marker,
            max_keys=max_keys
        )
        resp_marker = resp.marker  # 分页查询，下一次查询的起点
        print("[example] list record maker: %s" % resp_marker)
        print("[example] list record response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)