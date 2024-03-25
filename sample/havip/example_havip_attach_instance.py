# -*- coding: utf-8 -*-
"""
Example for havip attach instance.
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
        # Specify the parameters for havip attach instance
        instance_ids = ["i-1", "i-2"]
        instance_type = "bcc"
        havip_id = "havip-id"

        # Call the havip attach instance method
        resp = havip_client.havip_attach_instance(instance_ids=instance_ids,
                                                  instance_type=instance_type,
                                                  havip_id=havip_id)

        print("havip attach instance response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling API: %s" % e)