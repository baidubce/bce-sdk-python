# -*- coding: utf-8 -*-
"""
example for list propagation.
"""

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.csn import csn_client

if __name__ == "__main__":
    ak = "Your AK"
    sk = "Your SK"
    endpoint = "csn.baidubce.com"
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    csn_client = csn_client.CsnClient(config)
    csn_rt_id = "csnRt-abq04k8795z5n597" # 云智能网路由表ID
    try:
        resp = csn_client.list_propagation(csn_rt_id=csn_rt_id)
        propagations = resp.propagations
        print("List propagation response: %s" % propagations)
    except BceHttpClientError as e:
        print("Exception when calling api: %s" % e)
