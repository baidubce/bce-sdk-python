# -*- coding: utf-8 -*-

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
This module provide ET status condition.
"""
from enum import Enum

class ETStatus(Enum):
    """
    ET status enum query condition.
    """
    ACKWAIT = b'ack-wait'
    ACCEPT = b'accept'
    REJECT = b'reject'
    BUILDING = b'building'
    PAYWAIT = b'pay-wait'
    ESTABLISHED = b'established'
    STOPPED = b'stopped'
    DELETED = b'deleted'
