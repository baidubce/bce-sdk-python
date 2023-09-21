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
This module provides a client class for OOS.
"""

import copy
import json
import uuid

from baidubce.auth import bce_v1_signer
from baidubce.http import handler, bce_http_client, http_methods

from baidubce import bce_base_client


class OosClient(bce_base_client.BceBaseClient):
    """
    OOS base sdk client
    """
    prefix = b'/api/logic/oos'

    headers = {
        b"x-bce-request-id": uuid.uuid4(),
        b"content-type": b"application/json;charset=utf-8"
    }

    def __init__(self, config=None):
        bce_base_client.BceBaseClient.__init__(self, config)

    def _merge_config(self, config=None):
        if config is None:
            return self.config
        else:
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    def _send_request(self, http_method, path,
                      body=None, headers=None, params=None,
                      config=None, body_parser=None):
        config = self._merge_config(config)
        if body_parser is None:
            body_parser = handler.parse_json

        return bce_http_client.send_request(
            config, bce_v1_signer.sign, [handler.parse_error, body_parser],
            http_method, OosClient.prefix + path, body, headers, params)

    def create_template(self, name, operators, description="", linear=True, config=None):
        """
        Create oos template.

        This site may help you: https://cloud.baidu.com/doc/OOS/s/lli1cjcjh

        :param name:
            Template name.
        :type name: string

        :param operators:
            Include template operators to execute.
        :type operators: OperatorModel array

        :param description:
            Template description.
        :type description: string

        :param linear:
            Operator execute linearly.
        :type linear: bool

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/v2/template'
        body = {
            "description": description,
            "name": name,
            "operators": operators,
            "linear": linear
        }
        return self._send_request(http_methods.POST, path, body=json.dumps(body),
                                  headers=OosClient.headers, config=config)

    def check_template(self, name, operators, description="", linear=True, config=None):
        """
        Check oos template.

        This site may help you: https://cloud.baidu.com/doc/OOS/s/lli1cjcjh

        :param name:
            Template name.
        :type name: string

        :param operators:
            Include template operators to execute.
        :type operators: OperatorModel array

        :param description:
            Template description.
        :type description: string

        :param linear:
            Operator execute linearly.
        :type linear: bool

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/v2/template/check'
        body = {
            "description": description,
            "name": name,
            "operators": operators,
            "linear": linear
        }
        return self._send_request(http_methods.POST, path, body=json.dumps(body),
                                  headers=OosClient.headers, config=config)

    def update_template(self, template_id, name, operators, description="", linear=True, config=None):
        """
        Update oos template.

        This site may help you: https://cloud.baidu.com/doc/OOS/s/lli1cjcjh

        :param template_id:
            Template id.
        :type template_id: string

        :param name:
            Template name.
        :type name: string

        :param operators:
            Include template operators to execute.
        :type operators: OperatorModel array

        :param description:
            Template description.
        :type description: string

        :param linear:
            Operator execute linearly.
        :type linear: bool

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/v2/template'
        body = {
            "id": template_id,
            "description": description,
            "name": name,
            "operators": operators,
            "linear": linear
        }
        return self._send_request(http_methods.PUT, path, body=json.dumps(body),
                                  headers=OosClient.headers, config=config)

    def delete_template(self, template_id, config=None):
        """
        Delete oos template by template id.

        This site may help you: https://cloud.baidu.com/doc/OOS/s/lli1cjcjh

        :param template_id:
            Template id.
        :type template_id: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/v2/template'
        params = {
            "id": template_id
        }
        return self._send_request(http_methods.DELETE, path, params=params, headers=OosClient.headers, config=config)

    def get_template_detail(self, name, config=None):
        """
        Get template detail by template name.

        This site may help you: https://cloud.baidu.com/doc/OOS/s/lli1cjcjh

        :param name:
            Template name.
        :type name: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/v2/template'
        params = {
            "name": name
        }
        return self._send_request(http_methods.GET, path, params=params, headers=OosClient.headers, config=config)

    def get_template_list(self, page_no, page_size, sort="createTime", ascending=False, config=None):
        """
        Get template list.

        This site may help you: https://cloud.baidu.com/doc/OOS/s/lli1cjcjh

        :param page_no:
            Page number.
        :type page_no: int

        :param page_size:
            Page size.
        :type page_size: int

        :param sort:
            Template list sort by.
        :type sort: string

        :param ascending:
            ascend or not.
        :type ascending: bool

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/v2/template/list'
        body = {
            "sort": sort,
            "ascending": ascending,
            "pageNo": page_no,
            "pageSize": page_size
        }
        return self._send_request(http_methods.POST, path, body=json.dumps(body),
                                  headers=OosClient.headers, config=config)

    def get_operator_list(self, page_no, page_size, config=None):
        """
        Get operator list.

        This site may help you: https://cloud.baidu.com/doc/OOS/s/Oli1pd1bq

        :param page_no:
            Page number.
        :type page_no: int

        :param page_size:
            Page size.
        :type page_size: int

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/v1/operator/list'
        body = {
            "pageNo": page_no,
            "pageSize": page_size
        }
        return self._send_request(http_methods.POST, path, body=json.dumps(body),
                                  headers=OosClient.headers, config=config)

    def create_execution(self, template, properties={}, description="", tags=[], config=None):
        """
        Create oos execution by template.

        This site may help you: https://cloud.baidu.com/doc/OOS/s/fli1q43ih

        :param template:
            Template to execute.
        :type template: TemplateModel

        :param properties:
            Template execute global parameters.
        :type properties: dict

        :param description:
            Template description.
        :type description: string

        :param tags:
            Execution binding tags.
        :type tags: TagModel array

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/v2/execution'
        body = {
            "template": template,
            "properties": properties,
            "description": description,
            "tags": tags
        }
        return self._send_request(http_methods.POST, path, body=json.dumps(body),
                                  headers=OosClient.headers, config=config)

    def get_execution_detail(self, execution_id, config=None):
        """
        Get execution detail by execution id.

        This site may help you: https://cloud.baidu.com/doc/OOS/s/fli1q43ih

        :param execution_id:
            Execution id.
        :type execution_id: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/v2/execution'
        params = {
            "id": execution_id
        }
        return self._send_request(http_methods.GET, path, params=params, headers=OosClient.headers, config=config)
