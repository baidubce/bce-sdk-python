# -*- coding: utf-8 -*-
"""
example for create eni.
"""
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.eni import eni_client
from baidubce.services.eni import eni_model


if __name__ == '__main__':
    ak = "Your Ak"  # 账号的Ak
    sk = "Your Sk"  # 账号的Sk
    endpoint = "bcc.bj.baidubce.com"  # 服务对应的Region域名, 例如bj Region域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    client = eni_client.EniClient(config)  # client 初始化
    
    try:
        eni_ip_list = [eni_model.EniIPSet(public_ip="", private_ip="192.168.0.42", primary=True), 
                       eni_model.EniIPSet()]    # IP地址列表, EniIPSet不指定private_ip默认分配可用的内网IP
        resp = client.create_eni(name="eni-1", subnet_id="sbn-x1evbqf9vgxq", 
                                 enterprise_security_group_ids=["esg-p9y1mmu5fqkx"],
                                 eni_ip_address_list=eni_ip_list, network_interface_traffic_mode="standard")  # 创建eni
        eni_id = resp.eni_id    # 获取eni_id
        print("create eni response :%s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)
