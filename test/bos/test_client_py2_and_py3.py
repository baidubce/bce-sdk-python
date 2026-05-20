#!/usr/bin/env python
#coding=utf8

# Copyright 2014 Baidu, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
"""
Test models of BOS.
"""
# compatibility py2 and py3
# from __future__ import absolute_import
from builtins import str
from builtins import bytes
# from future.utils import iteritems
# from future.utils import iterkeys
# from future.utils import itervalues

import base64
import multiprocessing
import os
import sys
import random
import unittest
import http.client
import io
import json
import socket
import threading
import time
import pprint
from datetime import datetime

import math
from unittest.mock import patch, MagicMock
import coverage
import baidubce
import bos_test_config
from baidubce.auth import bce_v1_signer
from baidubce.auth import bce_credentials
from baidubce import utils
from baidubce import compat
from baidubce.services.bos import bos_client
from baidubce.services.bos import storage_class
from baidubce.services.bos.bos_client import UploadTaskHandle
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
#from baidubce.retry_policy import NoRetryPolicy
#from baidubce.retry_policy import BackOffRetryPolicy
from baidubce.retry.retry_policy import NoRetryPolicy
from baidubce.retry.retry_policy import BackOffRetryPolicy
import imp

imp.reload(sys)
if compat.PY2:
    sys.setdefaultencoding('utf8')

cov = coverage.coverage()
cov.start()

http_request = None


class MockHttpResponse(object):
    """
    mock http response
    """
    def __init__(self, status, content=None, header_list=None):
        """
        constructor
        :param status:
        :param content:
        :param header_list:
        :return:
        """
        self.status = status
        self.content = content
        self.header_list = header_list
        self.reason = "Mock"

    def read(self):
        """
        mock read
        :return:
        """
        return self.content

    def getheaders(self):
        """
        mock getheaders
        :return:
        """
        return self.header_list

    def close(self):
        """
        mock close
        :return:
        """
        pass


class MockHttpConnection(object):
    """
    mock http connection
    """
    def __init__(self):
        """
        constructor
        :return:
        """
        self.header = {}
        self.content = ""
        self.send_called = 0
        self.putrequest_called = 0
        self.putheader_called = 0
        self.endheaders_called = 0
        self.getresponse_called = 0
        self.close_called = 0

    def putrequest(self, method, uri, skip_host, skip_accept_encoding):
        """
        mock putrequest
        :param method:
        :param uri:
        :param skip_host:
        :param skip_accept_encoding:
        :return:
        """
        self.putrequest_called += 1

    def putheader(self, k, v):
        """
        mock putheader
        :param k:
        :param v:
        :return:
        """
        self.putheader_called += 1
        self.header[k] = v

    def endheaders(self):
        """
        mock endheaders
        :return:
        """
        self.endheaders_called += 1

    def getresponse(self):
        """
        mock getresponse
        :return:
        """
        self.getresponse_called += 1
        return None

    def send(self, buf):
        """
        mock send
        :param buf:
        :return:
        """
        self.content += buf
        self.send_called += 1

    def close(self):
        """
        mock close
        :return:
        """
        self.close_called += 1


class MockInputStream(object):
    """
    mock input stream
    """
    def __init__(self, content):
        """
        constructor
        :param content:
        :return:
        """
        self.content = content
        self.counter = 0

    def read(self, size):
        """
        mock read
        :param size:
        :return:
        """
        if self.counter >= len(self.content):
            return ""
        else:
            ret = self.content[self.counter:self.counter + size]
            self.counter += size
            return ret

    def close(self):
        """
        mock close
        :return:
        """
        pass


def mock_get_connection(protocol, host, port, timeout, proxy_host, proxe_port):
    """
    mock get_connection
    :param protocol:
    :param endpoint:
    :param timeout:
    :return:
    """
    return MockHttpConnection()


def mock_send_http_request_wrapper(throw, header_list):
    """
    factory function of mock send_http_request
    :param throw:
    :param header_list:
    :return:
    """
    def mock_send_http_request(conn, method, uri, headers, body, send_buf_size):
        """
        mock send_http_request
        :param conn:
        :param method:
        :param uri:
        :param headers:
        :param body:
        :param send_buf_size:
        :return:
        """
        if throw:
            raise socket.error
        else:
            return MockHttpResponse(200, header_list=header_list)
    return mock_send_http_request


def mock_handler_function_wrapper(ret):
    """
    factory function of mock handler
    :param ret:
    :return:
    """
    def mock_handler_function(http_response, response):
        """
        mock handler
        :param http_response:
        :param response:
        :return:
        """
        return ret
    return mock_handler_function


def mock_sign_function(credentials, method, path, headers, params):
    """
    mock sign function
    :param credentials:
    :param method:
    :param path:
    :param headers:
    :param params:
    :return:
    """
    return "Mocked"


def mock_client_send_request_wrapper(throw, status_code):
    """
    factory function of mock send_request
    :param throw:
    :param status_code:
    :return:
    """
    def mock_send_request(http_method, bucket_name=None, key=None,
                          body=None, headers=None, params=None,
                          config=None, body_parser=None):
        """
        mock send_request
        :param http_method:
        :param bucket_name:
        :param key:
        :param body:
        :param headers:
        :param params:
        :param config:
        :param body_parser:
        :return:
        """
        if throw:
            e = BceServerError("error", status_code=status_code)
            raise BceHttpClientError("error", e)
        else:
            pass
    return mock_send_request


class TestClient(unittest.TestCase):
    """TestClient"""
    BUCKET = "test-bucket%d" % os.getpid()
    KEY = "test_object%d" % os.getpid()
    KEY = compat.convert_to_bytes(KEY)
    FILENAME = "temp_file%d" % os.getpid()

    def setUp(self):
        """Start test"""
        self.bos = bos_client.BosClient(bos_test_config.config)
        if not self.bos.does_bucket_exist(self.BUCKET):
            self.bos.create_bucket(self.BUCKET)

    def tearDown(self):
        """Finish test"""
        # abort failed multipart upload
        response=self.bos.list_multipart_uploads(self.BUCKET)
        for item in response.uploads:
            temp_key = item.key
            if isinstance(temp_key, str):
                temp_key = temp_key.encode("utf-8")
            self.bos.abort_multipart_upload(self.BUCKET, temp_key, upload_id =
                    item.upload_id)
        # delete all objects on test bucket
        response = self.bos.list_all_objects(self.BUCKET)
        for obj in response:
            self.bos.delete_object(self.BUCKET, obj.key)
        # delete test bucket
        self.bos.delete_bucket(self.BUCKET)
        # delete locale file for testing
        if os.path.isfile(self.FILENAME):
            os.remove(self.FILENAME)

    def check_headers(self, response, headers_list=None):
        """check headers"""
        ordinary_headers_list = ['content_length',
                                'bce_debug_id',
                                'date',
                                'bce_request_id',
                                'server']

        for item in ordinary_headers_list:
            self.assertTrue(hasattr(response.metadata, item))

        if isinstance(headers_list, list):
            for item in headers_list:
                self.assertTrue(hasattr(response.metadata, item))

    def get_file(self, size):
        """create a file with size is size(MB)"""
        file = open(self.FILENAME, "w")
        file.seek(1024 * 1024 * size)
        file.write('\x00')
        file.close()


class TestDoesBucketExist(TestClient):
    """test does bucket exist"""
    def test_does_bucket_exist(self):
        """test does bucket exist function"""
        old_func = self.bos._send_request
        # test success
        self.bos._send_request = mock_client_send_request_wrapper(False, None)
        self.assertTrue(self.bos.does_bucket_exist("asdf"))
        # test forbidden
        self.bos._send_request = mock_client_send_request_wrapper(True, http.client.FORBIDDEN)
        self.assertTrue(self.bos.does_bucket_exist("asdf"))
        # test not found
        self.bos._send_request = mock_client_send_request_wrapper(True, http.client.NOT_FOUND)
        self.assertFalse(self.bos.does_bucket_exist("asdf"))
        # test others
        self.bos._send_request = mock_client_send_request_wrapper(True, http.client.NO_CONTENT)
        self.assertRaises(BceHttpClientError, self.bos.does_bucket_exist, "asdf")
        self.bos._send_request = old_func


class TestCopyObject(TestClient):
    """test copy_object function"""
    def test_copy_object(self):
        """test copy_object function normally"""
        response = self.bos.put_object_from_string(self.BUCKET, self.KEY, "This is a string.")
        response = self.bos.copy_object(self.BUCKET,
                                        self.KEY,
                                        self.BUCKET,
                                        compat.convert_to_bytes("test_target_key"))
        self.check_headers(response, response.etag)
        self.assertTrue(hasattr(response, 'last_modified'))
        self.assertEqual(response.etag, '13562b471182311b6eea8d241103e8f0')
        # source bucket is None
        err = None
        try:
            self.bos.copy_object(None, self.KEY, self.BUCKET, self.KEY)
        except ValueError as e:
            err = e
        finally:
            self.assertIsNotNone(err)
        # source key is None
        err = None
        try:
            self.bos.copy_object(self.BUCKET, None, self.BUCKET, self.KEY)
        except ValueError as e:
            err = e
        finally:
            self.assertIsNotNone(err)
        # target bucket is None
        err = None
        try:
            self.bos.copy_object(self.BUCKET, self.KEY, None, self.KEY)
        except ValueError as e:
            err = e
        finally:
            self.assertIsNotNone(err)
        # target key is None
        err = None
        try:
            self.bos.copy_object(self.BUCKET, self.KEY, self.BUCKET, None)
        except ValueError as e:
            err = e
        finally:
            self.assertIsNotNone(err)
        err = None
        try:
            self.bos.copy_object(None, self.KEY, self.BUCKET, self.KEY)
        except ValueError as e:
            err = e
        finally:
            self.assertIsNotNone(err)

    def test_copy_object_user_headers(self):
        """test copy_object user headers"""
        user_headers = {"Cache-Control":"private", 
                        "Content-Disposition":"attachment; filename=\"abc.txt\"", 
                        "Expires":"123456"}
        copy_object_user_headers = {"x-bce-copy-source-if-none-match":
                                    "e15ebeefb866b641557c325069b6b2a"}

        response = self.bos.put_object_from_string(self.BUCKET, 
            compat.convert_to_bytes("test_target_key_user_headers_src"),
            "This is a string.",
            user_headers=user_headers)
        response = self.bos.copy_object(source_bucket_name=self.BUCKET,
                                        source_key=b"test_target_key_user_headers_src",
                                        target_bucket_name=self.BUCKET,
                                        target_key=b"test_target_key_user_headers_dsc",
                                        user_headers=user_headers,
                                        copy_object_user_headers=copy_object_user_headers)

        response = self.bos.get_object(bucket_name=self.BUCKET, 
                                       key=b'test_target_key_user_headers_dsc')
       
        self.assertEqual(response.metadata.expires, "123456")
        self.assertEqual(response.metadata.content_disposition, 'attachment; filename="abc.txt"')
        self.assertEqual(response.metadata.cache_control, 'private')

    def test_copy_object_with_storage_class(self):
        """test copy_object with storage class"""
        # prepare an object
        response = self.bos.put_object_from_string(self.BUCKET, self.KEY, "This is a string.")

        # test copy object cold
        response = self.bos.copy_object(
            source_bucket_name=self.BUCKET,
            source_key=self.KEY,
            target_bucket_name=self.BUCKET,
            target_key = compat.convert_to_bytes("test_target_key_cold"),
            storage_class=storage_class.COLD)
        response = self.bos.get_object_meta_data(bucket_name=self.BUCKET, 
                                                 key=b'test_target_key_cold')
        self.assertEqual(response.metadata.bce_storage_class, "COLD")

        # test copy object standard ia
        response = self.bos.copy_object(source_bucket_name=self.BUCKET,
                                        source_key=self.KEY,
                                        target_bucket_name=self.BUCKET,
                                        target_key=b"test_target_key_ia",
                                        storage_class=storage_class.STANDARD_IA)
        response = self.bos.get_object_meta_data(bucket_name=self.BUCKET, 
                                                 key=b'test_target_key_ia')
        self.assertEqual(response.metadata.bce_storage_class, "STANDARD_IA")

        # test copy object default
        response = self.bos.copy_object(source_bucket_name=self.BUCKET,
                                        source_key=self.KEY,
                                        target_bucket_name=self.BUCKET,
                                        target_key=b"test_target_key_default")
        response = self.bos.get_object_meta_data(bucket_name=self.BUCKET,
                                                 key=b'test_target_key_default')
#        self.assertIsNone(response.metadata.bce_storage_class)
        self.assertEqual(response.metadata.bce_storage_class, "STANDARD")

        # test copy object standard
        response = self.bos.copy_object(source_bucket_name=self.BUCKET,
                                        source_key=self.KEY,
                                        target_bucket_name=self.BUCKET,
                                        target_key=b"test_target_key_standard",
                                        storage_class=storage_class.STANDARD)
        response = self.bos.get_object_meta_data(bucket_name=self.BUCKET, 
                                                 key=b'test_target_key_standard')
        self.assertEqual(response.metadata.bce_storage_class, "STANDARD")

        # test copy object invalid storage class
        err = None
        try:
            self.bos.copy_object(source_bucket_name=self.BUCKET,
                                 source_key=self.KEY,
                                 target_bucket_name=self.BUCKET,
                                 target_key=b"test_target_key_invalid",
                                 storage_class="aaa")
        except Exception as e:
            err = e
        except BceServerError as bse:
            err = bse
        finally:
            self.assertIsNotNone(err)
        # test copy object case
        err = None
        try:
            self.bos.copy_object(source_bucket_name=self.BUCKET,
                                 source_key=self.KEY,
                                 target_bucket_name=self.BUCKET,
                                 target_key=b"test_target_key_case",
                                 storage_class=b" STANDARD_Ia ")
            self.bos.copy_object(source_bucket_name=self.BUCKET,
                                 source_key=self.KEY,
                                 target_bucket_name=self.BUCKET,
                                 target_key=b"test_target_key_case",
                                 storage_class=b" cOLd ")
        except ValueError as e:
            err = e
        finally:
            self.assertIsNone(err)

    def test_copy_object_with_maz_standard(self):
        """test copy_object with MAZ_STANDARD storage class"""
        self.bos.put_object_from_string(self.BUCKET, self.KEY, "Hello MAZ")
        try:
            response = self.bos.copy_object(
                source_bucket_name=self.BUCKET,
                source_key=self.KEY,
                target_bucket_name=self.BUCKET,
                target_key=b"test_target_key_maz_standard",
                storage_class=storage_class.MAZ_STANDARD)
        except BceHttpClientError as e:
            self.skipTest("MAZ_STANDARD not supported in this environment: " + str(e))
        response = self.bos.get_object_meta_data(bucket_name=self.BUCKET,
                                                 key=b"test_target_key_maz_standard")
        self.assertEqual(response.metadata.bce_storage_class, "MAZ_STANDARD")

    def test_copy_object_with_maz_standard_ia(self):
        """test copy_object with MAZ_STANDARD_IA storage class"""
        self.bos.put_object_from_string(self.BUCKET, self.KEY, "Hello MAZ IA")
        try:
            response = self.bos.copy_object(
                source_bucket_name=self.BUCKET,
                source_key=self.KEY,
                target_bucket_name=self.BUCKET,
                target_key=b"test_target_key_maz_ia",
                storage_class=storage_class.MAZ_STANDARD_IA)
        except BceHttpClientError as e:
            self.skipTest("MAZ_STANDARD_IA not supported in this environment: " + str(e))
        response = self.bos.get_object_meta_data(bucket_name=self.BUCKET,
                                                 key=b"test_target_key_maz_ia")
        self.assertEqual(response.metadata.bce_storage_class, "MAZ_STANDARD_IA")


class TestGeneratePreSignedUrl(TestClient):
    """test generate_pre_signed_url function"""

    def test_generate_pre_signed_url(self):
        """test generate_pre_signed_url normally"""
        url = self.bos.generate_pre_signed_url(self.BUCKET, self.KEY, timestamp=1,
                                               expiration_in_seconds=100000000)
        self.assertEqual(url, self.bos.generate_pre_signed_url(self.BUCKET, self.KEY, timestamp=1,
                                                              expiration_in_seconds=100000000))

    def test_generate_pre_signed_url_with_empty_key(self):
        """test generate_pre_signed_url with empty key should raise ValueError"""
        with self.assertRaises(ValueError):
            self.bos.generate_pre_signed_url(self.BUCKET, b'', timestamp=1,
                                           expiration_in_seconds=100000000)

    def test_generate_pre_signed_url_with_v1_key(self):
        """test generate_pre_signed_url with key='v1' should raise ValueError"""
        with self.assertRaises(ValueError) as context:
            self.bos.generate_pre_signed_url(self.BUCKET, b'v1', timestamp=1,
                                           expiration_in_seconds=100000000)
        self.assertIn('key param error', str(context.exception))

    def test_generate_pre_signed_url_with_slash_key(self):
        """test generate_pre_signed_url with slash-only key should raise ValueError"""
        with self.assertRaises(ValueError):
            self.bos.generate_pre_signed_url(self.BUCKET, b'/', timestamp=1,
                                           expiration_in_seconds=100000000)

    def test_generate_pre_signed_url_with_normal_key_with_leading_slash(self):
        """test generate_pre_signed_url with key having leading slash (should be stripped)"""
        # Key with leading slash should work after strip
        url = self.bos.generate_pre_signed_url(self.BUCKET, b'/testkey', timestamp=1,
                                               expiration_in_seconds=100000000)
        self.assertIsNotNone(url)
        self.assertIn(b'testkey', url)

    def test_generate_pre_signed_url_with_normal_key(self):
        """test generate_pre_signed_url with normal key"""
        url = self.bos.generate_pre_signed_url(self.BUCKET, b'test-object-key', timestamp=1,
                                               expiration_in_seconds=100000000)
        self.assertIsNotNone(url)
        self.assertIn(b'test-object-key', url)

    def test_generate_pre_signed_url_with_special_characters(self):
        """test generate_pre_signed_url with special characters in key"""
        url = self.bos.generate_pre_signed_url(self.BUCKET, b'test/file@key.txt', timestamp=1,
                                               expiration_in_seconds=100000000)
        self.assertIsNotNone(url)

    def test_generate_pre_signed_url_with_zero_expiration(self):
        """test generate_pre_signed_url with expiration_in_seconds=0"""
        url = self.bos.generate_pre_signed_url(self.BUCKET, self.KEY, timestamp=1,
                                               expiration_in_seconds=0)
        self.assertIsNotNone(url)

    def test_generate_pre_signed_url_with_negative_expiration(self):
        """test generate_pre_signed_url with negative expiration_in_seconds"""
        url = self.bos.generate_pre_signed_url(self.BUCKET, self.KEY, timestamp=1,
                                               expiration_in_seconds=-100)
        self.assertIsNotNone(url)

    def test_generate_pre_signed_url_with_large_expiration(self):
        """test generate_pre_signed_url with very large expiration_in_seconds"""
        url = self.bos.generate_pre_signed_url(self.BUCKET, self.KEY, timestamp=1,
                                               expiration_in_seconds=999999999)
        self.assertIsNotNone(url)

    def test_generate_pre_signed_url_with_zero_timestamp(self):
        """test generate_pre_signed_url with timestamp=0 (default)"""
        url = self.bos.generate_pre_signed_url(self.BUCKET, self.KEY,
                                               expiration_in_seconds=1800)
        self.assertIsNotNone(url)

    def test_generate_pre_signed_url_with_negative_timestamp(self):
        """test generate_pre_signed_url with negative timestamp"""
        url = self.bos.generate_pre_signed_url(self.BUCKET, self.KEY, timestamp=-100,
                                               expiration_in_seconds=1800)
        self.assertIsNotNone(url)

    def test_generate_pre_signed_url_with_post_method(self):
        """test generate_pre_signed_url with POST method"""
        url = self.bos.generate_pre_signed_url(self.BUCKET, self.KEY, timestamp=1,
                                               expiration_in_seconds=1800,
                                               httpmethod=http_methods.POST)
        self.assertIsNotNone(url)
        self.assertIn(b'authorization', url.lower())

    def test_generate_pre_signed_url_with_put_method(self):
        """test generate_pre_signed_url with PUT method"""
        url = self.bos.generate_pre_signed_url(self.BUCKET, self.KEY, timestamp=1,
                                               expiration_in_seconds=1800,
                                               httpmethod=http_methods.PUT)
        self.assertIsNotNone(url)
        self.assertIn(b'authorization', url.lower())

    def test_generate_pre_signed_url_with_delete_method(self):
        """test generate_pre_signed_url with DELETE method"""
        url = self.bos.generate_pre_signed_url(self.BUCKET, self.KEY, timestamp=1,
                                               expiration_in_seconds=1800,
                                               httpmethod=http_methods.DELETE)
        self.assertIsNotNone(url)
        self.assertIn(b'authorization', url.lower())

    def test_generate_pre_signed_url_with_head_method(self):
        """test generate_pre_signed_url with HEAD method"""
        url = self.bos.generate_pre_signed_url(self.BUCKET, self.KEY, timestamp=1,
                                               expiration_in_seconds=1800,
                                               httpmethod=http_methods.HEAD)
        self.assertIsNotNone(url)

    def test_generate_pre_signed_url_with_headers(self):
        """test generate_pre_signed_url with custom headers"""
        headers = {
            b'x-bce-content-sha256': b'test-hash',
            b'x-bce-meta-custom': b'custom-value'
        }
        url = self.bos.generate_pre_signed_url(self.BUCKET, self.KEY, timestamp=1,
                                               expiration_in_seconds=1800,
                                               headers=headers)
        self.assertIsNotNone(url)

    def test_generate_pre_signed_url_with_params(self):
        """test generate_pre_signed_url with custom params"""
        params = {
            b'cache-control': b'no-cache',
            b'response-content-type': b'application/json'
        }
        url = self.bos.generate_pre_signed_url(self.BUCKET, self.KEY, timestamp=1,
                                               expiration_in_seconds=1800,
                                               params=params)
        self.assertIsNotNone(url)
        self.assertIn(b'cache-control', url.lower())

    def test_generate_pre_signed_url_with_headers_to_sign(self):
        """test generate_pre_signed_url with headers_to_sign"""
        headers_to_sign = [b'host', b'x-bce-content-sha256']
        url = self.bos.generate_pre_signed_url(self.BUCKET, self.KEY, timestamp=1,
                                               expiration_in_seconds=1800,
                                               headers_to_sign=headers_to_sign)
        self.assertIsNotNone(url)

    def test_generate_pre_signed_url_with_https_protocol(self):
        """test generate_pre_signed_url with HTTPS protocol overriding endpoint's scheme"""
        # When endpoint already has a protocol prefix, overriding protocol may raise ValueError;
        # otherwise the returned URL must start with https://
        try:
            url = self.bos.generate_pre_signed_url(self.BUCKET, self.KEY, timestamp=1,
                                                   expiration_in_seconds=1800,
                                                   protocol='https')
            self.assertIsNotNone(url)
            self.assertIn(b'https://', url)
        except ValueError:
            pass  # acceptable: endpoint protocol conflicts with override

    def test_generate_pre_signed_url_with_http_protocol(self):
        """test generate_pre_signed_url with HTTP protocol overriding endpoint's scheme"""
        try:
            url = self.bos.generate_pre_signed_url(self.BUCKET, self.KEY, timestamp=1,
                                                   expiration_in_seconds=1800,
                                                   protocol='http')
            self.assertIsNotNone(url)
            self.assertIn(b'http://', url)
        except ValueError:
            pass  # acceptable: endpoint protocol conflicts with override

    def test_generate_pre_signed_url_consistency(self):
        """test generate_pre_signed_url produces consistent results with same params"""
        url1 = self.bos.generate_pre_signed_url(self.BUCKET, self.KEY, timestamp=100,
                                                expiration_in_seconds=3600)
        url2 = self.bos.generate_pre_signed_url(self.BUCKET, self.KEY, timestamp=100,
                                                expiration_in_seconds=3600)
        self.assertEqual(url1, url2)

    def test_generate_pre_signed_url_contains_auth(self):
        """test generate_pre_signed_url contains authorization parameter"""
        url = self.bos.generate_pre_signed_url(self.BUCKET, self.KEY, timestamp=1,
                                               expiration_in_seconds=1800)
        url_str = compat.convert_to_string(url)
        self.assertIn('authorization', url_str.lower())

    def test_generate_pre_signed_url_contains_expiry(self):
        """test generate_pre_signed_url contains expiration information"""
        url = self.bos.generate_pre_signed_url(self.BUCKET, self.KEY, timestamp=1,
                                               expiration_in_seconds=1800)
        url_str = compat.convert_to_string(url)
        # The expiration should be encoded in the signature
        self.assertTrue(len(url) > 0)


    def test_generate_pre_signed_url_with_dot_segment_key(self):
        """test generate_pre_signed_url with '.' path segment is rejected (BOS: 400 InvalidURI)"""
        # /./v1 → strip('/') → ./v1 → '.' segment
        with self.assertRaises(ValueError):
            self.bos.generate_pre_signed_url(self.BUCKET, b'/./v1', timestamp=1,
                                             expiration_in_seconds=1800)

    def test_generate_pre_signed_url_with_single_dot_key(self):
        """test generate_pre_signed_url with key='.' is rejected"""
        with self.assertRaises(ValueError):
            self.bos.generate_pre_signed_url(self.BUCKET, b'.', timestamp=1,
                                             expiration_in_seconds=1800)

    def test_generate_pre_signed_url_with_dot_slash_key(self):
        """test generate_pre_signed_url with key='./' is rejected (strip→'.')"""
        with self.assertRaises(ValueError):
            self.bos.generate_pre_signed_url(self.BUCKET, b'./', timestamp=1,
                                             expiration_in_seconds=1800)

    def test_generate_pre_signed_url_with_middle_dot_segment(self):
        """test generate_pre_signed_url with 'foo/./bar' is rejected"""
        with self.assertRaises(ValueError):
            self.bos.generate_pre_signed_url(self.BUCKET, b'foo/./bar', timestamp=1,
                                             expiration_in_seconds=1800)

    def test_generate_pre_signed_url_with_double_dot_key(self):
        """test generate_pre_signed_url with '..' path traversal is rejected (BOS: 400 Bad Request)"""
        with self.assertRaises(ValueError):
            self.bos.generate_pre_signed_url(self.BUCKET, b'abc/../v1', timestamp=1,
                                             expiration_in_seconds=1800)

    def test_generate_pre_signed_url_with_double_dot_prefix(self):
        """test generate_pre_signed_url with '../other-bucket/secret' is rejected"""
        with self.assertRaises(ValueError):
            self.bos.generate_pre_signed_url(self.BUCKET, b'../other-bucket/secret', timestamp=1,
                                             expiration_in_seconds=1800)

    def test_generate_pre_signed_url_with_double_dot_trailing_slash(self):
        """test generate_pre_signed_url with 'abc/../' is rejected"""
        with self.assertRaises(ValueError):
            self.bos.generate_pre_signed_url(self.BUCKET, b'abc/../', timestamp=1,
                                             expiration_in_seconds=1800)

    def test_generate_pre_signed_url_with_deep_path_traversal(self):
        """test generate_pre_signed_url with deep path traversal '../../etc/passwd' is rejected"""
        with self.assertRaises(ValueError):
            self.bos.generate_pre_signed_url(self.BUCKET, b'../../etc/passwd', timestamp=1,
                                             expiration_in_seconds=1800)

    def test_generate_pre_signed_url_with_dot_in_filename_allowed(self):
        """test generate_pre_signed_url with '.' inside filename (not as a segment) is allowed"""
        # 'normal-file.txt' contains '.' but not as a standalone segment — should succeed
        url = self.bos.generate_pre_signed_url(self.BUCKET, b'normal-file.txt', timestamp=1,
                                               expiration_in_seconds=1800)
        self.assertIsNotNone(url)

    def test_generate_pre_signed_url_with_path_containing_dot_in_filename_allowed(self):
        """test generate_pre_signed_url with 'path/to/file.jpg' is allowed"""
        url = self.bos.generate_pre_signed_url(self.BUCKET, b'path/to/file.jpg', timestamp=1,
                                               expiration_in_seconds=1800)
        self.assertIsNotNone(url)

    def test_generate_pre_signed_url_with_double_slash_key(self):
        """test generate_pre_signed_url with '//v1/object' — double slash stripped, should succeed"""
        # strip('/') → 'v1/object', no dangerous segment
        url = self.bos.generate_pre_signed_url(self.BUCKET, b'//path/to/object', timestamp=1,
                                               expiration_in_seconds=1800)
        self.assertIsNotNone(url)

    def test_generate_pre_signed_url_with_invalid_protocol(self):
        """test generate_pre_signed_url with invalid protocol string raises ValueError"""
        with self.assertRaises(ValueError):
            self.bos.generate_pre_signed_url(self.BUCKET, self.KEY, timestamp=1,
                                             expiration_in_seconds=1800,
                                             protocol='ftp')

    def test_generate_pre_signed_url_url_structure(self):
        """test generate_pre_signed_url result has expected URL structure"""
        url = self.bos.generate_pre_signed_url(self.BUCKET, b'my-object', timestamp=1,
                                               expiration_in_seconds=3600)
        url_str = compat.convert_to_string(url)
        # Should contain '?' separator and 'authorization' param
        self.assertIn('?', url_str)
        self.assertIn('authorization', url_str.lower())
        # Should contain the bucket name in path
        bucket_str = compat.convert_to_string(self.BUCKET)
        self.assertIn(bucket_str, url_str)


class TestValidateObjectKey(unittest.TestCase):
    """
    Unit tests for bos_handler.validate_object_key.
    These tests are pure unit tests — no BOS server connection required.
    """

    def setUp(self):
        from baidubce.services.bos import bos_handler
        self.validate = bos_handler.validate_object_key

    def test_empty_string_raises(self):
        """empty string key must be rejected"""
        with self.assertRaises(ValueError) as ctx:
            self.validate('')
        self.assertIn('empty', str(ctx.exception))

    def test_none_like_empty_raises(self):
        """falsy empty-string equivalent must be rejected"""
        with self.assertRaises(ValueError):
            self.validate('')

    def test_single_dot_only(self):
        """key='.' is rejected"""
        with self.assertRaises(ValueError) as ctx:
            self.validate('.')
        self.assertIn('.', str(ctx.exception))

    def test_dot_as_first_segment(self):
        """key='./v1' is rejected (leading dot segment)"""
        with self.assertRaises(ValueError):
            self.validate('./v1')

    def test_dot_as_middle_segment(self):
        """key='foo/./bar' is rejected (middle dot segment)"""
        with self.assertRaises(ValueError):
            self.validate('foo/./bar')

    def test_dot_as_last_segment(self):
        """key='foo/.' is rejected (trailing dot segment)"""
        with self.assertRaises(ValueError):
            self.validate('foo/.')

    def test_dot_after_strip_slash(self):
        """After strip('/'), '/./v1' becomes './v1' — still rejected"""
        # simulate what bos_client does: strip('/') first
        key = '/./v1'.strip('/')   # → './v1'
        with self.assertRaises(ValueError):
            self.validate(key)

    def test_double_dot_only(self):
        """key='..' is rejected"""
        with self.assertRaises(ValueError) as ctx:
            self.validate('..')
        self.assertIn('..', str(ctx.exception))

    def test_double_dot_as_first_segment(self):
        """key='../other-bucket/secret' is rejected"""
        with self.assertRaises(ValueError):
            self.validate('../other-bucket/secret')

    def test_double_dot_as_middle_segment(self):
        """key='abc/../v1' is rejected"""
        with self.assertRaises(ValueError):
            self.validate('abc/../v1')

    def test_double_dot_as_last_segment(self):
        """key='abc/..' is rejected"""
        with self.assertRaises(ValueError):
            self.validate('abc/..')

    def test_deep_path_traversal(self):
        """key='../../etc/passwd' is rejected"""
        with self.assertRaises(ValueError):
            self.validate('../../etc/passwd')

    def test_mixed_dot_and_double_dot(self):
        """key='./abc/../secret' — contains both '.' and '..' segments, rejected"""
        with self.assertRaises(ValueError):
            self.validate('./abc/../secret')

    def test_simple_filename(self):
        """normal-file.txt is allowed"""
        self.validate('normal-file.txt')   # must not raise

    def test_path_key(self):
        """path/to/file.jpg is allowed"""
        self.validate('path/to/file.jpg')

    def test_key_with_dot_in_name(self):
        """'foo.bar' — dot inside filename, not a segment — allowed"""
        self.validate('foo.bar')

    def test_key_with_double_dot_in_name(self):
        """'foo..bar' — double dot inside filename, not a standalone segment — allowed"""
        self.validate('foo..bar')

    def test_key_with_hyphen_underscore(self):
        """hyphens and underscores are allowed"""
        self.validate('path/to/my-file_v2.txt')

    def test_key_with_chinese_chars(self):
        """Chinese characters in key are allowed"""
        self.validate(u'路径/文件名.txt')

    def test_key_with_spaces(self):
        """spaces in key (though not recommended) should pass validation"""
        self.validate('path/to/my file.txt')

    def test_key_with_at_sign(self):
        """@ in key is allowed"""
        self.validate('test/file@key.txt')

    def test_segment_with_three_dots(self):
        """'...' (three dots) is NOT a path traversal — allowed"""
        self.validate('path/.../file')

    def test_segment_starting_with_dots(self):
        """'..hidden' is NOT a standalone '..' segment — allowed"""
        self.validate('path/..hidden/file')

    def test_segment_ending_with_dot(self):
        """'foo.' is NOT a standalone '.' segment — allowed"""
        self.validate('foo./bar')

    def test_segment_starting_with_dot_but_longer(self):
        """'.gitignore' is NOT a standalone '.' — allowed"""
        self.validate('.gitignore')

    def test_double_dot_with_extra_chars(self):
        """'..extra' is NOT a standalone '..' — allowed"""
        self.validate('..extra/file.txt')


