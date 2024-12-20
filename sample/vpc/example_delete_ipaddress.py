# -*- coding: utf-8 -*-
"""
example for deleting an ip address from ip set.
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

    ip_address = ["192.168.18.0/24", "192.168.16.2"]
    try:
        resp = template_client.delete_ip_address(
            ip_set_id="ips-2etsti1g24hv",
            ip_address=ip_address
        )  # 删除IP地址
        print("[example] delete ip address response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)