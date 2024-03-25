# !/usr/bin/env python
# coding=utf-8
"""
Samples for vpn client.
"""

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
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
    try:
        resp = vpn_client.get_vpn_ssl_user(vpn_id='vpn-b4cs1yrbnrn9')
        for ssl_user in resp.ssl_vpn_users:
            print("ssl user id: %s" % ssl_user.user_id)
            print("ssl user name: %s" % ssl_user.user_name)
            print("ssl user description: %s" % ssl_user.description)
        request_id = resp.metadata.bce_request_id
        print("list vpn ssl user response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling: %s" % e)