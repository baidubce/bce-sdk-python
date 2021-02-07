# -*- coding: utf-8 -*-
# @Time    : 2021/1/22 11:29 上午
# @Author  : xcy
# @File    : test_endpoint_client.py
# @Software: PyCharm

import sys
import unittest

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.endpoint import endpoint_client
from baidubce.services.endpoint.model import Billing

if sys.version < '3':
    reload(sys)
    sys.setdefaultencoding('utf-8')


class TestEndpointClient(unittest.TestCase):
    """
    unit test
    """

    def setUp(self):
        """
        set up
        """
        HOST = b''
        AK = b''
        SK = b''
        config = BceClientConfiguration(credentials=BceCredentials(AK, SK), endpoint=HOST)
        self.the_client = endpoint_client.EndpointClient(config)

    def test_list_services(self):
        """
        test case for list_services
        """
        print(self.the_client.list_services())

    def test_create_endpoint(self):
        """
        test case for create_endpoint
        """
        vpc_id = 'vpc-q1hcnhf7nmve'
        subnet_id = 'sbn-crqu2vxzj049'
        name = 'python-sdk-1'
        service = '77.uservice-a7f5795b.beijing.baidubce.com'
        billing = Billing(payment_timing='Postpaid')
        print(self.the_client.create_endpoint(vpc_id=vpc_id, subnet_id=subnet_id, name=name, service=service,
                                              billing=billing, description="python create"))

    def test_delete_endpoint(self):
        """
        test case for delete_endpoint
        """
        print(self.the_client.delete_endpoint(endpoint_id='endpoint-643ee50d'))

    def test_list_endpoints(self):
        """
        test case for list_endpoints
        """
        print(self.the_client.list_endpoints('vpc-q1hcnhf7nmve', name='sdk'))

    def test_get_endpoint(self):
        """
        test case for get_endpoint
        """
        print(self.the_client.get_endpoint('endpoint-643ee50d'))

    def test_update_endpoint(self):
        """
        test case for update_endpoint
        """
        print(self.the_client.update_endpoint('endpoint-643ee50d', name='sdk-123', description="test python sdk"))
