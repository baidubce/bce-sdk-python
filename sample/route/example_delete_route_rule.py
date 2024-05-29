# -*- coding: utf-8 -*-
"""
Example for deleting a route.
"""

import uuid

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
        # Specify the parameters for deleting a route
        route_rule_id = "rr-dvq3cxpghw5e"  # Replace with the ID of the route rule you want to delete
        client_token = str(uuid.uuid4())

        # Call the delete_route method
        resp = route_client.delete_route(route_rule_id=route_rule_id,
                                         client_token=client_token)
        print("Delete route response: %s" % resp)
        
    except BceHttpClientError as e:
        print("Exception when calling API: %s" % e)
