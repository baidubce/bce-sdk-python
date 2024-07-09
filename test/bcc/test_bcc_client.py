# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
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
Unit tests for bcc client.
"""
import json
import os
import random
import string
import sys
import unittest
import uuid
import importlib

import baidubce
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.bcc import bcc_client
from baidubce.services.bcc import bcc_model
# from baidubce.services.bcc import gpu_card_type
# from baidubce.services.bcc import fpga_card_type
from baidubce.services.bcc.bcc_model import EphemeralDisk, PayTimingChangeReqModel
from baidubce import compat
from imp import reload

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')
reload(sys)

if compat.PY2:
    sys.setdefaultencoding('utf8')
# sys.setdefaultencoding('utf-8')
HOST = b'http://bcc.bj.baidubce.com'
AK = b''
SK = b''

instance_id = 'i-TC9evYT5'
volume_id = 'v-OBhaubpM'
image_id = 'm-AfH5u6IE'
snapshot_id = 's-7mEwKt4F'
system_snapshot_id = 's-hnsVUGIw'
security_group_id = 'g-dcrami1yg8u2'
region = ''

post_paid_billing = bcc_model.Billing('Postpaid', 1)
pre_paid_billing = bcc_model.Billing('Prepaid', 2)

force_stop = False
admin_pass = 'Caesar@test111'
eip_name = 'test-eip-name'
hostname = 'test-hostname'
auto_seq_suffix = True
is_open_hostname_domain = True
relation_tag = True
is_open_ipv6 = True
enterprise_security_group_id = "esg-eqk44sgk1sq2"
kunlunCard = 'KunlunR200'
isomerismCard = 'KunlunR200'
file_systems = [bcc_model.FileSystemModel("cfs-OOtXFH2RWZ",
                                          "mountAds",
                                          "/mnt",
                                          "nfs")]
user_data = "#!/bin/sh\\necho 'Hello World' | tee /root/userdata_test.txt"
deletion_protection = 1
is_open_hosteye = False
tags = [bcc_model.TagModel("test", "bcc")]
auto_snapshot_policy = bcc_model.AutoSnapshotPolicyModel('asp-name', [1,2], [1,2])
res_group_id = 'RESG-UtT3P4x4KxF'

def generate_client_token_by_random():
    """
    The alternative method to generate the random string for client_token
    if the optional parameter client_token is not specified by the user.
    :return:
    :rtype string
    """
    client_token = ''.join(random.sample(string.ascii_letters + string.digits, 36))
    return client_token


def generate_client_token_by_uuid():
    """
    The default method to generate the random string for client_token
    if the optional parameter client_token is not specified by the user.
    :return:
    :rtype string
    """
    return str(uuid.uuid4())


generate_client_token = generate_client_token_by_uuid


class TestBccClient(unittest.TestCase):
    """
    Test class for bcc sdk client
    """

    def setUp(self):
        config = BceClientConfiguration(credentials=BceCredentials(AK, SK),
                                        endpoint=HOST)
        self.client = bcc_client.BccClient(config)

    def test_create_instance(self):
        """
        test case for create_instance
        """
        instance_type = 'N3'
        spec = 'bcc.g3.c2m8'
        client_token = generate_client_token()
        instance_name = 'Caesar_test_instance_' + client_token
        self.assertEqual(
            type(self.client.create_instance(1, 1,
                                             image_id,
                                             spec=spec,
                                             eip_name=eip_name,
                                             network_capacity_in_mbps=1,
                                             hostname=hostname,
                                             auto_seq_suffix=auto_seq_suffix,
                                             is_open_hostname_domain=is_open_hostname_domain,
                                             is_open_ipv6=is_open_ipv6,
                                             relation_tag=relation_tag,
                                             enterprise_security_group_id=enterprise_security_group_id,
                                             kunlunCard=kunlunCard,
                                             isomerismCard=isomerismCard,
                                             file_systems=file_systems,
                                             user_data=user_data,
                                             deletion_protection=deletion_protection,
                                             is_open_hosteye=is_open_hosteye,
                                             instance_type=instance_type,
                                             name=instance_name,
                                             admin_pass=admin_pass,
                                             zone_name='cn-bd-a',
                                             client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_create_instance_with_interanl_ips(self):
        """
        test case for create_instance
        """
        instance_type = 'N3'
        client_token = generate_client_token()
        internal_ips = ['', '']
        instance_name = 'Caesar_test_instance_' + client_token
        self.assertEqual(
            type(self.client.create_instance(1, 1,
                                             image_id,
                                             instance_type=instance_type,
                                             name=instance_name,
                                             admin_pass=admin_pass,
                                             zone_name='cn-bd-a',
                                             purchase_count=2,
                                             internal_ips=internal_ips,
                                             client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_create_instance_by_cpu_memory(self):
        client_token = generate_client_token()
        instance_name = 'test_cpu_instance_' + client_token
        self.assertEqual(
            type(self.client.create_instance(1, 1,
                                             image_id,
                                             name=instance_name,
                                             billing=post_paid_billing,
                                             client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_create_gpu_instance(self):
        """
        test case for test_create_gpu_instance
        """
        client_token = generate_client_token()
        instance_name = 'test_instance_' + client_token
        self.assertEqual(
            type(self.client.create_instance(12, 40,
                                             image_id,
                                             name=instance_name,
                                             billing=post_paid_billing,
                                             client_token=client_token,
                                             instance_type='G1',
                                             root_disk_size_in_gb=40,
                                             gpuCard='P4',
                                             cardCount=1)),
            baidubce.bce_response.BceResponse)

    def test_create_fpga_instance(self):
        """
        test case for test_create_fpga_instance
        """
        client_token = generate_client_token()
        instance_name = 'test_instance_' + client_token
        self.assertEqual(
            type(self.client.create_instance(16, 64,
                                             "m-r3BBe7Ep",
                                             name=instance_name,
                                             billing=post_paid_billing,
                                             client_token=client_token,
                                             instance_type='F1',
                                             root_disk_size_in_gb=450,
                                             fpgaCard='KU115',
                                             cardCount=1)),
            baidubce.bce_response.BceResponse)

    def test_create_instance_with_res_group_id(self):
        """
        test case for create_instance with res_group_id
        """
        client_token = generate_client_token()
        instance_name = 'Caesar_test_instance_' + client_token
        self.assertEqual(
            type(self.client.create_instance(2, 8,
                                             image_id,
                                             spec="bcc.g5.c2m8",
                                             name=instance_name,
                                             admin_pass=admin_pass,
                                             zone_name='cn-bj-a',
                                             purchase_count=1,
                                             res_group_id=res_group_id,
                                             client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_create_instance_from_dedicated_host(self):
        """
        test case for create instance from dedicated host
        """
        ephemeral_disk = EphemeralDisk(6144)
        ephemeral_disks = [ephemeral_disk.__dict__, ephemeral_disk.__dict__]
        self.client.create_instance_from_dedicated_host(1, 2, 'm-32s5YYqD', 'd-MPgs6jPr', ephemeral_disks)

    def test_create_instance_from_dedicated_host_with_encrypted_password(self):
        """
        test case for create instance from dedicated host
        """
        ephemeral_disk = EphemeralDisk(40, 'ssd')
        ephemeral_disks = [ephemeral_disk.__dict__]
        self.client.create_instance_from_dedicated_host_with_encrypted_password(1, 2, 'm-8rU0UtxY', 'd-dgAcUk0U',
                                                                                ephemeral_disks, 1, None, admin_pass)

    def test_create_instance_of_bid(self):
        """
        test case for create_instance_of_bid
        """
        instance_type = 'N3'
        client_token = generate_client_token()
        instance_name = 'Caesar_test_instance_of_bid_' + client_token
        self.assertEqual(
            type(self.client.create_instance_of_bid(1, 1,
                                                    image_id,
                                                    instance_type=instance_type,
                                                    name=instance_name,
                                                    admin_pass=admin_pass,
                                                    client_token=client_token,
                                                    bid_model='market',
                                                    eip_name=eip_name,
                                                    hostname=hostname,
                                                    auto_seq_suffix=auto_seq_suffix,
                                                    is_open_hostname_domain=is_open_hostname_domain,
                                                    spec_id='N1',
                                                    relation_tag=relation_tag,
                                                    is_open_ipv6=is_open_ipv6,
                                                    deletion_protection=deletion_protection,
                                                    enterprise_security_group_id=enterprise_security_group_id,
                                                    isomerismCard=isomerismCard,
                                                    file_systems=file_systems,
                                                    spec='bcc.ic1.c1m1')),
            baidubce.bce_response.BceResponse)

    def test_create_instance_of_bid_with_res_group_id(self):
        """
        test case for create_instance_of_bid with res_group_id
        """
        client_token = generate_client_token()
        instance_name = 'Caesar_test_instance_of_bid_' + client_token
        self.assertEqual(
            type(self.client.create_instance_of_bid(2, 8,
                                                    image_id,
                                                    spec="bcc.g5.c2m8",
                                                    name=instance_name,
                                                    client_token=client_token,
                                                    bid_model='market',
                                                    res_group_id=res_group_id)),
            baidubce.bce_response.BceResponse)

    def test_list_instances(self):
        """
        test case for list_instances
        """
        # self.assertEqual(
        #     type(self.client.list_instances()),
        #     baidubce.bce_response.BceResponse)
        # print(self.client.list_instances(dedicated_host_id='d-MPgs6jPr'))
        # print(self.client.list_instances(zone_name='cn-bj-b'))
        print(self.client.list_instances())
        # print(self.client.list_instances(
        #     instance_ids='i-zadG8d4l,i-mOEGqKHc',
        #     instance_names='instance-u4l01f7s,instance-696snyc6',
        #     deployset_ids='dset-wSC3vLBE,dset-3KKDKcnY',
        #     security_group_ids='g-60m3jgnfdtmu,g-3g12wipcxxtc',
        #     payment_timing='Postpaid',
        #     status=' Running',
        #     tags='test:bcc1,test',
        #     vpc_id='vpc-0jna6xgejh7j',
        #     private_ips='192.168.3.31,192.168.3.3',
        #     auto_renew=True
        # ))

    def test_list_instances_by_ipv6(self):
        """
        test case for list_instances
        """
        resp = self.client.list_instances(vpc_id="vpc-nvdxt9jmp9ns", ipv6_addresses="2400:da00:e003:0:28b:4400:0:4")
        print(resp.instances)
        self.assertEqual(len(resp.instances), 1)

    def test_list_instances_by_ehc_cluster_id(self):
        """
        test case for list_instances
        """
        resp = self.client.list_instances(ehc_cluster_id="ehc-bk4hM1N3")
        print(resp.instances)
        self.assertEqual(len(resp.instances), 1)

    def test_get_instance(self):
        """
        test case for get_instance
        """

        instance_id = "i-oUXBvdIx"
        self.assertEqual(
            type(self.client.get_instance(instance_id)),
            baidubce.bce_response.BceResponse)
        print(self.client.get_instance(instance_id))

    def test_get_instance_contains_failed(self):
        """
        test case for get_instance
        """

        self.assertEqual(
            type(self.client.get_instance(instance_id, contains_failed=True)),
            baidubce.bce_response.BceResponse)
        print(self.client.get_instance(instance_id))

    def test_start_instance(self):
        """
        test case for start_instance
        """
        self.assertEqual(
            type(self.client.start_instance(instance_id)),
            baidubce.bce_response.BceResponse)

    def test_stop_instance(self):
        """
        test case for stop_instance
        """
        stopWithNoCharge = False
        self.assertEqual(
            type(self.client.stop_instance(instance_id=instance_id,
                                           stopWithNoCharge=stopWithNoCharge,
                                           force_stop=force_stop)),
            baidubce.bce_response.BceResponse)

    def test_reboot_instance(self):
        """
        test case for reboot_instance
        """
        self.assertEqual(
            type(self.client.reboot_instance(instance_id,
                                             force_stop)),
            baidubce.bce_response.BceResponse)

    def test_batch_add_ip(self):
        """
        test case for batch_add_ip
        """
        private_ips = ['192.168.1.53']
        print(self.client.batch_add_ip(instance_id, private_ips=private_ips))

    def test_batch_delete_ip(self):
        """
        test case for batch_delete_ip
        """
        private_ips = ['192.168.1.53']
        print(self.client.batch_delete_ip(instance_id, private_ips=private_ips))

    def test_modify_instance_password(self):
        """
        test case for modify_instance_password
        """
        self.assertEqual(
            type(self.client.modify_instance_password(instance_id,
                                                      admin_pass)),
            baidubce.bce_response.BceResponse)

    def test_modify_instance_attributes(self):
        """
        test case for modify_instance_attributes
        """
        name = 'name_modify'
        net_queue_cnt = 3
        self.assertEqual(
            type(self.client.modify_instance_attributes(instance_id,
                                                        name, net_queue_cnt)),
            baidubce.bce_response.BceResponse)

    def test_rebuild_instance(self):
        """
        test case for rebuild_instance
        """
        self.assertEqual(
            type(self.client.rebuild_instance(instance_id,
                                              image_id,
                                              admin_pass)),
            baidubce.bce_response.BceResponse)

    def test_rebuild_instance_with_keypair_id(self):
        '''
        test case for rebuild_instance with keypair id
        '''
        key_pair_id = 'k-JdqSutgI'
        self.assertEqual(
            type(self.client.rebuild_instance(instance_id,
                                              image_id,
                                              key_pair_id=key_pair_id)),
            baidubce.bce_response.BceResponse)

    def test_release_instance(self):
        """
        test case for release_instance
        """
        self.assertEqual(
            type(self.client.release_instance(instance_id)),
            baidubce.bce_response.BceResponse)

    def test_resize_instance(self):
        """
        test case for resize_instance
        """
        client_token = generate_client_token()
        self.assertEqual(
            type(self.client.resize_instance(instance_id,
                                             2, 4, False, 1, 40,
                                             client_token)),
            baidubce.bce_response.BceResponse)

    def test_bind_instance_to_security_group(self):
        """
        test case for bind_instance_to_security_group
        """
        self.assertEqual(
            type(self.client.bind_instance_to_security_group(instance_id,
                                                             security_group_id)),
            baidubce.bce_response.BceResponse)

    def test_unbind_instance_from_security_group(self):
        """
        test case for unbind_instance_from_security_group
        """
        self.assertEqual(
            type(self.client.unbind_instance_from_security_group(instance_id,
                                                                 security_group_id)),
            baidubce.bce_response.BceResponse)

    def test_get_instance_vnc(self):
        """
        test case for get_instance_vnc
        """
        self.assertEqual(
            type(self.client.get_instance_vnc(instance_id)),
            baidubce.bce_response.BceResponse)

    def test_purchase_reserved_instance(self):
        """
        test case for purchase_reserved_instance
        """
        billing = pre_paid_billing
        client_token = generate_client_token()
        related_renew_flag = 'CDS_EIP'
        self.assertEqual(
            type(self.client.purchase_reserved_instance(instance_id,
                                                        billing,
                                                        related_renew_flag,
                                                        client_token)),
            baidubce.bce_response.BceResponse)

    def test_list_instance_specs(self):
        """
        test case for list_instance_specs
        """
        self.assertEqual(
            type(self.client.list_instance_specs()),
            baidubce.bce_response.BceResponse)

    def test_create_volume_with_cds_size(self):
        """
        test case for create_volume_with_cds_size
        """
        client_token = generate_client_token()
        billing = pre_paid_billing
        cds_size_in_gb = 5
        create_response = self.client.create_volume_with_cds_size(cds_size_in_gb, zone_name='cn-bj-a',
                                                                  billing=billing,
                                                                  instance_id=instance_id,
                                                                  encrypt_key='k-uKooR0If',
                                                                  name='test-name',
                                                                  description='desc',
                                                                  renew_time_unit='month',
                                                                  renew_time=1,
                                                                  cluster_id='DC-luQT2ktY',
                                                                  relation_tag=True,
                                                                  auto_snapshot_policy=auto_snapshot_policy,
                                                                  tags=tags,
                                                                  client_token=client_token)
        print(create_response)
        self.assertEqual(
            type(create_response),
            baidubce.bce_response.BceResponse)

    def test_create_volume_with_snapshot_id(self):
        """
        test case for create_volume_with_snapshot_id
        """
        client_token = generate_client_token()
        self.assertEqual(
            type(self.client.create_volume_with_snapshot_id(snapshot_id,
                                                            instance_id=instance_id,
                                                            encrypt_key='k-uKooR0If',
                                                            name='test-name',
                                                            description='desc',
                                                            renew_time_unit='month',
                                                            renew_time=1,
                                                            cluster_id='DC-luQT2ktY',
                                                            relation_tag=True,
                                                            auto_snapshot_policy=auto_snapshot_policy,
                                                            tags=tags,
                                                            client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_list_volumes(self):
        """
        test case for list_volumes
        """
        print(self.client.list_volumes(cluster_id='DC-luQT2ktY'))
        # print(volume_list)
        # self.assertEqual(
        #   type(volume_list),
        #  baidubce.bce_response.BceResponse)

    def test_get_volume(self):
        """
        test case for get_volume
        """
        self.assertEqual(
            type(self.client.get_volume(volume_id)),
            baidubce.bce_response.BceResponse)
        print(self.client.get_volume(volume_id))

    def test_attach_volume(self):
        """
        test case for attach_volume
        """
        self.assertEqual(
            type(self.client.attach_volume(volume_id,
                                           instance_id)),
            baidubce.bce_response.BceResponse)

    def test_detach_volume(self):
        """
        test case for detach_volume
        """
        self.assertEqual(
            type(self.client.detach_volume(volume_id,
                                           instance_id)),
            baidubce.bce_response.BceResponse)

    def test_describe_regions(self):
        """
        test case for list all region's endpoint information with specific parameter
        """
        self.assertEqual(
            type(self.client.describe_regions(region)),
            baidubce.bce_response.BceResponse)

    def test_release_volume(self):
        """
        test case for release_volume
        """
        self.assertEqual(
            type(self.client.release_volume(volume_id)),
            baidubce.bce_response.BceResponse)

    def test_resize_volume(self):
        """
        test case for resize_volume
        """
        resize_cds_size_in_gb = 10
        new_volume_type = 'ssd'
        client_token = generate_client_token()
        self.assertEqual(
            type(self.client.resize_volume(volume_id,
                                           resize_cds_size_in_gb,
                                           new_volume_type,
                                           client_token)),
            baidubce.bce_response.BceResponse)

    def test_rollback_volume(self):
        """
        test case for rollback_volume
        """
        self.assertEqual(
            type(self.client.rollback_volume(volume_id,
                                             snapshot_id)),
            baidubce.bce_response.BceResponse)

    def test_purchase_reserved_volume(self):
        """
        test case for purchase_reserved_volume
        """
        billing = pre_paid_billing
        client_token = generate_client_token()
        self.assertEqual(
            type(self.client.purchase_reserved_volume(volume_id,
                                                      billing,
                                                      client_token)),
            baidubce.bce_response.BceResponse)

    def test_create_image_from_instance_id(self):
        """
        test case for create_image_from_instance_id
        """
        client_token = generate_client_token()
        image_name = 'test_image_from_instance_' + client_token
        self.assertEqual(
            type(self.client.create_image_from_instance_id(image_name,
                                                           instance_id=instance_id,
                                                           encrypt_key='encrypt_key',
                                                           relate_cds=True,
                                                           client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_create_image_from_snapshot_id(self):
        """
        test case for create_image_from_snapshot_id
        """
        client_token = generate_client_token()
        image_name = 'test_image_from_snapshot_' + client_token
        self.assertEqual(
            type(self.client.create_image_from_snapshot_id(image_name,
                                                           snapshot_id=system_snapshot_id,
                                                           encrypt_key='encrypt_key',
                                                           client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_list_images(self):
        """
        test case for list_images
        """
        self.assertEqual(
            type(self.client.list_images(image_name='image-name')),
            baidubce.bce_response.BceResponse)

    def test_get_image(self):
        """
        test case for get_image
        """
        self.assertEqual(
            type(self.client.get_image(image_id)),
            baidubce.bce_response.BceResponse)
        print(self.client.get_image(image_id))

    def test_delete_image(self):
        """
        test case for delete_image
        """
        self.assertEqual(
            type(self.client.delete_image(image_id)),
            baidubce.bce_response.BceResponse)

    def test_create_snapshot(self):
        """
        test case for create_snapshot
        """
        client_token = generate_client_token()
        snapshot_name = 'test_snapshot_' + client_token
        self.assertEqual(
            type(self.client.create_snapshot(volume_id,
                                             snapshot_name,
                                             tags=tags,
                                             client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_list_snapshots(self):
        """
        test case for list_snapshots
        """
        self.assertEqual(
            type(self.client.list_snapshots()),
            baidubce.bce_response.BceResponse)

    def test_get_snapshot(self):
        """
        test case for get_snapshot
        """
        self.assertEqual(
            type(self.client.get_snapshot(snapshot_id)),
            baidubce.bce_response.BceResponse)

    def test_delete_snapshot(self):
        """
        test case for delete_snapshot
        """
        self.assertEqual(
            type(self.client.delete_snapshot(snapshot_id)),
            baidubce.bce_response.BceResponse)

    def test_create_security_group(self):
        """
        test case for create_security_group
        """
        client_token = generate_client_token()
        security_group_name = 'test_security_group_' + client_token
        security_group_rule = bcc_model.SecurityGroupRuleModel('test_rule_' + client_token,
                                                               'ingress',
                                                               portRange='1-65535',
                                                               protocol='tcp',
                                                               sourceGroupId='',
                                                               sourceIp='')
        security_group_rule_list = []
        security_group_rule_list.append(security_group_rule)
        self.assertEqual(
            type(self.client.create_security_group(name=security_group_name,
                                                   rules=security_group_rule_list,
                                                   tags=tags,
                                                   client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_list_security_groups(self):
        """
        test case for list_security_groups
        """
        self.assertEqual(
            type(self.client.list_security_groups(instance_id=instance_id)),
            baidubce.bce_response.BceResponse)

    def test_delete_security_group(self):
        """
        test case for delete_security_group
        """
        self.assertEqual(
            type(self.client.delete_security_group(security_group_id)),
            baidubce.bce_response.BceResponse)

    def test_authorize_security_group_rule(self):
        """
        test case for authorize_security_group_rule
        """
        security_group_rule = bcc_model.SecurityGroupRuleModel(direction='ingress',
                                                               portRange='80-90',
                                                               protocol='tcp')
        print(self.client.authorize_security_group_rule("g-RrAecfjQ", security_group_rule))

    def test_revoke_security_group_rule(self):
        """
        test case for revoke_security_group_rule
        """
        security_group_rule = bcc_model.SecurityGroupRuleModel(direction='ingress',
                                                               portRange='80-90',
                                                               protocol='tcp')
        print(self.client.revoke_security_group_rule("g-RrAecfjQ", security_group_rule))

    def test_update_security_group_rule(self):
        """
        test case for update_security_group_rule
        """
        res = self.client.update_security_group_rule(security_group_rule_id="g-RrAecfjQ", direction='ingress')
        print(res)
        self.assertEqual(type(res), baidubce.bce_response.BceResponse)

    def test_delete_security_group_rule(self):
        """
        test case for delete_security_group_rule
        """
        res = self.client.delete_security_group_rule(security_group_rule_id="g-RrAecfjQ")
        print(res)
        self.assertEqual(type(res), baidubce.bce_response.BceResponse)

    def test_list_zones(self):
        """
        test case for list_zones
        """
        print(self.client.list_zones())

    def test_get_private_ip_list(self):
        """
        test case for get_private_ip
        """
        print(self.client.get_private_ip_list('i-gDwqItW2'))

    def test_assign_private_ip_to_instance(self):
        """
        test for assign_private_ip_to_instance
        """
        print(self.client.assign_private_ip_to_instance('i-gDwqItW2', '192.168.0.12'))

    def test_unassign_private_ip_from_instance(self):
        """
        test case for unassign_priv
        :return:
        """
        print(self.client.unassign_private_ip_from_instance('i-gDwqItW2', '192.168.0.12'))

    """
    New New New
    """

    def test_modify_instance_desc(self):
        """
        test case for modify_instance_desc
        """
        desc = 'This for testing modify_instance_desc'
        self.assertEqual(
            type(self.client.modify_instance_desc(instance_id,
                                                  desc)),
            baidubce.bce_response.BceResponse)

    def test_bind_instance_to_tags(self):
        instance_tag1 = bcc_model.TagModel(tagKey='TestKey02',
                                           tagValue='TestValue02')
        instance_tag2 = bcc_model.TagModel(tagKey='TestKey03',
                                           tagValue='TestValue03')
        instance_tag_list = []
        instance_tag_list.append(instance_tag1)
        instance_tag_list.append(instance_tag2)
        self.assertEqual(
            type(self.client.bind_instance_to_tags(instance_id=instance_id,
                                                   tags=instance_tag_list)),
            baidubce.bce_response.BceResponse)

    def test_bind_reserved_instance_to_tags(self):

        reserved_instance_ids = ['r-Qyycx1SX']
        instance_tag1 = bcc_model.TagModel(tagKey='TestKey02',
                                           tagValue='TestValue02')
        instance_tag2 = bcc_model.TagModel(tagKey='TestKey03',
                                           tagValue='TestValue03')
        instance_tags = [instance_tag1, instance_tag2]

        self.assertEqual(
            type(self.client.bind_reserved_instance_to_tags(reserved_instance_ids=reserved_instance_ids,
                                                            tags=instance_tags)),
            baidubce.bce_response.BceResponse)

    def test_unbind_reserved_instance_from_tags(self):

        reserved_instance_ids = ['r-Qyycx1SX']
        instance_tag1 = bcc_model.TagModel(tagKey='TestKey02',
                                           tagValue='TestValue02')
        instance_tag2 = bcc_model.TagModel(tagKey='TestKey03',
                                           tagValue='TestValue03')
        instance_tags = [instance_tag1, instance_tag2]

        self.assertEqual(
            type(self.client.unbind_reserved_instance_from_tags(reserved_instance_ids=reserved_instance_ids,
                                                            tags=instance_tags)),
            baidubce.bce_response.BceResponse)

    def test_bind_tags_batch_by_resource_type(self):
        resource_ids = ['r-Qyycx1SX']
        instance_tag1 = bcc_model.TagModel(tagKey='TestKey02',
                                           tagValue='TestValue02')
        instance_tag2 = bcc_model.TagModel(tagKey='TestKey03',
                                           tagValue='TestValue03')
        instance_tags = [instance_tag1, instance_tag2]
        self.client.bind_tags_batch_by_resource_type("bccri", resource_ids, instance_tags, False)

    def test_unbind_tags_batch_by_resource_type(self):
        resource_ids = ['r-Qyycx1SX']
        instance_tag1 = bcc_model.TagModel(tagKey='TestKey02',
                                           tagValue='TestValue02')
        instance_tag2 = bcc_model.TagModel(tagKey='TestKey03',
                                           tagValue='TestValue03')
        instance_tags = [instance_tag1, instance_tag2]
        self.client.unbind_tags_batch_by_resource_type("bccri", resource_ids, instance_tags, False)

    def test_unbind_instance_from_tags(self):
        instance_tag = bcc_model.TagModel(tagKey='TestKey',
                                          tagValue='TestValue')
        instance_tag_list = []
        instance_tag_list.append(instance_tag)
        self.assertEqual(
            type(self.client.unbind_instance_from_tags(instance_id=instance_id,
                                                       tags=instance_tag_list)),
            baidubce.bce_response.BceResponse)

    def test_modify_volume_attribute(self):
        cdsName = 'Test_Volume_Name01'
        self.assertEqual(
            type(self.client.modify_volume_Attribute(volume_id=volume_id,
                                                     cdsName=cdsName,
                                                     desc='desc')),
            baidubce.bce_response.BceResponse)

    def test_modify_volume_charge_type(self):
        billing = pre_paid_billing
        self.assertEqual(
            type(self.client.modify_volume_charge_type(volume_id=volume_id,
                                                       billing=billing)),
            baidubce.bce_response.BceResponse)

    def test_remote_copy_image(self):
        destRegions = ['bd']
        print(type(destRegions))
        print(destRegions)
        remote_image_name = 'Caesar-Test-01'
        self.assertEqual(
            type(self.client.remote_copy_image(image_id=image_id,
                                               name=remote_image_name,
                                               destRegions=destRegions)),
            baidubce.bce_response.BceResponse)

    def test_cancle_remote_copy_image(self):
        self.assertEqual(
            type(self.client.cancle_remote_copy_image(image_id=image_id)),
            baidubce.bce_response.BceResponse)

    def test_share_image(self):
        account_id = 'c2d9b1dfc12949c0939ca36e3aae96d7'
        self.assertEqual(
            type(self.client.share_image(image_id=image_id,
                                         account_id=account_id)),
            baidubce.bce_response.BceResponse)

    def test_unshare_image(self):
        account_id = 'c2d9b1dfc12949c0939ca36e3aae96d7'
        self.assertEqual(
            type(self.client.unshare_image(image_id=image_id,
                                           account_id=account_id)),
            baidubce.bce_response.BceResponse)

    def test_list_shared_user(self):
        self.assertEqual(
            type(self.client.list_shared_user(image_id=image_id)),
            baidubce.bce_response.BceResponse)
        print(self.client.list_shared_user(image_id=image_id))

    def test_list_os(self):
        instance_id1 = 'i-9sh6C5zx'
        instance_ids = []
        instance_ids.append(instance_id1)
        self.assertEqual(
            type(self.client.list_os(instance_ids=instance_ids)),
            baidubce.bce_response.BceResponse)
        print(self.client.list_os(instance_ids=instance_ids))

    def test_create_asp(self):
        asp_name = 'Test-asp-03'
        time_points = [0, 22]
        repeat_week_days = [0, 5]
        retention_days = '-1'
        self.assertEqual(
            type(self.client.create_asp(asp_name=asp_name,
                                        time_points=time_points,
                                        repeat_week_days=repeat_week_days,
                                        retention_days=retention_days)),
            baidubce.bce_response.BceResponse)

    def test_attach_asp(self):
        asp_id = 'asp-7RIUvnzZ'
        volume_ids = ['v-U1ngKoAp', 'v-OBhaubpM']
        self.assertEqual(
            type(self.client.attach_asp(asp_id=asp_id,
                                        volume_ids=volume_ids)),
            baidubce.bce_response.BceResponse)

    def test_detach_asp(self):
        asp_id = 'asp-7RIUvnzZ'
        volume_ids = ['v-U1ngKoAp', 'v-OBhaubpM']
        self.assertEqual(
            type(self.client.detach_asp(asp_id=asp_id,
                                        volume_ids=volume_ids)),
            baidubce.bce_response.BceResponse)

    def test_delete_asp(self):
        asp_id = 'asp-XOZhcflw'
        self.assertEqual(
            type(self.client.delete_asp(asp_id=asp_id)),
            baidubce.bce_response.BceResponse)

    def test_list_asp(self):
        self.assertEqual(
            type(self.client.list_asps()),
            baidubce.bce_response.BceResponse)

    def test_get_asp(self):
        asp_id = 'asp-KwqvyeLN'
        self.assertEqual(
            type(self.client.get_asp(asp_id=asp_id)),
            baidubce.bce_response.BceResponse)
        print(self.client.get_asp(asp_id=asp_id))

    def test_create_keypair(self):
        keypair_name = 'Test-Keypair-03'
        keypair_desc = 'This for testing creating keypair'
        self.assertEqual(
            type(self.client.create_keypair(keypair_name=keypair_name,
                                            keypair_desc=keypair_desc)),
            baidubce.bce_response.BceResponse)

    def test_import_keypair(self):
        keypair_name = 'Test-Keypair-02'
        keypair_desc = 'This for testing importing keypair'
        public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCvg3CLqlbcDsEuvweFFgNytgkpxjRXzsTFJMViLoq2DNEFK5CjR0Acg6ajRBgbjEz892XqskOZ/5aznh8OmJSK98RtIxIt9ks+9Fwhjd77Ir2hhPOd9gTUsQQDxYot2O9OYhrQFIcwHLE40X1oHESrQJPqBNda8vOmhYe3gURbxf5K/Clf6ZXXG3m3ulyWEo2xtejA36cHjfbysoQHm10a2os7oJ8pkyEjii0F2aZm8ITYdIj6h5nkNjUP15Q7IaQImqjw2mRRB+h86IYno2NJj3Y4srLcrfWwiqMQ2f8tPTbr3RuqygJvutf8bOGfME75krwo6DbUkpzJPYbBctqD'
        self.assertEqual(
            type(self.client.import_keypair(keypair_name=keypair_name,
                                            keypair_desc=keypair_desc,
                                            public_key=public_key)),
            baidubce.bce_response.BceResponse)

    def test_list_keypairs(self):
        self.assertEqual(
            type(self.client.list_keypairs()),
            baidubce.bce_response.BceResponse)

    def test_get_keypair(self):
        keypair_id = 'k-uKooR0If'
        self.assertEqual(
            type(self.client.get_keypair(keypair_id=keypair_id)),
            baidubce.bce_response.BceResponse)

    def test_attach_keypair(self):
        keypair_id = 'k-uKooR0If'
        instance_ids = ['i-9sh6C5zx', 'i-6LoHblf4']
        self.assertEqual(
            type(self.client.attach_keypair(keypair_id=keypair_id,
                                            instance_ids=instance_ids)),
            baidubce.bce_response.BceResponse)

    def test_detach_keypair(self):
        keypair_id = 'k-uKooR0If'
        instance_ids = ['i-9sh6C5zx', 'i-6LoHblf4']
        self.assertEqual(
            type(self.client.detach_keypair(keypair_id=keypair_id,
                                            instance_ids=instance_ids)),
            baidubce.bce_response.BceResponse)

    def test_delete_keypair(self):
        keypair_id = 'k-uKooR0If'
        self.assertEqual(
            type(self.client.delete_keypair(keypair_id=keypair_id)),
            baidubce.bce_response.BceResponse)

    def test_rename_keypair(self):
        keypair_id = 'k-2fywKBCN'
        keypair_name = 'Caesar-Test-01'
        self.assertEqual(
            type(self.client.rename_keypair(keypair_id=keypair_id,
                                            keypair_name=keypair_name)),
            baidubce.bce_response.BceResponse)

    def test_update_keypair_desc(self):
        keypair_id = 'k-2fywKBCN'
        keypair_desc = 'This for testing updating keypair description'
        self.assertEqual(
            type(self.client.update_keypair_desc(keypair_id=keypair_id,
                                                 keypair_desc=keypair_desc)),
            baidubce.bce_response.BceResponse)

    def test_create_volume_cluster(self):
        """
        test case for create_volume_cluster
        """
        client_token = generate_client_token()
        cluster_size_in_gb = 97280
        create_response = self.client.create_volume_cluster(cluster_size_in_gb=cluster_size_in_gb, zone_name='cn-bj-a')
        print(create_response)
        self.assertEqual(
            type(create_response),
            baidubce.bce_response.BceResponse)

    def test_list_volume_cluster(self):
        """
        test case for list_volume_cluster
        """
        create_response = self.client.list_volume_cluster()
        print(create_response)
        self.assertEqual(
            type(create_response),
            baidubce.bce_response.BceResponse)

    def test_get_volume_cluster(self):
        """
        test case for get_volume_cluster
        """
        create_response = self.client.get_volume_cluster(cluster_id='DC-yWfhpUbN')
        print(create_response)
        self.assertEqual(
            type(create_response),
            baidubce.bce_response.BceResponse)

    def test_resize_volume_cluster(self):
        """
        test case for resize_volume_cluster
        """
        create_response = self.client.resize_volume_cluster(cluster_id='DC-yWfhpUbN', new_cluster_size=107520)
        print(create_response)
        self.assertEqual(
            type(create_response),
            baidubce.bce_response.BceResponse)

    def test_renew_volume_cluster(self):
        """
        test case for renew_volume_cluster
        """
        create_response = self.client.renew_volume_cluster(cluster_id='DC-yWfhpUbN')
        print(create_response)
        self.assertEqual(
            type(create_response),
            baidubce.bce_response.BceResponse)

    def test_autoRenew_volume_cluster(self):
        """
        test case for autoRenew_volume_cluster
        """
        create_response = self.client.autoRenew_volume_cluster(cluster_id='DC-yWfhpUbN')
        print(create_response)
        self.assertEqual(
            type(create_response),
            baidubce.bce_response.BceResponse)

    def test_cancel_autoRenew_volume_cluster(self):
        """
        test case for cancel_autoRenew_volume_cluster
        """
        create_response = self.client.cancel_autoRenew_volume_cluster(cluster_id='DC-yWfhpUbN')
        print(create_response)
        self.assertEqual(
            type(create_response),
            baidubce.bce_response.BceResponse)

    def test_list_recycled_instances(self):
        """
        test case for list recycled instances
        """
        resp = self.client.list_recycled_instances(payment_timing="prepay", recycle_begin='2023-03-11T00:00:00Z')
        print(resp)
        # print(json.loads(resp.content.decode('utf-8')))

    def test_create_instance_by_spec(self):
        """
        test case for create_instance
        """
        client_token = generate_client_token()
        image_id = 'm-FBfg6s7W'
        instance_name = 'Caesar_test_instance_' + client_token
        resp = self.client.create_instance_by_spec("bcc.g4.c1m1",
                                                   image_id,
                                                   name=instance_name,
                                                   admin_pass=admin_pass,
                                                   enable_jumbo_frame=False,
                                                   ehc_cluster_id='ehc-bk4hM1N3',
                                                   client_token=client_token)
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)

    def test_auto_release_instance(self):
        """
        test case for auto_release_instance
        """
        instance_id = "i-XS7Db00e"
        resp = self.client.auto_release_instance(instance_id=instance_id, release_time='2023-03-15T14:20:00Z')
        # print(json.loads(resp.content.decode('utf-8')))

    def test_delete_with_related_resources(self):
        """
        test case for auto_release_instance
        """
        instance_id = "i-lBNzLEoM"
        resp = self.client.release_instance_with_related_resources(instance_id=instance_id, related_release_flag=True,
                                                                   bcc_recycle_flag=True)
        # print(json.loads(resp.content.decode('utf-8')))

    def test_delete_prepaid_instance_with_related_resources(self):
        """
        test case for delete prepaid instance with related resources
        """
        instance_id = "i-3OWgGtoG"
        resp = self.client.release_prepaid_instance_with_related_resources(instance_id=instance_id,
                                                                      related_release_flag=True,
                                                                      delete_cds_snapshot_flag=True,
                                                                      delete_related_enis_flag=True)
        print(resp)

    def test_get_instance_with_deploy_set(self):
        """
        test case for get_instance
        """
        instance_id = "i-oUXBvdIx"
        self.assertEqual(
            type(self.client.get_instance_with_deploy_set(instance_id)),
            baidubce.bce_response.BceResponse)
        print(self.client.get_instance(instance_id))

    def test_get_instance_with_deploy_set_and_failed(self):
        """
        test case for get_instance
        """
        instance_id = "i-oUXBvdIx"
        self.assertEqual(
            type(self.client.get_instance_with_deploy_set_and_failed(instance_id)),
            baidubce.bce_response.BceResponse)
        print(self.client.get_instance(instance_id))

    def test_modify_instance_hostname(self):
        """
        test case for modify_instance_hostname
        """
        instance_id = "i-XS7Db00e"
        resp = self.client.modify_instance_hostname(instance_id=instance_id, hostname="new.hostname20230315",
                                                    auto_reboot=True, is_open_hostname_domain=True)
        # print(json.loads(resp.content.decode('utf-8')))

    def test_recovery_instances(self):
        """
        test case for recovery_instances
        """
        instance_ids = ["i-XS7Db00e", "i-FhvOuv4t"]
        resp = self.client.recovery_instances(instance_ids)
        # print(json.loads(resp.content.decode('utf-8')))

    def test_batch_refund_resources(self):
        """
        test case for delete prepaid instance with related resources
        """
        instance_ids = ["i-oH4zX7NQ"]
        resp = self.client.batch_refund_resources(instance_ids=instance_ids, related_release_flag=True,
                                                  delete_cds_snapshot_flag=True, delete_related_enis_flag=True)
        print(resp)

    def test_get_bid_instance_price(self):
        """
        test case for get_bid_instance_price
        """
        resp = self.client.get_bid_instance_price(instance_type='N3', cpu_count=1, memory_cap_in_gb=1,
                                                  root_disk_size_in_gb=20)
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_list_bid_flavor(self):
        """
        test case for list_bid_flavor
        """
        resp = self.client.list_bid_flavor()
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_modify_deletion_protection(self):
        """
        test case for modify_deletion_protection
        """
        resp = self.client.modify_deletion_protection("i-XS7Db00e", 1)
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_modify_related_delete_policy(self):
        """
        test case for modify_related_delete_policy
        """
        resp = self.client.modify_related_delete_policy("i-ZMRzyU8f", True)
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)
        res = self.client.get_instance("i-ZMRzyU8f")
        print(res)
        self.assertEqual(res.instance.is_eip_auto_related_delete, True)
        self.client.modify_related_delete_policy("i-ZMRzyU8f", False)
        res = self.client.get_instance("i-ZMRzyU8f")
        self.assertEqual(res.instance.is_eip_auto_related_delete, False)

    def test_release_volume_new(self):
        """
        test case for release_volume_new
        """
        resp = self.client.release_volume_new("v-0RMyIJRq", manual_snapshot='on')
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_auto_renew_cds_volume(self):
        """
        test case for auto_renew_cds_volume
        """
        resp = self.client.auto_renew_cds_volume("v-0RMyIJRq", renew_time=1, renew_time_unit='month')
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_cancel_auto_renew_cds_volume(self):
        """
        test case for cancel_auto_renew_cds_volume
        """
        resp = self.client.cancel_auto_renew_cds_volume("v-0RMyIJRq")
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_get_available_disk_info(self):
        """
        test case for get_available_disk_info
        """
        resp = self.client.get_available_disk_info("cn-bj-a")
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_tag_volume(self):
        """
        test case for get_available_disk_info
        """
        tag1 = bcc_model.TagModel(tagKey='TestKey02',
                                  tagValue='TestValue02')
        tag2 = bcc_model.TagModel(tagKey='TestKey03',
                                  tagValue='TestValue03')
        tags = []
        tags.append(tag1)
        tags.append(tag2)
        resp = self.client.tag_volume("v-0RMyIJRq", relation_tag=True, tags=tags)
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_untag_volume(self):
        """
        test case for get_available_disk_info
        """
        tag1 = bcc_model.TagModel(tagKey='TestKey02',
                                  tagValue='TestValue02')
        tag2 = bcc_model.TagModel(tagKey='TestKey03',
                                  tagValue='TestValue03')
        tags = []
        tags.append(tag1)
        tags.append(tag2)
        resp = self.client.untag_volume("v-0RMyIJRq", relation_tag=True, tags=tags)
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_modify_instance_attributes_for_jumbo_frame(self):
        """
        test case for modify_instance_attributes_for_jumbo_frame
        """
        resp = self.client.modify_instance_attributes("i-XS7Db00e", enable_jumbo_frame=True)
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_list_snapshot_chain(self):
        """
        test case for get_available_disk_info
        """
        resp = self.client.list_snapshot_chain("v-0RMyIJRq")
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_tag_snapshot_chain(self):
        """
        test case for tag_snapshot_chain
        """
        tag1 = bcc_model.TagModel(tagKey='TestKey02',
                                  tagValue='TestValue02')
        tag2 = bcc_model.TagModel(tagKey='TestKey03',
                                  tagValue='TestValue03')
        tags = []
        tags.append(tag1)
        tags.append(tag2)
        resp = self.client.tag_snapshot_chain("sl-fJDs8G9i", tags=tags)
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_untag_snapshot_chain(self):
        """
        test case for untag_snapshot_chain
        """
        tag1 = bcc_model.TagModel(tagKey='TestKey02',
                                  tagValue='TestValue02')
        tag2 = bcc_model.TagModel(tagKey='TestKey03',
                                  tagValue='TestValue03')
        tags = []
        tags.append(tag1)
        tags.append(tag2)
        resp = self.client.untag_snapshot_chain("sl-fJDs8G9i", tags=tags)
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_update_asp(self):
        """
        test case for update_asp
        """
        resp = self.client.update_asp(name="sl-fJDs8G9i", asp_id="asp-CEZInnal", time_points=[0, 13],
                                      repeat_week_days=[0, 4], retention_days=2)
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_get_price_by_spec(self):
        """
        test case for get_price_by_spec
        """
        resp = self.client.get_price_by_spec(spec_id="sl-fJDs8G9i", spec="bcc.g4.c1m1", payment_timing="prepay",
                                             zone_name="szth", purchase_num=2, purchase_length=2)
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_list_type_zones(self):
        """
        test case for get_price_by_spec
        """
        resp = self.client.list_type_zones(spec_id="sl-fJDs8G9i", spec="bcc.g4.c1m1", product_type="prepay",
                                           instance_type="N3")
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_instance_change_subnet(self):
        """
        test case for instance_change_subnet
        """
        resp = self.client.instance_change_subnet(instance_id="i-pKq2Bnhf", subnet_id="sbn-wpea5ffqsu93",
                                                  internal_ip="192.168.0.5", reboot=True,
                                                  security_group_ids=["g-p8x028ept1c0"])
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_instance_change_vpc(self):
        """
        test case for instance_change_vpc
        """
        resp = self.client.instance_change_vpc(instance_id="i-oUXBvdIx", subnet_id="sbn-5k3wawcrtktz",
                                               internal_ip="192.168.32.2", reboot=True,
                                               security_group_ids=["g-9yjq****"])
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_list_instance_enis(self):
        """
        test case for list_instance_enis
        """
        resp = self.client.list_instance_enis(instance_id="i-oUXBvdIx")
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_list_flavor_spec(self):
        """
        test case for list_flavor_spec
        """
        resp = self.client.list_flavor_spec(zone_name='cn-bd-a')
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_resize_instance_by_spec(self):
        """
        test case for resize_instance_by_spec
        """
        resp = self.client.resize_instance_by_spec(instance_id="i-oUXBvdIx", spec='bcc.ic1.c1m1')
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_batch_rebuild_instances(self):
        """
        test case for resize_instance_by_spec
        """
        resp = self.client.batch_rebuild_instances(image_id="m-U4nNXY9T", admin_pass='123456', keypair_id="123",
                                                   instance_ids=["i-oUXBvdIx"])
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_change_to_prepaid(self):
        """
        test case for change_to_prepaid
        """
        resp = self.client.change_to_prepaid(instance_id="i-45IP2Tn7", duration=3, relation_cds=True)
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_list_instance_no_charge(self):
        """
        test case for list_instance_no_charge
        """
        resp = self.client.list_instance_no_charge(keypair_id='k-Mk1c8QPE', zone_name='cn-bj-a')
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_cancel_bid_order(self):
        """
        test case for cancel_bid_order
        """
        resp = self.client.cancel_bid_order(order_id='test_id')
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_batch_create_auto_renew_rules(self):
        """
        test case for batch_create_auto_renew_rules
        """
        resp = self.client.batch_create_auto_renew_rules(instance_id='i-oizn4nCC',
                                                         renew_eip=True, renew_cds=True,
                                                         renew_time=2, renew_time_unit='year')
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_batch_delete_auto_renew_rules(self):
        """
        test case for batch_delete_auto_renew_rules
        """
        resp = self.client.batch_delete_auto_renew_rules(instance_id='i-oizn4nCC', renew_eip=True, renew_cds=True)
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_delete_recycled_instance(self):
        """
        test case for delete_recycled_instance
        """
        resp = self.client.delete_recycled_instance(instance_id='i-LKFVi0gI')
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_list_instance_by_instance_ids(self):
        """
        test case for list_instance_by_instance_ids
        """
        resp = self.client.list_instance_by_instance_ids(instance_ids=['i-45IP2Tn7', 'i-FhvOuv4t', 'i-oUXBvdIx'],
                                                         marker='123', max_keys=10000)
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_get_instance_delete_progress(self):
        """
        test case for get_instance_delete_progress
        """
        resp = self.client.get_instance_delete_progress(instance_ids=['i-45IP2Tn7', 'i-FhvOuv4t', 'i-oUXBvdIx'])
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_batch_delete_instance_with_related_resource(self):
        """
        test case for batch_delete_instance_with_related_resource
        """
        resp = self.client.batch_delete_instance_with_related_resource(instance_ids=['i-FhvOuv4t'],
                                                                       related_release_flag=True, )
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_batch_start_instance(self):
        """
        test case for batch_start_instance
        """
        resp = self.client.batch_start_instance(instance_ids=['i-FhvOuv4t'])
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_batch_stop_instance(self):
        """
        test case for batch_stop_instance
        """
        resp = self.client.batch_stop_instance(instance_ids=['i-FhvOuv4t'], force_stop=True)
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_list_id_mappings(self):
        """
        test case for list_id_mappings
        """
        resp = self.client.list_id_mappings(ids=['i-FhvOuv4t'], id_type='short', object_type='bcc')
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_batch_resize_instance(self):
        """
        test case for batch_resize_instance
        """
        resp = self.client.batch_resize_instance(instance_ids=['i-FhvOuv4t'], spec='bcc.g4.c1m1',
                                                 subnet_id='subnet_id', logical_zone='zone_name', internal_ip_v4='ipv4')
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_list_available_resize_specs(self):
        """
        test case for list_available_resize_specs
        """
        resp = self.client.list_available_resize_specs(instance_ids=['i-FhvOuv4t'], spec='bcc.g4.c1m1',
                                                       spec_id='subnet_id', logical_zone='zone_name')
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_batch_change_instance_to_prepay(self):
        """
        test case for batch_change_instance_to_prepay
        """
        req1 = PayTimingChangeReqModel('i-FhvOuv4t', relationCds=True, cdsList=['cds1'], autoPay=False, duration=123)
        req2 = PayTimingChangeReqModel('i-45IP2Tn7')
        req = [req1, req2]
        resp = self.client.batch_change_instance_to_prepay(req)
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_batch_change_instance_to_postpay(self):
        """
        test case for batch_change_instance_to_postpay
        """
        req1 = PayTimingChangeReqModel('i-FhvOuv4t', relationCds=True, cdsList=['cds1'], autoPay=False, duration=123)
        req2 = PayTimingChangeReqModel('i-45IP2Tn7')
        req = [req1, req2]
        resp = self.client.batch_change_instance_to_postpay(req)
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_list_instance_roles(self):
        """
        test case for list_instance_roles
        """
        resp = self.client.list_instance_roles()
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_bind_instance_role(self):
        """
        test case for bind_instance_role
        """
        resp = self.client.bind_instance_role(['i-FhvOuv4t', 'i-45IP2Tn7'], role_name='admin')
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_unbind_instance_role(self):
        """
        test case for unbind_instance_role
        """
        resp = self.client.unbind_instance_role(['i-FhvOuv4t', 'i-45IP2Tn7'], role_name='admin')
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_add_ipv6(self):
        """
        test case for add_ipv6
        """
        resp = self.client.add_ipv6(instance_id='i-FhvOuv4t', ipv6_address='new_addr', reboot=True)
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_del_ipv6(self):
        """
        test case for delete_ipv6
        """
        resp = self.client.delete_ipv6(instance_id='i-FhvOuv4t', reboot=True)
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_bind_image_to_tags(self):
        """
        test case for bind_image_to_tags
        """
        tag1 = bcc_model.TagModel(tagKey='TestKey02',
                                  tagValue='TestValue02')
        tag2 = bcc_model.TagModel(tagKey='TestKey03',
                                  tagValue='TestValue03')
        tag_list = []
        tag_list.append(tag1)
        tag_list.append(tag2)
        resp = self.client.bind_image_to_tags(image_id='i-FhvOuv4t', tags=tag_list)
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_unbind_image_to_tags(self):
        """
        test case for unbind_image_to_tags
        """
        tag1 = bcc_model.TagModel(tagKey='TestKey02',
                                  tagValue='TestValue02')
        tag2 = bcc_model.TagModel(tagKey='TestKey03',
                                  tagValue='TestValue03')
        tag_list = []
        tag_list.append(tag1)
        tag_list.append(tag2)
        resp = self.client.unbind_image_to_tags(image_id='i-FhvOuv4t', tags=tag_list)
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_import_custom_image(self):
        """
        test case for import_custom_image
        """
        resp = self.client.import_custom_image(os_name='os-name', os_arch='os-arch', os_type='os-type',
                                               os_version='os_version', name='name', bos_url='url')
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_create_remote_copy_snapshot(self):
        """
        test case for create_remote_copy_snapshot
        """
        dest_region_infos = [bcc_model.DestRegionInfoModel("bj", "bj1"), bcc_model.DestRegionInfoModel("sh", "sh1")]
        resp = self.client.create_remote_copy_snapshot(snapshot_id='s_id', dest_region_infos=dest_region_infos)
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_create_deploy_set(self):
        """
        test case for create_deploy_set
        """
        resp = self.client.create_deploy_set(name='d_set_name', desc='this is deploy set desc', strategy='HA')
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_list_deploy_sets(self):
        """
        test case for list_deploy_sets
        """
        resp = self.client.list_deploy_sets()
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_delete_deploy_set(self):
        """
        test case for delete_deploy_set
        """
        resp = self.client.delete_deploy_set('deployset_id1')
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_modify_deploy_set(self):
        """
        test case for modify_deploy_set
        """
        resp = self.client.modify_deploy_set('deployset_id1', name='name-new', desc='new desc for ds1')
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_get_deploy_set(self):
        """
        test case for get_deploy_set
        """
        resp = self.client.get_deploy_set('deployset_id1')
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_update_instance_deploy(self):
        """
        test case for update_instance_deploy
        """
        resp = self.client.update_instance_deploy(instance_id='iid1', deployset_id_list=['did1', 'did2'], force=True)
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_del_instance_deploy(self):
        """
        test case for del_instance_deploy
        """
        resp = self.client.del_instance_deploy(instance_id_list=['iid1', 'iid2'], deploy_set_id='dsid')
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_create_ehc_cluster(self):
        """
        test case for create_ehc_cluster
        """
        resp = self.client.create_ehc_cluster('test-pysdk', 'cn-bj-a', 'test-description')
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_get_ehc_cluster_list(self):
        """
        test case for get_ehc_cluster_list
        """
        resp = self.client.get_ehc_cluster_list(ehc_cluster_id_list=['ehc-qFuANaBG'],
                                                name_list=['test-pysdk'], zone_name='cn-bj-a')
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_modify_ehc_cluster(self):
        """
        test case for modify_ehc_cluster
        """
        resp = self.client.modify_ehc_cluster('ehc-v2RcFsAI', name='test-pysdk-modify', description='')
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_delete_ehc_cluster(self):
        """
        test case for delete_ehc_cluster
        """
        ehc_cluster_id_list = []
        ehc_cluster_id_list.append('ehc-v2RcFsAI')
        ehc_cluster_id_list.append('ehc-zk7735uQ')
        resp = self.client.delete_ehc_cluster(ehc_cluster_id_list=ehc_cluster_id_list)
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_get_available_images_by_spec(self):
        """
        test case for get_available_images_by_spec
        """
        resp = self.client.get_available_images_by_spec(spec='bcc.ic4.c1m1', os_name='Centos')
        self.assertEqual(
            type(resp),
            baidubce.bce_response.BceResponse)
        if resp is not None and resp.content is not None:
            print(json.loads(resp.content.decode('utf-8')))
        else:
            print(resp)

    def test_get_cds_price(self):
        """
        test get cds price
        """
        print(self.client.get_cds_price(purchase_length=1, payment_timing='Prepaid', storage_type='cloud_hp1',
                                        cds_size_in_gb=1000, purchase_count=1, zone_name='cn-bj-a'))


if __name__ == '__main__':
    suite = unittest.TestSuite()

    # suite.addTest(TestBccClient("test_create_instance"))
    # suite.addTest(TestBccClient("test_create_instance_by_cpu_memory"))
    # suite.addTest(TestBccClient("test_create_instance_from_dedicated_host"))
    # suite.addTest(TestBccClient("test_create_volume_with_cds_size"))
    # suite.addTest(TestBccClient("test_create_volume_with_snapshot_id"))
    # suite.addTest(TestBccClient("test_create_image_from_instance_id"))
    # suite.addTest(TestBccClient("test_create_image_from_snapshot_id"))
    # suite.addTest(TestBccClient("test_create_snapshot"))
    # suite.addTest(TestBccClient("test_create_security_group"))

    # suite.addTest(TestBccClient("test_get_private_ip_list"))
    # suite.addTest(TestBccClient("test_assign_private_ip_to_instance"))
    # suite.addTest(TestBccClient("test_unassign_private_ip_from_instance"))

    # suite.addTest(TestBccClient("test_list_instances"))
    # suite.addTest(TestBccClient("test_create_gpu_instance"))
    # suite.addTest(TestBccClient("test_create_fpga_instance"))
    # suite.addTest(TestBccClient("test_list_volumes"))
    # suite.addTest(TestBccClient("test_list_images"))
    # suite.addTest(TestBccClient("test_list_snapshots"))
    # suite.addTest(TestBccClient("test_list_security_groups"))
    # suite.addTest(TestBccClient("test_get_instance"))
    # suite.addTest(TestBccClient("test_get_instance_vnc"))
    # suite.addTest(TestBccClient("test_list_instance_specs"))
    # suite.addTest(TestBccClient("test_get_volume"))
    # suite.addTest(TestBccClient("test_get_image"))
    # suite.addTest(TestBccClient("test_get_snapshot"))

    # suite.addTest(TestBccClient("test_modify_instance_password"))
    # suite.addTest(TestBccClient("test_resize_instance"))
    # suite.addTest(TestBccClient("test_release_instance"))
    # suite.addTest(TestBccClient("test_delete_snapshot"))
    # suite.addTest(TestBccClient("test_delete_security_group"))

    # suite.addTest(TestBccClient("test_authorize_security_group_rule"))
    # suite.addTest(TestBccClient("test_revoke_security_group_rule"))

    # suite.addTest(TestBccClient("test_list_zones"))

    """
    Caesar Test
    """
    # suite.addTest(TestBccClient("test_stop_instance"))
    # suite.addTest(TestBccClient("test_batch_add_bcc_ip"))
    # suite.addTest(TestBccClient("test_start_instance"))
    # suite.addTest(TestBccClient("test_create_instance"))
    # suite.addTest(TestBccClient("test_resize_instance"))
    # suite.addTest(TestBccClient("test_list_instances"))
    # suite.addTest(TestBccClient("test_get_instance"))
    # suite.addTest(TestBccClient("test_modify_instance_password"))
    # suite.addTest(TestBccClient("test_modify_instance_attributes"))
    # suite.addTest(TestBccClient("test_release_instance"))
    # suite.addTest(TestBccClient("test_resize_instance"))
    # suite.addTest(TestBccClient("test_bind_instance_to_security_group"))
    # suite.addTest(TestBccClient("test_unbind_instance_from_security_group"))
    # suite.addTest(TestBccClient("test_get_image"))
    # suite.addTest(TestBccClient("test_create_image_from_instance_id"))
    # suite.addTest(TestBccClient("test_bind_instance_to_security_group"))
    # suite.addTest(TestBccClient("test_unbind_instance_from_security_group"))
    # suite.addTest(TestBccClient("test_purchase_reserved_volume"))

    """
    Caesar New Test
    """
    # suite.addTest(TestBccClient("test_modify_instance_desc"))
    # suite.addTest(TestBccClient("test_bind_instance_to_tags"))
    # suite.addTest(TestBccClient("test_unbind_instance_from_tags"))
    # suite.addTest(TestBccClient("test_modify_volume_attribute"))
    # suite.addTest(TestBccClient("test_modify_volume_charge_type"))
    # suite.addTest(TestBccClient("test_remote_copy_image"))
    # suite.addTest(TestBccClient("test_cancle_remote_copy_image"))
    # suite.addTest(TestBccClient("test_share_image"))
    # suite.addTest(TestBccClient("test_unshare_image"))
    # suite.addTest(TestBccClient("test_list_shared_user"))
    # suite.addTest(TestBccClient("test_list_os"))
    # suite.addTest(TestBccClient("test_create_asp"))
    # suite.addTest(TestBccClient("test_attach_asp"))
    # suite.addTest(TestBccClient("test_detach_asp"))
    # suite.addTest(TestBccClient("test_delete_asp"))
    # suite.addTest(TestBccClient("test_list_asp"))
    # suite.addTest(TestBccClient("test_get_asp"))
    # suite.addTest(TestBccClient("test_create_keypair"))
    # suite.addTest(TestBccClient("test_import_keypair"))
    # suite.addTest(TestBccClient("test_list_keypairs"))
    # suite.addTest(TestBccClient("test_get_keypair"))
    # suite.addTest(TestBccClient("test_attach_keypair"))
    # suite.addTest(TestBccClient("test_detach_keypair"))
    # suite.addTest(TestBccClient("test_delete_keypair"))
    # suite.addTest(TestBccClient("test_rename_keypair"))
    # suite.addTest(TestBccClient("test_update_keypair_desc"))

    """
        0.8.84 New Testcases
    """
    # suite.addTest(TestBccClient("test_list_recycled_instances"))
    # suite.addTest(TestBccClient("test_create_instance_by_spec"))
    # suite.addTest(TestBccClient("test_auto_release_instance"))
    # suite.addTest(TestBccClient("test_delete_with_related_resources"))
    # suite.addTest(TestBccClient("test_get_instance_with_deploy_set"))
    # suite.addTest(TestBccClient("test_get_instance_with_deploy_set_and_failed"))
    # suite.addTest(TestBccClient("test_modify_instance_hostname"))
    # suite.addTest(TestBccClient("test_recovery_instances"))
    # suite.addTest(TestBccClient("test_get_bid_instance_price"))
    # suite.addTest(TestBccClient("test_list_bid_flavor"))
    # suite.addTest(TestBccClient("test_modify_deletion_protection"))
    # suite.addTest(TestBccClient("test_release_volume_new"))
    # suite.addTest(TestBccClient("test_auto_renew_cds_volume"))
    # suite.addTest(TestBccClient("test_cancel_auto_renew_cds_volume"))
    # suite.addTest(TestBccClient("test_get_available_disk_info"))
    # suite.addTest(TestBccClient("test_tag_volume"))
    # suite.addTest(TestBccClient("test_untag_volume"))
    # suite.addTest(TestBccClient("test_list_snapshot_chain"))
    # suite.addTest(TestBccClient("test_tag_snapshot_chain"))
    # suite.addTest(TestBccClient("test_untag_snapshot_chain"))
    # suite.addTest(TestBccClient("test_update_asp"))
    # suite.addTest(TestBccClient("test_get_price_by_spec"))
    # suite.addTest(TestBccClient("test_list_type_zones"))
    # suite.addTest(TestBccClient("test_instance_change_subnet"))
    # suite.addTest(TestBccClient("test_instance_change_vpc"))
    # suite.addTest(TestBccClient("test_list_instance_enis"))
    # suite.addTest(TestBccClient("test_list_flavor_spec"))
    # suite.addTest(TestBccClient("test_resize_instance_by_spec"))
    # suite.addTest(TestBccClient("test_batch_rebuild_instances"))
    # suite.addTest(TestBccClient("test_change_to_prepaid"))
    # suite.addTest(TestBccClient("test_list_instance_no_charge"))
    # suite.addTest(TestBccClient("test_cancel_bid_order"))
    # suite.addTest(TestBccClient("test_batch_create_auto_renew_rules"))
    # suite.addTest(TestBccClient("test_batch_delete_auto_renew_rules"))
    # suite.addTest(TestBccClient("test_delete_recycled_instance"))
    # suite.addTest(TestBccClient("test_list_instance_by_instance_ids"))
    # suite.addTest(TestBccClient("test_get_instance_delete_progress"))
    # suite.addTest(TestBccClient("test_batch_delete_instance_with_related_resource"))
    # suite.addTest(TestBccClient("test_batch_start_instance"))
    # suite.addTest(TestBccClient("test_batch_stop_instance"))
    # suite.addTest(TestBccClient("test_list_id_mappings"))
    # suite.addTest(TestBccClient("test_batch_resize_instance"))
    # suite.addTest(TestBccClient("test_list_available_resize_specs"))
    # suite.addTest(TestBccClient("test_batch_change_instance_to_prepay"))
    # suite.addTest(TestBccClient("test_batch_change_instance_to_postpay")))
    # suite.addTest(TestBccClient("test_list_instance_roles")))
    # suite.addTest(TestBccClient("test_bind_instance_role")))
    # suite.addTest(TestBccClient("test_unbind_instance_role")))
    # suite.addTest(TestBccClient("test_add_ipv6")))
    # suite.addTest(TestBccClient("test_del_ipv6")))
    # suite.addTest(TestBccClient("test_bind_image_to_tags")))
    # suite.addTest(TestBccClient("test_unbind_image_to_tags")))
    # suite.addTest(TestBccClient("test_import_custom_image")))
    # suite.addTest(TestBccClient("test_create_remote_copy_snapshot")))
    # suite.addTest(TestBccClient("test_create_deploy_set"))
    # suite.addTest(TestBccClient("test_list_deploy_sets"))
    # suite.addTest(TestBccClient("test_delete_deploy_set"))
    # suite.addTest(TestBccClient("test_modify_deploy_set"))
    # suite.addTest(TestBccClient("test_get_deploy_set"))
    # suite.addTest(TestBccClient("test_update_instance_deploy"))
    # suite.addTest(TestBccClient("test_del_instance_deploy"))
    # suite.addTest(TestBccClient("test_rebuild_instance_with_keypair_id"))
    # suite.addTest(TestBccClient("test_get_available_images_by_spec"))
    # suite.addTest(TestBccClient("test_delete_prepaid_instance_with_related_resources"))
    # suite.addTest(TestBccClient("test_list_instances_by_ipv6"))
    # suite.addTest(TestBccClient("test_batch_refund_resources"))

    # 0.8.91 New Testcases
    # suite.addTest(TestBccClient("test_update_security_group_rule"))
    # suite.addTest(TestBccClient("test_delete_security_group_rule"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
