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
This module provides a client class for EO.
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

_logger = logging.getLogger(__name__)


class EoClient(bce_base_client.BceBaseClient):
    """
    EoClient
    """
    prefix = b"/v2/geo"

    def __init__(self, config=None):
        bce_base_client.BceBaseClient.__init__(self, config)

    @required(tasks=list, site=str)
    def purge(self, tasks, site, config=None):
        """
        purge the cache of specified url or directory
        :param tasks: url or directory list to purge
        :type tasks: list
        :param site: the site of the purge tasks
        :type site: string
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        body = {}
        body['tasks'] = tasks
        body['site'] = site
        return self._send_request(
            http_methods.POST, '/cache/purge',
            config=config, body=json.dumps(body))

    @required(site=str)
    def list_purge_tasks(self, site, id=None, startTime=None,
                        endTime=None, type=None, marker=None, config=None):
        """
        query the status of purge tasks
        :param site: the site of the purge tasks
        :type site: string
        :param id: purge task id to query
        :type id: string
        :param startTime: query start time
        :type startTime: Timestamp
        :param endTime: query end time
        :type endTime: Timestamp
        :param type: purge type to query, 'url' or 'directory'
        :type type: string
        :param marker: 'nextMarker' get from last query
        :type marker: string
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        params = {}
        params['site'] = site
        params['id'] = id
        if startTime is not None:
            params['startTime'] = startTime

        if endTime is not None:
            params['endTime'] = endTime

        params['type'] = type
        params['marker'] = marker

        return self._send_request(
            http_methods.GET, '/cache/purge',
            params=params,
            config=config)

    @required(tasks=list, site=str)
    def prefetch(self, tasks, site, config=None):
        """
        prefetch the source of specified url from origin
        :param tasks: url list need prefetch
        :type tasks: list
        :param site: the site of the prefetch tasks
        :type site: string
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        body = {}
        body['tasks'] = tasks
        body['site'] = site
        return self._send_request(
            http_methods.POST,
            '/cache/prefetch',
            config=config, body=json.dumps(body))

    @required(site=str)
    def list_prefetch_tasks(self, site, id=None, startTime=None,
                            endTime=None, marker=None, config=None):
        """
        query the status of prefetch tasks
        :param site: the site of the prefetch tasks
        :type site: string
        :param id: prefetch task id to query
        :type id: string
        :param startTime: query start time
        :type startTime: Timestamp
        :param endTime: query end time
        :type endTime: Timestamp
        :param marker: 'nextMarker' get from last query
        :type marker: string
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        params = {}
        params['site'] = site
        params['id'] = id
        if startTime is not None:
            params['startTime'] = startTime

        if endTime is not None:
            params['endTime'] = endTime

        params['marker'] = marker

        return self._send_request(
            http_methods.GET, '/cache/prefetch',
            params=params,
            config=config)

    @required(site=str)
    def get_domain_log(self, site, startTime=None, endTime=None,
                       domainList=None, pageNo=None, pageSize=None, config=None):
        """
        get the download url of the offline log of one or more domains of a site
        :param site: the site of the domains
        :type site: string
        :param startTime: query start time
        :type startTime: Timestamp
        :param endTime: query end time
        :type endTime: Timestamp
        :param domainList: the domain list to query
        :type domainList: list
        :param pageNo: page number, default is 1
        :type pageNo: int
        :param pageSize: log number per page, default is 20
        :type pageSize: int
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        body = {}
        body['site'] = site
        if startTime is not None:
            body['startTime'] = startTime

        if endTime is not None:
            body['endTime'] = endTime

        if domainList is not None:
            body['domainList'] = domainList

        if pageNo is not None:
            body['pageNo'] = pageNo

        if pageSize is not None:
            body['pageSize'] = pageSize

        return self._send_request(
            http_methods.POST, '/log',
            config=config, body=json.dumps(body))

    @required(metrics=list)
    def stat(self, metrics, startTime=None, endTime=None, showType=None,
             group=None, filter=None, limit=None, config=None):
        """
        query the statistic metrics of a site or domain
        :param metrics: metric type list, e.g. 'sum_bps', 'sum_flow', 'pv'
        :type metrics: list
        :param startTime: query start time
        :type startTime: Timestamp
        :param endTime: query end time
        :type endTime: Timestamp
        :param showType: show type, 'peak', 'time', 'sum' or 'top', default 'time'
        :type showType: string
        :param group: group fields, e.g. 'code', 'host', 'ip'
        :type group: list
        :param filter: filter items, each is a dict of key/value/operation
        :type filter: list
        :param limit: limit field, e.g. {'pageSize': 100}
        :type limit: dict
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        body = {}
        body['metrics'] = metrics
        if startTime is not None:
            body['startTime'] = startTime

        if endTime is not None:
            body['endTime'] = endTime

        if showType is not None:
            body['showType'] = showType

        if group is not None:
            body['group'] = group

        if filter is not None:
            body['filter'] = filter

        if limit is not None:
            body['limit'] = limit

        return self._send_request(
            http_methods.POST, '/stat',
            config=config, body=json.dumps(body))

    @required(site=str, cacheTtl=list)
    def set_site_config(self, site, cacheTtl, config=None):
        """
        set the node cache config of a site
        :param site: the site to set config
        :type site: string
        :param cacheTtl: the cache rules of the node
        :type cacheTtl: list
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        body = {}
        body['cacheTtl'] = cacheTtl
        return self._send_request(
            http_methods.PUT,
            '/site/' + site + '/config',
            config=config, body=json.dumps(body))

    @required(site=str)
    def get_site_config(self, site, config=None):
        """
        get the node cache config of a site
        :param site: the site to query
        :type site: string
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        return self._send_request(
            http_methods.GET,
            '/site/' + site + '/config',
            config=config)

    @required(site=str, keys=list)
    def get_site_config_items(self, site, keys, config=None):
        """
        get the specified config items of a site.
        :param site: the site to query
        :type site: string
        :param keys: the config item keys to return, in api style, e.g. ['cacheTtl']
        :type keys: list
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return: a dict mapping each requested key to its config value
        :rtype: dict
        """
        response = self.get_site_config(site, config=config)
        result = {}
        for key in keys:
            attr = utils.pythonize_name(key)
            if attr in response.__dict__:
                result[key] = response.__dict__[attr]
        return result

    @required(site=str, cacheKey=dict)
    def set_site_cache_key(self, site, cacheKey, config=None):
        """
        set the query string (cache key) config of a site
        :param site: the site to set config
        :type site: string
        :param cacheKey: the query string config, e.g. {'query': True}
        :type cacheKey: dict
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        body = {}
        body['cacheKey'] = cacheKey
        return self._send_request(
            http_methods.PUT,
            '/site/' + site + '/config',
            config=config, body=json.dumps(body))

    @required(site=str, offlineMode=str)
    def set_site_offline_mode(self, site, offlineMode, config=None):
        """
        set the offline mode config of a site
        :param site: the site to set config
        :type site: string
        :param offlineMode: 'ON' to enable offline mode, 'OFF' to disable
        :type offlineMode: string
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        body = {}
        body['offlineMode'] = offlineMode
        return self._send_request(
            http_methods.PUT,
            '/site/' + site + '/config',
            config=config, body=json.dumps(body))

    @required(site=str, httpToHttpsEnabled=str)
    def set_site_https_redirect(self, site, httpToHttpsEnabled,
                                httpToHttpsCode=None, config=None):
        """
        set the force https redirect config of a site
        :param site: the site to set config
        :type site: string
        :param httpToHttpsEnabled: 'ON' to enable force https redirect, 'OFF' to disable
        :type httpToHttpsEnabled: string
        :param httpToHttpsCode: redirect status code, '301' or '302',
                                invalid when httpToHttpsEnabled is 'OFF'
        :type httpToHttpsCode: string
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        body = {}
        body['httpToHttpsEnabled'] = httpToHttpsEnabled
        if httpToHttpsCode is not None:
            body['httpToHttpsCode'] = httpToHttpsCode

        return self._send_request(
            http_methods.PUT,
            '/site/' + site + '/config',
            config=config, body=json.dumps(body))

    @required(site=str, hsts=dict)
    def set_site_hsts(self, site, hsts, config=None):
        """
        set the hsts config of a site
        :param site: the site to set config
        :type site: string
        :param hsts: the hsts config
        :type hsts: dict
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        body = {}
        body['hsts'] = hsts
        return self._send_request(
            http_methods.PUT,
            '/site/' + site + '/config',
            config=config, body=json.dumps(body))

    @required(site=str, clientMaxBodySize=str)
    def set_site_client_max_body_size(self, site, clientMaxBodySize, config=None):
        """
        set the max upload body size config of a site
        :param site: the site to set config
        :type site: string
        :param clientMaxBodySize: the max upload size
        :type clientMaxBodySize: string
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        body = {}
        body['clientMaxBodySize'] = clientMaxBodySize
        return self._send_request(
            http_methods.PUT,
            '/site/' + site + '/config',
            config=config, body=json.dumps(body))

    @required(site=str, compress=str, compressMethodArray=list)
    def set_site_compress(self, site, compress, compressMethodArray, config=None):
        """
        set the page compress config of a site
        :param site: the site to set config
        :type site: string
        :param compress: 'ON' to enable page compress, 'OFF' to disable
        :type compress: string
        :param compressMethodArray: the compress methods, e.g. ['gzip', 'br']
        :type compressMethodArray: list
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        body = {}
        body['compress'] = compress
        body['compressMethodArray'] = compressMethodArray
        return self._send_request(
            http_methods.PUT,
            '/site/' + site + '/config',
            config=config, body=json.dumps(body))

    @required(site=str, isa=str)
    def set_site_isa(self, site, isa, config=None):
        """
        set the intelligent acceleration config of a site
        :param site: the site to set config
        :type site: string
        :param isa: 'ON' to enable intelligent acceleration, 'OFF' to disable
        :type isa: string
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        body = {}
        body['isa'] = isa
        return self._send_request(
            http_methods.PUT,
            '/site/' + site + '/config',
            config=config, body=json.dumps(body))

    @required(site=str, httpHeader=list)
    def set_site_http_header(self, site, httpHeader, config=None):
        """
        set the custom http header config of a site.
        Note: this is a full-replace interface, the existing header settings
        must be included together, otherwise they will be overwritten.
        :param site: the site to set config
        :type site: string
        :param httpHeader: the custom http header config, each item is a dict of
                           type/header/value/action
        :type httpHeader: list
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        body = {}
        body['httpHeader'] = httpHeader
        return self._send_request(
            http_methods.PUT,
            '/site/' + site + '/config',
            config=config, body=json.dumps(body))

    @required(site=str, cacheCodeTtl=list)
    def set_site_cache_code_ttl(self, site, cacheCodeTtl, config=None):
        """
        set the status code cache config of a site
        :param site: the site to set config
        :type site: string
        :param cacheCodeTtl: the status code cache rules, each item is a dict of
                             value/weight/overrideOrigin/ttl/type
        :type cacheCodeTtl: list
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        body = {}
        body['cacheCodeTtl'] = cacheCodeTtl
        return self._send_request(
            http_methods.PUT,
            '/site/' + site + '/config',
            config=config, body=json.dumps(body))

    @required(site=str, grpcOrigin=str)
    def set_site_grpc_origin(self, site, grpcOrigin, config=None):
        """
        set the grpc origin config of a site
        :param site: the site to set config
        :type site: string
        :param grpcOrigin: 'ON' to enable grpc origin, 'OFF' to disable
        :type grpcOrigin: string
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        body = {}
        body['grpcOrigin'] = grpcOrigin
        return self._send_request(
            http_methods.PUT,
            '/site/' + site + '/config',
            config=config, body=json.dumps(body))

    @required(site=str, http2Origin=str)
    def set_site_http2_origin(self, site, http2Origin, config=None):
        """
        set the http2 origin config of a site
        :param site: the site to set config
        :type site: string
        :param http2Origin: 'ON' to enable http2 origin, 'OFF' to disable
        :type http2Origin: string
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        body = {}
        body['http2Origin'] = http2Origin
        return self._send_request(
            http_methods.PUT,
            '/site/' + site + '/config',
            config=config, body=json.dumps(body))

    @required(site=str, pageRules=list)
    def set_site_page_rules(self, site, pageRules, config=None):
        """
        set the rule engine config of a site.
        Note: this is a full-replace interface, the existing rules must be
        included together, otherwise they will be overwritten.
        :param site: the site to set config
        :type site: string
        :param pageRules: the rule engine config, each item is a PageRule dict of
                          name/status/rules/config
        :type pageRules: list
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        body = {}
        body['pageRules'] = pageRules
        return self._send_request(
            http_methods.PUT,
            '/site/' + site + '/config',
            config=config, body=json.dumps(body))

    @required(site=str, http2Disable=str)
    def set_site_http2_disable(self, site, http2Disable, config=None):
        """
        set the http2 config of a site.
        Note: 'ON' means disable http2, 'OFF' means enable http2.
        :param site: the site to set config
        :type site: string
        :param http2Disable: 'ON' to disable http2, 'OFF' to enable http2
        :type http2Disable: string
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        body = {}
        body['http2Disable'] = http2Disable
        return self._send_request(
            http_methods.PUT,
            '/site/' + site + '/config',
            config=config, body=json.dumps(body))

    @required(site=str, http3=dict)
    def set_site_http3(self, site, http3, config=None):
        """
        set the http3 config of a site
        :param site: the site to set config
        :type site: string
        :param http3: the http3 config, e.g. {'enable': True}
        :type http3: dict
        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        body = {}
        body['http3'] = http3
        return self._send_request(
            http_methods.PUT,
            '/site/' + site + '/config',
            config=config, body=json.dumps(body))

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
            http_method, utils.append_uri(EoClient.prefix, path), body, headers, params)
