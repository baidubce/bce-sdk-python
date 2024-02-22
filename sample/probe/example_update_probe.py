# -*- coding: utf-8 -*-
"""
example for update probe.
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
        resp = probe_client.update_probe(probe_id='Your probe id',  # 探测id
                                         name='test_update',  # 探测名称
                                         frequency=20,  # 探测频率(次/分钟)，可选10、20或30
                                         dst_ip='10.254.38.5',  # 探测目的ip
                                         dst_port='80',  # 探测目的端口，当协议为UDP、TCP或DNS时可以修改
                                         description='probe update example',  #探测描述
                                         payload='test update',  # 协议为UDP或DNS时，可以修改
                                         client_token=str(uuid.uuid4()))
        print("Update probe response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s" % e)