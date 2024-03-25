# -*- coding: utf-8 -*-
"""
example for open peerconn sync dns.
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
        resp = peerconn_client.open_peerconn_dns_sync(peer_conn_id="peerconn-9td54fmx143e",
                                                      role="initiator",
                                                      client_token=str(uuid.uuid4()))
        print("Open peerconn sync dns response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s" % e)