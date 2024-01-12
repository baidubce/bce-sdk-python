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
 This module defines BackUp interface
"""

from baidubce.bce_response import BceResponse


class BackUpPolicy(object):
    """
     this is BackUpPolicy
    """


class BackUpDetail(BceResponse):
    """
     this is BackUpDetail response
     :param BceResponse
    """

    def __init__(self, bce_response):
        """
        :param bce_response:
        """

        self.backupId = bce_response.backup_id
        self.backupSize = bce_response.backup_size
        self.backupType = bce_response.backup_type
        self.backupStatus = bce_response.backup_status
        self.backupStartTime = bce_response.backup_start_time
        self.backupEndTime = bce_response.backup_end_time
        self.downloadUrl = bce_response.download_url
        self.downloadExpires = bce_response.download_expires


class BackUpList(BceResponse):
    """
     this is BackUpList response
     :param BceResponse
    """

    def __init__(self, bce_response):
        """
         @param bce_response:
        """

        self.backups = bce_response.backups
        self.isTruncated = bce_response.is_truncated
        self.backupType = bce_response.backup_type
        self.marker = bce_response.marker
        self.nextMarker = bce_response.next_marker


class BinlogList(BceResponse):
    """
     this is BceResponse response
     :param BceResponse
    """

    def __init__(self, bce_response):
        """
        :param bce_response:
        """

        self.binLogs = bce_response.binlogs


class BinlogDetail(BceResponse):
    """
     this is BinlogDetail response
     :param BceResponse
    """

    def __init__(self, bce_response):
        """
        :param bce_response:
        """

        self.binlog = bce_response.binlog
