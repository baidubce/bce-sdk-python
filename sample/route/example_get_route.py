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
        # 方式1: 使用VPC ID查询
        vpc_id = "vpc-6tke3nxcmfzg"  # Replace with the VPC ID
                # Call the get_route method
        resp = route_client.get_route(vpc_id=vpc_id)
        vpcId = resp.vpcId
        print("Get route response: %s" % resp)

        # 方式2: 使用路由表ID查询
        route_table_id = "rt-1s7qb9mba41r"  # Replace with the ID of the route table
        resp = route_client.get_route(route_table_id=route_table_id)
        vpcId = resp.vpcId
        print("Get route response: %s" % resp)

    except BceHttpClientError as e:
        print("Exception when calling API: %s" % e)
