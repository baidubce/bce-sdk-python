# -*- coding: utf-8 -*-
"""
Example for unbinding a et.
"""

import uuid

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.etGateway import et_gateway_client

if __name__ == "__main__":
    ak = "Your AK"
    sk = "Your SK"
    endpoint = "bcc.bj.baidubce.com"
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    et_gateway_client = et_gateway_client.EtGatewayClient(config)

    try:
        resp = et_gateway_client.unbind_et(client_token=str(uuid.uuid4()),
                                           et_gateway_id="dcgw-4ds9x3kmds88")
        print("UnBind et response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling API: %s" % e)
