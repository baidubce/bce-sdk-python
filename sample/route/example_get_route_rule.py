# -*- coding: utf-8 -*-
"""
Example for getting route rule details.
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
        # Specify the route rule ID to get details
        routeTableId = "rt-q1zg3i8mx8p6"
        vpcId = "vpc-nx6bs5uaq2a2"
        marker = "rr-dvq3cxpghw5e"  # mark the start point of query, deafault null
        maxKeys = 10  # max number of query in each page, default 1000

        # Call the get_route_rule method
        resp = route_client.get_route_rule(routeTableId=routeTableId,
                                           vpcId=vpcId,
                                           marker=marker,
                                           maxKeys=maxKeys)
        routeRules = resp.routeRules
        print("Get route rule details response: %s" % resp)

    except BceHttpClientError as e:
        print("Exception when calling API: %s" % e)
