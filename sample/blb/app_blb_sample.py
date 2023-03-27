# !/usr/bin/env python
# coding=utf-8
"""
Samples for app blb client.
"""

import app_blb_sample_conf
from baidubce.services.blb.app_blb_client import AppBlbClient

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    __logger = logging.getLogger(__name__)

    # create an app blb client
    app_blb_client = AppBlbClient(app_blb_sample_conf.config)

    # create app blb server group port
    app_blb_client.create_app_server_group_port(app_blb_sample_conf.blbId,
                                                app_blb_sample_conf.appServerGroupId, 53, 'UDP')

    # update app blb server group port
    app_blb_client.update_app_server_group_port(app_blb_sample_conf.blbId, app_blb_sample_conf.appServerGroupId,
                                                app_blb_sample_conf.portId, 10)

    # create an app blb http listener
    app_blb_client.create_app_http_listener(
        app_blb_sample_conf.blbId, app_blb_sample_conf.portId, 'LeastConnection', x_forwarded_for=True)

    # create an app blb https listener
    app_blb_client.create_app_https_listener(
        app_blb_sample_conf.blbId, app_blb_sample_conf.portId,
        'LeastConnection', app_blb_sample_conf.certIds, x_forwarded_for=True)

    # update an app blb http listener
    app_blb_client.update_app_http_listener(
        app_blb_sample_conf.blbId, app_blb_sample_conf.portId, x_forwarded_for=False)

    # update an app blb https listener
    app_blb_client.update_app_https_listener(
        app_blb_sample_conf.blbId, app_blb_sample_conf.portId, x_forwarded_for=False)