# -*- coding: utf-8 -*-
"""
Example for creating a havip.
"""

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.havip import havip_client


if __name__ == "__main__":
    ak = "Your AK"
    sk = "Your SK"
    endpoint = "your.havip.endpoint.com"  # Replace with your havip endpoint
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    havip_client = havip_client.HavipClient(config)

    try:
        # Specify the parameters for creating a havip
        name = "havip_sdk_test"
        subnet_id = "sbn-id"
        private_ip_address = ""
        description = "Your havip description"

        # Call the create_havip method
        resp = havip_client.create_havip(name=name,
                                         subnet_id=subnet_id,
                                         private_ip_address=private_ip_address,
                                         description=description)
        print("Create havip response: %s" % resp.id)
    except BceHttpClientError as e:
        print("Exception when calling API: %s" % e)