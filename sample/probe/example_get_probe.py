# -*- coding: utf-8 -*-
"""
example for get probe.
"""

import uuid

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.probe import probe_client

if __name__ == "__main__":
    ak = "Your AK"  # 账号的AK
    sk = "Your SK"  # 账号的SK
    endpoint = "bcc.bj.baidubce.com"  # 服务对应region的域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    probe_client = probe_client.ProbeClient(config)
    try:
        resp = probe_client.get_probe(probe_id='Your probe id')
        probe_id = resp.probe_id
        print("Get probe response: %s" % probe_id)
    except BceHttpClientError as e:
        print("Exception when calling api: %s" % e)