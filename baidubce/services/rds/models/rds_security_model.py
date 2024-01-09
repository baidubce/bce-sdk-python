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
 This module defines Security model
"""

from baidubce.bce_response import BceResponse


class SecurityModel(object):
    """
    this is SecurityModel is no used
    """


class WhiteList(BceResponse):
    """
     this is WhiteList response
    """

    def __init__(self, bce_response):
        """
        @param bce_response:
        """

        self.security_ips = bce_response.security_ips
        self.etag = bce_response.etag


class SslState(BceResponse):
    """
    this is SslState response
    @param BceResponse
    """

    def __init__(self, bce_response):
        """
        @param bce_response:
        """

        self.sslState = bce_response.ssl_state
