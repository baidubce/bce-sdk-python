# -*- coding: utf-8 -*-
"""
example for list subnet.
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
    vpc_id = "xxxxx" # 要查询的子网所属的vpc的id
    try:
        resp = subnet_client.list_subnets(vpc_id=vpc_id)  # 查询子网信息
        print("[example] list subnet response :%s", resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)