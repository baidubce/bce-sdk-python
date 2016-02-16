# -*- coding: utf-8 -*- 
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
Samples for sms client.
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import logging
import os
import sys
import time

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')

import sms_sample_conf
from baidubce.services.sms import sms_client as sms
from baidubce import exception as ex


logging.basicConfig(level=logging.DEBUG, filename='./sms_sample.log', filemode='w')
LOG = logging.getLogger(__name__)
CONF = sms_sample_conf

tpl = 'smsTpl:e7476122a1c24e37b3b0de19d04ae900'
phone_numbers = ['13800138000']

if __name__ == '__main__':
    sms_client = sms.SmsClient(CONF.config)
    print '-------send a message--------'
    r = sms_client.send_message('{"code":"1234"}', phone_numbers, tpl)
    print r
    print '-------get message info------'
    message_id = r.message_id
    r = sms_client.get_message_info(message_id)
    print r
    print '-------get quota-------------'
    r = sms_client.get_quota()
    print r
