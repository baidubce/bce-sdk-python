# Copyright (c) 2011 X.commerce, a business unit of eBay Inc.
# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# Copyright 2011 Piston Cloud Computing, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""
This module provides models for BBC-SDK.
"""


class Billing(object):
    """
	This class define billing.
	param: paymentTiming:
		The pay time of the payment,
		see more detail in https://bce.baidu.com/doc/BCC/API.html#Billing
	param: reservationLength:
		The duration to buy in specified time unit,
		available values are [1,2,3,4,5,6,7,8,9,12,24,36] now.
	param: reservationTimeUnit:
		The time unit to specify the duration ,only "Month" can be used now.
	"""

    def __init__(self, paymentTiming=None, reservationLength=1, reservationTimeUnit='Month'):
        if paymentTiming:
            self.paymentTiming = paymentTiming
        self.reservation = {
            'reservationLength': reservationLength,
            'reservationTimeUnit': reservationTimeUnit
        }


class TagModel(object):
    """
    TAGModel
    """

    def __init__(self, tagKey=None, tagValue=None):
        self.tagKey = tagKey
        self.tagValue = tagValue
