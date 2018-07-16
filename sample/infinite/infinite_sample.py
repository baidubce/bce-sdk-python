# -*- coding: utf-8 -*- 
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
Samples for infinite client.
"""
import sys
import logging
import os
import json
from IPython.display import Image

reload(sys)
sys.setdefaultencoding('utf-8')

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')

import infinite_sample_conf
from baidubce.services.infinite import infinite_client as infinite
from baidubce import exception as ex

logging.basicConfig(level=logging.DEBUG, filename='./infinite_sample.log', filemode='w')
LOG = logging.getLogger(__name__)
CONF = infinite_sample_conf

if __name__ == '__main__':
    infinite_client = infinite.InfiniteClient(CONF.config)
    try:
        LOG.debug('\n\n\nSample 1: Predict x-image data\n\n\n')
        file_name = '/tmp/test.jpg'
        # show image
        Image(file_name)
        with open(file_name, 'rb') as f:
            payload = f.read()
        response = infinite_client.predict(
                endpoint_name='ep2',
                body=payload,
                content_type='application/x-image')
        print response
        
        LOG.debug('\n\n\nSample 2: Debug\n\n\n')
        response = infinite_client.debug(
                endpoint_name='ep2',
                body=payload,
                content_type='application/x-image')
        print response
        
        LOG.debug('\n\n\nSample 3: Get endpoint list\n\n\n')
        response = infinite_client.get_endpoint_list()
        print response
        
        LOG.debug('\n\n\nSample 4: Get endpoint info\n\n\n')
        response = infinite_client.get_endpoint_info(endpoint_name='ep2')
        print response
        
    except ex.BceHttpClientError as e:
        if isinstance(e.last_error, ex.BceServerError):
            LOG.error('send request failed. Response %s, code: %s, msg: %s'
                      % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            LOG.error('send request failed. Unknown exception: %s' % e)
