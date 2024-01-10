# -*- coding: utf-8 -*-
"""
example for query acl rules.
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
        response = acl_client.list_subnet_acl(subnet_id='sbn-zuabnf2w6qtn')  # 查询acl rule，传参为subnet id
        aclRules = response.aclRules  # 查询到的acl rule列表
        print("[example] query acl rule response: %s" % response)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)
