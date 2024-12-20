# -*- coding: utf-8 -*-
"""
example for binding ip set to ip group.
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

    ip_set_ids = ["ips-3399p5ng4ga0"]
    try:
        resp = template_client.bind_ip_set(
            ip_group_id="ipg-9vd6xtyjz0in",
            ip_set_ids=ip_set_ids
        )  # 增加ip地址组到ip地址族
        print("[example] add ip set to ip group response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)