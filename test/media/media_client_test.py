"""
Test models of BOS.
"""

import os
import sys
import random
import unittest
import httplib
import StringIO
import json
import socket
import time
import coverage
import baidubce
import media_conf
from baidubce.auth import bce_v1_signer
from baidubce.auth import bce_credentials
from baidubce import utils
from baidubce.services.media import media_client
from baidubce.exception import BceHttpClientError
from baidubce.exception import BceServerError
from baidubce.exception import BceClientError
from baidubce.http import http_methods
from baidubce.http import handler
from baidubce.bce_response import BceResponse
from baidubce import protocol
from baidubce.utils import Expando
from baidubce.utils import required
from baidubce.http import bce_http_client
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.retry_policy import NoRetryPolicy
from baidubce.retry_policy import BackOffRetryPolicy

reload(sys)
sys.setdefaultencoding('utf8')

cov = coverage.coverage()
cov.start()

http_request = None

pipeline = "sunye" + str(int(time.time()))


class TestMediaClient(unittest.TestCase):
    """
    TestMediaClient
    """
    def setUp(self):
        """
        set up
        """
        self.the_client = media_client.MediaClient(media_conf.config)

    def tearDown(self):
        """
        tear down
        """
        pass


class TestMediaPreset(TestMediaClient):
    """
    TestMediaPreset
    """
    def test_create_preset(self):
        """
        A test case
        """
        err = None
        try:
            audio = dict()
            audio['bitRateInBps'] = 256000
            self.the_client.create_preset(pipeline, "mp4", audio=audio)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)

    def test_list_presets(self):
        """
        A test case
        """
        err = None
        try:
            print self.the_client.list_presets()
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)

    def test_get_preset(self):
        """
        A test case
        """
        time.sleep(20)
        err = None
        try:
            self.the_client.get_preset(pipeline)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)

    def test_delete_preset(self):
        """
        A test case
        """
        try:
            self.the_client.delete_preset("321123321123")
        except BceHttpClientError as e:
            assert True


class TestMediaPipeline(TestMediaClient):
    """
    TestMediaJob
    """
    def test_list_pipelines(self):
        """
        A test case
        """
        err = None
        try:
            result = self.the_client.list_pipelines()
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)

    def test_create_pipelines(self):
        """
        A test case
        """
        print pipeline
        err = None
        try:
            self.the_client.create_pipeline(pipeline, "jianbininput", "jianbinoutput")

        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)

    def test_get_pipeline(self):
        """
        A test case
        """
        err = None
        time.sleep(20)
        try:
            self.the_client.get_pipeline(pipeline)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)

    def test_delete_pipeline(self):
        """
        A test case
        """
        try:
            self.the_client.delete_pipeline("321123321123")
        except BceHttpClientError as e:
            assert True


class TestMediaJob(TestMediaClient):
    """
    TestMediaJob
    """
    def test_list_jobs(self):
        """
        A test case
        """
        err = None
        try:
            result = self.the_client.list_jobs(pipeline)
            self.the_client.list_jobs(pipeline)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)

        def test_create_job(self):
            """
            A test case
            """
            time.sleep(20)
            err = None
            try:
                self.the_client.create_job(pipeline, {'sourceKey': 'love.mkv'},
                                           {'targetKey': 'ml.mp4', 'presetName':
                                               "bce.video_mp4_1280x720_1728kbps"})

            except BceServerError as e:
                err = e
            finally:
                self.assertIsNone(err)


def run_test():
    """
    :return:
    """
    runner = unittest.TextTestRunner()
    runner.run(unittest.makeSuite(TestMediaPipeline))
    runner.run(unittest.makeSuite(TestMediaPreset))
    runner.run(unittest.makeSuite(TestMediaJob))


run_test()

result = self.the_client.list_pipelines()
for i in result.pipelines:
    if str(i.pipeline_name).__contains__("sunye"):
        self.the_client.delete_pipeline(str(i.pipeline_name))

cov.stop()
cov.save()
cov.html_report()
