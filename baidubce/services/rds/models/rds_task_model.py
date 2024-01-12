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
 This module defines TaskModel model
"""

from baidubce.bce_response import BceResponse


class TaskModel(object):
    """
    this is TaskModel is no used
    """


class TaskResponse(BceResponse):
    """
    task response.
    """

    def __init__(self, bce_response):
        super(TaskResponse, self).__init__()
        self.tasks = bce_response.tasks
        self.count = bce_response.count
