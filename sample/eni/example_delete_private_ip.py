# -*- coding: utf-8 -*-
"""
example for delete private ip.
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
        # 删除弹性网卡内网IP
        resp = client.delete_private_ip(eni_id="eni-7bqg7jf0m88f", 
                                        private_ip_address="240c:4081:8005:5e04::8")

        print("delete private ip response :%s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)
