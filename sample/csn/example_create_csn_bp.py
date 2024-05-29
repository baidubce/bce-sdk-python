# -*- coding: utf-8 -*-
"""
example for create csn bp.
"""

import uuid

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.csn import csn_client
from baidubce.services.csn import csn_model

if __name__ == "__main__":
    ak = "Your AK"
    sk = "Your SK"
    endpoint = "csn.baidubce.com"
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    csn_client = csn_client.CsnClient(config)
    billing= csn_model.Billing("Prepaid", 1, "month")
    try:
        resp = csn_client.create_csn_bp(name="csn_bp_test", bandwidth=10, geographic_a="China", geographic_b="China",
                                        billing=billing, interwork_type="center", client_token=str(uuid.uuid4()))
        csn_bp_id = resp.csn_bp_id
        print("Create csn bp response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s" % e)