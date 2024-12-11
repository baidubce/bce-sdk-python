# -*- coding: utf-8 -*-
"""
example for associate et channel.
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
    et_id = "Your et_id"
    et_channel_id = "Your et_channel_id"
    extra_channel_id = "Your extra_channel_id"
    try:
        resp = et_client.associate_et_channel(et_id=et_id, et_channel_id=et_channel_id,
                                              extra_channel_id=extra_channel_id, client_token=str(uuid.uuid4()))
        print("Associate et channel response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s" % e)
