# coding=utf-8
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
import json
import urllib

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
        HOST = 'your_host'
        SK = 'your_sk'
        AK = 'your_ak'
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

        params = {}
        params['ip'] = ""

        response = self.the_client.call_open_api(
            uri='/location/ip',
            app_id='app_id_test',
            params=params
        )
        print response

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
            uri="/locapi/v2",
            app_id='app_id_test',
            body=json.dumps(params),
            method='POST'
        )
        print response

    """ trace service test """

    def test_create_service(self):
        """
        Test create service.
        """
        request = {}
        request['appId'] = 'YOUR_APP_ID'
        request['name'] = 'python'
        request['desc'] = 'python'
        request['type'] = 0

        params = {}
        params['create'] = None

        response = self.the_client.call_open_api(
            uri='/v1/trace/service',
            params=params,
            body=json.dumps(request),
            method='POST'
        )
        print response

    def test_update_service(self):
        """
        Test update service.
        """
        request = {}
        request['appId'] = 'YOUR_APP_ID'
        request['serviceId'] = 4
        request['name'] = 'python'
        request['desc'] = 'python'

        params = {}
        params['update'] = None

        response = self.the_client.call_open_api(
            uri='/v1/trace/service',
            params=params,
            body=json.dumps(request),
            method='POST'
        )
        print response

    def test_get_service_detail(self):
        """
        Test get service detail.
        """
        params = {}
        params['appId'] = 'YOUR_APP_ID'
        params['serviceId'] = 4

        response = self.the_client.call_open_api(
            uri='/v1/trace/service/detail',
            params=params,
            method='GET'
        )
        print response

    def test_list_service(self):
        """
        Test list service.
        """
        params = {}
        params['appId'] = 'YOUR_APP_ID'
        params['pageIndex'] = 1
        params['pageSize'] = 10

        response = self.the_client.call_open_api(
            uri='/v1/trace/service/list',
            params=params,
            method='GET'
        )
        print response

    def test_delete_service(self):
        """
        Test delete service.
        """
        params = {}
        params['appId'] = 'YOUR_APP_ID'
        params['serviceId'] = 116

        response = self.the_client.call_open_api(
            uri='/v1/trace/service',
            params=params,
            method='DELETE'
        )
        print response

    def test_add_entity(self):
        """
        Test add entity.
        """
        params = {}
        params['service_id'] = 3
        params['entity_name'] = '京B123'

        response = self.the_client.call_open_api(
            uri='/trace/v3/entity/add',
            app_id="YOUR_APP_ID",
            body=urllib.urlencode(params),
            method='POST'
        )
        print response

    def test_update_entity(self):
        """
        Test update entity.
        """
        params = {}
        params['service_id'] = 3
        params['entity_name'] = '京B123'
        params['entity_desc'] = 'test_python_sdk'

        response = self.the_client.call_open_api(
            uri='/trace/v3/entity/update',
            app_id="YOUR_APP_ID",
            body=urllib.urlencode(params),
            method='POST'
        )
        print response

    def test_delete_entity(self):
        """
        Test delete entity.
        """
        params = {}
        params['service_id'] = 3
        params['entity_name'] = '京B123'

        response = self.the_client.call_open_api(
            uri='/trace/v3/entity/delete',
            app_id="YOUR_APP_ID",
            body=urllib.urlencode(params),
            method='POST'
        )
        print response

    def test_list_entity(self):
        """
        Test list entity.
        """
        params = {}
        params['service_id'] = 3

        response = self.the_client.call_open_api(
            uri='/trace/v3/entity/list',
            app_id="YOUR_APP_ID",
            params=params,
            method='GET'
        )
        print response

    def test_add_point(self):
        """
        Test add point.
        """
        params = {}
        params['service_id'] = 3
        params['entity_name'] = '京B123'
        params['latitude'] = 39.92
        params['longitude'] = 116.44
        params['loc_time'] = 1554951546
        params['coord_type_input'] = 'bd09ll'

        response = self.the_client.call_open_api(
            uri='/trace/v3/track/addpoint',
            app_id="YOUR_APP_ID",
            body=urllib.urlencode(params),
            method='POST'
        )
        print response

    def test_add_points(self):
        """
        Test add points.
        """
        params = {}
        params['service_id'] = 3
        params['point_list'] = '[{"entity_name":"京B123","loc_time":1525232703,"latitude":39.989715,' \
                               '"longitude":116.437039,"coord_type_input":"wgs84","speed":27.23,' \
                               '"direction":178,"height":173.3,"radius":32}]'

        response = self.the_client.call_open_api(
            uri='/trace/v3/track/addpoints',
            app_id="YOUR_APP_ID",
            body=urllib.urlencode(params),
            method='POST'
        )
        print response

    def test_keyword_search(self):
        """
        Test keyword search.
        """
        params = {}
        params['service_id'] = 3
        params['query'] = '京'

        response = self.the_client.call_open_api(
            uri='/trace/v3/entity/search',
            app_id="YOUR_APP_ID",
            params=params,
            method='GET'
        )
        print response

    def test_bound_search(self):
        """
        Test bound search.
        """
        params = {}
        params['service_id'] = 3
        params['bounds'] = "29.513115638907068,106.2934528944364;29.556202598213056,106.54430397948912"

        response = self.the_client.call_open_api(
            uri='/trace/v3/entity/boundsearch',
            app_id="YOUR_APP_ID",
            params=params,
            method='GET'
        )
        print response

    def test_polygon_search(self):
        """
        Test polygon search.
        """
        params = {}
        params['service_id'] = 3
        params['vertexes'] = "29.513115638907068,106.2934528944364;29.598346607316349,106.23347456267436;" \
                             "29.556202598213056,106.54430397948912"

        response = self.the_client.call_open_api(
            uri='/trace/v3/entity/polygonsearch',
            app_id="YOUR_APP_ID",
            params=params,
            method='GET'
        )
        print response

    def test_district_search(self):
        """
        Test district search.
        """
        params = {}
        params['service_id'] = 3
        params['keyword'] = "北京"

        response = self.the_client.call_open_api(
            uri='/trace/v3/entity/districtsearch',
            app_id="YOUR_APP_ID",
            params=params,
            method='GET'
        )
        print response

    def test_get_latest_point(self):
        """
        Test get latest point.
        """
        params = {}
        params['service_id'] = 3
        params['entity_name'] = "京A123"

        response = self.the_client.call_open_api(
            uri='/trace/v3/track/getlatestpoint',
            app_id="YOUR_APP_ID",
            params=params,
            method='GET'
        )
        print response

    def test_get_distance(self):
        """
        Test get distance.
        """
        params = {}
        params['service_id'] = 3
        params['entity_name'] = "京A123"
        params['start_time'] = 1554951545
        params['end_time'] = 1554951548

        response = self.the_client.call_open_api(
            uri='/trace/v3/track/getdistance',
            app_id="YOUR_APP_ID",
            params=params,
            method='GET'
        )
        print response

    def test_get_track(self):
        """
        Test get track.
        """
        params = {}
        params['service_id'] = 3
        params['entity_name'] = "京A123"
        params['start_time'] = 1554951545
        params['end_time'] = 1554951548

        response = self.the_client.call_open_api(
            uri='/trace/v3/track/gettrack',
            app_id="YOUR_APP_ID",
            params=params,
            method='GET'
        )
        print response

    def test_stay_point(self):
        """
        Test stay point.
        """
        params = {}
        params['service_id'] = 3
        params['entity_name'] = "京A123"
        params['start_time'] = 1554951545
        params['end_time'] = 1554951548

        response = self.the_client.call_open_api(
            uri='/trace/v3/analysis/staypoint',
            app_id="YOUR_APP_ID",
            params=params,
            method='GET'
        )
        print response

    def test_driving_behavior(self):
        """
        Test driving behavior.
        """
        params = {}
        params['service_id'] = 3
        params['entity_name'] = "京A123"
        params['start_time'] = 1554951545
        params['end_time'] = 1554951548

        response = self.the_client.call_open_api(
            uri='/trace/v3/analysis/drivingbehavior',
            app_id="YOUR_APP_ID",
            params=params,
            method='GET'
        )
        print response

    def test_create_circle_fence(self):
        """
        Test create circle fence.
        """
        params = {}
        params['service_id'] = 3
        params['fence_name'] = "fence1"
        params['monitored_person'] = "京A123"
        params['longitude'] = 116.437039
        params['latitude'] = 39.989715
        params['radius'] = 100
        params['coord_type'] = 'bd09ll'

        response = self.the_client.call_open_api(
            uri='/trace/v3/fence/createcirclefence',
            app_id="YOUR_APP_ID",
            body=urllib.urlencode(params),
            method='POST'
        )
        print response

    def test_create_polygon_fence(self):
        """
        Test create polygon fence.
        """
        params = {}
        params['service_id'] = 3
        params['fence_name'] = "fence2"
        params['monitored_person'] = "京A123"
        params['vertexes'] = "39.989715,116.437039;39.989715,116.437039;39.989715,116.437039"
        params['coord_type'] = 'bd09ll'

        response = self.the_client.call_open_api(
            uri='/trace/v3/fence/createpolygonfence',
            app_id="YOUR_APP_ID",
            body=urllib.urlencode(params),
            method='POST'
        )
        print response

    def test_create_polyline_fence(self):
        """
        Test create polyline fence.
        """
        params = {}
        params['service_id'] = 3
        params['fence_name'] = "fence3"
        params['monitored_person'] = "京A123"
        params['vertexes'] = "39.989715,116.437039;39.989715,116.437039;39.989715,116.437039"
        params['offset'] = 100
        params['coord_type'] = 'bd09ll'

        response = self.the_client.call_open_api(
            uri='/trace/v3/fence/createpolylinefence',
            app_id="YOUR_APP_ID",
            body=urllib.urlencode(params),
            method='POST'
        )
        print response

    def test_create_district_fence(self):
        """
        Test create district fence.
        """
        params = {}
        params['service_id'] = 3
        params['fence_name'] = "fence4"
        params['monitored_person'] = "京A123"
        params['keyword'] = "北京"

        response = self.the_client.call_open_api(
            uri='/trace/v3/fence/createdistrictfence',
            app_id="YOUR_APP_ID",
            body=urllib.urlencode(params),
            method='POST'
        )
        print response

    def test_update_circle_fence(self):
        """
        Test create district fence.
        """
        params = {}
        params['service_id'] = 3
        params['fence_name'] = "fence1"
        params['fence_id'] = 1
        params['monitored_person'] = "京A123"
        params['longitude'] = 116.437039
        params['latitude'] = 39.989715
        params['radius'] = 100
        params['coord_type'] = 'bd09ll'

        response = self.the_client.call_open_api(
            uri='/trace/v3/fence/updatecirclefence',
            app_id="YOUR_APP_ID",
            body=urllib.urlencode(params),
            method='POST'
        )
        print response

    def test_update_polygon_fence(self):
        """
        Test update polygon fence.
        """
        params = {}
        params['service_id'] = 3
        params['fence_name'] = "fence2"
        params['fence_id'] = 2
        params['monitored_person'] = "京A123"
        params['vertexes'] = "39.989715,116.437039;39.989715,116.437039;39.989715,116.437039"
        params['coord_type'] = 'bd09ll'

        response = self.the_client.call_open_api(
            uri='/trace/v3/fence/updatepolygonfence',
            app_id="YOUR_APP_ID",
            body=urllib.urlencode(params),
            method='POST'
        )
        print response

    def test_update_polyline_fence(self):
        """
        Test update polyline fence.
        """
        params = {}
        params['service_id'] = 3
        params['fence_name'] = "fence3"
        params['fence_id'] = 3
        params['monitored_person'] = "京A123"
        params['vertexes'] = "39.989715,116.437039;39.989715,116.437039;39.989715,116.437039"
        params['offset'] = 100
        params['coord_type'] = 'bd09ll'

        response = self.the_client.call_open_api(
            uri='/trace/v3/fence/updatepolylinefence',
            app_id="YOUR_APP_ID",
            body=urllib.urlencode(params),
            method='POST'
        )
        print response

    def test_update_district_fence(self):
        """
        Test update district fence.
        """
        params = {}
        params['service_id'] = 3
        params['fence_name'] = "fence4"
        params['fence_id'] = 4
        params['monitored_person'] = "京A123"
        params['keyword'] = "北京"

        response = self.the_client.call_open_api(
            uri='/trace/v3/fence/updatedistrictfence',
            app_id="YOUR_APP_ID",
            body=urllib.urlencode(params),
            method='POST'
        )
        print response

    def test_list_fence(self):
        """
        Test list fence.
        """
        params = {}
        params['service_id'] = 3
        params['monitored_person'] = "京A123"

        response = self.the_client.call_open_api(
            uri='/trace/v3/fence/list',
            app_id="YOUR_APP_ID",
            params=params,
            method='GET'
        )
        print response

    def test_delete_fence(self):
        """
        Test delete fence.
        """
        params = {}
        params['service_id'] = 3
        params['monitored_person'] = "京A123"

        response = self.the_client.call_open_api(
            uri='/trace/v3/fence/delete',
            app_id="YOUR_APP_ID",
            body=urllib.urlencode(params),
            method='POST'
        )
        print response

    def test_add_monitored_entity(self):
        """
        Test add monitored entity.
        """
        params = {}
        params['service_id'] = 3
        params['fence_id'] = 1
        params['monitored_person'] = "京A123"

        response = self.the_client.call_open_api(
            uri='/trace/v3/fence/addmonitoredperson',
            app_id="YOUR_APP_ID",
            body=urllib.urlencode(params),
            method='POST'
        )
        print response

    def test_delete_monitored_entity(self):
        """
        Test delete monitored entity.
        """
        params = {}
        params['service_id'] = 3
        params['fence_id'] = 1
        params['monitored_person'] = "京A123"

        response = self.the_client.call_open_api(
            uri='/trace/v3/fence/deletemonitoredperson',
            app_id="YOUR_APP_ID",
            body=urllib.urlencode(params),
            method='POST'
        )
        print response

    def test_list_monitored_entity(self):
        """
        Test list monitored entity.
        """
        params = {}
        params['service_id'] = 3
        params['fence_id'] = 1
        params['page_index'] = 1
        params['page_size'] = 10

        response = self.the_client.call_open_api(
            uri='/trace/v3/fence/listmonitoredperson',
            app_id="YOUR_APP_ID",
            params=params,
            method='GET'
        )
        print response

    def test_query_status(self):
        """
        Test query status.
        """
        params = {}
        params['service_id'] = 3
        params['monitored_person'] = "京A123"

        response = self.the_client.call_open_api(
            uri='/trace/v3/fence/querystatus',
            app_id="YOUR_APP_ID",
            params=params,
            method='GET'
        )
        print response

    def test_query_status_by_location(self):
        """
        Test query status by location.
        """
        params = {}
        params['service_id'] = 3
        params['monitored_person'] = "京A123"
        params['latitude'] = 39.989715
        params['longitude'] = 116.437039
        params['coord_type'] = "bd09ll"

        response = self.the_client.call_open_api(
            uri='/trace/v3/fence/querystatusbylocation',
            app_id="YOUR_APP_ID",
            params=params,
            method='GET'
        )
        print response

    def test_history_alarm(self):
        """
        Test history alarm.
        """
        params = {}
        params['service_id'] = 3
        params['monitored_person'] = "京A123"

        response = self.the_client.call_open_api(
            uri='/trace/v3/fence/historyalarm',
            app_id="YOUR_APP_ID",
            params=params,
            method='GET'
        )
        print response

    def test_batch_history_alarm(self):
        """
        Test batch history alarm.
        """
        params = {}
        params['service_id'] = 3
        params['start_time'] = 1553593410
        params['end_time'] = 1553593410

        response = self.the_client.call_open_api(
            uri='/trace/v3/fence/batchhistoryalarm',
            app_id="YOUR_APP_ID",
            params=params,
            method='GET'
        )
        print response

    def test_set_callback_url(self):
        """
        Test set callback url.
        """
        params = {}
        params['service_id'] = 3
        params['url'] = "http://10.64.79.132:8011/callback"

        response = self.the_client.call_open_api(
            uri='/trace/v3/fence/seturl',
            app_id="YOUR_APP_ID",
            body=urllib.urlencode(params),
            method='POST'
        )
        print response

    def test_cancel_callback_url(self):
        """
        Test cancel callback url.
        """
        params = {}
        params['service_id'] = 3

        response = self.the_client.call_open_api(
            uri='/trace/v3/fence/cancelurl',
            app_id="YOUR_APP_ID",
            body=urllib.urlencode(params),
            method='POST'
        )
        print response

    def test_query_callback_url(self):
        """
        Test query callback url.
        """
        params = {}
        params['service_id'] = 3

        response = self.the_client.call_open_api(
            uri='/trace/v3/fence/queryurl',
            app_id="YOUR_APP_ID",
            params=params,
            method='GET'
        )
        print response

    def test_create_job(self):
        """
        Test create job.
        """
        params = {}
        params['service_id'] = 3
        params['start_time'] = 1554943015
        params['end_time'] = 1554943115

        response = self.the_client.call_open_api(
            uri='/trace/v3/export/createjob',
            app_id="YOUR_APP_ID",
            body=urllib.urlencode(params),
            method='POST'
        )
        print response

    def test_get_job(self):
        """
        Test get job.
        """
        params = {}
        params['service_id'] = 3

        response = self.the_client.call_open_api(
            uri='/trace/v3/export/getjob',
            app_id="YOUR_APP_ID",
            params=params,
            method='GET'
        )
        print response

    def test_delete_job(self):
        """
        Test delete job.
        """
        params = {}
        params['service_id'] = 3
        params['job_id'] = 1

        response = self.the_client.call_open_api(
            uri='/trace/v3/export/deletejob',
            app_id="YOUR_APP_ID",
            body=urllib.urlencode(params),
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
