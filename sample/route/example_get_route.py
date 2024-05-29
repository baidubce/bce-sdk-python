# -*- coding: utf-8 -*-
"""
Example for getting route details.
"""

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.route import route_client

if __name__ == "__main__":
    ak = "Your AK"
    sk = "Your SK"
    endpoint = "your.route.endpoint.com"  # Replace with your route endpoint
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    route_client = route_client.RouteClient(config)

    try:
        # Specify the parameters for getting route details
        vpc_id = "vpc-nx6bs5uaq2d2"  # Replace with the VPC ID
        route_table_id = "rt-q1zg3i8mx8p6"  # Replace with the ID of the route table

        # Call the get_route method
        resp = route_client.get_route(vpc_id=vpc_id,
                                      route_table_id=route_table_id)
        vpcId = resp.vpcId
        print("Get route response: %s" % resp)

    except BceHttpClientError as e:
        print("Exception when calling API: %s" % e)
