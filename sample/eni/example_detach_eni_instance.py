# -*- coding: utf-8 -*-
"""
example for detach eni instance.
"""
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.eni import eni_client

if __name__ == '__main__':
    ak = "Your Ak"  # 账号的Ak
    sk = "Your Sk"  # 账号的Sk
    endpoint = "bcc.bj.baidubce.com"  # 服务对应的Region域名, 例如bj Region域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    client = eni_client.EniClient(config)  # client 初始化
    
    try:
        # 弹性网卡卸载云主机
        resp = client.detach_eni_instance(eni_id="eni-7bqg7jf0m88f", instance_id="i-Dqf1k9ul")
        print("detach eni instance response :%s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)
