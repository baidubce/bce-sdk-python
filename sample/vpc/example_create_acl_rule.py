# -*- coding: utf-8 -*-
"""
example create acl rule.
"""
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
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
        acl_rule_list = [{                    # 创建acl rule 列表
            'subnetId': 'sbn-zuabnf2w6qtn',
            'protocol': 'tcp',
            'sourceIpAddress': '192.168.0.0',
            'destinationIpAddress': '192.168.0.0/20',
            'sourcePort': '1-65535',
            'destinationPort': '443',
            'position': 2,
            'direction': 'ingress',
            'action': 'allow',
            'description': ''
        }]
        response = acl_client.create_acl(rule_list=acl_rule_list)  # 创建acl rule
        print("[example] create acl rule response: %s" % response)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)
