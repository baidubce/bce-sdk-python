# -*- coding: utf-8 -*-
"""
example for create propagation.
"""

import uuid

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
    attach_id = "tgwAttach-n7yctm9zm605raig" # 网络实例在云智能网中的身份的ID
    try:
        resp = csn_client.create_propagation(csn_rt_id=csn_rt_id, attach_id=attach_id, client_token=str(uuid.uuid4()))
        print("Create csn propagation response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s" % e)
