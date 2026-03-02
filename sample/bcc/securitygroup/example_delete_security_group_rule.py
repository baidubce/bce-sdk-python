# -*- coding: utf-8 -*-
"""
    Example for deleting a security group rule from the specified security group.
"""
import uuid
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
    security_group_rule_id = 'r-ish7dim55rcd'  # 安全组规则ID

    try:
        resp = bcc_client.delete_security_group_rule(security_group_rule_id='r-q1ek3jvwuede', config=None) # security group rule id
        print("[example] delete sg rule response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)

    try:
        # 方式2：使用sg_version和client_token（推荐用于需要版本控制和幂等性的场景）
        client_token = str(uuid.uuid4())
        resp = bcc_client.delete_security_group_rule(security_group_rule_id=security_group_rule_id,
                                                     sg_version=0,  # 安全组版本号，用于版本控制
                                                     client_token=client_token)  # 用于幂等性控制
        print("[example] delete sg rule with version control response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)