# -*- coding: utf-8 -*-
"""
example for unbinding ip set.
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

    ip_set_ids = ["ips-z2a8uk9qnkc1"]
    try:
        resp = template_client.unbind_ip_set(
            ip_group_id="ipg-95eapsuw195m",
            ip_set_ids=ip_set_ids
        )  # IP地址族移除IP地址组
        print("[example] unbind ip set response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)