# -*- coding: utf-8 -*-
"""
Example for update a havip.
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
        # Specify the parameters for update a havip
        havip_id = "havip-id"  # Replace with the ID of the havip you want to delete
        name = "havip_sdk_update"  # Replace with the name of the havip you want to delete
        description = "YourHavipDescription"  # Replace with the description of the havip you want to delete
        # Call the update_havip method
        resp = havip_client.update_havip(havip_id=havip_id,
                                         name=name,
                                         description=description)

        print("Update havip response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling API: %s" % e)