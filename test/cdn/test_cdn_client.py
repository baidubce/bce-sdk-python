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
        error = None
        try:
            origin = [
                        {'peer': '1.2.3.4'}
                     ]
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
        error = None
        try:
            origin = [
                        {'peer': '1.2.3.4', 'host': 'www.origin_host.com'},
                        {'peer': '1.2.3.5', 'host': 'www.origin_host.com'}
                     ]
            response = self.cdn_client.set_domain_origin('www.example.com', origin)
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

if __name__ == "__main__":
    unittest.main()
