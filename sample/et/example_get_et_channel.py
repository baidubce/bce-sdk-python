# -*- coding: utf-8 -*-
"""
example for get et channel.
"""

import uuid
import sys

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.et.et_client import EtClient


if sys.version < '3':
    reload(sys)
    sys.setdefaultencoding('utf-8')

if __name__ == "__main__":
    ak = "Your AK"
    sk = "Your SK"
    endpoint = "bcc.bj.baidubce.com"
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    client = EtClient(config)
    try:
        # 获取所有专线通道
        resp = client.get_et_channel(et_id="Your Et ID", client_token=str(uuid.uuid4()))
        et_channels = resp.et_channels
        print("Get all et channels response: %s" % resp)

        # 获取指定专线通道
        resp = client.get_et_channel(et_id="Your Et ID", et_channel_id="Your Et Channel ID",
                                     client_token=str(uuid.uuid4()))
        print("Get specific et channel response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s" % e)