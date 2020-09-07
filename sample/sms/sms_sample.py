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
import logging
import os
import sys

import sms_sample_conf
import baidubce.services.sms.sms_client as sms
import baidubce.exception as ex

if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')

logging.basicConfig(level=logging.DEBUG, filename='./sms_sample.log', filemode='w')
LOG = logging.getLogger(__name__)
CONF = sms_sample_conf

if __name__ == '__main__':
    sms_client = sms.SmsClient(CONF.config)
    try:
        # send message
        LOG.debug('\n\n\nSample 1: Send Message\n\n\n')
        response = sms_client.send_message(signature_id='sms-sign-WWejWQ54455', template_id='sms-tmpl-wHoJXL09355',
                                           mobile='13800138000',
                                           content_var_dict={'content': "测试发送短信"})
        LOG.debug('\n%s', response)

        # create signature
        LOG.debug('\n\n\nSample 2: Create Signature\n\n\n')
        response = sms_client.create_signature(content="百度sms", content_type="Enterprise", description="用于测试的签名")
        signature_id = response.signature_id
        LOG.debug('\n%s', response)

        # update signature
        LOG.debug('\n\n\nSample 3: Update Signature\n\n\n')
        response = sms_client.update_signature(content="BaiduSms", content_type="MobileApp", country_type="GLOBAL",
                                               signature_id=signature_id)
        LOG.debug('\n%s', response)

        # get signature detail
        LOG.debug('\n\n\nSample 4: Get Signature Detail\n\n\n')
        response = sms_client.get_signature_detail(signature_id)
        LOG.debug('\n%s', response)

        # delete signature
        LOG.debug('\n\n\nSample 5: Delete Signature\n\n\n')
        response = sms_client.delete_signature(signature_id)
        LOG.debug('\n%s', response)

        # create template
        LOG.debug('\n\n\nSample 6: Create Template\n\n\n')
        response = sms_client.create_template(name="测试模板", content="模板样例${content}", sms_type="CommonNotice",
                                              description="用于测试的模板", country_type="DOMESTIC")
        template_id = response.template_id
        LOG.debug('\n%s', response)

        # update template
        LOG.debug('\n\n\nSample 7: Update Template\n\n\n')
        response = sms_client.update_template(template_id=template_id, name="测试模板2", content="模板样例${content}2",
                                              sms_type="CommonSale", country_type="GLOBAL")
        LOG.debug('\n%s', response)

        # get template detail
        LOG.debug('\n\n\nSample 8: Get Template Detail\n\n\n')
        response = sms_client.get_template_detail(template_id)
        LOG.debug('\n%s', response)

        # delete template
        LOG.debug('\n\n\nSample 9: Delete Template\n\n\n')
        response = sms_client.delete_template(template_id)
        LOG.debug('\n%s', response)

        # query quota rate
        LOG.debug('\n\n\nSample 10: Query Quota Rate\n\n\n')
        response = sms_client.query_quota_rate()
        LOG.debug('\n%s', response)

        # update quota rate
        LOG.debug('\n\n\nSample 11: Update Quota Rate\n\n\n')
        response = sms_client.update_quota_rate(quota_per_day=100, quota_per_month=100,
                                                rate_limit_per_mobile_per_sign_by_minute=0,
                                                rate_limit_per_mobile_per_sign_by_hour=0,
                                                rate_limit_per_mobile_per_sign_by_day=0)
        LOG.debug('\n%s', response)

    except ex.BceHttpClientError as e:
        if isinstance(e.last_error, ex.BceServerError):
            LOG.error('send request failed. Response %s, code: %s, request_id: %s'
                      % (e.last_error.status_code, e.last_error.code, e.last_error.request_id))
        else:
            LOG.error('send request failed. Unknown exception: %s' % e)
