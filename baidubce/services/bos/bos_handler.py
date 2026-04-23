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
This module provides general http handler functions for processing http responses from bos services.
"""

import json
import re
from baidubce import compat
from baidubce import utils
from baidubce.exception import BceServerError
from baidubce.http import handler
from builtins import str
from builtins import bytes

# Bucket naming rules per BOS official specification:
#   - Allowed characters: lowercase letters, digits, hyphens
#   - Length: 3 ~ 63
#   - Must start and end with a lowercase letter or digit
_BUCKET_NAME_REGEX = re.compile(r'^[a-z0-9][a-z0-9\-]{1,61}[a-z0-9]$')


def validate_bucket_name(bucket_name):
    """
    Validate bucket name against BOS official naming rules.
    Raises ValueError for any violation, blocking the request before URL assembly or signing.

    Rules:
      - Allowed characters: [a-z0-9-]
      - Length: 3 ~ 63
      - Must start and end with a lowercase letter or digit
    """
    if bucket_name is None:
        return
    if isinstance(bucket_name, bytes):
        try:
            bucket_name = bucket_name.decode('utf-8')
        except UnicodeDecodeError as e:
            raise ValueError("Invalid bucket name: not valid UTF-8: %s" % e)
    if not _BUCKET_NAME_REGEX.match(bucket_name):
        raise ValueError(
            "Invalid bucket name %r: must match ^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$ "
            "(lowercase letters, digits and hyphens only, length 3-63, "
            "start and end with letter or digit)" % bucket_name
        )

def parse_copy_object_response(http_response, response):
    """
    response parser for copy object
    """
    TRANSFER_ENCODING = compat.convert_to_string('transfer-encoding')
    CHUNKED = compat.convert_to_string('chunked')
    headers_list = {compat.convert_to_string(k).lower(): compat.convert_to_string(v)
                    for k, v in http_response.getheaders()}
    if headers_list.get(TRANSFER_ENCODING, '') == CHUNKED:
        body = http_response.read()
        if body:
            # json.loads always returns str keys on both Py2 (unicode) and Py3 (str).
            body_str = compat.convert_to_string(body)
            d = json.loads(body_str)
            if 'code' in d:
                http_response.close()
                raise BceServerError(d['message'], code=d['code'], request_id=d['requestId'])
            else:
                response.__dict__.update(
                    json.loads(body_str, object_hook=utils.dict_to_python_object).__dict__)
                http_response.close()
        else:
            e = BceServerError(http_response.reason, request_id=response.metadata.bce_request_id)
            http_response.close()
            raise e
        return True
    else:
        return handler.parse_json(http_response, response)

def validate_object_key(key):
    """
    Validate object key against path traversal and malformed URI attacks.
    Rules align with BOS server-side behavior:
      - empty key is rejected
      - '..' segments are rejected (400 Bad Request)
      - '.' segments are rejected (400 InvalidURI)
      - Leading '//' double-slash is normalized away by strip('/') before this call
    """
    if isinstance(key, bytes):
        try:
            key = key.decode('utf-8')
        except UnicodeDecodeError as e:
            raise ValueError("Invalid object key: key is not valid UTF-8: %s" % e)
    if not key:
        raise ValueError("Invalid object key: key must not be empty")
    for segment in key.split('/'):
        if segment == '..':
            raise ValueError(
                "Invalid object key: path traversal with '..' is not allowed: %s" % key
            )
        if segment == '.':
            raise ValueError(
                "Invalid object key: '.' path segment is not allowed: %s" % key
            )
