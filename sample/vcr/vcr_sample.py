# !/usr/bin/env python
# coding=utf-8
"""
Samples for vcr client.
"""

import vcr_sample_conf
from baidubce.services.vcr.vcr_client import VcrClient

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    __logger = logging.getLogger(__name__)

    # create a vcr client
    vcr_client = VcrClient(vcr_sample_conf.config)

    # media check
    media_source = "media url"
    """
    vcr_client.put_media(media_source)
    """

    # get media check result
    """
    print(vcr_client.get_media(media_source))
    """

    # audio check
    audio_source = "audio url"
    """
    vcr_client.put_audio(audio_source)
    """
    # get audio check result
    """
    print(vcr_client.get_audio(audio_source))
    """

    # image sync check
    image_source = "image url"
    """
    print(vcr_client.put_image(image_source))
    """

    # image async check
    """
    vcr_client.put_image_async_check(image_source)
    """

    # get image async check result
    """
    print(vcr_client.get_image_async_check_result(image_source))
    """

    # text check
    """
    print(vcr_client.put_text("text content"))
    """

    # add face image
    """
    vcr_client.add_face_image(lib="lib name", brief="person name", image="face image url")
    """

    # list face brief images
    """
    print(vcr_client.get_face_brief(lib="lib name", brief="person name"))
    """

    # delete face image
    """
    vcr_client.del_face_image(lib="lib name", brief="person name", image="image url")
    """

    # list face brief
    """
    print(vcr_client.get_face_lib(lib="lib name"))
    """

    # delete face brief
    """
    vcr_client.del_face_brief(lib="lib name", brief="person name")
    """

    # add logo image
    """
    vcr_client.add_logo_image(lib="lib name", brief="logo name", image="logo image url")
    """

    # list logo brief images
    """
    print(vcr_client.get_logo_brief(lib="lib name", brief="logo name"))
    """

    # delete logo image
    """
    vcr_client.del_logo_image(lib="lib name", image="logo image url")
    """

    # list logo brief
    """
    print(vcr_client.get_logo_lib(lib="lib name"))
    """

    # delete logo brief
    """
    vcr_client.del_logo_brief(lib="lib name", brief="logo name")
    """

