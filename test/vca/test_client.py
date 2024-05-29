# -*- coding: utf-8 -*
"""
Test models of VCA.
"""

import unittest
import coverage
import vca_test_config
from baidubce.services.vca import vca_client


cov = coverage.coverage()
cov.start()

http_request = None


class TestVcaClient(unittest.TestCase):
    """
    TestVcaClient
    """

    def setUp(self):
        """
        set up
        """
        print(dir(vca_client))
        self.the_client = vca_client.VcaClient(vca_test_config.config)

    def tearDown(self):
        """
        tear down
        """
        pass


class TestMedia(TestVcaClient):
    """
    TestAnalyzeMediaJob
    """

    def test_put_image(self):
        """
        A test case
        """
        err = None
        try:
            print(self.the_client.put_image("bos://vca-test-bucket/image.jpg"))
        except Exception as e:
            err = e
        finally:
            self.assertIsNone(err)

    def test_put_media(self):
        """
        A test case
        """
        err = None
        try:
            print(self.the_client.put_media("bos://vca-test-bucket/video.mp4"))
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
            print(self.the_client.get_media("bos://vca-test-bucket/video.mp4"))
        except Exception as e:
            err = e
        finally:
            self.assertIsNone(err)

    def test_cancel(self):
        """
        A test case
        """
        err = None
        try:
            # send + cancel
            self.the_client.put_media("bos://vca-test-bucket/video.mp4")
            print(self.the_client.cancel("bos://vca-test-bucket/video.mp4"))
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


run_test()

cov.stop()
cov.save()
cov.html_report()
