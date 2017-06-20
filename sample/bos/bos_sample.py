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
Samples for bos client.
"""

import os
import random
import string

import bos_sample_conf
from baidubce import exception
from baidubce.services.bos import canned_acl
from baidubce.services.bos.bos_client import BosClient


def _create_file(file_name, size):
    """Create a file with the file size is size"""
    file = open(file_name, "w")
    file.seek(size)
    file.write('\x00')
    file.close()


def _random_string(length):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    __logger = logging.getLogger(__name__)

    source_bucket = 'sourcebucket'
    target_bucket = 'targetbucket'
    source_key = 'sourcekey' + _random_string(6)
    target_key = 'targetkey' + _random_string(6)
    prefix = 'prefix' + _random_string(6)
    bucket_name = 'samplebucket'
    key = 'samplekey' + _random_string(6)
    file_name = 'samplefile'
    download = 'download'

    ######################################################################################################
    #            bucket operation samples
    ######################################################################################################

    # create a bos client
    bos_client = BosClient(bos_sample_conf.config)

    # check if bucket exists
    if not bos_client.does_bucket_exist(bucket_name):
        bos_client.create_bucket(bucket_name)

    # delete a bucket(you can't  delete a bucket which is not empty)
    # clear it first
    for obj in bos_client.list_all_objects(bucket_name):
        bos_client.delete_object(bucket_name, obj.key)
    bos_client.delete_bucket(bucket_name)

    # create the bucket again
    bos_client.create_bucket(bucket_name)

    # list your buckets
    response = bos_client.list_buckets()
    for bucket in response.buckets:
        __logger.debug("[Sample] list buckets:%s", bucket.name)

    ######################################################################################################
    #            object operation samples
    ######################################################################################################

    # put a string as object
    bos_client.put_object_from_string(bucket_name, key, "This is string content.")

    # get a object as string
    content = bos_client.get_object_as_string(bucket_name, key)
    __logger.debug("[Sample] get object as string:%s", content)

    # put a file as object
    _create_file(file_name, 4096)
    bos_client.put_object_from_file(bucket_name, key, file_name)

    # get object into file
    bos_client.get_object_to_file(bucket_name, key, download)
    __logger.debug("[Sample] get object into file, file size:%s", os.path.getsize(download))

    # put an appendable object
    append_key = 'test_append_key'
    result = bos_client.append_object_from_string(bucket_name=bucket_name,
                                                  key=append_key,
                                                  data='This is string content.')
    next_offset = result.metadata.bce_next_append_offset
    
    bos_client.append_object_from_string(bucket_name=bucket_name,
                                         key=append_key,
                                         data='append content.',
                                         offset=int(next_offset))
    response = bos_client.get_object_as_string(bucket_name=bucket_name, key=append_key)
    __logger.debug("[Sample] append object value:%s", response)

    bos_client.delete_object(bucket_name, append_key)

    # copy a object
    bos_client.copy_object(bucket_name, key, bucket_name, key + ".copy",)

    # list objects in a bucket(up to 1000)
    response = bos_client.list_objects(bucket_name)
    for obj in response.contents:
        __logger.debug("[Sample] list objects key:%s", obj.key)

    # delete an object
    bos_client.delete_object(bucket_name, key)

    # delete multiple objects
    key_list = ['key1', 'key2', 'key3']
    bos_client.delete_multiple_object(bucket_name, key_list)

    ######################################################################################################
    #            acl operation samples
    ######################################################################################################

    # set bucket canned acl to "private"
    bos_client.set_bucket_canned_acl(bucket_name, canned_acl.PRIVATE)

    # get bucket acl
    response = bos_client.get_bucket_acl(bucket_name)
    __logger.debug("[Sample] get bucket acl owner id:%s", response.owner_id)
    __logger.debug("[Sample] get bucket acl:%s", response.access_control_list)

    # set bucket acl from BucketAccessControl list
    bos_client.set_bucket_acl(
        bucket_name,
        [{'grantee': [{'id': 'b124deeaf6f641c9ac27700b41a350a8'},
                      {'id': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'}],
          'permission': ['FULL_CONTROL']}])

    # get bucket acl and see if it affects
    response = bos_client.get_bucket_acl(bucket_name)
    __logger.debug("[Sample] get bucket acl owner id:%s", response.owner_id)
    __logger.debug("[Sample] get bucket acl:%s", response.access_control_list)

    ######################################################################################################
    #            multi-upload operation samples
    ######################################################################################################

    # put a super file to object
    _create_file(file_name, 10 * 1024 * 1024)

    # SuperFile step 1: init multi-upload
    upload_id = bos_client.initiate_multipart_upload(bucket_name, key).upload_id
    upload_id_about = bos_client.initiate_multipart_upload(bucket_name, key + "_about").upload_id

    # SuperFile step 2: upload file part by part
    left_size = os.path.getsize(file_name)
    offset = 0
    part_number = 1
    part_list = []
    while left_size > 0:
        part_size = 5 * 1024 * 1024
        if left_size < part_size:
            part_size = left_size

        response = bos_client.upload_part_from_file(
            bucket_name, key, upload_id, part_number, part_size, file_name, offset)
        left_size -= part_size
        offset += part_size
        # your should store every part number and etag to invoke complete multi-upload
        part_list.append({
            "partNumber": part_number,
            "eTag": response.metadata.etag
        })
        part_number += 1

    # copy a object part by part

    # step 1: init multi-upload
    upload_id = bos_client.initiate_multipart_upload(target_bucket, target_key).upload_id
    upload_id_about = bos_client.initiate_multipart_upload(target_bucket, 
                                                           target_key + "_about").upload_id
    
    # step 2: upload copy part by part
    left_size = int(bos_client.get_object_meta_data(source_bucket, 
                                                    source_key).metadata.content_length)
    offset = 0
    part_number = 1
    part_list = []
    while left_size > 0:
        part_size = 5 * 1024 * 1024
        if left_size < part_size: 
            part_size = left_size
        response = bos_client.upload_part_copy(source_bucket, 
                                               source_key, 
                                               target_bucket, 
                                               target_key, 
                                               upload_id, 
                                               part_number, 
                                               part_size, 
                                               offset)
        left_size -= part_size
        offset += part_size
        part_list.append({"partNumber": part_number,
                          "eTag": response.etag})
        part_number += 1

    # step 3: update meta_data
    metadata = {'meta_key': 'meta_value'}
    bos_client.copy_object(source_bucket_name = source_bucket,
                           source_key = source_key,
                           target_bucket_name = target_bucket,
                           target_key = target_key,
                           user_metadata = metadata)
    # list multi-uploads
    response = bos_client.list_multipart_uploads(bucket_name)
    for upload in response.uploads:
        __logger.debug("[Sample] list multi-uploads, upload_id:%s", upload.upload_id)

    # list parts
    response = bos_client.list_parts(bucket_name, key, upload_id)
    for part in response.parts:
        __logger.debug("[Sample] list parts, etag:%s", upload.etag)

    # SuperFile step 3: complete multi-upload
    bos_client.complete_multipart_upload(bucket_name, key, upload_id, part_list)

    # abort multi-upload
    bos_client.abort_multipart_upload(bucket_name, key + "_about", upload_id_about)

    ######################################################################################################
    #            logging operation samples
    ######################################################################################################
    
    # put bucket logging
    bos_client.put_bucket_logging(source_bucket, target_bucket, prefix)

    # get bucket logging
    response = bos_client.get_bucket_logging(bucket_name)
    
    # delete bucket loggint
    bos_client.delet_bucket_loggint(bucket_name)

    ######################################################################################################
    #            lifecycle operation samples
    ######################################################################################################

    # put bucket lifecycle
    rule = {}
    rule['id'] = 'rule1'
    rule['status'] = 'enabled'
    rule['action'] = {}
    rule['action']['name'] = 'Transition' 
    rule['action']['storageClass'] = 'STANDARD_IA'
    rule['resource'] = [bucket_name + prefix]
    rule['condition'] = {}
    rule['condition']['time'] = {"dateGreaterThan": '2017-03-28T00:00:00Z'}
    rules=[]
    rules.append(rule)
    bos_client.put_bucket_lifecycle(bucket_name, rules)

    # get bucket lifecycle
    response = bos_client.get_bucket_lifecycle(bucket_name)

    # delete bucket lifecycle
    response = bos_client.delete_bucket_lifecycle(bucket_name)

    ######################################################################################################
    #            cors operation samples
    ######################################################################################################
    
    #put bucket cors
    conf={}
    conf['allowedOrigins'] = ['http://www.boluor.com']
    conf['allowedMethods'] = ['GET', 'HEAD', 'DELETE']
    conf['allowedHeaders'] = ['Authorization', 'x-bce-test', 'x-bce-test2']
    conf['allowedExposeHeaders'] = ['user-custom-expose-header']
    conf['maxAgeSeconds'] = 3600

    cors_confs=[]
    cors_confs.append(conf)

    bos_client.put_bucket_cors(bucket_name, cors_confs)

    #get bucket cors
    response = bos_client.get_bucket_cors(bucket_name)

    #delete bucket cors
    response = bos_client.delete_bucket_cors(bucket_name)

    ######################################################################################################
    #            failure samples
    ######################################################################################################

    # if you do something wrong, you will get a BceError
    try:
        bos_client.list_objects("notexist")
    except exception.BceError as e:
        __logger.debug("[Sample] failure:%s", e.message)
        if isinstance(e, exception.BceHttpClientError):
             # get last error of retry
            error = e.last_error