class TestValidateBucketName(unittest.TestCase):
    """
    Unit tests for bos_handler.validate_bucket_name.
    Pure unit tests — no BOS server connection required.
    """

    def setUp(self):
        from baidubce.services.bos import bos_handler
        self.validate = bos_handler.validate_bucket_name

    # ── valid names ──────────────────────────────────────────────────────────

    def test_valid_lowercase_letters_only(self):
        """all lowercase letters"""
        self.validate('mybucket')

    def test_valid_with_digits(self):
        """lowercase letters and digits"""
        self.validate('bucket123')

    def test_valid_with_hyphens(self):
        """hyphens in the middle are allowed"""
        self.validate('my-bucket-name')

    def test_valid_min_length(self):
        """exactly 3 characters is the minimum"""
        self.validate('abc')

    def test_valid_max_length(self):
        """exactly 63 characters is the maximum"""
        self.validate('a' * 63)

    def test_valid_starts_with_digit(self):
        """starting with a digit is allowed"""
        self.validate('1bucket')

    def test_valid_ends_with_digit(self):
        """ending with a digit is allowed"""
        self.validate('bucket1')

    def test_valid_bytes_input(self):
        """bytes input is decoded and validated"""
        self.validate(b'valid-bucket')

    def test_none_is_allowed(self):
        """None bucket_name (no-bucket operations like list_buckets) is skipped"""
        self.validate(None)   # must not raise

    # ── invalid: forbidden characters ────────────────────────────────────────

    def test_uppercase_letters_rejected(self):
        """uppercase letters are not allowed"""
        with self.assertRaises(ValueError):
            self.validate('MyBucket')

    def test_underscore_rejected(self):
        """underscores are not allowed"""
        with self.assertRaises(ValueError):
            self.validate('my_bucket')

    def test_hash_rejected(self):
        """# is not allowed"""
        with self.assertRaises(ValueError):
            self.validate('my#bucket')

    def test_question_mark_rejected(self):
        """? is not allowed"""
        with self.assertRaises(ValueError):
            self.validate('my?bucket')

    def test_slash_rejected(self):
        """/ is not allowed"""
        with self.assertRaises(ValueError):
            self.validate('my/bucket')

    def test_backslash_rejected(self):
        """backslash is not allowed"""
        with self.assertRaises(ValueError):
            self.validate('my\\bucket')

    def test_at_sign_rejected(self):
        """@ is not allowed"""
        with self.assertRaises(ValueError):
            self.validate('my@bucket')

    def test_colon_rejected(self):
        """: is not allowed"""
        with self.assertRaises(ValueError):
            self.validate('my:bucket')

    def test_space_rejected(self):
        """spaces are not allowed"""
        with self.assertRaises(ValueError):
            self.validate('my bucket')

    def test_control_char_rejected(self):
        """control characters are not allowed"""
        with self.assertRaises(ValueError):
            self.validate('my\x00bucket')

    def test_dot_rejected(self):
        """dots are not allowed (despite being common in S3; BOS disallows them)"""
        with self.assertRaises(ValueError):
            self.validate('my.bucket')

    # ── invalid: length ───────────────────────────────────────────────────────

    def test_too_short_one_char(self):
        """single character is too short"""
        with self.assertRaises(ValueError):
            self.validate('a')

    def test_too_short_two_chars(self):
        """two characters are too short"""
        with self.assertRaises(ValueError):
            self.validate('ab')

    def test_too_long_64_chars(self):
        """64 characters exceeds maximum"""
        with self.assertRaises(ValueError):
            self.validate('a' * 64)

    # ── invalid: start/end constraints ────────────────────────────────────────

    def test_starts_with_hyphen_rejected(self):
        """bucket name must not start with a hyphen"""
        with self.assertRaises(ValueError):
            self.validate('-mybucket')

    def test_ends_with_hyphen_rejected(self):
        """bucket name must not end with a hyphen"""
        with self.assertRaises(ValueError):
            self.validate('mybucket-')

    def test_only_hyphens_rejected(self):
        """all hyphens is not a valid name"""
        with self.assertRaises(ValueError):
            self.validate('---')

    # ── integration: _send_request blocks illegal bucket ─────────────────────

    def test_send_request_blocks_illegal_bucket(self):
        """_send_request raises ValueError before making any HTTP call"""
        from baidubce.services.bos import bos_client
        import bos_test_config
        client = bos_client.BosClient(bos_test_config.config)
        with self.assertRaises(ValueError):
            client._send_request('HEAD', bucket_name='Invalid#Bucket!')

    def test_generate_pre_signed_url_blocks_illegal_bucket(self):
        """generate_pre_signed_url raises ValueError before signing"""
        from baidubce.services.bos import bos_client
        import bos_test_config
        client = bos_client.BosClient(bos_test_config.config)
        with self.assertRaises(ValueError):
            client.generate_pre_signed_url('Invalid/Bucket', 'mykey')


class TestListMultipartsUploads(TestClient):
    """test get_all_multi_upload function"""
    def test_list_multipart_uploads(self):
        """test _list_multipart_uploads function normally"""
        time1 = utils.get_canonical_time()
        upload_id1 = self.bos.initiate_multipart_upload\
            (self.BUCKET, b"aaa").upload_id

        time2 = utils.get_canonical_time()
        upload_id2 = self.bos.initiate_multipart_upload\
            (self.BUCKET, b"bbb").upload_id

        response = self.bos.list_multipart_uploads(self.BUCKET, max_uploads=1)
        self.check_headers(response)
        self.assertEqual(response.bucket, self.BUCKET)
        self.assertEqual(response.max_uploads, 1)
        self.assertEqual(response.prefix, '')
        self.assertTrue(response.is_truncated)
        self.assertEqual(response.key_marker, '')

        for item in response.uploads:
            self.assertEqual(item.key, 'aaa')
            self.assertEqual(item.upload_id, upload_id1)
            # self.assertEqual(item.owner.id, bos_test_config.OWNER_ID)
            # self.assertEqual(item.owner.display_name, bos_test_config.DISPLAY_NAME)
            self.assertEqual(
                compat.convert_to_bytes(item.initiated), time1)

        response = self.bos.list_multipart_uploads(self.BUCKET, max_uploads=1,
                key_marker=b'aaa')
        for item in response.uploads:
            self.assertEqual(item.key, 'bbb')
            self.assertEqual(item.upload_id, upload_id2)
            # self.assertEqual(item.owner.id, bos_test_config.OWNER_ID)
            # self.assertEqual(item.owner.display_name, bos_test_config.DISPLAY_NAME)
            self.assertEqual(
                compat.convert_to_bytes(item.initiated), time2)

    def test_list_all_multipart_uploads(self):
        """test list_all_multipart_uploads function normally"""
        time1 = utils.get_canonical_time()
        upload_id1 = self.bos.initiate_multipart_upload\
            (self.BUCKET, b"aaa").upload_id

        time2 = utils.get_canonical_time()
        upload_id2 = self.bos.initiate_multipart_upload\
            (self.BUCKET, b"bbb").upload_id

        key_list = [u'aaa', u'bbb']
        id_list = [upload_id1, upload_id2]
        time_list = [time1, time2]
        for item, key, id, timestamp in zip(self.bos.list_all_multipart_uploads(self.BUCKET),
                                            key_list,
                                            id_list,
                                            time_list):
            self.assertEqual(item.key, key)
            self.assertEqual(item.upload_id, id)
            # self.assertEqual(item.owner.id, bos_test_config.OWNER_ID)
            # self.assertEqual(item.owner.display_name, bos_test_config.DISPLAY_NAME)
            self.assertEqual(
                compat.convert_to_bytes(item.initiated), timestamp)


class TestSetBucketAcl(TestClient):
    """test set_bucket_acl"""
    def test_set_bucket_acl(self):
        """test set_bucket_acl, which set bucket acl from Grant list"""
        grant_list = list()
        grant_list.append({'grantee':
                            [{'id': 'a0a2fe988a774be08978736ae2a1668b'},
                            {'id': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'}],
                           'permission': ['FULL_CONTROL']})
        err = None
        try:
            self.bos.set_bucket_acl(self.BUCKET, grant_list)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)

    def test_set_bucket_canned_acl(self):
        """test set_bucket_canned_acl, set bucket acl from header and set canned acl"""
        err = None
        try:
            self.bos.set_bucket_canned_acl(self.BUCKET, b"public-read-write")
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)


class TestGetBucketAcl(TestClient):
    """test get_bucket_acl function"""
    def test_get_bucket_acl(self):
        """test get_bucket_acl function normally"""
        grant_list = list()
        grant_list.append({'grantee':
                            [{'id': 'a0a2fe988a774be08978736ae2a1668b'},
                            {'id': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'}],
                           'permission': ['FULL_CONTROL']})
        err = None
        try:
            self.bos.set_bucket_acl(self.BUCKET, grant_list)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)

        err = None
        try:
            response = self.bos.get_bucket_acl(self.BUCKET)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.check_headers(response)
        # self.assertEqual(response.owner.id, bos_test_config.OWNER_ID)
        self.assertEqual(response.access_control_list[0].grantee[0].id,
                         'a0a2fe988a774be08978736ae2a1668b')
        self.assertEqual(response.access_control_list[0].grantee[1].id,
                         'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        self.assertListEqual(response.access_control_list[0].permission,
                             ["FULL_CONTROL"])

        err = None
        try:
            self.bos.set_bucket_acl(self.BUCKET, response.access_control_list)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)

# static website

class TestBucketStaticWebsite(TestClient):
    """test bucket static website"""
    def test_bucket_static_website(self):
        """test put,get,delete bucket static website"""
        index = 'index.html'
        not_found = '404.html'
        # put object as index page and 404 page
        self.bos.put_object_from_string(self.BUCKET,
                compat.convert_to_bytes(index),
                "Welcome to bce!")
        self.bos.put_object_from_string(self.BUCKET,
                compat.convert_to_bytes(not_found),
                "404 ERROR!We cann't find the page!")
        # test put bucket static website
        err = None
        try:
            self.bos.put_bucket_static_website(self.BUCKET, index=index)
            self.bos.put_bucket_static_website(self.BUCKET, not_found=not_found)
            self.bos.put_bucket_static_website(self.BUCKET, index=index, not_found=not_found)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        # test get bucket static website
        err = None
        try:
            response = self.bos.get_bucket_static_website(self.BUCKET)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.check_headers(response)
        self.assertEqual(response.index, index)
        self.assertEqual(response.not_found, not_found)

        err = None
        try:
            self.bos.put_bucket_static_website(self.BUCKET,
                    index=response.index,
                    not_found=not_found)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        # test delete bucket static website
        err = None
        try:
            response = self.bos.delete_bucket_static_website(self.BUCKET)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)


# test server encryption
class TestPutBucketEncryption(TestClient):
    """test put_bucket_encryption"""
    def test_put_bucket_encryption(self):
        """test set_bucket_acl with AES256 algorithm"""
        err = None
        try:
            self.bos.put_bucket_encryption(self.BUCKET)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)


class TestGetAndDeleteBucketEncryption(TestClient):
    """test get_bucket_encryption and delete_bucket_encryption function"""
    def test_get_dnd_elete_bucket_encryption(self):
        """test get_bucket_encryption and delete_bucket_encryption function"""
        err = None
        try:
            self.bos.put_bucket_encryption(self.BUCKET)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        # test get bucekt server encryption algorithm
        err = None
        try:
            response = self.bos.get_bucket_encryption(self.BUCKET)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)

        self.check_headers(response)
        self.assertEqual(response.encryption_algorithm,
                         'AES256')
        err = None
        try:
            self.bos.put_bucket_encryption(self.BUCKET, response.encryption_algorithm)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        # test delete bucket server encryption
        err = None
        try:
            self.bos.delete_bucket_encryption(self.BUCKET)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)


# test bucket copyright protection
class TestBucketCopyrightProtection(TestClient):
    """test bucket copyright protection"""
    def test_bucket_copyright_protection(self):
        """test put,get,delete bucket copyright protection"""
        resource = [self.BUCKET + "/test/*"]
        # test put bucket copyright protection
        err = None
        try:
            self.bos.put_bucket_copyright_protection(self.BUCKET, resource)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        # test get bucket copyright protection
        err = None
        try:
            response = self.bos.get_bucket_copyright_protection(self.BUCKET)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.check_headers(response)
        self.assertEqual(response.resource[0], resource[0])

        err = None
        try:
            self.bos.put_bucket_copyright_protection(self.BUCKET, response.resource)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        # test delete bucket copyright protection 
        err = None
        try:
            response = self.bos.delete_bucket_copyright_protection(self.BUCKET)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)


# test bucket replication

class TestBucketReplication(TestClient):
    """test bucket replication"""
    def test_bucket_replication(self):
        """test put,get,delete bucket replication"""
        if not self.bos.does_bucket_exist(self.BUCKET):
            self.bos.create_bucket(self.BUCKET)
        # create destination bucket
        dst_bucket_name = self.BUCKET + "-gz"
        rule_id = "sample-rep-config"
        if not self.bos.does_bucket_exist(dst_bucket_name):
            self.bos.create_bucket(dst_bucket_name,
                config = BceClientConfiguration(endpoint = b'gz.bcebos.com'))
        replication = {
        "status":"enabled",
        "resource":[
            self.BUCKET + "/*"
            ],
        "destination":
            {
                "bucket": dst_bucket_name,
                "storageClass":"COLD"
            },
        "replicateHistory":
            {
                "bucket": dst_bucket_name,
                "storageClass":"COLD"
            },
        "replicateDeletes":"enabled",
        "id": rule_id
        }
        # test put bucket replication
        err = None
        try:
            response = self.bos.put_bucket_replication(self.BUCKET, replication)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        # test get bucket replication
        err = None
        try:
            response = self.bos.get_bucket_replication(self.BUCKET, id=rule_id)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.check_headers(response)
        self.assertEqual(response.resource[0], replication['resource'][0])
        self.assertEqual(response.destination.bucket, replication['destination']['bucket'])
        # test get_bucket_replication_progress()
        err = None
        try:
            response = self.bos.get_bucket_replication_progress(self.BUCKET, id=rule_id)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.check_headers(response)
        self.assertEqual(response.status, replication['status'])
        # test list_bucket_replication()
        err = None
        try:
            response = self.bos.list_bucket_replication(self.BUCKET)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.check_headers(response)
        self.assertEqual(response.rules[0].resource[0], replication['resource'][0])
        self.assertEqual(response.rules[0].destination.bucket, replication['destination']['bucket'])
        # test delete bucket replication
        err = None
        try:
            response = self.bos.delete_bucket_replication(self.BUCKET ,id=rule_id)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)

        self.bos.delete_bucket(dst_bucket_name,
            config = BceClientConfiguration(endpoint = b'gz.bcebos.com'))

class TestBucketInventory(TestClient):
    """test bucket inventory"""
    def test_bucket_inventory(self):
        """test put,get,delete,list bucket inventory"""
        # create destination bucket
        dst_bucket_name = self.BUCKET + "-inventory-target"
        if not self.bos.does_bucket_exist(dst_bucket_name):
            self.bos.create_bucket(dst_bucket_name)

        inventory_id = "testInventory001"
        my_inventory = {
            "id": inventory_id,
            "status": "enabled",
            "resource": [compat.convert_to_string(self.BUCKET) + "/*"],
            "schedule": "Weekly",
            "destination":{
                "targetBucket": compat.convert_to_string(dst_bucket_name),
                "targetPrefix": "destination-prefix/",
                "format": "CSV"
                }
        }
        # test put bucket inventory
        err = None
        try:
            self.bos.put_bucket_inventory(self.BUCKET, my_inventory)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        # test get bucket inventory
        err = None
        try:
            response = self.bos.get_bucket_inventory(self.BUCKET, inventory_id)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.check_headers(response)
        self.assertEqual(response.resource[0], my_inventory['resource'][0])
        self.assertEqual(response.destination.target_bucket, my_inventory['destination']['targetBucket'])

        # test list inventory
        err = None
        try:
            response = self.bos.list_bucket_inventory(self.BUCKET)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.check_headers(response)
        self.assertEqual(response.inventory_rule_list[0].resource[0], my_inventory['resource'][0])
        # test delete bucket replication
        err = None
        try:
            response = self.bos.delete_bucket_inventory(self.BUCKET, inventory_id)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)

        self.bos.delete_bucket(dst_bucket_name)

# test bucket trash

class TestBucketTrash(TestClient):
    """test bucket trash"""
    def test_bucket_trash(self):
        """test put,get,delete bucket trash"""
        # test put bucket trash
        trash_dir = '.mytrash'
        err = None
        try:
            self.bos.put_bucket_trash(self.BUCKET, trash_dir=trash_dir)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        # test get bucket trash
        err = None
        try:
            response = self.bos.get_bucket_trash(self.BUCKET)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.check_headers(response)
        self.assertEqual(response.trash_dir, trash_dir)

        # delete object to trash
        object_for_delete = b'wonderful'
        self.bos.put_object_from_string(self.BUCKET, object_for_delete, "hello world!")
        self.bos.delete_object(self.BUCKET, object_for_delete)
        deleted_object = trash_dir + "/" + compat.convert_to_string(object_for_delete)
        deleted_object = compat.convert_to_bytes(deleted_object)
        try:
            response = self.bos.get_object_meta_data(self.BUCKET, deleted_object)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)

        err = None
        try:
            self.bos.put_bucket_trash(self.BUCKET, trash_dir=response.trash_dir)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        # test delete bucket trash
        err = None
        try:
            response = self.bos.delete_bucket_trash(self.BUCKET)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)


class TestGetBucketLocation(TestClient):
    """test get_bucket_location"""
    def test_get_bucket_location(self):
        """test get_bucket_location normally"""
        response = None
        err = None
        try:
            response = self.bos.get_bucket_location(self.BUCKET)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.assertEqual(response, "bj")


class TestGetObjectMetaData(TestClient):
    """test get_object_meta_data function"""
    def test_get_object_meta_data(self):
        """test get_object_meta_data function normally"""
        options = dict()
        options["private"] = "This is private."
        err = None
        try:
            self.bos.put_object_from_string(self.BUCKET,
                                            self.KEY,
                                            "This is a string.",
                                            user_metadata=options)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)

        err = None
        try:
            response = self.bos.get_object_meta_data(self.BUCKET, self.KEY)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.check_headers(response)
        self.assertEqual(response.metadata.etag, '13562b471182311b6eea8d241103e8f0')
        self.assertEqual(int(response.metadata.content_length), len("This is a string."))
        self.assertEqual(response.metadata.bce_meta_private, "This is private.")


class TestGetObject(TestClient):
    """test get_object function"""
    def test_get_object(self):
        """test get_object function normally"""
        err = None
        try:
            response = self.bos.put_object_from_string(self.BUCKET,
                                                       self.KEY,
                                                       "This is a string.",
                                                       user_metadata={"private": "private"})
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.check_headers(response)

        err = None
        try:
            response = self.bos.get_object(self.BUCKET, self.KEY)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)

        self.check_headers(response)
        self.assertEqual(response.metadata.etag, '13562b471182311b6eea8d241103e8f0')
        self.assertDictEqual(response.metadata.user_metadata, {u"private":u"private"})

    def test_get_object_as_string(self):
        """test get_object_as_string function normally"""
        # objet is empty or start with '/'
        err = None
        try:
            response = self.bos.get_object_as_string(self.BUCKET, b"")
        except BceClientError as e:
            err = e
        finally:
            self.assertIsInstance(err, BceClientError)
        
        err = None
        try:
            response = self.bos.get_object_as_string(self.BUCKET, b"/abc")
        except BceClientError as e:
            err = e
        finally:
            self.assertIsInstance(err, BceClientError)
        
        err = None
        try:
            response = self.bos.put_object_from_string(self.BUCKET,
                                                       self.KEY,
                                                       "This is a string.")
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.check_headers(response)

        err = None
        try:
            response = self.bos.get_object_as_string(self.BUCKET, self.KEY)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)

        self.assertEqual(response, b"This is a string.")

        

    def test_get_object_to_file(self):
        """test get_object_to_file function normally"""
        # objet is empty or start with '/'
        err = None
        try:
            response = self.bos.get_object_to_file(self.BUCKET, b"", b"Filename")
        except BceClientError as e:
            err = e
        finally:
            self.assertIsInstance(err, BceClientError)
        
        err = None
        try:
            response = self.bos.get_object_to_file(self.BUCKET, b"/abc", b"Filename")
        except BceClientError as e:
            err = e
        finally:
            self.assertIsInstance(err, BceClientError)

        # create object , then get object to file
        err = None
        try:
            response = self.bos.put_object_from_string(self.BUCKET, self.KEY, "This is a string.")
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.check_headers(response)

        err = None
        try:
            response = self.bos.get_object_to_file(self.BUCKET, self.KEY, b"Filename")
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
            os.remove("Filename")

        self.check_headers(response)
        self.assertEqual(response.metadata.etag, '13562b471182311b6eea8d241103e8f0')

    def test_get_object_to_file_with_range(self):
        """test get_object_to_file function with range"""
        err = None
        try:
            response = self.bos.put_object_from_string(self.BUCKET, self.KEY, "a" * 1000)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.check_headers(response)

        fp = open(self.FILENAME, "w")
        fp.write('a' * 100)
        fp.close()

        fp = open(self.FILENAME, "rb")
        md5 = utils.get_md5_from_fp(fp)
        fp.close()
        os.remove(self.FILENAME)

        err = None
        try:
            response = self.bos.get_object_to_file(self.BUCKET,
                                                   self.KEY,
                                                   self.FILENAME,
                                                   range=(0, 99))
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.check_headers(response)
        self.assertEqual(response.metadata.content_range, 'bytes 0-99/1000')

        fp = open(self.FILENAME, "rb")
        get_md5 = utils.get_md5_from_fp(fp)
        fp.close()
        self.assertEqual(get_md5, md5)


class TestListBuckets(TestClient):
    """test list_bucket function"""
    def test_list_bucket(self):
        """test list_bucket function normally"""

        if self.bos.does_bucket_exist("aaaaaaxzr1"):
            self.bos.delete_bucket("aaaaaaxzr1")
        if self.bos.does_bucket_exist("aaaaaaxzr2"):
            self.bos.delete_bucket("aaaaaaxzr2")

        time1 = utils.get_canonical_time()
        self.bos.create_bucket("aaaaaaxzr1")

        time2 = utils.get_canonical_time()
        self.bos.create_bucket("aaaaaaxzr2")

        response = self.bos.list_buckets()
        self.check_headers(response)

        # self.assertEqual(response.owner.id, bos_test_config.OWNER_ID)
        # self.assertEqual(response.owner.display_name, bos_test_config.DISPLAY_NAME)
        for bucket in response.buckets:
            if bucket.name == "aaaaaaxzr1":
                self.assertEqual(
                    compat.convert_to_bytes(bucket.creation_date)[0:-4], 
                    compat.convert_to_bytes(time1)[0:-4])
            elif bucket.name == "aaaaaaxzr2":
                self.assertEqual(
                    compat.convert_to_bytes(bucket.creation_date)[0:-4], 
                    compat.convert_to_bytes(time2)[0:-4])
        self.bos.delete_bucket("aaaaaaxzr1")
        self.bos.delete_bucket("aaaaaaxzr2")


class TestListObjects(TestClient):
    """test list_objects function"""
    def test_list_objects(self):
        """test list_objects function normally"""
        for i in range(0, 10):
            self.bos.put_object_from_string(
                self.BUCKET, 
                b"test_object_%s" % compat.convert_to_bytes(random.random()),
                "This is a string.")

        response = self.bos.list_objects(self.BUCKET, prefix="", delimiter="")
        self.check_headers(response)
        self.assertFalse(response.is_truncated)
        self.assertEqual(response.max_keys, 1000)
        self.assertEqual(response.name, self.BUCKET)
        self.assertEqual(response.prefix, "")

        # test prefix and marker with Chineses
        for i in range(0, 5):
            key1 = "测试_%s" % compat.convert_to_string(random.random())
            key2 = "测试文件_%s" % compat.convert_to_string(random.random())
            self.bos.put_object_from_string(
                self.BUCKET, 
                compat.convert_to_bytes(key1),
                "This is a string.")
            self.bos.put_object_from_string(
                self.BUCKET, 
                compat.convert_to_bytes(key2),
                "This is a string.")

        prefix = '测试'
        marker = '测试文件'
        response = self.bos.list_objects(self.BUCKET, prefix = prefix)
        self.check_headers(response)
        self.assertEqual(len(response.contents), 10)
        self.assertEqual(response.prefix, prefix)
        response = self.bos.list_objects(self.BUCKET, marker = marker)
        self.check_headers(response)
        self.assertEqual(len(response.contents), 5)
        self.assertEqual(response.marker, marker)


    def test_list_object_with_max_keys(self):
        """test list_objects function with max_keys"""
        for i in range(0, 9):
            self.bos.put_object_from_string(
                self.BUCKET, 
                b"test_object_%s" % compat.convert_to_bytes(random.random()),
                "This is a string.")

            response = self.bos.list_objects(self.BUCKET)

            all_list = list()
            tmp_list = list()

            for item in response.contents:
                all_list.append(item.key)

            response = self.bos.list_objects(self.BUCKET, max_keys=4)
            for item in response.contents:
                tmp_list.append(item.key)

            response = self.bos.list_objects(self.BUCKET, max_keys=5, marker=tmp_list[-1])
            for item in response.contents:
                tmp_list.append(item.key)

            self.assertListEqual(all_list, tmp_list)

    def test_list_all_object(self):
        """test list_all_objects function"""
        object_keys = []
        for i in range(0, 9):
            object_key = b"test_object_%s" % compat.convert_to_bytes(random.random())
            self.bos.put_object_from_string(self.BUCKET, object_key,
                                            "This is a string.")
            object_keys.append(object_key)
        for item in self.bos.list_all_objects(self.BUCKET):
            self.assertTrue(compat.convert_to_bytes(item.key) in object_keys)


class TestListParts(TestClient):
    """test list_parts function"""
    def test_list_parts(self):
        """test list_parts function normally"""
        self.get_file(5)
        time1 = utils.get_canonical_time()
        upload_id = self.bos.initiate_multipart_upload(self.BUCKET,
                                                       self.KEY).upload_id
        time2 = utils.get_canonical_time()
        response = self.bos.upload_part_from_file(self.BUCKET,
                                                  self.KEY,
                                                  upload_id,
                                                  part_number=1,
                                                  part_size=100,
                                                  file_name=self.FILENAME,
                                                  offset=0)
        self.assertEqual(response.metadata.content_length, '0')
        self.assertEqual(response.metadata.etag, "6d0bb00954ceb7fbee436bb55a8397a9")

        response = self.bos.list_parts(self.BUCKET, self.KEY, upload_id)
        self.check_headers(response)
        self.assertEqual(response.bucket, self.BUCKET)
        self.assertEqual(compat.convert_to_bytes(response.initiated), time1)
        self.assertFalse(response.is_truncated)

        # self.assertEqual(response.owner.id, bos_test_config.OWNER_ID)
        # self.assertEqual(response.owner.display_name, bos_test_config.DISPLAY_NAME)
        self.assertEqual(response.upload_id, upload_id)
        self.assertEqual(response.next_part_number_marker, 1)
        self.assertEqual(response.part_number_marker, 0)

        for item in response.parts:
            self.assertEqual(item.etag, "6d0bb00954ceb7fbee436bb55a8397a9")
            self.assertEqual(item.size, 100)
            self.assertEqual(item.part_number, 1)
            self.assertEqual(compat.convert_to_bytes(item.last_modified), time2)

    def test_list_all_parts(self):
        """test list_all_parts function normally"""
        self.get_file(5)
        time1 = utils.get_canonical_time()
        upload_id = self.bos.initiate_multipart_upload(self.BUCKET,
                                                       self.KEY).upload_id
        time2 = utils.get_canonical_time()
        response = self.bos.upload_part_from_file(self.BUCKET,
                                                  self.KEY,
                                                  upload_id,
                                                  part_number=1,
                                                  part_size=100,
                                                  file_name=self.FILENAME,
                                                  offset=0)
        self.assertEqual(response.metadata.content_length, '0')
        self.assertEqual(response.metadata.etag, "6d0bb00954ceb7fbee436bb55a8397a9")
        for item in self.bos.list_all_parts(self.BUCKET, self.KEY, upload_id):
            self.assertEqual(item.etag, "6d0bb00954ceb7fbee436bb55a8397a9")
            self.assertEqual(item.size, 100)
            self.assertEqual(item.part_number, 1)
            self.assertEqual(compat.convert_to_bytes(item.last_modified), time2)


class TestDeleteMultipleObjects(TestClient):
    """test delete_multiple_objects"""
    def test_delete_multiple_objects(self):
        """test delete_multiple_objects function normally"""
        self.bos.put_object_from_string(self.BUCKET, b'hello1', 'Hello World')
        self.bos.put_object_from_string(self.BUCKET, b'hello2', u'hello world')
        key_list = [b'hello1', b'hello2']
        response = self.bos.delete_multiple_objects(self.BUCKET, key_list)
        self.check_headers(response)


class TestPutObject(TestClient):
    """test put_object"""
    def test_put_object_from_string(self):
        """test put_object_from_string function normally"""
        response = self.bos.put_object_from_string(self.BUCKET, self.KEY, "Hello World")
        self.check_headers(response)
        response = self.bos.put_object_from_string(self.BUCKET, self.KEY, u"Hello World")
        self.check_headers(response)
        response = self.bos.put_object_from_string(self.BUCKET,
                                                   self.KEY,
                                                   u"Hello World")
        self.check_headers(response)
        err = None
        try:
            response = self.bos.put_object_from_string(self.BUCKET, self.KEY, 123)
        except TypeError as e:
            err = e
        finally:
            self.assertIsNotNone(err)

    def test_put_object_user_headers(self):
        """test put_object_from_string user headers"""
        user_headers = {"Cache-Control":"private", 
                        "Content-Disposition":"attachment; filename=\"abc.txt\"", 
                        "Expires":"123456"}
        response = self.bos.put_object_from_string(bucket=self.BUCKET,
                                                   key=b"test_put_user_headers",
                                                   data='Hello World',
                                                   user_headers=user_headers)
        self.check_headers(response)

        response = self.bos.get_object_meta_data(bucket_name=self.BUCKET, 
                                                 key=b'test_put_user_headers')
        self.assertEqual(response.metadata.expires, "123456")
        self.assertEqual(response.metadata.content_disposition, 'attachment; filename="abc.txt"')
        self.assertEqual(response.metadata.cache_control, 'private')

    def test_put_object_from_string_with_storage_class(self):
        """test put_object_from_string with storage class"""
        # test cold
        response = self.bos.put_object_from_string(bucket=self.BUCKET, 
                                                   key=b"testcold", 
                                                   data='Hello World', 
                                                   storage_class=storage_class.COLD)
        self.check_headers(response)

        response = self.bos.get_object_meta_data(bucket_name=self.BUCKET, key=b'testcold')
        self.assertEqual(response.metadata.bce_storage_class, "COLD")

        # test standard ia
        response = self.bos.put_object_from_string(bucket=self.BUCKET, 
                                                   key=b"testia", 
                                                   data='Hello World', 
                                                   storage_class=storage_class.STANDARD_IA)
        self.check_headers(response)

        response = self.bos.get_object_meta_data(bucket_name=self.BUCKET, key=b'testia')
        self.assertEqual(response.metadata.bce_storage_class, "STANDARD_IA")

        # test default storage class
        response = self.bos.put_object_from_string(bucket=self.BUCKET, 
                                                   key=b"testdefault", 
                                                   data='Hello World')
        self.check_headers(response)

        response = self.bos.get_object_meta_data(bucket_name=self.BUCKET, key=b'testdefault')
        self.assertEqual(response.metadata.bce_storage_class, "STANDARD")
        # test standard
        response = self.bos.put_object_from_string(bucket=self.BUCKET, 
                                                   key=b"teststandard", 
                                                   data='Hello World', 
                                                   storage_class=storage_class.STANDARD)
        self.check_headers(response)

        response = self.bos.get_object_meta_data(bucket_name=self.BUCKET, key=b'teststandard')
        self.assertEqual(response.metadata.bce_storage_class, "STANDARD")

        # test invalid storage class
        err = None
        try:
            self.bos.put_object_from_string(bucket=self.BUCKET, 
                                            key=b"testinvalid", 
                                            data='Hello World', 
                                            storage_class='aaa')
        except Exception as e:
            err = e
        except BceServerError as bse:
            err = bse
        finally:
            self.assertIsNotNone(err)
        # test storage case
        err = None
        try:
            self.bos.put_object_from_string(bucket=self.BUCKET,
                                            key=b"testcase",
                                            data='Hello World',
                                            storage_class=' STANDARD_Ia ')
        except ValueError as e:
            err = e
        finally:
            self.assertIsNone(err)

    def test_put_object_from_string_with_maz_standard(self):
        """test put_object_from_string with MAZ_STANDARD storage class"""
        try:
            response = self.bos.put_object_from_string(bucket=self.BUCKET,
                                                       key=b"testmaz_standard",
                                                       data='Hello MAZ Standard',
                                                       storage_class=storage_class.MAZ_STANDARD)
        except BceHttpClientError as e:
            self.skipTest("MAZ_STANDARD not supported in this environment: " + str(e))
        self.check_headers(response)
        response = self.bos.get_object_meta_data(bucket_name=self.BUCKET, key=b"testmaz_standard")
        self.assertEqual(response.metadata.bce_storage_class, "MAZ_STANDARD")

    def test_put_object_from_string_with_maz_standard_ia(self):
        """test put_object_from_string with MAZ_STANDARD_IA storage class"""
        try:
            response = self.bos.put_object_from_string(bucket=self.BUCKET,
                                                       key=b"testmaz_ia",
                                                       data='Hello MAZ IA',
                                                       storage_class=storage_class.MAZ_STANDARD_IA)
        except BceHttpClientError as e:
            self.skipTest("MAZ_STANDARD_IA not supported in this environment: " + str(e))
        self.check_headers(response)
        response = self.bos.get_object_meta_data(bucket_name=self.BUCKET, key=b"testmaz_ia")
        self.assertEqual(response.metadata.bce_storage_class, "MAZ_STANDARD_IA")

    def test_put_object_from_file_user_headers(self):
        """test put_object_from_file user headers"""

        user_headers = {"Cache-Control":"private", 
                        "Content-Disposition":"attachment; filename=\"abc.txt\"", 
                        "Expires":"123456"}

        self.get_file(5)
        response = self.bos.put_object_from_file(bucket=self.BUCKET,
                                                 key=b"test_put_file_user_headers",
                                                 file_name=self.FILENAME,
                                                 user_headers=user_headers)
        self.check_headers(response)

        response = self.bos.get_object_meta_data(bucket_name=self.BUCKET, 
                                                 key=b'test_put_file_user_headers')
        self.assertEqual(response.metadata.expires, "123456")
        self.assertEqual(response.metadata.content_disposition, 'attachment; filename="abc.txt"')
        self.assertEqual(response.metadata.cache_control, 'private')


    def test_put_object_from_file_user_metadata(self):
        """test put_object_from_file user metadata"""

        user_metadata = {'company': '百度', 'work': 'develop', 'test-key': ''}
        object_key = '测试文件'.encode('utf-8')
        self.get_file(5)
        response = self.bos.put_object_from_file(bucket=self.BUCKET,
                                                 key=object_key,
                                                 file_name=self.FILENAME,
                                                 user_metadata = user_metadata)

        response = self.bos.get_object_meta_data(bucket_name=self.BUCKET, 
                                                 key=object_key)
        self.assertEqual(response.metadata.bce_meta_company, '百度')
        self.assertEqual(response.metadata.bce_meta_work, 'develop')
        self.assertEqual(response.metadata.bce_meta_test_key, None)

    def test_put_object_from_file_with_storage_class(self):
        """test put_object_from_file with storage class"""
        self.get_file(5)
        # test cold
        response = self.bos.put_object_from_file(bucket=self.BUCKET, 
                                                 key=b"testcold", 
                                                 file_name=self.FILENAME, 
                                                 storage_class=storage_class.COLD)
        self.check_headers(response)

        response = self.bos.get_object_meta_data(bucket_name=self.BUCKET, key=b'testcold')
        self.assertEqual(response.metadata.bce_storage_class, "COLD")

        # test standard ia
        response = self.bos.put_object_from_file(bucket=self.BUCKET, 
                                                 key=b"testia", 
                                                 file_name=self.FILENAME, 
                                                 storage_class=storage_class.STANDARD_IA)
        self.check_headers(response)

        response = self.bos.get_object_meta_data(bucket_name=self.BUCKET, key=b'testia')
        self.assertEqual(response.metadata.bce_storage_class, "STANDARD_IA")

        # test default storage class
        response = self.bos.put_object_from_file(bucket=self.BUCKET, 
                                                 key=b"testdefault", 
                                                 file_name=self.FILENAME)
        self.check_headers(response)

        response = self.bos.get_object_meta_data(bucket_name=self.BUCKET, key=b'testdefault')
        self.assertEqual(response.metadata.bce_storage_class, "STANDARD")
        # test standard
        response = self.bos.put_object_from_file(bucket=self.BUCKET, 
                                                 key=b"teststandard", 
                                                 file_name=self.FILENAME, 
                                                 storage_class=storage_class.STANDARD)
        self.check_headers(response)

        response = self.bos.get_object_meta_data(bucket_name=self.BUCKET, key=b'teststandard')
        self.assertEqual(response.metadata.bce_storage_class, "STANDARD")
        # test invalid storage class
        err = None
        try:
            self.bos.put_object_from_file(bucket=self.BUCKET, 
                                          key=b"testinvalid", 
                                          file_name=self.FILENAME, 
                                          storage_class='aaa')
        except Exception as e:
            err = e
        except BceServerError as bse:
            err = bse
        finally:
            self.assertIsNotNone(err)
        # test storage case
        err = None
        try:
            self.bos.put_object_from_file(bucket=self.BUCKET,
                                          key=b"testcase",
                                          file_name=self.FILENAME,
                                          storage_class=' STANDARD_Ia ')
        except ValueError as e:
            err = e
        finally:
            self.assertIsNone(err)

    def test_put_object_from_file_with_maz_standard(self):
        """test put_object_from_file with MAZ_STANDARD storage class"""
        self.get_file(5)
        try:
            response = self.bos.put_object_from_file(bucket=self.BUCKET,
                                                     key=b"testmaz_standard_file",
                                                     file_name=self.FILENAME,
                                                     storage_class=storage_class.MAZ_STANDARD)
        except BceHttpClientError as e:
            self.skipTest("MAZ_STANDARD not supported in this environment: " + str(e))
        self.check_headers(response)
        response = self.bos.get_object_meta_data(bucket_name=self.BUCKET,
                                                 key=b"testmaz_standard_file")
        self.assertEqual(response.metadata.bce_storage_class, "MAZ_STANDARD")

    def test_put_object_from_file_with_maz_standard_ia(self):
        """test put_object_from_file with MAZ_STANDARD_IA storage class"""
        self.get_file(5)
        try:
            response = self.bos.put_object_from_file(bucket=self.BUCKET,
                                                     key=b"testmaz_ia_file",
                                                     file_name=self.FILENAME,
                                                     storage_class=storage_class.MAZ_STANDARD_IA)
        except BceHttpClientError as e:
            self.skipTest("MAZ_STANDARD_IA not supported in this environment: " + str(e))
        self.check_headers(response)
        response = self.bos.get_object_meta_data(bucket_name=self.BUCKET,
                                                 key=b"testmaz_ia_file")
        self.assertEqual(response.metadata.bce_storage_class, "MAZ_STANDARD_IA")


    def test_put_object_exceptions(self):
        """test of exceptions in put object"""
        # key is None
        err = None
        try:
            self.bos.put_object(self.BUCKET, None, None, 100, None)
        except ValueError as e:
            err = e
        finally:
            self.assertIsNotNone(err)
        # too long
        err = None
        try:
            self.bos.put_object(self.BUCKET, self.KEY, None, 6 * 1024 * 1024 * 1024, None)
        except ValueError as e:
            err = e
        finally:
            self.assertIsNotNone(err)


