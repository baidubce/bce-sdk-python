# -*- coding: utf-8 -*-
"""
Example for updating a route.
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
        # Specify the parameters for updating a route
        route_rule_id = "rr-rbn5yyz6rtn8"  # Replace with the ID of the route rule to be updated
        source_address = "192.168.0.0/20"  # Replace with the new source address
        destination_address = "0.0.0.0/0"  # Replace with the new destination address
        next_hop_type = "nat"
        description = "NewRouteDescription"  # Replace with the new route description
        next_hop_id = "nat-bdidwhwfwc7y"
        ip_version = 4 # Use 4 for IPv4, 6 for IPv6
        next_hops = []
        client_token = str(uuid.uuid4())

        # if you want to append a list of next_hops, cancel the comments below and append more next hops
        # next_hop = route_model.NextHop(next_hop_id="", next_hop_type="next_hop_type",
        #                                    path_type="next_hop_path_type")
        # next_hops.append(next_hop)

        # Call the update_route method
        resp = route_client.update_route(route_rule_id=route_rule_id,
                                         source_address=source_address,
                                         destination_address=destination_address,
                                         next_hop_type=next_hop_type,
                                         description=description,
                                         next_hop_id=next_hop_id,
                                         ip_version=ip_version,
                                         next_hops=next_hops,
                                         client_token=client_token)                  
        print("Update route response: %s" % resp)
        
    except BceHttpClientError as e:
        print("Exception when calling API: %s" % e)
