# Copyright 2014 Baidu, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the
# License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.

"""
This module provides a client class for BOS.
"""

import io
import copy
import http.client
import os
import json
import logging
import shutil
from builtins import str
from builtins import bytes
from future.utils import iteritems, iterkeys, itervalues

import baidubce
from baidubce import bce_client_configuration
from baidubce import utils
from baidubce.auth import bce_v1_signer
from baidubce.bce_base_client import BceBaseClient
from baidubce.exception import BceClientError
from baidubce.exception import BceServerError
from baidubce.exception import BceHttpClientError
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce.http import http_content_types
from baidubce.http import http_headers
from baidubce.http import http_methods
from baidubce.services import bos
from baidubce.services.bos import bos_handler
from baidubce.services.bos import storage_class
from baidubce.utils import required
from baidubce import compat


_logger = logging.getLogger(__name__)

FETCH_MODE_SYNC = b"sync"
FETCH_MODE_ASYNC = b"async"

ENCRYPTION_ALGORITHM= "AES256"


class BosClient(BceBaseClient):
    """
    sdk client
    """
    def __init__(self, config=None):
        BceBaseClient.__init__(self, config)

    def list_buckets(self, config=None):
        """
        List buckets of user

        :param config: None
        :type config: BceClientConfiguration
        :returns: all buckets owned by the user.
        :rtype: baidubce.bce_response.BceResponse
        """
        return self._send_request(http_methods.GET, config=config)

    @required(bucket_name=(bytes, str))
    def get_bucket_location(self, bucket_name, config=None):
        """
        Get the region which the bucket located in.

        :param bucket_name: the name of bucket
        :type bucket_name: string or unicode
        :param config: None
        :type config: BceClientConfiguration

        :return: region of the bucket
        :rtype: str
        """
        params = {b'location': b''}
        response = self._send_request(http_methods.GET, bucket_name, params=params, config=config)
        return response.location_constraint

    @required(bucket_name=(bytes, str))
    def create_bucket(self, bucket_name, config=None):
        """
        Create bucket with specific name

        :param bucket_name: the name of bucket
        :type bucket_name: string or unicode
        :param config: None
        :type config: BceClientConfiguration
        :returns:
        :rtype: baidubce.bce_response.BceResponse
        """
        return self._send_request(http_methods.PUT, bucket_name, config=config)

    @required(bucket_name=(bytes, str))
    def does_bucket_exist(self, bucket_name, config=None):
        """
        Check whether there is a bucket with specific name

        :param bucket_name: None
        :type bucket_name: str
        :return:True or False
        :rtype: bool
        """
        try:
            self._send_request(http_methods.HEAD, bucket_name, config=config)
            return True
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                if e.last_error.status_code == http.client.FORBIDDEN:
                    return True
                if e.last_error.status_code == http.client.NOT_FOUND:
                    return False
            raise e

    @required(bucket_name=(bytes, str))
    def get_bucket_acl(self, bucket_name, config=None):
        """
        Get Access Control Level of bucket

        :type bucket: string
        :param bucket: None
        :return:
            **json text of acl**
        """
        return self._send_request(
                http_methods.GET,
                bucket_name,
                params={b'acl': b''},
                config=config)

    @staticmethod
    def _dump_acl_object(acl):
        result = {}
        for k, v in iteritems(acl.__dict__):
            if not k.startswith('_'):
                result[k] = v
        return result

    @required(bucket_name=(bytes, str), acl=(list, dict))
    def set_bucket_acl(self, bucket_name, acl, config=None):
        """
        Set Access Control Level of bucket

        :type bucket: string
        :param bucket: None

        :type grant_list: list of grant
        :param grant_list: None
        :return:
            **HttpResponse Class**
        """
        self._send_request(http_methods.PUT,
                           bucket_name,
                           body=json.dumps({'accessControlList': acl},
                                           default=BosClient._dump_acl_object),
                           headers={http_headers.CONTENT_TYPE: http_content_types.JSON},
                           params={b'acl': b''},
                           config=config)

    @required(bucket_name=(bytes, str), canned_acl=bytes)
    def set_bucket_canned_acl(self, bucket_name, canned_acl, config=None):
        """

        :param bucket_name:
        :param canned_acl:
        :param config:
        :return:
        """
        self._send_request(http_methods.PUT,
                           bucket_name,
                           headers={http_headers.BCE_ACL: canned_acl},
                           params={b'acl': b''},
                           config=config)

    @required(bucket_name=(bytes, str))
    def delete_bucket(self, bucket_name, config=None):
        """
        Delete a Bucket(Must Delete all the Object in Bucket before)

        :type bucket: string
        :param bucket: None
        :return:
            **HttpResponse Class**
        """
        return self._send_request(http_methods.DELETE, bucket_name, config=config)

# bucket static website
    @required(bucket_name=(bytes, str))
    def put_bucket_static_website(self, bucket_name, index=None, not_found=None, config=None):
        """
        Set index page and not_found 404 page for static website trusteeship

        :type bucket_name: string
        :param bucket_name: None

        :type index:string
        :param index:object name of index page for static website trusteeship

        :type not_found:string
        :param not_found:object name of not_found 404 page for static website trusteeship

        :return:
            **HttpResponse Class**
        """
        body = {}
        if index is not None:
            body['index'] = index
        if not_found is not None:
            body['notFound'] = not_found
        return self._send_request(http_methods.PUT,
                           bucket_name,
                           body=json.dumps(body,
                                           default=BosClient._dump_acl_object),
                           headers={http_headers.CONTENT_TYPE: http_content_types.JSON},
                           params={b'website': b''},
                           config=config)

    @required(bucket_name=(bytes, str))
    def get_bucket_static_website(self, bucket_name, config=None):
        """
        Get Information of static website trusteeship

        :type bucket: string
        :param bucket: None

        :return:
            **HttpResponse Class**
        """
        return self._send_request(http_methods.GET,
                           bucket_name,
                           params={b'website': b''},
                           config=config)


    @required(bucket_name=(bytes, str))
    def delete_bucket_static_website(self, bucket_name, config=None):
        """
        Delete Information of static website trusteeship to be closed

        :type bucket: string
        :param bucket: None

        :return:
            **HttpResponse Class**
        """
        return self._send_request(http_methods.DELETE,
                           bucket_name,
                           params={b'website': b''},
                           config=config)

