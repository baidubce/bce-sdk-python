"""
Test models of BOS.
"""

import time
import unittest

import coverage
import media_conf

from baidubce.exception import BceHttpClientError
from baidubce.exception import BceServerError
from baidubce.services.media import media_client

#from baidubce.retry_policy import NoRetryPolicy
#from baidubce.retry_policy import BackOffRetryPolicy
import sys
import imp

imp.reload(sys)
#sys.setdefaultencoding('utf8')

#sys.path.append("./qa_test")


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

    def test_update_preset(self):
        """
        A test case
        """
        err = None
        try:
            bit_rate_in_bps = 256000
            bit_rate_in_bps_for_update = 80000
            audio = dict()
            audio['bitRateInBps'] = bit_rate_in_bps
            preset_name = "test_for_update"
            preset = self.the_client.get_preset_for_update(preset_name)
            preset.audio.bitRateInBps = bit_rate_in_bps_for_update
            self.the_client.update_preset(preset_name, preset)
            preset = self.the_client.get_preset(preset_name)
            self.assertEqual(preset.audio.bit_rate_in_bps, bit_rate_in_bps_for_update)

            body = {"presetName": preset_name, "description": "", "container": "mp4", "transmux": False, "audio": {"bitRateInBps": bit_rate_in_bps}}
            self.the_client.update_preset(preset_name, body)
            preset = self.the_client.get_preset(preset_name)
            self.assertEqual(preset.audio.bit_rate_in_bps, bit_rate_in_bps)

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
            print(self.the_client.list_presets())
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
            resul = self.the_client.delete_preset("321123321123")
        except BceHttpClientError as e:
            assert True


class TestMediaPipeline(TestMediaClient):
    """
    TestMediaJob
    """

    def test_update_pipeline(self):
        """
        A test case
        """
        err = None
        try:
            notification = "test"
            pipeline_name = "pipelineyu4"
            my_pipeline = self.the_client.get_pipeline_for_update(pipeline_name)
            my_pipeline.config.notification = notification
            self.the_client.update_pipeline(pipeline_name, my_pipeline)
            my_pipeline = self.the_client.get_pipeline(pipeline_name)
            self.assertEqual(my_pipeline.config.notification, notification)

        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)

    def test_list_pipelines(self):
        """
        A test case
        """
        err = None
        try:
            self.the_client.list_pipelines()
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)

    def test_create_pipelines(self):
        """
        A test case
        """
        print(pipeline)
        err = None
        try:
            self.the_client.create_pipeline(pipeline, "testmctjjm", "testmctjjm")

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


class TestMediaNotification(TestMediaClient):
    """
    TestMediaNotification
    """
    def test_list_notifications(self):
        """
        A test case
        """
        err = None
        try:
            result = self.the_client.list_notifications()
            assert len(result.notifications) > 0
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)

    def test_create_notifications(self):
        """
        A test case
        """
        err = None
        try:
            self.the_client.create_notification("test_for_create", "http://bce.baidu.com")
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)

    def test_get_notification(self):
        """
        A test case
        """
        err = None
        time.sleep(20)
        try:
            name = "test"
            notification = self.the_client.get_notification(name)
            assert notification.name, name
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)

    def test_delete_notification(self):
        """
        A test case
        """
        err = None
        try:
            self.the_client.create_notification("test_fo_delete", "http://bce.baidu.com")
            self.the_client.delete_notification("test_fo_delete")
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertIsNone(err)


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
            self.the_client.create_job(pipeline, {'sourceKey': '10706_csdn.mp4'},
                                        {'targetKey': 'test-out-1.mp4', 'presetName':
                                        "bce.video_mp4_1280x720_1728kbps"})

        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)


class TestMediaEncryptionKey(TestMediaClient):
    """
        TestMediaEncryptionKey
    """

    def test_get_transcoding_encryption_key(self):
        """
        list first page jobs of every pipeline, query transcoding key of them
        """
        for pipeline in self.the_client.list_pipelines().pipelines:
            for job in self.the_client.list_jobs(str(pipeline.pipeline_name)).jobs:
                try:
                    key = self.the_client.get_transcoding_encryption_key(str(job.job_id)).encryption_key
                    print("AES key of job " + job.job_id + " is " + key)
                except BceHttpClientError as e:
                    if not isinstance(e.last_error, BceServerError):
                        raise e
                    if e.last_error.status_code == 404:
                        print("AES key of job " + job.job_id + " dose not exist!")
                    elif e.last_error.status_code == 400:
                        print("This server dose not support get AES key!")
                    else:
                        raise e


def run_test():
    """
    :return:
    """
    runner = unittest.TextTestRunner()
    runner.run(unittest.makeSuite(TestMediaPipeline))
    runner.run(unittest.makeSuite(TestMediaPreset))
    runner.run(unittest.makeSuite(TestMediaJob))
    runner.run(unittest.makeSuite(TestMediaEncryptionKey))

run_test()

'''

result = self.the_client.list_pipelines()
for i in result.pipelines:
    if str(i.pipeline_name).__contains__("sunye"):
        self.the_client.delete_pipeline(str(i.pipeline_name))
'''

cov.stop()
cov.save()
cov.html_report()
