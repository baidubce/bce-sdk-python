# -*- coding: utf-8 -*-
"""
example for shutting down vpc relay.
"""
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.vpc import vpc_client

if __name__ == '__main__':
    ak = "Your Ak"  # 账号的Ak
    sk = "Your Sk"  # 账号的Sk
    endpoint = "bcc.bj.baidubce.com"  # 服务对应的Region域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    vpc_client = vpc_client.VpcClient(config)  # client 初始化
    vpc_id = "vpc-ncqec4mxy9xf" # 要关闭中继的vpc的id
    try:
        resp = vpc_client.shutdown_relay(
            vpc_id=vpc_id
        )  # 关闭VPC中继
        print("[example] shutdown relay response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)