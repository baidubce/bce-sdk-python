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
        # 查询详情（不指定 role）
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

        # 查询详情（指定 role 为发起端）
        resp_initiator = peerconn_client.get_peerconn(peer_conn_id="peerconn-bpz9thzzy2hk",
                                                      role="initiator")
        print("Get peerconn (initiator) response: %s" % resp_initiator)

        # 查询详情（指定 role 为接受端）
        resp_acceptor = peerconn_client.get_peerconn(peer_conn_id="peerconn-bpz9thzzy2hk",
                                                     role="acceptor")
        print("Get peerconn (acceptor) response: %s" % resp_acceptor)
    except BceHttpClientError as e:
        print("Exception when calling api: %s" % e)