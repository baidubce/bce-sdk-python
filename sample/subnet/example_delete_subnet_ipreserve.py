# -*- coding: utf-8 -*-
"""
Example for deleting a reserved subnet.
"""

import uuid

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.subnet import subnet_client

if __name__ == "__main__":
    ak = "Your AK"
    sk = "Your SK"
    endpoint = "your.subnet.endpoint.com"  # Replace with your subnet endpoint
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    subnet_client = subnet_client.SubnetClient(config)

    try:
        # Specify the ID of the reserved subnet to be deleted
        ip_reserve_id = "ipr-6k6a056t3y7t"  # Replace with the ID of the reserved subnet
        client_token = str(uuid.uuid4())

        # Call the delete_subnet_ipreserve method
        resp = subnet_client.delete_subnet_ipreserve(ip_reserve_id=ip_reserve_id, 
                                                     client_token=client_token)
        ip_reserve_list = resp.ipReserves
        print("Delete subnet ipreserve: %s" % resp)

    except BceHttpClientError as e:
        print("Exception when calling API: %s" % e)
