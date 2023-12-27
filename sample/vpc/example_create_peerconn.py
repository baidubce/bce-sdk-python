# -*- coding: utf-8 -*-
"""
example for create peerconn.
"""

import uuid

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.vpc import peerconn_client
from baidubce.services.vpc import peerconn_model

if __name__ == "__main__":
    ak = "Your AK"
    sk = "Your SK"
    endpoint = "bcc.bj.baidubce.com"
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    peerconn_client = peerconn_client.PeerConnClient(config)
    try:
        resp = peerconn_client.create_peerconn(client_token=str(uuid.uuid4()),
                                               bandwidth_in_mbps=500,
                                               local_vpc_id='vpc-13vuxu016dew',
                                               peer_vpc_id='vpc-jcvmhw9h1a35',
                                               peer_region='bj',
                                               billing=peerconn_model.Billing('Postpaid'),
                                               description='peer_same_account',
                                               local_if_name='localIfName',
                                               peer_if_name='peerIfName')
        peer_conn_id = resp.peer_conn_id
        print("Create peerconn response: %s", resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s" % e)