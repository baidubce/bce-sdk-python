"""
This module is test models of media sdk..
Date:    2019/04/15 16:50:06
"""

import unittest
from baidubce.services.media import media_client
from baidubce.exception import BceHttpClientError
from baidubce.exception import BceServerError
from test_create_pipeline import TestCreatePipeline
from test_create_preset import TestCreatePreset
from test_create_watermark import TestCreateWatermark
from test_create_thumbnail import TestCreateThumbnail
from test_create_transcoding import TestCreateTranscoding

from test_list_pipeline import TestListPipeline
from test_list_preset import TestListPreset
from test_list_thumbnail import TestListThumbnail
from test_list_trandcoding import TestListTranscoding
from test_list_watermark import TestListWatermark

from test_query_pipeline import TestQueryPipeline
from test_query_preset import TestQueryPreset
from test_query_thumbnail import TestQueryThumbnail
from test_query_transcoding import TestQueryTranscoding
from test_query_watermark import TestQueryWatermark
from test_query_media_info import TestQueryMediaInfo

from test_delete_pipeline import TestDeletePipeline
from test_delete_preset import TestDeletePreset
from test_delete_watermark import TestDeleteWatermark


class TestDict(unittest.TestCase):
    """qa test main class

    use qa test .py files for test media client info
    when test, you should check pipe/preset/src etc
    name. if the input is right, the test case will
    run succeed.

    Attributes:
        no
    """


    def test_init(self):
        """qa test init"""
        creatPipe = TestCreatePipeline()

    def test_create_Pipeline(self):
        """qa test creat pipeline

        here you can use other TestCreatePipeline function
        such as test_create_pipeline_with_name_empty

        :return:
        """
        creatPipe = TestCreatePipeline()
        creatPipe.test_create_pipeline_normal()

    def test_create_Preset(self):
        """qa test creat preset
        :return:
        """
        creatPreset = TestCreatePreset()
        creatPreset.test_create_preset_with_clip_normal()

    def test_create_watermark(self):
        """qa test creat watermark
        :return:
        """
        creatWatermark = TestCreateWatermark()
        creatWatermark.test_create_watermark_normal()

    def test_create_thumbnai(self):
        """qa test creat thumbnai
        :return:
        """
        createThumbnail = TestCreateThumbnail()
        createThumbnail.test_create_thumbnail_normal()
        createThumbnail.test_create_thumbnail_with_key_is_chiness()

    def test_create_job(self):
        """qa test creat job
        :return:
        """
        createTranscode = TestCreateTranscoding()
        createTranscode.test_create_transcoding_normal()
        createTranscode.test_create_transcoding_file_name_chinese()
        createTranscode.test_create_transcoding_file_name_spacial_chars()

    def test_list_pipeline(self):
        """qa test list pipeline
        :return:
        """
        listPipe = TestListPipeline()
        listPipe.test_list_pipeline_add_one()

    def test_list_preset(self):
        """qa test list preset
        :return:
        """
        listPreset = TestListPreset()
        listPreset.test_list_preset_with_add_one()

    def test_list_watermark(self):
        """qa test list watermark
        :return:
        """
        listWatermar = TestListWatermark()
        listWatermar.test_list_watermark_add_one()

    def test_list_thumbnail(self):
        """qa test list thumnail
        :return:
        """
        listThumbnail = TestListThumbnail()
        listThumbnail.test_list_thumbnail_job_with_pipeline()

    def test_query_pipeline(self):
        """qa test query pipeline
        :return:
        """
        queryPipe = TestQueryPipeline()
        queryPipe.test_query_pipeline_exsit()

    def test_query_preset(self):
        """qa test query preset
        :return:
        """
        queryPreset = TestQueryPreset()
        queryPreset.test_query_preset_exist()

    def test_query_watermark(self):
        """qa test query watermark
        :return:
        """
        queryWatermar = TestQueryWatermark()
        queryWatermar.test_query_watermark_exist()

    def test_query_thumbnail(self):
        """qa test query thumbnail
        :return:
        """
        queryThumbnail = TestQueryThumbnail()
        queryThumbnail.test_query_thumbnail_job_exist()

    def test_query_mediainfo(self):
        """qa test query mediainfo
        :return:
        """
        queryMediainfo = TestQueryMediaInfo()
        queryMediainfo.test_query_media_info_english_name()

    def test_delete_pipeline(self):
        """qa test delete pipeline
        :return:
        """
        deletePipe = TestDeletePipeline()
        deletePipe.test_delete_pipeline_exist()

    def test_delete_preset(self):
        """qa test delete preset
        :return:
        """
        deletePreset = TestDeletePreset()
        deletePreset.test_delete_preset_exist()

    def test_delete_watermark(self):
        """qa test delete watermark
        :return:
        """
        deleteWatermark = TestDeleteWatermark()
        deleteWatermark.test_delete_watermark_exist()

if __name__ == '__main__':
    unittest.main()
