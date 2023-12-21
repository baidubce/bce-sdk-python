# -*- coding: utf-8 -*-
"""
    Example for Deleting the specified SecurityGroup.
"""
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.bcc import bcc_client

if __name__ == '__main__':
    ak = "Your AK"  # 账号的Ak
    sk = "Your SK"  # 账号的Sk
    endpoint = "endpoint"  # 服务对应的Region域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    bcc_client = bcc_client.BccClient(config)  # client 初始化
    security_group_id = "g-dcqaukr9u3yn"  # 指定要删除的SecurityGroup的id
    try:
        resp = bcc_client.delete_security_group(security_group_id=security_group_id, config=None)  # 删除指定SecurityGroup
        print("[example] delete sg response :%s", resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)