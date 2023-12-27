# -*- coding: utf-8 -*-
"""
example for et channel ipv6.
"""
import uuid

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.et import et_client

if __name__ == '__main__':
    ak = "Your Ak"  # 账号的Ak
    sk = "Your Sk"  # 账号的Sk
    endpoint = "bcc.bj.baidubce.com"  # 服务对应的Region域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    client = et_client.EtClient(config)
  
    try:
        resp = client.disable_et_channel_ipv6(et_id="dcphy-gq65bz9ip712",
                                              et_channel_id="dedicatedconn-zy9t7n91k0iq",
                                              client_token=str(uuid.uuid4()))
        
        print("Disable et channel ipv6 response successfully, response: %s." % resp)
        print("request_id: %s." % resp.metadata.bce_request_id)
    except BceHttpClientError as e:
        print("Exception when calling api: %s." % e)
