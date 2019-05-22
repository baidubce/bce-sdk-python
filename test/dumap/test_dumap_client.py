# -*- coding: UTF-8 -*-
# Copyright (c) 2018 Baidu.com, Inc. All Rights Reserved
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

from baidubce.services.dumap import dumap_client
import dumap_test_config

import json


class TestDumapClient(unittest.TestCase):
    """
    unit test
    """

    def setUp(self):
        """
        set up
        """
        self.the_client = dumap_client.DumapClient(dumap_test_config.config)

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
            uri=b'/place/v2/search',
            app_id=dumap_test_config.APP_ID,
            params=params)
        print(response)

    def test_geocoder(self):
        """
        test call geocoder
        """
        params = {}
        params['address'] = '北京市海淀区上地十街10号'

        response = self.the_client.call_open_api(
            uri=b'/geocoder/v2/',
            app_id=dumap_test_config.APP_ID,
            params=params)
        print(response)

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
            uri=b'/geoconv/v1/',
            app_id=dumap_test_config.APP_ID,
            params=params)
        print(response)

    def test_direction(self):
        """
        test call direction
        """
        params = {}
        params['origin'] = '40.056878,116.30815'
        params['destination'] = '31.222965,121.505821'

        response = self.the_client.call_open_api(
            uri=b'/direction/v2/transit',
            app_id=dumap_test_config.APP_ID,
            params=params)
        print(response)

    def test_locate_ip(self):
        """
        test locate ip
        """

        params = {}
        params['ip'] = ""

        response = self.the_client.call_open_api(
            uri=b'/location/ip',
            app_id=dumap_test_config.APP_ID,
            params=params
        )
        print(response)

    def test_locate_hardware(self):
        """
        test locate hardware
        """

        body_elem_0 = {}
        body_elem_0['accesstype'] = 0
        body_elem_0['imei'] = ''
        body_elem_0['smac'] = ''
        body_elem_0['clientip'] = ''
        body_elem_0['cdma'] = 0
        body_elem_0['imsi'] = ''
        body_elem_0['gps'] = ''
        body_elem_0['network'] = ''
        body_elem_0['tel'] = ''
        body_elem_0['bts'] = ''
        body_elem_0['mmac'] = ''
        body_elem_0['macs'] = ''
        body_elem_0['coor'] = ''
        body_elem_0['output'] = 'JSON'
        body_elem_0['ctime'] = '1'
        body_elem_0['need_rgc'] = 'Y'

        body = [body_elem_0]

        params = {}
        params['src'] = ''
        params['prod'] = ''
        params['ver'] = '1.0'
        params['trace'] = False
        params['body'] = body

        response = self.the_client.call_open_api(
            uri=b'/locapi/v2',
            app_id=dumap_test_config.APP_ID,
            body=json.dumps(params),
            method=b'POST'
        )
        print(response)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestDumapClient("test_place_search"))
    suite.addTest(TestDumapClient("test_geocoder"))
    suite.addTest(TestDumapClient("test_geoconv"))
    suite.addTest(TestDumapClient("test_direction"))
    suite.addTest(TestDumapClient("test_locate_ip"))
    suite.addTest(TestDumapClient("test_locate_hardware"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
