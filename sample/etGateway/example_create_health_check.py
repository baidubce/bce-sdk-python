# -*- coding: utf-8 -*-
"""
Example for creating et health check.
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
        resp = et_gateway_client.create_health_check(client_token=str(uuid.uuid4()),
                                                     et_gateway_id="dcgw-4ds9x3kmds88",
                                                     health_check_source_ip=None,
                                                     health_check_type=None,
                                                     health_check_port=None,
                                                     health_check_interval=3,
                                                     health_check_threshold=2,
                                                     unhealth_threshold=2,
                                                     auto_generate_route_rule=True)
        print("Create et health check response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling API: %s" % e)
