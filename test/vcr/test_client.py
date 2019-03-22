# -*- coding: utf-8 -*
"""
Test models of VCR.
"""

import unittest
import coverage
import vcr_test_config
from baidubce.services.vcr import vcr_client

cov = coverage.coverage()
cov.start()

http_request = None


class TestVcrClient(unittest.TestCase):
    """
    TestVcrClient
    """
    def setUp(self):
        """
        set up
        """
        self.the_client = vcr_client.VcrClient(vcr_test_config.config)

    def tearDown(self):
        """
        tear down
        """
        pass


class TestMedia(TestVcrClient):
    """
    TestCheckMediaJob
    """
    def test_put_media(self):
        """
        A test case
        """
        err = None
        try:
            print(self.the_client.put_media("vod://mda-hkyks1ybf3w2fxxb"))
        except Exception as e:
            err = e
        finally:
            self.assertIsNone(err)

    def test_get_media(self):
        """
        A test case
        """
        err = None
        try:
            print(self.the_client.get_media("vod://mda-hkyks1ybf3w2fxxb"))
        except Exception as e:
            err = e
        finally:
            self.assertIsNone(err)


class TestStream(TestVcrClient):
    """
    TestCheckStreamJob
    """
    def test_put_stream(self):
        """
        A test case
        """
        err = None
        try:
            print(self.the_client.put_stream("rtmp://domain/app/stream"))
        except Exception as e:
            err = e
        finally:
            self.assertIsNone(err)

    def test_get_stream(self):
        """
        A test case
        """
        err = None
        try:
            print(self.the_client.get_stream("rtmp://domain/app/stream"))
        except Exception as e:
            err = e
        finally:
            self.assertIsNone(err)


class TestImage(TestVcrClient):
    """
    TestCheckImageJob
    """
    def test_put_image(self):
        """
        A test case
        """
        err = None
        try:
            print(self.the_client.put_image("http://sdingbucket.bj.bcebos.com/vcr/test/ad/logo/anjuke2.jpeg"))
        except Exception as e:
            err = e
        finally:
            self.assertIsNone(err)


class TestText(TestVcrClient):
    """
    TestMediaJob
    """
    def test_put_text(self):
        """
        A test case
        """
        err = None
        try:
            print(self.the_client.put_text("习近平"))
        except Exception as e:
            err = e
        finally:
            self.assertIsNone(err)


def run_test():
    """
    :return:
    """
    runner = unittest.TextTestRunner()
    runner.run(unittest.makeSuite(TestMedia))
    runner.run(unittest.makeSuite(TestStream))
    runner.run(unittest.makeSuite(TestImage))
    runner.run(unittest.makeSuite(TestText))


run_test()

cov.stop()
cov.save()
cov.html_report()
