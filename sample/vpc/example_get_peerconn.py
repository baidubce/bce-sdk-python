# -*- coding: utf-8 -*-
"""
example for get peerconn detail.
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
        resp = peerconn_client.get_peerconn(peer_conn_id="peerconn-9td54fmx143e")
        peer_conn_id = resp.peer_conn_id
        status = resp.status
        local_region = resp.local_region
        peer_region = resp.peer_region
        peer_account_id = resp.peer_account_id
        dns_status = resp.dns_status
        local_vpc_id = resp.local_vpc_id
        peer_vpc_id = resp.peer_vpc_id
        bandwith_in_mbp = resp.bandwith_in_mbp
        print("Get peerconn response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s" % e)