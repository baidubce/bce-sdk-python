# -*- coding: UTF-8 -*-
# Copyright 2014 Baidu, Inc.
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
Samples for AIHC client.
"""

from baidubce.services.aihc.aihc_client import AIHCClient
import aihc_sample_conf

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    __logger = logging.getLogger(__name__)

    aihc_client = AIHCClient(aihc_sample_conf.config)
    client_token = "client_token"

    # create aijob
    resourcePoolId = 'cce-e0isdmib'
    # payload = {}
    # create_response = aihc_client.create_aijob(
    #     client_token=client_token,
    #     resourcePoolId=resourcePoolId,
    #     payload=payload
    # )
    # __logger.debug("[Sample AIHC] create_response:%s", create_response)

    # ai_jobs = aihc_client.get_all_aijobs(resourcePoolId=resourcePoolId)
    # __logger.debug("[Sample AIHC] ai_jobs:%s", ai_jobs)
    # print(ai_jobs)

    chain_job_config = "/Users/zhangsan/Documents/GitHub/bce-sdk-python/sample/aihc"
    aiak_job_config = "/Users/zhangsan/Documents/GitHub/bce-sdk-python/sample/aihc/aiak_pretrain_job_info.json"
    job_chain_info = aihc_client.generate_aiak_parameter(chain_job_config, aiak_job_config)
    print(job_chain_info)

    # job_info_config = "/Users/zhangsan/Documents/GitHub/bce-sdk-python/sample/aihc/sft-qwen2-72b-train-v1.json"
    # job_info = aihc_client.create_job_chain(job_info_config, 1)
