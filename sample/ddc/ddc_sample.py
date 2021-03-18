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
Samples for ddc client.
"""

#!/usr/bin/env python
#coding=utf-8

import ddc_sample_conf
from baidubce.exception import BceHttpClientError
from baidubce.services.ddc.ddc_client import DdcClient

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    __logger = logging.getLogger(__name__)

    instance_id = 'ddc-mox9l5gy'
    db_name = 'xyltest'
    table_name = 'test02'
    log_type = 'slow'
    datetime = '2021-03-16'
    log_id = 'ddc-mox9l5gy_errlog.202103172000'
    download_valid_time_in_sec = '1000'

    ######################################################################################################
    #            ddc operation samples
    ######################################################################################################

    # create a ddc client
    ddc_client = DdcClient(ddc_sample_conf.config)

    # lazydrop create hard link
    try:
        response = ddc_client.lazydrop_create_hard_link(instance_id=instance_id,
                                                        db_name=db_name,
                                                        table_name=table_name)
        print response
    except BceHttpClientError as e:
        __logger.error('send request failed. Exception: %s' % e)

    # lazydrop delete hard link
    try:
        response = ddc_client.lazydrop_delete_hard_link(instance_id=instance_id,
                                                        db_name=db_name,
                                                        table_name=table_name)
        print response
    except BceHttpClientError as e:
        __logger.error('send request failed. Exception: %s' % e)

    # list log by instance id
    try:
        response = ddc_client.list_log_by_instance_id(instance_id=instance_id,
                                                      log_type=log_type,
                                                      datetime=datetime)
        print response
    except BceHttpClientError as e:
        __logger.error('send request failed. Exception: %s' % e)

    # get log by log id
    try:
        response = ddc_client.get_log_by_id(instance_id=instance_id,
                                            log_id=log_id,
                                            download_valid_time_in_sec=download_valid_time_in_sec)
        print response
    except BceHttpClientError as e:
        __logger.error('send request failed. Exception: %s' % e)







