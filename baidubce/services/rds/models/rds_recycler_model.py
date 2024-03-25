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
 This module defines recycler model
"""

from baidubce.bce_response import BceResponse


class RecyclerModel(object):
    """
    this is RecyclerModel no used
    """


class RecyclerList(BceResponse):
    """
    List RecyclerList Response
    """

    def __init__(self, bce_response):
        super(RecyclerList, self).__init__()
        self.max_keys = bce_response.max_keys
        self.marker = str(bce_response.marker)
        self.next_marker = str(bce_response.next_marker)
        self.is_truncated = bce_response.is_truncated
        self.instances = bce_response.instances
