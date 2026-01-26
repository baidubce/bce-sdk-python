# -*- coding: utf-8 -*-
"""
example for get vpc resource ip.
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
    vpc_id = "vpc-xxxxx"  # 要查询的vpc的id

    # 查询VPC内所有产品占用的IP
    try:
        resp = vpc_client.get_resource_ip(vpc_id=vpc_id)
        print("[example] get vpc resource ip response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)

    # 查询指定子网内的产品占用IP
    subnet_id = "sbn-xxxxx"  # 子网ID
    try:
        resp = vpc_client.get_resource_ip(vpc_id=vpc_id, subnet_id=subnet_id)
        print("[example] get vpc resource ip by subnet response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)

    # 查询指定产品类型占用的IP
    resource_type = "enic"  # 产品类型，如bcc、enic、blb等
    try:
        resp = vpc_client.get_resource_ip(vpc_id=vpc_id, resource_type=resource_type)
        print("[example] get vpc resource ip by type response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)

    # 分页查询
    page_no = 1
    page_size = 10
    try:
        resp = vpc_client.get_resource_ip(vpc_id=vpc_id, page_no=page_no, page_size=page_size)
        print("[example] get vpc resource ip with pagination response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)