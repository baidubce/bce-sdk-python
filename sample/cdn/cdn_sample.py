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
Samples for cdn client.
"""

import os
import random
import string

import cdn_sample_conf
from baidubce import compat
from baidubce import exception
from baidubce.exception import BceServerError
from baidubce.services.cdn.cdn_client import CdnClient
from baidubce.services.cdn.cdn_stats_param import CdnStatsParam

import imp
import sys 

imp.reload(sys)
if compat.PY2:
    sys.setdefaultencoding('utf8')


def test_list_domains(c):
    """
    test_list_domains
    """
    response = c.list_domains()
    print(response)


def test_create_domain(c):
    """
    test_create_domain
    """
    origin = [
                {'peer': '1.2.3.4'}
             ]
    response = c.create_domain('opencdn3.sys-qa.com', origin)
    print(response)


def test_delete_domain(c):
    """
    test_delete_domain
    """
    response = c.delete_domain('opencdn3.sys-qa.com')
    print(response)


def test_enable_domain(c):
    """
    test_enable_domain
    """
    response = c.enable_domain('opencdn3.sys-qa.com')
    print(response)


def test_disable_domain(c):
    """
    test_disable_domain
    """
    response = c.disable_domain('opencdn3.sys-qa.com')
    print(response)


def test_get_domain_config(c):
    """
    test_get_domain_config
    """
    response = c.get_domain_config('opencdn3.sys-qa.com')
    print(response)


def test_set_domain_origin(c):
    """
    test_set_domain_origin
    """
    origin = [
                {'peer': '1.2.3.4', 'host': 'www.origin_host.com'},
                {'peer': '1.2.3.5', 'host': 'www.origin_host.com'}
             ]
    response = c.set_domain_origin('opencdn3.sys-qa.com', origin)
    print(response)


def test_get_domain_cache_ttl(c):
    """
    test_get_domain_cache_ttl
    """
    response = c.get_domain_cache_ttl('opencdn3.sys-qa.com')
    print(response)


def test_set_domain_cache_ttl(c):
    """
    test_set_domain_cache_ttl
    """
    rules = []
    rules.append({'type':'suffix', 'value': '.jpg', 'ttl': 3600, 'weight': 30})
    rules.append({'type':'path', 'value': '/a/b/c', 'ttl': 1800, 'weight': 15})
    response = c.set_domain_cache_ttl('opencdn3.sys-qa.com', rules)
    print(response)


def test_set_domain_cache_full_url(c):
    """
    test_set_domain_cache_full_url
    """
    response = c.set_domain_cache_full_url('opencdn3.sys-qa.com', False)
    print(response)


def test_set_domain_referer_acl(c):
    """
    test_set_domain_referer_acl
    """
    blackList = ["http://a/b/c/", "http://c/d/e/"]
    response = c.set_domain_referer_acl(
                        domain = 'opencdn3.sys-qa.com',
                        blackList = blackList,
                        allowEmpty = True)
    print(response)


def test_set_domain_ip_acl(c):
    """
    test_set_domain_ip_acl
    """
    blackList = ['1.1.1.2', '1.1.1.3']
    response = c.set_domain_ip_acl(
                        domain = 'opencdn3.sys-qa.com',
                        blackList = blackList)
    print(response)


def test_set_domain_limit_rate(c):
    """
    test_set_domain_limit_rate
    """
    limitRate = 1024
    response = c.set_domain_limit_rate('opencdn3.sys-qa.com', limitRate)
    print(response)


def test_get_domain_pv_stat(c):
    """
    use new stat api
    params is optional
    no domain->all domains by uid
    no endTime->time by now
    no startTime->24hour before endTime
    no period->3600
    no withRegion->false
    """
    response = c.get_domain_pv_stat(
            domain = 'opencdn3.sys-qa.com',
            startTime = '2018-01-11T12:00:00Z',
            endTime = '2018-01-11T13:00:00Z',
            period = 3600, withRegion = '')
    print(response)


def test_get_domain_flow_stat(c):
    """
    use new stat api
    params is optional
    no domain->all domains by uid
    no endTime->time by now
    no startTime->24hour before endTime
    no period->3600
    no withRegion->false
    """
    response = c.get_domain_flow_stat(
            domain = 'opencdn3.sys-qa.com',
            startTime = '2018-01-11T12:00:00Z',
            endTime = '2018-01-11T13:00:00Z',
            period = 3600, withRegion = '')
    print(response)


def test_get_domain_src_flow_stat(c):
    """
    use new stat api
    params is optional
    no domain->all domains by uid
    no endTime->time by now
    no startTime->24hour before endTime
    no period->3600
    """
    response = c.get_domain_src_flow_stat(
                domain = 'opencdn3.sys-qa.com',
                startTime = '2018-01-11T12:00:00Z',
                endTime = '2018-01-11T13:00:00Z',
                period = 3600)
    print(response)


def test_get_domain_hitrate_stat(c):
    """
    use new stat api
    params is optional
    """
    response = c.get_domain_hitrate_stat(
                domain = 'opencdn3.sys-qa.com',
                startTime = '2018-01-11T12:00:00Z',
                endTime = '2018-01-11T13:00:00Z',
                period = 3600)
    print(response)


def test_get_domain_httpcode_stat(c):
    """
    use new stat api
    params is optional
    """
    response = c.get_domain_httpcode_stat(
                domain = 'opencdn3.sys-qa.com',
                startTime = '2018-01-11T12:00:00Z',
                endTime = '2018-01-11T13:00:00Z',
                period = 3600)
    print(response)


def test_get_domain_tpon_url_stat(c):
    """
    use new stat api
    params is optional
    """
    response = c.get_domain_topn_url_stat(
                domain = 'opencdn3.sys-qa.com',
                startTime = '2018-01-11T12:00:00Z',
                endTime = '2018-01-11T14:00:00Z',
                period = 3600)
    print(response)


def test_get_domain_topn_referer_stat(c):
    """
    use new stat api
    params is optional
    """
    response = c.get_domain_topn_referer_stat(
                    domain = 'opencdn3.sys-qa.com',
                    startTime = '2018-01-11T12:00:00Z',
                    endTime = '2018-01-11T14:00:00Z',
                    period = 3600)
    print(response)


def test_get_domain_uv_stat(c):
    """
    use new stat api
    params is optional
    """
    response = c.get_domain_uv_stat(
                domain = 'opencdn3.sys-qa.com',
                startTime = '2018-01-11T12:00:00Z',
                endTime = '2018-01-11T14:00:00Z',
                period = 3600)
    print(response)


def test_get_domain_avg_speed_stat(c):
    """
    use new stat api
    params is optional
    no domain->all domains by uid
    no endTime->time by now
    no startTime->24hour before endTime
    no period->3600
    no withDistribution->false
    """
    response = c.get_domain_avg_speed_stat(
                domain = 'opencdn3.sys-qa.com',
                startTime = '2018-01-11T12:00:00Z',
                endTime = '2018-01-11T13:00:00Z',
                period = 3600)
    print(response)


def test_purge(c):
    """
    test_purge
    """
    tasks = []
    tasks.append({'url': 'http://opencdn3.sys-qa.com/1.jpg'})
    tasks.append({'url': 'http://opencdn3.sys-qa.com/', "type":"directory"})
    response = c.purge(tasks)
    print(response)


def test_list_purge_tasks(c):
    """
    test_list_purge_tasks
    """
    response = c.list_purge_tasks(
                id = 'cb8eb1cf-b257-4426-8ac8-59c47b19a351',
                url = 'http://opencdn3.sys-qa.com/1.jpg',
                startTime = '2018-01-11T11:00:00Z',
                endTime = '2018-01-11T12:50:00Z'
                )
    print(response)


def test_prefetch(c):
    """
    test_prefetch
    """
    tasks = []
    tasks.append({'url': 'http://opencdn3.sys-qa.com/1.jpg'})
    tasks.append({'url': 'http://opencdn3.sys-qa.com/2.jpg'})
    response = c.prefetch(tasks)
    print(response)


def test_list_prefetch_tasks(c):
    """
    test_list_prefetch_tasks
    """
    response = c.list_prefetch_tasks(
            id = 'eJwzNDLXMTSyAAAFfAFi',
            startTime = '2018-01-11T11:00:00Z',
            endTime = '2018-01-11T12:50:00Z'
            )
    print(response)


def test_get_quota(c):
    """
    test_get_quota
    """
    response = c.list_quota()
    print(response)


def test_get_domain_log(c):
    """
    test_get_domain_log
    """
    response = c.get_domain_log(
            domain = 'opencdn3.sys-qa.com',
            startTime = '2018-01-11T10:00:00Z',
            endTime = '2018-01-11T12:50:00Z')
    print(response)


def test_set_seo(c):
    """
    test_set_seo
    """
    response = c.set_seo(domain='opencdn3.sys-qa.com', push_record=True, directory_origin=True)
    print(response)


def test_get_seo(c):
    """
    test_set_seo
    """
    response = c.get_seo(domain='opencdn3.sys-qa.com')
    print(response)


def test_set_follow_protocol(c):
    """
    test_set_http_header
    """
    response = c.set_follow_protocol(domain='opencdn3.sys-qa.com', follow=True)
    print(response)


def test_ip_query(c):
    """
    test_ip_query
    """
    response = c.ip_query(action = 'describeIp', ip = '221.195.34.1')
    print(response)


def test_get_domain_stats_avg_speed(c):
    """
    test_get_domain_stats_avg_speed
    """
    param = CdnStatsParam(start_time='2019-05-26T00:00:00Z', end_time='2019-05-26T01:00:00Z', key_type=0,
                          key=['opencdn3.sys-qa.com'], period=300, groupBy='')
    param.metric = 'avg_speed'
    response = c.get_domain_stats(param)
    print(response)


def test_get_domain_stats_avg_speed_region(c):
    """
    test_get_domain_stats_avg_speed_region
    """
    param = CdnStatsParam(start_time='2019-05-26T00:00:00Z', end_time='2019-05-26T01:00:00Z', key_type=None,
                          key=['opencdn3.sys-qa.com'], period=300, groupBy='')
    param.metric = 'avg_speed_region'
    param.prov = 'beijing'
    param.isp = 'ct'
    response = c.get_domain_stats(param)
    print(response)


def test_get_domain_stats_pv(c):
    """
    test_get_domain_stats_pv
    """
    param = CdnStatsParam(start_time='2019-05-26T00:00:00Z', end_time='2019-05-26T01:00:00Z', key_type=0,
                          key=['opencdn3.sys-qa.com'], period=300, groupBy='')
    param.metric = 'pv'
    param.level = 'edge'
    response = c.get_domain_stats(param)
    print(response)


def test_get_domain_stats_pv_src(c):
    """
    test_get_domain_stats_pv_src
    """
    param = CdnStatsParam(start_time='2019-05-26T00:00:00Z', end_time='2019-05-26T01:00:00Z', key_type=0,
                          key=['opencdn3.sys-qa.com'], period=300, groupBy='')
    param.metric = 'pv_src'
    response = c.get_domain_stats(param)
    print(response)


def test_get_domain_stats_pv_region(c):
    """
    test_get_domain_stats_pv_region
    """
    param = CdnStatsParam(start_time='2019-05-26T00:00:00Z', end_time='2019-05-26T01:00:00Z', key_type=0,
                          key=['opencdn3.sys-qa.com'], period=300, groupBy='')
    param.metric = 'pv_region'
    param.prov = 'beijing'
    param.isp = 'ct'
    response = c.get_domain_stats(param)
    print(response)


def test_get_domain_stats_uv(c):
    """
    test_get_domain_stats_uv
    """
    param = CdnStatsParam(start_time='2019-05-25T00:00:00Z', end_time='2019-05-26T00:00:00Z', key_type=0,
                          key=['opencdn3.sys-qa.com'], period=3600, groupBy='')
    param.metric = 'uv'
    response = c.get_domain_stats(param)
    print(response)


def test_get_domain_stats_flow(c):
    """
    test_get_domain_stats_flow
    """
    param = CdnStatsParam(start_time='2019-05-26T00:00:00Z', end_time='2019-05-26T01:00:00Z', key_type=0,
                          key=['opencdn3.sys-qa.com'], period=300, groupBy='')
    param.metric = 'flow'
    param.level = 'edge'
    response = c.get_domain_stats(param)
    print(response)


def test_get_domain_stats_flow_protocol(c):
    """
    test_get_domain_stats_flow_protocol
    """
    param = CdnStatsParam(start_time='2019-05-26T00:00:00Z', end_time='2019-05-26T01:00:00Z', key_type=0,
                          key=['opencdn3.sys-qa.com'], period=300, groupBy='')
    param.metric = 'flow_protocol'
    param.protocol = 'http'
    response = c.get_domain_stats(param)
    print(response)


def test_get_domain_stats_flow_region(c):
    """
    test_get_domain_stats_flow_region
    """
    param = CdnStatsParam(start_time='2019-05-26T00:00:00Z', end_time='2019-05-26T01:00:00Z', key_type=0,
                          key=['opencdn3.sys-qa.com'], period=300, groupBy='')
    param.metric = 'flow_region'
    param.prov = 'beijing'
    param.isp = 'ct'
    response = c.get_domain_stats(param)
    print(response)


def test_get_domain_stats_src_flow(c):
    """
    test_get_domain_stats_src_flow
    """
    param = CdnStatsParam(start_time='2019-05-26T00:00:00Z', end_time='2019-05-26T01:00:00Z', key_type=0,
                          key=['opencdn3.sys-qa.com'], period=300, groupBy='')
    param.metric = 'src_flow'
    response = c.get_domain_stats(param)
    print(response)


def test_get_domain_stats_real_hit(c):
    """
    test_get_domain_stats_real_hit
    """
    param = CdnStatsParam(start_time='2019-05-26T00:00:00Z', end_time='2019-05-26T01:00:00Z', key_type=0,
                          key=['opencdn3.sys-qa.com'], period=300, groupBy='')
    param.metric = 'real_hit'
    response = c.get_domain_stats(param)
    print(response)


def test_get_domain_stats_pv_hit(c):
    """
    test_get_domain_stats_pv_hit
    """
    param = CdnStatsParam(start_time='2019-05-26T00:00:00Z', end_time='2019-05-26T01:00:00Z', key_type=0,
                          key=['opencdn3.sys-qa.com'], period=300, groupBy='')
    param.metric = 'pv_hit'
    response = c.get_domain_stats(param)
    print(response)


def test_get_domain_stats_httpcode(c):
    """
    test_get_domain_stats_httpcode
    """
    param = CdnStatsParam(start_time='2019-05-26T00:00:00Z', end_time='2019-05-26T01:00:00Z', key_type=0,
                          key=['opencdn3.sys-qa.com'], period=300, groupBy='')
    param.metric = 'httpcode'
    response = c.get_domain_stats(param)
    print(response)


def test_get_domain_stats_src_httpcode(c):
    """
    test_get_domain_stats_src_httpcode
    """
    param = CdnStatsParam(start_time='2019-05-26T00:00:00Z', end_time='2019-05-26T01:00:00Z', key_type=0,
                          key=['opencdn3.sys-qa.com'], period=300, groupBy='')
    param.metric = 'src_httpcode'
    response = c.get_domain_stats(param)
    print(response)


def test_get_domain_stats_httpcode_region(c):
    """
    test_get_domain_stats_src_httpcode
    """
    param = CdnStatsParam(start_time='2019-05-26T00:00:00Z', end_time='2019-05-26T01:00:00Z', key_type=0,
                          key=['opencdn3.sys-qa.com'], period=300, groupBy='')
    param.metric = 'httpcode_region'
    param.prov = 'beijing'
    param.isp = 'ct'
    response = c.get_domain_stats(param)
    print(response)


def test_get_domain_stats_top_urls(c):
    """
    test_get_domain_stats_top_urls
    """
    param = CdnStatsParam(start_time='2019-05-26T00:00:00Z', end_time='2019-05-26T01:00:00Z', key_type=0,
                          key=['opencdn3.sys-qa.com'], period=300, groupBy='')
    param.metric = 'top_urls'
    param.extra = 200
    response = c.get_domain_stats(param)
    print(response)


def test_get_domain_stats_top_referers(c):
    """
    test_get_domain_stats_top_referers
    """
    param = CdnStatsParam(start_time='2019-05-26T00:00:00Z', end_time='2019-05-26T01:00:00Z', key_type=0,
                          key=['opencdn3.sys-qa.com'], period=300, groupBy='')
    param.metric = 'top_referers'
    param.extra = 200
    response = c.get_domain_stats(param)
    print(response)


def test_get_domain_stats_top_domains(c):
    """
    test_get_domain_stats_top_domains
    """
    param = CdnStatsParam(start_time='2019-05-26T00:00:00Z', end_time='2019-05-26T01:00:00Z', period=300, groupBy='')
    param.metric = 'top_domains'
    param.extra = 200
    response = c.get_domain_stats(param)
    print(response)


def test_get_domain_stats_error(c):
    """
    test_get_domain_stats_error
    """
    param = CdnStatsParam(start_time='2019-05-26T00:00:00Z', end_time='2019-05-26T01:00:00Z', key_type=0,
                          key=['opencdn3.sys-qa.com'], period=300, groupBy='')
    param.metric = 'error'
    response = c.get_domain_stats(param)
    print(response)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    __logger = logging.getLogger(__name__)

    c = CdnClient(cdn_sample_conf.config)
    # test_list_domains(c)
    # test_create_domain(c)
    # test_delete_domain(c)
    # test_enable_domain(c)
    # test_disable_domain(c)
    # test_get_domain_config(c)
    # test_set_domain_origin(c)
    # test_get_domain_cache_ttl(c)
    # test_set_domain_cache_ttl(c)
    # test_set_domain_cache_full_url(c)
    # test_set_domain_referer_acl(c)
    # test_set_domain_ip_acl(c)
    # test_set_domain_limit_rate(c)
    # test_get_domain_pv_stat(c)
    # test_get_domain_flow_stat(c)
    # test_get_domain_src_flow_stat(c)
    # test_get_domain_hitrate_stat(c)
    # test_get_domain_httpcode_stat(c)
    # test_get_domain_tpon_url_stat(c)
    # test_get_domain_topn_referer_stat(c)
    # test_get_domain_uv_stat(c)
    # test_get_domain_avg_speed_stat(c)
    # test_purge(c)
    # test_list_purge_tasks(c)
    # test_prefetch(c)
    # test_list_prefetch_tasks(c)
    # test_get_quota(c)
    # test_get_domain_log(c)
    # test_set_seo(c)
    # test_get_seo(c)
    # test_set_follow_protocol(c)
    # test_ip_query(c)
    # test_get_domain_stats_avg_speed(c)
    # test_get_domain_stats_avg_speed_region(c)
    # test_get_domain_stats_pv(c)
    # test_get_domain_stats_pv_region(c)
    # test_get_domain_stats_pv_src(c)
    # test_get_domain_stats_flow(c)
    # test_get_domain_stats_flow_protocol(c)
    # test_get_domain_stats_flow_region(c)
    # test_get_domain_stats_src_flow(c)
    # test_get_domain_stats_pv_hit(c)
    # test_get_domain_stats_pv_hit(c)
    # test_get_domain_stats_real_hit(c)
    # test_get_domain_stats_httpcode(c)
    # test_get_domain_stats_httpcode_region(c)
    # test_get_domain_stats_src_httpcode(c)
    # test_get_domain_stats_error(c)
    # test_get_domain_stats_top_urls(c)
    # test_get_domain_stats_top_referers(c)
    # test_get_domain_stats_top_domains(c)
    # test_get_domain_stats_uv(c)
