# -*- coding: utf-8 -*
"""
Test models of MvsClient.
"""
import unittest
import coverage
import mvs_test_config
import mock
from baidubce.utils import dict_to_python_object

from baidubce.bce_response import BceResponse

from baidubce.exception import BceServerError

from baidubce.services.mvs import mvs_client


cov = coverage.coverage()
cov.start()

http_request = None


class TestMvsClient(unittest.TestCase):
    """
    TestMvsClient
    """

    def setUp(self):
        """
        set up
        """
        self.the_client = mvs_client.MvsClient(mvs_test_config.config)

    def test_insert_video(self):
        """
        A test case for insert_video.
        """
        # Set request param.
        video_lib = 'baiduyun_test'
        source = 'http://baidu.com/test.mp4'
        notification = 'baiduyun_test'
        description = 'for test'

        # Set mock.
        error_mock = BceServerError('No such lib=baiduyun_test, please create it first!')
        error_mock.request_id = 'e58131ed-a961-452b-b54d-7bdd24aacbb4'
        error_mock.code = 'VideoSearchExceptions.NoSuchLibException'
        error_mock.status_code = 400
        self.the_client._send_request = mock.Mock(return_value=error_mock)

        try:
            # Run.
            self.the_client.insert_video(video_lib, source, notification, description=description)
        except BceServerError as e:
            # Validate result.
            self.assertEqual(e.status_code, error_mock.status_code)
            self.assertEqual(e.code, error_mock.code)
            self.assertEqual(e.request_id, error_mock.request_id)

    def test_search_video_by_video(self):
        """
        A test case for search_video_by_video.
        """
        # Set request param.
        video_lib = 'baiduyun_test'
        source = 'http://baidu.com/test.mp4'
        notification = 'baiduyun_test'
        description = 'for test'

        # Set mock.
        self.the_client._send_request = mock.Mock(return_value=None)

        # Run.
        response = self.the_client.search_video_by_video(video_lib,
                                                         source,
                                                         notification,
                                                         description=description)

        # Validate result.
        self.assertEqual(response, None)

    def test_insert_image(self):
        """
        A test case for insert_image.
        """
        # Set request param.
        image_lib = 'baiduyun_test'
        source = 'http://baidu.com/test.jpg'
        description = 'for test'

        # Set mock.
        error = {'code': 'InvalidLibName',
                 'message': 'invalid libName'}
        headers = {'status': 'failed',
                   'source': source,
                   'lib': image_lib,
                   'description': description}
        response_mock = BceResponse()
        response_mock.set_metadata_from_headers(headers)
        response_mock.error = dict_to_python_object(error)
        self.the_client._send_request = mock.Mock(return_value=response_mock)

        # Run.
        response = self.the_client.insert_image(image_lib, source, description=description)

        # Validate result.
        self.assertEqual(response.status, response_mock.status)
        self.assertEqual(response.source, response_mock.source)
        self.assertEqual(response.lib, response_mock.lib)
        self.assertEqual(response.description, response_mock.description)
        self.assertEqual(response.error.code, response_mock.error.code)
        self.assertEqual(response.error.message, response_mock.error.message)

    def test_search_image_by_image(self):
        """
        A test case for search_image_by_image.
        """
        # Set request param.
        image_lib = 'baiduyun_test'
        source = 'http://baidu.com/test.jpg'
        description = 'for test'

        # Set mock.
        result_item = {'score': 99.9,
                        'source': source,
                        'description': 'test'}
        results = [dict_to_python_object(result_item)]
        headers = {'status': 'failed',
                   'source': source,
                   'lib': image_lib,
                   'description': description}
        response_mock = BceResponse()
        response_mock.set_metadata_from_headers(headers)
        response_mock.results = results
        self.the_client._send_request = mock.Mock(return_value=response_mock)

        # Run.
        response = self.the_client.search_image_by_image(image_lib, source, description=description)

        # Validate result.
        self.assertEqual(response.status, response_mock.status)
        self.assertEqual(response.source, response_mock.source)
        self.assertEqual(response.lib, response_mock.lib)
        self.assertEqual(response.description, response_mock.description)
        self.assertEqual(response.results[0].score, response_mock.results[0].score)
        self.assertEqual(response.results[0].source, response_mock.results[0].source)
        self.assertEqual(response.results[0].description, response_mock.results[0].description)


if __name__ == "__main__":
    unittest.main()
    cov.stop()
    cov.save()
    cov.html_report()
