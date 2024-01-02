# -*- coding: utf-8 -*-
"""
example for enable et channel ipv6.
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
        resp = et_client.enable_et_channel_ipv6(et_id="Your et_id", et_channel_id="Your et_channel_id",
                                                local_ipv6="BaiduIPv6Address", remote_ipv6="CustomerIPv6Address",
                                                ipv6_networks=["Your IPv6 cidr"], client_token=str(uuid.uuid4()))
        print("Enable et IPv6 response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s" % e)