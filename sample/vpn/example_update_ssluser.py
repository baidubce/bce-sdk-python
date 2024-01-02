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
        resp = vpn_client.update_vpn_ssl_user(vpn_id='vpn-bk1i8fsirenz',
                                              ssluser_id='vpn-ssl-user-8pdy9cbyh2et',
                                              description='update desc')
        request_id = resp.metadata.bce_request_id
        print("update vpn ssl user response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling: %s" % e)