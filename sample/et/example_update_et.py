# -*- coding: utf-8 -*-
"""
example for update Et
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
        resp = et_client.update_et_dcphy(et_id='Your Et Id',
                                         name="Your Et name",
                                         description='Your Et description',
                                         user_name='Your name',
                                         user_phone='Your Phone',
                                         user_email='Your Email',
                                         client_token=str(uuid.uuid4()))
        print("update et response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s" % e)