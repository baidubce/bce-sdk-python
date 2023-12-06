# -*- coding: utf-8 -*-
"""
example for update acl rule.
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
        # 更新acl rule，acl_rule_id必选，除去subnetId其他字段均可更新
        response = acl_client.update_acl(acl_rule_id='ar-rvqxk21w6te2',
                                         description='update acl rule',
                                         protocol='tcp',
                                         source_ip_address='192.168.0.0/32',
                                         destination_ip_address='192.168.0.0/32',
                                         source_port=20,
                                         destination_port=20,
                                         action='deny',
                                         position=3)
        print("[example] update acl rule response :%s", response)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)
