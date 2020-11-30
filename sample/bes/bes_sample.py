# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
"""
Samples for bes client.
"""

# !/usr/bin/env python
# coding=utf-8

import sys

import bes_sample_conf

from baidubce.exception import BceHttpClientError
from baidubce.exception import BceServerError
from baidubce.services.bes.bes_client import BesClient
from baidubce.services.bes.bes_model import Billing
from baidubce.services.bes.bes_model import Module

PY2 = sys.version_info[0] == 2
if PY2:
    reload(sys)
    sys.setdefaultencoding('utf8')

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    __logger = logging.getLogger(__name__)

    name = 'test'
    password = '123456aA'
    modules = [Module(type='es_node', instance_num=1), Module(type='es_node', instance_num=1)]
    version = '6.5.3'
    is_old_package = 'false'
    available_zone = 'zoneA'
    security_group_id = '3742b538-039b-41fc-999b-b15d3bfb381b'
    subnet_uuid = '20d48ab8-22d4-4e13-a762-e806fb9a0e19'
    vpc_id = '0e4e00bc-4bf1-49bd-bdf6-854676922a1d'
    # prepay payment will not create cluster immediately
    # billing = Billing(payment='prepay', time=3)
    billing = Billing(payment_type='postpay', time=0)
    ######################################################################################################
    #            bes  operation samples
    ######################################################################################################

    # create a bes client
    bes_client = BesClient(bes_sample_conf.config)

    # create a cluster
    try:
        response = bes_client.create_cluster(name, password, modules, version, is_old_package, available_zone,
                                             security_group_id, subnet_uuid, vpc_id, billing)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list cluster
    try:
        response = bes_client.get_cluster_list(page_no=1, page_size=20)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)
