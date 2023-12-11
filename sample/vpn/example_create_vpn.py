# !/usr/bin/env python
# coding=utf-8
"""
Samples for vpn client.
"""

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
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

    billing = Billing('Postpaid', 'ByTraffic')
    result = vpn_client.create_vpn(vpc_id='vpc-kg01vdr7i7ar', vpn_name='mpc-ipsec', billing=billing)
    # result = vpn_client.create_vpn(vpc_id='vpc-kg01vdr7i7ar', vpn_name='mpc-ipsec',
    #                       billing=billing, vpn_type='SSL', max_connections=10)

    print(result.vpn_id)
    print(result.metadata.bce_request_id)