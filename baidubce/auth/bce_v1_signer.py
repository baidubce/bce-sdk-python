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
This module provides authentication functions for bce services.
"""

import hashlib
import hmac
import logging

from baidubce.http import http_headers
from baidubce import utils


_logger = logging.getLogger(__name__)


def _get_canonical_headers(headers, headers_to_sign=None):
    headers = headers or {}

    if headers_to_sign is None or len(headers_to_sign) == 0:
        headers_to_sign = set(["host",
                               "content-md5",
                               "content-length",
                               "content-type"])
    result = []
    for k in headers:
        k_lower = k.strip().lower()
        value = str(headers[k]).strip()
        if k_lower.startswith(http_headers.BCE_PREFIX) \
                or k_lower in headers_to_sign:
            str_tmp = "%s:%s" % (utils.normalize_string(k_lower), utils.normalize_string(value))
            result.append(str_tmp)
    result.sort()

    return '\n'.join(result)


def sign(credentials, http_method, path, headers, params,
         timestamp=0, expiration_in_seconds=1800, headers_to_sign=None):
    """
    Create the authorization
    """

    _logger.debug('Sign params: %s %s %s %s %d %d %s' % (
        http_method, path, headers, params, timestamp, expiration_in_seconds, headers_to_sign))

    headers = headers or {}
    params = params or {}

    sign_key_info = 'bce-auth-v1/%s/%s/%d' % (
        credentials.access_key_id,
        utils.get_canonical_time(timestamp),
        expiration_in_seconds)
    sign_key = hmac.new(
        credentials.secret_access_key,
        sign_key_info,
        hashlib.sha256).hexdigest()

    canonical_uri = path
    canonical_querystring = utils.get_canonical_querystring(params, True)

    canonical_headers = _get_canonical_headers(headers, headers_to_sign)

    string_to_sign = '\n'.join(
        [http_method, canonical_uri, canonical_querystring, canonical_headers])

    sign_result = hmac.new(sign_key, string_to_sign, hashlib.sha256).hexdigest()

    if headers_to_sign:
        result = '%s/%s/%s' % (sign_key_info, ';'.join(headers_to_sign), sign_result)
    else:
        result = '%s//%s' % (sign_key_info, sign_result)

    _logger.debug('sign_key=[%s] sign_string=[%d bytes][ %s ]' %
                  (sign_key, len(string_to_sign), string_to_sign))
    _logger.debug('result=%s' % result)
    return result