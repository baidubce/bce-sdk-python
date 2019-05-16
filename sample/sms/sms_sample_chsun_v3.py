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
Samples for sms client.
"""
import sys
import logging
import os

#imp.reload(sys)
#sys.setdefaultencoding("utf-8")

if sys.version_info[0] == 2 :
    reload(sys)
    sys.setdefaultencoding('utf-8')

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')

import sms_sample_conf_chsun
from baidubce.services.sms import sms_client as sms
from baidubce import exception as ex


logging.basicConfig(level=logging.DEBUG, filename='./sms_sample.log', filemode='w')
LOG = logging.getLogger(__name__)
CONF = sms_sample_conf_chsun

if __name__ == '__main__':
    sms_client = sms.SmsClient(CONF.config)
    try:
        LOG.debug('\n\n\nSample 8: Send Message 2\n\n\n')
        response = sms_client.send_message_2('y2W4LRun-9sMD-MeGd', 'smsTpl:78d20e6c-201c-4f97-b57b-240e9dc7d831',
                                             '13261559193', {'code': "测试发送短信使用csp-proxy"})
    except ex.BceHttpClientError as e:
        if isinstance(e.last_error, ex.BceServerError):
            LOG.error('send request failed. Response %s, code: %s, msg: %s'
                      % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            LOG.error('send request failed. Unknown exception: %s' % e)
