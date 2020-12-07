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
Unit tests for cdn client.
"""

import os
import random
import string
import unittest

import cdn_test_config
from baidubce import compat
from baidubce import exception
from baidubce.exception import BceServerError
from baidubce.services.cdn.cdn_client import CdnClient

import imp
import sys 

imp.reload(sys)
if compat.PY2:
    sys.setdefaultencoding('utf8')

class TestCdnClient(unittest.TestCase):
    """
    Test class for cdn sdk client
    """
    def setUp(self):
        self.cdn_client = CdnClient(cdn_test_config.config)
        """
        create_domain
        """
        origin = [
            {'peer': '1.2.3.4'}
        ]
        error = None
        try:
            response = self.cdn_client.create_domain('www.example.com', origin)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def tearDown(self):
        """
        delete_domain
        """
        error = None
        try:
            response = self.cdn_client.delete_domain('www.example.com')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_create_domain_form(self):
        """
        create_domain with form config
        """
        self.cdn_client.delete_domain('www.example.com')

        origin = [
            {'peer': '1.2.3.5'}
        ]
        other_config = {
            "form": "image"
        }

        error = None
        try:
            response = self.cdn_client.create_domain('www.example.com', origin, other_config)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_create_domain_defaulthost(self):
        """
        create_domain with defaultHost config
        """
        self.cdn_client.delete_domain('www.example.com')

        origin = [
            {'peer': '1.2.3.5'}
        ]
        other_config = {
            "defaultHost":"1.2.3.4"
        }

        error = None
        try:
            response = self.cdn_client.create_domain('www.example.com', origin, other_config)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_create_domain_with_follow302(self):
        """
        create_domain with origin follow302 config
        """
        self.cdn_client.delete_domain('www.example.com')

        origin = [
            {'peer': '1.2.3.5'}
        ]
        other_config = {
            "follow302": True
        }

        error = None
        try:
            response = self.cdn_client.create_domain('www.example.com', origin, other_config)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_create_domain_with_port(self):
        """
        create_domain with origin port config
        """
        self.cdn_client.delete_domain('test-sdk.sys-qa.com')

        origin = [
            {'peer': 'http://1.2.3.2'}, # no port
            {'peer': 'http://1.2.3.5:80'}, # set origin with http port
            {'peer': 'https://1.2.3.7:443'}, # set origin with https port
            {'peer': '1.2.3.1:8080'} # set origin with http port
        ]
        other_config = {
            "defaultHost":"1.2.3.4"
        }

        error = None
        try:
            response = self.cdn_client.create_domain('test-sdk.sys-qa.com', origin, other_config)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_create_domain_other(self):
        """
        create_domain with other config
        """
        self.cdn_client.delete_domain('www.example.com')

        origin = [
            {'peer': '1.2.3.5'}
        ]
        other_config = {
            "form":"image",
            "defaultHost":"1.2.3.4",
            "follow302": True
        }

        error = None
        try:
            response = self.cdn_client.create_domain('www.example.com', origin, other_config)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_list_domains(self):
        """
        test_list_domains
        """
        error = None
        try:
            response = self.cdn_client.list_domains()
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_domain_multi_configs(self):
        """
        test_set_domain_multi_configs
        """
        error = None
        multi_configs = {
            "origin": [
                {'peer': '1.2.3.4:80', 'host': 'www.originhost.com'},
                {'peer': '1.2.3.5', 'host': 'www.originhost.com'},
            ],
            "cacheFullUrl": {
                "cacheFullUrl": False,
                "cacheUrlArgs": [
                    "a",
                    "b"
                ]
            },
            "ipACL": {
                "blackList": [
                    "1.1.1.2",
                    "1.1.1.3"
                ]
            }
        }
        try:
            response = self.cdn_client.set_domain_multi_configs('test-sdk.sys-qa.com', multi_configs)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_enable_domain(self):
        """
        test_enable_domain
        """
        error = None
        try:
            response = self.cdn_client.enable_domain('www.example.com')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_disable_domain(self):
        """
        test_disable_domain
        """
        error = None
        try:
            response = self.cdn_client.disable_domain('www.example.com')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_domain_config(self):
        """
        test_get_domain_config
        """
        error = None
        try:
            response = self.cdn_client.get_domain_config('www.example.com')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_domain_origin(self):
        """
        test_set_domain_origin
        """
        origin = [
            {'peer': '1.2.3.4', 'host': 'www.originhost.com'},
            {'peer': '1.2.3.5', 'host': 'www.originhost.com'}
        ]
        error = None
        try:
            response = self.cdn_client.set_domain_origin('www.example.com', origin)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_domain_origin_with_follow302(self):
        """
        test_set_domain_origin_with_follow302
        """
        origin = [
            {'peer': '1.2.3.4', 'host': 'www.originhost.com'}
        ]
        other = {
            'follow302': True
        }
        error = None
        try:
            response = self.cdn_client.set_domain_origin('www.example.com', origin, other)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_domain_origin_with_defaulthost(self):
        """
        test_set_domain_origin_with_defaulthost
        """
        origin = [
            {'peer': '1.2.3.4', 'host': 'www.originhost.com'}
        ]
        other = {
            'defaultHost': 'myhost.com'
        }
        error = None
        try:
            response = self.cdn_client.set_domain_origin('www.example.com', origin, other)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_domain_origin_with_other(self):
        """
        test_set_domain_origin_with_default_host
        """
        origin = [
            {'peer': '1.2.3.4', 'host': 'www.originhost.com'}
        ]
        other = {
            'defaultHost': 'myhost.com',
            'follow302': True
        }
        error = None
        try:
            response = self.cdn_client.set_domain_origin('www.example.com', origin, other)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_domain_origin_with_port(self):
        """
        test_set_domain_origin_with_port
        """
        error = None
        try:
            origin = [
                {'peer': '1.2.3.4', 'host': 'www.originhost.com'},
                {'peer': '1.2.3.5', 'host': 'www.originhost.com'},
                {'peer': 'http://1.2.3.8:80', 'host': 'www.originhost.com'}, # set origin with http port
                {'peer': 'https://1.2.3.7:443', 'host': 'www.originhost.com'}, # set origin with https port
                {'peer': '1.2.3.9:8080', 'host': 'www.originhost.com'} # set origin with http port
             ]
            response = self.cdn_client.set_domain_origin('test-sdk.sys-qa.com', origin)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_domain_https(self):
        """
        test_set_domain_https
        """
        error = None
        try:
            https = {
                    'enabled': True,
                    'certId': 'cert-rm45x46isit4',
                    }
            response = self.cdn_client.set_domain_https('www.example.com', https)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_domain_cache_ttl(self):
        """
        test_set_domain_cache_ttl
        """
        error = None
        try:
            rules = []
            rules.append({'type':'suffix', 'value': '.jpg', 'ttl': 3600, 'weight': 30})
            rules.append({'type':'path', 'value': '/a/b/c', 'ttl': 1800, 'weight': 15})
            response = self.cdn_client.set_domain_cache_ttl('www.example.com', rules)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_domain_cache_ttl(self):
        """
        test_get_domain_cache_ttl
        """
        error = None
        try:
            response = self.cdn_client.get_domain_cache_ttl('www.example.com')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_domain_cache_full_url(self):
        """
        test_set_domain_cache_full_url
        """
        error = None
        try:
            response = self.cdn_client.set_domain_cache_full_url('www.example.com', True)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_domain_referer_acl(self):
        """
        test_set_domain_referer_acl
        """
        error = None
        try:
            blackList = ["http://a/b/c/", "http://c/d/e/"]
            response = self.cdn_client.set_domain_referer_acl(
                                domain = 'www.example.com',
                                blackList = blackList,
                                allowEmpty = True)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_domain_ip_acl(self):
        """
        test_set_domain_ip_acl
        """
        error = None
        try:
            blackList = ['1.1.1.2', '1.1.1.3']
            response = self.cdn_client.set_domain_ip_acl(
                                domain = 'www.example.com',
                                blackList = blackList)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_domain_limit_rate(self):
        """
        test_set_domain_limit_rate
        """
        error = None
        try:
            limitRate = 1024
            response = self.cdn_client.set_domain_limit_rate('www.example.com', limitRate)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_request_auth(self):
        """
        test_set_request_auth
        """
        error = None
        try:
            request_auth = {
                "type": "c",
                "key1": "secretekey1",
                "key2": "secretekey2",
                "timeout": 300,
                "whiteList": ["/crossdomain.xml"],
                "signArg": "sign",
                "timeArg": "t"
            }
            self.cdn_client.set_domain_request_auth('www.example.com', request_auth)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_domain_pv_stat(self):
        """
        use new stat api
        params is optional
        no domain->all domains by uid
        no endTime->time by now
        no startTime->24hour before endTime
        no period->3600
        no withRegion->false
        """
        error = None
        try:
            response = self.cdn_client.get_domain_pv_stat(
                                        domain = 'www.example.com',
                                        startTime = '2019-03-05T12:00:00Z',
                                        endTime = '2019-03-06T13:00:00Z',
                                        period = 3600, withRegion = '')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_domain_flow_stat(self):
        """
        use new stat api
        params is optional
        no domain->all domains by uid
        no endTime->time by now
        no startTime->24hour before endTime
        no period->3600
        no withRegion->false
        """
        error = None
        try:
            response = self.cdn_client.get_domain_flow_stat(
                                        domain = 'www.example.com',
                                        startTime = '2019-03-05T12:00:00Z',
                                        endTime = '2019-03-06T13:00:00Z',
                                        period = 3600, withRegion = '')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_domain_src_flow_stat(self):
        """
        use new stat api
        params is optional
        no domain->all domains by uid
        no endTime->time by now
        no startTime->24hour before endTime
        no period->3600
        """
        error = None
        try:
            response = self.cdn_client.get_domain_src_flow_stat(
                                        domain = 'www.example.com',
                                        startTime = '2019-03-05T12:00:00Z',
                                        endTime = '2019-03-06T13:00:00Z',
                                        period = 3600)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_domain_hitrate_stat(self):
        """
        use new stat api
        params is optional
        """
        error = None
        try:
            response = self.cdn_client.get_domain_hitrate_stat(
                                        domain = 'www.example.com',
                                        startTime = '2019-03-05T12:00:00Z',
                                        endTime = '2019-03-06T13:00:00Z',
                                        period = 3600)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_domain_httpcode_stat(self):
        """
        use new stat api
        params is optional
        """
        error = None
        try:
            response = self.cdn_client.get_domain_httpcode_stat(
                                        domain = 'www.example.com',
                                        startTime = '2019-03-05T12:00:00Z',
                                        endTime = '2019-03-06T13:00:00Z',
                                        period = 3600)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_domain_tpon_url_stat(self):
        """
        use new stat api
        params is optional
        """
        error = None
        try:
            response = self.cdn_client.get_domain_topn_url_stat(
                                    domain = 'www.example.com',
                                    startTime = '2019-03-05T12:00:00Z',
                                    endTime = '2019-03-06T13:00:00Z',
                                    period = 3600)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_domain_topn_referer_stat(self):
        """
        use new stat api
        params is optional
        """
        error = None
        try:
            response = self.cdn_client.get_domain_topn_referer_stat(
                                        domain = 'www.example.com',
                                        startTime = '2019-03-05T12:00:00Z',
                                        endTime = '2019-03-06T13:00:00Z',
                                        period = 3600)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_domain_uv_stat(self):
        """
        use new stat api
        params is optional
        """
        error = None
        try:
            response = self.cdn_client.get_domain_uv_stat(
                                        domain = 'www.example.com',
                                        startTime = '2019-03-05T12:00:00Z',
                                        endTime = '2019-03-06T13:00:00Z',
                                        period = 3600)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_domain_avg_speed_stat(self):
        """
        use new stat api
        params is optional
        no domain->all domains by uid
        no endTime->time by now
        no startTime->24hour before endTime
        no period->3600
        no withDistribution->false
        """
        error = None
        try:
            response = self.cdn_client.get_domain_avg_speed_stat(
                                        domain = 'www.example.com',
                                        startTime = '2019-03-05T12:00:00Z',
                                        endTime = '2019-03-06T13:00:00Z',
                                        period = 3600)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_purge(self):
        """
        test_purge
        """
        error = None
        try:
            tasks = []
            tasks.append({'url': 'http://www.example.com/1.jpg'})
            tasks.append({'url': 'http://www.example.com/', "type":"directory"})
            response = self.cdn_client.purge(tasks)
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
            response = self.cdn_client.list_purge_tasks(
                                # id = 'eJwztjA3swQAAy4BEg==',
                                url = 'http://www.example.com/1.jpg',
                                startTime = '2019-03-05T12:00:00Z',
                                endTime = '2019-03-06T13:00:00Z')
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
            tasks.append({'url': 'http://www.example.com/1.jpg'})
            tasks.append({'url': 'http://www.example.com/2.jpg'})
            response = self.cdn_client.prefetch(tasks)
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
            response = self.cdn_client.list_prefetch_tasks(
                                # id = 'c942f806-1246-5870-e724-1d579b56d438',
                                startTime = '2019-03-05T12:00:00Z',
                                endTime = '2019-03-06T13:00:00Z',)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_quota(self):
        """
        test_get_quota
        """
        error = None
        try:
            response = self.cdn_client.list_quota()
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
            response = self.cdn_client.get_domain_log(
                                    domain = 'www.example.com',
                                    startTime = '2019-03-05T12:00:00Z',
                                    endTime = '2019-03-06T13:00:00Z')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_ip_query(self):
        """
        test_ip_query
        """
        error = None
        try:
            response = self.cdn_client.ip_query(action = 'describeIp', ip = '112.67.254.34')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_seo(self):
        """
        test_set_seo
        """
        error = None
        try:
            self.cdn_client.set_seo(domain='www.example.com', push_record=True, directory_origin=True)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_seo(self):
        """
        test_get_seo
        """
        error = None
        try:
            response = self.cdn_client.get_seo(domain='www.example.com')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_follow_protocol(self):
        """
        test_set_follow_protocol
        """
        error = None
        try:
            response = self.cdn_client.set_follow_protocol(domain='www.example.com', follow=True)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_cache_share(self):
        """
        test_set_cache_share
        """
        cache_share = {
            "enabled": False,
        }
        error = None
        try:
            self.cdn_client.set_domain_cache_share('www.example.com', cache_share)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_cache_share(self):
        """
        test_get_cache_share
        """
        error = None
        try:
            response = self.cdn_client.get_domain_cache_share('www.example.com')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_traffic_limit(self):
        """
        test_set_traffic_limit
        """
        traffic_limit = {
            "enable": True,
            "limitRate": 1024,
            "limitStartHour": 1,
            "limitEndHour": 10,
            "limitRateAfter": 2048,
            "trafficLimitArg": "a",
            "trafficLimitUnit": "k"
        }
        error = None
        try:
            self.cdn_client.set_domain_traffic_limit('www.example.com', traffic_limit)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_traffic_limit(self):
        """
        test_get_traffic_limit
        """
        error = None
        try:
            response = self.cdn_client.get_domain_traffic_limit('www.example.com')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_ua_acl(self):
        """
        test_set_ua_acl
        """
        ua_acl = {
            "whiteList": [
                "Mozilla/5.0 (Windows NT 6.1",
                "Mozilla/5.0 (Linux; Android 7.0"
            ],
        }
        error = None
        try:
            self.cdn_client.set_domain_ua_acl('www.example.com', ua_acl)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_ua_acl(self):
        """
        test_get_ua_acl
        """
        error = None
        try:
            response = self.cdn_client.get_domain_ua_acl('www.example.com')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_origin_protocol(self):
        """
        test_set_origin_protocol
        """
        origin_protocol = {
            "value": "http"
        }
        error = None
        try:
            self.cdn_client.set_domain_origin_protocol('www.example.com', origin_protocol)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_origin_protocol(self):
        """
        test_get_origin_protocol
        """
        error = None
        try:
            response = self.cdn_client.get_domain_origin_protocol('www.example.com')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_retry_origin(self):
        """
        test_set_retry_origin
        """
        retry_origin = {
            "codes": [
                500,
                502
            ]
        }
        error = None
        try:
            self.cdn_client.set_domain_retry_origin('www.example.com', retry_origin)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_retry_origin(self):
        """
        test_get_retry_origin
        """
        error = None
        try:
            response = self.cdn_client.get_domain_retry_origin('www.example.com')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_ipv6_dispatch(self):
        """
        test_set_ipv6_dispatch
        """
        ipv6_dispatch = {"enable": False}
        error = None
        try:
            self.cdn_client.set_domain_ipv6_dispatch('www.example.com', ipv6_dispatch)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_ipv6_dispatch(self):
        """
        test_get_ipv6_dispatch
        """
        error = None
        try:
            response = self.cdn_client.get_domain_ipv6_dispatch('www.example.com')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_quic(self):
        """
        test_set_quic
        """
        quic = False
        error = None
        try:
            self.cdn_client.set_domain_quic('www.example.com', quic)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_quic(self):
        """
        test_get_quic
        """
        error = None
        try:
            response = self.cdn_client.get_domain_quic('www.example.com')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_offline_mode(self):
        """
        test_set_offline_mode
        """
        offline_mode = True
        error = None
        try:
            self.cdn_client.set_domain_offline_mode('www.example.com', offline_mode)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_offline_mode(self):
        """
        test_get_offline_mode
        """
        error = None
        try:
            response = self.cdn_client.get_domain_offline_mode('www.example.com')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_set_ocsp(self):
        """
        test_set_ocsp
        """
        ocsp = False
        error = None
        try:
            self.cdn_client.set_domain_ocsp('www.example.com', ocsp)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_ocsp(self):
        """
        test_get_ocsp
        """
        error = None
        try:
            response = self.cdn_client.get_domain_ocsp('www.example.com')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_ips_query(self):
        """
        test_ips_query
        """
        error = None
        action = 'describeIp'
        ips = [
            "1.3.5.6",
            "2.36.4.1",
            "1.56.97.180",
            "111.63.51.2"
        ]
        try:
            response = self.cdn_client.ips_query(action, ips)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_list_nodes(self):
        """
        test_list_nodes
        """
        error = None
        try:
            response = self.cdn_client.list_nodes()
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

if __name__ == "__main__":
    unittest.main()
