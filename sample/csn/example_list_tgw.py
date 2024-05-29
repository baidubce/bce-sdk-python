# -*- coding: utf-8 -*-
"""
example for list tgw.
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
    try:
        resp = csn_client.list_tgw(csn_id="Your csn-id", marker=None, max_keys=10)
        tgws = resp.tgws
        print("List tgw response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s" % e)