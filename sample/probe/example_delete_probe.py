# -*- coding: utf-8 -*-
"""
example for delete probe.
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
        resp = probe_client.delete_probe(probe_id='probe-mke05zx2ks9y1r1k')
        print("Delete probe response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s" % e)