# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
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
 This module defines Parameter model
"""

from baidubce.bce_response import BceResponse


class ParameterModel(object):
    """
     this is ParameterModel model is no uesd
    """


class ParameterList(BceResponse):
    """
     this is ParameterList response
     @param BceResponse
    """

    def __init__(self, bce_response):
        if (bce_response.etag is not None):
            self.etag = str(bce_response.etag).replace('u', "")
        self.parameters = bce_response.parameters


class ParameterModifyHistoryList(BceResponse):
    """
     this is ParameterModifyHistoryList response
     @param BceResponse
    """

    def __init__(self, bce_response):
        """
        @param bce_response:
        """

        self.parameters = bce_response.parameters


class ParameterTempList(BceResponse):
    """
     this is ParameterTempList response
     @param BceResponse
    """

    def __init__(self, bce_response):
        """
        @param bce_response:
        """

        self.list = bce_response.list
        self.page = bce_response.page
        self.perpage = bce_response.perpage
        self.total = bce_response.total


class TemplateApplyHistory(BceResponse):
    """
    this is TemplateApplyHistory response
    @param BceResponse
    """

    def __init__(self, bce_response):
        """
        @param bce_response:
        """

        self.message = bce_response.message
        self.success = bce_response.success
        self.result = bce_response.result


class TemplateApplyDetail(BceResponse):
    """
    this is TemplateApplyDetail response
    @param BceResponse
    """

    def __init__(self, bce_response):
        """
        @param bce_response:
        """

        self.message = bce_response.message
        self.success = bce_response.success
        self.result = bce_response.result


class ApplyTemplate(BceResponse):
    """
    this is ApplyTemplate response
    :param BceResponse
    """

    def __init__(self, bce_response):
        """
        :param bce_response:
        """

        self.message = bce_response.message
        self.success = bce_response.success
        self.status = bce_response.status
        self.result = bce_response.result
