# -*- coding: utf-8 -*-
"""
example for delete eni.
"""
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.eni import eni_client

if __name__ == '__main__':
    ak = "Your Ak"  # 账号的Ak
    sk = "Your Sk"  # 账号的Sk
    endpoint = "Your endpoint"  # 服务对应的Region域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)  
    client = eni_client.EniClient(config)  # client 初始化
    try:
        eni_id = "eni-c6adp40kpick"       # 要删除的eni id
        resp = client.delete_eni(eni_id)  # 删除一个eni
        print("delete eni response :%s", resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)
