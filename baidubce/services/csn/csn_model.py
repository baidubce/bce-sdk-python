# -*- coding: utf-8 -*-
"""
model for csn client
"""

# Copyright 2023 Baidu, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

class Billing(object):
    """
    billing information
    """

    def __init__(self, payment_timing=None, reservation_length=None, reservation_time_unit=None, billing_method=None):
        """
        :type payment_timing: string
        :param payment_timing: The pay time of the payment

        :type reservation_length: int
        :param reservation_length: purchase length

        :type reservation_time_unit: string
        :param reservation_time_unit: time unit of purchasing, default 'month'

        :type billing_method: string
        :param billing_method: The billing method of the payment, include ByTraffic, ByBandwidth,
                               PeakBandwidth_Percent_95, Enhanced_Percent_95
        """
        self.paymentTiming = payment_timing
        if billing_method:
            self.billingMethod = billing_method
        self.reservation = {
            "reservationLength": reservation_length,
            "reservationTimeUnit": reservation_time_unit
        }