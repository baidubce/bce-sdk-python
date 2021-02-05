# !/usr/bin/env python
# coding=utf-8
"""
Samples for vca client.
"""

import vca_sample_conf
from baidubce.services.vca.vca_client import VcaClient

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    __logger = logging.getLogger(__name__)

    # create a vca client
    vca_client = VcaClient(vca_sample_conf.config)

    # media check
    media_source = "media url"
    """
    vca_client.put_media(media_source)
    """

    # get media check result
    """
    print(vca_client.get_media(media_source))
    """

    # get media subtask
    sub_task_type = "thumbnail"
    """
    print(vca_client.get_sub_task(media_source, sub_task_type))
    """