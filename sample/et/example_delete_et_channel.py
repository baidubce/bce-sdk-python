# -*- coding: utf-8 -*-
"""
example for delete et channel.
"""

import uuid

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.et import et_client


if __name__ == "__main__":
    ak = "Your AK"
    sk = "Your SK"
    endpoint = "bcc.bj.baidubce.com"
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    et_client = et_client.EtClient(config)
    try:
        resp = et_client.delete_et_channel(et_id="Your Et ID", et_channel_id="Your Et Channel ID",
                                           client_token=str(uuid.uuid4()))
        print("Delete et response: %s", resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s" % e)