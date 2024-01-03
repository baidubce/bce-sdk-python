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
This module provides a api config list for csn.
"""

from baidubce.http import http_methods


csn_apis = {
    "attach_instance": {
        "method": http_methods.PUT,
        "path": "/v1/csn/[csnId]",
        "queries": {
        },
        "headers": {
        }
    },
    "bind_csn_bp": {
        "method": http_methods.PUT,
        "path": "/v1/csn/bp/[csnBpId]",
        "queries": {
        },
        "headers": {
        }
    },
    "create_association": {
        "method": http_methods.POST,
        "path": "/v1/csn/routeTable/[csnRtId]/association",
        "queries": {
        },
        "headers": {
        }
    },
    "create_csn": {
        "method": http_methods.POST,
        "path": "/v1/csn",
        "queries": {
            "client_token": None
        },
        "headers": {
        }
    },
    "create_csn_bp": {
        "method": http_methods.POST,
        "path": "/v1/csn/bp",
        "queries": {
            "client_token": None
        },
        "headers": {
        }
    },
    "create_csn_bp_limit": {
        "method": http_methods.POST,
        "path": "/v1/csn/bp/[csnBpId]/limit",
        "queries": {
        },
        "headers": {
        }
    },
    "create_propagation": {
        "method": http_methods.POST,
        "path": "/v1/csn/routeTable/[csnRtId]/propagation",
        "queries": {
            "client_token": None
        },
        "headers": {
        }
    },
    "create_route_rule": {
        "method": http_methods.POST,
        "path": "/v1/csn/routeTable/[csnRtId]/rule",
        "queries": {
            "client_token": None
        },
        "headers": {
        }
    },
    "delete_association": {
        "method": http_methods.DELETE,
        "path": "/v1/csn/routeTable/[csnRtId]/association/[attachId]",
        "queries": {
            "client_token": None
        },
        "headers": {
        }
    },
    "delete_csn": {
        "method": http_methods.DELETE,
        "path": "/v1/csn/[csnId]",
        "queries": {
            "client_token": None
        },
        "headers": {
        }
    },
    "delete_csn_bp": {
        "method": http_methods.DELETE,
        "path": "/v1/csn/bp/[csnBpId]",
        "queries": {
            "client_token": None
        },
        "headers": {
        }
    },
    "delete_csn_bp_limit": {
        "method": http_methods.POST,
        "path": "/v1/csn/bp/[csnBpId]/limit/delete",
        "queries": {
            "client_token": None
        },
        "headers": {
        }
    },
    "delete_propagation": {
        "method": http_methods.DELETE,
        "path": "/v1/csn/routeTable/[csnRtId]/propagation/[attachId]",
        "queries": {
            "client_token": None
        },
        "headers": {
        }
    },
    "delete_route_rule": {
        "method": http_methods.DELETE,
        "path": "/v1/csn/routeTable/[csnRtId]/rule/[csnRtRuleId]",
        "queries": {
            "client_token": None
        },
        "headers": {
        }
    },
    "detach_instance": {
        "method": http_methods.PUT,
        "path": "/v1/csn/[csnId]",
        "queries": {
        },
        "headers": {
        }
    },
    "get_csn": {
        "method": http_methods.GET,
        "path": "/v1/csn/[csnId]",
        "queries": {
        },
        "headers": {
        }
    },
    "get_csn_bp": {
        "method": http_methods.GET,
        "path": "/v1/csn/bp/[csnBpId]",
        "queries": {
        },
        "headers": {
        }
    },
    "list_association": {
        "method": http_methods.GET,
        "path": "/v1/csn/routeTable/[csnRtId]/association",
        "queries": {
        },
        "headers": {
        }
    },
    "list_csn": {
        "method": http_methods.GET,
        "path": "/v1/csn",
        "queries": {
            "marker": None,
            "max_keys": None
        },
        "headers": {
        }
    },
    "list_csn_bp": {
        "method": http_methods.GET,
        "path": "/v1/csn/bp",
        "queries": {
            "marker": None,
            "max_keys": None
        },
        "headers": {
        }
    },
    "list_csn_bp_limit": {
        "method": http_methods.GET,
        "path": "/v1/csn/bp/[csnBpId]/limit",
        "queries": {
        },
        "headers": {
        }
    },
    "list_csn_bp_limit_by_csn_id": {
        "method": http_methods.GET,
        "path": "/v1/csn/[csnId]/bp/limit",
        "queries": {
        },
        "headers": {
        }
    },
    "list_instance": {
        "method": http_methods.GET,
        "path": "/v1/csn/[csnId]/instance",
        "queries": {
            "marker": None,
            "max_keys": None
        },
        "headers": {
        }
    },
    "list_propagation": {
        "method": http_methods.GET,
        "path": "/v1/csn/routeTable/[csnRtId]/propagation",
        "queries": {
        },
        "headers": {
        }
    },
    "list_route_rule": {
        "method": http_methods.GET,
        "path": "/v1/csn/routeTable/[csnRtId]/rule",
        "queries": {
            "marker": None,
            "max_keys": None
        },
        "headers": {
        }
    },
    "list_route_table": {
        "method": http_methods.GET,
        "path": "/v1/csn/[csnId]/routeTable",
        "queries": {
            "marker": None,
            "max_keys": None
        },
        "headers": {
        }
    },
    "list_tgw": {
        "method": http_methods.GET,
        "path": "/v1/csn/[csnId]/tgw",
        "queries": {
            "marker": None,
            "max_keys": None
        },
        "headers": {
        }
    },
    "list_tgw_rule": {
        "method": http_methods.GET,
        "path": "/v1/csn/[csnId]/tgw/[tgwId]/rule",
        "queries": {
            "marker": None,
            "max_keys": None
        },
        "headers": {
        }
    },
    "resize_csn_bp": {
        "method": http_methods.PUT,
        "path": "/v1/csn/bp/[csnBpId]",
        "queries": {
            "client_token": None
        },
        "headers": {
        }
    },
    "unbind_csn_bp": {
        "method": http_methods.PUT,
        "path": "/v1/csn/bp/[csnBpId]",
        "queries": {
            "client_token": None
        },
        "headers": {
        }
    },
    "update_csn": {
        "method": http_methods.PUT,
        "path": "/v1/csn/[csnId]",
        "queries": {
            "client_token": None
        },
        "headers": {
        }
    },
    "update_csn_bp": {
        "method": http_methods.PUT,
        "path": "/v1/csn/bp/[csnBpId]",
        "queries": {
            "client_token": None
        },
        "headers": {
        }
    },
    "update_csn_bp_limit": {
        "method": http_methods.PUT,
        "path": "/v1/csn/bp/[csnBpId]/limit",
        "queries": {
            "client_token": None
        },
        "headers": {
        }
    },
    "update_tgw": {
        "method": http_methods.PUT,
        "path": "/v1/csn/[csnId]/tgw/[tgwId]",
        "queries": {
        },
        "headers": {
        }
    }
}