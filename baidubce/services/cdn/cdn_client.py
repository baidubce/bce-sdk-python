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
This module provides a client class for CDN.
"""

import copy
import json
import logging
import baidubce

from baidubce import bce_base_client
from baidubce.auth import bce_v1_signer
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce.http import http_content_types
from baidubce.http import http_headers
from baidubce.http import http_methods
from baidubce.exception import BceClientError
from baidubce.exception import BceServerError
from baidubce.utils import required
from baidubce import utils
from baidubce.services.cdn.cdn_stats_param import CdnStatsParam

_logger = logging.getLogger(__name__)


class CdnClient(bce_base_client.BceBaseClient):
    """
    CdnClient
    """
    prefix = b"/v2"

    def __init__(self, config=None):
        bce_base_client.BceBaseClient.__init__(self, config)

    def list_domains(self, config=None):
        """
        get domain list

        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        return self._send_request(
            http_methods.GET,
            '/domain',
            config=config)

    def create_domain(self, domain, origin, config=None):
        """
        create domain
        :param domain: the domain name
        :type domain: string
        :param origin: the origin address list
        :type origin: list<OriginPeer>
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        return self._send_request(
            http_methods.PUT,
            '/domain/' + domain,
            body=json.dumps({'origin': origin}),
            config=config)

    def delete_domain(self, domain, config=None):
        """
        delete a domain
        :param domain: the domain name
        :type domain: string
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        return self._send_request(
            http_methods.DELETE,
            '/domain/' + domain,
            config=config)

    def enable_domain(self, domain, config=None):
        """
        enable a domain
        :param domain: the domain name
        :type domain: string
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        return self._send_request(
            http_methods.POST,
            '/domain/' + domain,
            params={'enable': ''},
            config=config)

    def disable_domain(self, domain, config=None):
        """
        disable a domain
        :param domain: the domain name
        :type domain: string
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        return self._send_request(
            http_methods.POST,
            '/domain/' + domain,
            params={'disable': ''},
            config=config)

    def get_domain_config(self, domain, config=None):
        """
        get configuration of the domain
        :param domain: the domain name
        :type domain: string
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        if domain[0] == '*':
            domain = '%2A' + domain[1:]

        return self._send_request(
            http_methods.GET,
            '/domain/' + domain + '/config',
            config=config)

    def set_domain_origin(self, domain, origin, config=None):
        """
        update origin address of the domain
        :param domain: the domain name
        :type domain: string
        :param origin: the origin address list
        :type origin: list<OriginPeer>
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        return self._send_request(
            http_methods.PUT,
            '/domain/' + domain + '/config',
            params={'origin': ''},
            body=json.dumps({'origin': origin}),
            config=config)

    def get_domain_cache_ttl(self, domain, config=None):
        """
        get cache rules of a domain
        :param domain: the domain name
        :type domain: string
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        return self._send_request(
            http_methods.GET, '/domain/' + domain + '/config',
            params={'cacheTTL': ''},
            config=config)

    @required(domain=str, rules=list)
    def set_domain_cache_ttl(self, domain, rules, config=None):
        """
        set cache rules of a domain
        :param domain: the domain name
        :type domain: string
        :param rules: cache rules
        :type rules: list
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        return self._send_request(
            http_methods.PUT,
            '/domain/' + domain + '/config',
            params={'cacheTTL': ''},
            body=json.dumps({'cacheTTL': rules}),
            config=config)

    def set_domain_cache_full_url(self, domain, flag, config=None):
        """
        set if use the full url as cache key
        :param domain: the domain name
        :type domain: string
        :param flag: 
        :type flag: bool
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        return self._send_request(
            http_methods.PUT,
            '/domain/' + domain + '/config',
            params={'cacheFullUrl': ''},
            body=json.dumps({'cacheFullUrl': flag}),
            config=config)

    @required(domain=str)
    def set_domain_referer_acl(self, domain,
                            blackList=None, whiteList=None,
                            allowEmpty=True, config=None):
        """
        set request referer access control
        :param domain: the domain name
        :type domain: string
        :param blackList: referer blackList
        :type blackList: list
        :param whitelist: referer whitelist
        :type whitelist: list
        :param allowempty: allow empty referer?
        :type allowempty: bool
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        acl = {}
        acl['allowEmpty'] = allowEmpty

        if blackList is not None:
            acl['blackList'] = blackList
        if whiteList is not None:
            acl['whiteList'] = whiteList

        return self._send_request(
            http_methods.PUT, '/domain/' + domain + '/config',
            params={'refererACL': ''},
            body=json.dumps({'refererACL': acl}),
            config=config)

    @required(domain=str)
    def set_domain_ip_acl(self, domain, blackList=None, whiteList=None, config=None):
        """
        set request ip access control
        :param domain: the domain name
        :type domain: string
        :param blackList: ip blackList
        :type blackList: list
        :param whitelist: ip whitelist
        :type whitelist: list
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        acl = {}

        if blackList is not None:
            acl['blackList'] = blackList
        if whiteList is not None:
            acl['whiteList'] = whiteList

        return self._send_request(
            http_methods.PUT, '/domain/' + domain + '/config',
            params={'ipACL': ''},
            body=json.dumps({'ipACL': acl}),
            config=config)

    @required(domain=str, https=dict)
    def set_domain_https(self, domain, https, config=None):
        """
        set request ip access control
        :param domain: the domain name
        :type domain: string
        :param https: https config
        :type https: dict
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """

        return self._send_request(
            http_methods.PUT, '/domain/' + domain + '/config',
            params={'https': ''},
            body=json.dumps({'https': https}),
            config=config)

    @required(domain=str, limitRate=int)
    def set_domain_limit_rate(self, domain, limitRate, config=None):
        """
        set limit rate
        :param domain: the domain name
        :type domain: string
        :param limitRate: limit rate value (Byte/s)
        :type limitRate: int
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        return self._send_request(
            http_methods.PUT, '/domain/' + domain + '/config',
            params={'limitRate': ''},
            body=json.dumps({'limitRate': limitRate}),
            config=config)

    @required(domain=str, request_auth=dict)
    def set_domain_request_auth(self, domain, requestAuth, config=None):
        """
        set request auth
        :param domain: the domain
        :type domain: string
        :param requestAuth: request auth config
        :type requestAuth: dict
        :param config: None
        :type config: baidubce.BceClientConfiguration
        :return:
        :rtype: baidubce.bce_response.BceResponse

        """
        return self._send_request(
            http_methods.PUT, '/domain/' + domain + '/config',
            params={'requestAuth': ''},
            body=json.dumps({'requestAuth': requestAuth}),
            config=config)

    @required(param=CdnStatsParam)
    def get_domain_stats(self, param, config=None):
        """
        query stats of the domain or uid or tagId, eg : flow pv
        :param param: the stats query param
        :type param: cdn_stats_param.CdnStatsParam
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        return self._send_request(
            http_methods.POST,
            '/stat/query',
            body=json.dumps(param.__dict__),
            config=config)

    def get_domain_pv_stat(self, domain=None,
                        startTime=None, endTime=None,
                        period=300, withRegion=None, config=None):
        """
        query pv and qps of the domain
        :param domain: the domain name
        :type domain: string
        :param startTime: query start time
        :type startTime: Timestamp
        :param endTime: query end time
        :type endTime: Timestamp
        :param period: time interval of query result
        :type period: int
        :param withRegion: if need client region distribution
        :type withRegion: any
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        params = {}
        params['domain'] = domain
        if startTime is not None:
            params['startTime'] = startTime

        if endTime is not None:
            params['endTime'] = endTime

        params['period'] = period
        params['withRegion'] = withRegion
        return self._send_request(
            http_methods.GET, '/stat/pv',
            params=params,
            config=config)

    def get_domain_flow_stat(self, domain=None,
                        startTime=None, endTime=None,
                        period=300, withRegion=None, config=None):
        """
        query bandwidth of the domain
        :param domain: the domain name
        :type domain: string
        :param startTime: query start time
        :type startTime: Timestamp
        :param endTime: query end time
        :type endTime: Timestamp
        :param period: time interval of query result
        :type period: int
        :param withRegion: if need client region distribution
        :type withRegion: any
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        params = {}
        params['domain'] = domain
        if startTime is not None:
            params['startTime'] = startTime

        if endTime is not None:
            params['endTime'] = endTime

        params['period'] = period
        params['withRegion'] = withRegion

        return self._send_request(
            http_methods.GET, '/stat/flow',
            params=params,
            config=config)

    def get_domain_src_flow_stat(self, domain=None,
                        startTime=None, endTime=None,
                        period=300, config=None):
        """
        query origin bandwidth of the domain
        :param domain: the domain name
        :type domain: string
        :param startTime: query start time
        :type startTime: Timestamp
        :param endTime: query end time
        :type endTime: Timestamp
        :param period: time interval of query result
        :type period: int
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        params = {}
        params['domain'] = domain
        if startTime is not None:
            params['startTime'] = startTime

        if endTime is not None:
            params['endTime'] = endTime

        params['period'] = period

        return self._send_request(
            http_methods.GET, '/stat/srcflow',
            params=params,
            config=config)

    def get_domain_hitrate_stat(self, domain=None,
                        startTime=None, endTime=None,
                        period=300, config=None):
        """
        query hit rate of the domain
        :param domain: the domain name
        :type domain: string
        :param startTime: query start time
        :type startTime: Timestamp
        :param endTime: query end time
        :type endTime: Timestamp
        :param period: time interval of query result
        :type period: int
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        params = {}
        params['domain'] = domain
        if startTime is not None:
            params['startTime'] = startTime

        if endTime is not None:
            params['endTime'] = endTime

        params['period'] = period
        return self._send_request(
            http_methods.GET, '/stat/hitrate',
            params=params,
            config=config)

    def get_domain_httpcode_stat(self, domain=None,
                                startTime=None, endTime=None,
                                period=300, withRegion=None, config=None):
        """
        query http response code of a domain or all domains of the user
        :param domain: the domain name
        :type domain: string
        :param startTime: query start time
        :type startTime: Timestamp
        :param endTime: query end time
        :type endTime: Timestamp
        :param period: time interval of query result
        :type period: int
        :param withRegion: if need client region distribution
        :type withRegion: any
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        params = {}
        params['domain'] = domain
        if startTime is not None:
            params['startTime'] = startTime

        if endTime is not None:
            params['endTime'] = endTime

        params['period'] = period
        params['withRegion'] = withRegion
        return self._send_request(
            http_methods.GET, '/stat/httpcode',
            params=params,
            config=config)

    def get_domain_topn_url_stat(self, domain=None,
                                startTime=None, endTime=None,
                                period=300, config=None):
        """
        query top n url of the domain or all domains of the user
        :param domain: the domain name
        :type domain: string
        :param startTime: query start time
        :type startTime: Timestamp
        :param endTime: query end time
        :type endTime: Timestamp
        :param period: time interval of query result
        :type period: int
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        params = {}
        params['domain'] = domain
        if startTime is not None:
            params['startTime'] = startTime

        if endTime is not None:
            params['endTime'] = endTime

        params['period'] = period

        return self._send_request(
            http_methods.GET, '/stat/topn/url',
            params=params,
            config=config)

    def get_domain_topn_referer_stat(self, domain=None,
                                    startTime=None, endTime=None,
                                    period=300, config=None):
        """
        query top n referer of the domain or all domains of the user
        :param domain: the domain name
        :type domain: string
        :param startTime: query start time
        :type startTime: Timestamp
        :param endTime: query end time
        :type endTime: Timestamp
        :param period: time interval of query result
        :type period: int
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        params = {}
        params['domain'] = domain
        if startTime is not None:
            params['startTime'] = startTime

        if endTime is not None:
            params['endTime'] = endTime

        params['period'] = period

        return self._send_request(
            http_methods.GET, '/stat/topn/referer',
            params=params,
            config=config)

    def get_domain_uv_stat(self, domain=None,
                        startTime=None, endTime=None,
                        period=3600, config=None):
        """
        query the total number of client of a domain or all domains of the user
        :param domain: the domain name
        :type domain: string
        :param startTime: query start time
        :type startTime: Timestamp
        :param endTime: query end time
        :type endTime: Timestamp
        :param period: time interval of query result
        :type period: int
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        params = {}
        params['domain'] = domain
        if startTime is not None:
            params['startTime'] = startTime

        if endTime is not None:
            params['endTime'] = endTime

        params['period'] = period

        return self._send_request(
            http_methods.GET, '/stat/uv',
            params=params,
            config=config)

    def get_domain_avg_speed_stat(self, domain=None,
                                startTime=None, endTime=None,
                                period=300, config=None):
        """
        query average of the domain or all domains of the user
        :param domain: the domain name
        :type domain: string
        :param startTime: query start time
        :type startTime: Timestamp
        :param endTime: query end time
        :type endTime: Timestamp
        :param period: time interval of query result
        :type period: int
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        params = {}
        params['domain'] = domain
        if startTime is not None:
            params['startTime'] = startTime

        if endTime is not None:
            params['endTime'] = endTime

        params['period'] = period

        return self._send_request(
            http_methods.GET, '/stat/avgspeed',
            params=params,
            config=config)

    @required(tasks=list)
    def purge(self, tasks, config=None):
        """
        purge the cache of specified url or directory
        :param tasks: url or directory list to purge
        :type tasks: list
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        body = {}
        body['tasks'] = tasks
        return self._send_request(
            http_methods.POST, '/cache/purge',
            config=config, body=json.dumps(body))

    def list_purge_tasks(self, id=None, url=None,
                        startTime=None, endTime=None,
                        marker=None, config=None):
        """
        query the status of purge tasks
        :param id: purge task id to query
        :type id: string
        :param url: purge url to query
        :type url: string
        :param startTime: query start time
        :type startTime: Timestamp
        :param endTime: query end time
        :type endTime: Timestamp
        :param marker: 'nextMarker' get from last query
        :type marker: int
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        params = {}
        params['id'] = id
        params['url'] = url
        if startTime is not None:
            params['startTime'] = startTime

        if endTime is not None:
            params['endTime'] = endTime

        params['marker'] = marker

        return self._send_request(
            http_methods.GET, '/cache/purge',
            params=params,
            config=config)

    @required(tasks=list)
    def prefetch(self, tasks, config=None):
        """
        prefetch the source of specified url from origin
        :param tasks: url or directory list need prefetch
        :type tasks: list
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        body = {}
        body['tasks'] = tasks
        return self._send_request(
            http_methods.POST,
            '/cache/prefetch',
            config=config, body=json.dumps(body))

    def list_prefetch_tasks(self, id=None, url=None,
                            startTime=None, endTime=None,
                            marker=None, config=None):
        """
        query the status of prefetch tasks
        :param id: prefetch task id to query
        :type id: string
        :param url: prefetch url to query
        :type url: string
        :param startTime: query start time
        :type startTime: Timestamp
        :param endTime: query end time
        :type endTime: Timestamp
        :param marker: 'nextMarker' get from last query
        :type marker: int
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        params = {}
        params['id'] = id
        params['url'] = url
        if startTime is not None:
            params['startTime'] = startTime

        if endTime is not None:
            params['endTime'] = endTime

        params['marker'] = marker

        return self._send_request(
            http_methods.GET, '/cache/prefetch',
            params=params,
            config=config)

    def list_quota(self, config=None):
        """
        query purge quota of the user
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        return self._send_request(http_methods.GET,
                                '/cache/quota',
                                config=config)

    def get_domain_log(self, domain, startTime, endTime, config=None):
        """
        get log of the domain in specified period of time
        :param domain: the domain name
        :type domain: string
        :param startTime: query start time
        :type startTime: Timestamp
        :param endTime: query end time
        :type endTime: Timestamp
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        params = {}
        if startTime is not None:
            params['startTime'] = startTime

        if endTime is not None:
            params['endTime'] = endTime

        return self._send_request(
            http_methods.GET,
            '/log/' + domain + '/log',
            params=params,
            config=config)

    def ip_query(self, action, ip, config=None):
        """
        check specified ip if belongs to Baidu CDN
        :param action: 'describeIp'
        :type action: string
        :param ip: specified ip
        :type ip: string
        """
        params = {}
        params['action'] = action
        params['ip'] = ip
        if params is None:
            params = {}
        return self._send_request(
            http_methods.GET, '/utils',
            params=params,
            config=config)

    @required(domain=str)
    def set_seo(self, domain, push_record=False, directory_origin=False, config=None):
        """
        set seo
        :param domain: the domain name
        :type domain: string
        :param push_record: push record to baidu or not
        :type param: boolean
        :param directory_origin: directory access origin or not
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        body = dict()
        body['pushRecord'] = "ON" if push_record else "OFF"
        body['diretlyOrigin'] = "ON" if directory_origin else "OFF"

        return self._send_request(
            http_methods.PUT,
            '/domain/' + domain + '/config',
            params={'seoSwitch': ''},
            body=json.dumps({'seoSwitch': body}),
            config=config)

    @required(domain=str)
    def get_seo(self, domain, config=None):
        """
        get seo configuration.
        :param domain: the domain name
        :type domain: string

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        return self._send_request(
            http_methods.GET,
            '/domain/' + domain + '/config',
            params={'seoSwitch': ''},
            config=config)

    @required(domain=str)
    def set_follow_protocol(self, domain, follow, config=None):
        """
        set follow protocol.
        :param domain: the domain name
        :type domain: string
        :param follow: follow protocol or not
        :type follow: boolean

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        return self._send_request(
            http_methods.PUT,
            '/domain/' + domain + '/config',
            params={'followProtocol': ''},
            body=json.dumps({'followProtocol': follow}),
            config=config)

    @staticmethod
    def _merge_config(self, config):
        if config is None:
            return self.config
        else:
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    def _send_request(
            self, http_method, path,
            body=None, headers=None, params=None,
            config=None,
            body_parser=None):
        config = self._merge_config(self, config)
        if body_parser is None:
            body_parser = handler.parse_json

        return bce_http_client.send_request(
            config, bce_v1_signer.sign, [handler.parse_error, body_parser],
            http_method, utils.append_uri(CdnClient.prefix, path), body, headers, params)
