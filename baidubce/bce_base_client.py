# Copyright 2014 Baidu, Inc.
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
This module provide base class for BCE service clients.
"""

import copy

import baidubce
from baidubce import bce_client_configuration


class BceBaseClient(object):
    """
    TODO: add docstring
    """
    def __init__(self, config, region_supported=True):
        """
        :param config: the client configuration. The constructor makes a copy of this parameter so
                        that it is safe to change the configuration after then.
        :type config: BceClientConfiguration

        :param region_supported: true if this client supports region.
        :type region_supported: bool
        """
        self.service_id = self._compute_service_id()
        self.region_supported = region_supported
        self.config = copy.deepcopy(bce_client_configuration.DEFAULT_CONFIG)
        if config is not None:
            self.config.merge_non_none_values(config)
        if self.config.endpoint is None:
            self.config.endpoint = self._compute_endpoint()

    def _compute_service_id(self):
        return self.__module__.split('.')[2]

    def _compute_endpoint(self):
        if self.config.endpoint:
            return self.config.endpoint
        if self.region_supported:
            return '%s://%s.%s.%s' % (
                self.config.protocol,
                self.service_id,
                self.config.region,
                baidubce.DEFAULT_SERVICE_DOMAIN)
        else:
            return '%s://%s.%s' % (
                self.config.protocol,
                self.service_id,
                baidubce.DEFAULT_SERVICE_DOMAIN)