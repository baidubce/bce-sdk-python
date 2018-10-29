#coding=utf-8
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
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
Unit tests for dumap client.
"""

import unittest

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.dumap import dumap_client


class TestDumapClient(unittest.TestCase):
    """
    unit test
    """
    def setUp(self):
        """
        set up
        """
        HOST = '10.64.79.132:8011'
        # online AK SK
        SK = '6ccf204afbde4488a8d1518c4142aad1'
        AK = '7ada90b3347b4319b6053baaf3baa787'
        config = BceClientConfiguration(credentials=BceCredentials(AK, SK), endpoint=HOST)
        self.the_client = dumap_client.DumapClient(config)

    def tearDown(self):
        """
        tear down
        """
        self.the_client = None

    def test_place_search(self):
        """
        test call place_serach
        """
        params = {}
        params['query'] = 'ATM机'
        params['tag'] = '银行'
        params['region'] = '北京'
        params['output'] = 'json'

        response = self.the_client.call_open_api(
            uri='/place/v2/search',
            app_id='app_id_test',
            params=params)
        print response

    def test_geocoder(self):
        """
        test call geocoder
        """
        params = {}
        params['address'] = '北京市海淀区上地十街10号'

        response = self.the_client.call_open_api(
            uri='/geocoder/v2/',
            app_id='app_id_test',
            params=params)
        print response

    def test_geoconv(self):
        """
        test call geoconv
        """
        params = {}
        params['coords'] = '114.21892734521,29.575429778924'
        params['from'] = 1
        params['to'] = 5
        params['output'] = 'json'

        response = self.the_client.call_open_api(
            uri='/geoconv/v1/',
            app_id='app_id_test',
            params=params)
        print response

    def test_direction(self):
        """
        test call direction
        """
        params = {}
        params['origin'] = '40.056878,116.30815'
        params['destination'] = '31.222965,121.505821'

        response = self.the_client.call_open_api(
            uri='/direction/v2/transit',
            app_id='app_id_test',
            params=params)
        print response



if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestDumapClient("test_place_search"))
    suite.addTest(TestDumapClient("test_geocoder"))
    suite.addTest(TestDumapClient("test_geoconv"))
    suite.addTest(TestDumapClient("test_direction"))
    runner = unittest.TextTestRunner()
    runner.run(suite)