# -*- coding: utf-8 -*-
"""
example for create subnet.
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
    subnet_name = "subnetName" # 创建的子网名称
    zone_name = "cn-bj-a" # 创建的子网所属的可用区
    cidr = "192.168.0.0/24" # 子网cidr
    vpc_id = "xxxxxx" # 所属vpc的id
    try:
        resp = subnet_client.create_subnet(name=subnet_name,
                                           zone_name=zone_name,
                                           cidr=cidr,
                                           vpc_id=vpc_id)  # 创建子网
        print("[example] create subnet response :%s", resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)