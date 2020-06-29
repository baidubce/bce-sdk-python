# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the
# License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.

"""
Unit tests for cert client.
"""

import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
rootPath = os.path.split(rootPath)[0]
sys.path.append(rootPath)

import unittest
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.cert import cert_client
from baidubce.services.cert import cert_model

cert_server_data = """
"""

cert_private_data = """
"""

cert_link_data = """
"""


def get_create_request():
    """
    The method to generate a certificate create request

    :return:
    :rtype string
    """
    return cert_model.CertCreateRequest('test_cert', cert_server_data, cert_private_data, cert_link_data, 1)


class TestCertClient(unittest.TestCase):
    """
    unit test
    """

    def setUp(self):
        """
        set up
        """

        host = ''
        ak = ''
        sk = ''
        config = BceClientConfiguration(credentials=BceCredentials(ak, sk), endpoint=host)
        self.the_client = cert_client.CertClient(config)

        # clean certificates
        for cert in self.the_client.list_user_certs().certs:
            self.the_client.delete_cert(cert.cert_id)

    def tearDown(self):
        """
        tear down
        """

        self.the_client = None

    def test_create_cert(self):
        """
        test case for create certificate
        """

        # test: create certificate
        response = self.the_client.create_cert(get_create_request())
        self.assertEqual('test_cert', response.cert_name)

        # clean
        self.the_client.delete_cert(response.cert_id)

    def test_list_cert(self):
        """
        test case for list certificate
        """

        # create certificate
        cert_id = self.the_client.create_cert(get_create_request()).cert_id

        # test: list certificate
        response = self.the_client.list_user_certs()
        cert = response.certs[0]
        self.assertEqual(cert_id, cert.cert_id)
        self.assertEqual('test_cert', cert.cert_name)

        # clean
        self.the_client.delete_cert(cert.cert_id)

    def test_get_cert(self):
        """
        test case for get certificate
        """

        # create certificate
        cert_id = self.the_client.create_cert(get_create_request()).cert_id

        # test: get certificate
        response = self.the_client.get_cert_info(cert_id)
        self.assertEqual(cert_id, response.cert_id)
        self.assertEqual('test_cert', response.cert_name)

        # clean
        self.the_client.delete_cert(response.cert_id)

    def test_replace_cert(self):
        """
        test case for replace certificate
        """

        # create certificate
        cert_id = self.the_client.create_cert(get_create_request()).cert_id

        # test: replace certificate
        cert_replace_request = get_create_request()
        cert_replace_request.certName = 'new_test_cert'
        self.the_client.replace_cert(cert_id, cert_replace_request)

        # delete certificate
        self.the_client.delete_cert(cert_id)

    def test_delete_cert(self):
        """
        test case for delete certificate
        """

        # create certificate
        cert_id = self.the_client.create_cert(get_create_request()).cert_id

        # test: delete certificate
        response = self.the_client.delete_cert(cert_id)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    # suite.addTest(TestCertClient('test_create_cert'))
    # suite.addTest(TestCertClient('test_list_cert'))
    # suite.addTest(TestCertClient('test_get_cert'))
    # suite.addTest(TestCertClient('test_replace_cert'))
    # suite.addTest(TestCertClient('test_delete_cert'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
