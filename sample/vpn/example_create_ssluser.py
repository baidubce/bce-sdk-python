# !/usr/bin/env python
# coding=utf-8
"""
Samples for vpn client.
"""

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.vpn.vpn_client import VpnClient
from baidubce.services.vpn.vpn_model import SSLUser

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

    ssluser = SSLUser("zhangsan", "1234567abc!", "zhangsan test")
    sslusers = [ssluser]

    result = vpn_client.create_vpn_sslusers(vpn_id='vpn-b4cs1yrbnrn9', sslusers=sslusers)
    for user_id in result.ssl_vpn_user_ids:
        print(user_id)

    print(result.metadata.bce_request_id)

