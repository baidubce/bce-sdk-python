# -*- coding: utf-8 -*-
"""
example for update subnet.
"""
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.subnet import subnet_client

if __name__ == '__main__':
    ak = "Your Ak"  # 账号的Ak
    sk = "Your Sk"  # 账号的Sk
    endpoint = "bcc.bj.baidubce.com"  # 服务对应的Region域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    subnet_client = subnet_client.SubnetClient(config)  # client 初始化
    subnet_id = "xxxxx" # 要更新的子网的id
    try:
        resp = subnet_client.update_subnet(subnet_id, name="subnet_name")  # 更新子网的名称
        print("[example] update subnet response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)