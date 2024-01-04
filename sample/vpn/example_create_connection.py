# !/usr/bin/env python
# coding=utf-8
"""
Samples for vpn client.
"""

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.vpn.vpn_client import VpnClient
from baidubce.services.vpn.vpn_model import IkeConfig, IpsecConfig

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
        ike_config = IkeConfig(ike_version="v1", ike_mode="main", ike_enc_alg="aes",
                               ike_auth_alg="sha1", ike_pfs="group2", ike_lifeTime="3600")
        ipsec_config = IpsecConfig(ipsec_enc_alg="aes", ipsec_auth_alg="sha1",
                                   ipsec_pfs="group2", ipsec_lifetime="3600")
        resp = vpn_client.create_vpn_conn(vpn_id='vpn-b12z2iu0t3a1', secret_key='qwer@1234',
                                          local_subnets=['192.168.0.0/24'], remote_ip='2.2.2.2',
                                          remote_subnets=['10.20.1.0/24'], vpn_conn_name='aaaa1111',
                                          ike_config=ike_config, ipsec_config=ipsec_config, description="test")
        vpn_conn_id = resp.vpn_conn_id
        request_id = resp.metadata.bce_request_id
        print("create vpn connection response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling: %s" % e)