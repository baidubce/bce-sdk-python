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
This module provides a general response class for BCE services.
"""
import json

from future.utils import iteritems
from builtins import str
from builtins import bytes
from baidubce import utils
from baidubce import compat
from baidubce.http import http_headers


class BceResponse(object):
    """

    """
    def __init__(self):
        self.metadata = utils.Expando()

    def set_metadata_from_headers(self, headers):
        """

        :param headers:
        :return:
        """
        for k, v in iteritems(headers):
            if k.startswith(compat.convert_to_string(http_headers.BCE_PREFIX)):
                k = 'bce_' + k[len(compat.convert_to_string(http_headers.BCE_PREFIX)):]
            k = utils.pythonize_name(k.replace('-', '_'))
            if k.lower() == compat.convert_to_string(http_headers.ETAG.lower()):
                v = v.strip('"')
            setattr(self.metadata, k, v)
    
    def set_metadata_from_headers_no_underlined(self, headers):
        """

        :param headers:
        :return:
        """
        for k, v in iteritems(headers):
            if k.lower() == compat.convert_to_string(http_headers.ETAG.lower()):
                v = v.strip('"')
            setattr(self.metadata, k, v)

    def __getattr__(self, item):
        if item.startswith('__'):
            raise AttributeError
        return None

    def __repr__(self):
        return utils.print_object(self)

    def to_map(self):
        """

        :return: dict
        """
        result = dict()
        result['headers'] = self._to_dict(self.metadata)
        result['statusCode'] = self.status_code
        result['body'] = self.get_body_map()
        return result

    def get_body_map(self):
        """
        Deserialize self.raw_data JSON string into a Python object.
        """
        content = self.raw_data
        if not content:
            return {}
        try:
            if isinstance(content, dict):
                return content
            if isinstance(content, str):
                content = content.strip()
            return json.loads(content)
        except (json.JSONDecodeError, TypeError):
            return {"raw_content": content}

    @staticmethod
    def _to_dict(obj):
        """
        Recursively convert an object to a dictionary
        """
        if isinstance(obj, (list, tuple, set)):
            return [BceResponse._to_dict(i) for i in obj]
        elif isinstance(obj, dict):
            return {k: BceResponse._to_dict(v) for k, v in obj.items()}
        elif hasattr(obj, "__dict__"):
            return {k: BceResponse._to_dict(v) for k, v in obj.__dict__.items() if not k.startswith('_')}
        else:
            # Return primitive types directly
            return obj