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
Samples for bcc client.
"""

# !/usr/bin/env python
# coding=utf-8

import bcc_sample_conf
from baidubce.exception import BceHttpClientError
from baidubce.exception import BceServerError
from baidubce.services.bcc import bcc_model
from baidubce.services.bcc import fpga_card_type
from baidubce.services.bcc import gpu_card_type
from baidubce.services.bcc.bcc_client import BccClient
from baidubce.services.bcc.bcc_model import PayTimingChangeReqModel

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    __logger = logging.getLogger(__name__)

    instance_id = 'i-lxhfzmm5'
    volume_id = 'volume_id'
    image_id = 'm-lxhfzmm5'
    admin_pass = '!QAZ2wsx'
    new_cpu_count = 1
    new_memory_in_gb = 1
    network_capacity_in_mbps = 1
    new_name = 'test-bcc-name'
    delicade_id = 'd-MPgs6jPr'
    internalIp = 'internalIp'
    zone_name = 'cn-bj-a'
    security_group_id = 'security_group_id'
    cds_size_in_gb = 5
    snapshot_id = 's-xaffgsdd'
    volume_id_markar = 'volume_id_markar'
    image_name = 'image_name'
    image_type = 'image_type'
    image_id_marker = 'image_id_marker'
    snapshot_description = 'snapshot_description'
    snapshot_name = 'snapshot_name'
    snapshot_id_marker = 'snapshot_id_marker'
    vpc_id = 'vpc_id'
    vpc_id_marker = 'vpc_id_marker'
    security_group_name = 'security_group_name'
    security_group_description = 'security_group_description'
    sourceGroupId = "sourceGroupId"
    sourceIp = "sourceIp"
    destGroupId = "destGroupId"
    destIp = "destIp"
    test_tag1 = bcc_model.TagModel(tagKey='TestKey02', tagValue='TestValue02')
    test_tag2 = bcc_model.TagModel(tagKey='TestKey03', tagValue='TestValue03')
    test_tags = [test_tag1, test_tag2]
    test_create_cds_model = bcc_model.CreateCdsModel(cdsSizeInGB=100, storageType='ssd', snapshotId='sid_test')
    test_create_cds_model2 = bcc_model.CreateCdsModel(cdsSizeInGB=200, storageType='ssd', snapshotId='sid_test2')
    test_create_cds_model_list = [test_create_cds_model, test_create_cds_model2]
    test_e_disk = bcc_model.EphemeralDisk(10, 'sata')
    test_e_disk2 = bcc_model.EphemeralDisk(20, 'sata2')
    test_e_disk_list = [test_e_disk, test_e_disk2]
    test_cds = bcc_model.CreateCdsModel(cdsSizeInGB=100, storageType='ssd', snapshotId='sid1')
    test_cds2 = bcc_model.CreateCdsModel(cdsSizeInGB=200, storageType='ssd2', snapshotId='sid2')
    test_cds_list = [test_cds, test_cds2]

    ######################################################################################################
    #            bcc operation samples
    ######################################################################################################

    # create a bcc client
    bcc_client = BccClient(bcc_sample_conf.config)

    # create a bcc only
    try:
        response = bcc_client.create_instance(cpu_count=new_cpu_count,
                                              memory_capacity_in_gb=new_memory_in_gb,
                                              image_id=image_id,
                                              instance_type='N1',
                                              purchase_count=1)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create a bcc with cds and eip
    try:
        create_cds_list = [
            {"storageType": "hp1", "cdsSizeInGB": "5"},
            {"storageType": "hp1", "cdsSizeInGB": "10"}
        ]
        response = bcc_client.create_instance(cpu_count=new_cpu_count,
                                              memory_capacity_in_gb=new_memory_in_gb,
                                              image_id=image_id,
                                              network_capacity_in_mbps=network_capacity_in_mbps,
                                              create_cds_list=create_cds_list,
                                              instance_type='N2',
                                              purchase_count=1)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create a GPU bcc
    try:
        create_cds_list = [
            {"storageType": "hp1", "cdsSizeInGB": "5"},
            {"storageType": "hp1", "cdsSizeInGB": "10"}
        ]
        response = bcc_client.create_instance(cpu_count=12,
                                              memory_capacity_in_gb=40,
                                              image_id=image_id,
                                              instance_type='G1',
                                              gpuCard=gpu_card_type.P40,
                                              cardCount=1,
                                              local_disk_size_in_gb=450,
                                              purchase_count=1)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create a FPGA bcc
    try:
        response = bcc_client.create_instance(cpu_count=16,
                                              memory_capacity_in_gb=64,
                                              image_id=image_id,
                                              instance_type='F1',
                                              fpgaCard=fpga_card_type.KU115,
                                              cardCount=1,
                                              local_disk_size_in_gb=450,
                                              purchase_count=1)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create a dedicated_host bcc
    try:
        response = bcc_client.create_instance_from_dedicated_host(
            cpu_count=new_cpu_count,
            memory_capacity_in_gb=new_memory_in_gb,
            image_id=image_id,
            dedicated_host_id=delicade_id,
            purchase_count=1)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create bccs with internal_ips
    try:
        internal_ips = ['192.168.131.110', '192.168.131.112']
        response = bcc_client.create_instance_from_dedicated_host(
            cpu_count=new_cpu_count,
            memory_capacity_in_gb=new_memory_in_gb,
            image_id=image_id,
            purchase_count=2,
            internal_ips=internal_ips)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create a dedicated_host bcc with encrypted password
    try:
        response = bcc_client.create_instance_from_dedicated_host_with_encrypted_password(
            cpu_count=new_cpu_count,
            memory_capacity_in_gb=new_memory_in_gb,
            image_id=image_id,
            dedicated_host_id=delicade_id,
            purchase_count=1,
            name=new_name,
            admin_pass=admin_pass)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create a bcc of bid
    try:
        response = bcc_client.create_instance_of_bid(cpu_count=new_cpu_count,
                                              memory_capacity_in_gb=new_memory_in_gb,
                                              image_id=image_id,
                                              instance_type='N1',
                                              purchase_count=1,
                                              bid_model='market',
                                              spec='bcc.ic1.c1m1')
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list and get instance detail
    try:
        response = bcc_client.list_instances(
            marker='',
            max_keys=1000,
            dedicated_host_id=delicade_id,
            internal_ip=internalIp,
            zone_name=zone_name)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get instance detail
    try:
        bcc_client.get_instance(instance_id)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get instance detail which contains the failed message
    try:
        bcc_client.get_instance(instance_id, contains_failed=True)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # start instance
    try:
        bcc_client.start_instance(instance_id)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # stop instance
    try:
        bcc_client.stop_instance(instance_id=instance_id)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # stop instance force
    try:
        bcc_client.stop_instance(instance_id=instance_id, force_stop=True)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # reboot instance
    try:
        bcc_client.reboot_instance(instance_id=instance_id)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # reboot instance force
    try:
        bcc_client.reboot_instance(instance_id=instance_id, force_stop=True)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # batch add ip
    try:
        bcc_client.batch_add_ip(instance_id=instance_id, secondary_private_ip_address_count=1)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # batch del ip
    try:
        bcc_client.batch_delete_ip(instance_id=instance_id, private_ips=[''])
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # modify password
    try:
        bcc_client.modify_instance_password(instance_id=instance_id, admin_pass=admin_pass)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # modify attribute
    try:
        bcc_client.modify_instance_attributes(instance_id=instance_id, name=new_name)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # rebuild bcc instance
    try:
        bcc_client.rebuild_instance(instance_id=instance_id,
                                    image_id=image_id,
                                    admin_pass=admin_pass)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # release bcc instance
    try:
        bcc_client.release_instance(instance_id=instance_id)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # resize bcc instance
    try:
        bcc_client.resize_instance(instance_id=instance_id,
                                   cpu_count=new_cpu_count,
                                   memory_capacity_in_gb=new_memory_in_gb)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # bind bcc instance to security group
    try:
        bcc_client.bind_instance_to_security_group(instance_id=instance_id,
                                                   security_group_id=security_group_id)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # unbind bcc instance from security group
    try:
        bcc_client.unbind_instance_from_security_group(instance_id=instance_id,
                                                       security_group_id=security_group_id)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get bcc instance vnc url
    try:
        bcc_client.get_instance_vnc(instance_id)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # renew bcc instance
    try:
        billing = bcc_model.Billing(reservationLength=2)
        bcc_client.purchase_reserved_instance(instance_id=instance_id, billing=billing)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    ######################################################################################################
    #            volume operation samples
    ######################################################################################################

    # create empty cds volume
    try:
        billing = bcc_model.Billing(paymentTiming='Postpaid', reservationLength=2)
        bcc_client.create_volume_with_cds_size(cds_size_in_gb=cds_size_in_gb,
                                               billing=billing,
                                               purchase_count=1)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create cds volume form snapshot
    try:
        billing = bcc_model.Billing(paymentTiming='Postpaid', reservationLength=2)
        bcc_client.create_volume_with_snapshot_id(snapshot_id=snapshot_id,
                                                  billing=billing,
                                                  purchase_count=1)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list volume
    try:
        response = bcc_client.list_volumes(instance_id=instance_id,
                                           zone_name=zone_name,
                                           marker=volume_id_markar,
                                           max_keys=100)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get volume detail
    try:
        response = bcc_client.get_volume(volume_id=volume_id)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # attach cds volume to bcc instance
    try:
        bcc_client.attach_volume(volume_id=volume_id, instance_id=instance_id)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # detach cds volume from bcc instance
    try:
        bcc_client.detach_volume(volume_id=volume_id, instance_id=instance_id)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # release cds volume
    try:
        bcc_client.release_volume(volume_id=volume_id)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # resize cds volume
    try:
        bcc_client.resize_volume(volume_id=volume_id, new_cds_size=cds_size_in_gb)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # rollback cds volume
    try:
        bcc_client.rollback_volume(volume_id=volume_id, snapshot_id=snapshot_id)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # renew cds volume
    try:
        billing = bcc_model.Billing(reservationLength=2)
        bcc_client.purchase_reserved_volume(volume_id=volume_id, billing=billing)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    ######################################################################################################
    #            image operation samples
    ######################################################################################################

    # create image from bcc instance
    try:
        response = bcc_client.create_image_from_instance_id(image_name=image_name,
                                                            instance_id=instance_id)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create image from snapshot
    try:
        response = bcc_client.create_image_from_snapshot_id(image_name=image_name,
                                                            snapshot_id=snapshot_id)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list image
    try:
        response = bcc_client.list_images(image_type=image_type,
                                          marker=image_id_marker,
                                          max_keys=100)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get image detail
    try:
        response = bcc_client.get_image(image_id=image_id)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # delete image
    try:
        bcc_client.delete_image(image_id=image_id)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    ######################################################################################################
    #            snapshot operation samples
    ######################################################################################################

    # create snapshot from cds volume
    try:
        response = bcc_client.create_snapshot(volume_id=volume_id,
                                              snapshot_name=snapshot_name,
                                              desc=snapshot_description)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list snapshot
    try:
        response = bcc_client.list_snapshots(marker=snapshot_id_marker,
                                             max_keys=100,
                                             volume_id=volume_id)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get snapshot detail
    try:
        response = bcc_client.get_snapshot(snapshot_id=snapshot_id)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # delete snapshot
    try:
        bcc_client.delete_snapshot(snapshot_id=snapshot_id)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    ######################################################################################################
    #            security group operation samples
    ######################################################################################################

    # list security group
    try:
        response = bcc_client.list_security_groups(instance_id=instance_id,
                                                   vpc_id=vpc_id,
                                                   marker=vpc_id_marker,
                                                   max_keys=100)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create security group
    security_group_rule_ingress = bcc_model.SecurityGroupRuleModel(remark='test_rule_remark',
                                                                   direction='ingress',
                                                                   portRange='1-65535',
                                                                   protocol='tcp',
                                                                   sourceGroupId=sourceGroupId,
                                                                   sourceIp=sourceIp)

    security_group_rule_egress = bcc_model.SecurityGroupRuleModel(remark='test_rule_remark',
                                                                  direction='egress',
                                                                  portRange='1-65535',
                                                                  protocol='tcp',
                                                                  destGroupId=destGroupId,
                                                                  destIp=destIp)
    security_group_rule_list = []
    security_group_rule_list.append(security_group_rule_ingress)
    security_group_rule_list.append(security_group_rule_egress)
    try:
        response = bcc_client.create_security_group(name=security_group_name,
                                                    rules=security_group_rule_list,
                                                    vpc_id=vpc_id,
                                                    desc=security_group_description)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # delete security group
    try:
        bcc_client.delete_security_group(security_group_id=security_group_id)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # authorize security group rule
    # create security group rule
    security_group_rule_ingress = bcc_model.SecurityGroupRuleModel(remark='test_rule_remark',
                                                                   direction='ingress',
                                                                   portRange='1-65535',
                                                                   protocol='tcp',
                                                                   sourceGroupId=sourceGroupId,
                                                                   sourceIp=sourceIp)
    try:
        bcc_client.authorize_security_group_rule(security_group_id=security_group_id,
                                                 rule=security_group_rule_egress)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # revoke security group rule
    try:
        bcc_client.revoke_security_group_rule(security_group_id, rule=security_group_rule_ingress)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    ######################################################################################################
    #            zone operation samples
    ######################################################################################################

    #
    try:
        response = bcc_client.list_zones()
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # cancel autoRenew volume cluster
    try:
        response = bcc_client.cancel_autoRenew_volume_cluster(cluster_id='DC-yWfhpUbN')
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create volume cluster
    try:
        response = bcc_client.create_volume_cluster(cluster_size_in_gb=97280)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list volume cluster
    try:
        response = bcc_client.list_volume_cluster()
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get volume cluster detail
    try:
        response = bcc_client.get_volume_cluster(cluster_id='DC-yWfhpUbN')
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # resize volume cluster
    try:
        response = bcc_client.resize_volume_cluster(cluster_id='DC-yWfhpUbN', new_cluster_size=107520)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # renew volume cluster
    try:
        response = bcc_client.renew_volume_cluster(cluster_id='DC-yWfhpUbN')
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # autoRenew volume cluster
    try:
        response = bcc_client.autoRenew_volume_cluster(cluster_id='DC-yWfhpUbN')
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list recycled instances
    try:
        response = bcc_client.list_recycled_instances(payment_timing="prepay", recycle_begin='2023-03-11T00:00:00Z',
                                                      recycle_end='2023-03-31T00:00:00Z',
                                                      marker='marker', max_keys=1000, name='name')
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create instance by spec
    try:
        billing = bcc_model.Billing(paymentTiming='Prepaid', reservationLength=2, reservationTimeUnit='Year')
        response = bcc_client.create_instance_by_spec(spec='bcc.g4.c1m1', image_id='m-FBfg6s7W',
                                                      root_disk_size_in_gb=50, root_disk_storage_type='HP1',
                                                      ephemeral_disks=test_e_disk_list, create_cds_list=test_cds_list,
                                                      network_capacity_in_mbps=100, eip_name='eip_name',
                                                      internet_charge_type='charge_t1', purchase_count=2, name='n_name',
                                                      hostname='hostname-new', auto_seq_suffix=True,
                                                      is_open_hostname_domain=True, admin_pass='1234', billing=billing,
                                                      zone_name='szth', subnet_id='snet_id', security_group_id='sg_id',
                                                      relation_tag=True, is_open_ipv6=True, tags=test_tags,
                                                      key_pair_id='kp_id_test', auto_renew_time_unit='year',
                                                      auto_renew_time=3, cds_auto_renew=True, asp_id='asp_id',
                                                      bid_model='model_test', bid_price='3.14', dedicate_host_id='id1',
                                                      deploy_id='did1', deploy_id_list=['did2', 'did3'])
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # set instance auto release
    try:
        response = bcc_client.auto_release_instance(instance_id='i-XS7Db00e', release_time='2023-03-15T14:20:00Z')
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # delete instance with related resource
    try:
        response = bcc_client.release_instance_with_related_resources(instance_id='i-XS7Db00e',
                                                                      related_release_flag=True,
                                                                      delete_cds_snapshot_flag=True,
                                                                      delete_related_enis_flag=True,
                                                                      bcc_recycle_flag=True)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get instance with deploy set
    try:
        response = bcc_client.get_instance_with_deploy_set(instance_id='i-XS7Db00e', contains_failed=True)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get instance with deploy set with failed
    try:
        response = bcc_client.get_instance_with_deploy_set_and_failed(instance_id='i-XS7Db00e', contains_failed=True)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # modify instance hostname
    try:
        response = bcc_client.modify_instance_hostname(instance_id='i-XS7Db00e', hostname='new.hostname',
                                                       reboot=True, is_open_hostname_domain=True)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # recovery instances
    try:
        response = bcc_client.recovery_instances(instance_id_list=['i-XS7Db00e', 'i-vrLaXNTm'])
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get bid instance price
    try:
        response = bcc_client.get_bid_instance_price(instance_type='N1', cpu_count=1, memory_cap_in_gb=2,
                                                     root_disk_size_in_gb=200, root_disk_storage_type='new_type',
                                                     create_cds_list=test_create_cds_model_list, purchase_count=1,
                                                     name='new-name', admin_pass='admin-pass', key_pair_id='kp_id',
                                                     asp_id='asp_id', image_id='image_id', bid_model='bid_model',
                                                     bid_price='12345', network_cap_in_mbps=100, relation_tag=True,
                                                     tags=test_tags, security_group_id='sec_id', subnet_id='snet-id',
                                                     zone_name='z-name', internet_charge_type='c-type')
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get bid instance flavor
    try:
        response = bcc_client.list_bid_flavor()
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # modify_deletion_protection
    try:
        response = bcc_client.modify_deletion_protection(instance_id='i-vrLaXNTm', deletion_protection=1)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # modify_deletion_protection
    try:
        response = bcc_client.release_volume_new(volume_id='i-vrLaXNTm', auto_snapshot='on', manual_snapshot='on')
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # cancel_auto_renew_cds_volume
    try:
        response = bcc_client.cancel_auto_renew_cds_volume(volume_id='i-vrLaXNTm')
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get_available_disk_info
    try:
        response = bcc_client.get_available_disk_info(zone_name='bj')
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # tag_volume
    try:
        response = bcc_client.tag_volume("v-0RMyIJRq", relation_tag=True, tags=test_tags)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # untag_volume
    try:
        response = bcc_client.untag_volume("v-0RMyIJRq", relation_tag=True, tags=test_tags)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list_snapshot_chain
    try:
        response = bcc_client.list_snapshot_chain("v-0RMyIJRq", order='desc', order_by='volumeSize', page_no=2,
                                                  page_size=20)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # tag_snapshot_chain
    try:
        response = bcc_client.tag_snapshot_chain(chain_id='c_id', tags=test_tags)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # untag_snapshot_chain
    try:
        response = bcc_client.untag_snapshot_chain(chain_id='c_id', tags=test_tags)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # update_asp
    try:
        response = bcc_client.update_asp(name="sl-fJDs8G9i", asp_id="asp-CEZInnal", time_points=[0,13],
                                      repeat_week_days=[0,4], retention_days=2)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get_price_by_spec
    try:
        response = bcc_client.get_price_by_spec(spec_id="sl-fJDs8G9i", spec="bcc.g4.c1m1", payment_timing="prepay",
                                      zone_name="szth", purchase_num=2, purchase_length=2)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list_type_zones
    try:
        response = bcc_client.list_type_zones(spec_id="sl-fJDs8G9i", spec="bcc.g4.c1m1", product_type="prepay",
                                      instance_type="N3")
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # instance_change_vpc
    try:
        response = bcc_client.instance_change_vpc(instance_id="i-oUXBvdIx", subnet_id="sbn-5k3wawcrtktz",
                                                  internal_ip="192.168.32.2", reboot=True)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list_instance_enis
    try:
        response = bcc_client.list_instance_enis(instance_id="i-oUXBvdIx")
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list_flavor_spec
    try:
        response = bcc_client.list_flavor_spec(zone_name="szth")
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # resize_instance_by_spec
    try:
        response = bcc_client.resize_instance_by_spec(instance_id="i-oUXBvdIx", spec='bcc.g4.c1m1')
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # batch_rebuild_instances
    try:
        response = bcc_client.batch_rebuild_instances(image_id="m-U4nNXY9T", admin_pass='123456', keypair_id="123",
                                                      instance_ids=["i-oUXBvdIx", "i_id2"])
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # change_to_prepaid
    try:
        response = bcc_client.change_to_prepaid(instance_id="i-45IP2Tn7", duration=3, relation_cds=True)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list_instance_no_charge
    try:
        response = bcc_client.list_instance_no_charge(keypair_id='k-Mk1c8QPE', marker="marker", max_keys=100,
                                                      internal_ip="in_ip", zone_name='cn-bj-a')
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # cancel_bid_order
    try:
        response = bcc_client.cancel_bid_order(order_id='test_id')
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # batch_create_auto_renew_rules
    try:
        response = bcc_client.batch_create_auto_renew_rules(instance_id='i-45IP2Tn7', renew_time=2,
                                                            renew_time_unit='year')
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # batch_delete_auto_renew_rules
    try:
        response = bcc_client.batch_delete_auto_renew_rules(instance_id='i-45IP2Tn7')
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # delete_recycled_instance
    try:
        response = bcc_client.delete_recycled_instance(instance_id='i-45IP2Tn7')
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list_instance_by_instance_ids
    try:
        response = bcc_client.list_instance_by_instance_ids(instance_ids=['i-45IP2Tn7', 'i-FhvOuv4t', 'i-oUXBvdIx'],
                                                            marker='123', max_keys=10000)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get_instance_delete_progress
    try:
        response = bcc_client.get_instance_delete_progress(instance_ids=['i-45IP2Tn7', 'i-FhvOuv4t', 'i-oUXBvdIx'])
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # batch_delete_instance_with_related_resource
    try:
        response = bcc_client.batch_delete_instance_with_related_resource(instance_ids=['i-45IP2Tn7', 'i-FhvOuv4t'],
                                                                          related_release_flag=True,
                                                                          delete_cds_snapshot_flag=True,
                                                                          delete_related_enis_flag=True,
                                                                          bcc_recycle_flag=True)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # batch_start_instance
    try:
        response = bcc_client.batch_start_instance(instance_ids=['i-45IP2Tn7', 'i-FhvOuv4t'])
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # batch_stop_instance
    try:
        response = bcc_client.batch_stop_instance(instance_ids=['i-45IP2Tn7', 'i-FhvOuv4t'], force_stop=True,
                                                  stop_with_no_charge=True)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list_id_mappings
    try:
        response = bcc_client.list_id_mappings(ids=['i-FhvOuv4t'], id_type='short', object_type='bcc')
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # batch_resize_instance
    try:
        response = bcc_client.batch_resize_instance(instance_ids=['i-FhvOuv4t'], spec='bcc.g4.c1m1',
                                                    subnet_id='subnet_id', logical_zone='zone_name',
                                                    internal_ip_v4='ipv4')
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list_available_resize_specs
    try:
        response = bcc_client.list_available_resize_specs(instance_ids=['i-FhvOuv4t'], spec='bcc.g4.c1m1',
                                                          spec_id='subnet_id', logical_zone='zone_name')
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # batch_change_instance_to_prepay
    try:
        req1 = PayTimingChangeReqModel('i-FhvOuv4t', relationCds=True, cdsList=['cds1'], autoPay=False, duration=123)
        req2 = PayTimingChangeReqModel('i-45IP2Tn7')
        req = [req1, req2]
        response = bcc_client.batch_change_instance_to_prepay(req)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # batch_change_instance_to_postpay
    try:
        req1 = PayTimingChangeReqModel('i-FhvOuv4t', relationCds=True, cdsList=['cds1'], autoPay=False, duration=123)
        req2 = PayTimingChangeReqModel('i-45IP2Tn7')
        req = [req1, req2]
        response = bcc_client.batch_change_instance_to_postpay(req)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list_instance_roles
    try:
        response = bcc_client.list_instance_roles()
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # bind_instance_role
    try:
        response = bcc_client.bind_instance_role(instance_ids=['i-FhvOuv4t', 'i-FhvOuv4f'], role_name='role1')
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # unbind_instance_role
    try:
        response = bcc_client.unbind_instance_role(instance_ids=['i-FhvOuv4t', 'i-FhvOuv4f'], role_name='role1')
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # add_ipv6
    try:
        response = bcc_client.add_ipv6(instance_id='i-FhvOuv4t', ipv6_address='new_addr', reboot=True)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # delete_ipv6
    try:
        response = bcc_client.delete_ipv6(instance_id='i-FhvOuv4t', reboot=True)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # bind_image_to_tags
    try:
        response = bcc_client.bind_image_to_tags(image_id='i-FhvOuv4t', tags=test_tags)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # unbind_image_to_tags
    try:
        response = bcc_client.unbind_image_to_tags(image_id='i-FhvOuv4t', tags=test_tags)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # import_custom_image
    try:
        response = bcc_client.import_custom_image(os_name='os-name', os_arch='os-arch', os_type='os-type',
                                                  os_version='os_version', name='name', bos_url='url')
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create_remote_copy_snapshot
    try:
        dest_region_infos = [bcc_model.DestRegionInfoModel("bj", "bj1"), bcc_model.DestRegionInfoModel("sh", "sh1")]
        response = bcc_client.create_remote_copy_snapshot(snapshot_id='sid', dest_region_infos=dest_region_infos)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create_deploy_set
    try:
        response = bcc_client.create_deploy_set(name='d_set_name', desc='this is deploy set desc', strategy='HA')
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list_deploy_sets
    try:
        response = bcc_client.list_deploy_sets()
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # delete_deploy_set
    try:
        response = bcc_client.delete_deploy_set('deployset_id1')
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # modify_deploy_set
    try:
        response = bcc_client.modify_deploy_set('deployset_id1', name='name-new', desc='new desc for ds1')
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get_deploy_set
    try:
        response = bcc_client.get_deploy_set('deployset_id1')
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # update_instance_deploy
    try:
        response = bcc_client.update_instance_deploy(instance_id='iid1', deployset_id_list=['did1', 'did2'], force=True)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # del_instance_deploy
    try:
        response = bcc_client.del_instance_deploy(instance_id_list=['iid1', 'iid2'], deploy_set_id='dsid')
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)