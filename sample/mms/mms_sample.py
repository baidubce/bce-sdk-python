# !/usr/bin/env python
# coding=utf-8
"""
Samples for mms client.
"""
import logging

from baidubce.services.mms.mms_client import MmsClient
import mms_sample_conf

'''
# if use python 2
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
'''

logging.basicConfig(level=logging.DEBUG,
                    filename='./mms_sample.log', filemode='w')
LOG = logging.getLogger(__name__)

if __name__ == "__main__":
    import logging

    # create a mms client
    mms_client = MmsClient(mms_sample_conf.config)

    video_url = "https://测试视频.mp4"
    image_url = "https://测试图片.jpg"

    # video lib
    video_lib = "test_video_lib"
    # image lib
    image_lib = "test_image_lib"

    try:
        # insert video to video lib
        response = mms_client.insert_video(video_lib, video_url)
        LOG.debug('\n%s', response)

        # get insert video task result
        response = mms_client.get_insert_video_task_result(
            video_lib, video_url)
        LOG.debug('\n%s', response)

        # create search video by video task
        response = mms_client.create_search_video_by_video_task(
            video_lib, video_url)
        LOG.debug('\n%s', response)

        # get search video by video task result
        response = mms_client.get_search_video_by_video_task_result(
            video_lib, video_url)
        LOG.debug('\n%s', response)

        # search video by image
        response = mms_client.search_video_by_image(video_lib, image_url)
        LOG.debug('\n%s', response)

        # delete video from lib
        response = mms_client.delete_video(video_lib, video_url)
        LOG.debug('\n%s', response)

        # insert image to image lib
        response = mms_client.insert_image(image_lib, image_url)
        LOG.debug('\n%s', response)

        # search image by image
        response = mms_client.search_image_by_image(image_lib, image_url)
        LOG.debug('\n%s', response)

        # delete image from lib
        response = mms_client.delete_image(image_lib, image_url)
        LOG.debug('\n%s', response)
    except Exception as e:
        LOG.error('send request failed. Unknown exception: %s' % e)