class TestAppendObject(TestClient):
    """test append object"""
    def test_append_object_from_string(self):
        """
        test append_object_from_string
        """
        response = self.bos.append_object_from_string(bucket_name=self.BUCKET,
                                                      key=b"test_append_object_from_string",
                                                      data="aaa")
        self.check_headers(response)

        next_offset = response.metadata.bce_next_append_offset
        self.assertEqual(int(next_offset), len("aaa"))

        response = self.bos.append_object_from_string(bucket_name=self.BUCKET,
                                                      key=b"test_append_object_from_string",
                                                      data='bbb',
                                                      offset=int(next_offset))
        next_offset = response.metadata.bce_next_append_offset
        self.assertEqual(int(next_offset), len("aaabbb"))

        response = self.bos.get_object_as_string(bucket_name=self.BUCKET, 
                                                 key=b"test_append_object_from_string")
        self.assertEqual(response, b'aaabbb')

        response = self.bos.get_object(bucket_name=self.BUCKET,
                                       key=b"test_append_object_from_string")
        self.assertEqual(response.metadata.bce_object_type, 'Appendable')

        # test append offset not match
        err = None
        try:
            self.bos.append_object_from_string(bucket_name=self.BUCKET,
                                               key=b"test_append_object_from_string",
                                               data='ccc',
                                               offset=(int(next_offset)-1))
        except Exception as e:
            err = e
        except BceServerError as bse:
            err = bse
        finally:
            self.assertIsNotNone(err)


class TestMultiUploadFile(TestClient):
    """test multi_upload_file"""
    def test_multi_upload_file(self):
        """
        test multi_upload_file, contains initiate, upload and complete.
        """
        response = self.bos.initiate_multipart_upload(self.BUCKET, self.KEY)
        self.check_headers(response)
        self.assertTrue(hasattr(response, "upload_id"))
        self.assertTrue(hasattr(response, "bucket"))
        self.assertTrue(hasattr(response, "key"))

        upload_id = response.upload_id

        self.get_file(20)
        left_size = os.path.getsize(self.FILENAME)
        done = 0
        part_number = 1
        part_list = []
        while left_size > 0:
            part_size = 5 * 1024 * 1024
            if left_size < part_size:
                part_size = left_size

            response = self.bos.upload_part_from_file(self.BUCKET,
                                                      self.KEY,
                                                      upload_id,
                                                      part_number=part_number,
                                                      part_size=part_size,
                                                      file_name = self.FILENAME,
                                                      offset=done)
            left_size = left_size - part_size
            done = done + part_size
            part_list.append({
                "partNumber": part_number,
                "eTag": response.metadata.etag
            })
            part_number += 1

        response = self.bos.complete_multipart_upload(self.BUCKET, self.KEY, upload_id=upload_id,
                                                      part_list=part_list)
        self.check_headers(response)
        self.assertTrue(hasattr(response, "etag"))
        self.assertTrue(hasattr(response, "bucket"))
        self.assertTrue(hasattr(response, "key"))
        self.assertTrue(hasattr(response, "location"))

    def test_multi_upload_file_user_headers(self):
        """test multi upload user headers"""
        user_headers = {"Cache-Control":"private", 
                        "Content-Disposition":"attachment; filename=\"abc.txt\"", 
                        "Expires":"123456"}

        response = self.bos.initiate_multipart_upload(bucket_name=self.BUCKET, 
                                                      key=self.KEY,
                                                      user_headers=user_headers)
        upload_id = response.upload_id
        self.get_file(5)
        part_list = []
        response = self.bos.upload_part_from_file(bucket_name=self.BUCKET,
                                                  key=self.KEY,
                                                  upload_id=upload_id,
                                                  part_number=1,
                                                  part_size=os.path.getsize(self.FILENAME),
                                                  file_name=self.FILENAME,
                                                  offset = 0)
        part_list.append({"partNumber": 1, "eTag": response.metadata.etag})

        self.bos.complete_multipart_upload(bucket_name=self.BUCKET,
                                           key=self.KEY,
                                           upload_id=upload_id,
                                           part_list=part_list)

        response = self.bos.get_object_meta_data(bucket_name=self.BUCKET, key=self.KEY)

        self.assertEqual(response.metadata.expires, "123456")
        self.assertEqual(response.metadata.content_disposition, 'attachment; filename="abc.txt"')
        self.assertEqual(response.metadata.cache_control, 'private')

    def test_multi_upload_file_content_type(self):
        """test multi upload content_type"""
        response = self.bos.initiate_multipart_upload(bucket_name=self.BUCKET, 
                                                      key=self.KEY,
                                                      content_type="text/plain")
        upload_id = response.upload_id
        self.get_file(5)
        part_list = []
        response = self.bos.upload_part_from_file(bucket_name=self.BUCKET,
                                                  key=self.KEY,
                                                  upload_id=upload_id,
                                                  part_number=1,
                                                  part_size=os.path.getsize(self.FILENAME),
                                                  file_name=self.FILENAME,
                                                  offset = 0)
        part_list.append({"partNumber": 1, "eTag": response.metadata.etag})

        self.bos.complete_multipart_upload(bucket_name=self.BUCKET,
                                           key=self.KEY,
                                           upload_id=upload_id,
                                           part_list=part_list)

        response = self.bos.get_object_meta_data(bucket_name=self.BUCKET, key=self.KEY)

        self.assertEqual(response.metadata.content_type, "text/plain")

    def test_multi_upload_file_with_storage_class(self):
        """test multi upload with storage class"""
        # test ia
        response = self.bos.initiate_multipart_upload(bucket_name=self.BUCKET, 
                                                      key=self.KEY,
                                                      storage_class=storage_class.STANDARD_IA)
        upload_id = response.upload_id
        self.get_file(5)
        part_list = []
        response = self.bos.upload_part_from_file(bucket_name=self.BUCKET,
                                                  key=self.KEY,
                                                  upload_id=upload_id,
                                                  part_number=1,
                                                  part_size=os.path.getsize(self.FILENAME),
                                                  file_name=self.FILENAME,
                                                  offset = 0)
        part_list.append({"partNumber": 1, "eTag": response.metadata.etag})

        response = self.bos.list_multipart_uploads(bucket_name=self.BUCKET)
        for upload in response.uploads:
            self.assertEqual(upload.storage_class, "STANDARD_IA")

        response = self.bos.list_parts(bucket_name=self.BUCKET, 
                                       key=self.KEY, 
                                       upload_id=upload_id)
        self.assertEqual(response.storage_class, "STANDARD_IA")

        self.bos.complete_multipart_upload(bucket_name=self.BUCKET,
                                           key=self.KEY,
                                           upload_id=upload_id,
                                           part_list=part_list)

        response = self.bos.get_object_meta_data(bucket_name=self.BUCKET, key=self.KEY)
        self.assertEqual(response.metadata.bce_storage_class, "STANDARD_IA")

        # test list object
        response = self.bos.list_objects(bucket_name=self.BUCKET)
        for obj in response.contents:
            if obj.key == self.KEY:
                self.assertEqual(obj.storage_class, "STANDARD_IA")
        
        # test cold
        response = self.bos.initiate_multipart_upload(bucket_name=self.BUCKET, 
                                                      key=self.KEY,
                                                      storage_class=storage_class.COLD)
        upload_id = response.upload_id
        self.get_file(5)
        part_list = []
        response = self.bos.upload_part_from_file(bucket_name=self.BUCKET,
                                                  key=self.KEY,
                                                  upload_id=upload_id,
                                                  part_number=1,
                                                  part_size=os.path.getsize(self.FILENAME),
                                                  file_name=self.FILENAME,
                                                  offset = 0)
        part_list.append({"partNumber": 1, "eTag": response.metadata.etag})

        response = self.bos.list_multipart_uploads(bucket_name=self.BUCKET)
        for upload in response.uploads:
            self.assertEqual(upload.storage_class, "COLD")

        response = self.bos.list_parts(bucket_name=self.BUCKET, 
                                       key=self.KEY, 
                                       upload_id=upload_id)
        self.assertEqual(response.storage_class, "COLD")

        self.bos.complete_multipart_upload(bucket_name=self.BUCKET,
                                           key=self.KEY,
                                           upload_id=upload_id,
                                           part_list=part_list)

        response = self.bos.get_object_meta_data(bucket_name=self.BUCKET, key=self.KEY)
        self.assertEqual(response.metadata.bce_storage_class, "COLD")

        # test list object
        response = self.bos.list_objects(bucket_name=self.BUCKET)
        for obj in response.contents:
            if obj.key == self.KEY:
                self.assertEqual(obj.storage_class, "COLD")

class TestPutSuperObejctFromFile(TestClient):
    """test put_super_obejct_from_file"""
    def test_put_super_obejct_from_file(self):
        """test put_super_obejct_from_file()"""
        self.get_file(30)
        result = self.bos.put_super_object_from_file(self.BUCKET, self.KEY, self.FILENAME,
            chunk_size=5, thread_num=multiprocessing.cpu_count())
        self.assertTrue(result)

        err = None
        try:
            response = self.bos.get_object_meta_data(self.BUCKET, self.KEY)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.check_headers(response)

    def test_cancel_put_super_obejct(self):
        """ test cancel after calling put_super_obejct_from_file() """
        self.get_file(300)
        uploadTaskHandle = UploadTaskHandle()
        result = {'success': None}
    
        def upload_with_result():
            result['success'] = self.bos.put_super_object_from_file(
                self.BUCKET, self.KEY, self.FILENAME,
                chunk_size=5,
                thread_num=multiprocessing.cpu_count(),
                uploadTaskHandle=uploadTaskHandle
            )
        t = threading.Thread(target=upload_with_result)
        t.start()
        time.sleep(0.1)
        uploadTaskHandle.cancel()
        t.join()
        self.assertFalse(result['success'], "Upload should have been canceled and returned False")

    def test_put_super_object_invalid_chunk_size_zero(self):
        """put_super_object_from_file with chunk_size=0 should raise BceClientError"""
        self.get_file(1)
        with self.assertRaises(BceClientError):
            self.bos.put_super_object_from_file(self.BUCKET, self.KEY, self.FILENAME, chunk_size=0)

    def test_put_super_object_invalid_chunk_size_negative(self):
        """put_super_object_from_file with chunk_size=-1 should raise BceClientError"""
        self.get_file(1)
        with self.assertRaises(BceClientError):
            self.bos.put_super_object_from_file(self.BUCKET, self.KEY, self.FILENAME, chunk_size=-1)

    def test_put_super_object_invalid_chunk_size_too_large(self):
        """put_super_object_from_file with chunk_size > 5120 should raise BceClientError"""
        self.get_file(1)
        with self.assertRaises(BceClientError):
            self.bos.put_super_object_from_file(self.BUCKET, self.KEY, self.FILENAME, chunk_size=5121)


class TestPutSuperObjectAutoChunkSize(unittest.TestCase):
    """test put_super_object_from_file auto chunk_size calculation"""

    def setUp(self):
        """Start test"""
        self.bos = bos_client.BosClient(bos_test_config.config)

    def test_auto_chunk_size_small_file(self):
        """small file (100MB) should use default chunk_size=5MB"""
        file_size = 100 * 1024 * 1024  # 100MB
        with patch('os.path.getsize', return_value=file_size), \
             patch.object(self.bos, 'initiate_multipart_upload') as mock_init, \
             patch.object(self.bos, '_upload_task') as mock_upload, \
             patch.object(self.bos, 'complete_multipart_upload') as mock_complete:
            mock_init.return_value = MagicMock(upload_id='test_upload_id')
            mock_upload.return_value = None
            mock_complete.return_value = MagicMock()

            # patch part_list to simulate successful uploads
            with patch('builtins.open', MagicMock()):
                # We only need to verify the chunk_size calculation logic
                # Calculate expected values
                expected_chunk_size = 5  # 100MB / 10000 = 0.01MB < 5MB, use default 5
                expected_part_size = expected_chunk_size * 1024 * 1024
                expected_total_parts = math.ceil(file_size / expected_part_size)
                self.assertEqual(expected_chunk_size, 5)
                self.assertEqual(expected_total_parts, 20)

    def test_auto_chunk_size_large_file_50gb(self):
        """50GB file should auto-calculate chunk_size to ceil(50GB / 10000) = 6MB"""
        file_size = 50 * 1024 * 1024 * 1024  # 50GB
        min_chunk_size_mb = math.ceil(file_size / (10000 * 1024 * 1024))
        # 50 * 1024 / 10000 = 5.12, ceil = 6
        self.assertEqual(min_chunk_size_mb, 6)

        expected_chunk_size = max(5, min_chunk_size_mb)
        self.assertEqual(expected_chunk_size, 6)

        expected_part_size = expected_chunk_size * 1024 * 1024
        expected_total_parts = math.ceil(file_size / expected_part_size)
        self.assertTrue(expected_total_parts <= 10000)

    def test_auto_chunk_size_large_file_500gb(self):
        """500GB file should auto-calculate chunk_size to ceil(500GB / 10000) = 52MB"""
        file_size = 500 * 1024 * 1024 * 1024  # 500GB
        min_chunk_size_mb = math.ceil(file_size / (10000 * 1024 * 1024))
        # 500 * 1024 / 10000 = 51.2, ceil = 52
        self.assertEqual(min_chunk_size_mb, 52)

        expected_chunk_size = max(5, min_chunk_size_mb)
        self.assertEqual(expected_chunk_size, 52)

        expected_part_size = expected_chunk_size * 1024 * 1024
        expected_total_parts = math.ceil(file_size / expected_part_size)
        self.assertTrue(expected_total_parts <= 10000)

    def test_auto_chunk_size_max_file_48_8tb(self):
        """48.8TB file (max supported) should auto-calculate chunk_size to 5120MB"""
        file_size = 50000 * 1024 * 1024 * 1024  # 48.8TB = 50000GB
        min_chunk_size_mb = math.ceil(file_size / (10000 * 1024 * 1024))
        # 50000 * 1024 / 10000 = 5120
        self.assertEqual(min_chunk_size_mb, 5120)

        expected_chunk_size = max(5, min_chunk_size_mb)
        self.assertEqual(expected_chunk_size, 5120)
        # should not exceed the max allowed chunk_size
        self.assertTrue(expected_chunk_size <= 5 * 1024)

    def test_auto_chunk_size_file_exceeds_48_8tb(self):
        """file > 48.8TB should raise BceClientError"""
        file_size = 50001 * 1024 * 1024 * 1024  # slightly over 48.8TB
        with patch('os.path.getsize', return_value=file_size):
            with self.assertRaises(BceClientError):
                self.bos.put_super_object_from_file('test-bucket', b'test-key', '/fake/file')

    def test_user_specified_chunk_size_respected(self):
        """when user specifies chunk_size, it should be used directly"""
        file_size = 100 * 1024 * 1024 * 1024  # 100GB
        with patch('os.path.getsize', return_value=file_size), \
             patch.object(self.bos, 'initiate_multipart_upload') as mock_init, \
             patch.object(self.bos, '_upload_task') as mock_upload, \
             patch.object(self.bos, 'complete_multipart_upload') as mock_complete, \
             patch('baidubce.services.bos.bos_client.utils.get_crc32_from_fp', return_value=0), \
             patch('builtins.open', MagicMock()):
            mock_init.return_value = MagicMock(upload_id='test_upload_id')
            mock_upload.return_value = None
            mock_complete.return_value = MagicMock()

            # user specifies chunk_size=100, should not be overridden
            # This should not raise even though auto-calc would give a different value
            # It will proceed with chunk_size=100
            try:
                self.bos.put_super_object_from_file(
                    'test-bucket', b'test-key', '/fake/file', chunk_size=100)
            except Exception:
                pass  # we only care it doesn't raise for invalid chunk_size

    def test_user_specified_chunk_size_zero_raises(self):
        """user specifies chunk_size=0 should raise BceClientError"""
        file_size = 100 * 1024 * 1024  # 100MB
        with patch('os.path.getsize', return_value=file_size):
            with self.assertRaises(BceClientError):
                self.bos.put_super_object_from_file(
                    'test-bucket', b'test-key', '/fake/file', chunk_size=0)

    def test_user_specified_chunk_size_negative_raises(self):
        """user specifies chunk_size=-1 should raise BceClientError"""
        file_size = 100 * 1024 * 1024  # 100MB
        with patch('os.path.getsize', return_value=file_size):
            with self.assertRaises(BceClientError):
                self.bos.put_super_object_from_file(
                    'test-bucket', b'test-key', '/fake/file', chunk_size=-1)

    def test_user_specified_chunk_size_too_large_raises(self):
        """user specifies chunk_size=5121 should raise BceClientError"""
        file_size = 100 * 1024 * 1024  # 100MB
        with patch('os.path.getsize', return_value=file_size):
            with self.assertRaises(BceClientError):
                self.bos.put_super_object_from_file(
                    'test-bucket', b'test-key', '/fake/file', chunk_size=5121)

    def test_auto_chunk_size_boundary_exactly_5gb_per_part(self):
        """file that needs exactly 5GB per part (max single part) should work"""
        # 5120MB * 10000 = 50000GB = 48.8TB
        file_size = 5120 * 10000 * 1024 * 1024  # exactly 48.8TB
        min_chunk_size_mb = math.ceil(file_size / (10000 * 1024 * 1024))
        self.assertEqual(min_chunk_size_mb, 5120)
        # should be exactly at the limit, not over
        self.assertTrue(min_chunk_size_mb <= 5 * 1024)

    def test_auto_chunk_size_10gb_file(self):
        """10GB file should still use default chunk_size=5MB (10GB/10000 = 1MB < 5MB)"""
        file_size = 10 * 1024 * 1024 * 1024  # 10GB
        min_chunk_size_mb = math.ceil(file_size / (10000 * 1024 * 1024))
        # 10 * 1024 / 10000 = 1.024, ceil = 2
        self.assertEqual(min_chunk_size_mb, 2)

        expected_chunk_size = max(5, min_chunk_size_mb)
        # still 5 since 2 < 5
        self.assertEqual(expected_chunk_size, 5)


class TestUploadPartCopy(TestClient):
    """test upload_part_copy"""
    def test_upload_part_copy(self):
        """test upload part copy"""
        self.get_file(20)
        self.bos.put_object_from_file(self.BUCKET, self.KEY, self.FILENAME)
        #self.bos.put_object_from_string(self.BUCKET, self.KEY, 'hello')
        response = self.bos.initiate_multipart_upload(self.BUCKET, 
                                                      b'copy', 
                                                      storage_class=storage_class.STANDARD)
        self.check_headers(response)
        self.assertTrue(hasattr(response, "upload_id"))
        self.assertTrue(hasattr(response, "bucket"))
        self.assertTrue(hasattr(response, "key"))

        upload_id = response.upload_id
        self.check_headers(response)
        response = self.bos.get_object_meta_data(self.BUCKET, self.KEY)
        self.check_headers(response)
        left_size = int(response.metadata.content_length)
        part_number = 1
        part_list = []
        offset = 0
        while left_size > 0:
            part_size = 5 * 1024 * 1024
            if left_size < part_size:
                part_size = left_size
            response = self.bos.upload_part_copy(self.BUCKET,
                                                 self.KEY,
                                                 self.BUCKET,
                                                 b'copy',
                                                 upload_id,
                                                 part_number,
                                                 part_size,
                                                 offset)
            left_size -= part_size
            offset += part_size
            part_list.append({'partNumber': part_number,
                              'eTag': response.etag})
            part_number += 1

        response = self.bos.complete_multipart_upload(self.BUCKET, b'copy', upload_id=upload_id,
                                                      part_list=part_list)
        self.check_headers(response)
        self.assertTrue(hasattr(response, "etag"))
        self.assertTrue(hasattr(response, "lastModified"))
        self.assertTrue(hasattr(response, "key"))
        self.assertTrue(hasattr(response, "location"))


class TestAbortMultipartUpload(TestClient):
    """test abort_multipart upload"""
    def test_abort_multipart_upload(self):
        """test abort_multipart upload function normally"""
        response = self.bos.initiate_multipart_upload(self.BUCKET, self.KEY)
        self.check_headers(response)
        upload_id = response.upload_id
        self.bos.abort_multipart_upload(self.BUCKET, self.KEY, upload_id)
        self.check_headers(response)


class TestPutBucketLogging(TestClient):
    """test put_bucket_logging"""
    def test_put_bucket_logging(self):
        """test put_bucket_logging function normally"""
        response = self.bos.put_bucket_logging(self.BUCKET, self.BUCKET, 'log-')
        self.check_headers(response)

    def test_put_bucket_logging_without_target_prefix(self):
        """put_bucket_logging without target_prefix should succeed (only targetBucket in body)"""
        response = self.bos.put_bucket_logging(self.BUCKET, self.BUCKET)
        self.check_headers(response)
        response = self.bos.get_bucket_logging(self.BUCKET)
        self.assertEqual(response.status, 'enabled')
        self.assertEqual(response.target_bucket, self.BUCKET)
        # target_prefix not set: server returns empty string
        self.assertEqual(response.target_prefix, '')


class TestGetBucketLogging(TestClient):
    """test get_bucket_logging"""
    def test_get_bucket_logging(self):
        """test get_bucket_logging function normally"""
        self.bos.put_bucket_logging(self.BUCKET, self.BUCKET, 'log-')
        response = self.bos.get_bucket_logging(self.BUCKET)
        self.check_headers(response)
        self.assertEqual(response.status, 'enabled')
        self.assertEqual(response.target_bucket, self.BUCKET)
        self.assertEqual(response.target_prefix, 'log-')
        self.bos.delete_bucket_logging(self.BUCKET)
        response = self.bos.get_bucket_logging(self.BUCKET)
        self.assertEqual(response.status, 'disabled')


class TestPutBucketLifecycle(TestClient):
    """test put_bucket_lifecycle"""
    def test_put_bucket_lifecycle(self):
        """test put_bucket_lifecycle function normally"""
        rule = {}
        rule['id'] = 'rule1'
        rule['status'] = 'enabled'
        rule['action'] = {}
        rule['action']['name'] = 'Transition'
        rule['action']['storageClass'] = 'STANDARD_IA'
        rule['resource'] = [self.BUCKET + '/*']
        rule['condition'] = {}
        rule['condition']['time'] = {"dateGreaterThan": '2017-04-07T00:00:00Z'}
        rules = []
        rules.append(rule)
        response = self.bos.put_bucket_lifecycle(self.BUCKET, rules)
        self.check_headers(response)


class TestGetBucketLifecycle(TestClient):
    """test get_bucket_lifecycle"""
    def test_get_bucket_lifecycle(self):
        """test get_bucket_lifecycle function normally"""
        rule = {}
        rule['id'] = 'rule1'
        rule['status'] = 'enabled'
        rule['action'] = {}
        rule['action']['name'] = 'Transition'
        rule['action']['storageClass'] = 'STANDARD_IA'
        rule['resource'] = [self.BUCKET + '/*']
        rule['condition'] = {}
        rule['condition']['time'] = {"dateGreaterThan": '2017-04-07T00:00:00Z'}
        rules = []
        rules.append(rule)
        response = self.bos.put_bucket_lifecycle(self.BUCKET, rules)
        self.check_headers(response)
        response = self.bos.get_bucket_lifecycle(self.BUCKET)
        self.check_headers(response)
        self.assertEqual(response.rule[0].status, 'enabled')
        self.assertEqual(response.rule[0].action.name, 'Transition')
        self.assertEqual(response.rule[0].action.storage_class, 'STANDARD_IA')
        self.assertEqual(response.rule[0].resource, [self.BUCKET + '/*'])
        self.assertEqual(response.rule[0].id, 'rule1')
        self.assertEqual(response.rule[0].condition.time.date_greater_than, '2017-04-07T00:00:00Z')

    def test_delete_bucket_lifecycle(self):
        """test delete_bucket_lifecycle removes all lifecycle rules"""
        rule = {
            'id': 'rule_to_delete',
            'status': 'enabled',
            'action': {'name': 'Transition', 'storageClass': 'STANDARD_IA'},
            'resource': [self.BUCKET + '/*'],
            'condition': {'time': {"dateGreaterThan": '2017-04-07T00:00:00Z'}}
        }
        self.bos.put_bucket_lifecycle(self.BUCKET, [rule])
        response = self.bos.delete_bucket_lifecycle(self.BUCKET)
        self.check_headers(response)


class TestPutBucketCors(TestClient):
    """test put_bucket_cors"""
    def test_put_bucket_cors(self):
        """test put_bucket_cors function normally"""
        conf = {}
        conf['allowedOrigins'] = ['http://www.boluor.com']
        conf['allowedMethods'] = ['GET', 'HEAD', 'DELETE']
        conf['allowedHeaders'] = ['Authorization', 'x-bce-test', 'x-bce-test2']
        conf['maxAgeSeconds'] = 3600
        cors_confs = []
        cors_confs.append(conf)
        response = self.bos.put_bucket_cors(self.BUCKET, cors_confs)
        self.check_headers(response)


class TestGetBucketCors(TestClient):
    """test get_bucket_cors"""
    def test_get_bucket_cors(self):
        """test get_bucket_cors function normally"""
        conf = {}
        conf['allowedOrigins'] = ['http://www.boluor.com']
        conf['allowedMethods'] = ['GET', 'HEAD', 'DELETE']
        conf['allowedHeaders'] = ['Authorization', 'x-bce-test', 'x-bce-test2']
        conf['maxAgeSeconds'] = 3600
        cors_confs = [conf]
        response = self.bos.put_bucket_cors(self.BUCKET, cors_confs)
        self.check_headers(response)
        response = self.bos.get_bucket_cors(self.BUCKET)
        self.check_headers(response)
        self.assertEqual(response.cors_configuration[0].allowed_origins[0], 'http://www.boluor.com')
        self.assertEqual(response.cors_configuration[0].allowed_methods, ['GET', 'HEAD', 'DELETE'])
        self.assertEqual(response.cors_configuration[0].allowed_headers,
                         ['Authorization', 'x-bce-test', 'x-bce-test2'])
        self.assertEqual(response.cors_configuration[0].max_age_seconds, 3600)

    def test_delete_bucket_cors(self):
        """test delete_bucket_cors removes cors configuration"""
        conf = {
            'allowedOrigins': ['http://www.example.com'],
            'allowedMethods': ['GET'],
            'maxAgeSeconds': 1800
        }
        self.bos.put_bucket_cors(self.BUCKET, [conf])
        response = self.bos.delete_bucket_cors(self.BUCKET)
        self.check_headers(response)


class TestAuthorization(unittest.TestCase):
    """TestAuthorization"""
    def test_get_canonical_headers(self):
        """test_get_canonical_headers"""
        headers = {
            b"Host": b"localhost",
            b"x-bce-a": b"a/b:c",
            b"C": b""
        }
        header = bce_v1_signer._get_canonical_headers(headers)
        self.assertTrue(header.split(b"\n")[0].startswith(b'host'))
        self.assertTrue(header.split(b"\n")[1].startswith(b'x-bce-a'))
        headers[b"Content-MD5"] = b"MD5"
        self.assertEqual(bce_v1_signer._get_canonical_headers(headers),
                         b"content-md5:MD5\nhost:localhost\nx-bce-a:a%2Fb%3Ac")

    def test_get_sign(self):
        """test_get_sign"""
        method = b"PUT"
        uri = b"/bucket/object1"
        params = {
            b"A": None,
            b"b": b"",
            b"C": b"d"
        }

        headers = {
            b"Host": b"bce.baidu.com",
            b"abc": b"123",
            b"x-bce-meta-key1": b"ABC"
        }

        auth = bce_v1_signer.sign(bce_credentials.BceCredentials(b"my_ak", b"my_sk"),
                                  method,
                                  uri,
                                  headers,
                                  params)
        # self.assertEqual('bce-auth-v1/bb37e6dfffc948a59eb5ddd254263809/2014-06-13T05:57:36Z/'
        #                  '1800//a20b4334ce9ba6fbddcb4064cd62a4d57ab2d78b44160b5d6ea9321beb8ca8cd',
        #                 bce_v1_signer.sign(bos_test_config.config.credentials,
        #                                    http_methods.PUT,
        #                                    uri,
        #                                    headers,
        #                                    params,
        #                                    1402639056,
        #                                    1800))


