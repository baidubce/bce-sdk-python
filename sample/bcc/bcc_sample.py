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

#!/usr/bin/env python
#coding=utf-8

import bcc_sample_conf
from baidubce.exception import BceHttpClientError
from baidubce.exception import BceServerError
from baidubce.services.bcc import bcc_model
from baidubce.services.bcc import fpga_card_type
from baidubce.services.bcc import gpu_card_type
from baidubce.services.bcc.bcc_client import BccClient

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









