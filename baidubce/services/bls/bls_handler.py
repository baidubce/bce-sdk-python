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
This module provides general http handler functions for processing http responses from BCM services.
"""

import http.client
import json
from baidubce import compat, utils
from baidubce.exception import BceClientError
from baidubce.exception import BceServerError


def parse_error(http_response, response):
    """If the body is not empty, convert it to a python object and set as the value of
    response.body. http_response is always closed if no error occurs.

    :param http_response: the http_response object returned by HTTPConnection.getresponse()
    :type http_response: httplib.HTTPResponse

    :param response: general response object which will be returned to the caller
    :type response: baidubce.BceResponse

    :return: false if http status code is 2xx, raise an error otherwise
    :rtype bool

    :raise baidubce.exception.BceClientError: if http status code is NOT 2xx
    """
    if http_response.status // 100 == http.client.OK // 100:
        return False
    if http_response.status // 100 == http.client.CONTINUE // 100:
        raise BceClientError(b'Can not handle 1xx http status code')
    body = http_response.read()
    if not body:
        bse = BceServerError(http_response.reason, request_id=response.metadata.bce_request_id)
        bse.status_code = http_response.status
        raise bse

    error_dict = json.loads(compat.convert_to_string(body))
    message = str(error_dict)
    if 'message' in error_dict and error_dict['message'] is not None:
        message = error_dict['message']
    code = "Exception"
    if 'code' in error_dict and error_dict['code'] is not None:
        code = error_dict['code']
    request_id = response.metadata.bce_request_id
    if 'request_id' in error_dict and error_dict['request_id'] is not None:
        request_id = error_dict['request_id']

    bse = BceServerError(message, code=code, request_id=request_id)
    bse.status_code = http_response.status
    raise bse