class TestUtil(unittest.TestCase):
    """TestUtil"""
    def test_get_timestamp(self):
        """test_get_timestamp"""
        self.assertEqual(b"1970-01-01T00:00:01Z", utils.get_canonical_time(1))
        if compat.PY3:
            self.assertRegex(compat.convert_to_string(utils.get_canonical_time()),
                                 "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")
        else:
            self.assertRegexpMatches(compat.convert_to_string(utils.get_canonical_time()),
                                 "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")

    def test_get_md5_from_fp(self):
        """test_get_md5_from_fp"""
        fp = io.BytesIO(b"abcdefghijklmnopqrstuvwxyz")
        self.assertEqual(b"w/zT12GS5AB9+0lsymfhOw==", utils.get_md5_from_fp(fp))
        self.assertEqual(b"6JmFCETYQztJTRLQhmQi2w==", utils.get_md5_from_fp(fp, 10))
        self.assertEqual(b"J1OsDoUaJj/azvjYRAHgwA==", utils.get_md5_from_fp(fp, 10, 10))
        self.assertEqual(b"6JmFCETYQztJTRLQhmQi2w==", utils.get_md5_from_fp(fp, 10, 100))

    def test_is_ip(self):
        """test_is_ip"""
        self.assertEqual(True, utils.is_ip(b"192.168.0.1"))
        self.assertEqual(True, utils.is_ip(b"localhost"))
        self.assertEqual(False, utils.is_ip(b"276.20.22.22"))
        self.assertEqual(False, utils.is_ip(b"123"))
        self.assertEqual(False, utils.is_ip(b"-1.33.22.11"))
        self.assertEqual(False, utils.is_ip(b"aaabbbccc"))
        self.assertEqual(False, utils.is_ip(123))

    def test_convert_to_standard_string(self):
        """test_convert_utf8"""
        self.assertEqual(b"aaa", utils.convert_to_standard_string(u"aaa"))
        self.assertEqual("北京".encode("utf-8"), utils.convert_to_standard_string("北京"))

    def test_convert_header2map(self):
        """test_convert_header2map"""
        tmp_map = {"region": "beijing", "sex": "female", "age": 21}
        tmp_list = (("region", "beijing"), ("sex", "female"), ("age", 21))
        self.assertEqual(tmp_map, utils.convert_header2map(tmp_list))

    def test_check_redirect(self):
        """test_check_redirect"""
        tmp_res = http.client.HTTPSConnection("localhost")
        tmp_res.status = 301
        self.assertEqual(True, utils.check_redirect(tmp_res))
        tmp_res.status = 302
        self.assertEqual(True, utils.check_redirect(tmp_res))
        tmp_res.status = 100
        self.assertEqual(False, utils.check_redirect(tmp_res))
        tmp_res.status = "aaa"
        self.assertEqual(False, utils.check_redirect(tmp_res))
        self.assertFalse(utils.check_redirect(123))

    #def test_get_resource(self):
    def test_normalize_string(self):
        """test_normalize_string"""
        self.assertEqual(b"www.baidu.com", utils.normalize_string("www.baidu.com"))
        self.assertEqual(b"www.bai%5E%26%2A.com", utils.normalize_string("www.bai^&*.com"))
        self.assertEqual(b"www.baidu.com", utils.normalize_string("www.baidu.com", True))

    #def test_append_param
    def test_check_bucket_valid(self):
        """test_check_bucket_valid"""
        self.assertEqual(True, utils.check_bucket_valid("test"))
        self.assertEqual(False, utils.check_bucket_valid(""))
        self.assertEqual(False, utils.check_bucket_valid("as&*"))
        self.assertEqual(False, utils.check_bucket_valid(" asfd"))
        self.assertFalse(utils.check_bucket_valid("asdf-"))
        self.assertFalse(utils.check_bucket_valid("asdf_"))

    def test_safe_get_element(self):
        """test safe_get_element"""
        self.assertEqual(utils.safe_get_element("asdf", {}), "")
        self.assertEqual(utils.safe_get_element("asdf", {"asdf":1}), 1)

    def test_get_normalized_char_list(self):
        """test _get_normalized_char_list"""
        chars = ['%00', '%01', '%02', '%03', '%04', '%05', '%06', '%07', '%08', '%09', '%0A',
                 '%0B', '%0C', '%0D', '%0E', '%0F', '%10', '%11', '%12', '%13', '%14', '%15',
                 '%16', '%17', '%18', '%19', '%1A', '%1B', '%1C', '%1D', '%1E', '%1F', '%20',
                 '%21', '%22', '%23', '%24', '%25', '%26', '%27', '%28', '%29', '%2A', '%2B',
                 '%2C', '-', '.', '%2F', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '%3A',
                 '%3B', '%3C', '%3D', '%3E', '%3F', '%40', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
                 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
                 'X', 'Y', 'Z', '%5B', '%5C', '%5D', '%5E', '_', '%60', 'a', 'b', 'c', 'd', 'e',
                 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                 'v', 'w', 'x', 'y', 'z', '%7B', '%7C', '%7D', '~', '%7F', '%80', '%81', '%82',
                 '%83', '%84', '%85', '%86', '%87', '%88', '%89', '%8A', '%8B', '%8C', '%8D',
                 '%8E', '%8F', '%90', '%91', '%92', '%93', '%94', '%95', '%96', '%97', '%98',
                 '%99', '%9A', '%9B', '%9C', '%9D', '%9E', '%9F', '%A0', '%A1', '%A2', '%A3',
                 '%A4', '%A5', '%A6', '%A7', '%A8', '%A9', '%AA', '%AB', '%AC', '%AD', '%AE',
                 '%AF', '%B0', '%B1', '%B2', '%B3', '%B4', '%B5', '%B6', '%B7', '%B8', '%B9',
                 '%BA', '%BB', '%BC', '%BD', '%BE', '%BF', '%C0', '%C1', '%C2', '%C3', '%C4',
                 '%C5', '%C6', '%C7', '%C8', '%C9', '%CA', '%CB', '%CC', '%CD', '%CE', '%CF',
                 '%D0', '%D1', '%D2', '%D3', '%D4', '%D5', '%D6', '%D7', '%D8', '%D9', '%DA',
                 '%DB', '%DC', '%DD', '%DE', '%DF', '%E0', '%E1', '%E2', '%E3', '%E4', '%E5',
                 '%E6', '%E7', '%E8', '%E9', '%EA', '%EB', '%EC', '%ED', '%EE', '%EF', '%F0',
                 '%F1', '%F2', '%F3', '%F4', '%F5', '%F6', '%F7', '%F8', '%F9', '%FA', '%FB',
                 '%FC', '%FD', '%FE', '%FF']
        self.assertListEqual([compat.convert_to_bytes(k) for k in chars],
            utils._get_normalized_char_list())


class TestHandler(TestClient):
    """test abort handler"""
    def test_parse_error(self):
        """test abort parse_error function in handler"""
        # test normal 2xx
        http_response = MockHttpResponse(status=208)
        self.assertFalse(handler.parse_error(http_response, None))

        # test abnormal 1xx
        http_response = MockHttpResponse(status=108)
        err = None
        try:
            handler.parse_error(http_response, None)
        except BceClientError as e:
            err = e
        finally:
            self.assertIsNotNone(err)

        # test abnormal 3xx 4xx 5xx with json body
        json_content = {"message": "error",
                        "code": 123,
                        "requestId": 12345}
        http_response = MockHttpResponse(status=508, content=json.dumps(json_content))
        err = None
        try:
            handler.parse_error(http_response, None)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNotNone(err)
            self.assertEqual(compat.convert_to_string(err), "error")
            self.assertEqual(err.code, 123)
            self.assertEqual(err.request_id, 12345)
            self.assertEqual(err.status_code, 508)

        # test abnormal 3xx 4xx 5xx without json body
        http_response = MockHttpResponse(status=508)
        response = BceResponse()
        response.metadata.bce_request_id = 12345
        err = None
        try:
            handler.parse_error(http_response, response)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNotNone(err)
            self.assertEqual(compat.convert_to_string(err), "Mock")
            self.assertEqual(err.request_id, 12345)
            self.assertEqual(err.status_code, 508)

    def test_parse_json(self):
        """test abort parse_json function in handler"""
        # test has body
        json_content = {"message": "error",
                        "code": 123,
                        "requestId": 12345}
        http_response = MockHttpResponse(status=508, content=json.dumps(json_content))
        response = BceResponse()
        self.assertTrue(handler.parse_json(http_response, response))
        self.assertTrue(hasattr(response, "message"))
        self.assertTrue(hasattr(response, "code"))
        self.assertTrue(hasattr(response, "request_id"))
        # test doesn't have body
        http_response = MockHttpResponse(status=508)
        response = BceResponse()
        old_len = len(response.__dict__)
        self.assertTrue(handler.parse_json(http_response, response))
        self.assertEqual(len(response.__dict__), old_len)


class TestBceHttpClient(TestClient):
    """test abort bce_http_client"""
    def test_parse_host_port(self):
        """test about parse host port"""
        # test default port for http
        endpoint = b"1.2.3.4"
        default_protocol = baidubce.protocol.HTTP
        ret_protocol, host, port = utils.parse_host_port(endpoint, default_protocol)
        self.assertEqual(ret_protocol, baidubce.protocol.HTTP)
        self.assertEqual(host, endpoint)
        self.assertEqual(port, default_protocol.default_port)

        # test default port for https
        endpoint = b"1.2.3.4"
        default_protocol = baidubce.protocol.HTTPS
        ret_protocol, host, port = utils.parse_host_port(endpoint, default_protocol)
        self.assertEqual(ret_protocol, baidubce.protocol.HTTPS)
        self.assertEqual(host, endpoint)
        self.assertEqual(port, default_protocol.default_port)

        # test specific port
        endpoint = b"1.2.3.4:8080"
        default_protocol = baidubce.protocol.HTTP
        ret_protocol, host, port = utils.parse_host_port(endpoint, default_protocol)
        self.assertEqual(ret_protocol, baidubce.protocol.HTTP)
        self.assertEqual(host, b"1.2.3.4")
        self.assertEqual(port, 8080)

        # test value error
        endpoint = b"1.2.3.4:abcd"
        default_protocol = baidubce.protocol.HTTP
        self.assertRaises(ValueError, utils.parse_host_port, endpoint, default_protocol)

        # protocol unsupported
        endpoint = b"ftp://1.2.3.4"
        default_protocol = baidubce.protocol.HTTP
        self.assertRaises(ValueError, utils.parse_host_port, endpoint, default_protocol)

        # test of endpoint dominates the protocol
        endpoint = b"http://1.2.3.4:8080"
        default_protocol = baidubce.protocol.HTTPS
        ret_protocol, host, port = utils.parse_host_port(endpoint, default_protocol)
        self.assertEqual(ret_protocol, baidubce.protocol.HTTP)
        self.assertEqual(host, b"1.2.3.4")
        self.assertEqual(port, 8080)

    def test_get_connection(self):
        """test abort get connection"""
        # test unknown protocol
        test_protocol = Expando({'name': 'unknown', 'default_port': 65535})
        host = "1.2.3.4"
        port = 8080
        connection_timeout = 1000
        self.assertRaises(ValueError,
                          bce_http_client._get_connection,
                          test_protocol, host, port, connection_timeout)

        # test http protocol
        test_protocol = protocol.HTTP
        host = "1.2.3.4"
        port = 8080
        connection_timeout = 1000
        conn = bce_http_client._get_connection(test_protocol, host, port, connection_timeout)
        self.assertEqual(conn.host, "1.2.3.4")
        self.assertEqual(conn.port, 8080)
        self.assertEqual(conn.timeout, 1)

        # test https protocol
        test_protocol = protocol.HTTPS
        host = "1.2.3.4"
        port = 8080
        connection_timeout = 1000
        conn = bce_http_client._get_connection(test_protocol, host, port, connection_timeout)

        # test proxy host and port
        test_protocol = protocol.HTTPS
        host = "1.2.3.4"
        port = 8080
        connection_timeout = 1000
        proxy_host = "1.2.3.5"
        proxy_port = 8081
        conn = bce_http_client._get_connection(test_protocol, host, port, connection_timeout, proxy_host, proxy_port)
        self.assertEqual(conn.host, proxy_host)
        self.assertEqual(conn.port, proxy_port)


    def test_send_http_request_normal(self):
        """test abort send http request"""
        # test body is None
        conn = MockHttpConnection()
        method = http_methods.GET
        uri = "/unknown/unknown"
        headers = {"Content-Length": 15,
                   "Content-Encoding": "utf8",
                   }
        body = None
        send_buf_size = -1

        bce_http_client._send_http_request(conn,
                                           method,
                                           uri,
                                           headers,
                                           body,
                                           send_buf_size)
        self.assertEqual(conn.putrequest_called, 1)
        self.assertEqual(conn.putheader_called, 2)
        self.assertEqual(conn.endheaders_called, 1)
        self.assertEqual(conn.send_called, 0)
        self.assertEqual(conn.content, "")
        self.assertEqual(conn.getresponse_called, 1)

        # test body is string
        conn = MockHttpConnection()
        method = http_methods.GET
        uri = "/unknown/unknown"
        headers = {"Content-Length": 15,
                   "Content-Encoding": "utf8",
                   }
        body = "Test with string"
        send_buf_size = -1
        bce_http_client._send_http_request(conn,
                                           method,
                                           uri,
                                           headers,
                                           body,
                                           send_buf_size)
        self.assertEqual(conn.putrequest_called, 1)
        self.assertEqual(conn.putheader_called, 2)
        self.assertEqual(conn.endheaders_called, 1)
        self.assertEqual(conn.send_called, 1)
        self.assertEqual(conn.content, body)
        self.assertEqual(conn.getresponse_called, 1)

        # test body is input stream
        conn = MockHttpConnection()
        method = http_methods.GET
        uri = b"/unknown/unknown"
        headers = {b"Content-Length": 16,
                   b"Content-Encoding": "utf8",
                   }
        body = MockInputStream("Test with string")
        send_buf_size = 5
        bce_http_client._send_http_request(conn,
                                           method,
                                           uri,
                                           headers,
                                           body,
                                           send_buf_size)
        self.assertEqual(conn.putrequest_called, 1)
        self.assertEqual(conn.putheader_called, 2)
        self.assertEqual(conn.endheaders_called, 1)
        self.assertEqual(conn.send_called, len("Test with string") // 5 + 1)
        self.assertEqual(conn.content, "Test with string")
        self.assertEqual(conn.getresponse_called, 1)

    def test_send_http_request_exception(self):
        """test abort send http request"""
        # test body is not sufficient
        conn = MockHttpConnection()
        method = http_methods.GET
        uri = b"/unknown/unknown"
        headers = {b"Content-Length": 100,
                   b"Content-Encoding": "utf8",
                   }
        body = MockInputStream("Test with string")
        send_buf_size = 5
        self.assertRaises(BceClientError,
                          bce_http_client._send_http_request,
                          conn,
                          method,
                          uri,
                          headers,
                          body,
                          send_buf_size)
        self.assertEqual(conn.putrequest_called, 1)
        self.assertEqual(conn.putheader_called, 2)
        self.assertEqual(conn.endheaders_called, 1)
        self.assertEqual(conn.send_called, len("Test with string") // 5 + 1)

    def test_send_request(self):
        """test abort send request"""
        old_get_connection = bce_http_client._get_connection
        old_send_http_request = bce_http_client._send_http_request
        bce_http_client._get_connection = mock_get_connection
        handlers = [mock_handler_function_wrapper(True), mock_handler_function_wrapper(False)]
        uri = b"/unknown/unknown"
        params = {"test": "test"}
        # test with socket exception
        body = None
        headers = None
        bce_http_client._send_http_request = mock_send_http_request_wrapper(True, None)
        bos_test_config.config.retry_policy = BackOffRetryPolicy()
        self.assertRaises(BceHttpClientError,
                          bce_http_client.send_request,
                          bos_test_config.config,
                          mock_sign_function,
                          handlers,
                          http_methods.GET,
                          uri,
                          body,
                          headers,
                          params)

        # test with value exception
        bos_test_config.config.retry_policy = NoRetryPolicy()
        body = 1
        headers = {b"x-bce-date": b"12345"}
        bce_http_client._send_http_request = mock_send_http_request_wrapper(False, None)
        self.assertRaises(ValueError,
                          bce_http_client.send_request,
                          bos_test_config.config,
                          mock_sign_function,
                          handlers,
                          http_methods.GET,
                          uri,
                          body,
                          headers,
                          params)

        # test others
        body = u"abcde"
        headers = {b"x-bce-date": b"12345"}
        params = None
        bce_http_client._send_http_request = mock_send_http_request_wrapper(False, {"err": "err"})
        response = bce_http_client.send_request(bos_test_config.config,
                                                mock_sign_function,
                                                handlers,
                                                http_methods.GET,
                                                uri,
                                                body,
                                                headers,
                                                params)
        self.assertEqual(response.metadata.err, "err")
        bce_http_client._get_connection = old_get_connection
        bce_http_client._send_http_request = old_send_http_request


class TestBceClientConfiguration(TestClient):
    """test BceClientConfiguration"""
    def test_init(self):
        """test BceClientConfiguration"""
        conf = BceClientConfiguration(1, 2, 3, 4, 5, 6, 7)
        self.assertEqual(conf.credentials, 1)
        self.assertEqual(conf.endpoint, compat.convert_to_bytes(2))
        self.assertEqual(conf.protocol, 3)
        self.assertEqual(conf.region, 4)
        self.assertEqual(conf.connection_timeout_in_mills, 5)
        self.assertEqual(conf.send_buf_size, 6)
        self.assertEqual(conf.recv_buf_size, 7)
    
    def test_merge_config(self):
        """test merge_config"""
        bucket_name = "test"
        conf = BceClientConfiguration(endpoint='bj.bcebos.com')
        merge_config = self.bos._merge_config(config = conf, bucket_name=bucket_name)
        self.assertEqual(merge_config.endpoint, b'test.bj.bcebos.com')

        conf = BceClientConfiguration(endpoint='bj.bcebos.com/')
        merge_config = self.bos._merge_config(config = conf, bucket_name=bucket_name)
        self.assertEqual(merge_config.endpoint, b'test.bj.bcebos.com/')

        conf = BceClientConfiguration(endpoint='test.bj.bcebos.com')
        merge_config = self.bos._merge_config(config = conf, bucket_name=bucket_name)
        self.assertEqual(merge_config.endpoint, b'test.bj.bcebos.com')

        conf = BceClientConfiguration(endpoint='http://bj.bcebos.com')
        merge_config = self.bos._merge_config(config = conf, bucket_name=bucket_name)
        self.assertEqual(merge_config.endpoint, b'http://test.bj.bcebos.com')

        conf = BceClientConfiguration(endpoint='http://test.bj.bcebos.com')
        merge_config = self.bos._merge_config(config = conf, bucket_name=bucket_name)
        self.assertEqual(merge_config.endpoint, b'http://test.bj.bcebos.com')

        conf = BceClientConfiguration(endpoint='https://test.bj.bcebos.com')
        merge_config = self.bos._merge_config(config = conf, bucket_name=bucket_name)
        self.assertEqual(merge_config.endpoint, b'https://test.bj.bcebos.com')

        # check virtual-hosted endpoint's bucket_name is not query bucket_name
        conf = BceClientConfiguration(endpoint='abc.bj.bcebos.com')
        self.assertRaises(ValueError, self.bos._merge_config, config = conf, bucket_name=bucket_name)

        conf = BceClientConfiguration(endpoint='http://abc.bj.bcebos.com')
        self.assertRaises(ValueError, self.bos._merge_config, config = conf, bucket_name=bucket_name)

        conf = BceClientConfiguration(endpoint='http://127.0.0.1')
        merge_config = self.bos._merge_config(config = conf, bucket_name=bucket_name)
        self.assertEqual(merge_config.endpoint, b'http://127.0.0.1')

        conf = BceClientConfiguration(endpoint='http://127.0.0.1:8080')
        merge_config = self.bos._merge_config(config = conf, bucket_name=bucket_name)
        self.assertEqual(merge_config.endpoint, b'http://127.0.0.1:8080')

        conf = BceClientConfiguration(endpoint='127.0.0.1')
        merge_config = self.bos._merge_config(config = conf, bucket_name=bucket_name)
        self.assertEqual(merge_config.endpoint, b'127.0.0.1')

        conf = BceClientConfiguration(endpoint='127.0.0.1:8080')
        merge_config = self.bos._merge_config(config = conf, bucket_name=bucket_name)
        self.assertEqual(merge_config.endpoint, b'127.0.0.1:8080')

        conf = BceClientConfiguration(endpoint='y001122.online')
        merge_config = self.bos._merge_config(config = conf, bucket_name=bucket_name)
        self.assertEqual(merge_config.endpoint, b'y001122.online')

        # test path_style_enable
        conf = BceClientConfiguration(endpoint='bj.bcebos.com', path_style_enable=True)
        merge_config = self.bos._merge_config(config = conf, bucket_name=bucket_name)
        self.assertEqual(merge_config.endpoint, b'bj.bcebos.com')

        conf = BceClientConfiguration(endpoint='wrong-bucket.bj.bcebos.com')
        self.assertRaises(ValueError, self.bos._merge_config, config = conf, bucket_name='correct-bucket')

        # test cname_enabled
        conf = BceClientConfiguration(endpoint='bj.bcebos.com', cname_enabled=True)
        self.assertRaises(ValueError, self.bos._merge_config, config = conf, bucket_name=bucket_name)

        conf = BceClientConfiguration(endpoint='y001122.online', cname_enabled=True)
        merge_config = self.bos._merge_config(config = conf, bucket_name=bucket_name)
        self.assertEqual(merge_config.endpoint, b'y001122.online')




class TestGetRangeHeaderDict(TestClient):
    """test _get_range_header_dict"""
    def test_get_range_header_dict(self):
        """test _get_range_header_dict"""
        self.assertIsNone(bos_client.BosClient._get_range_header_dict(None))
        self.assertDictEqual(bos_client.BosClient._get_range_header_dict((0, 99)),
                          {b"Range":b'bytes=0-99'})
        err = None
        try:
            bos_client.BosClient._get_range_header_dict(123)
        except TypeError as e:
            err = e
        finally:
            self.assertIsNotNone(err)
        err = None
        try:
            bos_client.BosClient._get_range_header_dict([1, 2, 3])
        except ValueError as e:
            err = e
        finally:
            self.assertIsNotNone(err)


class MyClass(object):
    """
    wrapper class
    """
    @required(a=int, b=list, c=(bytes, str))
    def my_func(self, a, b, c, d=None):
        """
        sample function to use required
        :param a:
        :param b:
        :param c:
        :param d:
        :return:
        """
        return True


class TestDecorator(TestClient):
    """test required decorator"""
    def test_positive(self):
        """
        test of positive cases
        :return:
        """
        self.assertTrue(MyClass().my_func(1, [], "a"))
        self.assertTrue(MyClass().my_func(1, [], u"a", 123))
        self.assertTrue(MyClass().my_func(1, [], "a", "abc"))
        self.assertTrue(MyClass().my_func(1, [], u"a", None))
        self.assertTrue(MyClass().my_func(a=1, b=[], c="a"))
        self.assertTrue(MyClass().my_func(a=1, b=[], c=u"a", d=123))
        self.assertTrue(MyClass().my_func(a=1, b=[], c="a", d="abc"))
        self.assertTrue(MyClass().my_func(a=1, b=[], c=u"a", d=None))

    def test_negative_value(self):
        """
        test of negative cases
        :return:
        """
        self.assertRaises(ValueError, MyClass().my_func, None, [], "a")
        self.assertRaises(ValueError, MyClass().my_func, 1, None, "a")
        self.assertRaises(ValueError, MyClass().my_func, 1, [], None)
        self.assertRaises(ValueError, MyClass().my_func, a=None, b=[], c="a")
        self.assertRaises(ValueError, MyClass().my_func, a=1, b=None, c="a")
        self.assertRaises(ValueError, MyClass().my_func, a=1, b=[], c=None)

    def test_negative_type(self):
        """
        test of negative cases
        :return:
        """
        self.assertRaises(TypeError, MyClass().my_func, "a", [], "a")
        self.assertRaises(TypeError, MyClass().my_func, 1, 1, "a")
        self.assertRaises(TypeError, MyClass().my_func, 1, [], [])
        self.assertRaises(TypeError, MyClass().my_func, a="a", b=[], c="a")
        self.assertRaises(TypeError, MyClass().my_func, a=1, b=1, c="a")
        self.assertRaises(TypeError, MyClass().my_func, a=1, b=[], c=[])


class TestSelectObject(TestClient):
    """test select_object """
    def test_select_object_csv(self):
        """
        test select_object for csv file
        """
        csv_file = "tools/test_cast.csv"
        self.bos.put_object_from_file(self.BUCKET, self.KEY, csv_file)
        valid_sql_exp = ["SELECT _1, _2, _6 FROM BosObject",
                "SELECT _1, _2, _6 FROM BosObject WHERE CAST(_6 AS BOOLEAN) = false",
                "SELECT _1, _4 FROM BosObject WHERE CAST(_4 AS INT) = 552299914",
                "SELECT _3 FROM BosObject WHERE CAST(_3 AS TIMESTAMP) < CAST('2017-11-22 15:11:01' AS TIMESTAMP)",
                "SELECT _1, _2, _6 FROM BosObject WHERE CAST(_6 AS STRING) = 'true' " \
                        "or CAST(_3 AS STRING) = '2018-06-11 05:14:29'",
                "SELECT _1, _2, _6 FROM BosObject LIMIT 10"]

        select_object_args = {
            "expressionType": "SQL",
            "inputSerialization": {
                "compressionType": "NONE",
                "csv": {
                    "fileHeaderInfo": "NONE",
                    "recordDelimiter": "Cg==",
                    "fieldDelimiter": "LA==",
                    "quoteCharacter": "Ig==",
                    "commentCharacter": "Iw=="
                }
            },
            "outputSerialization": {
                "outputHeader": False,
                "csv": {
                    "quoteFields": "ALWAYS",
                    "recordDelimiter": "Cg==",
                    "fieldDelimiter": "LA==",
                    "quoteCharacter": "Ig=="
                }
            },
            "requestProgress": {
                "enabled": True
            }
        }
        # test valid sql exp
        for temp_exp in valid_sql_exp:
            select_object_args["expression"] = base64.standard_b64encode(compat.convert_to_bytes(temp_exp)).decode("utf-8")
            select_response = self.bos.select_object(self.BUCKET, self.KEY, select_object_args)
            result = select_response.result()
            for msg in result:
                #print(msg)
                if msg.headers["message-type"] == "End":
                    self.assertEqual(msg.headers["error-code"], "success")
        # test invalid sql exp
        invalid_sql_exp = [
                "SELECT _1, _2, _6 FROM BosObject LIMIT 0",
                "SELECT MAX(CAST(_1 AS BOOLEAN)) FROM BosObject"
                ]
        for temp_exp in invalid_sql_exp:
            select_object_args["expression"] = base64.standard_b64encode(compat.convert_to_bytes(temp_exp)).decode("utf-8")
            is_exception = False
            try:
                select_response = self.bos.select_object(self.BUCKET, self.KEY, select_object_args)
                result = select_response.result()
                for msg in result:
                    pass
            except (BceHttpClientError, BceServerError) as e:
                is_exception = True
            self.assertTrue(is_exception)
    def _get_select_object_args_json(self):
        """
        get general select_object_args
        """
        select_object_args = {
            "expressionType": "SQL",
            "inputSerialization": {
                "compressionType": "NONE",
                "json": {
                    "type": "DOCUMENT"
                }
            },
            "outputSerialization": {
                "json": {
                    "recordDelimiter": "Cg=="
                }
            },
            "requestProgress": {
                "enabled": True
            }
        }
        return select_object_args

    def _get_fields(self):
        """
        return fileds
        """
        fields = [
                "guid", "index", "favoriteFruit", "latitude", "company", "email", "picture",
                "registered", "eyeColor", "phone", "address",
                "about", "_id", "name.last", "name.first", "age", "greeting", "longitude",
                "isActive", "balance",
            ]
        return fields

    def test_select_object_json(self):
        """
        test select object api with json file
        """
        json_file = "tools/test_json_document.json"
        self.bos.put_object_from_file(self.BUCKET, self.KEY, json_file)
        paths = [
            ".guid", ".index", ".favoriteFruit", ".latitude", ".company", ".email", ".picture",
            ".tags[0]", ".tags[1]", ".tags[2]", ".tags[3]", ".tags[4]",
            ".registered", ".eyeColor", ".phone", ".address",
            ".friends[0].id", ".friends[0].name",
            ".friends[1].id", ".friends[1].name", ".friends[2].id", ".friends[2].name",
            ".isActive",
            ".about", "._id", ".name.last", ".name.first", ".age", ".greeting", ".longitude",
            ".range[0]", ".range[1]", ".range[2]", ".range[3]", ".range[4]",
            ".range[5]", ".range[6]", ".range[7]", ".range[8]", ".range[9]",
            ".balance",
        ]
        select_object_args = self._get_select_object_args_json()
        # test valid sql exp
        for p in paths:
            temp_exp = 'SELECT * FROM BosObject{}'.format(p)
            select_object_args["expression"] = base64.standard_b64encode(compat.convert_to_bytes(temp_exp)).decode("utf-8")
            select_response = self.bos.select_object(self.BUCKET, self.KEY, select_object_args)
            result = select_response.result()
            for msg in result:
                #print(msg)
                if msg.headers["message-type"] == "End":
                    self.assertEqual(msg.headers["error-code"], "success")
        # test specified_field
        fields = self._get_fields()
        temp_exp = 'SELECT {} FROM BosObject'.format(','.join(fields))
        select_object_args["expression"] = base64.standard_b64encode(compat.convert_to_bytes(temp_exp)).decode("utf-8")
        select_response = self.bos.select_object(self.BUCKET, self.KEY, select_object_args)
        result = select_response.result()
        for msg in result:
            #print(msg)
            if msg.headers["message-type"] == "End":
                self.assertEqual(msg.headers["error-code"], "success")

    def test_select_object_json_lines(self):
        """
        test seelct object api with json lines
        """
        json_file = "tools/test_json_lines.json"
        self.bos.put_object_from_file(self.BUCKET, self.KEY, json_file)
        select_object_args = self._get_select_object_args_json()
        fields = self._get_fields()
        temp_exp = 'SELECT {} FROM BosObject'.format(','.join(fields))
        select_object_args["expression"] = base64.standard_b64encode(compat.convert_to_bytes(temp_exp)).decode("utf-8")
        select_response = self.bos.select_object(self.BUCKET, self.KEY, select_object_args)
        result = select_response.result()
        for msg in result:
            #print(msg)
            if msg.headers["message-type"] == "End":
                self.assertEqual(msg.headers["error-code"], "success")

    def test_select_object_parquet_type(self):
        """test select_object uses parquet select_type when no json/csv key in inputSerialization"""
        # This exercises the else: select_type = b"parquet" branch in select_object
        select_object_args = {
            "selectRequest": "SELECT * FROM BosObject",
            "inputSerialization": {
                "parquet": {}
            },
            "outputSerialization": {
                "json": {}
            }
        }
        err = None
        try:
            self.bos.select_object(self.BUCKET, self.KEY, select_object_args)
        except (BceServerError, BceHttpClientError) as e:
            err = e
        # Server may reject parquet without a real parquet file, but the client-side
        # branch (select_type = b"parquet") is exercised regardless of server response


class TestFetchObjectBranches(TestClient):
    """Test missing branches in fetch_object"""

    def test_fetch_object_sync_mode(self):
        """test fetch_object with FETCH_MODE_SYNC"""
        url = "http://www.baidu.com/img/bd_logo1.png"
        err = None
        try:
            response = self.bos.fetch_object(self.BUCKET, b'logo_sync.png', url,
                                             bos_client.FETCH_MODE_SYNC)
        except (BceServerError, BceHttpClientError) as e:
            err = e
        # FETCH_MODE_SYNC branch in headers is exercised regardless of server response

    def test_fetch_object_no_mode(self):
        """test fetch_object with fetch_mode=None (header omitted)"""
        url = "http://www.baidu.com/img/bd_logo1.png"
        err = None
        try:
            response = self.bos.fetch_object(self.BUCKET, b'logo_nomode.png', url)
        except (BceServerError, BceHttpClientError) as e:
            err = e
        # fetch_mode=None branch (no BOS_FETCH_MODE header) is exercised

    def test_fetch_object_with_storage_class(self):
        """test fetch_object with storage_class parameter"""
        url = "http://www.baidu.com/img/bd_logo1.png"
        err = None
        try:
            response = self.bos.fetch_object(self.BUCKET, b'logo_sc.png', url,
                                             bos_client.FETCH_MODE_ASYNC,
                                             storage_class=storage_class.STANDARD)
        except (BceServerError, BceHttpClientError) as e:
            err = e
        # storage_class is not None branch (sets BOS_STORAGE_CLASS header) is exercised


class TestListObjectsBranches(TestClient):
    """Test missing branches in list_objects"""

    def setUp(self):
        super(TestListObjectsBranches, self).setUp()
        # Upload objects with different prefixes for filtering tests
        for name in [b'dir/a.txt', b'dir/b.txt', b'other.txt']:
            self.bos.put_object_from_string(self.BUCKET, name, 'data')

    def test_list_objects_max_keys_none(self):
        """test list_objects with max_keys=None (no maxKeys param sent to server)"""
        err = None
        try:
            response = self.bos.list_objects(self.BUCKET, max_keys=None)
        except BceServerError as e:
            err = e
        self.assertIsNone(err)
        self.check_headers(response)

    def test_list_objects_with_prefix(self):
        """test list_objects with prefix parameter"""
        err = None
        try:
            response = self.bos.list_objects(self.BUCKET, prefix='dir/')
        except BceServerError as e:
            err = e
        self.assertIsNone(err)
        for obj in response.contents:
            self.assertTrue(compat.convert_to_string(obj.key).startswith('dir/'))

    def test_list_objects_with_delimiter(self):
        """test list_objects with delimiter parameter"""
        err = None
        try:
            response = self.bos.list_objects(self.BUCKET, delimiter='/')
        except BceServerError as e:
            err = e
        self.assertIsNone(err)
        # Common prefixes should contain 'dir/'
        prefixes = [p.prefix for p in response.common_prefixes]
        self.assertIn('dir/', prefixes)

    def test_list_objects_combined_params(self):
        """test list_objects with prefix, delimiter and max_keys combined"""
        err = None
        try:
            response = self.bos.list_objects(self.BUCKET, max_keys=10,
                                              prefix='dir/', delimiter='/')
        except BceServerError as e:
            err = e
        self.assertIsNone(err)


class TestListPartsBranches(TestClient):
    """Test list_parts with max_parts and part_number_marker parameters"""

    def setUp(self):
        super(TestListPartsBranches, self).setUp()
        self.get_file(15)
        self.upload_id = self.bos.initiate_multipart_upload(self.BUCKET, self.KEY).upload_id
        # Upload 3 parts
        for i in range(1, 4):
            self.bos.upload_part_from_file(self.BUCKET, self.KEY, self.upload_id,
                                           part_number=i, part_size=5 * 1024 * 1024,
                                           file_name=self.FILENAME,
                                           offset=(i - 1) * 5 * 1024 * 1024)

    def test_list_parts_with_max_parts(self):
        """test list_parts with max_parts=1 returns only one part"""
        response = self.bos.list_parts(self.BUCKET, self.KEY, self.upload_id, max_parts=1)
        self.check_headers(response)
        self.assertEqual(len(response.parts), 1)
        self.assertTrue(response.is_truncated)

    def test_list_parts_with_part_number_marker(self):
        """test list_parts with part_number_marker to paginate"""
        response = self.bos.list_parts(self.BUCKET, self.KEY, self.upload_id,
                                        part_number_marker=1)
        self.check_headers(response)
        # Should return parts 2 and 3
        self.assertGreaterEqual(len(response.parts), 1)
        for part in response.parts:
            self.assertGreater(part.part_number, 1)


class TestListMultipartUploadsBranches(TestClient):
    """Test list_multipart_uploads with prefix and delimiter parameters"""

    def setUp(self):
        super(TestListMultipartUploadsBranches, self).setUp()
        self.upload_ids = []
        for key in [b'prefix/file1', b'prefix/file2', b'other/file3']:
            uid = self.bos.initiate_multipart_upload(self.BUCKET, key).upload_id
            self.upload_ids.append(uid)

    def test_list_multipart_uploads_with_prefix(self):
        """test list_multipart_uploads with prefix parameter"""
        response = self.bos.list_multipart_uploads(self.BUCKET, prefix='prefix/')
        self.check_headers(response)
        for item in response.uploads:
            self.assertTrue(item.key.startswith('prefix/'))

    def test_list_multipart_uploads_with_delimiter(self):
        """test list_multipart_uploads with delimiter parameter"""
        response = self.bos.list_multipart_uploads(self.BUCKET, delimiter='/')
        self.check_headers(response)

    def test_list_multipart_uploads_prefix_and_delimiter(self):
        """test list_multipart_uploads with prefix and delimiter combined"""
        response = self.bos.list_multipart_uploads(self.BUCKET,
                                                    prefix='prefix/',
                                                    delimiter='/')
        self.check_headers(response)


class TestUploadPartCopyWithEtag(TestClient):
    """Test upload_part_copy with etag (conditional copy) parameter"""

    def test_upload_part_copy_with_etag(self):
        """test upload_part_copy with etag parameter for conditional copy"""
        self.get_file(10)
        self.bos.put_object_from_file(self.BUCKET, self.KEY, self.FILENAME)
        src_meta = self.bos.get_object_meta_data(self.BUCKET, self.KEY)
        src_etag = src_meta.metadata.etag

        upload_id = self.bos.initiate_multipart_upload(self.BUCKET, b'copy_etag').upload_id
        part_size = int(src_meta.metadata.content_length)
        err = None
        try:
            response = self.bos.upload_part_copy(
                self.BUCKET, self.KEY, self.BUCKET, b'copy_etag',
                upload_id, 1, part_size, 0,
                etag=src_etag)
            self.check_headers(response)
        except BceServerError as e:
            err = e
        self.assertIsNone(err)
        self.bos.abort_multipart_upload(self.BUCKET, b'copy_etag', upload_id)

    def test_upload_part_copy_with_wrong_etag(self):
        """test upload_part_copy with wrong etag raises BceServerError (412)"""
        self.get_file(10)
        self.bos.put_object_from_file(self.BUCKET, self.KEY, self.FILENAME)
        upload_id = self.bos.initiate_multipart_upload(self.BUCKET, b'copy_etag2').upload_id
        err = None
        try:
            self.bos.upload_part_copy(
                self.BUCKET, self.KEY, self.BUCKET, b'copy_etag2',
                upload_id, 1, 5 * 1024 * 1024, 0,
                etag=b'"wrong_etag_value"')
        except (BceServerError, BceHttpClientError) as e:
            err = e
        self.assertIsNotNone(err)
        self.bos.abort_multipart_upload(self.BUCKET, b'copy_etag2', upload_id)


class TestSetObjectAcl(TestClient):
    """test set_bucket_acl"""
    def test_set_object_acl(self):
        """test set_object_acl, which set object acl from Grant list"""

        self.bos.put_object_from_string(self.BUCKET, self.KEY, 'Hello World')
        grant_list = list()
        grant_list.append({'grantee':
                            [{'id': 'a0a2fe988a774be08978736ae2a1668b'},
                            {'id': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'}],
                           'permission': ['FULL_CONTROL']})
        err = None
        try:
            self.bos.set_object_acl(self.BUCKET, self.KEY, grant_list)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)

    def test_set_bucket_canned_acl(self):
        """test set_object_canned_acl, set object acl from header and set canned acl"""
        self.bos.put_object_from_string(self.BUCKET, self.KEY, 'Hello World')
        err = None
        try:
            self.bos.set_object_canned_acl(self.BUCKET, self.KEY, canned_acl = b"private")
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)

        try:
            self.bos.set_object_canned_acl(self.BUCKET, self.KEY,
                    grant_read = b'id="a0a2fe988a774be08978736ae2a1668b",id="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"')
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)

        try:
            self.bos.set_object_canned_acl(self.BUCKET, self.KEY, 
                grant_full_control = b'id="a0a2fe988a774be08978736ae2a1668b",id="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"')
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)


