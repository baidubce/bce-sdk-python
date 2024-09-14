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
Samples for bcc client.
"""

# !/usr/bin/env python
# coding=utf-8

from baidubce.services.bcc import bcc_model
from baidubce.services.bcc.bcc_client import BccClient
from sample.bcc import bcc_sample_conf

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    __logger = logging.getLogger(__name__)
    bcc_client = BccClient(bcc_sample_conf.config)

    reserved_instance = bcc_model.ModifyReservedInstanceModel(reservedInstanceId='r-UBVQFB5b',
                                                              reservedInstanceName='rename-reservedInstanceName')

    reserved_instances_list = [reserved_instance]
    response = bcc_client.modify_reserved_instances(reserved_instances=reserved_instances_list)

    # 打印返回结果
    print(response)
