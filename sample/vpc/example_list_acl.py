# -*- coding: utf-8 -*-
"""
example for query acl.
"""
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.exception import BceHttpClientError
from baidubce.services.vpc import acl_client

if __name__ == '__main__':

    config = BceClientConfiguration(
        credentials=BceCredentials(
            access_key_id='Your Ak',  # 用户的ak
            secret_access_key='Your Sk'  # 用户的sk
        ),
        endpoint='Your endpoint'  # 服务器对应的Region域名
    )
    acl_client = acl_client.AclClient(config)  # 创建acl client
    try:
        response = acl_client.list_acl_entrys(vpc_id='vpc-vi7kwp20ii5z')  # 查询所属vpc所有的acl，传参为vpc id
        vpcId = response.vpcId  # 查询的vpc id
        vpcName = response.vpcName  # 查询的vpc name
        vpcCidr = response.vpcCidr  # 查询的vpc cidr
        aclEntrys = response.aclEntrys  # 查询到的acl列表
        print("[example] query acl  response: %s" % response)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)
