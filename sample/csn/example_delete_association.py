# -*- coding: utf-8 -*-
"""
example for delete association.
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
    try:
        resp = csn_client.delete_association(csn_rt_id="csn_rt_id", attach_id="attach_id",
                                             client_token=str(uuid.uuid4()))
        print("Delete csn association response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)
