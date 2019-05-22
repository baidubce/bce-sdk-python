# Copyright 2017 Baidu, Inc.
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
This module provides a client class for VCR.
"""

import copy
import json
import logging
from builtins import str
from builtins import bytes

from baidubce.auth import bce_v1_signer
from baidubce.bce_base_client import BceBaseClient
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce.http import http_methods
from baidubce.utils import required

_logger = logging.getLogger(__name__)


class VcrClient(BceBaseClient):
    """
    vcr client
    """

    def __init__(self, config=None):
        BceBaseClient.__init__(self, config)

    @required(source=(bytes, str))
    def put_media(self, source, auth=None, description=None,
                  preset=None, notification=None, config=None):
        """
        Check a media.
        :param source: media source
        :type source: string or unicode
        :param auth: media source auth param
        :type auth: string or unicode
        :param description: media description
        :type description: string or unicode
        :param preset: analyze preset name
        :type preset: string or unicode
        :param notification: notification name
        :type notification: string or unicode
        :return: **Http Response**
        """
        body = {
            'source': source
        }
        if auth is not None:
            body['auth'] = auth
        if description is not None:
            body['description'] = description
        if preset is not None:
            body['preset'] = preset
        if notification is not None:
            body['notification'] = notification
        return self._send_request(http_methods.PUT, b'/v1/media',
                                  body=json.dumps(body),
                                  config=config)

    @required(source=(bytes, str))
    def get_media(self, source, config=None):
        """
        :param source: media source
        :type source: string or unicode
        :return: **Http Response**
        """
        return self._send_request(http_methods.GET, b'/v1/media',
                                  params={b'source': source},
                                  config=config)

    @required(source=(bytes, str))
    def put_stream(self, source, preset=None, notification=None, config=None):
        """
        :param source: media source
        :type source: string or unicode
        :param preset: analyze preset name
        :type preset: string or unicode
        :param notification: notification name
        :type notification: string or unicode
        :return: **Http Response**
        """
        body = {
            'source': source
        }
        if preset is not None:
            body['preset'] = preset
        if notification is not None:
            body['notification'] = notification
        return self._send_request(http_methods.POST, b'/v1/stream',
                                  body=json.dumps(body),
                                  config=config)

    @required(source=(bytes, str))
    def get_stream(self, source, start_time=None, end_time=None, config=None):
        """
        :param source: media source
        :type source: string or unicode
        :param start_time: None
        :type start_time: string or unicode
        :param end_time: start_time should be earlier than end_time
        :type end_time: string or unicode
        :return: **Http Response**
        """
        params = {b'source': source}
        if start_time is not None:
            params[b'startTime'] = start_time
        if end_time is not None:
            params[b'endTime'] = end_time
        return self._send_request(http_methods.GET, b'/v1/stream',
                                  params=params,
                                  config=config)

    @required(source=(bytes, str))
    def put_image(self, source, preset=None, config=None):
        """
        :param source: media source
        :type source: string or unicode
        :param preset: analyze preset name
        :type preset: string or unicode
        :return: **Http Response**
        """
        body = {
            'source': source
        }
        if preset is not None:
            body['preset'] = preset
        return self._send_request(http_methods.PUT, b'/v1/image',
                                  body=json.dumps(body),
                                  config=config)

    @required(text=(bytes, str))
    def put_text(self, text, preset=None, config=None):
        """
        :param text: string
        :type text: text to check
        :param preset: analyze preset name
        :type preset: string or unicode
        :return: **Http Response**
        """
        body = {
            'text': text
        }
        if preset is not None:
            body['preset'] = preset
        return self._send_request(http_methods.PUT, b'/v1/text',
                                  body=json.dumps(body),
                                  config=config)

    @required(lib=(str, unicode), brief=(str, unicode), image=(str, unicode))
    def add_face_image(self, lib, brief, image, config=None):
        """
        :param lib: private face lib
        :param brief: private face brief
        :param image: private face image
        :return: **Http Response**
        """
        body = {
            'brief': brief,
            'image': image
        }
        return self._send_request(http_methods.POST, '/v1/face/lib/%s' % lib,
                                  body=json.dumps(body),
                                  config=config)

    @required(lib=(str, unicode), brief=(str, unicode))
    def del_face_brief(self, lib, brief, config=None):
        """
        :param lib: private face lib
        :param brief: private face brief
        :return: **Http Response**
        """
        params = {
            'brief': brief
        }
        return self._send_request(http_methods.DELETE, '/v1/face/lib/%s' % lib,
                                  params=params,
                                  config=config)

    @required(lib=(str, unicode), brief=(str, unicode), image=(str, unicode))
    def del_face_image(self, lib, brief, image, config=None):
        """
        :param lib: private face lib
        :param brief: private face brief
        :param image: private face image
        :return: **Http Response**
        """
        params = {
            'brief': brief,
            'image': image
        }
        return self._send_request(http_methods.DELETE, '/v1/face/lib/%s' % lib,
                                  params=params,
                                  config=config)

    @required(lib=(str, unicode))
    def get_face_lib(self, lib, config=None):
        """
        :param lib: private face lib
        :return: **Http Response**
        """
        return self._send_request(http_methods.GET, '/v1/face/lib/%s' % lib,
                                  config=config)

    @required(lib=(str, unicode), brief=(str, unicode))
    def get_face_brief(self, lib, brief, config=None):
        """
        :param lib: private face lib
        :param brief: private face brief
        :return: **Http Response**
        """
        params = {
            'brief': brief
        }
        return self._send_request(http_methods.GET, '/v1/face/lib/%s' % lib,
                                  params=params,
                                  config=config)

    @required(lib=(str, unicode), brief=(str, unicode), image=(str, unicode))
    def add_logo_image(self, lib, brief, image, config=None):
        """
        :param lib: private logo lib
        :param brief: private logo brief
        :param image: private logo image
        :return: **Http Response**
        """
        body = {
            'brief': brief,
            'image': image
        }
        return self._send_request(http_methods.POST, '/v1/logo/lib/%s' % lib,
                                  body=json.dumps(body),
                                  config=config)

    @required(lib=(str, unicode), brief=(str, unicode))
    def del_logo_brief(self, lib, brief, config=None):
        """
        :param lib: private logo lib
        :param brief: private logo brief
        :return: **Http Response**
        """
        params = {
            'brief': brief
        }
        return self._send_request(http_methods.DELETE, '/v1/logo/lib/%s' % lib,
                                  params=params,
                                  config=config)

    @required(lib=(str, unicode), image=(str, unicode))
    def del_logo_image(self, lib, image, config=None):
        """
        :param lib: private logo lib
        :param image: private logo image
        :return: **Http Response**
        """
        params = {
            'image': image
        }
        return self._send_request(http_methods.DELETE, '/v1/logo/lib/%s' % lib,
                                  params=params,
                                  config=config)

    @required(lib=(str, unicode))
    def get_logo_lib(self, lib, config=None):
        """
        :param lib: private logo lib
        :return: **Http Response**
        """
        return self._send_request(http_methods.GET, '/v1/logo/lib/%s' % lib,
                                  config=config)

    @required(lib=(str, unicode), brief=(str, unicode))
    def get_logo_brief(self, lib, brief, config=None):
        """
        :param lib: private logo lib
        :param brief: private logo brief
        :return: **Http Response**
        """
        params = {
            'brief': brief
        }
        return self._send_request(http_methods.GET, '/v1/logo/lib/%s' % lib,
                                  params=params,
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
            http_method, path, body, headers, params)
