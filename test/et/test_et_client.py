# -*- coding: utf-8 -*-

"""
This module for test et.
"""
import sys
import uuid
import unittest

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.et import et_client
from baidubce.services.et.model import ETStatus

et_id = 'dcphy-gq65bz9ip712'
etchannel_id = 'dedicatedconn-zy9t7n91k0iq'
authorized_users = ['xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx']
description = ''
local_ip = '11.11.11.21/24'
remote_ip = '11.11.11.12/24'
name = 'channel_name'
networks = ['192.168.0.0/16']
route_type = 'static-route'
vlan_id = 56
enable_ipv6 = 1
local_ipv6 = '2400:da00:e003:0:1eb:200::1/88'
remote_ipv6 = '2400:da00:e003:0:0:200::1/88'
ipv6_networks = ['2400:da00:e003:0:15f::/87']


if sys.version < '3':
    reload(sys)
    sys.setdefaultencoding('utf-8')

def generate_client_token_by_uuid():
    """
    The default method to generate the random string for client_token
    if the optional parameter client_token is not specified by the user.
    :return:
    :rtype string
    """
    return str(uuid.uuid4())

generate_client_token = generate_client_token_by_uuid

class TestEtClient(unittest.TestCase):
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
        self.the_client = et_client.EtClient(config)

    def test_get_et_channel(self):
        """
        test case for get et channel
        """
        client_token = generate_client_token()

        print(self.the_client.get_et_channel(et_id, client_token=client_token))

    def test_recommit_et_channel(self):
        """
        test case for recommit et channel
        """
        client_token = generate_client_token()

        print(self.the_client.recommit_et_channel(et_id, etchannel_id, authorized_users, description,
                                                  local_ip, name, networks, remote_ip, route_type,
                                                  vlan_id, enable_ipv6, local_ipv6, remote_ipv6,
                                                  ipv6_networks, client_token=client_token))

    def test_update_et_channel(self):
        """
        test case for update et channel
        """
        client_token = generate_client_token()

        print(self.the_client.update_et_channel(et_id, etchannel_id, description,
                                                name, client_token=client_token))

    def test_delete_et_channel(self):
        """
        test case for delete et channel
        """
        client_token = generate_client_token()

        print(self.the_client.delete_et_channel(et_id, etchannel_id, client_token=client_token))

    def test_enable_et_channel_ipv6(self):
        """
        test case for enable et channel ipv6
        """
        client_token = generate_client_token()

        print(self.the_client.enable_et_channel_ipv6(et_id, etchannel_id, local_ipv6, remote_ipv6,
                                                     ipv6_networks, client_token=client_token))

    def test_disable_et_channel_ipv6(self):
        """
        test case for disable et channel ipv6
        """
        client_token = generate_client_token()
        print(self.the_client.disable_et_channel_ipv6(et_id, etchannel_id, client_token=client_token))

    def test_create_et_dcphy(self):
        """
        test case for create_et_dcphy
        """
        self.the_client.create_et_dcphy('et_18', 'ISP_CMCC', '1G', 'SINGLE', 'BJYZ', 'z3',
                                        '13333333333', '123@123.com', 'BJ|K2')
        
    def test_update_et_dcphy(self):
        """
        test case for update_et_dcphy
        """
        self.the_client.update_et_dcphy('dcphy-2222', name='et_update', user_name='z3', user_phone='13333333336', user_email='123@126.com')

    def test_list_et_dcphy(self):
        """
        test case for list_et_dcphy
        """
        self.the_client.list_et_dcphy()
        
    def test_list_et_dcphy_detail(self):
        """
        test case for list_et_dcphy_detail
        """
        self.the_client.list_et_dcphy_detail('dcphy-2222')

    def test_create_et_channel(self):
        """
        test case for create_et_channel
        """
        self.the_client.create_et_channel('dcphy-234r5', '172.1.1.1/24', 'testChannel', '172.1.1.2/24',
                                          'static-route', 100)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    #suite.addTest(TestEtClient("test_create_et_dcphy"))
    #suite.addTest(TestEtClient("test_update_et_dcphy"))
    #suite.addTest(TestEtClient("test_list_et_dcphy"))
    #suite.addTest(TestEtClient("test_list_et_dcphy_detail"))
    #suite.addTest(TestEtClient("test_create_et_channel"))
    #suite.addTest(TestEtClient("test_get_et_channel"))
    #suite.addTest(TestEtClient("test_recommit_et_channel"))
    #suite.addTest(TestEtClient("test_update_et_channel"))
    #suite.addTest(TestEtClient("test_delete_et_channel"))
    #suite.addTest(TestEtClient("test_enable_et_channel_ipv6"))
    #suite.addTest(TestEtClient("test_disable_et_channel_ipv6"))
    runner = unittest.TextTestRunner()
    runner.run(suite)