# -*- coding: utf-8 -*-
"""
Example for listing reserved subnets.
"""

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
        # Specify optional parameters for listing reserved subnets
        subnet_id = "sbn-a4cikyt7756r"  # Replace with the ID of the subnet
        marker = "sbn-a4cikyt7756r"  # mark the start point of query, deafault null
        max_keys = 1000  # max number of query in each page, default 1000

        # Call the list_subnet_ipreserve method
        resp = subnet_client.list_subnet_ipreserve(subnet_id=subnet_id, 
                                                   marker=marker,
                                                   max_keys=max_keys)
        ipReserves = resp.ipReserves
        print("List subnet ipreserve: %s" % resp)

    except BceHttpClientError as e:
        print("Exception when calling API: %s" % e)
