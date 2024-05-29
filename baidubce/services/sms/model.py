#! usr/bin/python
# coding=utf-8

# Copyright 2014 Baidu, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the
# License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.


"""
This module defines some Response classes for BTS
"""
from baidubce.bce_response import BceResponse


class CreateSignatureResponse(BceResponse):
    """
    Create Signature Response
    """

    def __init__(self, bce_response):
        super(CreateSignatureResponse, self).__init__()
        self.signature_id = str(bce_response.signature_id)
        self.status = str(bce_response.status)
        self.metadata = bce_response.metadata


class GetSignatureResponse(BceResponse):
    """
    Get Signature Response
    """

    def __init__(self, bce_response):
        super(GetSignatureResponse, self).__init__()
        self.signature_id = str(bce_response.signature_id)
        self.user_id = str(bce_response.user_id)
        self.content = str(bce_response.content)
        self.country_type = str(bce_response.country_type)
        self.content_type = str(bce_response.content_type)
        self.review = str(bce_response.review)
        self.status = str(bce_response.status)
        self.metadata = bce_response.metadata


class CreateTemplateResponse(BceResponse):
    """
    Create Template Response
    """

    def __init__(self, bce_response):
        super(CreateTemplateResponse, self).__init__()
        self.template_id = str(bce_response.template_id)
        self.status = str(bce_response.status)
        self.metadata = bce_response.metadata


class GetTemplateResponse(BceResponse):
    """
    Get Template Response
    """

    def __init__(self, bce_response):
        super(GetTemplateResponse, self).__init__()
        self.template_id = str(bce_response.template_id)
        self.user_id = str(bce_response.user_id)
        self.name = str(bce_response.name)
        self.content = str(bce_response.content)
        self.sms_type = str(bce_response.sms_type)
        self.description = str(bce_response.description)
        self.review = str(bce_response.review)
        self.status = str(bce_response.status)
        self.country_type = str(bce_response.country_type)
        self.metadata = bce_response.metadata


class QueryQuotaResponse(BceResponse):
    """
    Query Quota Response
    """

    def __init__(self, bce_response):
        super(QueryQuotaResponse, self).__init__()
        self.quota_per_day = bce_response.quota_per_day
        self.quota_per_month = bce_response.quota_per_month
        self.quota_remain_today = bce_response.quota_remain_today
        self.quota_remain_this_month = bce_response.quota_remain_this_month
        self.apply_quota_per_day = bce_response.apply_quota_per_day
        self.apply_quota_per_month = bce_response.apply_quota_per_month
        self.apply_check_status = bce_response.apply_check_status
        self.check_reply = bce_response.check_reply
        self.rate_limit_per_mobile_per_sign_by_minute = bce_response.rate_limit_per_mobile_per_sign_by_minute
        self.rate_limit_per_mobile_per_sign_by_hour = bce_response.rate_limit_per_mobile_per_sign_by_hour
        self.rate_limit_per_mobile_per_sign_by_day = bce_response.reate_limit_per_mobile_per_sign_by_day
        self.rate_limit_white_list = bce_response.rate_limit_white_list
        self.metadata = bce_response.metadata


class GetMobileBlackResponse(BceResponse):
    """
    Get Mobile Black Response
    """

    def __init__(self, bce_response):
        super(GetMobileBlackResponse, self).__init__()
        self.total_count = bce_response.total_count
        self.page_no = bce_response.page_no
        self.page_size = bce_response.page_size
        self.black_lists = bce_response.blacklists
        self.metadata = bce_response.metadata


class ListStatisticsResponse(BceResponse):
    """
    Get Statistics Information Response as List
    """

    def __init__(self, bce_response):
        super(ListStatisticsResponse, self).__init__()
        self.statistics_results = list(map(self.__result_trans, bce_response.statistics_results))

    def __result_trans(self, statistics_result):
        res = {
            'datetime': statistics_result.datetime,
            'country_alpha2_code': statistics_result.country_alpha2_code,
            'submit_count': statistics_result.submit_count,
            'submit_long_count': statistics_result.submit_long_count,
            'response_success_count': statistics_result.response_success_count,
            'response_success_proportion': statistics_result.response_success_proportion,
            'deliver_success_count': statistics_result.deliver_success_count,
            'deliver_success_long_count': statistics_result.deliver_success_long_count,
            'deliver_success_proportion': statistics_result.deliver_success_proportion,
            'deliver_failure_count': statistics_result.deliver_failure_count,
            'deliver_failure_proportion': statistics_result.deliver_failure_proportion,
            'receipt_proportion': statistics_result.receipt_proportion,
            'unknown_count': statistics_result.unknown_count,
            'unknown_proportion': statistics_result.unknown_proportion,
            'response_timeout_count': statistics_result.response_timeout_count,
            'unknown_error_count': statistics_result.unknown_error_count,
            'not_exist_count': statistics_result.not_exist_count,
            'signature_or_template_count': statistics_result.signature_or_template_count,
            'abnormal_count': statistics_result.abnormal_count,
            'overclocking_count': statistics_result.overclocking_count,
            'other_error_count': statistics_result.other_error_count,
            'blacklist_count': statistics_result.blacklist_count,
            'route_error_count': statistics_result.route_error_count,
            'issue_failure_count': statistics_result.issue_failure_count,
            'parameter_error_count': statistics_result.parameter_error_count,
            'illegal_word_count': statistics_result.illegal_word_count,
            'anomaly_count': statistics_result.anomaly_count
        }
        return res

