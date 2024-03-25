# -*- coding: utf-8 -*-
"""
Example for creating a et gateway.
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
        resp = et_gateway_client.create_et_gateway(client_token=str(uuid.uuid4()),
                                                   name="dcGateway",
                                                   vpc_id="vpc-IyrqYIQ7",
                                                   speed=100,
                                                   description="test et gateway",
                                                   local_cidrs=[
                                                       '10.243.87.0/24'],
                                                   et_id="dcphy-478px3km77dh",
                                                   channel_id="dedicatedconn-i7c1skfd0djs")

        et_gateway_id = resp.et_gateway_id
        print("Create et gateway response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling API: %s" % e)
