# -*- coding: utf-8 -*-
"""
    Example for deleting an enterprise security group rule.
"""
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.esg import esg_client

if __name__ == '__main__':
    ak = "Your AK"  # 账号的Ak
    sk = "Your SK"  # 账号的Sk
    endpoint = "endpoint"  # 服务对应的Region域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    esg_client = esg_client.EsgClient(config)  # client 初始化
    try:
        # 删除企业安全组规则
        resp = esg_client.delete_enterprise_security_group_rule(enterprise_security_group_rule_id='esgr-6eh9yhp8ugw3')# 企业安全组id
        print("[example] delete esg rules response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)