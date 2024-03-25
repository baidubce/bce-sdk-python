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
        marker = "zone-7ssiavcjqi90"  # 标记查询的起点，deafault为null
        max_keys = 1000  # 每页的最大查询数，默认为1000
        resp = ld_client.list_private_zone(
            marker=marker,
            max_keys=max_keys
        )
        resp_marker = resp.marker  # 分页查询，下一次查询的起点
        print("[example] list private zone maker: %s" % resp_marker)
        print("[example] list private zone response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)