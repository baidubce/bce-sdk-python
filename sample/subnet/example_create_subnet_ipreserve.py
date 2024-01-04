# -*- coding: utf-8 -*-
"""
Example for creating a reserved subnet.
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
        # Specify the parameters for creating a reserved subnet
        subnet_id = "sbn-a4cikyt7756r"  # Replace with your subnet ID
        ip_cidr = "192.168.0.100/30"  # Replace with your desired IP CIDR
        ip_version = 4  # Use 4 for IPv4, 6 for IPv6
        description = "YourDescription"
        client_token = str(uuid.uuid4())

        # Call the create_subnet_ipreserve method
        resp = subnet_client.create_subnet_ipreserve(subnet_id=subnet_id,
                                                     ip_cidr=ip_cidr,
                                                     ip_version=ip_version,
                                                     description=description,
                                                     client_token=client_token)
        ipReserveId = resp.ipReserveId
        print("Create subnet ipreserve: %s" % resp)
        
    except BceHttpClientError as e:
        print("Exception when calling API: %s" % e)
