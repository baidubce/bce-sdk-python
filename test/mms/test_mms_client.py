# -*- coding: utf-8 -*
"""
Test models of MmsClient.
"""
import unittest
import coverage
import mms_test_config
import mock
from baidubce.utils import dict_to_python_object
from baidubce.bce_response import BceResponse
from baidubce.exception import BceServerError
from baidubce.services.mms import mms_client

cov = coverage.coverage()
cov.start()


class TestMmsClient(unittest.TestCase):
    """
    TestMmsClient
    """

    def setUp(self):
        """
        set up
        """
        self.the_client = mms_client.MmsClient(mms_test_config.config)
        self.image_lib = "zhx_v_test"
        self.vedio_lib = "zhx_v_test"

    def test_create_video_lib(self):
        """
        A test case for create_video_lib.
        """
        # Set request param.
        video_lib = 'baiduyun_test'
        params = {'description': 'for test'}

        # Set mock.
        BceResponse.lib_id = 'test_video_lib_id'
        self.the_client._send_request = mock.Mock(return_value=BceResponse)

        try:
            # Run.
            response = self.the_client.create_video_lib(video_lib, params=params)
            self.assertEqual(response.lib_id, BceResponse.lib_id)
        except BceServerError as e:
            # Validate result.
            raise e

    def test_delete_video_lib(self):
        """
        A test case for delete_video_lib.
        """
        # Set request param.
        video_lib_id = 'lib_id'

        # Set mock.
        BceResponse.status = 'success'
        self.the_client._send_request = mock.Mock(return_value=BceResponse)

        try:
            # Run.
            response = self.the_client.delete_video_lib(video_lib_id)
            self.assertEqual(response.status, BceResponse.status)
        except BceServerError as e:
            # Validate result.
            raise e

    def test_create_image_lib(self):
        """
        A test case for create_image_lib.
        """
        # Set request param.
        image_lib = 'baiduyun_test'
        params = {'description': 'for test'}

        # Set mock.
        BceResponse.lib_id = 'test_image_lib_id'
        self.the_client._send_request = mock.Mock(return_value=BceResponse)

        try:
            # Run.
            response = self.the_client.create_image_lib(image_lib, params=params)
            self.assertEqual(response.lib_id, BceResponse.lib_id)
        except BceServerError as e:
            # Validate result.
            raise e

    def test_delete_image_lib(self):
        """
        A test case for delete_image_lib.
        """
        # Set request param.
        image_lib_id = 'lib_id'

        # Set mock.
        BceResponse.status = 'success'
        self.the_client._send_request = mock.Mock(return_value=BceResponse)

        try:
            # Run.
            response = self.the_client.delete_image_lib(image_lib_id)
            self.assertEqual(response.status, BceResponse.status)
        except BceServerError as e:
            # Validate result.
            raise e

    def test_list_lib(self):
        """
        A test case for list_lib.
        """

        # Set mock.
        BceResponse.totalCount = 0
        self.the_client._send_request = mock.Mock(return_value=BceResponse)

        try:
            # Run.
            response = self.the_client.list_lib({"type": "IMAGE"})
            self.assertEqual(response.totalCount, BceResponse.totalCount)
        except BceServerError as e:
            # Validate result.
            raise e

    def test_list_media(self):
        """
        A test case for list_media.
        """

        # Set mock.
        BceResponse.totalCount = 0
        self.the_client._send_request = mock.Mock(return_value=BceResponse)

        try:
            # Run.
            response = self.the_client.list_media({"type": "IMAGE", "id": "lib_id"})
            self.assertEqual(response.totalCount, BceResponse.totalCount)
        except BceServerError as e:
            # Validate result.
            raise e

    def test_insert_video(self):
        """
        A test case for insert_video.
        """
        # Set request param.
        video_lib = 'baiduyun_test'
        source = 'http://baidu.com/test.mp4'
        description = 'for test'
        notification = 'notification'

        # Set mock.
        error_mock = BceServerError(
            'No such lib=baiduyun_test, please create it first!')
        error_mock.request_id = 'e58131ed-a961-452b-b54d-7bdd24aacbb4'
        error_mock.code = 'VideoSearchExceptions.NoSuchLibException'
        error_mock.status_code = 400
        self.the_client._send_request = mock.Mock(return_value=error_mock)

        try:
            # Run.
            self.the_client.insert_video(
                video_lib, source, description=description, notification=notification)
        except BceServerError as e:
            # Validate result.
            self.assertEqual(e.status_code, error_mock.status_code)
            self.assertEqual(e.code, error_mock.code)
            self.assertEqual(e.request_id, error_mock.request_id)

    def test_get_insert_video_task_result_by_id(self):
        """
        A test case for get_insert_video_task_result_by_id.
        """
        # Set request param.
        video_lib_id = 'baiduyun_test_id'
        media_id = 'media_id'

        # Set mock.
        error_mock = BceServerError(
            'No such video=media_id, please create it first!')
        error_mock.request_id = 'e58131ed-a961-452b-b54d-7bdd24aacbb4'
        error_mock.code = 'MmsExceptions.NoSuchVideo'
        error_mock.status_code = 404
        self.the_client._send_request = mock.Mock(return_value=error_mock)

        try:
            # Run.
            self.the_client.get_insert_video_task_result_by_id(video_lib_id, media_id)
        except BceServerError as e:
            # Validate result.
            self.assertEqual(e.status_code, error_mock.status_code)
            self.assertEqual(e.code, error_mock.code)
            self.assertEqual(e.request_id, error_mock.request_id)


    def test_get_search_video_by_video_task_result_by_id(self):
        """
        A test case for get_search_video_by_video_task_result_by_id.
        """
        # Set request param.
        video_lib = 'baiduyun_test'
        task_id = 'task_id'

        # Set mock.
        error_mock = BceServerError(
            'No such task=task_id, please create it first!')
        error_mock.request_id = 'e58131ed-a961-452b-b54d-7bdd24aacbb4'
        error_mock.code = 'MmsExceptions.NoSuchSearchTask'
        error_mock.status_code = 404
        self.the_client._send_request = mock.Mock(return_value=error_mock)

        try:
            # Run.
            self.the_client.get_search_video_by_video_task_result_by_id(video_lib, task_id)
        except BceServerError as e:
            # Validate result.
            self.assertEqual(e.status_code, error_mock.status_code)
            self.assertEqual(e.code, error_mock.code)
            self.assertEqual(e.request_id, error_mock.request_id)


    def test_delete_video_by_id(self):
        """
        A test case for delete_video_by_id.
        """
        # Set request param.
        video_lib_id = 'baiduyun_test_id'
        media_id = 'media_id'

        # Set mock.
        error_mock = BceServerError(
            'No such video=media_id, please create it first!')
        error_mock.request_id = 'e58131ed-a961-452b-b54d-7bdd24aacbb4'
        error_mock.code = 'MmsExceptions.NoSuchVideo'
        error_mock.status_code = 404
        self.the_client._send_request = mock.Mock(return_value=error_mock)

        try:
            # Run.
            self.the_client.delete_video_by_id(video_lib_id, media_id)
        except BceServerError as e:
            # Validate result.
            self.assertEqual(e.status_code, error_mock.status_code)
            self.assertEqual(e.code, error_mock.code)
            self.assertEqual(e.request_id, error_mock.request_id)


    def test_delete_image_by_id(self):
        """
        A test case for delete_image_by_id.
        """
        # Set request param.
        image_lib_id = 'baiduyun_test_id'
        media_id = 'media_id'

        # Set mock.
        error_mock = BceServerError(
            'No such image=NoSuchImage, please create it first!')
        error_mock.request_id = 'e58131ed-a961-452b-b54d-7bdd24aacbb4'
        error_mock.code = 'MmsExceptions.NoSuchImage'
        error_mock.status_code = 404
        self.the_client._send_request = mock.Mock(return_value=error_mock)

        try:
            # Run.
            self.the_client.delete_image_by_id(image_lib_id, media_id)
        except BceServerError as e:
            # Validate result.
            self.assertEqual(e.status_code, error_mock.status_code)
            self.assertEqual(e.code, error_mock.code)
            self.assertEqual(e.request_id, error_mock.request_id)


if __name__ == "__main__":
    unittest.main()
    cov.stop()
    cov.save()
    cov.html_report()
