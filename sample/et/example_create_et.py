# -*- coding: utf-8 -*-
"""
example for create Et
"""

import uuid

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.et import et_client

if __name__ == "__main__":
    ak = "Your AK"    #用户的ak
    sk = "Your SK"    #用户的sk
    endpoint = 'Your endpoint'  # 服务器对应的Region域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    et_client = et_client.EtClient(config)
    try:
        resp = et_client.create_et_dcphy(name="Your Et name",
                                         isp='ISP_CMCC',
                                         intf_type='1G',
                                         ap_type='SINGLE',
                                         ap_addr='BJYZ',
                                         user_name='Your name',
                                         user_phone='Your Phone',
                                         user_email='Your Email',
                                         user_idc='Your Idc',
                                         description='Your Et description',
                                         client_token=str(uuid.uuid4()))
        print("create et response: %s" % resp.id)
    except BceHttpClientError as e:
        print("Exception when calling api: %s" % e)