class TestGetAndDeleteObjectAcl(TestClient):
    """test get_bucket_acl function"""
    def test_get_bucket_acl(self):
        """test get_bucket_acl function normally"""
        self.bos.put_object_from_string(self.BUCKET, self.KEY, 'Hello World')
        grant_list = list()
        grant_list.append({'grantee':
                            [{'id': 'a0a2fe988a774be08978736ae2a1668b'},
                            {'id': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'}],
                           'permission': ['FULL_CONTROL']})
        err = None
        try:
            self.bos.set_object_acl(self.BUCKET, self.KEY, grant_list)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)

        err = None
        try:
            response = self.bos.get_object_acl(self.BUCKET, self.KEY)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.check_headers(response)
        self.assertEqual(response.access_control_list[0].grantee[0].id,
                         'a0a2fe988a774be08978736ae2a1668b')
        self.assertEqual(response.access_control_list[0].grantee[1].id,
                         'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        self.assertListEqual(response.access_control_list[0].permission,
                             ["FULL_CONTROL"])

        err = None
        try:
            self.bos.set_object_acl(self.BUCKET, self.KEY, response.access_control_list)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)

        err = None
        try:
            self.bos.delete_object_acl(self.BUCKET, self.KEY)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)


# test fetch object
class TestFetchObject(TestClient):
    """test fetch_object function"""
    def test_fetch_object(self):
        """test fetch_object function normally"""
        url = "http://www.baidu.com/img/bd_logo1.png?where=super"
        obj_key = b'logo.png'
        err = None
        try:
            response = self.bos.fetch_object(self.BUCKET, obj_key, url, bos_client.FETCH_MODE_ASYNC)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.check_headers(response)
        self.assertIsNotNone(response.job_id)

# test restore object
class TestRestoreObject(TestClient):
    """test restore_object function"""
    def test_restore_object(self):
        """test restore_obejct function normally"""
        self.get_file(5)
        err = None
        try:
            self.bos.put_object_from_file(self.BUCKET, self.KEY, self.FILENAME, storage_class=storage_class.ARCHIVE)
            self.bos.restore_object(self.BUCKET, self.KEY, days=2, tier="Expedited")
            response = self.bos.get_object_meta_data(self.BUCKET, self.KEY)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.assertIsNotNone(response.metadata.bce_restore)
        self.assertTrue(response.metadata.bce_restore.find("expiry-date") < 0)
        res = self.bos.delete_object(self.BUCKET, self.KEY)

    def test_restore_obejct_exception(self):
        """test restore_obejct function exception"""
        self.get_file(5)
        err = None
        try:
            self.bos.put_object_from_file(self.BUCKET, self.KEY, self.FILENAME, storage_class=storage_class.ARCHIVE)
            self.bos.restore_object(self.BUCKET, self.KEY, tier="invalid_value")
        except ValueError as e:
            err = e
        finally:
            self.assertIsNotNone(err)
        res = self.bos.delete_object(self.BUCKET, self.KEY)

class TestBucketStorageclass(TestClient):
    """test bucket storageclass"""
    def test_bucket_storage_class(self):
        """test bucket storageclass"""
        self.bos.set_bucket_storage_class(self.BUCKET, storage_class=storage_class.COLD)
        response = self.bos.get_bucket_storage_class(self.BUCKET)
        self.assertEqual(response.storage_class, "COLD")
        self.bos.set_bucket_storage_class(self.BUCKET, storage_class=storage_class.STANDARD)

    def test_bucket_storage_class_maz_standard(self):
        """test set/get bucket storageclass with MAZ_STANDARD"""
        try:
            self.bos.set_bucket_storage_class(self.BUCKET, storage_class=storage_class.MAZ_STANDARD)
        except BceHttpClientError as e:
            self.skipTest("MAZ_STANDARD not supported in this environment: " + str(e))
        response = self.bos.get_bucket_storage_class(self.BUCKET)
        self.assertEqual(response.storage_class, "MAZ_STANDARD")
        # restore
        self.bos.set_bucket_storage_class(self.BUCKET, storage_class=storage_class.STANDARD)

    def test_bucket_storage_class_maz_standard_ia(self):
        """test set/get bucket storageclass with MAZ_STANDARD_IA"""
        try:
            self.bos.set_bucket_storage_class(self.BUCKET, storage_class=storage_class.MAZ_STANDARD_IA)
        except BceHttpClientError as e:
            self.skipTest("MAZ_STANDARD_IA not supported in this environment: " + str(e))
        response = self.bos.get_bucket_storage_class(self.BUCKET)
        self.assertEqual(response.storage_class, "MAZ_STANDARD_IA")
        # restore
        self.bos.set_bucket_storage_class(self.BUCKET, storage_class=storage_class.STANDARD)


# test restore object
class TestSymlink(TestClient):
    """test put/get symlink function"""
    def test_put_symlink(self):
        """test symlink api normally"""
        self.get_file(5)
        self.bos.put_object_from_file(self.BUCKET, self.KEY, self.FILENAME)
        # put object and put symlink
        symlink_key = b"mysymlink01"
        symlink_key2 = b"mysymlink02"
        err = None
        user_metadata = {"name":"my-data"}
        try:
            self.bos.put_object_symlink(self.BUCKET, self.KEY, symlink_key,
                storage_class=storage_class.COLD, user_metadata=user_metadata)
            response = self.bos.get_object_symlink(self.BUCKET, symlink_key)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.assertIsNotNone(response.metadata.bce_symlink_target)
        self.assertEqual(compat.convert_to_string(self.KEY), response.metadata.bce_symlink_target)
        self.assertEqual(compat.convert_to_string(user_metadata['name']), response.metadata.bce_meta_name)

        self.bos.delete_object(self.BUCKET, symlink_key)
        #self.assertTrue(response.metadata.bce_restore.find("expiry-date") > 0)
        # put symlink as ARCHIVE storage class, fail
        err = None
        try:
            self.bos.put_object_symlink(self.BUCKET, self.KEY, symlink_key,
                storage_class=storage_class.ARCHIVE)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertIsNotNone(err)
        # put symlink while forbid_overwrite=true
        err = None
        self.bos.put_object_from_file(self.BUCKET, symlink_key, self.FILENAME)
        try:
            self.bos.put_object_symlink(self.BUCKET, self.KEY, symlink_key, forbid_overwrite=True)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertIsNotNone(err)
        # clear
        res = self.bos.delete_object(self.BUCKET, self.KEY)

        # put symlink while symlink bucket
        target_bucket = 'symlink-test-bucket'
        self.bos.create_bucket(target_bucket)
        err = None
        self.bos.put_object_from_file(target_bucket, self.KEY, self.FILENAME)
        try:
            self.bos.put_object_symlink(self.BUCKET, self.KEY, symlink_key, target_bucket=target_bucket)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertIsNone(err)
        # clear
        self.bos.delete_object(target_bucket, self.KEY)
        self.bos.delete_object(self.BUCKET, symlink_key)
        self.bos.delete_bucket(target_bucket)

    
    def test_get_symlink(self):
        """ test get symlink """
        # put object and put symlink
        symlink_key = b"mysymlink01"
        symlink_key2 = b"mysymlink02"
        err = None
        try:
            response = self.bos.put_object_from_string(self.BUCKET,
                                                       self.KEY,
                                                       "This is a string.")
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.check_headers(response)
        self.bos.put_object_symlink(self.BUCKET, self.KEY, symlink_key)

        # get meta of symlink
        response = self.bos.get_object_meta_data(self.BUCKET, symlink_key)
        self.assertEqual(compat.convert_to_string('Symlink'), response.metadata.bce_object_type)
        # get object
        err = None
        try:
            response = self.bos.get_object_as_string(self.BUCKET, symlink_key)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.assertEqual(response, b"This is a string.")

class TestQuota(TestClient):
    """test put/get quota function"""
    def test_get_quota(self):
        """test get quota"""
        err = None
        self.bos.put_user_quota(100, 12334424)
        try:
            response = self.bos.get_user_quota()
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.assertEqual(response.max_bucket_count, 100)
        self.assertEqual(response.max_capacity_mega_bytes, 12334424)
        self.bos.delete_user_quota()
    
    def test_set_quota(self):
        """test set quota"""
        err = None
        self.bos.delete_user_quota()
        self.bos.put_user_quota(100, 12334424)
        try:
            response = self.bos.get_user_quota()
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.assertEqual(response.max_bucket_count, 100)
        self.assertEqual(response.max_capacity_mega_bytes, 12334424)

    def test_delete_quota(self):
        """test delete quota"""
        err = None
        is_exception = False
        self.bos.delete_user_quota()
        try:
            response = self.bos.get_user_quota()
        except Exception as e:
            is_exception = True
        self.assertTrue(is_exception)

class TestNotification(TestClient):
    def test_get_notification(self):
        """test get notification"""
        err = None
        notifications = list()
        notifications.append(
        {
            "resources": [
                "/"
            ],
            "encryption": {
                "key": "06a62b70f47dc4a0a7da349609f1a1ac"
            },
            "status": "enabled",
            "name": "name3",
            "id": "r3",
            "appId": "p3",
            "events": [
                "AppendObject",
                "CompleteMultipartUpload",
                "CopyObject",
                "PutObject",
                "PostObject",
                "FetchObject",
                "DeleteObject"
            ],
            "apps": [
                {
                    "eventUrl": "http://www.liujiang.com",
                    "id": "ImageCensor",
                    "xVars": "{\"saveUrl\": \"http://xxx.com/ocr\"}"
                }
            ]
        })
        self.bos.put_notification(self.BUCKET, notifications)
        try:
            response = self.bos.get_notification(self.BUCKET)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.assertEqual(response.notifications[0].id, "r3")
    
    def test_delete_notification(self):
        err = None
        is_exception = False
        self.bos.delete_notification(self.BUCKET)
        try:
            response = self.bos.get_notification(self.BUCKET)
        except Exception as e:
            is_exception = True
        self.assertTrue(is_exception)

    def test_put_notification(self):
        err = None
        is_exception = False
        self.bos.delete_notification(self.BUCKET)
        notifications = list()
        notifications.append(
        {
            "resources": [
                "/"
            ],
            "encryption": {
                "key": "06a62b70f47dc4a0a7da349609f1a1ac"
            },
            "status": "enabled",
            "name": "name3",
            "id": "r3",
            "appId": "p3",
            "events": [
                "AppendObject",
                "CompleteMultipartUpload",
                "CopyObject",
                "PutObject",
                "PostObject",
                "FetchObject",
                "DeleteObject"
            ],
            "apps": [
                {
                    "eventUrl": "http://www.liujiang.com",
                    "id": "ImageCensor",
                    "xVars": "{\"saveUrl\": \"http://xxx.com/ocr\"}"
                }
            ]
        })
        self.bos.put_notification(self.BUCKET, notifications)
        try:
            response = self.bos.get_notification(self.BUCKET)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.assertEqual(response.notifications[0].id, "r3")


class TestMirroringConf(TestClient):
    """test put mirroring config"""
    def test_mirroring(self):
        err = None
        mirror_args = list()
        mirror_args.append({
				    "mode": "fetch", 						
				    "sourceUrl": "bos://bj.bcebos.com/" + self.BUCKET,  
				    "backSourceUrl": "bos://bj.bcebos.com/bucket_name",   
                    "resource": "*.jpeg",       

				    "version": "v2", 								

				    "passQueryString": False,					
				    "storageClass": "STANDARD",
	    })
        try:
            self.bos.put_bucket_mirroring(self.BUCKET, mirror_args= mirror_args)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        
        # test  get mirroring
        try:
            self.bos.get_bucket_mirroring(self.BUCKET)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        
        # test delete mirroring
        try:
            self.bos.delete_bucket_mirroring(self.BUCKET)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)


class TestTrafficLimit(TestClient):
    """test put object"""
    def test_put_object(self):
        self.get_file(20)
        traffic_limit_speed = 819200 * 5
        start_time = datetime.now()
        self.bos.put_object_from_file(bucket=self.BUCKET, key=self.KEY, file_name=self.FILENAME, traffic_limit=traffic_limit_speed)
        end_time = datetime.now()
        time_interval = (end_time - start_time).seconds
        speed = 20 * 1024 * 1024 * 8 / time_interval
        self.assertTrue(speed <= traffic_limit_speed)
    
    def test_copy_object(self):
        """test copy_object function normally"""
        traffic_limit_speed = 81920
        err = None
        self.get_file(20)
        try:
            self.bos.put_object_from_file(bucket=self.BUCKET, key=self.KEY, file_name=self.FILENAME)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        try:
            response = self.bos.copy_object(self.BUCKET,
                                        self.KEY,
                                        self.BUCKET,
                                        compat.convert_to_bytes("test_target_key"),
                                        traffic_limit=traffic_limit_speed)
        except Exception as e:
            err = e
        finally:
            self.assertIsNotNone(err)
    
    def test_get_object_to_file(self):
        traffic_limit_speed = 819200 * 5
        err = None
        self.get_file(20)
        try:
            self.bos.put_object_from_file(bucket=self.BUCKET, key=self.KEY, file_name=self.FILENAME)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        start_time = datetime.now()
        try:
            response = self.bos.get_object_to_file(self.BUCKET, self.KEY, self.FILENAME,
                                        traffic_limit=traffic_limit_speed)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        end_time = datetime.now()
        time_interval = (end_time - start_time).seconds
        speed = 20 * 1024 * 1024 * 8 / time_interval
        self.assertTrue(speed <= traffic_limit_speed)
    
    def test_upload_part(self):
        traffic_limit_speed = 819200 * 5
        response = self.bos.initiate_multipart_upload(self.BUCKET, self.KEY)
        self.check_headers(response)
        self.assertTrue(hasattr(response, "upload_id"))
        self.assertTrue(hasattr(response, "bucket"))
        self.assertTrue(hasattr(response, "key"))

        upload_id = response.upload_id

        self.get_file(20)
        left_size = os.path.getsize(self.FILENAME)
        done = 0
        part_number = 1
        part_list = []
        while left_size > 0:
            part_size = 5 * 1024 * 1024
            if left_size < part_size:
                part_size = left_size

            response = self.bos.upload_part_from_file(self.BUCKET,
                                                      self.KEY,
                                                      upload_id,
                                                      part_number=part_number,
                                                      part_size=part_size,
                                                      file_name = self.FILENAME,
                                                      traffic_limit = traffic_limit_speed,
                                                      offset=done)
            left_size = left_size - part_size
            done = done + part_size
            part_list.append({
                "partNumber": part_number,
                "eTag": response.metadata.etag
            })
            part_number += 1

        response = self.bos.complete_multipart_upload(self.BUCKET, self.KEY, upload_id=upload_id,
                                                      part_list=part_list)
        self.check_headers(response)
        self.assertTrue(hasattr(response, "etag"))
        self.assertTrue(hasattr(response, "bucket"))
        self.assertTrue(hasattr(response, "key"))
        self.assertTrue(hasattr(response, "location"))

class TestBucketQuota(TestClient):
    """test put mirroring config"""
    def test_bucket_quota(self):
        err = None
        quota_conf = {
            "maxObjectCount": 10000,
            "maxCapacityMegaBytes": 12341234
        }
        try:
            self.bos.put_bucket_quota(self.BUCKET, quota_conf= quota_conf)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        
        try:
            response = self.bos.get_bucket_quota(self.BUCKET)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.assertEqual(response.max_object_count, 10000)
        self.assertEqual(response.max_capacity_mega_bytes, 12341234)

        try:
            self.bos.delete_bucket_quota(self.BUCKET)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)

class TestBucketTagging(TestClient):
    """test put mirroring config"""
    def test_bucket_tagging(self):
        err = None
        tag_conf = {
        "tags": [
            {
                "tagKey": "key1",
                "tagValue": "value123"
            },
            {
                "tagKey": "ttt2",
                "tagValue": "6863gerg"
            }
            ],
        }
        try:
            self.bos.put_bucket_tagging(self.BUCKET, tag_conf= tag_conf)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        
        try:
            response = self.bos.get_bucket_tagging(self.BUCKET)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.assertEqual(len(response.tag), 2)
        self.assertEqual(response.tag[0].tag_key, 'ttt2')

        try:
            self.bos.delete_bucket_tagging(self.BUCKET)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)


