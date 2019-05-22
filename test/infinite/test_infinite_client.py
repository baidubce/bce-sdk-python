# Copyright 2014 Baidu, Inc.
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
Unit tests for infinite client.
"""

import unittest
import mock
import os
import sys
import json

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.infinite import infinite_client as infinite

class MockHttpResponse(object):
    """
    Mock HttpResponse
    """

    def __init__(self, status, content=None, header_list=None):
        self.status = status
        self.content = content
        self.header_list = header_list

    def read(self):
        """
        mock HttpResponse.read()

        :return: self.content
        """
        return self.content

    def getheaders(self):
        """
        mock HttpResponse.getheaders()

        :return: self.header_list
        """
        return self.header_list

    def close(self):
        """
        mock HttpResponse.close()
        """
        return


class TestInfiniteClient(unittest.TestCase):
    """
    Test class for infinite sdk client
    """

    def setUp(self):
        HOST = 'host'
        AK = 'ak'
        SK = 'sk'
        config = BceClientConfiguration(
            credentials=BceCredentials(AK, SK),
            endpoint=HOST
        )
        self.infinite_client = infinite.InfiniteClient(config)

    @mock.patch('baidubce.http.bce_http_client._send_http_request')
    def test_predict(self, send_http_request):
        """
        test case for predict
        """
        res_data = {}
        res_data['categories'] = [0.1, 0.3, 0.5, 0.1]
        mock_http_response = MockHttpResponse(
            200,
            content=json.dumps(res_data),
            header_list=[
                ('x-bce-request-id', 'predict_x_bce_req_id'),
                ('content-type', 'application/json;charset=UTF-8')
            ])
        send_http_request.return_value = mock_http_response
        
        file_name = os.path.normpath(os.path.dirname(__file__)) + '/what.jpg'
        with open(file_name, 'rb') as f:
            payload = f.read()
        res = self.infinite_client.predict(
            endpoint_name='ep1',
            body=payload,
            content_type='application/x-image')
        data = json.loads(res.Body)
        self.assertEqual(data['categories'], res_data['categories'])

    @mock.patch('baidubce.http.bce_http_client._send_http_request')
    def test_debug(self, send_http_request):
        """
        test case for debug
        """
        res_data = {}
        res_data['categories'] = [0.1, 0.3, 0.5, 0.1]
        res_data['debug_str'] = 'debug info'
        mock_http_response = MockHttpResponse(
            200,
            content=json.dumps(res_data),
            header_list=[
                ('x-bce-request-id', 'predict_x_bce_req_id'),
                ('content-type', 'application/json;charset=UTF-8')
            ])
        send_http_request.return_value = mock_http_response

        file_name = os.path.normpath(os.path.dirname(__file__)) + '/what.jpg'
        with open(file_name, 'rb') as f:
            payload = f.read()
        res = self.infinite_client.debug(
            endpoint_name='ep1',
            variant_name="v1",
            body=payload,
            content_type='application/x-image')
        data = json.loads(res.Body)
        self.assertEqual(data['categories'], res_data['categories'])
        self.assertEqual(data['debug_str'], res_data['debug_str'])

    @mock.patch('baidubce.http.bce_http_client._send_http_request')
    def test_get_endpoint_list(self, send_http_request):
        """
        test case for get_endpoint_list
        """
        res_data = {}
        ep_list = ["ep1_name", "ep2_name", "ep3_name", "ep4_name"]
        res_data['endpoint_list'] = ep_list
        mock_http_response = MockHttpResponse(
            200,
            content=json.dumps(res_data),
            header_list=[
                ('x-bce-request-id', 'predict_x_bce_req_id'),
                ('content-type', 'application/json;charset=UTF-8')
            ])

        send_http_request.return_value = mock_http_response
        res = self.infinite_client.get_endpoint_list()
        data = json.loads(res.Body)
        self.assertEqual(data['endpoint_list'], ep_list)

    @mock.patch('baidubce.http.bce_http_client._send_http_request')
    def test_get_endpoint_info(self, send_http_request):
        """
        test case for get_endpoint_info
        """
        res_data = {}
        res_data['endpoint_uuid'] = 'ep1_uuid'
        res_data['endpoint_name'] = 'ep1'
        res_data['endpoint_version'] = 1
        var1 = {}
        var1['variant_uuid'] = 'v1_uuid'
        var1['variant_name'] = 'v1'
        var1['vip'] = '127.0.0.1'
        var1['vport'] = '8010'
        var1['service_name'] = 'ImageClassifyService'
        var1['variant_weight'] = 1.0
        var1['normalized_variant_weight'] = 1.0
        res_data['variant_configs'] = []
        res_data['variant_configs'].append(var1)
        mock_http_response = MockHttpResponse(
            200,
            content=json.dumps(res_data),
            header_list=[
                ('x-bce-request-id', 'predict_x_bce_req_id'),
                ('content-type', 'application/json;charset=UTF-8')
            ])

        send_http_request.return_value = mock_http_response
        res = self.infinite_client.get_endpoint_info(endpoint_name='ep1')
        data = json.loads(res.Body)
        self.assertEqual(data['endpoint_name'], 'ep1')
        self.assertEqual(data['endpoint_uuid'], 'ep1_uuid')

if __name__ == '__main__':
    unittest.main()
