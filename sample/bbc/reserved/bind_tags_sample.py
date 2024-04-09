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
Samples for bbc client.
"""
# !/usr/bin/env python
# coding=utf-8
from baidubce.services.bbc import bbc_model
from baidubce.services.bbc.bbc_client import BbcClient
from sample.bbc import bbc_sample_conf

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    __logger = logging.getLogger(__name__)
    bbc_client = BbcClient(bbc_sample_conf.config)

    # 预留实例券ID，最多支持100个
    reserved_instance_ids = ['r-Qyycx1SX']
    instance_tag1 = bbc_model.TagModel(tagKey='TestKey02',
                                       tagValue='TestValue02')
    instance_tag2 = bbc_model.TagModel(tagKey='TestKey03',
                                       tagValue='TestValue03')
    # 待绑定tag列表
    instance_tags = [instance_tag1, instance_tag2]
    bbc_client.bind_reserved_instance_to_tags(reserved_instance_ids=reserved_instance_ids, tags=instance_tags)
