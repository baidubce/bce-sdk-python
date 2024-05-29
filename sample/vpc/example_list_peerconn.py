# -*- coding: utf-8 -*-
"""
example for list peerconn.
"""

import uuid

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.vpc import peerconn_client

if __name__ == "__main__":
    ak = "Your AK"
    sk = "Your SK"
    endpoint = "bcc.bj.baidubce.com"
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    peerconn_client = peerconn_client.PeerConnClient(config)
    try:
        resp = peerconn_client.list_peerconns(vpc_id="vpc-13vuxu016dew",
                                              marker="20",
                                              max_keys=1)
        peer_conns = resp.peer_conns
        print("List peerconn response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s" % e)