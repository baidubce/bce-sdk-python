# -*- coding: utf-8 -*-
"""
example for get csn bp price.
"""

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.csn import csn_client, csn_model

if __name__ == "__main__":
    ak = "Your AK"
    sk = "Your SK"
    endpoint = "csn.baidubce.com"
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    csn_client = csn_client.CsnClient(config)
    billing= csn_model.Billing("Prepaid", 1, "month", "ByBandwidth")
    try:
        resp = csn_client.get_csn_bp_price(name='test', geographic_a='China', geographic_b='China',
                                           billing=billing, bandwidth=10)
        csn_id = resp.csn_id
        name = resp.name
        description = resp.description
        status = resp.status
        instance_num = resp.instance_num
        csn_bp_num = resp.csn_bp_num
        print("Get csn response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s" % e)