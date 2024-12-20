# -*- coding: utf-8 -*-
"""
example for creating ip group
"""
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.vpc import template_client

if __name__ == '__main__':
    ak = "Your Ak"  # 账号的Ak
    sk = "Your Sk"  # 账号的Sk
    endpoint = "bcc.bj.baidubce.com"  # 服务对应的Region域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    template_client = template_client.TemplateClient(config)  # client 初始化
    

    name = "test-ip-group"  # 地址族名称
    ip_version = "IPv4"  # 地址族支持的IP版本，可选值：IPv4, IPv6
    ip_set_ids = ["ips-z2a8uk9qnkc1", "ips-hms1n8fu184f"]
    description = "test"  # 描述
    try:
        resp = template_client.create_ip_group(
            name=name,
            ip_version=ip_version,
            ip_set_ids=ip_set_ids,
            description=description
        )  # 创建地址族
        print("[example] create ip group response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)