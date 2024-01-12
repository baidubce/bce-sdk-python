#! usr/bin/python
# -*-coding:utf-8 -*-
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
This module defines RdsParameterManager interface,
"""

import json

from baidubce.utils import required
from baidubce.http import http_methods
from baidubce.services.rds import rds_http
from baidubce.services.rds.models import rds_parameter_model
from baidubce.services.rds.custom.requestparam import rds_request_param_object as request_param


class RdsParameterManager(rds_http.HttpRequest):
    """
     this is RdsParameterManager openApi interface
    :param rds_http.HttpRequest:
    """

    def __init__(self, config):
        """
        :param config:
        :type config: baidubce.BceClientConfiguration
        """

        rds_http.HttpRequest.__init__(self, config)

    @required(instance_id=str)
    def parameter_list(self, instance_id, keyword=None, config=None):
        """
         Gets a list of parameters for the specified instance

        :param instance_id:
            the specified instance id
        :type instance_id: str

        :param keyword:
            the keyword of parameter
        :type keyword: str or None

        :param config: config
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        return rds_parameter_model.ParameterList(
            self._send_request(http_method=http_methods.GET,
                               function_name='instance',
                               key=instance_id + '/parameter',
                               params={'keyword': keyword},
                               config=config,
                               api_version=1))

    @required(instance_id=(str), e_tag=(str), effective_time=(str), parameters=(list))
    def modify_config_parameter(self, instance_id, e_tag, effective_time, parameters,
                                config=None):
        """
         Modifying config parameters for the specified instance

        :param instance_id:
            The specified instance id
        :type instance_id: str

        :param e_tag:
            The new version, for example, v1,
            is obtained from the details list
        :type e_tag: str

        :param effective_time:
            Actual validity mode: immediate or
            maintenance time (timewindow)
        :type effective_time: str

        :param parameters:
            Parameter list to be modified
        :type parameters: list

        :param config: config
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        header = {b"x-bce-if-match": e_tag}
        data = {
            "effectiveTime": effective_time,
            "parameters": parameters
        }

        return self._send_request(http_method=http_methods.PUT,
                                  function_name='instance',
                                  key=instance_id + '/parameter',
                                  body=json.dumps(data, cls=request_param.JsonWrapper),
                                  headers=header,
                                  config=config,
                                  api_version=1)

    @required(instance_id=(str))
    def query_modify_parameter_history_List(self, instance_id, config=None):
        """
         query modify parameter history list

        :param instance_id:
            The specified instance id
        :type instance_id: str

        :param config: config
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        return rds_parameter_model.ParameterModifyHistoryList(
            self._send_request(http_method=http_methods.GET,
                               function_name='instance',
                               key=instance_id + '/parameter/history',
                               config=config,
                               api_version=1))

    def query_parameter_template_list(self, page_no=None, page_size=None, template_type=None,
                                      db_type=None, db_version=None, config=None):
        """
         query parameter template

        :param page_no:
            The current page number,default is 1
        :type page_no: int

        :param page_size:
            The number of records per page,default is 10
        :type page_no: int

        :param template_type:
            The template type can be user or system.
            The default value is user. user: Returns
            a list of custom parameters. system:
            Returns the system parameter list.
        :type template_type: string

        :param db_type:
            Tthe Database type
        :type db_type: string

        :param db_version:
            The Database version
        :type db_version: string

        :param config:
        :type config: baidubce.BceClientConfiguration
        :return:
        """

        params = {}

        if page_no is not None:
            params['pageNo'] = page_no
        if page_size is not None:
            params['pageSize'] = page_size
        if template_type is not None:
            params['type'] = template_type
        if db_type is not None:
            params['dbType'] = db_type
        if db_version is not None:
            params['dbVersion'] = db_version

        return rds_parameter_model.ParameterTempList(
            self._send_request(http_method=http_methods.GET,
                               function_name='instance',
                               key='/paraTemplate',
                               params=params,
                               config=config,
                               api_version=1))

    @required(template_id=(str))
    def query_parameter_template_detail(self, template_id, config=None):
        """
         query parameter template detail

        :param template_id:
            The id of parameter template
        :type template_id: str

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        return self._send_request(http_method=http_methods.GET,
                                  function_name='instance',
                                  key='/paraTemplate/template/detail/' + template_id,
                                  config=config,
                                  api_version=1)

    @required(template_id=(str), name=(str), desc=(str))
    def copy_parameter_template(self, template_id, name, desc, config=None):
        """
         copy parameter template

        :param name:
            The name of parameter template
        :type name: str

        :param desc:
            The description of parameter template
        :type desc: str

        :param template_id:
            The id of parameter template
        :type template_id: str

        :param config:
        :type config: baidubce.BceClientConfiguration
        :return:

        """

        data = {
            'name': name,
            'desc': desc,
            "templateId": template_id
        }
        return self._send_request(http_method=http_methods.POST,
                                  function_name='instance',
                                  key='/paraTemplate/duplicate/template',
                                  body=json.dumps(data),
                                  config=config,
                                  api_version=1)

    # template_apply
    @required(template_id=(str))
    def parameter_template_apply_history(self, template_id, page_no=None, page_size=None, config=None):
        """
        query parameter template apply history

        :param template_id:
            The id of parameter template
        :type template_id: str

        :param page_no:
            The current page number,default is 1
        :type page_no: int

        :param page_size:
            The number of records per page,default is 10
        :type page_size: int

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        params = {}
        if page_no is not None:
            params['pageNo'] = page_no
        if page_size is not None:
            params['pageSize'] = page_size

        return rds_parameter_model.TemplateApplyHistory(
            self._send_request(http_method=http_methods.GET,
                               function_name='instance/paraTemplate/apply',
                               key=template_id,
                               params=params,
                               config=config,
                               api_version=1))

    # template_apply_detail
    @required(apply_id=(str))
    def parameter_template_apply_detail(self, apply_id, config=None):
        """
         parameter template apply detail
        :param apply_id:
            The apply id
        :type apply_id: str

        :param config: config
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        return rds_parameter_model.TemplateApplyDetail(
            self._send_request(http_method=http_methods.GET,
                               function_name='instance',
                               key='/paraTemplate/apply/detail/' + apply_id,
                               config=config,
                               api_version=1))

    # create_parameter_template
    @required(name=(str), db_type=(str), db_version=(str), parameters=list)
    def create_parameter_template(self, name, db_type, db_version, parameters, desc, config=None):
        """
         create parameter template

        :param name:
            The create parameter template name
        :type name: str

        :param db_type:
            This parameter is the type of database, for example: mysql,
            sqlserver，postgresql
        :type db_type: str

        :param db_version:
            The version of database
        :type db_version: str

        :param parameters:
            The create a parameter list for the parameter template
        :type parameters: list

        :param desc:
           The description information of this template
         :type db_version: str or None
        :param config:
        :return:
        """
        if parameters is None:
            parameters = []

        paraTemplateModel = {"name": name,
                             "dbType": db_type,
                             "desc": desc,
                             "dbVersion": db_version,
                             "parameters": parameters
                             }

        return self._send_request(http_method=http_methods.POST,
                                  function_name='instance',
                                  key='/paraTemplate/add/template',
                                  body=json.dumps(paraTemplateModel, cls=request_param.JsonWrapper),
                                  config=config,
                                  api_version=1)

    # delete_parameter_template
    @required(template_id=(str))
    def delete_parameter_template(self, template_id, config=None):
        """
         Deletes the specified template

        :param template_id:
            The specified template id
        :type template_id: str

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        return self._send_request(http_method=http_methods.DELETE,
                                  function_name='instance',
                                  key='/paraTemplate/delete/template/' + template_id,
                                  config=config,
                                  api_version=1)

    # modify_parameter_template
    @required(template_id=(str))
    def modify_parameter_template(self, template_id, name=None, update_list=None, config=None):
        """
         modify parameter template

        :param template_id:
            The specified template id
        :type template_id: str

        :param name:
            The modify name of parameter template
        :type name: str

        :param update_list:
            The modify list of parameter template
        :type update_list: list

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:

        """

        params = {'name': None}
        if name is not None:
            params['name'] = name

        if update_list is None:
            update_list = []

        return self._send_request(http_method=http_methods.PUT,
                                  function_name='instance',
                                  key='/paraTemplate/update/template/' + template_id,
                                  params=params,
                                  body=json.dumps(update_list),
                                  config=config,
                                  api_version=1)

    @required(template_id=(str), apply_template=(dict))
    def parameter_template_apply(self, template_id, apply_template, config=None):
        """
         parameter template apply

        :param template_id:
            apply template id
        :type template_id: str

        :param apply_template:
            apply template object , the object is a dict
        :type apply_template: dict

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        return rds_parameter_model.ApplyTemplate(
            self._send_request(http_method=http_methods.POST,
                               function_name='instance',
                               key='/paraTemplate/template/apply/' + template_id,
                               body=json.dumps(apply_template, cls=request_param.JsonWrapper),
                               config=config,
                               api_version=1))

    # template_can_apply_instance_list
    @required(engine=(str), engine_version=(str))
    def parameter_template_can_apply_instance_list(self, engine, engine_version, config=None):
        """
         parameter template can apply instance list

        :param engine:
            The database engine
            For example mysql, sqlserver, postgresql
        :type engine: str

        :param engine_version:
            The database engine version
        :type engine: str

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        params = {"engine": engine, "engineVersion": engine_version}

        return self._send_request(http_method=http_methods.GET,
                                  function_name='instance',
                                  key='/paraTemplate/apply/instanceList',
                                  params=params,
                                  config=config,
                                  api_version=1)

    # template_compare
    @required(template_id=(str), instance_id=(str))
    def compare_parameter_template(self, template_id, instance_id=None, config=None):
        """
         compare parameter template

        :param template_id:
            id of the comparison template
        :type template_id: str

        :param instance_id:
            The Specifies the instance id
        :type instance_id: str

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        return self._send_request(http_method=http_methods.POST,
                                  function_name='instance',
                                  key='/paraTemplate/compare/' + template_id + "/" +
                                      instance_id,
                                  config=config,
                                  api_version=1)

    # database_parameter
    @required(db_type=(str), db_version=(str))
    def query_database_parameter(self, db_type, db_version, template_id=None, config=None):
        """
         Query the parameters of the instance database

        :param db_type:
            The database type, for example mysql,sqlserver,postgresql
        :type db_type: str

        :param db_version:
            The database version
        :type db_type: str

        :param template_id:
            The Specifies the instance id
        :type db_type: str

        :param config:
            The BceClientConfiguration
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        params = {'dbType': db_type, 'dbVersion': db_version}
        if template_id is not None:
            params['templateId'] = template_id
        return self._send_request(http_method=http_methods.GET,
                                  function_name='instance',
                                  key='/paraTemplate/list/datebaseParameters',
                                  params=params,
                                  config=config,
                                  api_version=1)
