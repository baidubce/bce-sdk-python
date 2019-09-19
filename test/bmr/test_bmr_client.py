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
Unit tests for bmr client.
"""

import unittest
import os
import sys
import json

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.bmr import bmr_client as bmr

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY3:
    import unittest.mock as mock
else:
    import mock as mock


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


class TestBmrClient(unittest.TestCase):
    """
    Test class for bmr sdk client
    """

    def setUp(self):
        HOST = 'bmr.bce-api.baidu.com'
        AK = 'ak'
        SK = 'sk'
        config = BceClientConfiguration(
            credentials=BceCredentials(AK, SK),
            endpoint=HOST
        )
        self.bmr_client = bmr.BmrClient(config)

    @mock.patch('baidubce.http.bce_http_client._send_http_request')
    def test_create_cluster(self, send_http_request):
        """
        test case for create_cluster
        """
        mock_http_response = MockHttpResponse(
            201,
            content=json.dumps({'clusterId': 'c003'}),
            header_list=[
                ('x-bce-request-id', 'create01'),
                ('content-type', 'application/json;charset=UTF-8')
            ])
        send_http_request.return_value = mock_http_response
        res = self.bmr_client.create_cluster(
            'hadoop',
            '0.1.0',
            [
                bmr.instance_group(
                    'Master',
                    'g.small',
                    1,
                    'ig-master'),
                bmr.instance_group(
                    'Core',
                    'g.small',
                    2,
                    'ig-core')
            ],
            auto_terminate=True,
            log_uri='bos://path/to/log',
            name='cluster03')
        self.assertEqual(res.cluster_id, 'c003')

    @mock.patch('baidubce.http.bce_http_client._send_http_request')
    def test_scale_cluster(self, send_http_request):
        """
        test case for scale cluster
        """

    @mock.patch('baidubce.http.bce_http_client._send_http_request')
    def test_list_cluster(self, send_http_request):
        """
        test case for list_cluster
        """
        res_body = {
            'clusters': [
                {
                    'id': 'c001',
                    'name': 'cluster01',
                    'imageType': 'hadoop',
                    'imageVersion': '0.1.0',
                    'logUri': 'bos://path/to/log',
                    'autoTerminate': False,
                    'applications': [
                        {
                            'name': 'hive',
                            'version': '0.13.0'
                        }
                    ],
                    'status': {
                        'code': None,
                        'createDateTime': '2015-08-12T00:00:00Z',
                        'endDateTime': None,
                        'message': None,
                        'readyDateTime': None,
                        'state': 'Starting'
                    }
                },
                {
                    'id': 'c002',
                    'name': 'cluster02',
                    'imageType': 'spark',
                    'imageVersion': '0.1.0',
                    'logUri': 'bos://path/to/log',
                    'autoTerminate': False,
                    'applications': [],
                    'status': {
                        'code': None,
                        'createDateTime': '2015-08-12T00:00:00Z',
                        'endDateTime': None,
                        'message': None,
                        'readyDateTime': None,
                        'state': 'Starting'
                    }
                }
            ],
            'isTruncated': False,
            'marker': '003'
        }
        mock_http_response = MockHttpResponse(
            200,
            content=json.dumps(res_body),
            header_list=[
                ('x-bce-request-id', 'list01'),
                ('content-type', 'application/json;charset=UTF-8')
            ]
        )
        send_http_request.return_value = mock_http_response
        res = self.bmr_client.list_clusters(max_keys=2, marker='001')
        self.assertEqual(res.clusters[1].name, 'cluster02')

    @mock.patch('baidubce.http.bce_http_client._send_http_request')
    def test_get_cluster(self, send_http_request):
        """
        test case for get_cluster
        """
        res_body = {
            'id': 'c002',
            'name': 'cluster02',
            'imageType': 'spark',
            'imageVersion': '0.1.0',
            'logUri': 'bos://path/to/log',
            'autoTerminate': False,
            'applications': [],
            'status': {
                'code': None,
                'createDateTime': '2015-08-12T00:00:00Z',
                'endDateTime': None,
                'message': None,
                'readyDateTime': None,
                'state': 'Starting'
            }
        }
        mock_http_response = MockHttpResponse(
            200,
            content=json.dumps(res_body),
            header_list=[
                ('x-bce-request-id', 'describe01'),
                ('content-type', 'application/json;charset=UTF-8')
            ]
        )
        send_http_request.return_value = mock_http_response
        res = self.bmr_client.get_cluster('c002')
        self.assertEqual(res.name, 'cluster02')

    @mock.patch('baidubce.http.bce_http_client._send_http_request')
    def test_add_steps(self, send_http_request):
        """
        test case for add_steps 
        """
        mock_http_response = MockHttpResponse(
            201,
            content=json.dumps({'stepIds': ['j001', 'j002']}),
            header_list=[
                ('x-bce-request-id', 'create02'),
                ('content-type', 'application/json;charset=UTF-8')
            ]
        )
        additional_files = [bmr.additional_file("bos://path/to/remote1", "local1")]
        send_http_request.return_value = mock_http_response
        res = self.bmr_client.add_steps(
            'c001',
            [
                {
                    'name': 'job01',
                    'id': 'j001',
                    'type': 'Java',
                    'actionOnFailure': 'Continue',
                    'properties': bmr.java_step_properties(
                        'bos://path/to/jar',
                        'WordCount',
                        arguments='bos://path/to/input, bos://path/to/output'
                    ),
                    'additional_files': additional_files
                },
                {
                    'name': 'job02',
                    'id': 'j002',
                    'type': 'Hive',
                    'actionOnFailure': 'Continue',
                    'properties': bmr.hive_step_properties(
                        'bos://path/to/script',
                        input='bos://path/to/input',
                        output='bos://path/to/output',
                        arguments='arg1 arg2',
                    ),
                    'additional_files': additional_files
                }
            ]
        )
        self.assertEqual(res.step_ids, ['j001', 'j002'])

    @mock.patch('baidubce.http.bce_http_client._send_http_request')
    def test_list_steps(self, send_http_request):
        """
        test case for list_steps 
        """
        res_body = {
            'steps': [
                {
                    'name': 'job01',
                    'id': 'j001',
                    'type': 'Java',
                    'actionOnFailure': 'Continue',
                    'properties': bmr.java_step_properties(
                        'bos://path/to/jar',
                        'WordCount',
                        'bos://path/to/input, bos://path/to/output'
                    ),
                    'status': {
                        'code': None,
                        'createDateTime': '2015-08-12T00:00:00Z',
                        'endDateTime': '2015-08-12T00:01:00Z',
                        'startDateTime': '2015-08-12T00:00:05Z',
                        'state': 'Completed',
                        'message': None
                    }
                },
                {
                    'name': 'job02',
                    'id': 'j002',
                    'type': 'Streaming',
                    'actionOnFailure': 'Continue',
                    'properties': bmr.streaming_step_properties(
                        'bos://path/to/input',
                        'bos://path/to/output',
                        'cat',
                        arguments='arg1 arg2'
                    ),
                    'status': {
                        'code': None,
                        'createDateTime': '2015-08-12T00:00:00Z',
                        'endDateTime': '2015-08-12T00:01:00Z',
                        'startDateTime': '2015-08-12T00:00:05Z',
                        'state': 'Completed',
                        'message': None
                    }
                }
            ],
            'isTruncated': False,
            'marker': '003'
        }
        mock_http_response = MockHttpResponse(
            200,
            content=json.dumps(res_body),
            header_list=[
                ('x-bce-request-id', 'list02'),
                ('content-type', 'application/json;charset=UTF-8')
            ]
        )
        send_http_request.return_value = mock_http_response
        res = self.bmr_client.list_steps('c001', max_keys=2, marker='j001')
        self.assertEqual(res.steps[1].properties.reducer, '')

    @mock.patch('baidubce.http.bce_http_client._send_http_request')
    def test_get_step(self, send_http_request):
        """
        test case for get_steps 
        """
        res_body = {
            'name': 'job01',
            'id': 'j001',
            'type': 'Java',
            'actionOnFailure': 'Continue',
            'properties': bmr.java_step_properties(
                'bos://path/to/jar',
                'WordCount',
                'bos://path/to/input, bos://path/to/output'
            ),
            'status': {
                'code': None,
                'createDateTime': '2015-08-12T00:00:00Z',
                'endDateTime': '2015-08-12T00:01:00Z',
                'startDateTime': '2015-08-12T00:00:05Z',
                'state': 'Completed',
                'message': None
            }
        }
        mock_http_response = MockHttpResponse(
            200,
            content=json.dumps(res_body),
            header_list=[
                ('x-bce-request-id', 'describe02'),
                ('content-type', 'application/json;charset=UTF-8')
            ]
        )
        send_http_request.return_value = mock_http_response
        res = self.bmr_client.get_step('c001', 'j001')
        self.assertEqual(res.status.state, 'Completed')

    @mock.patch('baidubce.http.bce_http_client._send_http_request')
    def test_list_instances(self, send_http_request):
        """
        test case for list_instances
        """
        res_body = {
            'instances': [
                {
                    'id': '001',
                    'privateIpAddress': '192.168.12.55',
                    'publicIpAddress': '180.76.145.145',
                },
                {
                    'id': '002',
                    'privateIpAddress': '192.168.160.42',
                    'publicIpAddress': '180.76.236.132'
                }
            ]
        }
        mock_http_response = MockHttpResponse(
            200,
            content=json.dumps(res_body),
            header_list=[
                ('x-bce-request-id', 'list02'),
                ('content-type', 'application/json;charset=UTF-8')
            ]
        )
        send_http_request.return_value = mock_http_response
        res = self.bmr_client.list_instances('c001', 'i001')
        self.assertEqual(res.instances[1].id, '002')

    @mock.patch('baidubce.http.bce_http_client._send_http_request')
    def test_list_instance_groups(self, send_http_request):
        """
        test case for list instance groups
        """
        res_body = {
            'instanceGroups': [
                {
                    'id': '001',
                    'instanceType': 'batch.g.small',
                    'name': 'ng431212c-master',
                    'requestedInstanceCount': 1,
                    'type': 'MASTER'
                },
                {
                    'id': '002',
                    'instanceType': 'batch.g.small',
                    'name': 'ng207f29a-core',
                    'requestedInstanceCount': 2,
                    'type': 'CORE'
                }
            ]
        }
        mock_http_response = MockHttpResponse(
            200,
            content=json.dumps(res_body),
            header_list=[
                ('x-bce-request-id', 'list03'),
                ('content-type', 'application/json;charset=UTF-8')
            ]
        )
        send_http_request.return_value = mock_http_response
        res = self.bmr_client.list_instance_groups('c001')
        self.assertEqual(res.instance_groups[1].id, '002')

if __name__ == '__main__':
    unittest.main()
