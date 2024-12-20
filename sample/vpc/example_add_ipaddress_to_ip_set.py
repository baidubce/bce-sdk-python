# -*- coding: utf-8 -*-
"""
example for adding ip address to ip set.
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

    ip_address_info = [template_model.TemplateIpAddressInfo(ip_address="192.168.17.0/24", description="test1"),
                       template_model.TemplateIpAddressInfo(ip_address="192.168.18.0/24", description="test2")]
    try:
        resp = template_client.add_ip_address_to_ip_set(
            ip_set_id="ips-2etsti1g24hv",
            ip_address_info=ip_address_info
        )  # 增加ip地址到ip地址组
        print("[example] add ip address to ip set response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)