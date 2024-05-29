# -*- coding: utf-8 -*-

"""
This module for test vpn.
"""
import sys
import unittest

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.vpn import vpn_client
from baidubce.services.vpn.vpn_model import Billing
from baidubce.services.vpn.vpn_model import IkeConfig
from baidubce.services.vpn.vpn_model import IpsecConfig
from baidubce.services.vpn.vpn_model import Billing, IkeConfig, IpsecConfig, SSLUser

if sys.version < '3':
    reload(sys)
    sys.setdefaultencoding('utf-8')


class TestVpnClient(unittest.TestCase):
    """
    unit test
    """

    def setUp(self):
        """
        set up
        """
        HOST = b'host'
        AK = b'ak'
        SK = b'sk'
        config = BceClientConfiguration(credentials=BceCredentials(AK, SK), endpoint=HOST)
        self.the_client = vpn_client.VpnClient(config)

    def test_list_vpns(self):
        """
        test case for list_vpns
        """
        print(self.the_client.list_vpns('vpc-rif0euejenz7'))

    def test_create_vpn(self):
        """
        test case for create_vpn
        """
        billing = Billing('Postpaid', 'ByTraffic')
        print(self.the_client.create_vpn('vpc-rif0euejenz7', 'hzb_test_vpn_1', billing))

    def test_update_vpn(self):
        """
        test case for update vpn
        """
        print(self.the_client.update_vpn('vpn-suzg1sm2gd8f', 'hzb_test_vpn_update_1', '描述'))

    def test_get_vpn(self):
        """
        test case for get vpn
        """
        print(self.the_client.get_vpn('vpn-suzg1sm2gd8f'))

    def test_delete_vpn(self):
        """
        only allow the release of payment type as post-paid and no billing change task vpn instance
        test case for delete_vpn
        """
        print(self.the_client.delete_vpn('vpn-suzg1sm2gd8f'))

    def test_bind_eip(self):
        """
        test case for bind eip
        """
        print(self.the_client.bind_eip('vpn-bzehyume6vzh', 'your ip'))

    def test_unbind_eip(self):
        """
        test case for unbind eip
        """
        print(self.the_client.unbind_eip('vpn-bzehyume6vzh'))

    def test_renew_vpn(self):
        """
        test case for renew vpn
        """
        billing = Billing()
        print(self.the_client.renew_vpn('vpn-s28gd54ub5ce', billing))

    def test_create_vpn_conn(self):
        """
        test case for create vpnconn
        """
        ikeConfig = IkeConfig()
        ipsecConfig = IpsecConfig()
        print(self.the_client.create_vpn_conn('vpn-s28gd54ub5ce', 'your password', ['192.168.0.0/20'], 'your ip',
                                              ['192.168.100.0/24'], 'hzb_vpn_conn', ikeConfig, ipsecConfig))

    def test_update_vpn_conn(self):
        """
        test case for update vpnconn
        """
        ikeConfig = IkeConfig()
        ipsecConfig = IpsecConfig()
        print(self.the_client.update_vpn_conn('vpnconn-uk06cb68awe7', 'vpn-s28gd54ub5ce', 'your password',
                                              ['192.168.0.0/20'], 'your ip', ['192.168.100.0/24'],
                                              'hzb_vpn_conn', ikeConfig, ipsecConfig, '描述'))

    def test_get_vpn_conn(self):
        """
        test case for get vpnconn
        """
        print(self.the_client.get_vpn_conn('vpn-s28gd54ub5ce'))

    def test_delete_vpn_conn(self):
        """
        test case for delete vpnconn
        """
        print(self.the_client.delete_vpn_conn('vpnconn-ss8gdgpkh00n'))

    def test_create_sslvpn(self):
        """
        test case for create_vpn
        """
        billing = Billing('Postpaid', 'ByTraffic')
        print(self.the_client.create_vpn('vpc-rif0euejenz7', 'test-ssl-vpn', \
                                         billing, vpntype='SSL', max_connections=10))

    def test_create_sslservice(self):
        """
        test case for create_sslservice
        """
        print(self.the_client.create_vpn_sslservice(vpn_id='vpn-bk1i8fsirenz', sslservice_name='test_name', \
                                                    local_routes=['10.20.0.0/24', '10.20.1.0/24'], \
                                                    address_pool='10.20.3.0/24', interface_type='tun'))

    def test_update_sslservice(self):
        """
        test case for create_sslservice
        """
        print(self.the_client.update_vpn_sslservice(vpn_id='vpn-bk1i8fsirenz', sslservice_id='sslvpn-ymg18jxqcn0m', \
                                                    sslservice_name='test_nam1111e', local_routes=['10.20.0.0/16'], \
                                                    address_pool='10.20.3.0/24'))

    def test_get_sslservice(self):
        """
        test case for get_sslservice
        """
        print(self.the_client.get_vpn_sslservice(vpn_id='vpn-bk1i8fsirenz'))

    def test_delete_sslservice(self):
        """
        test case for delete_sslservice
        """
        print(self.the_client.delete_vpn_sslservice(vpn_id='vpn-bk1i8fsirenz', sslservice_id='sslvpn-ymg18jxqcn0m'))

    def test_create_ssluser(self):
        """
        test case for create_ssluser
        """
        ssluser = SSLUser("zhangsan", "1234567abc!", "zhangsan test")
        sslusers = [ssluser]
        print(self.the_client.create_vpn_sslusers(vpn_id='vpn-bk1i8fsirenz', sslusers=sslusers))

    def test_get_vpn_ssl_user(self):
        """
        test case for get_vpn_ssl_user
        """
        print(self.the_client.get_vpn_ssl_user(vpn_id='vpn-bk1i8fsirenz'))

    def test_update_vpn_ssl_user(self):
        """
        test case for update_vpn_ssl_user
        """
        print(self.the_client.update_vpn_ssl_user(vpn_id='vpn-bk1i8fsirenz', \
                                                  ssluser_id='vpn-ssl-user-8pdy9cbyh2et', \
                                                  description='update desc'))

    def test_delete_vpn_ssl_user(self):
        """
        test case for update_vpn_ssl_user
        """
        print(self.the_client.delete_vpn_ssl_user(vpn_id='vpn-bk1i8fsirenz', ssluser_id='vpn-ssl-user-8pdy9cbyh2et'))

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestVpnClient("test_update_vpn"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
