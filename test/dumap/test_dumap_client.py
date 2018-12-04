# coding=utf-8
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
import json

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

    def test_locate_ip(self):
        """
        test locate ip
        """
        HOST = '10.64.79.132:8011'
        AK = '701107a8de6f41c29f74ec3f19da6c97'
        SK = 'ccc32a43dcb7495cb820919e2597e99b'
        config = BceClientConfiguration(credentials=BceCredentials(AK, SK), endpoint=HOST)
        client = dumap_client.DumapClient(config)

        params = {}
        params['ip'] = "61.135.162.115"

        response = client.call_open_api(
            uri='/location/ip',
            app_id='574f48d0-9c74-4ae4-8239-f0df906614e9',
            params=params
        )
        print response

    def test_locate_hardware(self):
        """
        test locate hardware
        """
        HOST = '10.64.79.132:8011'
        AK = '701107a8de6f41c29f74ec3f19da6c97'
        SK = 'ccc32a43dcb7495cb820919e2597e99b'
        config = BceClientConfiguration(credentials=BceCredentials(AK, SK), endpoint=HOST)
        client = dumap_client.DumapClient(config)

        body_elem_0 = {}
        body_elem_0['accesstype'] = 0
        body_elem_0['imei'] = '868573030002015'
        body_elem_0['smac'] = ''
        body_elem_0['clientip'] = ''
        body_elem_0['cdma'] = 0
        body_elem_0['imsi'] = ''
        body_elem_0['gps'] = ''
        body_elem_0['network'] = 'GSM'
        body_elem_0['tel'] = '17821710693'
        body_elem_0['bts'] = '460,0,22547,100666882,140'
        body_elem_0['mmac'] = ''
        body_elem_0['macs'] = 'aa:8d:4c:68:39:75,47,|24:de:c6:9a:9d:91,54,|30:fc:68:1d:cc:64,63,|00:1f:7a:4d:76:e1,74,|24:de:c6:9a:b3:81,76,|72:77:81:13:b3:ce,77,DIRECT-ce-HP M252 LaserJet|0c:37:47:dc:70:e0,80,|c0:61:18:8b:6f:00,84,|7c:76:30:c4:00:50,85,|24:de:c6:9a:9b:f0,87,'
        body_elem_0['coor'] = 'GCJ02'
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

        response = client.call_open_api(
            uri="/locapi/v2",
            app_id='697ce5f3-f59a-4a72-9c05-0ee7207465dc',
            body=json.dumps(params),
            method='POST'
        )
        print response


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
