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
 This module defines LogModel model
"""

from baidubce.bce_response import BceResponse


class LogModel(object):
    """
    this is LogModel no used
    """


class SlowLogDetail(BceResponse):
    """
     this is SlowLogDetail response
     @param BceResponse
    """

    def __init__(self, bce_response):
        """
        @param bce_response:
        """

        self.slowLogs = bce_response.slow_logs
        self.count = bce_response.count


class ErrorDetail(BceResponse):
    """
    this is ErrorDetail response
    @param BceResponse
    """

    def __init__(self, bce_response):
        """
        @param bce_response:
        """

        self.errorLogs = bce_response.error_logs
        self.count = bce_response.count


class SlowLogList(BceResponse):
    """
    this is SlowLogList response
    @param BceResponse
    """

    def __init__(self, bce_response):
        """
        @param bce_response:
        """

        self.slowlogs = bce_response.slowlogs


class ErrorLogList(BceResponse):
    """
    this is ErrorLogList response
     @param BceResponse
    """

    def __init__(self, bce_response):
        """
        @param bce_response:
        """

        self.errorlogs = bce_response.errorlogs


class DownLoadDetail(BceResponse):
    """
    this is DownLoadDetail response
     @param BceResponse
    """

    def __init__(self, bce_response):
        """
        @param bce_response:
        """

        self.url = bce_response.url
        self.downloadExpires = bce_response.download_expires
        self.dataBackupType = bce_response.data_backup_type
