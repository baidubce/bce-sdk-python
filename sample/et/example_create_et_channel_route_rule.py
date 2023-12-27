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
        resp = client.create_et_channel_route_rule(et_id="dcphy-gq65bz9ip712",
                                                   et_channel_id="dedicatedconn-zy9t7n91k0iq",
                                                   dest_address="192.168.0.7/32",
                                                   nexthop_type="etGateway",
                                                   nexthop_id="dcgw-p5x55p77u8ah",
                                                   description="Your description",
                                                   ip_version=4,
                                                   client_token=str(uuid.uuid4()))
        print("Create et channel route rule successfully, response: %s." % resp)
        print("request_id: %s, route_rule_id: %s." % 
              (resp.metadata.bce_request_id, resp.route_rule_id))
    except BceHttpClientError as e:
        print("Exception when calling api: %s." % e)