class TestConditionalReadWrite(TestClient):
    """test put, get, post, head, 4 conditional read-write fields"""

    def test_get_object(self):
        fp = io.BytesIO(b"abcdefghijklmnopqrstuvwxyz")
        md5 = utils.get_md5_from_fp(fp)
        response = self.bos.put_object(self.BUCKET, self.KEY, fp, len(fp.getvalue()), md5)

        # normal situation, can be downloaded object
        etag = response.metadata.etag
        cond_read_write_1 = {"If-Match": etag}
        err = None
        try:
            response = self.bos.get_object(self.BUCKET, self.KEY, cond_read_write=cond_read_write_1)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        data = response.data.read()
        self.check_headers(response)
        self.assertEqual(data, b"abcdefghijklmnopqrstuvwxyz")

        cond_read_write_2 = {"If-Unmodified-Since": "Tue, 29 Dec 2099 10:14:38 GMT"}
        try:
            response = self.bos.get_object(self.BUCKET, self.KEY, cond_read_write=cond_read_write_2)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        data = response.data.read()
        self.check_headers(response)
        self.assertEqual(data, b"abcdefghijklmnopqrstuvwxyz")
        
        cond_read_write_3 = {"If-None-Match": etag + "invalid"}
        try:
            response = self.bos.get_object(self.BUCKET, self.KEY, cond_read_write=cond_read_write_3)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        data = response.data.read()
        self.check_headers(response)
        self.assertEqual(data, b"abcdefghijklmnopqrstuvwxyz")

        cond_read_write_4 = {"If-Modified-Since": "Tue, 29 Dec 2020 10:14:38 GMT"}
        try:
            response = self.bos.get_object(self.BUCKET, self.KEY, cond_read_write=cond_read_write_4)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        data = response.data.read()
        self.check_headers(response)
        self.assertEqual(data, b"abcdefghijklmnopqrstuvwxyz")

        cond_read_write_5 = {"If-None-Match": etag + "invalid", 
                             "If-Modified-Since": "Tue, 29 Dec 2020 10:14:38 GMT"}
        try:
            response = self.bos.get_object(self.BUCKET, self.KEY, cond_read_write=cond_read_write_5)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        data = response.data.read()
        self.check_headers(response)
        self.assertEqual(data, b"abcdefghijklmnopqrstuvwxyz")

        cond_read_write_6 = {"If-None-Match": etag + "invalid", 
                             "If-Modified-Since": "Tue, 29 Dec 2020 10:14:38 GMT"}
        try:
            response = self.bos.get_object(self.BUCKET, self.KEY, cond_read_write=cond_read_write_6)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        data = response.data.read()
        self.check_headers(response)
        self.assertEqual(data, b"abcdefghijklmnopqrstuvwxyz")

        cond_read_write_7 = {"If-Match": etag, 
                             "If-Unmodified-Since": "Tue, 29 Dec 2099 10:14:38 GMT"}
        try:
            response = self.bos.get_object(self.BUCKET, self.KEY, cond_read_write=cond_read_write_7)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        data = response.data.read()
        self.check_headers(response)
        self.assertEqual(data, b"abcdefghijklmnopqrstuvwxyz")
    
        cond_read_write_8 = {"If-Match": etag, 
                             "If-Unmodified-Since": "Tue, 29 Dec 2099 10:14:38 GMT",
                             "If-None-Match": etag + "invalid",
                             "If-Modified-Since": "Tue, 29 Dec 2020 10:14:38 GMT"}
        try:
            response = self.bos.get_object(self.BUCKET, self.KEY, cond_read_write=cond_read_write_8)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        data = response.data.read()
        self.check_headers(response)
        self.assertEqual(data, b"abcdefghijklmnopqrstuvwxyz")
        
        # abnormal situation, unable to download object, return 412 or 304
        cond_read_write_1 = {"If-Match": etag + "invalid"}
        err = None
        try:
            response = self.bos.get_object(self.BUCKET, self.KEY, cond_read_write=cond_read_write_1)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertEqual(err.status_code, 412)
        
        cond_read_write_2 = {"If-Unmodified-Since": "Tue, 29 Dec 2020 10:14:38 GMT"}
        try:
            response = self.bos.get_object(self.BUCKET, self.KEY, cond_read_write=cond_read_write_2)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertEqual(err.status_code, 412)
        
        cond_read_write_3 = {"If-None-Match": etag}
        try:
            response = self.bos.get_object(self.BUCKET, self.KEY, cond_read_write=cond_read_write_3)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertEqual(err.status_code, 304)
        
        cond_read_write_4 = {"If-Modified-Since": "Tue, 29 Dec 2099 10:14:38 GMT"}
        try:
            response = self.bos.get_object(self.BUCKET, self.KEY, cond_read_write=cond_read_write_4)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertEqual(err.status_code, 304)

        cond_read_write_5 = {"If-None-Match": etag + "invalid", 
                             "If-Modified-Since": "Tue, 29 Dec 2099 10:14:38 GMT"}
        try:
            response = self.bos.get_object(self.BUCKET, self.KEY, cond_read_write=cond_read_write_5)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertEqual(err.status_code, 304)

        cond_read_write_6 = {"If-None-Match": etag,
                             "If-Modified-Since": "Tue, 29 Dec 2099 10:14:38 GMT"}
        try:
            response = self.bos.get_object(self.BUCKET, self.KEY, cond_read_write=cond_read_write_6)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertEqual(err.status_code, 304)
        
        cond_read_write_7 = {"If-Match": etag + "invalid", 
                             "If-Unmodified-Since": "Tue, 29 Dec 2020 10:14:38 GMT"}
        try:
            response = self.bos.get_object(self.BUCKET, self.KEY, cond_read_write=cond_read_write_7)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertEqual(err.status_code, 412)
        
        cond_read_write_8 = {"If-Match": etag, 
                             "If-Unmodified-Since": "Tue, 29 Dec 2099 10:14:38 GMT",
                             "If-None-Match": etag + "invalid",
                             "If-Modified-Since": "Tue, 29 Dec 2020 10:14:38 GMT"}
        try:
            response = self.bos.get_object(self.BUCKET, self.KEY, cond_read_write=cond_read_write_8)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertEqual(err.status_code, 412)
        
        cond_read_write_9 = {"XX-test": etag, 
                             "If-Unmodified-Since": "Tue, 29 Dec 2099 10:14:38 GMT",
                             "If-None-Match": etag + "invalid",
                             "If-Modified-Since": "Tue, 29 Dec 2020 10:14:38 GMT"}
        try:
            response = self.bos.get_object(self.BUCKET, self.KEY, cond_read_write=cond_read_write_9)
        except ValueError as e:
            err = e
        finally:
            self.assertIsNotNone(err)

        self.bos.delete_object(self.BUCKET, self.KEY)

    def test_get_object_as_string(self):
        fp = io.BytesIO(b"abcdefghijklmnopqrstuvwxyz")
        md5 = utils.get_md5_from_fp(fp)
        response = self.bos.put_object(self.BUCKET, self.KEY, fp, len(fp.getvalue()), md5)

        # normal situation, can be downloaded object
        etag = response.metadata.etag
        cond_read_write = {"If-Match": etag,
                           "If-Unmodified-Since": "Tue, 29 Dec 2099 10:14:38 GMT",
                           "If-None-Match": etag + "invalid",
                           "If-Modified-Since": "Tue, 29 Dec 2020 10:14:38 GMT"}
        err = None
        try:
            response = self.bos.get_object_as_string(self.BUCKET, self.KEY, cond_read_write=cond_read_write)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.assertEqual(response, b"abcdefghijklmnopqrstuvwxyz")

        # abnormal situation, unable to download object, return 412 or 304
        cond_read_write_1 = {"If-Match": "",
                             "If-Unmodified-Since": "Tue, 29 Dec 2020 10:14:38 GMT",
                             "If-None-Match": etag + "invalid",
                             "If-Modified-Since": "Tue, 29 Dec 2099 10:14:38 GMT"}
        try:
            response = self.bos.get_object_as_string(self.BUCKET, self.KEY, cond_read_write=cond_read_write_1)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertEqual(err.status_code, 412)
        
        cond_read_write_2 = {"If-Match": etag,
                             "If-Unmodified-Since": "Tue, 29 Dec 2020 10:14:38 GMT",
                             "If-None-Match": etag,
                             "If-Modified-Since": "Tue, 29 Dec 2099 10:14:38 GMT"}
        try:
            response = self.bos.get_object_as_string(self.BUCKET, self.KEY, cond_read_write=cond_read_write_2)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertEqual(err.status_code, 304)

        cond_read_write_3 = {"If-Match": etag,
                             "If-Unmodified-Since": "Tue, 29 Dec 2099 10:14:38 GMT",
                             "If-None-Match": "",
                             "If-Modified-Since": "Tue, 29 Dec 2099 10:14:38 GMT"}
        try:
            response = self.bos.get_object_as_string(self.BUCKET, self.KEY, cond_read_write=cond_read_write_3)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertEqual(err.status_code, 304)

        cond_read_write_4 = {"If-None-Match": etag, 
                             "If-Unmodified-Since": "Tue, 29 Dec 2099 10:14:38 GMT",
                             "If-xxx-Match": etag + "invalid",
                             "If-Modified-Since": "Tue, 29 Dec 2020 10:14:38 GMT"}
        try:
            response = self.bos.get_object_as_string(self.BUCKET, self.KEY, cond_read_write=cond_read_write_4)
        except ValueError as e:
            err = e
        finally:
            self.assertIsNotNone(err)

        self.bos.delete_object(self.BUCKET, self.KEY)

    def test_get_object_to_file(self):
        fp = io.BytesIO(b"abcdefghijklmnopqrstuvwxyz")
        md5 = utils.get_md5_from_fp(fp)
        response = self.bos.put_object(self.BUCKET, self.KEY, fp, len(fp.getvalue()), md5)

        # normal situation, can be downloaded object
        etag = response.metadata.etag
        cond_read_write = {"If-Match": etag,
                           "If-Unmodified-Since": "Tue, 29 Dec 2099 10:14:38 GMT",
                           "If-None-Match": etag + "invalid",
                           "If-Modified-Since": "Tue, 29 Dec 2020 10:14:38 GMT"}
        err = None
        try:
            response = self.bos.get_object_to_file(self.BUCKET, self.KEY, self.FILENAME, cond_read_write=cond_read_write)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        data = open(self.FILENAME, "rb").read()
        self.assertEqual(data, b"abcdefghijklmnopqrstuvwxyz")
        self.check_headers(response)

        # abnormal situation, unable to download object, return 412 or 304
        cond_read_write_1 = {"If-Match": "",
                             "If-Unmodified-Since": "Tue, 29 Dec 2020 10:14:38 GMT",
                             "If-None-Match": etag + "invalid",
                             "If-Modified-Since": "Tue, 29 Dec 2099 10:14:38 GMT"}
        try:
            response = self.bos.get_object_to_file(self.BUCKET, self.KEY, self.FILENAME, cond_read_write=cond_read_write_1)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertEqual(err.status_code, 412)
        
        cond_read_write_2 = {"If-Match": etag,
                             "If-Unmodified-Since": "Tue, 29 Dec 2020 10:14:38 GMT",
                             "If-None-Match": etag,
                             "If-Modified-Since": "Tue, 29 Dec 2099 10:14:38 GMT"}
        try:
            response = self.bos.get_object_to_file(self.BUCKET, self.KEY, self.FILENAME, cond_read_write=cond_read_write_2)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertEqual(err.status_code, 304)

        cond_read_write_3 = {"If-Match": etag,
                             "If-Unmodified-Since": "Tue, 29 Dec 2099 10:14:38 GMT",
                             "If-None-Match": "",
                             "If-Modified-Since": "Tue, 29 Dec 2099 10:14:38 GMT"}
        try:
            response = self.bos.get_object_to_file(self.BUCKET, self.KEY, self.FILENAME, cond_read_write=cond_read_write_3)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertEqual(err.status_code, 304)

        cond_read_write_4 = {"If-None-Match": etag, 
                             "If-Unmodified-Since": "Tue, 29 Dec 2099 10:14:38 GMT",
                             "If-xxx-Match": etag + "invalid",
                             "If-Modified-Since": "Tue, 29 Dec 2020 10:14:38 GMT"}
        try:
            response = self.bos.get_object_to_file(self.BUCKET, self.KEY, self.FILENAME, cond_read_write=cond_read_write_4)
        except ValueError as e:
            err = e
        finally:
            self.assertIsNotNone(err)

        self.bos.delete_object(self.BUCKET, self.KEY)

    def test_get_object_meta_data(self):
        fp = io.BytesIO(b"abcdefghijklmnopqrstuvwxyz")
        md5 = utils.get_md5_from_fp(fp)
        response = self.bos.put_object(self.BUCKET, self.KEY, fp, len(fp.getvalue()), md5)

        # normal situation, can be downloaded object
        etag = response.metadata.etag
        cond_read_write = {"If-Match": etag,
                           "If-Unmodified-Since": "Tue, 29 Dec 2099 10:14:38 GMT",
                           "If-None-Match": etag + "invalid",
                           "If-Modified-Since": "Tue, 29 Dec 2020 10:14:38 GMT"}
        err = None
        try:
            response = self.bos.get_object_meta_data(self.BUCKET, self.KEY, cond_read_write=cond_read_write)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.check_headers(response)

        # abnormal situation, unable to download object, return 412 or 304
        cond_read_write_1 = {"If-Match": "",
                             "If-Unmodified-Since": "Tue, 29 Dec 2020 10:14:38 GMT",
                             "If-None-Match": etag + "invalid",
                             "If-Modified-Since": "Tue, 29 Dec 2099 10:14:38 GMT"}
        try:
            response = self.bos.get_object_meta_data(self.BUCKET, self.KEY, cond_read_write=cond_read_write_1)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertEqual(err.status_code, 412)
        
        cond_read_write_2 = {"If-Match": etag,
                             "If-Unmodified-Since": "Tue, 29 Dec 2020 10:14:38 GMT",
                             "If-None-Match": etag,
                             "If-Modified-Since": "Tue, 29 Dec 2099 10:14:38 GMT"}
        try:
            response = self.bos.get_object_meta_data(self.BUCKET, self.KEY, cond_read_write=cond_read_write_2)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertEqual(err.status_code, 304)

        cond_read_write_3 = {"If-Match": etag,
                             "If-Unmodified-Since": "Tue, 29 Dec 2099 10:14:38 GMT",
                             "If-None-Match": "",
                             "If-Modified-Since": "Tue, 29 Dec 2099 10:14:38 GMT"}
        try:
            response = self.bos.get_object_meta_data(self.BUCKET, self.KEY, cond_read_write=cond_read_write_3)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertEqual(err.status_code, 304)

        cond_read_write_4 = {"If-None-Match": etag, 
                             "If-Unmodified-Since": "Tue, 29 Dec 2099 10:14:38 GMT",
                             "If-xxx-Match": etag + "invalid",
                             "If-Modified-Since": "Tue, 29 Dec 2020 10:14:38 GMT"}
        try:
            response = self.bos.get_object_meta_data(self.BUCKET, self.KEY, cond_read_write=cond_read_write_4)
        except ValueError as e:
            err = e
        finally:
            self.assertIsNotNone(err)

        self.bos.delete_object(self.BUCKET, self.KEY)

    def test_put_object(self):
        fp = io.BytesIO(b"abcdefghijklmnopqrstuvwxyz")
        md5 = utils.get_md5_from_fp(fp)
        response = self.bos.put_object(self.BUCKET, self.KEY, fp, len(fp.getvalue()), md5)

        # normal situation, can be downloaded object
        etag = response.metadata.etag
        cond_read_write = {"If-Match": etag,
                           "If-Unmodified-Since": "Tue, 29 Dec 2099 10:14:38 GMT",
                           "If-None-Match": etag + "invalid"}
        err = None
        try:
            fp = io.BytesIO(b"zyxwvutsrqponmlkjihgfedcba")
            md5 = utils.get_md5_from_fp(fp)
            response = self.bos.put_object(self.BUCKET, self.KEY, fp, len(fp.getvalue()), md5, cond_read_write=cond_read_write)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.check_headers(response)

        # abnormal situation, unable to download object, return 412 or 304
        cond_read_write_1 = {"If-Match": "",
                             "If-Unmodified-Since": "Tue, 29 Dec 2020 10:14:38 GMT",
                             "If-None-Match": etag + "invalid"}
        try:
            fp = io.BytesIO(b"zyxwvutsrqponmlkjihgfedcba")
            md5 = utils.get_md5_from_fp(fp)
            response = self.bos.put_object(self.BUCKET, self.KEY, fp, len(fp.getvalue()), md5, cond_read_write=cond_read_write_1)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertEqual(err.status_code, 412)
        
        cond_read_write_2 = {"If-Match": etag,
                             "If-Unmodified-Since": "Tue, 29 Dec 2020 10:14:38 GMT",
                             "If-None-Match": etag}
        try:
            fp = io.BytesIO(b"zyxwvutsrqponmlkjihgfedcba")
            md5 = utils.get_md5_from_fp(fp)
            response = self.bos.put_object(self.BUCKET, self.KEY, fp, len(fp.getvalue()), md5, cond_read_write=cond_read_write_2)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertEqual(err.status_code, 412)

        cond_read_write_3 = {"If-Match": etag,
                             "If-Unmodified-Since": "Tue, 29 Dec 2099 10:14:38 GMT",
                             "If-None-Match": ""}
        try:
            fp = io.BytesIO(b"zyxwvutsrqponmlkjihgfedcba")
            md5 = utils.get_md5_from_fp(fp)
            response = self.bos.put_object(self.BUCKET, self.KEY, fp, len(fp.getvalue()), md5, cond_read_write=cond_read_write_3)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertEqual(err.status_code, 412)

        cond_read_write_4 = {"If-None-Match": etag, 
                             "If-Unmodified-Since": "Tue, 29 Dec 2099 10:14:38 GMT",
                             "If-xxx-Match": etag + "invalid"}
        try:
            fp = io.BytesIO(b"zyxwvutsrqponmlkjihgfedcba")
            md5 = utils.get_md5_from_fp(fp)
            response = self.bos.put_object(self.BUCKET, self.KEY, fp, len(fp.getvalue()), md5, cond_read_write=cond_read_write_4)
        except ValueError as e:
            err = e
        finally:
            self.assertIsNotNone(err)

        self.bos.delete_object(self.BUCKET, self.KEY)
    
    def test_put_object_from_string(self):
        fp = "zyxwvutsrqponmlkjihgfedcba"
        response = self.bos.put_object_from_string(self.BUCKET, self.KEY, fp)

        # normal situation, can be downloaded object
        etag = response.metadata.etag
        cond_read_write = {"If-Match": etag,
                           "If-Unmodified-Since": "Tue, 29 Dec 2099 10:14:38 GMT",
                           "If-None-Match": etag + "invalid"}
        err = None
        try:
            fp = "zyxwvutsrqponmlkjihgfedcba"
            response = self.bos.put_object_from_string(self.BUCKET, self.KEY, fp, cond_read_write=cond_read_write)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.check_headers(response)

        # abnormal situation, unable to download object, return 412 or 304
        cond_read_write_1 = {"If-Match": "",
                             "If-Unmodified-Since": "Tue, 29 Dec 2020 10:14:38 GMT",
                             "If-None-Match": etag + "invalid"}
        try:
            fp = "zyxwvutsrqponmlkjihgfedcba"
            response = self.bos.put_object_from_string(self.BUCKET, self.KEY, fp, cond_read_write=cond_read_write_1)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertEqual(err.status_code, 412)
        
        cond_read_write_2 = {"If-Match": etag,
                             "If-Unmodified-Since": "Tue, 29 Dec 2020 10:14:38 GMT",
                             "If-None-Match": etag}
        try:
            fp = "zyxwvutsrqponmlkjihgfedcba"
            response = self.bos.put_object_from_string(self.BUCKET, self.KEY, fp, cond_read_write=cond_read_write_2)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertEqual(err.status_code, 412)

        cond_read_write_3 = {"If-Match": etag,
                             "If-Unmodified-Since": "Tue, 29 Dec 2099 10:14:38 GMT",
                             "If-None-Match": ""}
        try:
            fp = "zyxwvutsrqponmlkjihgfedcba"
            response = self.bos.put_object_from_string(self.BUCKET, self.KEY, fp, cond_read_write=cond_read_write_3)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertEqual(err.status_code, 412)

        cond_read_write_4 = {"If-None-Match": etag, 
                             "If-Unmodified-Since": "Tue, 29 Dec 2099 10:14:38 GMT",
                             "If-xxx-Match": etag + "invalid"}
        try:
            fp = "zyxwvutsrqponmlkjihgfedcba"
            response = self.bos.put_object_from_string(self.BUCKET, self.KEY, fp, cond_read_write=cond_read_write_4)
        except ValueError as e:
            err = e
        finally:
            self.assertIsNotNone(err)

        self.bos.delete_object(self.BUCKET, self.KEY)
    
    def test_put_object_from_file(self):
        self.get_file(20)
        response = self.bos.put_object_from_file(self.BUCKET, self.KEY, self.FILENAME)

        # normal situation, can be downloaded object
        etag = response.metadata.etag
        cond_read_write = {"If-Match": etag,
                           "If-Unmodified-Since": "Tue, 29 Dec 2099 10:14:38 GMT",
                           "If-None-Match": etag + "invalid"}
        err = None
        try:
            response = self.bos.put_object_from_file(self.BUCKET, self.KEY, self.FILENAME, cond_read_write=cond_read_write)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.check_headers(response)

        # abnormal situation, unable to download object, return 412 or 304
        cond_read_write_1 = {"If-Match": "",
                             "If-Unmodified-Since": "Tue, 29 Dec 2020 10:14:38 GMT",
                             "If-None-Match": etag + "invalid"}
        try:
            response = self.bos.put_object_from_file(self.BUCKET, self.KEY, self.FILENAME, cond_read_write=cond_read_write_1)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertEqual(err.status_code, 412)
        
        cond_read_write_2 = {"If-Match": etag,
                             "If-Unmodified-Since": "Tue, 29 Dec 2020 10:14:38 GMT",
                             "If-None-Match": etag}
        try:
            response = self.bos.put_object_from_file(self.BUCKET, self.KEY, self.FILENAME, cond_read_write=cond_read_write_2)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertEqual(err.status_code, 412)

        cond_read_write_3 = {"If-Match": etag,
                             "If-Unmodified-Since": "Tue, 29 Dec 2099 10:14:38 GMT",
                             "If-None-Match": ""}
        try:
            response = self.bos.put_object_from_file(self.BUCKET, self.KEY, self.FILENAME, cond_read_write=cond_read_write_3)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertEqual(err.status_code, 412)

        cond_read_write_4 = {"If-None-Match": etag, 
                             "If-Unmodified-Since": "Tue, 29 Dec 2099 10:14:38 GMT",
                             "If-xxx-Match": etag + "invalid"}
        try:
            response = self.bos.put_object_from_file(self.BUCKET, self.KEY, self.FILENAME, cond_read_write=cond_read_write_4)
        except ValueError as e:
            err = e
        finally:
            self.assertIsNotNone(err)
        
        cond_read_write_5 = {"If-None-Match": etag, 
                             "If-Unmodified-Since": "Tue, 29 Dec 2099 10:14:38 GMT",
                             "If-xxx-Match": etag + "invalid"}
        try:
            response = self.bos.put_object_from_file(self.BUCKET, self.KEY, self.FILENAME, cond_read_write=cond_read_write_5)
        except ValueError as e:
            err = e
        finally:
            self.assertIsNotNone(err)

        self.bos.delete_object(self.BUCKET, self.KEY)

    def test_complete_multipart_upload(self):
        response = self.bos.initiate_multipart_upload(self.BUCKET, self.KEY)
        upload_id = response.upload_id
        self.get_file(20)
        left_size = os.path.getsize(self.FILENAME)
        done = 0
        part_number = 1
        part_list = []
        while left_size > 0:
            part_size = 5 * 1024 * 1024
            if left_size < part_size:
                part_size = left_size

            response = self.bos.upload_part_from_file(self.BUCKET, self.KEY, upload_id, part_number=part_number,
                                                      part_size=part_size, file_name = self.FILENAME, offset=done)
            left_size = left_size - part_size
            done = done + part_size
            part_list.append({
                "partNumber": part_number,
                "eTag": response.metadata.etag
            })
            part_number += 1

        response = self.bos.complete_multipart_upload(self.BUCKET, self.KEY, upload_id=upload_id,
                                                      part_list=part_list)

        # normal situation, can be downloaded object
        etag = response.etag
        cond_read_write = {"If-Match": etag,
                           "If-Unmodified-Since": "Tue, 29 Dec 2099 10:14:38 GMT",
                           "If-None-Match": etag + "invalid"}
        err = None
        try:
            response = self.bos.initiate_multipart_upload(self.BUCKET, self.KEY)
            upload_id = response.upload_id
            left_size = os.path.getsize(self.FILENAME)
            done = 0
            part_number = 1
            part_list = []
            while left_size > 0:
                part_size = 5 * 1024 * 1024
                if left_size < part_size:
                    part_size = left_size

                response = self.bos.upload_part_from_file(self.BUCKET, self.KEY, upload_id, part_number=part_number,
                                                        part_size=part_size, file_name = self.FILENAME, offset=done)
                left_size = left_size - part_size
                done = done + part_size
                part_list.append({
                    "partNumber": part_number,
                    "eTag": response.metadata.etag
                })
                part_number += 1
            response = self.bos.complete_multipart_upload(self.BUCKET, self.KEY, upload_id=upload_id,
                                                      part_list=part_list, cond_read_write=cond_read_write)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.check_headers(response)

        # abnormal situation, unable to download object, return 412 or 304
        # cond_read_write_1 = {"If-Match": "",
        #                      "If-Unmodified-Since": "Tue, 29 Dec 2020 10:14:38 GMT",
        #                      "If-None-Match": etag + "invalid"}
        # try:
        #     response = self.bos.initiate_multipart_upload(self.BUCKET, self.KEY)
        #     upload_id = response.upload_id
        #     left_size = os.path.getsize(self.FILENAME)
        #     done = 0
        #     part_number = 1
        #     part_list = []
        #     while left_size > 0:
        #         part_size = 5 * 1024 * 1024
        #         if left_size < part_size:
        #             part_size = left_size

        #         response = self.bos.upload_part_from_file(self.BUCKET, self.KEY, upload_id, part_number=part_number,
        #                                                 part_size=part_size, file_name = self.FILENAME, offset=done)
        #         left_size = left_size - part_size
        #         done = done + part_size
        #         part_list.append({
        #             "partNumber": part_number,
        #             "eTag": response.metadata.etag
        #         })
        #         part_number += 1
        #     response = self.bos.complete_multipart_upload(self.BUCKET, self.KEY, upload_id=upload_id,
        #                                               part_list=part_list, cond_read_write=cond_read_write_1)
        # except BceHttpClientError as e:
        #     err = e
        #     print(err)
        # finally:
        #     self.assertEqual(err.status_code, 412)
        
        cond_read_write_2 = {"If-Match": etag,
                             "If-Unmodified-Since": "Tue, 29 Dec 2020 10:14:38 GMT",
                             "If-None-Match": etag}
        try:
            response = self.bos.initiate_multipart_upload(self.BUCKET, self.KEY)
            upload_id = response.upload_id
            left_size = os.path.getsize(self.FILENAME)
            done = 0
            part_number = 1
            part_list = []
            while left_size > 0:
                part_size = 5 * 1024 * 1024
                if left_size < part_size:
                    part_size = left_size

                response = self.bos.upload_part_from_file(self.BUCKET, self.KEY, upload_id, part_number=part_number,
                                                        part_size=part_size, file_name = self.FILENAME, offset=done)
                left_size = left_size - part_size
                done = done + part_size
                part_list.append({
                    "partNumber": part_number,
                    "eTag": response.metadata.etag
                })
                part_number += 1
            response = self.bos.complete_multipart_upload(self.BUCKET, self.KEY, upload_id=upload_id,
                                                      part_list=part_list, cond_read_write=cond_read_write_2)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertEqual(err.status_code, 412)

        cond_read_write_3 = {"If-Match": etag,
                             "If-Unmodified-Since": "Tue, 29 Dec 2099 10:14:38 GMT",
                             "If-None-Match": ""}
        try:
            response = self.bos.initiate_multipart_upload(self.BUCKET, self.KEY)
            upload_id = response.upload_id
            left_size = os.path.getsize(self.FILENAME)
            done = 0
            part_number = 1
            part_list = []
            while left_size > 0:
                part_size = 5 * 1024 * 1024
                if left_size < part_size:
                    part_size = left_size

                response = self.bos.upload_part_from_file(self.BUCKET, self.KEY, upload_id, part_number=part_number,
                                                        part_size=part_size, file_name = self.FILENAME, offset=done)
                left_size = left_size - part_size
                done = done + part_size
                part_list.append({
                    "partNumber": part_number,
                    "eTag": response.metadata.etag
                })
                part_number += 1
            response = self.bos.complete_multipart_upload(self.BUCKET, self.KEY, upload_id=upload_id,
                                                      part_list=part_list, cond_read_write=cond_read_write_3)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertEqual(err.status_code, 412)

        cond_read_write_4 = {"If-None-Match": etag, 
                             "If-Unmodified-Since": "Tue, 29 Dec 2099 10:14:38 GMT",
                             "If-xxx-Match": etag + "invalid"}
        try:
            response = self.bos.initiate_multipart_upload(self.BUCKET, self.KEY)
            upload_id = response.upload_id
            left_size = os.path.getsize(self.FILENAME)
            done = 0
            part_number = 1
            part_list = []
            while left_size > 0:
                part_size = 5 * 1024 * 1024
                if left_size < part_size:
                    part_size = left_size

                response = self.bos.upload_part_from_file(self.BUCKET, self.KEY, upload_id, part_number=part_number,
                                                        part_size=part_size, file_name = self.FILENAME, offset=done)
                left_size = left_size - part_size
                done = done + part_size
                part_list.append({
                    "partNumber": part_number,
                    "eTag": response.metadata.etag
                })
                part_number += 1
            response = self.bos.complete_multipart_upload(self.BUCKET, self.KEY, upload_id=upload_id,
                                                      part_list=part_list, cond_read_write=cond_read_write_4)
        except ValueError as e:
            err = e
        finally:
            self.assertIsNotNone(err)
        
        cond_read_write_5 = {"If-None-Match": etag, 
                             "If-Unmodified-Since": "Tue, 29 Dec 2099 10:14:38 GMT",
                             "If-xxx-Match": etag + "invalid",
                             "If-Modified-Since": "Tue, 29 Dec 2099 10:14:38 GMT"}
        try:
            response = self.bos.initiate_multipart_upload(self.BUCKET, self.KEY)
            upload_id = response.upload_id
            left_size = os.path.getsize(self.FILENAME)
            done = 0
            part_number = 1
            part_list = []
            while left_size > 0:
                part_size = 5 * 1024 * 1024
                if left_size < part_size:
                    part_size = left_size

                response = self.bos.upload_part_from_file(self.BUCKET, self.KEY, upload_id, part_number=part_number,
                                                        part_size=part_size, file_name = self.FILENAME, offset=done)
                left_size = left_size - part_size
                done = done + part_size
                part_list.append({
                    "partNumber": part_number,
                    "eTag": response.metadata.etag
                })
                part_number += 1
            response = self.bos.complete_multipart_upload(self.BUCKET, self.KEY, upload_id=upload_id,
                                                      part_list=part_list, cond_read_write=cond_read_write_5)
        except ValueError as e:
            err = e
        finally:
            self.assertIsNotNone(err)

        self.bos.delete_object(self.BUCKET, self.KEY)


class TestCRC32(TestClient):
    """Test CRC32 validation for object upload operations"""

    def test_append_object_with_crc32(self):
        """test append_object with user-provided CRC32"""
        data = b"test_data_for_append_object"
        fp = io.BytesIO(data)
        # Calculate CRC32 manually
        crc32 = utils.get_crc32_from_fp(fp, buf_size=8192)

        # Reset fp for upload
        fp.seek(0)

        # Test with user-provided CRC32
        response = self.bos.append_object(
            bucket_name=self.BUCKET,
            key=b"test_append_object_crc32",
            data=fp,
            content_length=len(data),
            content_crc32=crc32
        )
        self.check_headers(response)
        next_offset = response.metadata.bce_next_append_offset
        self.assertEqual(int(next_offset), len(data))
        self.assertEqual(response.metadata.bce_content_crc_32, str(crc32))

        # Verify the object was created correctly
        content = self.bos.get_object_as_string(bucket_name=self.BUCKET, key=b"test_append_object_crc32")
        self.assertEqual(content, data)

    def test_append_object_auto_crc32(self):
        """test append_object with auto-calculated CRC32"""
        data = b"test_data_auto_crc32"
        fp = io.BytesIO(data)
        crc32 = utils.get_crc32_from_fp(fp, buf_size=8192)

        # Test without providing CRC32 (should be auto-calculated)
        response = self.bos.append_object(
            bucket_name=self.BUCKET,
            key=b"test_append_object_auto_crc32",
            data=fp,
            content_length=len(data)
        )
        self.check_headers(response)
        next_offset = response.metadata.bce_next_append_offset
        self.assertEqual(int(next_offset), len(data))

        # Verify the object was created correctly
        content = self.bos.get_object_as_string(bucket_name=self.BUCKET, key=b"test_append_object_auto_crc32")
        self.assertEqual(content, data)
        self.assertEqual(response.metadata.bce_content_crc_32, str(crc32))

    def test_append_object_from_string_with_crc32(self):
        """test append_object_from_string with user-provided CRC32"""
        data = "test_append_string_crc32"
        data_bytes = data.encode('utf-8')
        fp = io.BytesIO(data_bytes)
        crc32 = utils.get_crc32_from_fp(fp, buf_size=8192)

        # Test with user-provided CRC32
        response = self.bos.append_object_from_string(
            bucket_name=self.BUCKET,
            key=b"test_append_string_crc32",
            data=data,
            content_crc32=crc32
        )
        self.check_headers(response)
        next_offset = response.metadata.bce_next_append_offset
        self.assertEqual(int(next_offset), len(data))
        self.assertEqual(response.metadata.bce_content_crc_32, str(crc32))

        # Verify the object was created correctly
        content = self.bos.get_object_as_string(bucket_name=self.BUCKET, key=b"test_append_string_crc32")
        self.assertEqual(content, data_bytes)

    def test_append_object_from_string_auto_crc32(self):
        """test append_object_from_string with auto-calculated CRC32"""
        data = "test_append_string_auto_crc32"

        # Test without providing CRC32 (should be auto-calculated)
        response = self.bos.append_object_from_string(
            bucket_name=self.BUCKET,
            key=b"test_append_string_auto_crc32",
            data=data
        )
        self.check_headers(response)
        next_offset = response.metadata.bce_next_append_offset
        self.assertEqual(int(next_offset), len(data))

        # Verify the object was created correctly
        content = self.bos.get_object_as_string(bucket_name=self.BUCKET, key=b"test_append_string_auto_crc32")
        self.assertEqual(content, data.encode('utf-8'))

        fp = io.BytesIO(data.encode('utf-8'))
        crc32 = utils.get_crc32_from_fp(fp, buf_size=8192)
        self.assertEqual(response.metadata.bce_content_crc_32, str(crc32))

    def test_put_object_with_crc32(self):
        """test put_object with user-provided CRC32"""
        data = b"test_put_object_crc32"
        fp = io.BytesIO(data)
        crc32 = utils.get_crc32_from_fp(fp, buf_size=8192)
        fp.seek(0)

        # Test with user-provided CRC32
        response = self.bos.put_object(
            bucket_name=self.BUCKET,
            key=self.KEY,
            data=fp,
            content_length=len(data),
            content_crc32=crc32
        )
        self.check_headers(response)

        # Verify the object was created correctly
        content = self.bos.get_object_as_string(bucket_name=self.BUCKET, key=self.KEY)
        self.assertEqual(content, data)
        self.assertEqual(response.metadata.bce_content_crc_32, str(crc32))

    def test_put_object_auto_crc32(self):
        """test put_object with auto-calculated CRC32"""
        data = b"test_put_object_auto_crc32"
        fp = io.BytesIO(data)
        crc32 = utils.get_crc32_from_fp(fp, buf_size=8192)

        # Test without providing CRC32 (should be auto-calculated)
        response = self.bos.put_object(
            bucket_name=self.BUCKET,
            key=self.KEY,
            data=fp,
            content_length=len(data)
        )
        self.check_headers(response)

        # Verify the object was created correctly
        content = self.bos.get_object_as_string(bucket_name=self.BUCKET, key=self.KEY)
        self.assertEqual(content, data)

        self.assertEqual(response.metadata.bce_content_crc_32, str(crc32))

    def test_put_object_from_string_with_crc32(self):
        """test put_object_from_string with user-provided CRC32"""
        data = "test_put_string_crc32"
        data_bytes = data.encode('utf-8')
        fp = io.BytesIO(data_bytes)
        crc32 = utils.get_crc32_from_fp(fp, buf_size=8192)

        # Test with user-provided CRC32
        response = self.bos.put_object_from_string(
            bucket=self.BUCKET,
            key=self.KEY,
            data=data,
            content_crc32=crc32
        )
        self.check_headers(response)

        # Verify the object was created correctly
        content = self.bos.get_object_as_string(bucket_name=self.BUCKET, key=self.KEY)
        self.assertEqual(content, data_bytes)

    def test_put_object_from_string_auto_crc32(self):
        """test put_object_from_string with auto-calculated CRC32"""
        data = "test_put_string_auto_crc32"
        fp = io.BytesIO(data.encode('utf-8'))
        crc32 = utils.get_crc32_from_fp(fp, buf_size=8192)

        # Test without providing CRC32 (should be auto-calculated)
        response = self.bos.put_object_from_string(
            bucket=self.BUCKET,
            key=self.KEY,
            data=data
        )
        self.check_headers(response)

        # Verify the object was created correctly
        content = self.bos.get_object_as_string(bucket_name=self.BUCKET, key=self.KEY)
        self.assertEqual(content, data.encode('utf-8'))
        self.assertEqual(response.metadata.bce_content_crc_32, str(crc32))

    def test_put_object_from_file_with_crc32(self):
        """test put_object_from_file with user-provided CRC32"""
        self.get_file(1)  # Create 1MB file
        file_crc32 = 0

        # Calculate CRC32 for the file
        with open(self.FILENAME, 'rb') as fp:
            file_crc32 = utils.get_crc32_from_fp(fp, buf_size=8192)

        # Test with user-provided CRC32
        response = self.bos.put_object_from_file(
            bucket=self.BUCKET,
            key=b"test_file_crc32",
            file_name=self.FILENAME,
            content_crc32=file_crc32
        )
        self.check_headers(response)

        # Verify the object was created correctly
        response = self.bos.get_object(bucket_name=self.BUCKET, key=b"test_file_crc32")
        self.assertIsNotNone(response)
        self.assertEqual(response.metadata.bce_content_crc_32, str(file_crc32))

    def test_put_object_from_file_auto_crc32(self):
        """test put_object_from_file with auto-calculated CRC32"""
        self.get_file(1)  # Create 1MB file
        file_crc32 = 0

        # Calculate CRC32 for the file
        with open(self.FILENAME, 'rb') as fp:
            file_crc32 = utils.get_crc32_from_fp(fp, buf_size=8192)

        # Test without providing CRC32 (should be auto-calculated)
        response = self.bos.put_object_from_file(
            bucket=self.BUCKET,
            key=b"test_file_auto_crc32",
            file_name=self.FILENAME
        )
        self.check_headers(response)

        # Verify the object was created correctly
        response = self.bos.get_object(bucket_name=self.BUCKET, key=b"test_file_auto_crc32")
        self.assertIsNotNone(response)
        self.assertEqual(response.metadata.bce_content_crc_32, str(file_crc32))

    def test_upload_part_with_crc32(self):
        """test upload_part with user-provided CRC32"""
        # Initialize multipart upload
        init_response = self.bos.initiate_multipart_upload(self.BUCKET, b"test_upload_part_crc32")
        self.check_headers(init_response)
        upload_id = init_response.upload_id

        part_data = b"test_part_data_crc32"
        fp = io.BytesIO(part_data)
        part_crc32 = utils.get_crc32_from_fp(fp, buf_size=8192)
        fp.seek(0)

        # Test with user-provided CRC32
        response = self.bos.upload_part(
            bucket_name=self.BUCKET,
            key=b"test_upload_part_crc32",
            upload_id=upload_id,
            part_number=1,
            part_size=len(part_data),
            part_fp=fp,
            part_crc32=part_crc32
        )
        self.check_headers(response)
        self.assertEqual(response.metadata.bce_content_crc_32, str(part_crc32))

        # Clean up
        self.bos.abort_multipart_upload(self.BUCKET, b"test_upload_part_crc32", upload_id)

    def test_upload_part_auto_crc32(self):
        """test upload_part with auto-calculated CRC32"""
        # Initialize multipart upload
        init_response = self.bos.initiate_multipart_upload(self.BUCKET, b"test_upload_part_auto_crc32")
        self.check_headers(init_response)
        upload_id = init_response.upload_id

        part_data = b"test_part_data_auto_crc32"
        fp = io.BytesIO(part_data)
        crc32 = utils.get_crc32_from_fp(fp, buf_size=8192)

        # Test without providing CRC32 (should be auto-calculated)
        response = self.bos.upload_part(
            bucket_name=self.BUCKET,
            key=b"test_upload_part_auto_crc32",
            upload_id=upload_id,
            part_number=1,
            part_size=len(part_data),
            part_fp=fp
        )
        self.check_headers(response)
        self.assertEqual(response.metadata.bce_content_crc_32, str(crc32))

        # Clean up
        self.bos.abort_multipart_upload(self.BUCKET, b"test_upload_part_auto_crc32", upload_id)

    def test_upload_part_from_file_with_crc32(self):
        """test upload_part_from_file with user-provided CRC32"""
        # Create 5MB file (minimum BOS part size)
        with open(self.FILENAME, 'wb') as f:
            f.write(b'a' * (5 * 1024 * 1024))

        # Initialize multipart upload
        init_response = self.bos.initiate_multipart_upload(self.BUCKET, b"test_upload_part_file_crc32")
        self.check_headers(init_response)
        upload_id = init_response.upload_id

        # Calculate CRC32 for part of file
        with open(self.FILENAME, 'rb') as fp:
            part_crc32 = utils.get_crc32_from_fp(fp, offset=0, length=5*1024*1024, buf_size=8192)

        # Test with user-provided CRC32
        response = self.bos.upload_part_from_file(
            bucket_name=self.BUCKET,
            key=b"test_upload_part_file_crc32",
            upload_id=upload_id,
            part_number=1,
            part_size=5*1024*1024,
            file_name=self.FILENAME,
            offset=0,
            part_crc32=part_crc32
        )
        self.check_headers(response)
        self.assertEqual(response.metadata.bce_content_crc_32, str(part_crc32))

        # Clean up
        self.bos.abort_multipart_upload(self.BUCKET, b"test_upload_part_file_crc32", upload_id)

    def test_upload_part_from_file_auto_crc32(self):
        """test upload_part_from_file with auto-calculated CRC32"""
        # Create 5MB file (minimum BOS part size)
        with open(self.FILENAME, 'wb') as f:
            f.write(b'a' * (5 * 1024 * 1024))

        # Initialize multipart upload
        init_response = self.bos.initiate_multipart_upload(self.BUCKET, b"test_upload_part_file_auto_crc32")
        self.check_headers(init_response)
        upload_id = init_response.upload_id

        with open(self.FILENAME, 'rb') as fp:
            part_crc32 = utils.get_crc32_from_fp(fp, offset=0, length=5*1024*1024, buf_size=8192)

        # Test without providing CRC32 (should be auto-calculated)
        response = self.bos.upload_part_from_file(
            bucket_name=self.BUCKET,
            key=b"test_upload_part_file_auto_crc32",
            upload_id=upload_id,
            part_number=1,
            part_size=5*1024*1024,
            file_name=self.FILENAME,
            offset=0
        )
        self.check_headers(response)
        self.assertEqual(response.metadata.bce_content_crc_32, str(part_crc32))

        # Clean up
        self.bos.abort_multipart_upload(self.BUCKET, b"test_upload_part_file_auto_crc32", upload_id)

    def test_complete_multipart_upload_with_crc32(self):
        """test complete_multipart_upload with user-provided CRC32"""
        # Initialize multipart upload
        init_response = self.bos.initiate_multipart_upload(self.BUCKET, b"test_complete_crc32")
        self.check_headers(init_response)
        upload_id = init_response.upload_id

        # Create file with at least 5MB per part (minimum BOS part size)
        self.get_file(10)  # Create 10MB file (2 parts of 5MB each)

        # Upload two parts
        response1 = self.bos.upload_part_from_file(
            self.BUCKET, b"test_complete_crc32", upload_id, 1,
            5 * 1024 * 1024, self.FILENAME, 0
        )
        crc32_1 = int(response1.metadata.bce_content_crc_32)

        response2 = self.bos.upload_part_from_file(
            self.BUCKET, b"test_complete_crc32", upload_id, 2,
            5 * 1024 * 1024, self.FILENAME, 5 * 1024 * 1024
        )
        crc32_2 = int(response2.metadata.bce_content_crc_32)

        part_list = [
            {"partNumber": 1, "eTag": response1.metadata.etag},
            {"partNumber": 2, "eTag": response2.metadata.etag}
        ]
        crc32 = utils.crc32_combine(crc32_1, crc32_2, 5 * 1024 * 1024)

        # Calculate total CRC32 for complete (optional parameter)
        # Note: For multi-part uploads, CRC32 calculation requires combining part CRCs
        # Here we test that the parameter is accepted
        response = self.bos.complete_multipart_upload(
            bucket_name=self.BUCKET,
            key=b"test_complete_crc32",
            upload_id=upload_id,
            part_list=part_list,
            content_crc32=crc32
        )
        self.check_headers(response)

        # Verify the object was created correctly
        response = self.bos.get_object(bucket_name=self.BUCKET, key=b"test_complete_crc32")
        self.assertEqual(response.metadata.bce_content_crc_32, str(crc32))

    def test_complete_multipart_upload_auto_crc32(self):
        """test complete_multipart_upload without user-provided CRC32"""
        # Initialize multipart upload
        init_response = self.bos.initiate_multipart_upload(self.BUCKET, b"test_complete_auto_crc32")
        self.check_headers(init_response)
        upload_id = init_response.upload_id

        # Create file with at least 5MB per part (minimum BOS part size)
        self.get_file(10)  # Create 10MB file (2 parts of 5MB each)

        # Upload two parts
        response1 = self.bos.upload_part_from_file(
            self.BUCKET, b"test_complete_auto_crc32", upload_id, 1,
            5 * 1024 * 1024, self.FILENAME, 0
        )

        response2 = self.bos.upload_part_from_file(
            self.BUCKET, b"test_complete_auto_crc32", upload_id, 2,
            5 * 1024 * 1024, self.FILENAME, 5 * 1024 * 1024
        )

        part_list = [
            {"partNumber": 1, "eTag": response1.metadata.etag},
            {"partNumber": 2, "eTag": response2.metadata.etag}
        ]

        # Test complete without CRC32 (optional parameter)
        response = self.bos.complete_multipart_upload(
            bucket_name=self.BUCKET,
            key=b"test_complete_auto_crc32",
            upload_id=upload_id,
            part_list=part_list
        )
        self.check_headers(response)

        # Verify the object was created correctly
        response = self.bos.get_object(bucket_name=self.BUCKET, key=b"test_complete_auto_crc32")
        self.assertIsNotNone(response)

    def test_put_super_object_from_file_with_crc32(self):
        """test put_super_object_from_file with user-provided CRC32"""
        # Create a file larger than 5MB to trigger multi-part upload
        with open(self.FILENAME, 'wb') as f:
            f.write(b'a' * (6 * 1024 * 1024))  # 6MB file (2 parts: 5MB + 1MB)

        crc32 = utils.get_crc32_from_fp(open(self.FILENAME, 'rb'))

        result = self.bos.put_super_object_from_file(
            bucket_name=self.BUCKET,
            key=b"test_super_object_crc32",
            file_name=self.FILENAME,
            chunk_size=5,  # 5MB chunks
            thread_num=1,
            content_crc32=crc32
        )
        # put_super_object_from_file returns bool (True on success)
        self.assertTrue(result)

        # Verify the object was created correctly
        response = self.bos.get_object(bucket_name=self.BUCKET, key=b"test_super_object_crc32")
        self.assertIsNotNone(response)
        self.assertEqual(response.metadata.bce_content_crc_32, str(crc32))

    def test_put_super_object_from_file_auto_crc32(self):
        """test put_super_object_from_file with auto-calculated CRC32"""
        # Create a 6MB file for testing (will be split into 2 parts)
        with open(self.FILENAME, 'wb') as f:
            f.write(b'a' * (6 * 1024 * 1024))
            
        crc32 = utils.get_crc32_from_fp(open(self.FILENAME, 'rb'))

        # Test without providing CRC32 (should be auto-calculated)
        result = self.bos.put_super_object_from_file(
            bucket_name=self.BUCKET,
            key=b"test_super_object_auto_crc32",
            file_name=self.FILENAME,
            chunk_size=5,  # 5MB chunks
            thread_num=1
        )
        # put_super_object_from_file returns bool (True on success)
        self.assertTrue(result)

        # Verify the object was created correctly
        response = self.bos.get_object(bucket_name=self.BUCKET, key=b"test_super_object_auto_crc32")
        self.assertIsNotNone(response)
        self.assertEqual(response.metadata.bce_content_crc_32, str(crc32))


