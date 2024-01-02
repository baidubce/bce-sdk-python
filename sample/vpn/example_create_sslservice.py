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
        resp = vpn_client.create_vpn_sslservice(vpn_id='vpn-b4cs1yrbnrn9', sslservice_name='test_name',
                                                local_routes=['10.20.0.0/24', '10.20.1.0/24'],
                                                address_pool='10.20.3.0/24', interface_type='tun')
        vpn_sslservice_id = resp.ssl_vpn_server_id
        request_id = resp.metadata.bce_request_id
        print("create vpn ssl service response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling: %s" % e)

