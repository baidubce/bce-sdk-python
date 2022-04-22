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
from __future__ import print_function
import os
import random
import string
import time
import base64
import multiprocessing
import threading
import sys

import bos_sample_conf
import bos_sts_sample_conf
from baidubce import exception
from baidubce import compat
from baidubce.services.bos import canned_acl
from baidubce.services.bos import storage_class
from baidubce.services.bos.bos_client import BosClient
from baidubce.services.bos.bos_client import UploadTaskHandle
from baidubce import utils


def _create_file(file_name, size):
    """Create a file with the file size is size"""
    file = open(file_name, "w")
    file.seek(size)
    file.write('\x00')
    file.close()


def _random_string(length):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

def percentage(consumed_bytes, total_bytes):
    """Progress bar callback function that calculates the percentage of current completion
    
    :param consumed_bytes: Amount of data that has been uploaded/downloaded
    :param total_bytes: total file bytes
    """

    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        start_progress = '*' * rate
        end_progress = '.' * (100 - rate)
        if rate == 100:
            print("\r{}%[{}->{}]\n".format(rate, start_progress, end_progress), end="")
        else:
            print("\r{}%[{}->{}]".format(rate, start_progress, end_progress), end="")
        
        sys.stdout.flush()


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

    # create a bos client
    bos_client = BosClient(bos_sample_conf.config)

    ######################################################################################################
    #            bucket operation samples
    ######################################################################################################

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

    # put an archive object and restore object with days=2
    bos_client.put_object_from_file(bucket_name, key, file_name, storage_class=storage_class.ARCHIVE)
    bos_client.restore_object(bucket_name, key, days=2)

    # get obj url by ak/sk
    url = bos_client.generate_pre_signed_url(bucket_name, key, timestamp=1649923427,
                                               expiration_in_seconds=100000000)
    __logger.debug("[Sample] get object url is  %s", url)

    # get obj url by sts
    # create a sts bos client
    sts_bos_client = BosClient(bos_sts_sample_conf.config)
    url = sts_bos_client.generate_pre_signed_url(bucket_name, key, timestamp=1649923427,
                                               expiration_in_seconds=100000000)
    __logger.debug("[Sample] sts get object url is  %s", url)

    ######################################################################################################
    #            symlink operation samples
    ######################################################################################################
    symlink_key = "mysymlink"
    # put symlink
    bos_client.put_object_symlink(bucket_name, key, symlink_key, storage_class=storage_class.STANDARD)
    # get symlink
    respones = bos_client.get_object_symlink(bucket_name, symlink_key)
    print(response.metadata.bce_symlink_target)
    # get object meta with symlink
    respones = bos_client.get_object_meta_data(bucket_name, symlink_key)
    print(response.metadata.bce_object_type)
    # get object with symlnk
    bos_client.get_object_to_file(bucket_name, symlink_key, download)

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
        [{'grantee': [{'id': 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'},
                      {'id': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'}],
          'permission': ['FULL_CONTROL']}])

    # get bucket acl and see if it affects
    response = bos_client.get_bucket_acl(bucket_name)
    __logger.debug("[Sample] get bucket acl owner id:%s", response.owner_id)
    __logger.debug("[Sample] get bucket acl:%s", response.access_control_list)

    ######################################################################################################
    #            bucket inventory operation samples
    ######################################################################################################

    dst_bucket_name = "samplebucket-inventory-target"
    if not bos_client.does_bucket_exist(dst_bucket_name):
        bos_client.create_bucket(dst_bucket_name)

    inventory_id = "testInventory001"
    my_inventory = {
        "id": inventory_id,
        "status": "enabled",
        "resource": [bucket_name + "/*"],
        "schedule": "Weekly",
        "destination":{
            "targetBucket": "samplebucket-inventory-target",
            "targetPrefix": "destination-prefix/",
            "format": "CSV"
            }
    }
    # put bucket inventory
    bos_client.put_bucket_inventory(bucket_name, my_inventory)

    # get bucket inventory
    response = bos_client.get_bucket_inventory(bucket_name, inventory_id)
    __logger.debug("[Sample] get bucket inventory resource:%s", response.resource)
    __logger.debug("[Sample] get bucket inventory destination:%s", response.destination.target_bucket)

    # list inventory
    response = bos_client.list_bucket_inventory(bucket_name)
    __logger.debug("[Sample] list bucket inventory :%s", response.inventory_rule_list)

    # delete bucket inventory
    response = bos_client.response = bos_client.delete_bucket_inventory(bucket_name, inventory_id)

    ######################################################################################################
    #            put_super_obejct_from_file operation samples
    ######################################################################################################

    # put a super file to object
    _create_file(file_name, 10 * 1024 * 1024)
    result = bos_client.put_super_obejct_from_file(bucket_name, key, file_name,
            chunk_size=5, thread_num=multiprocessing.cpu_count())
    if result:
        print("Upload success!")

    # cancel after calling put_super_obejct_from_file
    uploadTaskHandle = UploadTaskHandle()
    t = threading.Thread(target=bos_client.put_super_obejct_from_file, args=(bucket_name, key, file_name),
            kwargs={
                "chunk_size": 5,
                "thread_num": multiprocessing.cpu_count(),
                "uploadTaskHandle": uploadTaskHandle
                })
    t.start()
    time.sleep(2)
    uploadTaskHandle.cancel()
    t.join()

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
    bos_client.delete_bucket_logging(bucket_name)

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
    ######################################################################################################
    #            select object samples with csv
    ######################################################################################################
    csv_content = """
        1,Maurits,2017-09-1216:32:57,685856330,-540265154.48,true
        2,Iago,2018-02-01 12:25:01,-642946677,3781354659.89,false
        3,Dionisio,2018-02-16 09:52:24,-3823711977,79336720.77,false
        4,Aleen,2018-05-17 11:48:45,-3289131518,1499686289.41,false
        5,Herschel,2019-06-04 02:28:37,3456163349,-3810272511.88,true
        """
    bos_client.put_object_from_string(bucket_name, key, csv_content)
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
    sql_exp = "SELECT _1, _2, _6 FROM BosObject"
    select_object_args["expression"] = \
        compat.convert_to_string(base64.standard_b64encode(compat.convert_to_bytes(sql_exp)))
    select_response = bos_client.select_object(bucket_name, key, select_object_args)
    result = select_response.result()
    for msg in result:
        if msg.headers["message-type"] == "Records":
            print("type: {}, heades: {}, payload: {}, crc: {}".format(msg.type, msg.headers, msg.payload, msg.crc))
        elif msg.headers["message-type"] == "Cont":
            print("type: {}, heades: {}, bytes_scanned: {}, bytes_returned: {},  crc: {}".format(msg.type, msg.headers,
                msg.bytes_scanned, msg.bytes_returned, msg.crc))
        else:
            print("type: {}, heades: {}, crc: {}".format(msg.type, msg.headers, msg.crc))

    ######################################################################################################
    #            select object samples with json
    ######################################################################################################
    json_content = """
    {
    "name": "Smith",
    "age": 16,
    "weight": 65.5,
    "org": null,
    "projects":
        [
         {"project_name":"project1", "completed":false},
         {"project_name":"project2", "completed":true}
        ]
    }
    """
    bos_client.put_object_from_string(bucket_name, key, json_content)
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
    sql_exp = "select projects from BosObject where name='Smith'"
    select_object_args["expression"] = \
        compat.convert_to_string(base64.standard_b64encode(compat.convert_to_bytes(sql_exp)))
    select_response = bos_client.select_object(bucket_name, key, select_object_args)
    result = select_response.result()
    for msg in result:
        if msg.headers["message-type"] == "Records":
            print("type: {}, heades: {}, payload: {}, crc: {}".format(msg.type, msg.headers, msg.payload, msg.crc))
        elif msg.headers["message-type"] == "Cont":
            print("type: {}, heades: {}, bytes_scanned: {}, bytes_returned: {},  crc: {}".format(msg.type, msg.headers,
                msg.bytes_scanned, msg.bytes_returned, msg.crc))
        else:
            print("type: {}, heades: {}, crc: {}".format(msg.type, msg.headers, msg.crc))

    ######################################################################################################
    #            quata operation samples
    ######################################################################################################
    
    # get user quota
    try:
        response = bos_client.get_user_quota()
    except Exception as e: 
        __logger.debug("[Sample] get user quota error :%s", e)

    __logger.debug("[Sample] get user quota maxBucketCount:%s", response.max_bucket_count)
    __logger.debug("[Sample] get user quota maxCapacityMegaBytes:%s", response.max_capacity_mega_bytes)
    
    # delete user quota
    response = bos_client.delete_user_quota()
    __logger.debug("[Sample] delete user quota The response is %s", response)
    
    # put user quota
    response = bos_client.put_user_quota(50,12334424)
    __logger.debug("[Sample] put user quota The response is %s", response)

    ######################################################################################################
    #            notification operation samples
    ######################################################################################################
    # put notification
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
    response = bos_client.put_notification(bucket_name, notifications)
    __logger.debug("[Sample] put notification response :%s", response)

    # get notification
    try:
        response = bos_client.get_notification(bucket_name)
        __logger.debug("[Sample] get notification response :%s", response)
    except Exception as e:
        __logger.debug("[Sample] get notification error :%s", e)

    # delete notification
    try:
        response = bos_client.delete_notification(bucket_name)
        __logger.debug("[Sample] delete notification response :%s", response)
    except Exception as e:
        __logger.debug("[Sample] delete notification error :%s", e)

    #####################################################################################################
    #            test progress_callback samples
    ######################################################################################################

    # put a file as object
    _create_file(file_name, 4096)
    bos_client.put_object_from_file(bucket_name, key, file_name, progress_callback=utils.default_progress_callback)

    # get object into file
    bos_client.get_object_to_file(bucket_name, key, download, progress_callback=utils.default_progress_callback)
    __logger.debug("[Sample] get object into file, file size:%s", os.path.getsize(download))

    # put an appendable object
    append_key = 'test_append_key'
    result = bos_client.append_object_from_string(bucket_name=bucket_name,
                                                  key=append_key,
                                                  data='This is string content.', progress_callback=utils.default_progress_callback)
    next_offset = result.metadata.bce_next_append_offset
    
    bos_client.append_object_from_string(bucket_name=bucket_name,
                                         key=append_key,
                                         data='append content.',
                                         offset=int(next_offset), progress_callback=utils.default_progress_callback)
    response = bos_client.get_object_as_string(bucket_name=bucket_name, key=append_key)
    __logger.debug("[Sample] append object value:%s", response)

    bos_client.delete_object(bucket_name, append_key)


    # put_super_obejct_from_file operation samples
    # put a super file to object
    _create_file(file_name, 10 * 1024 * 1024)
    result = bos_client.put_super_obejct_from_file(bucket_name, key, file_name,
            chunk_size=5, thread_num=multiprocessing.cpu_count(), progress_callback=utils.default_progress_callback)
    if result:
        print("Upload success!")

    # cancel after calling put_super_obejct_from_file
    uploadTaskHandle = UploadTaskHandle()
    t = threading.Thread(target=bos_client.put_super_obejct_from_file, args=(bucket_name, key, file_name),
            kwargs={
                "chunk_size": 5,
                "thread_num": multiprocessing.cpu_count(),
                "uploadTaskHandle": uploadTaskHandle,
                "progress_callback": utils.default_progress_callback
                })
    t.start()
    time.sleep(2)
    uploadTaskHandle.cancel()
    t.join()


    # multi-upload operation samples
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
            bucket_name, key, upload_id, part_number, part_size, file_name, offset, progress_callback=utils.default_progress_callback)
        left_size -= part_size
        offset += part_size
        # your should store every part number and etag to invoke complete multi-upload
        part_list.append({
            "partNumber": part_number,
            "eTag": response.metadata.etag
        })
        part_number += 1