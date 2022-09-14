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
    # video lib id
    video_lib_id = "test_video_lib_id"
    # image lib id
    image_lib_id = "test_image_lib_id"

    try:
        # create video lib
        params = {"scoreThreshold": 90, "description": "test lib"}
        create_video_lib_response = mms_client.create_video_lib(video_lib, params)
        LOG.debug('\n%s', create_video_lib_response)
        video_lib_id = create_video_lib_response.lib_id
        LOG.debug('\n%s', video_lib_id)

        # create image lib
        create_image_lib_response = mms_client.create_image_lib(image_lib, params)
        LOG.debug('\n%s', create_image_lib_response)
        image_lib_id = create_image_lib_response.lib_id

        video_lib_list = mms_client.list_lib({"type": "VIDEO"})
        LOG.debug('{\n%s', video_lib_list)

        image_lib_list = mms_client.list_lib({"type": "IMAGE"})
        LOG.debug('{\n%s', image_lib_list)

        video_media_list = mms_client.list_media({"type": "VIDEO", "id": video_lib_id})
        LOG.debug('{\n%s', video_media_list)

        image_media_list = mms_client.list_media({"type": "IMAGE", "id": image_lib_id})
        LOG.debug('{\n%s', image_media_list)

        # insert video to video lib
        response = mms_client.insert_video(video_lib, video_url)
        video_id = response.media_id
        LOG.debug('\n%s', response)

        # get insert video task result
        # response = mms_client.get_insert_video_task_result(video_lib, video_url)
        # LOG.debug('\n%s', response)

        # get insert video task result by id
        response = mms_client.get_insert_video_task_result_by_id(video_lib_id, video_id)
        LOG.debug('\n%s', response)

        # create search video by video task
        response = mms_client.create_search_video_by_video_task(video_lib, video_url)
        task_id = response.task_id
        LOG.debug('\n%s', response)

        # get search video by video task result
        # response = mms_client.get_search_video_by_video_task_result(video_lib, video_url)
        # LOG.debug('\n%s', response)

        # get search video by video task result by id
        response = mms_client.get_search_video_by_video_task_result_by_id(video_lib, task_id)
        LOG.debug('\n%s', response)

        # search video by image
        response = mms_client.search_video_by_image(video_lib, image_url)
        LOG.debug('\n%s', response)

        # delete video from lib
        # response = mms_client.delete_video(video_lib, video_url)
        # LOG.debug('\n%s', response)

        # delete video from lib by id
        response = mms_client.delete_video_by_id(video_lib_id, video_id)
        LOG.debug('\n%s', response)

        # insert image to image lib
        response = mms_client.insert_image(image_lib, image_url)
        image_id = response.media_id
        LOG.debug('\n%s', response)

        # search image by image
        response = mms_client.search_image_by_image(image_lib, image_url)
        LOG.debug('\n%s', response)

        # delete image from lib
        # response = mms_client.delete_image(image_lib, image_url)
        # LOG.debug('\n%s', response)

        # delete image from lib by id
        response = mms_client.delete_image_by_id(image_lib_id, image_id)
        LOG.debug('\n%s', response)

        # delete video lib
        mms_client.delete_video_lib(video_lib_id)

        # delete image lib
        mms_client.delete_image_lib(image_lib_id)
    except Exception as e:
        LOG.error('send request failed. Unknown exception: %s' % e)
