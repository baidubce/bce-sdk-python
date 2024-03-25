# -*- coding: utf-8 -*-
"""
Example for deleting a havip.
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
        # Specify the parameters for deleting a havip
        havip_id = "havip-id"  # Replace with the ID of the havip you want to delete

        # Call the delete_havip method
        resp = havip_client.delete_havip(havip_id=havip_id)

        print("Delete havip response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling API: %s" % e)