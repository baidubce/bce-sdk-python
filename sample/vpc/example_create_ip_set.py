# -*- coding: utf-8 -*-
"""
example for creating ip set.
"""
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.vpc import template_client
from baidubce.services.vpc import template_model

if __name__ == '__main__':
    ak = "Your Ak"  # 账号的Ak
    sk = "Your Sk"  # 账号的Sk
    endpoint = "bcc.bj.baidubce.com"  # 服务对应的Region域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    template_client = template_client.TemplateClient(config)  # client 初始化
    

    name = "vpcName"  # 地址组名称
    ip_version = "IPv4"  # 地址组支持的IP版本，可选值：IPv4, IPv6
    ip_address_info = [template_model.TemplateIpAddressInfo(ip_address="192.168.11.0/24", description="test1"),
                       template_model.TemplateIpAddressInfo(ip_address="192.168.12.0/24", description="test2")]
    description = "test"  # 描述
    try:
        resp = template_client.create_ip_set(
            name=name,
            ip_version=ip_version,
            ip_address_info=ip_address_info,
            description=description
        )  # 创建地址组
        print("[example] create ip set response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)