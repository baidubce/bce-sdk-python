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
Samples for eo client.
"""

import imp
import sys

import eo_sample_conf
from baidubce import compat
from baidubce.services.eo.eo_client import EoClient

imp.reload(sys)
if compat.PY2:
    sys.setdefaultencoding('utf8')


def test_purge(eo_client):
    """
    test_purge
    """
    tasks = []
    tasks.append({'url': 'http://1.test-sdk-eo.baidu.com/test1.png', 'type': 'file'})
    tasks.append({'url': 'http://1.test-sdk-eo.baidu.com/', 'type': 'directory'})
    response = eo_client.purge(tasks, 'test-sdk-eo.baidu.com')
    print(response)


def test_list_purge_tasks(eo_client):
    """
    test_list_purge_tasks
    """
    response = eo_client.list_purge_tasks(
            site='test-sdk-eo.baidu.com',
            type='file',
            startTime='2026-07-21T05:10:10Z',
            endTime='2026-07-21T07:10:10Z')
    print(response)


def test_list_purge_tasks_by_task_id(eo_client):
    """
    test_list_purge_tasks_by_task_id
    """
    response = eo_client.list_purge_tasks(
            site = 'test-sdk-eo.baidu.com',
            id = 'task_id')
    print(response)


def test_prefetch(eo_client):
    """
    test_prefetch
    """
    tasks = []
    tasks.append({'url': 'http://1.test-sdk-eo.baidu.com/test1.png'})
    tasks.append({'url': 'http://1.test-sdk-eo.baidu.com/test2.png'})
    response = eo_client.prefetch(tasks, 'test-sdk-eo.baidu.com')
    print(response)


def test_list_prefetch_tasks(eo_client):
    """
    test_list_prefetch_tasks
    """
    response = eo_client.list_prefetch_tasks(
            site='test-sdk-eo.baidu.com',
            startTime='2026-07-21T05:26:55Z',
            endTime='2026-07-21T07:26:55Z')
    print(response)


def test_list_prefetch_tasks_by_task_id(eo_client):
    """
    test_list_prefetch_tasks_by_task_id
    """
    response = eo_client.list_prefetch_tasks(
        site = 'test-sdk-eo.baidu.com',
        id = 'task_id')
    print(response)


def test_get_domain_log(eo_client):
    """
    test_get_domain_log
    """
    response = eo_client.get_domain_log(
            site='test-sdk-eo.baidu.com',
            startTime='2026-07-21T05:00:00Z',
            endTime='2026-07-21T07:00:00Z',
            domainList=['1.test-sdk-eo.baidu.com'],
            pageNo=1,
            pageSize=20)
    print(response)


def test_stat_bps_peak(eo_client):
    """
    query peak of sum_bps/upstream_bps/download_bps by site
    """
    response = eo_client.stat(
            metrics=['sum_bps', 'upstream_bps', 'download_bps'],
            startTime='2026-05-10T16:00:00Z',
            endTime='2026-05-11T09:06:29Z',
            showType='peak',
            filter=[{
                'key': 'site',
                'operation': 'equal',
                'value': ['test-sdk-eo.baidu.com']
            }])
    print(response)


def test_stat_sum_bps_time(eo_client):
    """
    query time series of sum_bps by site
    """
    response = eo_client.stat(
            metrics=['sum_bps'],
            startTime='2026-05-10T16:00:00Z',
            endTime='2026-05-11T09:06:29Z',
            showType='time',
            filter=[{
                'key': 'site',
                'operation': 'equal',
                'value': ['test-sdk-eo.baidu.com']
            }])
    print(response)


def test_stat_flow_sum(eo_client):
    """
    query sum of sum_flow/upstream_flow/download_flow by site
    """
    response = eo_client.stat(
            metrics=['sum_flow', 'upstream_flow', 'download_flow'],
            startTime='2026-05-10T16:00:00Z',
            endTime='2026-05-11T09:06:29Z',
            showType='sum',
            filter=[{
                'key': 'site',
                'operation': 'equal',
                'value': ['test-sdk-eo.baidu.com']
            }])
    print(response)


def test_stat_sum_flow_time(eo_client):
    """
    query time series of sum_flow by site
    """
    response = eo_client.stat(
            metrics=['sum_flow'],
            startTime='2026-05-10T16:00:00Z',
            endTime='2026-05-11T09:06:29Z',
            showType='time',
            filter=[{
                'key': 'site',
                'operation': 'equal',
                'value': ['test-sdk-eo.baidu.com']
            }])
    print(response)


def test_stat_pv_sum(eo_client):
    """
    query sum of pv by site
    """
    response = eo_client.stat(
            metrics=['pv'],
            startTime='2026-05-10T16:00:00Z',
            endTime='2026-05-11T09:06:29Z',
            showType='sum',
            filter=[{
                'key': 'site',
                'operation': 'equal',
                'value': ['test-sdk-eo.baidu.com']
            }])
    print(response)


def test_stat_pv_peak(eo_client):
    """
    query peak of pv by site
    """
    response = eo_client.stat(
            metrics=['pv'],
            startTime='2026-05-10T16:00:00Z',
            endTime='2026-05-11T09:06:29Z',
            showType='peak',
            filter=[{
                'key': 'site',
                'operation': 'equal',
                'value': ['test-sdk-eo.baidu.com']
            }])
    print(response)


def test_stat_pv_time(eo_client):
    """
    query time series of pv by site
    """
    response = eo_client.stat(
            metrics=['pv'],
            startTime='2026-05-10T16:00:00Z',
            endTime='2026-05-11T09:06:29Z',
            showType='time',
            filter=[{
                'key': 'site',
                'operation': 'equal',
                'value': ['test-sdk-eo.baidu.com']
            }])
    print(response)


def test_stat_code_sum(eo_client):
    """
    query sum of status code (pv grouped by code) by site
    """
    response = eo_client.stat(
            metrics=['pv'],
            startTime='2026-05-10T16:00:00Z',
            endTime='2026-05-11T11:05:47Z',
            showType='sum',
            group=['code'],
            filter=[{
                'key': 'site',
                'operation': 'equal',
                'value': ['test-sdk-eo.baidu.com']
            }])
    print(response)


def test_stat_code_time(eo_client):
    """
    query time series of status code (pv grouped by code) by site
    """
    response = eo_client.stat(
            metrics=['pv'],
            startTime='2026-05-10T16:00:00Z',
            endTime='2026-05-11T11:05:47Z',
            showType='time',
            group=['code'],
            filter=[{
                'key': 'site',
                'operation': 'equal',
                'value': ['test-sdk-eo.baidu.com']
            }])
    print(response)


def test_stat_host_top(eo_client):
    """
    query top pv grouped by host by site
    """
    response = eo_client.stat(
            metrics=['pv'],
            startTime='2026-06-02T16:00:00Z',
            endTime='2026-06-03T02:03:14Z',
            showType='top',
            group=['host'],
            filter=[{
                'key': 'site',
                'operation': 'equal',
                'value': ['test-sdk-eo.baidu.com']
            }],
            limit={'pageSize': 100})
    print(response)


def test_set_site_config_follow_origin_default(eo_client):
    """
    follow origin - default cache policy
    """
    response = eo_client.set_site_config(
            site='test-sdk-eo.baidu.com',
            cacheTtl=[])
    print(response)


def test_set_site_config_follow_origin_no_cache(eo_client):
    """
    follow origin - no cache
    """
    response = eo_client.set_site_config(
            site='test-sdk-eo.baidu.com',
            cacheTtl=[{
                'value': '/',
                'weight': 100,
                'override_origin': False,
                'ttl': 0,
                'type': 'path'
            }])
    print(response)


def test_get_site_config(eo_client):
    """
    test_get_site_config
    """
    response = eo_client.get_site_config(site='test-sdk-eo.baidu.com')
    print(response)


def test_get_site_config_items(eo_client):
    """
    test_get_site_config_items: only get the specified config items
    """
    result = eo_client.get_site_config_items(
            site='test-sdk-eo.baidu.com',
            keys=['cacheTtl'])
    print(result)


def test_set_site_cache_key_keep_all(eo_client):
    """
    keep all query string
    """
    response = eo_client.set_site_cache_key(
            site='test-sdk-eo.baidu.com',
            cacheKey={'query': True})
    print(response)


def test_set_site_cache_key_ignore_all(eo_client):
    """
    ignore all query string
    """
    response = eo_client.set_site_cache_key(
            site='test-sdk-eo.baidu.com',
            cacheKey={'query': False, 'include_args': []})
    print(response)


def test_set_site_cache_key_include_args(eo_client):
    """
    keep the specified query args
    """
    response = eo_client.set_site_cache_key(
            site='test-sdk-eo.baidu.com',
            cacheKey={'query': False, 'include_args': ['test1']})
    print(response)


def test_set_site_cache_key_exclude_args(eo_client):
    """
    ignore the specified query args
    """
    response = eo_client.set_site_cache_key(
            site='test-sdk-eo.baidu.com',
            cacheKey={'query': False, 'exclude_args': ['test1', 'test2']})
    print(response)


def test_set_site_offline_mode_on(eo_client):
    """
    enable offline mode
    """
    response = eo_client.set_site_offline_mode(
            site='test-sdk-eo.baidu.com',
            offlineMode='ON')
    print(response)


def test_set_site_https_redirect_302(eo_client):
    """
    enable force https redirect with 302
    """
    response = eo_client.set_site_https_redirect(
            site='test-sdk-eo.baidu.com',
            httpToHttpsEnabled='ON',
            httpToHttpsCode='302')
    print(response)


def test_set_site_https_redirect_301(eo_client):
    """
    enable force https redirect with 301
    """
    response = eo_client.set_site_https_redirect(
            site='test-sdk-eo.baidu.com',
            httpToHttpsEnabled='ON',
            httpToHttpsCode='301')
    print(response)


def test_set_site_https_redirect_off(eo_client):
    """
    disable force https redirect
    """
    response = eo_client.set_site_https_redirect(
            site='test-sdk-eo.baidu.com',
            httpToHttpsEnabled='OFF')
    print(response)


def test_set_site_hsts_off(eo_client):
    """
    disable hsts
    """
    response = eo_client.set_site_hsts(
            site='test-sdk-eo.baidu.com',
            hsts={'maxAge': -1, 'includeSubDomains': False, 'preload': False})
    print(response)


def test_set_site_hsts_on(eo_client):
    """
    enable hsts
    """
    response = eo_client.set_site_hsts(
            site='test-sdk-eo.baidu.com',
            hsts={'includeSubDomains': True, 'preload': False, 'maxAge': 60})
    print(response)


def test_set_site_client_max_body_size(eo_client):
    """
    set the max upload body size config
    """
    response = eo_client.set_site_client_max_body_size(
            site='test-sdk-eo.baidu.com',
            clientMaxBodySize='500m')
    print(response)


def test_set_site_compress_on(eo_client):
    """
    enable page compress
    """
    response = eo_client.set_site_compress(
            site='test-sdk-eo.baidu.com',
            compress='ON',
            compressMethodArray=['gzip', 'br'])
    print(response)


def test_set_site_compress_off(eo_client):
    """
    disable page compress
    """
    response = eo_client.set_site_compress(
            site='test-sdk-eo.baidu.com',
            compress='OFF',
            compressMethodArray=[])
    print(response)


def test_set_site_isa_on(eo_client):
    """
    enable intelligent acceleration
    """
    response = eo_client.set_site_isa(
            site='test-sdk-eo.baidu.com',
            isa='ON')
    print(response)


def test_set_site_isa_off(eo_client):
    """
    disable intelligent acceleration
    """
    response = eo_client.set_site_isa(
            site='test-sdk-eo.baidu.com',
            isa='OFF')
    print(response)


def test_set_site_http_header_set(eo_client):
    """
    set http header
    """
    response = eo_client.set_site_http_header(
            site='test-sdk-eo.baidu.com',
            httpHeader=[
                {'type': 'response', 'header': 'Cache-Control', 'value': 'test', 'action': 'add'},
                {'action': 'add', 'type': 'origin', 'header': 'Expires', 'value': 'test'}
            ])
    print(response)


def test_set_site_http_header_remove(eo_client):
    """
    remove http header
    """
    response = eo_client.set_site_http_header(
            site='test-sdk-eo.baidu.com',
            httpHeader=[
                {'type': 'response', 'value': '', 'action': 'remove', 'header': 'Expires'},
                {'value': '', 'type': 'origin', 'action': 'remove', 'header': 'Cache-Control'}
            ])
    print(response)


def test_set_site_cache_code_ttl(eo_client):
    """
    set the status code cache config
    """
    response = eo_client.set_site_cache_code_ttl(
            site='test-sdk-eo.baidu.com',
            cacheCodeTtl=[
                {'value': '404', 'weight': 100, 'overrideOrigin': True, 'ttl': 10, 'type': 'code'},
                {'value': '400', 'weight': 100, 'overrideOrigin': True, 'ttl': 10, 'type': 'code'}
            ])
    print(response)


def test_set_site_grpc_origin_on(eo_client):
    """
    enable grpc origin
    """
    response = eo_client.set_site_grpc_origin(
            site='test-sdk-eo.baidu.com',
            grpcOrigin='ON')
    print(response)


def test_set_site_grpc_origin_off(eo_client):
    """
    disable grpc origin
    """
    response = eo_client.set_site_grpc_origin(
            site='test-sdk-eo.baidu.com',
            grpcOrigin='OFF')
    print(response)


def test_set_site_http2_origin_on(eo_client):
    """
    enable http2 origin
    """
    response = eo_client.set_site_http2_origin(
            site='test-sdk-eo.baidu.com',
            http2Origin='ON')
    print(response)


def test_set_site_http2_origin_off(eo_client):
    """
    disable http2 origin
    """
    response = eo_client.set_site_http2_origin(
            site='test-sdk-eo.baidu.com',
            http2Origin='OFF')
    print(response)


def test_set_site_page_rules(eo_client):
    """
    set the rule engine config
    """
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
    response = eo_client.set_site_page_rules(
            site='test-sdk-eo.baidu.com',
            pageRules=page_rules)
    print(response)


def test_get_site_page_rules(eo_client):
    """
    get the rule engine config
    """
    result = eo_client.get_site_config_items(
            site='test-sdk-eo.baidu.com',
            keys=['pageRules'])
    print(result)


def test_set_site_http2_disable(eo_client):
    """
    disable http2
    """
    response = eo_client.set_site_http2_disable(
            site='test-sdk-eo.baidu.com',
            http2Disable='ON')
    print(response)


def test_set_site_http3_on(eo_client):
    """
    enable http3
    """
    response = eo_client.set_site_http3(
            site='test-sdk-eo.baidu.com',
            http3={'enable': True})
    print(response)


def test_set_site_http3_off(eo_client):
    """
    disable http3
    """
    response = eo_client.set_site_http3(
            site='test-sdk-eo.baidu.com',
            http3={'enable': False})
    print(response)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    __logger = logging.getLogger(__name__)

    eo_client = EoClient(eo_sample_conf.config)

    # 缓存管理
    # test_purge(eo_client)
    # test_list_purge_tasks(eo_client)
    # test_list_purge_tasks_by_task_id(eo_client)
    # test_prefetch(eo_client)
    # test_list_prefetch_tasks(eo_client)
    # test_list_prefetch_tasks_by_task_id(eo_client)

    # 离线日志
    # test_get_domain_log(eo_client)

    # 统计指标
    # test_stat_bps_peak(eo_client)
    # test_stat_sum_bps_time(eo_client)
    # test_stat_flow_sum(eo_client)
    # test_stat_sum_flow_time(eo_client)
    # test_stat_pv_sum(eo_client)
    # test_stat_pv_peak(eo_client)
    # test_stat_pv_time(eo_client)
    # test_stat_code_sum(eo_client)
    # test_stat_code_time(eo_client)
    # test_stat_host_top(eo_client)

    # 站点配置、规则引擎
    # test_set_site_config_follow_origin_default(eo_client)
    # test_set_site_config_follow_origin_no_cache(eo_client)
    # test_get_site_config(eo_client)
    # test_get_site_config_items(eo_client)
    # test_set_site_cache_key_keep_all(eo_client)
    # test_set_site_cache_key_ignore_all(eo_client)
    # test_set_site_cache_key_include_args(eo_client)
    # test_set_site_cache_key_exclude_args(eo_client)
    # test_set_site_offline_mode_on(eo_client)
    # test_set_site_https_redirect_302(eo_client)
    # test_set_site_https_redirect_301(eo_client)
    # test_set_site_https_redirect_off(eo_client)
    # test_set_site_hsts_off(eo_client)
    # test_set_site_hsts_on(eo_client)
    # test_set_site_client_max_body_size(eo_client)
    # test_set_site_compress_on(eo_client)
    # test_set_site_compress_off(eo_client)
    # test_set_site_isa_on(eo_client)
    # test_set_site_isa_off(eo_client)
    # test_set_site_http_header_set(eo_client)
    # test_set_site_http_header_remove(eo_client)
    # test_set_site_cache_code_ttl(eo_client)
    # test_set_site_grpc_origin_on(eo_client)
    # test_set_site_grpc_origin_off(eo_client)
    # test_set_site_http2_origin_on(eo_client)
    # test_set_site_http2_origin_off(eo_client)
    # test_set_site_page_rules(eo_client)
    # test_get_site_page_rules(eo_client)
    # test_set_site_http2_disable(eo_client)
    # test_set_site_http3_on(eo_client)
    # test_set_site_http3_off(eo_client)
