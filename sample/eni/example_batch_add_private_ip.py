# -*- coding: utf-8 -*-
"""
example for batch add private ip.
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
        # 批量增加弹性网卡内网IP
        resp = client.batch_add_private_ip(eni_id="eni-7bqg7jf0m88f", 
                                           is_ipv6=True, 
                                           private_ip_address_list=["240c:4081:8005:5e04::0a", 
                                                                    "240c:4081:8005:5e04::0b"])
        private_ip_addresses = resp.private_ip_addresses # 添加的弹性网卡的内网IPv4/IPv6地址列表
        print("batch add private ip response :%s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)
