# -*- coding: utf-8 -*-
"""
Example for get havip detail list.
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
        # Specify the parameters for get havip detail list
        vpc_id = "vpc-id"

        # Call the get_havip_detail_list method
        resp = havip_client.get_havip_detail_list(vpc_id=vpc_id)

        print("get havip detail list response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling API: %s" % e)