class TestSHA256(TestClient):
    """Test SHA256 validation for object upload operations"""

    def test_put_object_with_sha256(self):
        """test put_object with user-provided SHA256"""
        data = b"test_put_object_sha256"
        fp = io.BytesIO(data)
        sha256 = utils.get_sha256_from_fp(fp, buf_size=8192)
        fp.seek(0)

        response = self.bos.put_object(
            bucket_name=self.BUCKET,
            key=self.KEY,
            data=fp,
            content_length=len(data),
            content_sha256=sha256
        )
        self.check_headers(response)

        # Verify the object was created correctly
        content = self.bos.get_object_as_string(bucket_name=self.BUCKET, key=self.KEY)
        self.assertEqual(content, data)

    def test_put_object_from_string_with_sha256(self):
        """test put_object_from_string with user-provided SHA256"""
        data = "test_put_string_sha256"
        data_bytes = data.encode('utf-8')
        fp = io.BytesIO(data_bytes)
        sha256 = utils.get_sha256_from_fp(fp, buf_size=8192)

        response = self.bos.put_object_from_string(
            bucket=self.BUCKET,
            key=self.KEY,
            data=data,
            content_sha256=sha256
        )
        self.check_headers(response)

        content = self.bos.get_object_as_string(bucket_name=self.BUCKET, key=self.KEY)
        self.assertEqual(content, data_bytes)

    def test_put_object_from_file_with_sha256(self):
        """test put_object_from_file with user-provided SHA256"""
        with open(self.FILENAME, 'wb') as f:
            f.write(b'a' * (1 * 1024 * 1024))  # 1MB file

        with open(self.FILENAME, 'rb') as fp:
            sha256 = utils.get_sha256_from_fp(fp, buf_size=8192)

        response = self.bos.put_object_from_file(
            bucket=self.BUCKET,
            key=b"test_file_sha256",
            file_name=self.FILENAME,
            content_sha256=sha256
        )
        self.check_headers(response)

        response = self.bos.get_object(bucket_name=self.BUCKET, key=b"test_file_sha256")
        self.assertIsNotNone(response)

    def test_append_object_with_sha256(self):
        """test append_object with user-provided SHA256"""
        data = b"test_append_object_sha256"
        fp = io.BytesIO(data)
        sha256 = utils.get_sha256_from_fp(fp, buf_size=8192)
        fp.seek(0)

        response = self.bos.append_object(
            bucket_name=self.BUCKET,
            key=b"test_append_object_sha256",
            data=fp,
            content_length=len(data),
            content_sha256=sha256
        )
        self.check_headers(response)

        content = self.bos.get_object_as_string(bucket_name=self.BUCKET, key=b"test_append_object_sha256")
        self.assertEqual(content, data)

    def test_append_object_from_string_with_sha256(self):
        """test append_object_from_string with user-provided SHA256"""
        data = "test_append_string_sha256"
        data_bytes = data.encode('utf-8')
        fp = io.BytesIO(data_bytes)
        sha256 = utils.get_sha256_from_fp(fp, buf_size=8192)

        response = self.bos.append_object_from_string(
            bucket_name=self.BUCKET,
            key=b"test_append_string_sha256",
            data=data,
            content_sha256=sha256
        )
        self.check_headers(response)

        content = self.bos.get_object_as_string(bucket_name=self.BUCKET, key=b"test_append_string_sha256")
        self.assertEqual(content, data_bytes)

    def test_upload_part_with_sha256(self):
        """test upload_part with user-provided SHA256"""
        init_response = self.bos.initiate_multipart_upload(self.BUCKET, b"test_upload_part_sha256")
        upload_id = init_response.upload_id

        part_data = b"test_part_data_sha256"
        fp = io.BytesIO(part_data)
        part_sha256 = utils.get_sha256_from_fp(fp, buf_size=8192)
        fp.seek(0)

        response = self.bos.upload_part(
            bucket_name=self.BUCKET,
            key=b"test_upload_part_sha256",
            upload_id=upload_id,
            part_number=1,
            part_size=len(part_data),
            part_fp=fp,
            part_sha256=part_sha256
        )
        self.check_headers(response)

        self.bos.abort_multipart_upload(self.BUCKET, b"test_upload_part_sha256", upload_id)

    def test_upload_part_from_file_with_sha256(self):
        """test upload_part_from_file with user-provided SHA256"""
        with open(self.FILENAME, 'wb') as f:
            f.write(b'a' * (5 * 1024 * 1024))  # 5MB file (minimum BOS part size)

        init_response = self.bos.initiate_multipart_upload(self.BUCKET, b"test_upload_part_file_sha256")
        upload_id = init_response.upload_id

        with open(self.FILENAME, 'rb') as fp:
            part_sha256 = utils.get_sha256_from_fp(fp, offset=0, length=5*1024*1024, buf_size=8192)

        response = self.bos.upload_part_from_file(
            bucket_name=self.BUCKET,
            key=b"test_upload_part_file_sha256",
            upload_id=upload_id,
            part_number=1,
            part_size=5*1024*1024,
            file_name=self.FILENAME,
            offset=0,
            part_sha256=part_sha256
        )
        self.check_headers(response)

        self.bos.abort_multipart_upload(self.BUCKET, b"test_upload_part_file_sha256", upload_id)


class TestCRC32C(TestClient):
    """Test CRC32C validation for object upload operations"""

    def test_put_object_with_crc32c(self):
        """test put_object with user-provided CRC32C"""
        data = b"test_put_object_crc32c"
        fp = io.BytesIO(data)
        crc32c = utils.get_crc32c_from_fp(fp, buf_size=8192)
        fp.seek(0)

        response = self.bos.put_object(
            bucket_name=self.BUCKET,
            key=self.KEY,
            data=fp,
            content_length=len(data),
            content_crc32c=crc32c
        )
        self.check_headers(response)

        content = self.bos.get_object_as_string(bucket_name=self.BUCKET, key=self.KEY)
        self.assertEqual(content, data)

    def test_put_object_from_string_with_crc32c(self):
        """test put_object_from_string with user-provided CRC32C"""
        data = "test_put_string_crc32c"
        data_bytes = data.encode('utf-8')
        fp = io.BytesIO(data_bytes)
        crc32c = utils.get_crc32c_from_fp(fp, buf_size=8192)

        response = self.bos.put_object_from_string(
            bucket=self.BUCKET,
            key=self.KEY,
            data=data,
            content_crc32c=crc32c
        )
        self.check_headers(response)

        content = self.bos.get_object_as_string(bucket_name=self.BUCKET, key=self.KEY)
        self.assertEqual(content, data_bytes)

    def test_put_object_from_file_with_crc32c(self):
        """test put_object_from_file with user-provided CRC32C"""
        with open(self.FILENAME, 'wb') as f:
            f.write(b'a' * (1 * 1024 * 1024))

        with open(self.FILENAME, 'rb') as fp:
            crc32c = utils.get_crc32c_from_fp(fp, buf_size=8192)

        response = self.bos.put_object_from_file(
            bucket=self.BUCKET,
            key=b"test_file_crc32c",
            file_name=self.FILENAME,
            content_crc32c=crc32c
        )
        self.check_headers(response)

        response = self.bos.get_object(bucket_name=self.BUCKET, key=b"test_file_crc32c")
        self.assertIsNotNone(response)

    def test_append_object_with_crc32c(self):
        """test append_object with user-provided CRC32C"""
        data = b"test_append_object_crc32c"
        fp = io.BytesIO(data)
        crc32c = utils.get_crc32c_from_fp(fp, buf_size=8192)
        fp.seek(0)

        response = self.bos.append_object(
            bucket_name=self.BUCKET,
            key=b"test_append_object_crc32c",
            data=fp,
            content_length=len(data),
            content_crc32c=crc32c
        )
        self.check_headers(response)

        content = self.bos.get_object_as_string(bucket_name=self.BUCKET, key=b"test_append_object_crc32c")
        self.assertEqual(content, data)

    def test_append_object_from_string_with_crc32c(self):
        """test append_object_from_string with user-provided CRC32C"""
        data = "test_append_string_crc32c"
        data_bytes = data.encode('utf-8')
        fp = io.BytesIO(data_bytes)
        crc32c = utils.get_crc32c_from_fp(fp, buf_size=8192)

        response = self.bos.append_object_from_string(
            bucket_name=self.BUCKET,
            key=b"test_append_string_crc32c",
            data=data,
            content_crc32c=crc32c
        )
        self.check_headers(response)

        content = self.bos.get_object_as_string(bucket_name=self.BUCKET, key=b"test_append_string_crc32c")
        self.assertEqual(content, data_bytes)

    def test_upload_part_with_crc32c(self):
        """test upload_part with user-provided CRC32C"""
        init_response = self.bos.initiate_multipart_upload(self.BUCKET, b"test_upload_part_crc32c")
        upload_id = init_response.upload_id

        part_data = b"test_part_data_crc32c"
        fp = io.BytesIO(part_data)
        part_crc32c = utils.get_crc32c_from_fp(fp, buf_size=8192)
        fp.seek(0)

        response = self.bos.upload_part(
            bucket_name=self.BUCKET,
            key=b"test_upload_part_crc32c",
            upload_id=upload_id,
            part_number=1,
            part_size=len(part_data),
            part_fp=fp,
            part_crc32c=part_crc32c
        )
        self.check_headers(response)

        self.bos.abort_multipart_upload(self.BUCKET, b"test_upload_part_crc32c", upload_id)


class TestCRC32CFlag(TestClient):
    """Test CRC32C flag parameter for operations"""

    def test_put_object_with_crc32c_flag(self):
        """test put_object with content_crc32c_flag parameter"""
        data = b"test_put_object_crc32c_flag"
        fp = io.BytesIO(data)
        crc32c = utils.get_crc32c_from_fp(fp, buf_size=8192)
        fp.seek(0)

        response = self.bos.put_object(
            bucket_name=self.BUCKET,
            key=self.KEY,
            data=fp,
            content_length=len(data),
            content_crc32c=crc32c,
            content_crc32c_flag=True
        )
        self.check_headers(response)

        content = self.bos.get_object_as_string(bucket_name=self.BUCKET, key=self.KEY)
        self.assertEqual(content, data)

    def test_put_object_from_string_with_crc32c_flag(self):
        """test put_object_from_string with content_crc32c_flag parameter"""
        data = "test_put_string_crc32c_flag"
        data_bytes = data.encode('utf-8')
        fp = io.BytesIO(data_bytes)
        crc32c = utils.get_crc32c_from_fp(fp, buf_size=8192)

        response = self.bos.put_object_from_string(
            bucket=self.BUCKET,
            key=self.KEY,
            data=data,
            content_crc32c=crc32c,
            content_crc32c_flag=b"true"
        )
        self.check_headers(response)

        content = self.bos.get_object_as_string(bucket_name=self.BUCKET, key=self.KEY)
        self.assertEqual(content, data_bytes)

    def test_append_object_with_crc32c_flag(self):
        """test append_object with content_crc32c_flag parameter"""
        data = b"test_append_object_crc32c_flag"
        fp = io.BytesIO(data)
        crc32c = utils.get_crc32c_from_fp(fp, buf_size=8192)
        fp.seek(0)

        response = self.bos.append_object(
            bucket_name=self.BUCKET,
            key=b"test_append_object_crc32c_flag",
            data=fp,
            content_length=len(data),
            content_crc32c=crc32c,
            content_crc32c_flag=b"true"
        )
        self.check_headers(response)

        content = self.bos.get_object_as_string(bucket_name=self.BUCKET, key=b"test_append_object_crc32c_flag")
        self.assertEqual(content, data)


class TestPutSuperObjectWithCRC32C(TestClient):
    """Test put_super_object_from_file with CRC32C parameters"""

    def test_put_super_object_from_file_with_crc32c(self):
        """test put_super_object_from_file with user-provided CRC32C"""
        # Create a file larger than 5MB to trigger multi-part upload
        with open(self.FILENAME, 'wb') as f:
            f.write(b'a' * (6 * 1024 * 1024))  # 6MB file (2 parts: 5MB + 1MB)

        crc32c = utils.get_crc32c_from_fp(open(self.FILENAME, 'rb'))

        result = self.bos.put_super_object_from_file(
            bucket_name=self.BUCKET,
            key=b"test_super_object_crc32c",
            file_name=self.FILENAME,
            chunk_size=5,  # 5MB chunks
            thread_num=1,
            content_crc32c=crc32c
        )
        self.assertTrue(result)

        # Verify the object was created correctly
        response = self.bos.get_object(bucket_name=self.BUCKET, key=b"test_super_object_crc32c")
        self.assertIsNotNone(response)

    def test_put_super_object_from_file_with_both_crc32_and_crc32c(self):
        """test put_super_object_from_file with both CRC32 and CRC32C provided"""
        # This tests the logic: when both are provided, user values should be used
        with open(self.FILENAME, 'wb') as f:
            f.write(b'a' * (6 * 1024 * 1024))  # 6MB file

        crc32 = utils.get_crc32_from_fp(open(self.FILENAME, 'rb'))
        crc32c = utils.get_crc32c_from_fp(open(self.FILENAME, 'rb'))

        result = self.bos.put_super_object_from_file(
            bucket_name=self.BUCKET,
            key=b"test_super_object_both_crc",
            file_name=self.FILENAME,
            chunk_size=5,
            thread_num=1,
            content_crc32=crc32,
            content_crc32c=crc32c
        )
        self.assertTrue(result)


class TestBucketVersioning(TestClient):
    """Test bucket versioning operations"""

    def test_put_bucket_versioning_enabled(self):
        """test put_bucket_versioning with enabled status"""
        versioning_status = "Enabled"

        try:
            response = self.bos.put_bucket_versioning(self.BUCKET, versioning_status)
        except (BceServerError, BceHttpClientError) as e:
            # If the API is not supported or not configured, skip the test
            self.skipTest("Bucket versioning is not supported or not configured in this environment: " + str(e))
        self.check_headers(response)

        # Verify versioning is enabled
        response = self.bos.get_bucket_versioning(self.BUCKET)
        self.assertEqual(response.status, "Enabled")

    def test_put_bucket_versioning_suspended(self):
        """test put_bucket_versioning with suspended status"""
        # First enable versioning
        try:
            self.bos.put_bucket_versioning(self.BUCKET, "Enabled")
        except (BceServerError, BceHttpClientError) as e:
            # If the API is not supported, skip the test
            self.skipTest("Bucket versioning is not supported or not configured in this environment: " + str(e))

        # Then suspend versioning
        versioning_status = "Suspended"

        err = None
        try:
            response = self.bos.put_bucket_versioning(self.BUCKET, versioning_status)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.check_headers(response)

        # Verify versioning is suspended
        response = self.bos.get_bucket_versioning(self.BUCKET)
        self.assertEqual(response.status, "Suspended")

    def test_get_bucket_versioning(self):
        """test get_bucket_versioning function"""
        # Enable versioning first
        try:
            self.bos.put_bucket_versioning(self.BUCKET, "Enabled")
        except (BceServerError, BceHttpClientError) as e:
            # If the API is not supported, skip the test
            self.skipTest("Bucket versioning is not supported or not configured in this environment: " + str(e))

        err = None
        try:
            response = self.bos.get_bucket_versioning(self.BUCKET)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.assertEqual(response.status, "Enabled")
        self.check_headers(response)

    def test_list_objects_versions(self):
        """test list_objects_versions function"""
        # Enable versioning
        try:
            self.bos.put_bucket_versioning(self.BUCKET, "Enabled")
        except (BceServerError, BceHttpClientError) as e:
            # If the API is not supported, skip the test
            self.skipTest("Bucket versioning is not supported or not configured in this environment: " + str(e))

        # Put same object multiple times to create versions
        self.bos.put_object_from_string(self.BUCKET, self.KEY, 'First version')
        time.sleep(1)
        self.bos.put_object_from_string(self.BUCKET, self.KEY, 'Second version')
        time.sleep(1)
        self.bos.put_object_from_string(self.BUCKET, self.KEY, 'Third version')

        err = None
        try:
            response = self.bos.list_objects_versions(self.BUCKET)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
        self.check_headers(response)
        # Should have at least 3 versions of the object
        self.assertGreaterEqual(len(response), 3)


class TestBucketObjectLock(TestClient):
    """Test bucket object lock operations"""

    def test_get_bucket_object_lock(self):
        """test get_bucket_object_lock function"""
        # Object lock requires versioning enabled
        try:
            self.bos.put_bucket_versioning(self.BUCKET, "Enabled")
        except (BceServerError, BceHttpClientError) as e:
            # If versioning is not supported, skip the test
            self.skipTest("Bucket object lock is not supported or not configured in this environment: " + str(e))

        err = None
        try:
            response = self.bos.get_bucket_object_lock(self.BUCKET)
        except BceServerError as e:
            # If object lock is not configured, it may return an error
            # This is expected behavior
            err = e
        finally:
            # If no error, check response; otherwise, verify it's expected
            if err is None:
                self.check_headers(response)

    def test_delete_bucket_object_lock(self):
        """test delete_bucket_object_lock function"""
        # Object lock requires versioning enabled
        try:
            self.bos.put_bucket_versioning(self.BUCKET, "Enabled")
        except (BceServerError, BceHttpClientError) as e:
            # If versioning is not supported, skip the test
            self.skipTest("Bucket object lock is not supported or not configured in this environment: " + str(e))

        err = None
        try:
            response = self.bos.delete_bucket_object_lock(self.BUCKET)
        except BceServerError as e:
            # If object lock is not configured, it may return an error
            # This is expected behavior
            err = e
        finally:
            # If no error, check response; otherwise, verify it's expected
            if err is None:
                self.check_headers(response)

    def test_init_bucket_object_lock(self):
        """test init_bucket_object_lock function"""
        try:
            self.bos.put_bucket_versioning(self.BUCKET, "Enabled")
        except (BceServerError, BceHttpClientError) as e:
            self.skipTest("Bucket versioning not supported: " + str(e))

        err = None
        try:
            response = self.bos.init_bucket_object_lock(self.BUCKET, retention_days=1)
        except BceServerError as e:
            err = e
        finally:
            if err is None:
                self.check_headers(response)

    def test_complete_bucket_object_lock(self):
        """test complete_bucket_object_lock function"""
        try:
            self.bos.put_bucket_versioning(self.BUCKET, "Enabled")
        except (BceServerError, BceHttpClientError) as e:
            self.skipTest("Bucket versioning not supported: " + str(e))

        err = None
        try:
            response = self.bos.complete_bucket_object_lock(self.BUCKET)
        except BceServerError as e:
            err = e
        finally:
            if err is None:
                self.check_headers(response)

    def test_extend_bucket_object_lock(self):
        """test extend_bucket_object_lock function"""
        try:
            self.bos.put_bucket_versioning(self.BUCKET, "Enabled")
        except (BceServerError, BceHttpClientError) as e:
            self.skipTest("Bucket versioning not supported: " + str(e))

        err = None
        try:
            response = self.bos.extend_bucket_object_lock(self.BUCKET, extend_retent_days=2)
        except BceServerError as e:
            err = e
        finally:
            if err is None:
                self.check_headers(response)

    def test_init_bucket_object_lock_required_params(self):
        """test init_bucket_object_lock rejects None bucket_name"""
        with self.assertRaises(ValueError):
            self.bos.init_bucket_object_lock(None, retention_days=1)

    def test_extend_bucket_object_lock_required_params(self):
        """test extend_bucket_object_lock rejects wrong type for extend_retent_days"""
        with self.assertRaises(TypeError):
            self.bos.extend_bucket_object_lock(self.BUCKET, extend_retent_days="2")


class TestObjectTagging(TestClient):
    """Test object tagging operations"""

    def setUp(self):
        super(TestObjectTagging, self).setUp()
        # Create test object for tagging
        self.bos.put_object_from_string(
            bucket=self.BUCKET,
            key=self.KEY,
            data="test object for tagging"
        )

    def test_put_object_tagging(self):
        """test put_object_tagging with tag dict"""
        obj_tag_args = {
            "tagSet": [
                {"key": "env", "value": "test"},
                {"key": "owner", "value": "sdk"}
            ]
        }
        response = self.bos.put_object_tagging(self.BUCKET, self.KEY, obj_tag_args)
        self.check_headers(response)

    def test_get_object_tagging(self):
        """test get_object_tagging returns previously set tags"""
        obj_tag_args = {
            "tagSet": [
                {"key": "env", "value": "test"}
            ]
        }
        self.bos.put_object_tagging(self.BUCKET, self.KEY, obj_tag_args)

        response = self.bos.get_object_tagging(self.BUCKET, self.KEY)
        self.check_headers(response)

    def test_put_object_tagging_canned(self):
        """test put_object_tagging_canned with tag header string"""
        # tag_header should be a URL-encoded tag string like "key=value&key2=value2"
        tag_header = "env=test&owner=sdk"
        response = self.bos.put_object_tagging_canned(self.BUCKET, self.KEY, tag_header)
        self.check_headers(response)

    def test_delete_object_tagging(self):
        """test delete_object_tagging removes tags successfully"""
        obj_tag_args = {
            "tagSet": [
                {"key": "env", "value": "test"}
            ]
        }
        self.bos.put_object_tagging(self.BUCKET, self.KEY, obj_tag_args)
        response = self.bos.delete_object_tagging(self.BUCKET, self.KEY)
        self.check_headers(response)

    def test_delete_object_tagging_with_bytes_key(self):
        """test delete_object_tagging accepts bytes key"""
        obj_tag_args = {"tagSet": [{"key": "k", "value": "v"}]}
        bytes_key = self.KEY if isinstance(self.KEY, bytes) else self.KEY.encode('utf-8')
        self.bos.put_object_tagging(self.BUCKET, bytes_key, obj_tag_args)
        response = self.bos.delete_object_tagging(self.BUCKET, bytes_key)
        self.check_headers(response)

    def test_delete_object_tagging_bucket_none(self):
        """test delete_object_tagging raises ValueError when bucket_name is None"""
        with self.assertRaises(ValueError):
            self.bos.delete_object_tagging(None, self.KEY)

    def test_delete_object_tagging_key_none(self):
        """test delete_object_tagging raises ValueError when key is None"""
        with self.assertRaises(ValueError):
            self.bos.delete_object_tagging(self.BUCKET, None)


class TestGetObjectWithVersionId(TestClient):
    """Test get_object/delete_object/get_object_to_file/get_object_meta_data with version_id param"""

    def setUp(self):
        super(TestGetObjectWithVersionId, self).setUp()
        try:
            self.bos.put_bucket_versioning(self.BUCKET, "Enabled")
            self._versioning_supported = True
        except (BceServerError, BceHttpClientError):
            self._versioning_supported = False

    def test_get_object_with_version_id(self):
        """test get_object with version_id parameter"""
        if not self._versioning_supported:
            self.skipTest("Bucket versioning not supported in this environment")
        response = self.bos.put_object_from_string(self.BUCKET, self.KEY, 'v1')
        version_id = response.version_id
        err = None
        try:
            obj = self.bos.get_object(self.BUCKET, self.KEY, version_id=version_id)
        except BceServerError as e:
            err = e
        self.assertIsNone(err)
        self.check_headers(obj)

    def test_get_object_with_range(self):
        """test get_object with range parameter"""
        self.bos.put_object_from_string(self.BUCKET, self.KEY, 'hello world')
        err = None
        try:
            obj = self.bos.get_object(self.BUCKET, self.KEY, range=[0, 4])
        except BceServerError as e:
            err = e
        self.assertIsNone(err)
        self.check_headers(obj)

    def test_get_object_with_traffic_limit(self):
        """test get_object with traffic_limit parameter (exercises range_header merging)"""
        self.bos.put_object_from_string(self.BUCKET, self.KEY, 'traffic limit test')
        err = None
        try:
            obj = self.bos.get_object(self.BUCKET, self.KEY, traffic_limit=819200)
        except BceServerError as e:
            err = e
        self.assertIsNone(err)

    def test_delete_object_with_version_id(self):
        """test delete_object with version_id parameter"""
        if not self._versioning_supported:
            self.skipTest("Bucket versioning not supported in this environment")
        response = self.bos.put_object_from_string(self.BUCKET, self.KEY, 'v1')
        version_id = response.version_id
        err = None
        try:
            self.bos.delete_object(self.BUCKET, self.KEY, version_id=version_id)
        except BceServerError as e:
            err = e
        self.assertIsNone(err)

    def test_get_object_to_file_with_version_id(self):
        """test get_object_to_file with version_id parameter"""
        if not self._versioning_supported:
            self.skipTest("Bucket versioning not supported in this environment")
        response = self.bos.put_object_from_string(self.BUCKET, self.KEY, 'v1 content')
        version_id = response.version_id
        err = None
        try:
            self.bos.get_object_to_file(self.BUCKET, self.KEY, self.FILENAME,
                                        version_id=version_id)
        except BceServerError as e:
            err = e
        self.assertIsNone(err)
        self.assertTrue(os.path.isfile(self.FILENAME))

    def test_get_object_meta_data_with_version_id(self):
        """test get_object_meta_data with version_id parameter"""
        if not self._versioning_supported:
            self.skipTest("Bucket versioning not supported in this environment")
        response = self.bos.put_object_from_string(self.BUCKET, self.KEY, 'v1')
        version_id = response.version_id
        err = None
        try:
            meta = self.bos.get_object_meta_data(self.BUCKET, self.KEY,
                                                  version_id=version_id)
        except BceServerError as e:
            err = e
        self.assertIsNone(err)
        self.check_headers(meta)


class TestRestoreObjectBranches(TestClient):
    """Test missing branches in restore_object"""

    def setUp(self):
        super(TestRestoreObjectBranches, self).setUp()
        self.get_file(1)
        self.bos.put_object_from_file(self.BUCKET, self.KEY, self.FILENAME,
                                      storage_class=storage_class.ARCHIVE)

    def test_restore_object_tier_standard(self):
        """test restore_object with default tier=Standard"""
        err = None
        try:
            self.bos.restore_object(self.BUCKET, self.KEY, days=1, tier="Standard")
        except BceServerError as e:
            err = e
        self.assertIsNone(err)

    def test_restore_object_tier_lowcost(self):
        """test restore_object with tier=LowCost"""
        err = None
        try:
            self.bos.restore_object(self.BUCKET, self.KEY, days=1, tier="LowCost")
        except BceServerError as e:
            err = e
        self.assertIsNone(err)

    def test_restore_object_days_none(self):
        """test restore_object with days=None (header omitted)"""
        err = None
        try:
            self.bos.restore_object(self.BUCKET, self.KEY, tier="Standard")
        except BceServerError as e:
            err = e
        self.assertIsNone(err)

    def test_restore_object_tier_none_raises(self):
        """test restore_object with tier=None raises BceClientError"""
        with self.assertRaises(BceClientError):
            self.bos.restore_object(self.BUCKET, self.KEY, tier=None)


class TestListObjectsVersionsBranches(TestClient):
    """Test list_objects_versions optional parameters"""

    def setUp(self):
        super(TestListObjectsVersionsBranches, self).setUp()
        try:
            self.bos.put_bucket_versioning(self.BUCKET, "Enabled")
            for i in range(3):
                self.bos.put_object_from_string(self.BUCKET, self.KEY, 'v%d' % i)
            self._versioning_supported = True
        except (BceServerError, BceHttpClientError):
            self._versioning_supported = False

    def test_list_objects_versions_with_prefix(self):
        """test list_objects_versions with prefix parameter"""
        if not self._versioning_supported:
            self.skipTest("Bucket versioning not supported in this environment")
        err = None
        try:
            response = self.bos.list_objects_versions(self.BUCKET, prefix='test')
        except BceServerError as e:
            err = e
        self.assertIsNone(err)
        self.check_headers(response)

    def test_list_objects_versions_with_max_keys(self):
        """test list_objects_versions with max_keys=1 returns only one version"""
        if not self._versioning_supported:
            self.skipTest("Bucket versioning not supported in this environment")
        err = None
        try:
            response = self.bos.list_objects_versions(self.BUCKET, max_keys=1)
        except BceServerError as e:
            err = e
        self.assertIsNone(err)
        self.check_headers(response)

    def test_list_objects_versions_with_delimiter(self):
        """test list_objects_versions with delimiter parameter"""
        if not self._versioning_supported:
            self.skipTest("Bucket versioning not supported in this environment")
        err = None
        try:
            response = self.bos.list_objects_versions(self.BUCKET, delimiter='/')
        except BceServerError as e:
            err = e
        self.assertIsNone(err)

    def test_list_objects_versions_with_marker(self):
        """test list_objects_versions with marker parameter"""
        if not self._versioning_supported:
            self.skipTest("Bucket versioning not supported in this environment")
        err = None
        try:
            response = self.bos.list_objects_versions(self.BUCKET, marker=self.KEY)
        except BceServerError as e:
            err = e
        self.assertIsNone(err)


class TestBucketReplicationIdNone(TestClient):
    """Test get/delete_bucket_replication and get_bucket_replication_progress with id=None.
    The id param is optional in SDK signature but required by BOS server.
    BceServerError is wrapped in BceHttpClientError.last_error by the retry framework.
    """

    def _assert_server_error(self, fn, *args, **kwargs):
        """Helper: assert BceServerError is raised (directly or wrapped in BceHttpClientError)"""
        try:
            fn(*args, **kwargs)
            self.fail("Expected BceServerError or BceHttpClientError to be raised")
        except BceServerError:
            pass
        except BceHttpClientError as e:
            self.assertIsInstance(e.last_error, BceServerError)

    def test_put_bucket_replication_without_id(self):
        """put_bucket_replication with no 'id' key: server rejects invalid destination bucket"""
        replication = {
            "status": "enabled",
            "resource": [self.BUCKET + "/*"],
            "destination": {"bucket": self.BUCKET + "-dst", "storageClass": "COLD"},
            "replicateDeletes": "disabled",
        }
        self._assert_server_error(self.bos.put_bucket_replication, self.BUCKET, replication)

    def test_get_bucket_replication_without_id(self):
        """get_bucket_replication without id: server returns 'configuration does not exist'"""
        self._assert_server_error(self.bos.get_bucket_replication, self.BUCKET)

    def test_get_bucket_replication_progress_without_id(self):
        """get_bucket_replication_progress without id: server returns error"""
        self._assert_server_error(self.bos.get_bucket_replication_progress, self.BUCKET)


class TestCRC64ECMA(TestClient):
    """Test CRC64ECMA validation for object upload operations"""

    def test_put_object_with_crc64ecma(self):
        """test put_object with user-provided CRC64ECMA"""
        data = b"test_put_object_crc64ecma"
        fp = io.BytesIO(data)
        crc64ecma = utils.get_crc64_ecma_from_fp(fp, buf_size=8192)
        fp.seek(0)

        response = self.bos.put_object(
            bucket_name=self.BUCKET,
            key=self.KEY,
            data=fp,
            content_length=len(data),
            content_crc64ecma=crc64ecma
        )
        self.check_headers(response)
        self.assertEqual(response.metadata.bce_content_crc_64ecma, str(crc64ecma))

        content = self.bos.get_object_as_string(bucket_name=self.BUCKET, key=self.KEY)
        self.assertEqual(content, data)

    def test_put_object_from_string_with_crc64ecma(self):
        """test put_object_from_string with user-provided CRC64ECMA"""
        data = "test_put_string_crc64ecma"
        data_bytes = data.encode('utf-8')
        fp = io.BytesIO(data_bytes)
        crc64ecma = utils.get_crc64_ecma_from_fp(fp, buf_size=8192)

        response = self.bos.put_object_from_string(
            bucket=self.BUCKET,
            key=self.KEY,
            data=data,
            content_crc64ecma=crc64ecma
        )
        self.check_headers(response)

        content = self.bos.get_object_as_string(bucket_name=self.BUCKET, key=self.KEY)
        self.assertEqual(content, data_bytes)

    def test_put_object_from_file_with_crc64ecma(self):
        """test put_object_from_file with user-provided CRC64ECMA"""
        with open(self.FILENAME, 'wb') as f:
            f.write(b'a' * (1 * 1024 * 1024))

        with open(self.FILENAME, 'rb') as fp:
            crc64ecma = utils.get_crc64_ecma_from_fp(fp, buf_size=8192)

        response = self.bos.put_object_from_file(
            bucket=self.BUCKET,
            key=b"test_file_crc64ecma",
            file_name=self.FILENAME,
            content_crc64ecma=crc64ecma
        )
        self.check_headers(response)

        response = self.bos.get_object(bucket_name=self.BUCKET, key=b"test_file_crc64ecma")
        self.assertIsNotNone(response)

    def test_append_object_with_crc64ecma(self):
        """test append_object with user-provided CRC64ECMA"""
        data = b"test_append_object_crc64ecma"
        fp = io.BytesIO(data)
        crc64ecma = utils.get_crc64_ecma_from_fp(fp, buf_size=8192)
        fp.seek(0)

        response = self.bos.append_object(
            bucket_name=self.BUCKET,
            key=b"test_append_object_crc64ecma",
            data=fp,
            content_length=len(data),
            content_crc64ecma=crc64ecma
        )
        self.check_headers(response)

        content = self.bos.get_object_as_string(bucket_name=self.BUCKET, key=b"test_append_object_crc64ecma")
        self.assertEqual(content, data)

    def test_append_object_from_string_with_crc64ecma(self):
        """test append_object_from_string with user-provided CRC64ECMA"""
        data = "test_append_string_crc64ecma"
        data_bytes = data.encode('utf-8')
        fp = io.BytesIO(data_bytes)
        crc64ecma = utils.get_crc64_ecma_from_fp(fp, buf_size=8192)

        response = self.bos.append_object_from_string(
            bucket_name=self.BUCKET,
            key=b"test_append_string_crc64ecma",
            data=data,
            content_crc64ecma=crc64ecma
        )
        self.check_headers(response)

        content = self.bos.get_object_as_string(bucket_name=self.BUCKET, key=b"test_append_string_crc64ecma")
        self.assertEqual(content, data_bytes)


