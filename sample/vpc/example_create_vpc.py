# -*- coding: utf-8 -*-
"""
example for create vpc.
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
    vpc_name = "vpcName_test2"  # vpc名称
    cidr = "192.168.0.0/16"  # vpc的cidr
    enable_ipv6 = True
    tags = [{"tagKey": "test_tag", "tagValue": "test_val"}]
    try:
        resp = vpc_client.create_vpc(
            name=vpc_name,
            cidr=cidr,
            enable_ipv6=enable_ipv6,
            tags=tags
        )  # 创建vpc
        print("[example] create vpc response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)