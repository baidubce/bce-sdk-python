# -*- coding: utf-8 -*-
"""
example for list eni.
"""
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.eni import eni_client

if __name__ == '__main__':
    ak = "Your Ak"  # 账号的Ak
    sk = "Your Sk"  # 账号的Sk
    endpoint = "bcc.bj.baidubce.com"  # 服务对应的Region域名, 例如bj Region域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    client = eni_client.EniClient(config)  # client 初始化
    
    try:
        resp = client.list_eni(vpc_id="vpc-jm7h2j497ut7", instance_id="i-Dqf1k9ul", name="eni-1", 
                               private_ip_address_list=["10.0.1.115", "10.0.1.116"], 
                               marker="eni-tnj00he350fh", max_keys=2)  # 查询弹性网卡列表
        print("list eni response :%s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)
