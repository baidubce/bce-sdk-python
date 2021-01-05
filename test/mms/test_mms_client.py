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

    def test_insert_video(self):
        """
        A test case for insert_video.
        """
        # Set request param.
        video_lib = 'baiduyun_test'
        source = 'http://baidu.com/test.mp4'
        description = 'for test'

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
                video_lib, source, description=description)
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
