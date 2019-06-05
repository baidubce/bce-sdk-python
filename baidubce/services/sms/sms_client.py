#! usr/bin/python
# coding=utf-8

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
This module provides a client class for SMS.
"""

import copy
import logging
import json
import warnings

from baidubce import utils
from baidubce.auth import bce_v1_signer
from baidubce.bce_base_client import BceBaseClient
from baidubce.http import bce_http_client
from baidubce.http import http_headers
from baidubce.http import http_methods
from baidubce.utils import required
from baidubce.services import sms
import http.client
from baidubce.exception import BceClientError
from baidubce.exception import BceServerError
from baidubce.bce_client_configuration import BceClientConfiguration

_logger = logging.getLogger(__name__)


def _parse_result(http_response, response):
    if http_response.status / 100 == http.client.CONTINUE / 100:
        raise BceClientError('Can not handle 1xx http status code')
    bse = None
    body = http_response.read()
    if body:
        d = json.loads(body)

        if 'message' in d and 'code' in d and 'requestId' in d:
            r_code = d['code']
            # 1000 means success
            if r_code != '1000':
                bse = BceServerError(d['message'],
                                     code=d['code'],
                                     request_id=d['requestId'])
            else:
                response.__dict__.update(
                    json.loads(body, object_hook=utils.dict_to_python_object).__dict__)
                http_response.close()
                return True
        elif http_response.status / 100 == http.client.OK / 100:
            response.__dict__.update(
                json.loads(body, object_hook=utils.dict_to_python_object).__dict__)
            http_response.close()
            return True
    elif http_response.status / 100 == http.client.OK / 100:
        return True
    
    if bse is None:
        bse = BceServerError(http_response.reason, request_id=response.metadata.bce_request_id)
    bse.status_code = http_response.status
    raise bse


class SmsClient(BceBaseClient):
    """
    Sms sdk client
    """
    def __init__(self, config=None):
        if config is not None:
            self._check_config_type(config)
        BceBaseClient.__init__(self, config)
    
    @required(config=BceClientConfiguration)
    def _check_config_type(self, config):
        return True
    
    @required(template_id=(bytes, str),
              receiver_list=list,
              content_var_dict=dict)
    def send_message(self, template_id, receiver_list, content_var_dict, config=None):
        """
        send a short message to a group of users
        
        :param template_id: template id used to send this message        
        :type template_id: string or unicode
        
        :param receiver_list: receivers to which this message will be send
        :type receiver_list: list
        
        :param content_var_dict: variable values to be replaced
        :type content_var_dict: dict
        
        :param config: None
        :type config: BceClientConfiguration
        
        :return: message result as following format
            {
                "messageId": "123456789abefghiqwertioplkjhgfds",
                "sendStat": {
                                "sendCount":2,
                                "successCount":1,
                                "failList":["13800138001", "13800138000"]
                            }
            }

        :rtype: baidubce.bce_response.BceResponse
        """
        warnings.warn("send_message deprecated, use send_message_2 instead",
                      DeprecationWarning)

        data = {
                    'templateId': template_id,
                    'receiver': receiver_list,
                    'contentVar': json.dumps(content_var_dict)
               }
        return self._send_request(http_methods.POST, 'message',
                                  body=json.dumps(data), config=config)

    @required(invoke_id=(bytes, str),
              template_id=(bytes, str),
              phone_number=(bytes, str),
              content_var_dict=dict)
    def send_message_2(self, invoke_id, template_id, phone_number, content_var_dict, config=None):
        """
        send a short message to a group of users

        :param invoke_id: id of signature
        :type invoke_id: string or unicode

        :param template_id: template id used to send this message
        :type template_id: string or unicode

        :param phone_number: phone number to receive this message
        :type phone_number: string or unicode

        :param content_var_dict: variable values to be replaced
        :type content_var_dict: dict

        :param config: None
        :type config: BceClientConfiguration

        :return: message result as following format
            {
                "requestId": "f585d09c-7bd7-486d-8e30-529c0e69efe2",
                "code": "1000",
                "message": "成功"
            }

        :rtype: baidubce.bce_response.BceResponse
        """

        data = {
            'invokeId': invoke_id,
            'templateCode': template_id,
            'phoneNumber': phone_number,
            'contentVar': content_var_dict
        }

        return self._send_request(http_methods.POST, 'message',
                                  body=json.dumps(data), config=config,
                                  api_version=2)

    @required(message_id=(bytes, str))
    def query_message_detail(self, message_id, config=None):
        """
        Get the message detail.

        :param message_id: the id of message to be queried
        :type message_id: string or unicode
        
        :param config: None
        :type config: BceClientConfiguration

        :return: detailed message as following format
            {
                'messageId': '123456789abefghiqwertioplkjhgfds',
                'content': 'this is JDMALL, your code is 123456',
                'receiver': ['13800138000'],
                'sendTime': '2014-06-12T10:08:22Z'
            }
        :rtype: baidubce.bce_response.BceResponse
        """
        
        return self._send_request(http_methods.GET, 'message', message_id, config=config)

    @required(name=(bytes, str), content=(bytes, str),
              invoke_id=(bytes, str))
    def create_template(self, name, content, invoke_id, profile_id=None, config=None):
        """
        Create template with specific name and content

        :param name: the name of template
        :type name: string or unicode
        
        :param content: the content of template,such as 'this is ${APP}, your code is ${VID}'
        :type content: string or unicode

        :param invoke_id: id of signature
        :type invoke_id: string or unicode

        :param profile_id: id of scene type, it can be none for there's only one scene in signature
        :type profile_id: string or unicode
        
        :param config: None
        :type config: BceClientConfiguration
        
        :return: create result as following format
            {
                "requestId": "f585d09c-7bd7-486d-8e30-529c0e69efe2",
                "code": "1000",
                "message": "成功",
                "data": {
                   "templateId":"smsTpl:64820901-a9d3-40fe-ad3d"
                }
            }

        :rtype: baidubce.bce_response.BceResponse
        """
        data = {'invokeId': invoke_id,
                'name': name,
                'content': content}
        if profile_id:
            data['profileId'] = profile_id

        return self._send_request(http_methods.POST, 'applyTemplate',
                                  body=json.dumps(data), config=config,
                                  api_version=2)

    @required(template_id=(bytes, str))
    def delete_template(self, template_id, config=None):
        """
        delete an existing template by given id

        :param template_id: id of template to be deleted
        :type template_id: string or unicode
        
        :param config: None
        :type config: BceClientConfiguration
        
        :return: None
        """
        self._send_request(http_methods.DELETE, 'template', template_id, config=config)

    @required(template_id=(bytes, str))
    def get_template_detail(self, template_id, config=None):
        """
        get detailed information of template by id

        :param template_id: the template id to be queried
        :type template_id: string or unicode
        
        :param config: None
        :type config: BceClientConfiguration
        
        :return: detailed template  as following format
            {
                'templateId': 'smsTpl:6nHdNumZ4ZtGaKO',
                'name: 'verifyID',
                'content': 'this is ${APP}, your code is ${VID}',
                'status: 'VALID',
                'createTime': '2014-06-12T10:08:22Z',
                'updateTime': '2014-06-12T10:08:22Z'
            }
        :rtype: baidubce.bce_response.BceResponse
        """
        return self._send_request(http_methods.GET, 'template', template_id, config=config)

    def get_template_list(self, config=None):
        """
        query all templates
        
        :param config: None
        :type config: BceClientConfiguration

        :return: template list as following format
            {
                "templateList": {    
                    'templateId': 'smsTpl:6nHdNumZ4ZtGaKO',
                    'name: 'verifyID',
                    'content': 'this is ${APP}, your code is ${VID}',
                    'status: 'VALID',
                    'createTime': '2014-06-12T10:08:22Z',
                    'updateTime': '2014-06-12T10:08:22Z'
                },
                ...
            }
        :rtype: baidubce.bce_response.BceResponse
        """
        return self._send_request(http_methods.GET, 'template', config=config)

    def query_quota(self, config=None):
        """
        query quota information of user
        
        :param config: None
        :type config: BceClientConfiguration
        
        :return: quota information as following format
            {
                'maxSendPerDay': 10000,
                'maxReceivePerPhoneNumberDay': 10,
                'sentToday': 8000
            }
        :rtype: baidubce.bce_response.BceResponse
        """
        return self._send_request(http_methods.GET, 'quota', config=config)
    
    @required(receiver=(bytes, str))
    def stat_receiver(self, receiver, config=None):
        """
        query quota information of receiver
        
        :param receiver: receiver to be queried
        :type receiver: string or unicode
        
        :param config: None
        :type config: BceClientConfiguration
        
        :return: quota information as following format
            {
                'maxReceivePerPhoneNumberDay': 10,
                'receivedToday': 8
            }
        :rtype: baidubce.bce_response.BceResponse
        """
        return self._send_request(http_methods.GET, 'receiver', receiver, config=config)

    @staticmethod
    def _get_path(config, function_name=None, key=None):
        return utils.append_uri(sms.URL_PREFIX, function_name, key)

    @staticmethod
    def _get_path_v2(config, function_name=None, key=None):
        return utils.append_uri(sms.URL_PREFIX_V2, function_name, key)

    @staticmethod
    def _bce_sms_sign(credentials, http_method, path, headers, params,
                      timestamp=0, expiration_in_seconds=1800,
                      headers_to_sign=None):
        
        headers_to_sign_list = [b"host",
                                b"content-md5",
                                b"content-length",
                                b"content-type"]

        if headers_to_sign is None or len(headers_to_sign) == 0:
            headers_to_sign = []
            for k in headers:
                k_lower = k.strip().lower()
                if k_lower.startswith(http_headers.BCE_PREFIX) or k_lower in headers_to_sign_list:
                    headers_to_sign.append(k_lower)
            headers_to_sign.sort()
        else:
            for k in headers:
                k_lower = k.strip().lower()
                if k_lower.startswith(http_headers.BCE_PREFIX):
                    headers_to_sign.append(k_lower)
            headers_to_sign.sort()

        return bce_v1_signer.sign(credentials,
                                  http_method,
                                  path,
                                  headers,
                                  params,
                                  timestamp,
                                  expiration_in_seconds,
                                  headers_to_sign)

    def _merge_config(self, config):
        if config is None:
            return self.config
        else:
            self._check_config_type(config)
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    def _send_request(
            self, http_method, function_name=None, key=None,
            body=None, headers=None, params=None,
            config=None,
            body_parser=None,
            api_version=1):
        config = self._merge_config(config)
        path = {1: SmsClient._get_path,
                2: SmsClient._get_path_v2
                }[api_version](config, function_name, key)

        if body_parser is None:
            body_parser = _parse_result
        
        if headers is None:
            headers = {b'Accept': b'*/*', b'Content-Type': b'application/json;charset=utf-8'}

        return bce_http_client.send_request(
            config, SmsClient._bce_sms_sign, [body_parser],
            http_method, path, body, headers, params)
