# -*- coding: utf-8 -*-
"""
Example for updating a et gateway.
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
        resp = et_gateway_client.update_et_gateway(et_gateway_id="dcgw-4ds9x3kmds88",
                                                   name="dcGateway",
                                                   description="test et gateway",
                                                   speed=100,
                                                   local_cidrs=[
                                                       '10.243.87.0/24'],
                                                   client_token=str(uuid.uuid4()))
        print("Update et gateway response: %s", resp)
    except BceHttpClientError as e:
        print("Exception when calling API: %s" % e)
