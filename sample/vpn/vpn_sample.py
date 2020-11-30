# !/usr/bin/env python
# coding=utf-8
"""
Samples for vpn client.
"""

import vpn_sample_conf
from baidubce.services.vpn.vpn_client import VpnClient
from baidubce.services.vpn.vpn_model import Billing, IkeConfig, IpsecConfig

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    __logger = logging.getLogger(__name__)

    # create a vpn client
    vpn_client = VpnClient(vpn_sample_conf.config)

    # vpn list
    print(vpn_client.list_vpns(vpc_id='vpc-rif0euejenz7'))

    # create vpn
    billing = Billing('Postpaid', 'ByTraffic')
    vpn_client.create_vpn(vpc_id='vpc-rif0euejenz7', vpn_name='hzb_test_vpn_1', billing=billing)

    # update vpn
    vpn_client.update_vpn(vpn_id='vpn-suzg1sm2gd8f', vpn_name='hzb_test_vpn_update_1', description='描述')

    # get vpn
    print(vpn_client.get_vpn(vpn_id='vpn-suzg1sm2gd8f'))

    # delete vpn
    vpn_client.delete_vpn(vpn_id='vpn-suzg1sm2gd8f')

    # bind eip
    vpn_client.bind_eip(vpn_id='vpn-bzehyume6vzh', eip='your ip')

    # unbind eip
    vpn_client.unbind_eip(vpn_id='vpn-bzehyume6vzh')

    # renew vpn
    billing = Billing()
    vpn_client.renew_vpn(vpn_id='vpn-s28gd54ub5ce', billing=billing)

    # create vpn conn
    ikeConfig = IkeConfig()
    ipsecConfig = IpsecConfig()
    vpn_client.create_vpn_conn(vpn_id='vpn-s28gd54ub5ce', secret_key='your password', local_subnets=['192.168.0.0/20'],
                               remote_ip='your ip', remote_subnets=['192.168.100.0/24'], vpn_conn_name='hzb_vpn_conn',
                               ike_config=ikeConfig, ipsec_config=ipsecConfig)

    # update vpn cpnn
    ikeConfig = IkeConfig()
    ipsecConfig = IpsecConfig()
    vpn_client.update_vpn_conn(vpn_conn_id='vpnconn-uk06cb68awe7', vpn_id='vpn-s28gd54ub5ce',
                               secret_key='your password',
                               local_subnets=['192.168.0.0/20'], remote_ip='your ip',
                               remote_subnets=['192.168.100.0/24'],
                               vpn_conn_name='hzb_vpn_conn', ike_config=ikeConfig, ipsec_config=ipsecConfig)

    # get vpn conn
    print(vpn_client.get_vpn_conn(vpn_id='vpn-s28gd54ub5ce'))

    # delete vpn conn
    vpn_client.delete_vpn_conn(vpn_conn_id='vpnconn-ss8gdgpkh00n')
