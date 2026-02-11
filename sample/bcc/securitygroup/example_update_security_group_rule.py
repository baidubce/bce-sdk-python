# -*- coding: utf-8 -*-
"""
    Example for updating a security group rule from the specified security group
"""
import uuid
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
    security_group_rule_id = "r-eg280qrkmxp0"  # 指定SecurityGroupRule的id（注意：应该是r-开头的规则ID，不是g-开头的安全组ID）

    try:
        # 方式1：更新单个字段（推荐用于快速调用）
        resp = bcc_client.update_security_group_rule(security_group_rule_id=security_group_rule_id,
                                                     remark="test_update")
        print("[example] update sg rule (remark only) response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)

    try:
        # 方式2：更新多个字段
        resp = bcc_client.update_security_group_rule(security_group_rule_id=security_group_rule_id,
                                                    remark="test_update",
                                                     protocol="udp",
                                                     portrange='809',
                                                     source_ip="10.0.0.1")
        print("[example] update sg rule (multiple fields) response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)