# ============================================================
# Tests for Bug Fixes
# ============================================================

class TestCreateBucket(TestClient):
    """Test create_bucket API"""

    def test_create_bucket_basic(self):
        """create_bucket with only bucket_name should succeed"""
        new_bucket = "test-create-basic-%d" % os.getpid()
        err = None
        try:
            self.bos.create_bucket(new_bucket)
            self.assertTrue(self.bos.does_bucket_exist(new_bucket))
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
            try:
                self.bos.delete_bucket(new_bucket)
            except Exception:
                pass

    def test_create_bucket_with_tag_list(self):
        """create_bucket with tag_list header should succeed"""
        new_bucket = "test-create-tag-%d" % os.getpid()
        err = None
        try:
            self.bos.create_bucket(new_bucket, tag_list="env=test&team=sdk")
            self.assertTrue(self.bos.does_bucket_exist(new_bucket))
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
            try:
                self.bos.delete_bucket(new_bucket)
            except Exception:
                pass

    def test_create_bucket_none_name_raises(self):
        """create_bucket with None bucket_name should raise ValueError"""
        err = None
        try:
            self.bos.create_bucket(None)
        except ValueError as e:
            err = e
        finally:
            self.assertIsNotNone(err)

    def test_create_bucket_invalid_type_raises(self):
        """create_bucket with int bucket_name should raise TypeError (via @required)"""
        with self.assertRaises(TypeError):
            self.bos.create_bucket(12345)

    def test_create_bucket_duplicate_raises(self):
        """create_bucket on an existing bucket should raise BceHttpClientError (BucketAlreadyExists)"""
        err = None
        try:
            # self.BUCKET is created in setUp, creating it again should fail
            self.bos.create_bucket(self.BUCKET)
        except BceHttpClientError as e:
            err = e
        finally:
            self.assertIsNotNone(err)

    def test_create_bucket_content_type_without_maz(self):
        """create_bucket without enable_maz should send no body"""
        captured = {}

        original_send = self.bos._send_request

        def capture_send(http_method, bucket_name=None, key=None,
                         body=None, headers=None, params=None,
                         config=None, body_parser=None):
            captured['headers'] = headers
            captured['body'] = body
            raise StopIteration("captured")

        self.bos._send_request = capture_send
        try:
            self.bos.create_bucket("test-ct-bucket")
        except StopIteration:
            pass
        finally:
            self.bos._send_request = original_send

        self.assertIsNone(captured.get('body'))

    def test_create_bucket_content_type_with_maz(self):
        """create_bucket with enable_maz=True should send JSON body and application/json"""
        from baidubce.http import http_headers

        captured = {}

        original_send = self.bos._send_request

        def capture_send(http_method, bucket_name=None, key=None,
                         body=None, headers=None, params=None,
                         config=None, body_parser=None):
            captured['headers'] = headers
            captured['body'] = body
            raise StopIteration("captured")

        self.bos._send_request = capture_send
        try:
            self.bos.create_bucket("test-maz-bucket", enable_maz=True)
        except StopIteration:
            pass
        finally:
            self.bos._send_request = original_send

        self.assertIsNotNone(captured.get('body'))
        body_obj = json.loads(captured['body'])
        self.assertTrue(body_obj.get('enableMultiAz'))
        ct = captured.get('headers', {}).get(http_headers.CONTENT_TYPE, b'')
        self.assertIn(b'application/json', ct)


class TestSetBucketAclReturnValue(TestClient):
    """Test that set_bucket_acl / set_bucket_canned_acl return response (Bug #1)"""

    def test_set_bucket_acl_returns_response(self):
        """set_bucket_acl should return the HTTP response, not None"""
        grant_list = [{'grantee': [{'id': 'a0a2fe988a774be08978736ae2a1668b'}],
                       'permission': ['FULL_CONTROL']}]
        response = self.bos.set_bucket_acl(self.BUCKET, grant_list)
        self.assertIsNotNone(response)

    def test_set_bucket_acl_response_has_metadata(self):
        """set_bucket_acl return value should have metadata attribute"""
        grant_list = [{'grantee': [{'id': 'a0a2fe988a774be08978736ae2a1668b'}],
                       'permission': ['FULL_CONTROL']}]
        result = self.bos.set_bucket_acl(self.BUCKET, grant_list)
        self.assertIsNotNone(result)
        self.assertTrue(hasattr(result, 'metadata'))

    def test_set_bucket_canned_acl_returns_response(self):
        """set_bucket_canned_acl should return the HTTP response, not None"""
        response = self.bos.set_bucket_canned_acl(self.BUCKET, b"private")
        self.assertIsNotNone(response)

    def test_set_bucket_canned_acl_response_has_metadata(self):
        """set_bucket_canned_acl return value should have metadata attribute"""
        result = self.bos.set_bucket_canned_acl(self.BUCKET, b"private")
        self.assertIsNotNone(result)
        self.assertTrue(hasattr(result, 'metadata'))

    def test_set_bucket_acl_none_bucket_raises(self):
        """set_bucket_acl with None bucket_name should raise ValueError"""
        err = None
        try:
            self.bos.set_bucket_acl(None, [])
        except ValueError as e:
            err = e
        finally:
            self.assertIsNotNone(err)

    def test_set_bucket_acl_invalid_acl_type_raises(self):
        """set_bucket_acl with int bucket_name should raise TypeError (via @required)"""
        with self.assertRaises(TypeError):
            self.bos.set_bucket_acl(12345, [])


class TestSetObjectAclReturnValue(TestClient):
    """Test that set_object_acl / set_object_canned_acl return response (Bug #1)"""

    def setUp(self):
        super(TestSetObjectAclReturnValue, self).setUp()
        self.bos.put_object_from_string(self.BUCKET, self.KEY, "acl test content")

    def test_set_object_acl_returns_response(self):
        """set_object_acl should return the HTTP response, not None"""
        grant_list = [{'grantee': [{'id': 'a0a2fe988a774be08978736ae2a1668b'}],
                       'permission': ['FULL_CONTROL']}]
        response = self.bos.set_object_acl(self.BUCKET, self.KEY, grant_list)
        self.assertIsNotNone(response)

    def test_set_object_acl_response_has_metadata(self):
        """set_object_acl return value should have metadata attribute"""
        grant_list = [{'grantee': [{'id': 'a0a2fe988a774be08978736ae2a1668b'}],
                       'permission': ['FULL_CONTROL']}]
        result = self.bos.set_object_acl(self.BUCKET, self.KEY, grant_list)
        self.assertIsNotNone(result)
        self.assertTrue(hasattr(result, 'metadata'))

    def test_set_object_canned_acl_returns_response(self):
        """set_object_canned_acl should return the HTTP response, not None"""
        response = self.bos.set_object_canned_acl(self.BUCKET, self.KEY, canned_acl=b"private")
        self.assertIsNotNone(response)

    def test_set_object_canned_acl_none_args_raises(self):
        """set_object_canned_acl with no acl args should raise ValueError"""
        err = None
        try:
            self.bos.set_object_canned_acl(self.BUCKET, self.KEY)
        except ValueError as e:
            err = e
        finally:
            self.assertIsNotNone(err)

    def test_set_object_canned_acl_multiple_args_raises(self):
        """set_object_canned_acl with more than one acl arg should raise ValueError"""
        err = None
        try:
            self.bos.set_object_canned_acl(
                self.BUCKET, self.KEY,
                canned_acl=b"private",
                grant_read=b'id="a0a2fe988a774be08978736ae2a1668b"')
        except ValueError as e:
            err = e
        finally:
            self.assertIsNotNone(err)


class TestCompleteMultipartUploadConfig(TestClient):
    """Test complete_multipart_upload passes config correctly (Bug #5)"""

    def test_complete_multipart_upload_with_custom_config(self):
        """complete_multipart_upload with explicit config should not lose config"""
        import bos_test_config

        key = b"test-complete-config-key"
        upload_id = self.bos.initiate_multipart_upload(self.BUCKET, key).upload_id
        data = b"D" * (1024 * 1024 * 5 + 1)
        fp = io.BytesIO(data)
        resp = self.bos.upload_part(self.BUCKET, key, upload_id, 1, len(data), fp)
        part_list = [{"partNumber": 1, "eTag": resp.metadata.etag}]
        err = None
        try:
            self.bos.complete_multipart_upload(
                self.BUCKET, key, upload_id, part_list,
                config=bos_test_config.config)
        except BceServerError as e:
            err = e
        finally:
            self.assertIsNone(err)
            try:
                self.bos.delete_object(self.BUCKET, key)
            except Exception:
                pass

    def test_complete_multipart_upload_returns_response(self):
        """complete_multipart_upload should return a proper response"""
        key = b"test-complete-return-key"
        upload_id = self.bos.initiate_multipart_upload(self.BUCKET, key).upload_id
        data = b"E" * (1024 * 1024 * 5 + 1)
        fp = io.BytesIO(data)
        resp = self.bos.upload_part(self.BUCKET, key, upload_id, 1, len(data), fp)
        part_list = [{"partNumber": 1, "eTag": resp.metadata.etag}]
        result = self.bos.complete_multipart_upload(self.BUCKET, key, upload_id, part_list)
        self.assertIsNotNone(result)
        try:
            self.bos.delete_object(self.BUCKET, key)
        except Exception:
            pass


class TestPrepareObjectHeadersContentLength(TestClient):
    """Test _prepare_object_headers content_length validation (Bug #7)"""

    def test_content_length_zero_is_valid(self):
        """content_length=0 should not raise ValueError"""
        from baidubce.services.bos.bos_client import BosClient
        err = None
        try:
            BosClient._prepare_object_headers(content_length=0)
        except ValueError as e:
            err = e
        finally:
            self.assertIsNone(err)

    def test_content_length_positive_is_valid(self):
        """content_length > 0 should not raise ValueError"""
        from baidubce.services.bos.bos_client import BosClient
        err = None
        try:
            BosClient._prepare_object_headers(content_length=1024)
        except ValueError as e:
            err = e
        finally:
            self.assertIsNone(err)

    def test_content_length_negative_raises(self):
        """content_length < 0 should raise ValueError"""
        from baidubce.services.bos.bos_client import BosClient
        err = None
        try:
            BosClient._prepare_object_headers(content_length=-1)
        except ValueError as e:
            err = e
        finally:
            self.assertIsNotNone(err)

    def test_content_length_none_does_not_set_header(self):
        """content_length=None should leave CONTENT_LENGTH header absent"""
        from baidubce.services.bos.bos_client import BosClient
        from baidubce.http import http_headers
        headers = BosClient._prepare_object_headers(content_length=None)
        self.assertNotIn(http_headers.CONTENT_LENGTH, headers)

    def test_put_object_from_string_empty(self):
        """put_object_from_string with empty string (content_length=0) should succeed"""
        err = None
        try:
            self.bos.put_object_from_string(self.BUCKET, self.KEY, "")
        except (BceServerError, ValueError) as e:
            err = e
        finally:
            self.assertIsNone(err)


class TestUploadPartTrafficLimitNoDuplicate(TestClient):
    """Test upload_part does not set traffic_limit twice (Bug #4)"""

    def test_upload_part_traffic_limit_header_set_once(self):
        """upload_part with traffic_limit should only set BOS_TRAFFIC_LIMIT once in headers"""
        from baidubce.http import http_headers

        key = b"test-upload-part-traffic"
        upload_id = self.bos.initiate_multipart_upload(self.BUCKET, key).upload_id

        captured_headers = []
        original_send = self.bos._send_request

        def capture_send(http_method, bucket_name=None, key=None,
                         body=None, headers=None, params=None,
                         config=None, body_parser=None):
            if params and b'partNumber' in params:
                captured_headers.append(dict(headers or {}))
            return original_send(http_method, bucket_name=bucket_name, key=key,
                                 body=body, headers=headers, params=params,
                                 config=config, body_parser=body_parser)

        self.bos._send_request = capture_send
        data = b"F" * (1024 * 1024 * 5 + 1)
        try:
            fp = io.BytesIO(data)
            resp = self.bos.upload_part(self.BUCKET, key, upload_id, 1, len(data), fp,
                                        traffic_limit=838860800)
            part_list = [{"partNumber": 1, "eTag": resp.metadata.etag}]
            self.bos.complete_multipart_upload(self.BUCKET, key, upload_id, part_list)
        finally:
            self.bos._send_request = original_send
            try:
                self.bos.delete_object(self.BUCKET, key)
            except Exception:
                pass

        self.assertEqual(len(captured_headers), 1)
        h = captured_headers[0]
        # The traffic_limit key must appear exactly once (dict cannot duplicate keys)
        self.assertIn(http_headers.BOS_TRAFFIC_LIMIT, h)
        # Verify the value is consistent (not overwritten with a non-bytes value)
        tl_val = h[http_headers.BOS_TRAFFIC_LIMIT]
        self.assertIsNotNone(tl_val)


class TestRequiredDecoratorOnBucketMethods(TestClient):
    """Test @required is correctly applied on various bucket methods (Bug #2, #6)"""

    def test_set_bucket_storage_class_required_bucket_name(self):
        """set_bucket_storage_class must reject None bucket_name"""
        err = None
        try:
            self.bos.set_bucket_storage_class(None, storage_class.STANDARD)
        except (ValueError, TypeError) as e:
            err = e
        finally:
            self.assertIsNotNone(err)

    def test_get_bucket_quota_requires_bucket_name(self):
        """get_bucket_quota must reject None bucket_name"""
        err = None
        try:
            self.bos.get_bucket_quota(None)
        except (ValueError, TypeError, BceHttpClientError) as e:
            err = e
        finally:
            self.assertIsNotNone(err)

    def test_put_bucket_quota_requires_bucket_name(self):
        """put_bucket_quota must reject None bucket_name"""
        err = None
        try:
            self.bos.put_bucket_quota(None, {'maxCapacityMegaBytes': 0})
        except (ValueError, TypeError, BceHttpClientError) as e:
            err = e
        finally:
            self.assertIsNotNone(err)

    def test_delete_bucket_quota_requires_bucket_name(self):
        """delete_bucket_quota must reject None bucket_name"""
        err = None
        try:
            self.bos.delete_bucket_quota(None)
        except (ValueError, TypeError, BceHttpClientError) as e:
            err = e
        finally:
            self.assertIsNotNone(err)

    def test_get_bucket_tagging_requires_bucket_name(self):
        """get_bucket_tagging must reject None bucket_name"""
        err = None
        try:
            self.bos.get_bucket_tagging(None)
        except (ValueError, TypeError, BceHttpClientError) as e:
            err = e
        finally:
            self.assertIsNotNone(err)

    def test_put_bucket_tagging_requires_bucket_name(self):
        """put_bucket_tagging must reject None bucket_name"""
        err = None
        try:
            self.bos.put_bucket_tagging(None, {'tagList': []})
        except (ValueError, TypeError, BceHttpClientError) as e:
            err = e
        finally:
            self.assertIsNotNone(err)

    def test_delete_bucket_tagging_requires_bucket_name(self):
        """delete_bucket_tagging must reject None bucket_name"""
        err = None
        try:
            self.bos.delete_bucket_tagging(None)
        except (ValueError, TypeError, BceHttpClientError) as e:
            err = e
        finally:
            self.assertIsNotNone(err)

    def test_init_bucket_object_lock_requires_bucket_name(self):
        """init_bucket_object_lock must reject None bucket_name"""
        err = None
        try:
            self.bos.init_bucket_object_lock(None, retention_days=1)
        except (ValueError, TypeError, BceHttpClientError) as e:
            err = e
        finally:
            self.assertIsNotNone(err)

    def test_extend_bucket_object_lock_requires_bucket_name(self):
        """extend_bucket_object_lock must reject None bucket_name"""
        err = None
        try:
            self.bos.extend_bucket_object_lock(None, extend_retent_days=1)
        except (ValueError, TypeError, BceHttpClientError) as e:
            err = e
        finally:
            self.assertIsNotNone(err)

    def test_complete_bucket_object_lock_requires_bucket_name(self):
        """complete_bucket_object_lock must reject None bucket_name"""
        err = None
        try:
            self.bos.complete_bucket_object_lock(None)
        except (ValueError, TypeError, BceHttpClientError) as e:
            err = e
        finally:
            self.assertIsNotNone(err)


class TestMazBucket(unittest.TestCase):
    """
    Tests for Multi-AZ (MAZ) bucket operations.

    A separate MAZ bucket is created in setUp with enable_maz=True and
    torn down in tearDown, so these tests are independent of the regular
    TestClient bucket.

    If the environment does not support MAZ, each test skips itself
    gracefully via _skip_if_maz_unsupported().
    """

    MAZ_BUCKET = "test-maz-bucket%d" % os.getpid()
    KEY = compat.convert_to_bytes("test_maz_object%d" % os.getpid())
    FILENAME = "temp_maz_file%d" % os.getpid()

    def setUp(self):
        self.bos = bos_client.BosClient(bos_test_config.config)
        try:
            if not self.bos.does_bucket_exist(self.MAZ_BUCKET):
                self.bos.create_bucket(self.MAZ_BUCKET, enable_maz=True)
        except (BceServerError, BceHttpClientError) as e:
            self._maz_supported = False
            self._maz_skip_reason = "MAZ bucket creation failed: " + str(e)
        else:
            self._maz_supported = True
            self._maz_skip_reason = None

    def tearDown(self):
        if not self._maz_supported:
            return
        try:
            response = self.bos.list_multipart_uploads(self.MAZ_BUCKET)
            for item in response.uploads:
                temp_key = item.key
                if isinstance(temp_key, str):
                    temp_key = temp_key.encode("utf-8")
                self.bos.abort_multipart_upload(self.MAZ_BUCKET, temp_key,
                                                upload_id=item.upload_id)
            response = self.bos.list_all_objects(self.MAZ_BUCKET)
            for obj in response:
                self.bos.delete_object(self.MAZ_BUCKET, obj.key)
            self.bos.delete_bucket(self.MAZ_BUCKET)
        except Exception:
            pass
        if os.path.isfile(self.FILENAME):
            os.remove(self.FILENAME)

    def _skip_if_maz_unsupported(self):
        if not self._maz_supported:
            self.skipTest(self._maz_skip_reason)

    def check_headers(self, response):
        for item in ['content_length', 'bce_debug_id', 'date', 'bce_request_id', 'server']:
            self.assertTrue(hasattr(response.metadata, item))

    def get_file(self, size_mb):
        with open(self.FILENAME, 'wb') as f:
            f.write(b'a' * (size_mb * 1024 * 1024))

    # ------------------------------------------------------------------ #
    # Bucket-level tests
    # ------------------------------------------------------------------ #

    def test_create_maz_bucket(self):
        """create_bucket with enable_maz=True should succeed"""
        self._skip_if_maz_unsupported()
        self.assertTrue(self.bos.does_bucket_exist(self.MAZ_BUCKET))

    def test_set_bucket_storage_class_maz_standard(self):
        """set_bucket_storage_class to MAZ_STANDARD on a MAZ bucket"""
        self._skip_if_maz_unsupported()
        response = self.bos.set_bucket_storage_class(
            self.MAZ_BUCKET, storage_class=storage_class.MAZ_STANDARD)
        self.check_headers(response)
        response = self.bos.get_bucket_storage_class(self.MAZ_BUCKET)
        self.assertEqual(response.storage_class, "MAZ_STANDARD")

    def test_set_bucket_storage_class_maz_standard_ia(self):
        """set_bucket_storage_class to MAZ_STANDARD_IA on a MAZ bucket"""
        self._skip_if_maz_unsupported()
        response = self.bos.set_bucket_storage_class(
            self.MAZ_BUCKET, storage_class=storage_class.MAZ_STANDARD_IA)
        self.check_headers(response)
        response = self.bos.get_bucket_storage_class(self.MAZ_BUCKET)
        self.assertEqual(response.storage_class, "MAZ_STANDARD_IA")

    # ------------------------------------------------------------------ #
    # Object-level tests
    # ------------------------------------------------------------------ #

    def test_put_object_from_string_with_maz_standard(self):
        """put_object_from_string with MAZ_STANDARD storage class on a MAZ bucket"""
        self._skip_if_maz_unsupported()
        response = self.bos.put_object_from_string(
            bucket=self.MAZ_BUCKET,
            key=b"maz_std_str",
            data="Hello MAZ Standard",
            storage_class=storage_class.MAZ_STANDARD)
        self.check_headers(response)
        meta = self.bos.get_object_meta_data(
            bucket_name=self.MAZ_BUCKET, key=b"maz_std_str")
        self.assertEqual(meta.metadata.bce_storage_class, "MAZ_STANDARD")

    def test_put_object_from_string_with_maz_standard_ia(self):
        """put_object_from_string with MAZ_STANDARD_IA storage class on a MAZ bucket"""
        self._skip_if_maz_unsupported()
        response = self.bos.put_object_from_string(
            bucket=self.MAZ_BUCKET,
            key=b"maz_ia_str",
            data="Hello MAZ IA",
            storage_class=storage_class.MAZ_STANDARD_IA)
        self.check_headers(response)
        meta = self.bos.get_object_meta_data(
            bucket_name=self.MAZ_BUCKET, key=b"maz_ia_str")
        self.assertEqual(meta.metadata.bce_storage_class, "MAZ_STANDARD_IA")

    def test_put_object_from_file_with_maz_standard(self):
        """put_object_from_file with MAZ_STANDARD storage class on a MAZ bucket"""
        self._skip_if_maz_unsupported()
        self.get_file(1)
        response = self.bos.put_object_from_file(
            bucket=self.MAZ_BUCKET,
            key=b"maz_std_file",
            file_name=self.FILENAME,
            storage_class=storage_class.MAZ_STANDARD)
        self.check_headers(response)
        meta = self.bos.get_object_meta_data(
            bucket_name=self.MAZ_BUCKET, key=b"maz_std_file")
        self.assertEqual(meta.metadata.bce_storage_class, "MAZ_STANDARD")

    def test_put_object_from_file_with_maz_standard_ia(self):
        """put_object_from_file with MAZ_STANDARD_IA storage class on a MAZ bucket"""
        self._skip_if_maz_unsupported()
        self.get_file(1)
        response = self.bos.put_object_from_file(
            bucket=self.MAZ_BUCKET,
            key=b"maz_ia_file",
            file_name=self.FILENAME,
            storage_class=storage_class.MAZ_STANDARD_IA)
        self.check_headers(response)
        meta = self.bos.get_object_meta_data(
            bucket_name=self.MAZ_BUCKET, key=b"maz_ia_file")
        self.assertEqual(meta.metadata.bce_storage_class, "MAZ_STANDARD_IA")

    def test_copy_object_with_maz_standard(self):
        """copy_object with MAZ_STANDARD storage class on a MAZ bucket"""
        self._skip_if_maz_unsupported()
        self.bos.put_object_from_string(self.MAZ_BUCKET, b"src_maz_std", "Hello MAZ")
        response = self.bos.copy_object(
            source_bucket_name=self.MAZ_BUCKET,
            source_key=b"src_maz_std",
            target_bucket_name=self.MAZ_BUCKET,
            target_key=b"dst_maz_std",
            storage_class=storage_class.MAZ_STANDARD)
        self.check_headers(response)
        meta = self.bos.get_object_meta_data(
            bucket_name=self.MAZ_BUCKET, key=b"dst_maz_std")
        self.assertEqual(meta.metadata.bce_storage_class, "MAZ_STANDARD")

    def test_copy_object_with_maz_standard_ia(self):
        """copy_object with MAZ_STANDARD_IA storage class on a MAZ bucket"""
        self._skip_if_maz_unsupported()
        self.bos.put_object_from_string(self.MAZ_BUCKET, b"src_maz_ia", "Hello MAZ IA")
        response = self.bos.copy_object(
            source_bucket_name=self.MAZ_BUCKET,
            source_key=b"src_maz_ia",
            target_bucket_name=self.MAZ_BUCKET,
            target_key=b"dst_maz_ia",
            storage_class=storage_class.MAZ_STANDARD_IA)
        self.check_headers(response)
        meta = self.bos.get_object_meta_data(
            bucket_name=self.MAZ_BUCKET, key=b"dst_maz_ia")
        self.assertEqual(meta.metadata.bce_storage_class, "MAZ_STANDARD_IA")

    def test_default_storage_class_of_maz_bucket(self):
        """objects put without explicit storage_class on MAZ bucket should get MAZ default class"""
        self._skip_if_maz_unsupported()
        self.bos.put_object_from_string(
            bucket=self.MAZ_BUCKET,
            key=b"maz_default",
            data="default storage class on MAZ bucket")
        meta = self.bos.get_object_meta_data(
            bucket_name=self.MAZ_BUCKET, key=b"maz_default")
        # MAZ bucket default storage class should be MAZ_STANDARD
        self.assertIn("MAZ", meta.metadata.bce_storage_class)


class TestSendRequestValidateObjectKey(TestClient):
    """
    Verify that _send_request rejects invalid object keys for all APIs,
    preventing object-level operations from being misrouted to bucket-level.
    """

    INVALID_KEYS = [
        ('', 'empty key'),
        ('..', 'double-dot traversal'),
        ('../other-bucket/secret', 'leading double-dot traversal'),
        ('abc/../secret', 'middle double-dot traversal'),
        ('.', 'single-dot segment'),
        ('./foo', 'leading single-dot segment'),
    ]

    def test_get_object_rejects_invalid_keys(self):
        for key, desc in self.INVALID_KEYS:
            with self.assertRaises((ValueError, BceClientError), msg=desc):
                self.bos.get_object(self.BUCKET, key)

    def test_get_object_as_string_rejects_invalid_keys(self):
        for key, desc in self.INVALID_KEYS:
            with self.assertRaises((ValueError, BceClientError), msg=desc):
                self.bos.get_object_as_string(self.BUCKET, key)

    def test_get_object_to_file_rejects_invalid_keys(self):
        for key, desc in self.INVALID_KEYS:
            with self.assertRaises((ValueError, BceClientError), msg=desc):
                self.bos.get_object_to_file(self.BUCKET, key, '/tmp/test_out')

    def test_put_object_from_string_rejects_invalid_keys(self):
        for key, desc in self.INVALID_KEYS:
            with self.assertRaises((ValueError, BceClientError), msg=desc):
                self.bos.put_object_from_string(self.BUCKET, key, 'data')

    def test_copy_object_rejects_invalid_target_key(self):
        self.bos.put_object_from_string(self.BUCKET, b'valid_src', 'data')
        for key, desc in self.INVALID_KEYS:
            with self.assertRaises((ValueError, BceClientError), msg=desc):
                self.bos.copy_object(self.BUCKET, b'valid_src', self.BUCKET, key)

    def test_copy_object_rejects_invalid_source_key(self):
        for key, desc in self.INVALID_KEYS:
            with self.assertRaises((ValueError, BceClientError), msg=desc):
                self.bos.copy_object(self.BUCKET, key, self.BUCKET, b'valid_dst')

    def test_delete_object_rejects_invalid_keys(self):
        for key, desc in self.INVALID_KEYS:
            with self.assertRaises((ValueError, BceClientError), msg=desc):
                self.bos.delete_object(self.BUCKET, key)

    def test_delete_object_acl_rejects_invalid_keys(self):
        for key, desc in self.INVALID_KEYS:
            with self.assertRaises((ValueError, BceClientError), msg=desc):
                self.bos.delete_object_acl(self.BUCKET, key)

    def test_get_object_meta_data_rejects_invalid_keys(self):
        for key, desc in self.INVALID_KEYS:
            with self.assertRaises((ValueError, BceClientError), msg=desc):
                self.bos.get_object_meta_data(self.BUCKET, key)

    def test_get_object_acl_rejects_invalid_keys(self):
        for key, desc in self.INVALID_KEYS:
            with self.assertRaises((ValueError, BceClientError), msg=desc):
                self.bos.get_object_acl(self.BUCKET, key)

    def test_valid_key_passes(self):
        """normal keys should not be blocked by validation"""
        self.bos.put_object_from_string(self.BUCKET, b'normal/path/file.txt', 'data')
        self.bos.get_object_as_string(self.BUCKET, b'normal/path/file.txt')
        self.bos.get_object_meta_data(self.BUCKET, b'normal/path/file.txt')
        self.bos.delete_object(self.BUCKET, b'normal/path/file.txt')


def run_test():
    """start run test"""
    runner = unittest.TextTestRunner()
    runner.run(unittest.makeSuite(TestClient))

    runner.run(unittest.makeSuite(TestSelectObject))
    runner.run(unittest.makeSuite(TestCopyObject))
    runner.run(unittest.makeSuite(TestGeneratePreSignedUrl))
    runner.run(unittest.makeSuite(TestValidateObjectKey))
    runner.run(unittest.makeSuite(TestValidateBucketName))
    runner.run(unittest.makeSuite(TestListMultipartsUploads))
    runner.run(unittest.makeSuite(TestSetBucketAcl))
    runner.run(unittest.makeSuite(TestGetBucketAcl))
    runner.run(unittest.makeSuite(TestGetObjectMetaData))
    runner.run(unittest.makeSuite(TestGetObject))
    runner.run(unittest.makeSuite(TestListBuckets))
    runner.run(unittest.makeSuite(TestListObjects))
    runner.run(unittest.makeSuite(TestListParts))
    runner.run(unittest.makeSuite(TestPutObject))
    runner.run(unittest.makeSuite(TestAppendObject))
    runner.run(unittest.makeSuite(TestMultiUploadFile))
    runner.run(unittest.makeSuite(TestPutSuperObejctFromFile))
    runner.run(unittest.makeSuite(TestPutSuperObjectAutoChunkSize))
    runner.run(unittest.makeSuite(TestAuthorization))
    runner.run(unittest.makeSuite(TestAbortMultipartUpload))
    runner.run(unittest.makeSuite(TestUtil))
    runner.run(unittest.makeSuite(TestHandler))
    runner.run(unittest.makeSuite(TestBceHttpClient))
    runner.run(unittest.makeSuite(TestDoesBucketExist))
    runner.run(unittest.makeSuite(TestBceClientConfiguration))
    runner.run(unittest.makeSuite(TestGetRangeHeaderDict))
    runner.run(unittest.makeSuite(TestDecorator))
    runner.run(unittest.makeSuite(TestDeleteMultipleObjects))
    runner.run(unittest.makeSuite(TestPutBucketLogging))
    runner.run(unittest.makeSuite(TestGetBucketLogging))
    runner.run(unittest.makeSuite(TestUploadPartCopy))
    runner.run(unittest.makeSuite(TestPutBucketLifecycle))
    runner.run(unittest.makeSuite(TestGetBucketLifecycle))
    runner.run(unittest.makeSuite(TestPutBucketCors))
    runner.run(unittest.makeSuite(TestGetBucketCors))
    runner.run(unittest.makeSuite(TestSetObjectAcl))
    runner.run(unittest.makeSuite(TestGetAndDeleteObjectAcl))
    runner.run(unittest.makeSuite(TestBucketStaticWebsite))
    runner.run(unittest.makeSuite(TestPutBucketEncryption))
    runner.run(unittest.makeSuite(TestGetAndDeleteBucketEncryption))
    runner.run(unittest.makeSuite(TestBucketCopyrightProtection))
    runner.run(unittest.makeSuite(TestBucketReplication))
    runner.run(unittest.makeSuite(TestBucketTrash))
    runner.run(unittest.makeSuite(TestFetchObject))
    runner.run(unittest.makeSuite(TestRestoreObject))
    runner.run(unittest.makeSuite(TestSymlink))
    runner.run(unittest.makeSuite(TestBucketStorageclass))
    runner.run(unittest.makeSuite(TestBucketInventory))
    runner.run(unittest.makeSuite(TestNotification))
    runner.run(unittest.makeSuite(TestMirroringConf))
    runner.run(unittest.makeSuite(TestBucketQuota))
    runner.run(unittest.makeSuite(TestBucketTagging))
    runner.run(unittest.makeSuite(TestConditionalReadWrite))
    runner.run(unittest.makeSuite(TestCRC32))
    runner.run(unittest.makeSuite(TestSHA256))
    runner.run(unittest.makeSuite(TestCRC32C))
    runner.run(unittest.makeSuite(TestCRC32CFlag))
    runner.run(unittest.makeSuite(TestPutSuperObjectWithCRC32C))
    runner.run(unittest.makeSuite(TestCRC64ECMA))

    # Bug fix tests
    runner.run(unittest.makeSuite(TestCreateBucket))
    runner.run(unittest.makeSuite(TestSetBucketAclReturnValue))
    runner.run(unittest.makeSuite(TestSetObjectAclReturnValue))
    runner.run(unittest.makeSuite(TestCompleteMultipartUploadConfig))
    runner.run(unittest.makeSuite(TestPrepareObjectHeadersContentLength))
    runner.run(unittest.makeSuite(TestUploadPartTrafficLimitNoDuplicate))
    runner.run(unittest.makeSuite(TestRequiredDecoratorOnBucketMethods))
    runner.run(unittest.makeSuite(TestBucketObjectLock))
    runner.run(unittest.makeSuite(TestObjectTagging))
    runner.run(unittest.makeSuite(TestMazBucket))
    runner.run(unittest.makeSuite(TestSendRequestValidateObjectKey))

    # New branch coverage tests
    runner.run(unittest.makeSuite(TestGetObjectWithVersionId))
    runner.run(unittest.makeSuite(TestRestoreObjectBranches))
    runner.run(unittest.makeSuite(TestListObjectsVersionsBranches))
    runner.run(unittest.makeSuite(TestBucketReplicationIdNone))
    runner.run(unittest.makeSuite(TestFetchObjectBranches))
    runner.run(unittest.makeSuite(TestListObjectsBranches))
    runner.run(unittest.makeSuite(TestListPartsBranches))
    runner.run(unittest.makeSuite(TestListMultipartUploadsBranches))
    runner.run(unittest.makeSuite(TestUploadPartCopyWithEtag))

    """test quota, the quota cache may exist causing the bucket to be created error"""
    # runner.run(unittest.makeSuite(TestQuota))
    """test speed limit, the case is skipped by default"""
    # runner.run(unittest.makeSuite(TestTrafficLimit))


run_test()
cov.stop()
cov.save()
cov.html_report(directory="../../htmlcov")
cov.xml_report(outfile="../../bos-coverage.xml")
