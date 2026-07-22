# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
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
Unit tests for eo client.
"""

import imp
import sys
import unittest

import eo_test_config
from baidubce import compat
from baidubce.exception import BceServerError
from baidubce.services.eo.eo_client import EoClient

imp.reload(sys)
if compat.PY2:
    sys.setdefaultencoding('utf8')


class TestEoClient(unittest.TestCase):
    """
    Test class for eo sdk client
    """
    def setUp(self):
        self.eo_client = EoClient(eo_test_config.config)

    def test_purge(self):
        """
        test_purge
        """
        error = None
        try:
            tasks = []
            tasks.append({'url': 'http://1.test-sdk-eo.baidu.com/test1.png', 'type': 'file'})
            tasks.append({'url': 'http://1.test-sdk-eo.baidu.com/', 'type': 'directory'})
            response = self.eo_client.purge(tasks, 'test-sdk-eo.baidu.com')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_list_purge_tasks(self):
        """
        test_list_purge_tasks
        """
        error = None
        try:
            response = self.eo_client.list_purge_tasks(
                                site = 'test-sdk-eo.baidu.com',
                                type = 'file',
                                startTime = '2026-07-21T05:10:10Z',
                                endTime = '2026-07-21T07:10:10Z')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_list_purge_tasks_by_task_id(self):
        """
        test_list_purge_tasks_by_task_id
        """
        error = None
        try:
            response = self.eo_client.list_purge_tasks(
                                site = 'test-sdk-eo.baidu.com',
                                id = 'task_id')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_prefetch(self):
        """
        test_prefetch
        """
        error = None
        try:
            tasks = []
            tasks.append({'url': 'http://1.test-sdk-eo.baidu.com/test1.png'})
            tasks.append({'url': 'http://1.test-sdk-eo.baidu.com/test2.png'})
            response = self.eo_client.prefetch(tasks, 'test-sdk-eo.baidu.com')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_list_prefetch_tasks(self):
        """
        test_list_prefetch_tasks
        """
        error = None
        try:
            response = self.eo_client.list_prefetch_tasks(
                                site = 'test-sdk-eo.baidu.com',
                                startTime = '2026-07-21T05:26:55Z',
                                endTime = '2026-07-21T07:26:55Z')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_list_prefetch_tasks_by_task_id(self):
        """
        test_list_prefetch_tasks_by_task_id
        """
        error = None
        try:
            response = self.eo_client.list_prefetch_tasks(
                                site = 'test-sdk-eo.baidu.com',
                                id = 'task_id')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_domain_log(self):
        """
        test_get_domain_log
        """
        error = None
        try:
            response = self.eo_client.get_domain_log(
                                site = 'test-sdk-eo.baidu.com',
                                startTime = '2026-07-21T05:00:00Z',
                                endTime = '2026-07-21T07:00:00Z',
                                domainList = ['1.test-sdk-eo.baidu.com'],
                                pageNo = 1,
                                pageSize = 20)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_stat_bps_peak(self):
        """
        query peak of sum_bps/upstream_bps/download_bps by site
        """
        error = None
        try:
            response = self.eo_client.stat(
                                metrics = ['sum_bps', 'upstream_bps', 'download_bps'],
                                startTime = '2026-07-21T00:00:00Z',
                                endTime = '2026-07-21T09:06:29Z',
                                showType = 'peak',
                                filter = [{
                                    'key': 'site',
                                    'operation': 'equal',
                                    'value': ['test-sdk-eo.baidu.com']
                                }])
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_stat_sum_bps_time(self):
        """
        query time series of sum_bps by site
        """
        error = None
        try:
            response = self.eo_client.stat(
                                metrics = ['sum_bps'],
                                startTime = '2026-07-21T00:00:00Z',
                                endTime = '2026-07-21T09:06:29Z',
                                showType = 'time',
                                filter = [{
                                    'key': 'site',
                                    'operation': 'equal',
                                    'value': ['test-sdk-eo.baidu.com']
                                }])
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_stat_flow_sum(self):
        """
        query sum of sum_flow/upstream_flow/download_flow by site
        """
        error = None
        try:
            response = self.eo_client.stat(
                                metrics = ['sum_flow', 'upstream_flow', 'download_flow'],
                                startTime = '2026-07-21T00:00:00Z',
                                endTime = '2026-07-21T09:06:29Z',
                                showType = 'sum',
                                filter = [{
                                    'key': 'site',
                                    'operation': 'equal',
                                    'value': ['test-sdk-eo.baidu.com']
                                }])
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_stat_sum_flow_time(self):
        """
        query time series of sum_flow by site
        """
        error = None
        try:
            response = self.eo_client.stat(
                                metrics = ['sum_flow'],
                                startTime = '2026-07-21T00:00:00Z',
                                endTime = '2026-07-21T09:06:29Z',
                                showType = 'time',
                                filter = [{
                                    'key': 'site',
                                    'operation': 'equal',
                                    'value': ['test-sdk-eo.baidu.com']
                                }])
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_stat_pv_sum(self):
        """
        query sum of pv by site
        """
        error = None
        try:
            response = self.eo_client.stat(
                                metrics = ['pv'],
                                startTime = '2026-07-21T00:00:00Z',
                                endTime = '2026-07-21T09:06:29Z',
                                showType = 'sum',
                                filter = [{
                                    'key': 'site',
                                    'operation': 'equal',
                                    'value': ['test-sdk-eo.baidu.com']
                                }])
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_stat_pv_peak(self):
        """
        query peak of pv by site
        """
        error = None
        try:
            response = self.eo_client.stat(
                                metrics = ['pv'],
                                startTime = '2026-07-21T00:00:00Z',
                                endTime = '2026-07-21T09:06:29Z',
                                showType = 'peak',
                                filter = [{
                                    'key': 'site',
                                    'operation': 'equal',
                                    'value': ['test-sdk-eo.baidu.com']
                                }])
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_stat_pv_time(self):
        """
        query time series of pv by site
        """
        error = None
        try:
            response = self.eo_client.stat(
                                metrics = ['pv'],
                                startTime = '2026-07-21T00:00:00Z',
                                endTime = '2026-07-21T09:06:29Z',
                                showType = 'time',
                                filter = [{
                                    'key': 'site',
                                    'operation': 'equal',
                                    'value': ['test-sdk-eo.baidu.com']
                                }])
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_stat_code_sum(self):
        """
        query sum of status code (pv grouped by code) by site
        """
        error = None
        try:
            response = self.eo_client.stat(
                                metrics = ['pv'],
                                startTime = '2026-07-21T00:00:00Z',
                                endTime = '2026-07-21T09:06:29Z',
                                showType = 'sum',
                                group = ['code'],
                                filter = [{
                                    'key': 'site',
                                    'operation': 'equal',
                                    'value': ['test-sdk-eo.baidu.com']
                                }])
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_stat_code_time(self):
        """
        query time series of status code (pv grouped by code) by site
        """
        error = None
        try:
            response = self.eo_client.stat(
                                metrics = ['pv'],
                                startTime = '2026-07-21T00:00:00Z',
                                endTime = '2026-07-21T09:06:29Z',
                                showType = 'time',
                                group = ['code'],
                                filter = [{
                                    'key': 'site',
                                    'operation': 'equal',
                                    'value': ['test-sdk-eo.baidu.com']
                                }])
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_stat_host_top(self):
        """
        query top pv grouped by host by site
        """
        error = None
        try:
            response = self.eo_client.stat(
                                metrics = ['pv'],
                                startTime='2026-07-21T00:00:00Z',
                                endTime='2026-07-21T09:06:29Z',
                                showType = 'top',
                                group = ['host'],
                                filter = [{
                                    'key': 'site',
                                    'operation': 'equal',
                                    'value': ['test-sdk-eo.baidu.com']
                                }],
                                limit = {'pageSize': 100})
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_site_config_cacheTtl_default(self):
        """
        follow origin - default cache policy
        """
        error = None
        try:
            response = self.eo_client.set_site_config(
                                site = 'test-sdk-eo.baidu.com',
                                cacheTtl = [])
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_site_config_cacheTtl_follow_origin_no_cache(self):
        """
        follow origin - no cache
        """
        error = None
        try:
            response = self.eo_client.set_site_config(
                                site = 'test-sdk-eo.baidu.com',
                                cacheTtl = [{
                                    'value': '/',
                                    'weight': 100,
                                    'override_origin': False,
                                    'ttl': 0,
                                    'type': 'path'
                                }])
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_site_config(self):
        """
        test_get_site_config
        """
        error = None
        try:
            response = self.eo_client.get_site_config(site = 'test-sdk-eo.baidu.com')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_site_config_items(self):
        """
        test_get_site_config_items
        """
        error = None
        try:
            result = self.eo_client.get_site_config_items(
                                site = 'test-sdk-eo.baidu.com',
                                keys = ['cacheTtl','cacheKey'])
            print(result)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_site_cache_key_keep_all(self):
        """
        keep all query string
        """
        error = None
        try:
            response = self.eo_client.set_site_cache_key(
                                site = 'test-sdk-eo.baidu.com',
                                cacheKey = {'query': True})
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_site_cache_key_ignore_all(self):
        """
        ignore all query string
        """
        error = None
        try:
            response = self.eo_client.set_site_cache_key(
                                site = 'test-sdk-eo.baidu.com',
                                cacheKey = {'query': False, 'include_args': []})
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_site_cache_key_include_args(self):
        """
        keep the specified query args
        """
        error = None
        try:
            response = self.eo_client.set_site_cache_key(
                                site = 'test-sdk-eo.baidu.com',
                                cacheKey = {'query': False, 'include_args': ['test1']})
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_site_cache_key_exclude_args(self):
        """
        ignore the specified query args
        """
        error = None
        try:
            response = self.eo_client.set_site_cache_key(
                                site = 'test-sdk-eo.baidu.com',
                                cacheKey = {'query': False, 'exclude_args': ['test1', 'test2']})
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_site_offline_mode_on(self):
        """
        enable offline mode
        """
        error = None
        try:
            response = self.eo_client.set_site_offline_mode(
                                site = 'test-sdk-eo.baidu.com',
                                offlineMode = 'ON')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_site_https_redirect_302(self):
        """
        enable force https redirect with 302
        """
        error = None
        try:
            response = self.eo_client.set_site_https_redirect(
                                site = 'test-sdk-eo.baidu.com',
                                httpToHttpsEnabled = 'ON',
                                httpToHttpsCode = '302')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_site_https_redirect_301(self):
        """
        enable force https redirect with 301
        """
        error = None
        try:
            response = self.eo_client.set_site_https_redirect(
                                site = 'test-sdk-eo.baidu.com',
                                httpToHttpsEnabled = 'ON',
                                httpToHttpsCode = '301')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_site_https_redirect_off(self):
        """
        disable force https redirect
        """
        error = None
        try:
            response = self.eo_client.set_site_https_redirect(
                                site = 'test-sdk-eo.baidu.com',
                                httpToHttpsEnabled = 'OFF')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_site_hsts_off(self):
        """
        disable hsts
        """
        error = None
        try:
            response = self.eo_client.set_site_hsts(
                                site = 'test-sdk-eo.baidu.com',
                                hsts = {'maxAge': -1, 'includeSubDomains': False, 'preload': False})
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_site_hsts_on(self):
        """
        enable hsts
        """
        error = None
        try:
            response = self.eo_client.set_site_hsts(
                                site = 'test-sdk-eo.baidu.com',
                                hsts = {'includeSubDomains': True, 'preload': False, 'maxAge': 60})
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_site_client_max_body_size(self):
        """
        set the max upload body size config
        """
        error = None
        try:
            response = self.eo_client.set_site_client_max_body_size(
                                site = 'test-sdk-eo.baidu.com',
                                clientMaxBodySize = '500m')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_site_compress_on(self):
        """
        enable page compress
        """
        error = None
        try:
            response = self.eo_client.set_site_compress(
                                site = 'test-sdk-eo.baidu.com',
                                compress = 'ON',
                                compressMethodArray = ['gzip', 'br'])
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_site_compress_off(self):
        """
        disable page compress
        """
        error = None
        try:
            response = self.eo_client.set_site_compress(
                                site = 'test-sdk-eo.baidu.com',
                                compress = 'OFF',
                                compressMethodArray = [])
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_site_isa_on(self):
        """
        enable intelligent acceleration
        """
        error = None
        try:
            response = self.eo_client.set_site_isa(
                                site = 'test-sdk-eo.baidu.com',
                                isa = 'ON')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_site_isa_off(self):
        """
        disable intelligent acceleration
        """
        error = None
        try:
            response = self.eo_client.set_site_isa(
                                site = 'test-sdk-eo.baidu.com',
                                isa = 'OFF')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_site_http_header_set(self):
        """
        set http header
        """
        error = None
        try:
            response = self.eo_client.set_site_http_header(
                                site = 'test-sdk-eo.baidu.com',
                                httpHeader = [
                                    {'type': 'response', 'header': 'Cache-Control', 'value': 'ceshi', 'action': 'add'},
                                    {'action': 'add', 'type': 'origin', 'header': 'Expires', 'value': 'test'}
                                ])
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_site_http_header_remove(self):
        """
        remove http header
        """
        error = None
        try:
            response = self.eo_client.set_site_http_header(
                                site = 'test-sdk-eo.baidu.com',
                                httpHeader = [
                                    {'type': 'response', 'value': '', 'action': 'remove', 'header': 'Expires'},
                                    {'value': '', 'type': 'origin', 'action': 'remove', 'header': 'Cache-Control'}
                                ])
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_site_cache_code_ttl(self):
        """
        set the status code cache config
        """
        error = None
        try:
            response = self.eo_client.set_site_cache_code_ttl(
                            site = 'test-sdk-eo.baidu.com',
                            cacheCodeTtl = [
                                {'value': '403', 'weight': 100, 'overrideOrigin': True, 'ttl': 10, 'type': 'code'},
                                {'value': '400', 'weight': 100, 'overrideOrigin': True, 'ttl': 10, 'type': 'code'}
                            ])
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_site_grpc_origin_on(self):
        """
        enable grpc origin
        """
        error = None
        try:
            response = self.eo_client.set_site_grpc_origin(
                                site = 'test-sdk-eo.baidu.com',
                                grpcOrigin = 'ON')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_site_grpc_origin_off(self):
        """
        disable grpc origin
        """
        error = None
        try:
            response = self.eo_client.set_site_grpc_origin(
                                site = 'test-sdk-eo.baidu.com',
                                grpcOrigin = 'OFF')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_site_http2_origin_on(self):
        """
        enable http2 origin
        """
        error = None
        try:
            response = self.eo_client.set_site_http2_origin(
                                site = 'test-sdk-eo.baidu.com',
                                http2Origin = 'ON')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_site_http2_origin_off(self):
        """
        disable http2 origin
        """
        error = None
        try:
            response = self.eo_client.set_site_http2_origin(
                                site = 'test-sdk-eo.baidu.com',
                                http2Origin = 'OFF')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_site_page_rules(self):
        """
        set the rule engine config
        """
        error = None
        try:
            page_rules = [
                {
                    'name': 'example',
                    'status': 'ON',
                    'rules': [
                        [
                            {
                                'matchFrom': 'path',
                                'operator': 'inValues',
                                'values': ['/test'],
                                'ignoreCase': True
                            },
                            {
                                'matchFrom': 'arg',
                                'operator': 'inValues',
                                'matchKey': 'test',
                                'values': ['abc']
                            }
                        ],
                        [
                            {
                                'matchFrom': 'path',
                                'operator': 'regex',
                                'values': '^/example/test[123]/$'
                            }
                        ]
                    ],
                    'config': {
                        'offlineMode': 'OFF'
                    }
                }
            ]
            response = self.eo_client.set_site_page_rules(
                                site = 'test-sdk-eo.baidu.com',
                                pageRules = page_rules)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_site_page_rules(self):
        """
        get the rule engine config
        """
        error = None
        try:
            result = self.eo_client.get_site_config_items(
                                site = 'test-sdk-eo.baidu.com',
                                keys = ['pageRules'])
            print(result)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_site_http2_disable(self):
        """
        disable http2
        """
        error = None
        try:
            response = self.eo_client.set_site_http2_disable(
                                site = 'test-sdk-eo.baidu.com',
                                http2Disable = 'ON')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_site_http3_on(self):
        """
        enable http3
        """
        error = None
        try:
            response = self.eo_client.set_site_http3(
                                site = 'test-sdk-eo.baidu.com',
                                http3 = {'enable': True})
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_site_http3_off(self):
        """
        disable http3
        """
        error = None
        try:
            response = self.eo_client.set_site_http3(
                                site = 'test-sdk-eo.baidu.com',
                                http3 = {'enable': False})
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

if __name__ == "__main__":
    unittest.main()
