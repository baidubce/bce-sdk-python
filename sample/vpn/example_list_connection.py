# !/usr/bin/env python
# coding=utf-8
"""
Samples for vpn client.
"""

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.vpn.vpn_client import VpnClient

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

    result = vpn_client.get_vpn_conn(vpn_id='vpn-b12z2iu0t3a1')

    for vpnconn in result.vpn_conns:
        print(vpnconn.vpn_conn_id)
        print(vpnconn)

    print(result.metadata.bce_request_id)

    