# bucket encryption
    @required(bucket_name=(bytes, str))
    def put_bucket_encryption(self, bucket_name, encryption_algorithm=ENCRYPTION_ALGORITHM, config=None):
        """
        Set server encryption for bucket

        :type bucket: string
        :param bucket: None

        :type encryption_algorithm: string
        :param grant_list: server encryption algorithm for bucekt.Now the value of encryption_algorithm
        only is 'AES256'

        :return:
            **HttpResponse Class**
        """
        encryption_algorithm = compat.convert_to_string(encryption_algorithm)
        return self._send_request(http_methods.PUT,
                           bucket_name,
                           body=json.dumps({"encryptionAlgorithm":encryption_algorithm},
                                           default=BosClient._dump_acl_object),
                           headers={http_headers.CONTENT_TYPE: http_content_types.JSON},
                           params={b'encryption': b''},
                           config=config)

    @required(bucket_name=(bytes, str))
    def get_bucket_encryption(self, bucket_name, config=None):
        """
        Get status of server encryption

        :type bucket: string
        :param bucket: None

        :return:
            **HttpResponse Class**
        """
        return self._send_request(http_methods.GET,
                           bucket_name,
                           params={b'encryption': b''},
                           config=config)


    @required(bucket_name=(bytes, str))
    def delete_bucket_encryption(self, bucket_name, config=None):
        """
        Close server encryption

        :type bucket: string
        :param bucket: None

        :return:
            **HttpResponse Class**
        """
        return self._send_request(http_methods.DELETE,
                           bucket_name,
                           params={b'encryption': b''},
                           config=config)

# Bucket Copyright Protection

    @required(bucket_name=(bytes, str), resource=(list))
    def put_bucket_copyright_protection(self, bucket_name, resource, config=None):
        """
        Open image copyright protection and set resource

        :type bucket: string
        :param bucket: None

        :type resource: list of  string
        :param grant_list: resource range to be protected

        :return:
            **HttpResponse Class**
        """
        return self._send_request(http_methods.PUT,
                           bucket_name,
                           body=json.dumps({"resource": resource},
                                           default=BosClient._dump_acl_object),
                           headers={http_headers.CONTENT_TYPE: http_content_types.JSON},
                           params={b'copyrightProtection': b''},
                           config=config)

    @required(bucket_name=(bytes, str))
    def get_bucket_copyright_protection(self, bucket_name, config=None):
        """
        Get configuration of image copyright protection

        :type bucket: string
        :param grant_list: None

        :return:
            **HttpResponse Class**
        """
        return self._send_request(http_methods.GET,
                           bucket_name,
                           params={b'copyrightProtection': b''},
                           config=config)


    @required(bucket_name=(bytes, str))
    def delete_bucket_copyright_protection(self, bucket_name, config=None):
        """
        Close image copyright protection

        :type bucket: string
        :param bucket: None

        :return:
            **HttpResponse Class**
        """
        return self._send_request(http_methods.DELETE,
                           bucket_name,
                           params={b'copyrightProtection': b''},
                           config=config)

