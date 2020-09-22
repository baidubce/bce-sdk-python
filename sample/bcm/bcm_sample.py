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
Samples for bcm client.
"""

# !/usr/bin/env python
# coding=utf-8
from baidubce.exception import BceHttpClientError, BceServerError
from baidubce.services.bcm.bcm_client import BcmClient
import bcm_sample_conf

if __name__ == '__main__':

    import logging

    logging.basicConfig(level=logging.DEBUG)
    __logger = logging.getLogger(__name__)

    user_id = "fakeuser1ba678asdf8as7df6a5sdf67"
    scope = "BCE_BCC"
    metric_name = "vCPUUsagePercent"
    dimensions = "InstanceId:i-xxx"
    statistics = "average,maximum,minimum"
    start_time = "2020-01-20T00:00:01Z"
    end_time = "2020-01-20T00:10:01Z"
    period_in_second = 60

    # create a bcm client
    bcm_client = BcmClient(bcm_sample_conf.config)

    # query metric data from bcm interface
    try:
        response = bcm_client.get_metric_data(user_id=user_id,
                                              scope=scope,
                                              metric_name=metric_name,
                                              dimensions=dimensions,
                                              statistics=statistics,
                                              start_time=start_time,
                                              end_time=end_time,
                                              period_in_second=period_in_second)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)
