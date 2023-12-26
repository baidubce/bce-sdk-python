# -*- coding: utf-8 -*-
"""
example for et channel route rule.
"""
import uuid

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.et import et_client

if __name__ == '__main__':
    ak = "Your Ak"  # 账号的Ak
    sk = "Your Sk"  # 账号的Sk
    endpoint = "bcc.bj.baidubce.com"  # 服务对应的Region域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    client = et_client.EtClient(config)

    try:
        resp = client.delete_et_channel_route_rule(et_id="Your etId",
                                                   et_channel_id="Your etChannelId",
                                                   et_channel_route_rule_id="Your routeRuleId",
                                                   client_token=str(uuid.uuid4()))
        print("delete et channel route rule response: %s." % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s.\n" % e)
