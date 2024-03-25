# -*- coding: utf-8 -*-
"""
example for get vpc private ip address infomation.
"""
import sys
sys.path.insert(1, "/Users/ninja/Projects/sdk/python/baidu/bce-sdk/python")
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.vpc import vpc_client

if __name__ == '__main__':
    ak = "Your AK"  # 账号的Ak
    sk = "Your SK"  # 账号的Sk
    endpoint = "bcc.bj.baidubce.com"  # 服务对应的Region域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    vpc_client = vpc_client.VpcClient(config)  # client 初始化
    vpc_id = "vpc-xxxxx"  # 要查询的vpc的id

    # 查询列表中的私有ip地址
    private_ip_addresses = ["192.168.0.1", "192.168.0.2"]  # 私有ip地址
    try:
        resp = vpc_client.get_private_ip_address_info(vpc_id=vpc_id,
                                                        private_ip_addresses=private_ip_addresses)  # 查询vpc私有ip地址信息
        print("[example] get vpc private ip response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)

    # 查询某个范围内的私有ip地址
    private_ip_addresses_range = "192.168.0.1-192.168.0.5"  # 私有ip地址范围
    try:
        resp = vpc_client.get_private_ip_address_info(vpc_id=vpc_id,
                                                        private_ip_range=private_ip_addresses_range)  # 查询vpc私有ip地址信息
        print("[example] get vpc private ip range response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)