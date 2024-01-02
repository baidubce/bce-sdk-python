# !/usr/bin/env python
# coding=utf-8
"""
Samples for vpn client.
"""

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.vpn.vpn_client import VpnClient
from baidubce.services.vpn.vpn_model import Billing

if __name__ == "__main__":
    config = BceClientConfiguration(
        credentials=BceCredentials(
            access_key_id='', # 用户的ak
            secret_access_key='' # 用户的sk
        ),
        endpoint='bcc.bj.baidubce.com' # 请求的域名信息
    )

    # create a vpn client
    vpn_client = VpnClient(config)

    try:
        billing = Billing('Postpaid')
        resp = vpn_client.create_vpn(vpc_id='vpc-kg01vdr7i7ar', vpn_name='mpc-ipsec', billing=billing)
        # resp = vpn_client.create_vpn(vpc_id='vpc-kg01vdr7i7ar', vpn_name='mpc-ipsec',
        #                              billing=billing, vpn_type='SSL', max_connections=10)
        vpn_id = resp.vpn_id
        request_id = resp.metadata.bce_request_id
        print("create vpn gw response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling: %s" % e)