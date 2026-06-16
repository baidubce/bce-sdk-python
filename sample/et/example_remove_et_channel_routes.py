# -*- coding: utf-8 -*-
"""
example for remove et channel routes
"""

import uuid

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.et.et_client import EtClient

if __name__ == "__main__":
    ak = "Your AK"
    sk = "Your SK"
    endpoint = 'Your endpoint'
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    client = EtClient(config)
    try:
        resp = client.remove_et_channel_routes(et_id='dcphy-gq65bz9ip712',
                                               et_channel_id='dedicatedconn-zy9t7n91k0iq',
                                               route_type='static-route',
                                               networks=['192.168.100.0/24'],
                                               ipv6_networks=['2400:da00:e003:0:15f::/87'],
                                               client_token=str(uuid.uuid4()))
        print("remove et channel routes response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s" % e)
