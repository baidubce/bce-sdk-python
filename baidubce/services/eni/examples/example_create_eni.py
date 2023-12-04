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
    endpoint = "Your endpoint"  # 服务对应的Region域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    client = eni_client.EniClient(config)  # client 初始化
    eni_ip_list = [eni_model.EniIPSet(public_ip="", private_ip="10.0.1.111", primary=True), # IP地址列表
                   eni_model.EniIPSet(public_ip="", private_ip="10.0.1.112", primary=False)]
    try:
        resp = client.create_eni(name="PYTHON-SDK-TEST", subnet_id="sbn-d63m7t0bbwt5", 
                                     security_group_ids=["g-92600fd1grhr"],
                                     eni_ip_address_list=eni_ip_list)  # 创建eni
        print("create eni response :%s", resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)
