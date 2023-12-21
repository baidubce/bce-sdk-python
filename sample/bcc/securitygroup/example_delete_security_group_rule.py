# -*- coding: utf-8 -*-
"""
    Example for deleting a security group rule from the specified security group.
"""
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.bcc import bcc_client
from baidubce.services.bcc import bcc_model

if __name__ == '__main__':
    ak = "Your AK"  # 账号的Ak
    sk = "Your SK"  # 账号的Sk
    endpoint = "endpoint"  # 服务对应的Region域名
    endpoint = "bcc.bj.baidubce.com"  # 服务对应的Region域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    bcc_client = bcc_client.BccClient(config)  # client 初始化
    try:
        resp = bcc_client.delete_security_group_rule(security_group_rule_id='r-q1ek3jvwuede', config=None) # security group rule id
        print("[example] delete sg rule response :%s", resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)