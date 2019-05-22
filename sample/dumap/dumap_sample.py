# coding=utf-8
# Copyright (c) 2018 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
"""
Samples for dumap client.
"""

import dumap_sample_conf
from baidubce.services.dumap.dumap_client import DumapClient

import xml.etree.cElementTree as ET
import json

def test_place_search(dumap_client):
    """
    test_place_serach
    """
    params = {}
    params['query'] = 'ATM机'
    params['tag'] = '银行'
    params['region'] = '北京'
    params['output'] = 'json'

    response = dumap_client.call_open_api(
        uri=b'/place/v2/search',
        app_id=dumap_sample_conf.APP_ID,
        params=params)
    print(response)

    # josn 解析
    body = json.loads(response.body)
    print(body["status"])


def test_geocoder(dumap_client):
    """
    test_geocoder
    """
    params = {}
    params['address'] = '北京市海淀区上地十街10号'

    response = dumap_client.call_open_api(
        uri=b'/geocoder/v2/',
        app_id=dumap_sample_conf.APP_ID,
        params=params)
    print(response)

    # xml 解析
    GeocoderSearchResponse = ET.fromstring(response.body)
    print(GeocoderSearchResponse[0].text)  # status
    print(GeocoderSearchResponse[1][0][0].text)  # GeocoderSearchResponse.result.location.lng
    print(GeocoderSearchResponse[1][0][1].text)  # GeocoderSearchResponse.result.location.lat
    print(GeocoderSearchResponse[1][1].text)  # GeocoderSearchResponse.result.precise


def test_geoconv(dumap_client):
    """
    test_geoconv
    """
    params = {}
    params['coords'] = '114.21892734521,29.575429778924'
    params['from'] = 1
    params['to'] = 5
    params['output'] = 'json'

    response = dumap_client.call_open_api(
        uri=b'/geoconv/v1/',
        app_id=dumap_sample_conf.APP_ID,
        params=params)
    print(response)


def test_direction(dumap_client):
    """
    test_direction
    """
    params = {}
    params['origin'] = '40.056878,116.30815'
    params['destination'] = '31.222965,121.505821'

    response = dumap_client.call_open_api(
        uri=b'/direction/v2/transit',
        app_id=dumap_sample_conf.APP_ID,
        params=params)
    print(response)


def test_locate_ip(dumap_client):
    """
    test locate ip
    """

    params = {}
    params['ip'] = ""

    response = dumap_client.call_open_api(
        uri=b'/location/ip',
        app_id=dumap_sample_conf.APP_ID,
        params=params
    )
    print(response)


def test_locate_hardware(dumap_client):
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

    response = dumap_client.call_open_api(
        uri=b'/locapi/v2',
        app_id=dumap_sample_conf.APP_ID,
        body=json.dumps(params),
        method=b'POST'
    )
    print(response)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    __logger = logging.getLogger(__name__)

    dumap_client = DumapClient(dumap_sample_conf.config)
    test_geocoder(dumap_client)
    test_place_search(dumap_client)
    test_geoconv(dumap_client)
    test_direction(dumap_client)
    test_locate_ip(dumap_client)
    test_locate_hardware(dumap_client)
