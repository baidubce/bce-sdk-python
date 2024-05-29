# !/usr/bin/env python
# coding=utf-8
"""
Samples for app blb client.
"""

import route_sample_conf
from baidubce.services.route.route_client import RouteClient
from baidubce.services.route.route_model import NextHop

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    __logger = logging.getLogger(__name__)

    # create an route client
    route_client = RouteClient(route_sample_conf.config)

    # create route rule
    route_client.create_route(route_table_id="route_table_id",
                                       source_address='12.0.0.0/25',
                                       destination_address='3.3.3.9/32',
                                       next_hop_id="",
                                       next_hop_type="dcGateway",
                                       description='3 sdk python dcgw single',
                                       client_token="client_token")

    # create  dcGateway Multi-line mode route rule

    active_route = NextHop(next_hop_id="", next_hop_type="dcGateway",
                                       path_type="ha:active");
    standby_route = NextHop(next_hop_id="", next_hop_type="dcGateway",
                                        path_type="ha:standby")
    next_hops = []
    next_hops.append(active_route)
    next_hops.append(standby_route)
    route_client.create_route(route_table_id="route_table_id",
                                       source_address='12.0.0.0/25',
                                       destination_address='3.3.3.6/32',
                                       next_hops=next_hops,
                                       description='2 sdk python dcgw mul',
                                       client_token="client_token")


