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
 This module defines ReadOnlyGroup model
"""

from baidubce.bce_response import BceResponse


class ReadOnlyGroupModel(object):
    """
     this is ReadOnlyGroupModel model is no uesd
    """


class ReadOnlyGroupList(BceResponse):
    """
     this is ReadOnlyGroupList response
     :param BceResponse
    """

    def __init__(self, bce_response):
        self.roGroupId = str(bce_response.ro_group_id)
        self.roGroupName = str(bce_response.ro_group_name)
        self.sourceAppId = str(bce_response.source_app_id)
        self.appAmount = int(bce_response.app_amount)
        self.vpcId = str(bce_response.vpc_id)
        self.subnetId = str(bce_response.subnet_id)
        self.enableDelayOff = str(bce_response.enable_delay_off)
        self.delayThreshold = int(bce_response.delay_threshold)
        self.leastAppAmount = int(bce_response.least_app_amount)
        self.balanceReload = bool(bce_response.balance_reload)
        self.bgwGroupExclusive = bool(bce_response.bgw_group_exclusive)
        self.bgwGroupId = str(bce_response.bgw_group_id)
        self.endpoint = str(bce_response.endpoint)


class ReadOnlyGroupDetail(ReadOnlyGroupList):
    """
     this is ReadOnlyGroupDetail response
     @param ReadOnlyGroupList
    """

    def __init__(self, bce_response):
        ReadOnlyGroupList.__init__(self, bce_response)
        self.status = str(bce_response.status)
        self.appList = bce_response.app_list
        self.region = str(bce_response.region)


class MasterInstanceAssociatedReadOnlyList(BceResponse):
    """
     this is MasterInstanceAssociatedReadOnlyList response
     @param BceResponse
    """

    def __init__(self, bce_response):
        self.roGroupList = bce_response.ro_group_list