# bucket replication
    @required(bucket_name=(bytes, str), replication=(dict))
    def put_bucket_replication(self, bucket_name, replication, config=None):
        """
        Open cross-region replication

        :type bucket: string
        :param bucket: None

        :type replication: dict
        :type replication: configuration for cross-region replication

        :return:
            **HttpResponse Class**
        """
        return self._send_request(http_methods.PUT,
                           bucket_name,
                           body=json.dumps(replication,
                                           default=BosClient._dump_acl_object),
                           headers={http_headers.CONTENT_TYPE: http_content_types.JSON},
                           params={b'replication': b''},
                           config=config)

    @required(bucket_name=(bytes, str))
    def get_bucket_replication(self, bucket_name, config=None):
        """
        Get configuration of cross-region replication 

        :type bucket: string
        :param bucket: None

        :return:
            **HttpResponse Class**
        """
        return self._send_request(http_methods.GET,
                           bucket_name,
                           params={b'replication': b''},
                           config=config)


    @required(bucket_name=(bytes, str))
    def delete_bucket_replication(self, bucket_name, config=None):
        """
        Delete configuration of cross-region replication and close it 

        :type bucket: string
        :param bucket: None

        :return:
            **HttpResponse Class**
        """
        return self._send_request(http_methods.DELETE,
                           bucket_name,
                           params={b'replication': b''},
                           config=config)


    @required(bucket_name=(bytes, str))
    def get_bucket_replication_progress(self, bucket_name, config=None):
        """
        Get status of cross-region replication,for exapmle 'historyReplicationPercent',
        'latestReplicationTime'

        :type bucket: string
        :param bucket: None

        :return:
            **HttpResponse Class**
        """
        return self._send_request(http_methods.GET,
                           bucket_name,
                           params={b'replicationProgress': b''},
                           config=config)


    @required(bucket_name=(bytes, str))
    def put_bucket_trash(self, bucket_name, trash_dir=None, config=None):
        """
        Open bucket trash function

        :type bucket: string
        :param bucket: None

        :type trash_dir: string
        :param trash_dir: directory of trash,optional

        :return:
            **HttpResponse Class**
        """
        if trash_dir is not None:
            trash_dir = compat.convert_to_string(trash_dir)
        return self._send_request(http_methods.PUT,
                           bucket_name,
                           body=json.dumps({"trashDir": trash_dir},
                                           default=BosClient._dump_acl_object),
                           headers={http_headers.CONTENT_TYPE: http_content_types.JSON},
                           params={b'trash': b''},
                           config=config)

    @required(bucket_name=(bytes, str))
    def get_bucket_trash(self, bucket_name, config=None):
        """
        Get status of bucket trash

        :type bucket: string
        :param grant_list: None

        :return:
            **HttpResponse Class**
        """
        return self._send_request(http_methods.GET,
                           bucket_name,
                           params={b'trash': b''},
                           config=config)


    @required(bucket_name=(bytes, str))
    def delete_bucket_trash(self, bucket_name, config=None):
        """
        Close bucket trash

        :type bucket: string
        :param bucket: None

        :return:
            **HttpResponse Class**
        """
        return self._send_request(http_methods.DELETE,
                           bucket_name,
                           params={b'trash': b''},
                           config=config)

    @required(bucket_name=(bytes, str), key=(bytes, str))
    def generate_pre_signed_url(self,
                                bucket_name,
                                key,
                                timestamp=0,
                                expiration_in_seconds=1800,
                                headers=None,
                                params=None,
                                headers_to_sign=None,
                                protocol=None,
                                config=None):
        """
        Get an authorization url with expire time

        :type timestamp: int
        :param timestamp: None

        :type expiration_in_seconds: int
        :param expiration_in_seconds: None

        :type options: dict
        :param options: None

        :return:
            **URL string**
        """
        key = compat.convert_to_bytes(key)
        config = self._merge_config(config)
        headers = headers or {}
        params = params or {}
        # specified protocol > protocol in endpoint > default protocol
        endpoint_protocol, endpoint_host, endpoint_port = \
            utils.parse_host_port(config.endpoint, config.protocol)
        protocol = protocol or endpoint_protocol

        full_host = endpoint_host
        if endpoint_port != config.protocol.default_port:
            full_host += b':' + compat.convert_to_bytes(endpoint_port)
        headers[http_headers.HOST] = full_host

        path = self._get_path(config, bucket_name, key)

        params[http_headers.AUTHORIZATION.lower()] = bce_v1_signer.sign(
            config.credentials,
            http_methods.GET,
            path,
            headers,
            params,
            timestamp,
            expiration_in_seconds,
            headers_to_sign)
        return b"%s://%s%s?%s" % (compat.convert_to_bytes(protocol.name),
                                 full_host,
                                 path,
                                 utils.get_canonical_querystring(params, False))

    @required(bucket_name=(bytes, str), rules=(list, dict))
    def put_bucket_lifecycle(self, 
                             bucket_name,
                             rules,
                             config=None):
        """
        Put Bucket Lifecycle
       
        :type bucket: string
        :param bucket: None

        :type rules: list
        :param rules: None

        :return:**Http Response**
        """
        return self._send_request(http_methods.PUT, 
                                  bucket_name,
                                  params={b'lifecycle': b''},
                                  body=json.dumps({'rule': rules}),
                                  config=config)

    @required(bucket_name=(bytes, str))
    def get_bucket_lifecycle(self, bucket_name, config=None):
        """
        Get Bucket Lifecycle

        :type bucket: string
        :param bucket: None

        :return:**Http Response**
        """
        return self._send_request(http_methods.GET, 
                                  bucket_name, 
                                  params={b'lifecycle': b''},
                                  config=config) 

    @required(bucket_name=(bytes, str))
    def delete_bucket_lifecycle(self, bucket_name, config=None):
        """
        Delete Bucket Lifecycle
        
        :type bucket: string
        :param bucket: None

        :return:**Http Response**
        """
        return self._send_request(http_methods.DELETE,
                                  bucket_name,
                                  params={b'lifecycle': b''},
                                  config=config)       
    
    @required(bucket_name=(bytes, str), cors_configuration=list)
    def put_bucket_cors(self, 
                        bucket_name,
                        cors_configuration,
                        config=None):
        """
        Put Bucket Cors
        :type bucket: string
        :param bucket: None

        :type cors_configuration: list
        :param cors_configuration: None

        :return:**Http Response**
        """
        return self._send_request(http_methods.PUT,
                                  bucket_name,
                                  params={b'cors': b''},
                                  body=json.dumps({'corsConfiguration': cors_configuration}),
                                  config=config)

    @required(bucket_name=(bytes, str))
    def get_bucket_cors(self, bucket_name, config=None):
        """
        Get Bucket Cors

        :type bucket: string
        :param bucket: None

        :return:**Http Response**
        """
        return self._send_request(http_methods.GET,
                                  bucket_name,
                                  params={b'cors': b''},
                                  config=config)

    @required(bucket_name=(bytes, str))
    def delete_bucket_cors(self, bucket_name, config=None):
        """
        Delete Bucket Cors

        :type bucket: string
        :param bucket: None

        :return:**Http Response**
        """
        return self._send_request(http_methods.DELETE,
                                  bucket_name,
                                  params={b'cors': b''},
                                  config=config)

    @required(bucket_name=(bytes, str))        
    def list_objects(self, bucket_name,
                     max_keys=1000, prefix=None, marker=None, delimiter=None,
                     config=None):
        """
        Get Object Information of bucket

        :type bucket: string
        :param bucket: None

        :type delimiter: string
        :param delimiter: None

        :type marker: string
        :param marker: None

        :type max_keys: int
        :param max_keys: value <= 1000

        :type prefix: string
        :param prefix: None

        :return:
            **_ListObjectsResponse Class**
        """
        params = {}
        if max_keys is not None:
            params[b'maxKeys'] = max_keys
        if prefix is not None:
            params[b'prefix'] = prefix
        if marker is not None:
            params[b'marker'] = marker
        if delimiter is not None:
            params[b'delimiter'] = delimiter

        return self._send_request(http_methods.GET, bucket_name, params=params, config=config)

    @required(bucket_name=(bytes, str))
    def list_all_objects(self, bucket_name, prefix=None, delimiter=None, config=None):
        """

        :param bucket_name:
        :param prefix:
        :param delimiter:
        :param config:
        :return:
        """
        marker = None
        while True:
            response = self.list_objects(
                bucket_name, marker=marker, prefix=prefix, delimiter=delimiter, config=config)
            for item in response.contents:
                yield item
            if response.is_truncated:
                marker = response.next_marker
            else:
                break

    @staticmethod
    def _get_range_header_dict(range):
        if range is None:
            return None
        if not isinstance(range, (list, tuple)):
            raise TypeError('range should be a list or a tuple')
        if len(range) != 2:
            raise ValueError('range should have length of 2')
        return {http_headers.RANGE: b'bytes=%d-%d' % tuple(range)}


    @staticmethod
    def _parse_bos_object(http_response, response):
        """Sets response.body to http_response and response.user_metadata to a dict consists of all http
        headers starts with 'x-bce-meta-'.

        :param http_response: the http_response object returned by HTTPConnection.getresponse()
        :type http_response: httplib.HTTPResponse

        :param response: general response object which will be returned to the caller
        :type response: baidubce.BceResponse

        :return: always true
        :rtype bool
        """
        user_metadata = {}
        headers_list = http_response.getheaders()
        if compat.PY3:
            temp_heads = []
            for k,v in headers_list:
                k = k.lower()
                temp_heads.append((k, v))
            headers_list = temp_heads

        prefix = compat.convert_to_string(
                http_headers.BCE_USER_METADATA_PREFIX
        )
        for k, v in headers_list:
            if k.startswith(prefix):
                k = k[len(prefix):]
                user_metadata[compat.convert_to_unicode(k)] = \
                    compat.convert_to_unicode(v)
        response.metadata.user_metadata = user_metadata
        response.data = http_response
        return True

    @required(bucket_name=(bytes, str), key=(bytes, str))
    def get_object(self, bucket_name, key, range=None, config=None):
        """

        :param bucket_name:
        :param key:
        :param range:
        :param config:
        :return:
        """
        key = compat.convert_to_bytes(key)
        return self._send_request(
            http_methods.GET,
            bucket_name,
            key,
            headers=BosClient._get_range_header_dict(range),
            config=config,
            body_parser=BosClient._parse_bos_object)

    @staticmethod
    def _save_body_to_file(http_response, response, file_name, buf_size):
        f = open(file_name, 'wb')
        try:
            shutil.copyfileobj(http_response, f, buf_size)
            http_response.close()
        finally:
            f.close()
        return True

    @required(bucket_name=(bytes, str), key=(bytes, str))
    def get_object_as_string(self, bucket_name, key, range=None, config=None):
        """

        :param bucket_name:
        :param key:
        :param range:
        :param config:
        :return:
        """
        key = compat.convert_to_bytes(key)
        response = self.get_object(bucket_name, key, range=range, config=config)
        s = response.data.read()
        response.data.close()
        return s

    @required(bucket_name=(bytes, str), key=(bytes, str), file_name=(bytes, str))
    def get_object_to_file(self, bucket_name, key, file_name, range=None, config=None):
        """
        Get Content of Object and Put Content to File

        :type bucket: string
        :param bucket: None

        :type key: string
        :param key: None

        :type file_name: string
        :param file_name: None

        :type range: tuple
        :param range: (0,9) represent get object contents of 0-9 in bytes. 10 bytes date in total.
        :return:
            **HTTP Response**
        """
        key = compat.convert_to_bytes(key)
        file_name = compat.convert_to_bytes(file_name)
        return self._send_request(
            http_methods.GET,
            bucket_name,
            key,
            headers=BosClient._get_range_header_dict(range),
            config=config,
            body_parser=lambda http_response, response: BosClient._save_body_to_file(
                http_response,
                response,
                file_name,
                self._get_config_parameter(config, 'recv_buf_size')))

    @required(bucket_name=(bytes, str), key=(bytes, str))
    def get_object_meta_data(self, bucket_name, key, config=None):
        """
        Get head of object

        :type bucket: string
        :param bucket: None

        :type key: string
        :param key: None
        :return:
            **_GetObjectMetaDataResponse Class**
        """
        key = compat.convert_to_bytes(key)
        return self._send_request(http_methods.HEAD, bucket_name, key, config=config)

    @required(bucket_name=(bytes, str),
              key=(bytes, str),
              data=object,
              content_length=compat.integer_types,
              content_md5=(bytes, str))
    def append_object(self, bucket_name, key, data,
                     content_md5,
                     content_length,
                     offset=None,
                     content_type=None,
                     user_metadata=None,
                     content_sha256=None,
                     storage_class=None,
                     user_headers=None,
                     config=None):
        """
        Put an appendable object to BOS or add content to an appendable object

        :type bucket: string
        :param bucket: None

        :type key: string
        :param key: None

        :type content_length: long
        :type offset: long
        :return:
            **HTTP Response**
        """
        key = compat.convert_to_bytes(key)
        content_md5 = compat.convert_to_bytes(content_md5)
        headers = self._prepare_object_headers(
            content_length=content_length,
            content_md5=content_md5,
            content_type=content_type,
            content_sha256=content_sha256,
            user_metadata=user_metadata,
            storage_class=storage_class,
            user_headers=user_headers)

        if content_length > bos.MAX_APPEND_OBJECT_LENGTH:
            raise ValueError('Object length should be less than %d. '
                             'Use multi-part upload instead.' % bos.MAX_APPEND_OBJECT_LENGTH)

        params = {b'append': b''}
        if offset is not None:
            params[b'offset'] = offset

        return self._send_request(
            http_methods.POST,
            bucket_name,
            key,
            body=data,
            headers=headers,
            params=params,
            config=config)

    @required(bucket_name=(bytes, str),
                           key=(bytes, str),
                           data=(bytes, str))
    def append_object_from_string(self, bucket_name, key, data,
                                  content_md5=None,
                                  offset=None,
                                  content_type=None,
                                  user_metadata=None,
                                  content_sha256=None,
                                  storage_class=None,
                                  user_headers=None,
                                  config=None):
        """
        Create an appendable object and put content of string to the object
        or add content of string to an appendable object
        """
        key = compat.convert_to_bytes(key)
        if isinstance(data, str):
            data = data.encode(baidubce.DEFAULT_ENCODING)

        fp = None
        try:
            fp = io.BytesIO(data)
            if content_md5 is None:
                content_md5 = utils.get_md5_from_fp(
                    fp, buf_size=self._get_config_parameter(config, 'recv_buf_size'))

            return self.append_object(bucket_name=bucket_name,
                                      key=key,
                                      data=fp,
                                      content_md5=content_md5,
                                      content_length=len(data),
                                      offset=offset,
                                      content_type=content_type,
                                      user_metadata=user_metadata,
                                      content_sha256=content_sha256,
                                      storage_class=storage_class,
                                      user_headers=user_headers,
                                      config=config)
        finally:
            if fp is not None:
                fp.close()

    @required(bucket_name=(bytes, str),
              key=(bytes, str),
              data=object,
              content_length=compat.integer_types,
              content_md5=(bytes, str))
    def put_object(self, bucket_name, key, data,
                   content_length,
                   content_md5,
                   content_type=None,
                   content_sha256=None,
                   user_metadata=None,
                   storage_class=None,
                   user_headers=None,
                   config=None):
        """
        Put object and put content of file to the object

        :type bucket: string
        :param bucket: None

        :type key: string
        :param key: None

        :type fp: FILE
        :param fp: None

        :type file_size: long
        :type offset: long
        :type content_length: long
        :return:
            **HTTP Response**
        """
        key = compat.convert_to_bytes(key)
        content_md5 = compat.convert_to_bytes(content_md5)
        headers = self._prepare_object_headers(
            content_length=content_length,
            content_md5=content_md5,
            content_type=content_type,
            content_sha256=content_sha256,
            user_metadata=user_metadata,
            storage_class=storage_class,
            user_headers=user_headers)

        buf_size = self._get_config_parameter(config, 'recv_buf_size')

        if content_length > bos.MAX_PUT_OBJECT_LENGTH:
            raise ValueError('Object length should be less than %d. '
                             'Use multi-part upload instead.' % bos.MAX_PUT_OBJECT_LENGTH)

        return self._send_request(
            http_methods.PUT,
            bucket_name,
            key,
            body=data,
            headers=headers,
            config=config)

    @required(bucket=(bytes, str), key=(bytes, str), data=(bytes, str))
    def put_object_from_string(self, bucket, key, data,
                               content_md5=None,
                               content_type=None,
                               content_sha256=None,
                               user_metadata=None,
                               storage_class=None,
                               user_headers=None,
                               config=None):
        """
        Create object and put content of string to the object

        :type bucket: string
        :param bucket: None

        :type key: string
        :param key: None

        :type input_content: string
        :param input_content: None

        :type options: dict
        :param options: None
        :return:
            **HTTP Response**
        """
        key = compat.convert_to_bytes(key)
        if isinstance(data, str):
            data = data.encode(baidubce.DEFAULT_ENCODING)

        fp = None
        try:
            fp = io.BytesIO(data)
            if content_md5 is None:
                content_md5 = utils.get_md5_from_fp(
                    fp, buf_size=self._get_config_parameter(config, 'recv_buf_size'))
            return self.put_object(bucket, key, fp,
                                   content_length=len(data),
                                   content_md5=content_md5,
                                   content_type=content_type,
                                   content_sha256=content_sha256,
                                   user_metadata=user_metadata,
                                   storage_class=storage_class,
                                   user_headers=user_headers,
                                   config=config)
        finally:
            if fp is not None:
                fp.close()

    @required(bucket=(bytes, str), key=(bytes, str), file_name=(bytes, str))
    def put_object_from_file(self, bucket, key, file_name,
                             content_length=None,
                             content_md5=None,
                             content_type=None,
                             content_sha256=None,
                             user_metadata=None,
                             storage_class=None,
                             user_headers=None,
                             config=None):

        """
        Put object and put content of file to the object

        :type bucket: string
        :param bucket: None

        :type key: string
        :param key: None

        :type file_name: string
        :param file_name: None

        :type options: dict
        :param options: None
        :return:
            **HttpResponse Class**
        """
        key = compat.convert_to_bytes(key)
        fp = open(file_name, 'rb')
        try:
            if content_length is None:
                fp.seek(0, os.SEEK_END)
                content_length = fp.tell()
                fp.seek(0)
            if content_md5 is None:
                recv_buf_size = self._get_config_parameter(config, 'recv_buf_size')
                content_md5 = utils.get_md5_from_fp(fp, length=content_length,
                                                    buf_size=recv_buf_size)
            if content_type is None:
                content_type = utils.guess_content_type_by_file_name(file_name)
            return self.put_object(bucket, key, fp,
                                   content_length=content_length,
                                   content_md5=content_md5,
                                   content_type=content_type,
                                   content_sha256=content_sha256,
                                   user_metadata=user_metadata,
                                   storage_class=storage_class,
                                   user_headers=user_headers,
                                   config=config)
        finally:
            fp.close()

    @required(source_bucket_name=(bytes, str),
              source_key=(bytes, str),
              target_bucket_name=(bytes, str),
              target_key=(bytes, str))
    def copy_object(self,
                    source_bucket_name, source_key,
                    target_bucket_name, target_key,
                    etag=None,
                    content_type=None,
                    user_metadata=None,
                    storage_class=None,
                    user_headers=None,
                    copy_object_user_headers=None,
                    config=None):
        """
        Copy one object to another object

        :type source_bucket: string
        :param source_bucket: None

        :type source_key: string
        :param source_key: None

        :type target_bucket: string
        :param target_bucket: None

        :type target_key: string
        :param target_key: None
        :return:
            **HttpResponse Class**
        """
        source_key = compat.convert_to_bytes(source_key)
        target_key = compat.convert_to_bytes(target_key)
        headers = self._prepare_object_headers(
            content_type=content_type,
            user_metadata=user_metadata,
            storage_class=storage_class,
            user_headers=user_headers)
        headers[http_headers.BCE_COPY_SOURCE] = utils.normalize_string(
            b'/%s/%s' % (
                compat.convert_to_bytes(source_bucket_name), 
                source_key), False)
        if etag is not None:
            headers[http_headers.BCE_COPY_SOURCE_IF_MATCH] = etag
        if user_metadata is not None or content_type is not None:
            headers[http_headers.BCE_COPY_METADATA_DIRECTIVE] = b'replace'
        else:
            headers[http_headers.BCE_COPY_METADATA_DIRECTIVE] = b'copy'

        if copy_object_user_headers is not None:
            try:
                headers = BosClient._get_user_header(headers, copy_object_user_headers, True)
            except Exception as e:
                raise e

        return self._send_request(
            http_methods.PUT,
            target_bucket_name,
            target_key,
            headers=headers,
            config=config,
            body_parser=bos_handler.parse_copy_object_response)

    @required(bucket_name=(bytes, str), key=(bytes, str))
    def delete_object(self, bucket_name, key, config=None):
        """
        Delete Object

        :type bucket: string
        :param bucket: None

        :type key: string
        :param key: None
        :return:
            **HttpResponse Class**
        """
        key = compat.convert_to_bytes(key)
        return self._send_request(http_methods.DELETE, bucket_name, key, config=config)

    @required(bucket_name=(bytes, str), key_list=list)
    def delete_multiple_objects(self, bucket_name, key_list, config=None):
        """
        Delete Multiple Objects

        :type bucket: string
        :param bucket: None

        :type key_list: string list
        :param key_list: None
        :return:
            **HttpResponse Class**
        """
        key_list_json = [{'key': compat.convert_to_string(k)} for k in key_list]
        return self._send_request(http_methods.POST, 
                                  bucket_name, 
                                  body=json.dumps({'objects': key_list_json}),
                                  params={b'delete': b''},
                                  config=config)

    @required(source_bucket=(bytes, str),
              target_bucket=(bytes, str),
              target_prefix=(bytes, str))
    def put_bucket_logging(self,
                          source_bucket,
                          target_bucket,
                          target_prefix=None,
                          config=None):
        """
        Put Bucket Logging

        :type source_bucket: string
        :param source_bucket: None

        :type target_bucket: string
        :param target_bucket: None
        :return:
            **HttpResponse Class**
        """
        return self._send_request(http_methods.PUT, 
                                  source_bucket, 
                                  params={b'logging': b''}, 
                                  body=json.dumps({'targetBucket': target_bucket, 
                                                  'targetPrefix': target_prefix}),
                                  config=config)

    @required(bucket_name=(bytes, str))
    def get_bucket_logging(self, bucket_name, config=None):
        """
        Get Bucket Logging

        :type bucket_name: string
        :param bucket_name: None
        :return:
            **HttpResponse Class**
        """
        return self._send_request(http_methods.GET,
                                  bucket_name,
                                  params={b'logging': b''},
                                  config=config)

    @required(bucket_name=(bytes, str))
    def delete_bucket_logging(self, bucket_name, config=None):
        """
        Delete Bucket Logging

        :type bucket_name: string
        :param bucket_name: None
        :return:
            **HttpResponse Class**
        """
        return self._send_request(http_methods.DELETE,
                                  bucket_name,
                                  params={b'logging': b''},
                                  config=config)

    @required(bucket_name=(bytes, str), key=(bytes, str))
    def initiate_multipart_upload(self,
                                  bucket_name,
                                  key,
                                  content_type=None,
                                  storage_class=None,
                                  user_headers=None,
                                  config=None):
        """
        Initialize multi_upload_file.

        :type bucket: string
        :param bucket: None

        :type key: string
        :param key: None
        :return:
            **HttpResponse**
        """
        key = compat.convert_to_bytes(key)
        headers = {}
        if storage_class is not None:
            headers[http_headers.BOS_STORAGE_CLASS] = storage_class

        if content_type is not None:
            headers[http_headers.CONTENT_TYPE] = utils.convert_to_standard_string(content_type)
        else:
            headers[http_headers.CONTENT_TYPE] = http_content_types.OCTET_STREAM

        if user_headers is not None:
            try:
                headers = BosClient._get_user_header(headers, user_headers, False)
            except Exception as e:
                raise e

        return self._send_request(
            http_methods.POST,
            bucket_name,
            key,
            headers=headers,
            params={b'uploads': b''},
            config=config)

    @required(bucket_name=(bytes, str),
              key=(bytes, str),
              upload_id=(bytes, str),
              part_number=int,
              part_size=compat.integer_types,
              part_fp=object)
    def upload_part(self, bucket_name, key, upload_id,
                    part_number, part_size, part_fp, part_md5=None,
                    config=None):
        """
        Upload a part.

        :type bucket: string
        :param bucket: None

        :type key: string
        :param key: None

        :type upload_id: string
        :param upload_id: None

        :type part_number: int
        :param part_number: None

        :type part_size: int or long
        :param part_size: None

        :type part_fp: file pointer
        :param part_fp: not None

        :type part_md5: str
        :param part_md5: None

        :type config: dict
        :param config: None

        :return:
               **HttpResponse**
        """
        key = compat.convert_to_bytes(key)
        if part_number < bos.MIN_PART_NUMBER or part_number > bos.MAX_PART_NUMBER:
            raise ValueError('Invalid part_number %d. The valid range is from %d to %d.' % (
                part_number, bos.MIN_PART_NUMBER, bos.MAX_PART_NUMBER))

        if part_size > bos.MAX_PUT_OBJECT_LENGTH:
            raise ValueError('Single part length should be less than %d. '
                             % bos.MAX_PUT_OBJECT_LENGTH)

        headers = {http_headers.CONTENT_LENGTH: part_size,
                   http_headers.CONTENT_TYPE: http_content_types.OCTET_STREAM}
        if part_md5 is not None:
            headers[http_headers.CONTENT_MD5] = part_md5

        return self._send_request(
            http_methods.PUT,
            bucket_name,
            key,
            body=part_fp,
            headers=headers,
            params={b'partNumber': part_number, b'uploadId': upload_id},
            config=config)

    @required(source_bucket_name=(bytes, str),
              source_key=(bytes, str),
              target_bucket_name=(bytes, str),
              target_key=(bytes, str),
              upload_id=(bytes, str),
              part_number=int,
              part_size=compat.integer_types,
              offset=compat.integer_types)
    def upload_part_copy(self, 
                         source_bucket_name, source_key, 
                         target_bucket_name, target_key,
                         upload_id, part_number, part_size, offset,
                         etag=None,
                         content_type=None,
                         user_metadata=None,
                         config=None):
        """
        Copy part.

        :type source_bucket_name: string
        :param source_bucket_name: None

        :type source_key: string
        :param source_key: None

        :type target_bucket_name: string
        :param target_bucket_name: None

        :type target_key: string
        :param target_key: None

        :type upload_id: string
        :param upload_id: None

        :return:
            **HttpResponse**
        """
        source_key = compat.convert_to_bytes(source_key)
        target_key = compat.convert_to_bytes(target_key)
        headers = self._prepare_object_headers(
                         content_type=content_type,
                         user_metadata=user_metadata)
        headers[http_headers.BCE_COPY_SOURCE] = utils.normalize_string(
                         b"/%s/%s" % (compat.convert_to_bytes(source_bucket_name),
                         source_key), False)
        range = b"""bytes=%d-%d""" % (offset, offset + part_size - 1)
        headers[http_headers.BCE_COPY_SOURCE_RANGE] = range
        if etag is not None:
            headers[http_headers.BCE_COPY_SOURCE_IF_MATCH] = etag

        return self._send_request(
            http_methods.PUT,
            target_bucket_name,
            target_key,
            headers=headers,
            params={b'partNumber': part_number, b'uploadId': upload_id},
            config=config)

    @required(bucket_name=(bytes, str),
              key=(bytes, str),
              upload_id=(bytes, str),
              part_number=int,
              part_size=compat.integer_types,
              file_name=(bytes, str),
              offset=compat.integer_types)
    def upload_part_from_file(self, bucket_name, key, upload_id,
                              part_number, part_size, file_name, offset, part_md5=None,
                              config=None):
        """

        :param bucket_name:
        :param key:
        :param upload_id:
        :param part_number:
        :param part_size:
        :param file_name:
        :param offset:
        :param part_md5:
        :param config:
        :return:
        """
        key = compat.convert_to_bytes(key)
        f = open(file_name, 'rb')
        try:
            f.seek(offset)
            return self.upload_part(bucket_name, key, upload_id, part_number, part_size, f,
                                    part_md5=part_md5, config=config)
        finally:
            f.close()

    @required(bucket_name=(bytes, str),
              key=(bytes, str),
              upload_id=(bytes, str),
              part_list=list)
    def complete_multipart_upload(self, bucket_name, key,
                                  upload_id, part_list,
                                  user_metadata=None,
                                  config=None):
        """
        After finish all the task, complete multi_upload_file.

        :type bucket: string
        :param bucket: None

        :type key: string
        :param key: None

        :type upload_id: string
        :param upload_id: None

        :type part_list: list
        :param part_list: None

        :return:
            **HttpResponse**
        """
        key = compat.convert_to_bytes(key)
        headers = self._prepare_object_headers(
            content_type=http_content_types.JSON,
            user_metadata=user_metadata)

        return self._send_request(
            http_methods.POST,
            bucket_name,
            key,
            body=json.dumps({'parts': part_list}),
            headers=headers,
            params={b'uploadId': upload_id})

    @required(bucket_name=(bytes, str), key=(bytes, str), upload_id=(bytes, str))
    def abort_multipart_upload(self, bucket_name, key, upload_id, config=None):
        """
        Abort upload a part which is being uploading.

        :type bucket: string
        :param bucket: None

        :type key: string
        :param key: None

        :type upload_id: string
        :param upload_id: None
        :return:
            **HttpResponse**
        """
        key = compat.convert_to_bytes(key)
        return self._send_request(http_methods.DELETE, bucket_name, key,
                                  params={b'uploadId': upload_id})

    @required(bucket_name=(bytes, str), key=(bytes, str), upload_id=(bytes, str))
    def list_parts(self, bucket_name, key, upload_id,
                   max_parts=None, part_number_marker=None,
                   config=None):
        """
        List all the parts that have been upload success.

        :type bucket: string
        :param bucket: None

        :type key: string
        :param key: None

        :type upload_id: string
        :param upload_id: None

        :type max_parts: int
        :param max_parts: None

        :type part_number_marker: string
        :param part_number_marker: None
        :return:
            **_ListPartsResponse Class**
        """
        key = compat.convert_to_bytes(key)
        params = {b'uploadId': upload_id}
        if max_parts is not None:
            params[b'maxParts'] = max_parts
        if part_number_marker is not None:
            params[b'partNumberMarker'] = part_number_marker

        return self._send_request(http_methods.GET, bucket_name, key, params=params, config=config)

    @required(bucket_name=(bytes, str), key=(bytes, str), upload_id=(bytes, str))
    def list_all_parts(self, bucket_name, key, upload_id, config=None):
        """

        :param bucket_name:
        :param key:
        :param upload_id:
        :param config:
        :return:
        """
        key = compat.convert_to_bytes(key)
        part_number_marker = None
        while True:
            response = self.list_parts(bucket_name, key, upload_id,
                                      part_number_marker=part_number_marker, config=config)
            for item in response.parts:
                yield item
            if not response.is_truncated:
                break
            part_number_marker = response.next_part_number_marker

    @required(bucket_name=(bytes, str))
    def list_multipart_uploads(self, bucket_name, max_uploads=None, key_marker=None,
                               prefix=None, delimiter=None,
                               config=None):
        """
        List all Multipart upload task which haven't been ended.(Completed Init_MultiPartUpload
        but not completed Complete_MultiPartUpload or Abort_MultiPartUpload)

        :type bucket: string
        :param bucket: None

        :type delimiter: string
        :param delimiter: None

        :type max_uploads: int
        :param max_uploads: <=1000

        :type key_marker: string
        :param key_marker: None

        :type prefix: string
        :param prefix: None

        :type upload_id_marker: string
        :param upload_id_marker:
        :return:
            **_ListMultipartUploadResponse Class**
        """
        params = {b'uploads': b''}
        if delimiter is not None:
            params[b'delimiter'] = delimiter
        if max_uploads is not None:
            params[b'maxUploads'] = max_uploads
        if key_marker is not None:
            params[b'keyMarker'] = key_marker
        if prefix is not None:
            params[b'prefix'] = prefix

        return self._send_request(http_methods.GET, bucket_name, params=params, config=config)

    @required(bucket_name=(bytes, str))
    def list_all_multipart_uploads(self, bucket_name, prefix=None, delimiter=None, config=None):
        """

        :param bucket_name:
        :param prefix:
        :param delimiter:
        :param config:
        :return:
        """
        key_marker = None
        while True:
            response = self.list_multipart_uploads(bucket_name,
                                                   key_marker=key_marker,
                                                   prefix=prefix,
                                                   delimiter=delimiter,
                                                   config=config)
            for item in response.uploads:
                yield item
            if not response.is_truncated:
                break
            if response.next_key_marker is not None:
                key_marker = response.next_key_marker
            elif len(response.uploads) != 0:
                key_marker = response.uploads[-1].key
            else:
                break

    @required(bucket_name=(bytes, str), key=(bytes, str), acl=(list, dict))
    def set_object_acl(self, bucket_name, key, acl, config=None):
        """
        Set Access Control Level of object

        :type bucket: string
        :param bucket: None

        :type acl: list of grant
        :param acl: None
        :return:
            **HttpResponse Class**
        """
        key = compat.convert_to_bytes(key)
        self._send_request(http_methods.PUT,
                           bucket_name,
                           key,
                           body=json.dumps({'accessControlList': acl},
                                           default=BosClient._dump_acl_object),
                           headers={http_headers.CONTENT_TYPE: http_content_types.JSON},
                           params={b'acl': b''},
                           config=config)

    @required(bucket_name=(bytes, str), key=(bytes, str))
    def set_object_canned_acl(self, bucket_name, key,
            canned_acl=None,
            grant_read=None,
            grant_full_control=None,
            config=None):
        """

        :type bucket_name: string
        :param bucket_name: None

        :type key: string
        :param key: None

        :type canned_acl: string
        :param canned_acl: for header 'x-bce-acl', it's value only is
        canned_acl.PRIVATE or canned_acl.PRIVATE_READ

        :type grant_read: string
        :param grant_read: Object id of getting READ right permission.
        for exapmle,grant_read = 'id="6c47...4c94",id="8c42...4c94"'

        :type grant_full_control: string
        :param grant_full_control: Object id of getting READ right permission.
        for exapmle,grant_full_control = 'id="6c47...4c94",id="8c42...4c94"'

        :param config:
        :return:
            **HttpResponse Class**
        """
        key = compat.convert_to_bytes(key)
        headers = None
        num_args = 0
        if canned_acl is not None:
            headers =  {http_headers.BCE_ACL: compat.convert_to_bytes(canned_acl)}
            num_args += 1
        if grant_read is not None:
            headers = {http_headers.BOS_GRANT_READ: compat.convert_to_bytes(grant_read)}
            num_args += 1
        if grant_full_control is not None:
            headers = {http_headers.BOS_GRANT_FULL_CONTROL: compat.convert_to_bytes(grant_full_control)}
            num_args += 1

        if num_args == 0:
            raise ValueError("donn't give any object canned acl arguments!")
        elif num_args >= 2:
            raise ValueError("cann't get more than one object canned acl arguments!")

        self._send_request(http_methods.PUT,
                           bucket_name,
                           key,
                           headers=headers,
                           params={b'acl': b''},
                           config=config)

    @required(bucket_name=(bytes, str), key=(bytes, str))
    def get_object_acl(self, bucket_name, key, config=None):
        """
        Get Access Control Level of object

        :type bucket: string
        :param bucket: None

        :type key: string
        :param key: None

        :return:
            **HttpResponse Class**
        """
        key = compat.convert_to_bytes(key)
        return self._send_request(
                http_methods.GET,
                bucket_name,
                key,
                params={b'acl': b''},
                config=config)

    @required(bucket_name=(bytes, str), key=(bytes, str))
    def delete_object_acl(self, bucket_name, key, config=None):
        """
        Get Access Control Level of  object

        :type bucket: string
        :param bucket: None

        :type key: string
        :param key: None

        :return:
            **HttpResponse Class**
        """
        key = compat.convert_to_bytes(key)
        return self._send_request(
                http_methods.DELETE,
                bucket_name,
                key,
                params={b'acl': b''},
                config=config)

    @required(bucket_name=(bytes, str), key=(bytes, str), url=(bytes, str))
    def fetch_object(self, bucket_name, key, url,
            fetch_mode=None,
            storage_class=None,
            config=None):
        """
        fetch object with given url and save to Baidu object storage

        :type bucket: string
        :param bucket: None

        :type key: string
        :param key: object name to be saved

        :type url:string
        :param url: url of resource to be fetched

        :type fetch_mode:string
        :param fetch_mode: fetch mode for get resource, valid value only is
        'sync' and 'async'

        :return:
            **HttpResponse Class**
        """
        key = compat.convert_to_bytes(key)
        headers = {}
        headers[http_headers.BOS_FETCH_SOURCE] = compat.convert_to_bytes(url)
        if fetch_mode is not None:
            headers[http_headers.BOS_FETCH_MODE] = fetch_mode
        if storage_class is not None:
            headers[http_headers.BOS_STORAGE_CLASS] = storage_class
        return self._send_request(
                http_methods.POST,
                bucket_name,
                key,
                headers=headers,
                params={b'fetch': b''},
                config=config)

    @staticmethod
    def _prepare_object_headers(
            content_length=None,
            content_md5=None,
            content_type=None,
            content_sha256=None,
            etag=None,
            user_metadata=None,
            storage_class=None,
            user_headers=None):
        headers = {}

        if content_length is not None:
            if content_length and content_length < 0:
                raise ValueError('content_length should not be negative.')
            headers[http_headers.CONTENT_LENGTH] = compat.convert_to_bytes(content_length)

        if content_md5 is not None:
            headers[http_headers.CONTENT_MD5] = utils.convert_to_standard_string(content_md5)

        if content_type is not None:
            headers[http_headers.CONTENT_TYPE] = utils.convert_to_standard_string(content_type)
        else:
            headers[http_headers.CONTENT_TYPE] = http_content_types.OCTET_STREAM

        if content_sha256 is not None:
            headers[http_headers.BCE_CONTENT_SHA256] = content_sha256

        if etag is not None:
            headers[http_headers.ETAG] = b'"%s"' % utils.convert_to_standard_string(etag)

        if user_metadata is not None:
            meta_size = 0
            if not isinstance(user_metadata, dict):
                raise TypeError('user_metadata should be of type dict.')
            for k, v in iteritems(user_metadata):
                k = utils.convert_to_standard_string(k)
                v = utils.convert_to_standard_string(v)
                normalized_key = http_headers.BCE_USER_METADATA_PREFIX + k
                headers[normalized_key] = v
                meta_size += len(normalized_key)
                meta_size += len(v)
            if meta_size > bos.MAX_USER_METADATA_SIZE:
                raise ValueError(
                    'Metadata size should not be greater than %d.' % bos.MAX_USER_METADATA_SIZE)

        if storage_class is not None:
            headers[http_headers.BOS_STORAGE_CLASS] = storage_class

        if user_headers is not None:
            try:
                headers = BosClient._get_user_header(headers, user_headers, False)
            except Exception as e:
                raise e

        return headers


    @staticmethod
    def _get_user_header(headers, user_headers, is_copy=False):
        if not isinstance(user_headers, dict):
            raise TypeError('user_headers should be of type dict.')

        if not is_copy:
            user_headers_set = set([http_headers.CACHE_CONTROL,
                                    http_headers.CONTENT_ENCODING,
                                    http_headers.CONTENT_DISPOSITION,
                                    http_headers.EXPIRES])
        else:
            user_headers_set = set([http_headers.BCE_COPY_SOURCE_IF_NONE_MATCH,
                                    http_headers.BCE_COPY_SOURCE_IF_UNMODIFIED_SINCE,
                                    http_headers.BCE_COPY_SOURCE_IF_MODIFIED_SINCE])

        for k, v in iteritems(user_headers):
            k = utils.convert_to_standard_string(k)
            v = utils.convert_to_standard_string(v)
            if k in user_headers_set:
                headers[k] = v
        return headers

    def _get_config_parameter(self, config, attr):
        result = None
        if config is not None:
            result = getattr(config, attr)
        if result is not None:
            return result
        return getattr(self.config, attr)


    @staticmethod
    def _get_path(config, bucket_name=None, key=None):
        return utils.append_uri(bos.URL_PREFIX, bucket_name, key)

    def _merge_config(self, config):
        if config is None:
            return self.config
        else:
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    def _send_request(
            self, http_method, bucket_name=None, key=None,
            body=None, headers=None, params=None,
            config=None,
            body_parser=None):
        config = self._merge_config(config)
        path = BosClient._get_path(config, bucket_name, key)
        if body_parser is None:
            body_parser = handler.parse_json

        if config.security_token is not None:
            headers = headers or {}
            headers[http_headers.STS_SECURITY_TOKEN] = config.security_token

        return bce_http_client.send_request(
            config, bce_v1_signer.sign, [handler.parse_error, body_parser],
            http_method, path, body, headers, params)
