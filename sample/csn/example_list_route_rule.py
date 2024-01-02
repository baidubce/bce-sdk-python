# -*- coding: utf-8 -*-
"""
example for list route rule.
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
        resp = csn_client.list_route_rule(csn_rt_id=csn_rt_id)
        route_rules = resp.csnRtRules
        print("List csn route rule response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s" % e)
