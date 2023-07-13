# !/usr/bin/env python
# coding=UTF-8
#
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
"""
This module provides a api config list for ld.
"""

from baidubce.http import http_methods


ld_apis = {
    "add_record": {
        "method": http_methods.POST,
        "path": "/v1/privatezone/[zoneId]/record",
        "queries": {
            "client_token": None
        },
        "headers": {
        }
    },
    "bind_vpc": {
        "method": http_methods.PUT,
        "path": "/v1/privatezone/[zoneId]",
        "queries": {
            "bind": '',
            "client_token": None
        },
        "headers": {
        }
    },
    "create_private_zone": {
        "method": http_methods.POST,
        "path": "/v1/privatezone",
        "queries": {
            "client_token": None
        },
        "headers": {
        }
    },
    "delete_private_zone": {
        "method": http_methods.DELETE,
        "path": "/v1/privatezone/[zoneId]",
        "queries": {
            "client_token": None
        },
        "headers": {
        }
    },
    "delete_record": {
        "method": http_methods.DELETE,
        "path": "/v1/privatezone/record/[recordId]",
        "queries": {
            "client_token": None
        },
        "headers": {
        }
    },
    "disable_record": {
        "method": http_methods.PUT,
        "path": "/v1/privatezone/record/[recordId]",
        "queries": {
            "disable": '',
            "client_token": None
        },
        "headers": {
        }
    },
    "enable_record": {
        "method": http_methods.PUT,
        "path": "/v1/privatezone/record/[recordId]",
        "queries": {
            "enable": '',
            "client_token": None
        },
        "headers": {
        }
    },
    "get_private_zone": {
        "method": http_methods.GET,
        "path": "/v1/privatezone/[zoneId]",
        "queries": {
        },
        "headers": {
        }
    },
    "list_private_zone": {
        "method": http_methods.GET,
        "path": "/v1/privatezone",
        "queries": {
            "marker": None,
            "max_keys": None
        },
        "headers": {
        }
    },
    "list_record": {
        "method": http_methods.GET,
        "path": "/v1/privatezone/[zoneId]/record",
        "queries": {
        },
        "headers": {
        }
    },
    "unbind_vpc": {
        "method": http_methods.PUT,
        "path": "/v1/privatezone/[zoneId]",
        "queries": {
            "unbind": '',
            "client_token": None
        },
        "headers": {
        }
    },
    "update_record": {
        "method": http_methods.PUT,
        "path": "/v1/privatezone/record/[recordId]",
        "queries": {
            "client_token": None
        },
        "headers": {
        }
    }
}