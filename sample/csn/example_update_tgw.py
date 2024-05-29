# -*- coding: utf-8 -*-
"""
example for update tgw.
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
    update_tgw_request = {
        "name": "csn_test",
        "description": "csn_test description"
    }
    try:
        resp = csn_client.update_tgw(csn_id="Your csn_id", tgw_id="Your tgw_id",
                                     update_tgw_request=update_tgw_request)
        print("Update csn response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s" % e)