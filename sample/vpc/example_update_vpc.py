# -*- coding: utf-8 -*-
"""
example for update vpc.
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
    vpc_id = "vpc-c46sdgpdkams" # 要更新的vpc的id
    try:
        resp = vpc_client.update_vpc(vpc_id, name="vpc_name", description="测试")  # 更新vpc的名称
        print("[example] update vpc response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)