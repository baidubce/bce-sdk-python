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
 This module defines HotActiveInstanceGroupModel model
"""

from baidubce.bce_response import BceResponse


class HotActiveInstanceGroupModel(object):
    """
     this HotActiveInstanceGroupModel is model is no uesd
    """


class GroupCheckGtidResponse(BceResponse):
    """
    grop check Gtid response.
    """

    def __init__(self, bce_response):
        super(GroupCheckGtidResponse, self).__init__()
        self.result = bce_response.result


class ForceChangeResponse(BceResponse):
    """
    ForceChange response.
    """

    def __init__(self, bce_response):
        super(ForceChangeResponse, self).__init__()
        self.behindMaster = bce_response.behindMaster


class GroupResponse(BceResponse):
    """
    grop response.
    """

    def __init__(self, bce_response):
        super(GroupResponse, self).__init__()
        self.result = bce_response.result
        self.orders = bce_response.orders
        self.orderBy = bce_response.order_by
        self.order = bce_response.order
        self.pageNo = bce_response.page_no
        self.pageSize = bce_response.page_size
        self.totalCount = bce_response.total_count


class GroupDetailResponse(BceResponse):
    """
    grop detail response.
    """

    def __init__(self, bce_response):
        super(GroupDetailResponse, self).__init__()
        self.group = bce_response.group


class GroupCheckPingResponse(BceResponse):
    """
    grop CheckPing response.
    """

    def __init__(self, bce_response):
        super(GroupCheckPingResponse, self).__init__()
        self.result = bce_response.result


class GroupCheckDataResponse(BceResponse):
    """
    grop CheckData response.
    """

    def __init__(self, bce_response):
        super(GroupCheckDataResponse, self).__init__()
        self.result = bce_response.result
