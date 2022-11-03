# !/usr/bin/env python
# coding=UTF-8
#
# Copyright 2022 Baidu, Inc.
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
This module provides a api config list for dns.
"""

from baidubce.http import http_methods


dns_apis = {
    "add_line_group": {
        "method": http_methods.POST,
        "path": "/v1/dns/customline",
        "queries": {
            "client_token": None
        },
        "headers": {
        }
    },
    "create_paid_zone": {
        "method": http_methods.POST,
        "path": "/v1/dns/zone/order",
        "queries": {
            "client_token": None
        },
        "headers": {
        }
    },
    "create_record": {
        "method": http_methods.POST,
        "path": "/v1/dns/zone/[zoneName]/record",
        "queries": {
            "client_token": None
        },
        "headers": {
        }
    },
    "create_zone": {
        "method": http_methods.POST,
        "path": "/v1/dns/zone",
        "queries": {
            "client_token": None
        },
        "headers": {
        }
    },
    "delete_line_group": {
        "method": http_methods.DELETE,
        "path": "/v1/dns/customline/[lineId]",
        "queries": {
            "client_token": None
        },
        "headers": {
        }
    },
    "delete_record": {
        "method": http_methods.DELETE,
        "path": "/v1/dns/zone/[zoneName]/record/[recordId]",
        "queries": {
            "client_token": None
        },
        "headers": {
        }
    },
    "delete_zone": {
        "method": http_methods.DELETE,
        "path": "/v1/dns/zone/[zoneName]",
        "queries": {
            "client_token": None
        },
        "headers": {
        }
    },
    "list_line_group": {
        "method": http_methods.GET,
        "path": "/v1/dns/customline",
        "queries": {
            "marker": None,
            "max_keys": None
        },
        "headers": {
        }
    },
    "list_record": {
        "method": http_methods.GET,
        "path": "/v1/dns/zone/[zoneName]/record",
        "queries": {
            "rr": None,
            "id": None,
            "marker": None,
            "max_keys": None
        },
        "headers": {
        }
    },
    "list_zone": {
        "method": http_methods.GET,
        "path": "/v1/dns/zone",
        "queries": {
            "name": None,
            "marker": None,
            "max_keys": None
        },
        "headers": {
        }
    },
    "renew_zone": {
        "method": http_methods.PUT,
        "path": "/v1/dns/zone/order/[name]",
        "queries": {
            "client_token": None,
            "purchaseReserved": ''
        },
        "headers": {
        }
    },
    "update_line_group": {
        "method": http_methods.PUT,
        "path": "/v1/dns/customline/[lineId]",
        "queries": {
            "client_token": None
        },
        "headers": {
        }
    },
    "update_record": {
        "method": http_methods.PUT,
        "path": "/v1/dns/zone/[zoneName]/record/[recordId]",
        "queries": {
            "client_token": None
        },
        "headers": {
        }
    },
    "update_record_disable": {
        "method": http_methods.PUT,
        "path": "/v1/dns/zone/[zoneName]/record/[recordId]",
        "queries": {
            "client_token": None,
            "disable": ''
        },
        "headers": {
        }
    },
    "update_record_enable": {
        "method": http_methods.PUT,
        "path": "/v1/dns/zone/[zoneName]/record/[recordId]",
        "queries": {
            "client_token": None,
            "enable": ''
        },
        "headers": {
        }
    },
    "upgrade_zone": {
        "method": http_methods.PUT,
        "path": "/v1/dns/zone/order",
        "queries": {
            "client_token": None,
            "upgradeToDiscount": ''
        },
        "headers": {
        }
    }
}