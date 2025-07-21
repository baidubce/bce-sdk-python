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
This module provides general http handler functions for processing http responses from AIHC V2 services.

This module contains utility functions for parsing HTTP responses from AIHC (AI Hosting Cloud) services,
including JSON parsing, error handling, and response object conversion. The functions are designed
to work with the BCE (Baidu Cloud Engine) SDK framework.

Functions:
    parse_json: Parse JSON response and convert to Python object
    dict_to_python_object: Convert dictionary to Python object with Expando
    parse_json_list: Parse JSON list response
    parse_error: Handle error responses and raise appropriate exceptions
"""

import http.client
import json
from baidubce import compat, utils
from baidubce.utils import Expando
from baidubce.exception import BceClientError
from baidubce.exception import BceServerError


def parse_json(http_response, response):
    """
    Parse JSON response and convert to Python object.
    
    If the response body is not empty, convert it to a Python object and update
    the response object's attributes. The http_response is always closed if no error occurs.
    
    Args:
        http_response: The http_response object returned by HTTPConnection.getresponse()
        response: General response object which will be returned to the caller
        
    Returns:
        bool: Always returns True
        
    Note:
        This function removes the 'metadata' key from the response if it exists.
    """
    body = http_response.read()
    if body:
        response.__dict__.update(json.loads(
            body, object_hook=dict_to_python_object).__dict__)
        
        # 移除metadata key（如果存在）
        if 'metadata' in response.__dict__:
            del response.__dict__['metadata']
    http_response.close()
    return True


def dict_to_python_object(d):
    """
    Convert dictionary to Python object with Expando.
    
    Args:
        d: Dictionary to convert
        
    Returns:
        Expando: Python object with dictionary attributes
    """
    attr = {}
    for k, v in list(d.items()):
        k = str(k)
        attr[k] = v
    return Expando(attr)


def parse_json_list(http_response, response):
    """
    Parse JSON list response and convert to Python object.
    
    If the body is not empty, convert it to a Python object and set as the value of
    response.result. The http_response is always closed if no error occurs.
    
    Args:
        http_response: The http_response object returned by HTTPConnection.getresponse()
        response: General response object which will be returned to the caller
        
    Returns:
        bool: Always returns True
    """
    body = http_response.read()
    if body:
        body = compat.convert_to_string(body)
        response.__dict__["result"] = json.loads(body, object_hook=utils.dict_to_python_object)
        response.__dict__["raw_data"] = body
    http_response.close()
    return True


def parse_error(http_response, response):
    """
    Handle error responses and raise appropriate exceptions.
    
    If the HTTP status code is not 2xx, parse the error response and raise
    appropriate BCE exceptions. The http_response is always closed.
    
    Args:
        http_response: The http_response object returned by HTTPConnection.getresponse()
        response: General response object which will be returned to the caller
        
    Returns:
        bool: False if HTTP status code is 2xx
        
    Raises:
        BceClientError: If HTTP status code is 1xx (not handled)
        BceServerError: If HTTP status code is not 2xx (error response)
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
