# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
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

    # copy a object
    bos_client.copy_object(bucket_name, key, bucket_name, key + ".copy",)

    # list objects in a bucket(up to 1000)
    response = bos_client.list_objects(bucket_name)
    for obj in response.contents:
        __logger.debug("[Sample] list objects key:%s", obj.key)

    # delete an object
    bos_client.delete_object(bucket_name, key)

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

    # about multi-upload
    bos_client.abort_multipart_upload(bucket_name, key + "_about", upload_id_about)

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