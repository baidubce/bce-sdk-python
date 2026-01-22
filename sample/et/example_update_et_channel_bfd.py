# -*- coding: utf-8 -*-
"""
example for update et channel bfd.
"""

import uuid

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.et.et_client import EtClient


if __name__ == "__main__":
    ak = "Your AK"
    sk = "Your SK"
    endpoint = "bcc.bj.baidubce.com"
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    client = EtClient(config)
    try:
        resp = client.update_et_channel_bfd(et_id="Your Et ID",
                                            et_channel_id="Your Et Channel ID",
                                            detect_multiplier=4,
                                            send_interval=300,
                                            receive_interval=300,
                                            client_token=str(uuid.uuid4()))
        print("Update et channel bfd response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s" % e)