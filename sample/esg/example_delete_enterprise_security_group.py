# -*- coding: utf-8 -*-
"""
    Example for deleting the specified EnterpriseSecurityGroup.
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
    enterprise_security_group_id = "esg-fg01y9tdm13a"
    try:
        # 删除esg
        resp = esg_client.delete_enterprise_security_group(enterprise_security_group_id=enterprise_security_group_id)  #企业安全组id
        print("[example] delete esg response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)