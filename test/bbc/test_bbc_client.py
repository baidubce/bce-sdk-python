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
Unit tests for bbc client.
"""
import sys
import random
import string
import time
import unittest
import uuid

import baidubce
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.bbc import bbc_client, bbc_model

PY2 = sys.version_info[0]==2
if PY2:
    reload(sys)
    sys.setdefaultencoding('utf8')

HOST = b'http://bbc.bj.baidubce.com'
AK = b''
SK = b''

instance_id = 'i-N1hiBeYI'
image_id = 'm-gpsiCYAx'
flavor_id = 'BBC-I3-01S'
raid_id = 'raid-KOh4qTRC'
snapshot_id = 's-Ro9vAnQE'
system_snapshot_id = 's-hnsVUGIw'
security_group_id = 'g-1utufn3mtg1y'
subnet_id = "f42b9393-e721-4693-a1ab-2d67fe2f4d65"
zone = 'cn-bj-a'
region = ''


force_stop = False
admin_pass = 'testbbc123@baidu'

change_tags = [{"tagKey" : "test_key", "tagValue" : "test_val"}]

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

class TestBbcClient(unittest.TestCase):
    """
    Test class for bbc sdk client
    """

    def setUp(self):
        config = BceClientConfiguration(credentials=BceCredentials(AK, SK),
                        endpoint=HOST)
        self.client = bbc_client.BbcClient(config)

    def test_create_instance(self):
        """
        test create bbc instance
        """
        client_token = generate_client_token()
        zone_name = 'cn-bj-a'
        name = 'test_bbc_instance'
        billing = bbc_model.Billing('Prepaid')
        response = self.client.create_instance(flavor_id=flavor_id, image_id=image_id,
                                               raid_id=raid_id, zone_name=zone_name,
                                               client_token=client_token, name=name,
                                               admin_pass=admin_pass, security_group_id=security_group_id,
                                               auto_renew_time_unit='month', auto_renew_time=1,
                                               billing=billing, tags=change_tags)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_create_instance_with_deploy_set(self):
        """
        test create bbc instance with specified deploy set
        """
        client_token = generate_client_token()
        zone_name = 'cn-bj-a'
        name = 'test_bbc_deploy_set'
        deploy_set_id = 'dset-Ut1FNWme'
        response = self.client.create_instance(flavor_id=flavor_id, image_id=image_id,
                                               raid_id=raid_id, zone_name=zone_name,
                                               client_token=client_token, name=name,
                                               admin_pass=admin_pass, deploy_set_id=deploy_set_id, subnet_id=subnet_id)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_list_instances(self):
        """
        test list bbc instances
        """
        response = self.client.list_instances()
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)


    def test_get_instance(self):
        """
        test get bbc instance
        """

        response = self.client.get_instance(instance_id)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)
        self.assertEqual(instance_id, response.id)

    def test_get_instance_contains_failed(self):
        """
        test get bbc instance
        """

        response = self.client.get_instance(instance_id, contains_failed=True)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)
        self.assertEqual(instance_id, response.id)

    def test_start_instance(self):
        """
        test start bbc instance.
        """
        response = self.client.start_instance(instance_id=instance_id)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)
        time.sleep(5)
        instance_status = self.client.get_instance(instance_id).status
        self.assertEqual(instance_status, "Starting")


    def test_stop_instance(self):
        """
        test stop bbc instance
        """
        response = self.client.stop_instance(instance_id=instance_id, force_stop=force_stop)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)
        time.sleep(10)
        instance_status = self.client.get_instance(instance_id).status
        self.assertEqual(instance_status, "Stopped")


    def test_reboot_instance(self):
        """
        test reboot bbc instance
        """

        response = self.client.reboot_instance(instance_id=instance_id, force_stop=force_stop)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)
        instance_status = self.client.get_instance(instance_id).status
        time.sleep(20)
        self.assertEqual(instance_status, "Starting")

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

    def test_create_auto_renew_rules(self):
        """
        test case for create auto renew rules
        """
        renew_time_unit = "month"
        renew_time = 1
        print(self.client.create_auto_renew_rules(instance_id, renew_time_unit, renew_time))

    def test_delete_auto_renew_rules(self):
        """
        test case for delete auto renew rules
        """
        print(self.client.delete_auto_renew_rules(instance_id))

    def test_describe_regions(self):
        """
        test case for list all region's endpoint information with specific parameter
        """
        print(self.client.describe_regions(region))

    def test_modify_instance_name(self):
        """
        test modify the name of bbc instance
        """
        new_name = "new_test_bbc_instance2"
        response = self.client.modify_instance_name(instance_id=instance_id, name=new_name)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)
        new_instance = self.client.get_instance(instance_id)
        self.assertEqual(new_name, new_instance.name)


    def test_modify_instance_desc(self):
        """
        test modify bbc instance desc
        """
        new_desc = "example desc"
        response = self.client.modify_instance_desc(instance_id=instance_id, desc=new_desc)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)
        new_instance = self.client.get_instance(instance_id)
        self.assertEqual(new_desc, new_instance.desc)

    def test_rebuild_instance(self):
        """
        test rebuild bbc instance
        """
        rebuild_image_id = "m-BPwwiJYh"
        is_preserve_data = False
        response = self.client.rebuild_instance(instance_id=instance_id, image_id=rebuild_image_id,
                                                admin_pass=admin_pass, is_preserve_data=is_preserve_data,
                                                raid_id=raid_id)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_release_instance(self):
        """
        test release the specified bbc instance
        """
        response = self.client.release_instance(instance_id=instance_id)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_modify_instance_password(self):
        """
        test modify the admin password of the specified instance
        """
        new_admin_pass = "newpass@bbc123"
        response = self.client.modify_instance_password(instance_id=instance_id, admin_pass=new_admin_pass)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_vpc_subnet(self):
        """
        test get the information of subnet/vpc of the specified bbc instance
        """
        bbc_ids = [instance_id]
        response = self.client.get_vpc_subnet(bbc_ids=bbc_ids)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_unbind_tags(self):
        """
        test unbind the existing labels of the instance
        """

        response = self.client.unbind_tags(instance_id=instance_id, change_tags=change_tags)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_bind_tags(self):
        """
        test bind the existing labels of the instance
        """

        response = self.client.bind_tags(instance_id=instance_id, change_tags=change_tags)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_bind_reserved_instance_to_tags(self):

        reserved_instance_ids = ['r-Aev4dfQV']
        instance_tag1 = bbc_model.TagModel(tagKey='TestKey02',
                                           tagValue='TestValue02')
        instance_tag2 = bbc_model.TagModel(tagKey='TestKey03',
                                           tagValue='TestValue03')
        instance_tags = [instance_tag1, instance_tag2]

        self.assertEqual(
            type(self.client.bind_reserved_instance_to_tags(reserved_instance_ids=reserved_instance_ids,
                                                            tags=instance_tags)),
            baidubce.bce_response.BceResponse)

    def test_unbind_reserved_instance_from_tags(self):

        reserved_instance_ids = ['r-Aev4dfQV']
        instance_tag1 = bbc_model.TagModel(tagKey='TestKey02',
                                           tagValue='TestValue02')
        instance_tag2 = bbc_model.TagModel(tagKey='TestKey03',
                                           tagValue='TestValue03')
        instance_tags = [instance_tag1, instance_tag2]

        self.assertEqual(
            type(self.client.unbind_reserved_instance_from_tags(reserved_instance_ids=reserved_instance_ids,
                                                            tags=instance_tags)),
            baidubce.bce_response.BceResponse)


    def test_list_flavors(self):
        """
        test list flavors
        """
        existing_flavor_id = "BBC-I2-01"
        response = self.client.list_flavors()
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)
        flavor_ids = []
        for flavor in response.flavors:
            flavor_ids.append(flavor.flavor_id)
        self.assertTrue(existing_flavor_id in flavor_ids)



    def test_get_flavor(self):
        """
        test get flavor
        """
        response = self.client.get_flavor(flavor_id)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)
        self.assertEqual(flavor_id, response.flavor_id)


    def test_get_flavor_raid(self):
        """
        test get the raid of the specified flavor
        """
        response = self.client.get_flavor_raid(flavor_id)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)


    def test_create_image_from_instance_id(self):
        """
        test create image from instance
        """
        image_name = "test_create_image"
        response = self.client.create_image_from_instance_id(image_name=image_name, instance_id=instance_id)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)
        time.sleep(20)
        images = self.client.list_images().images
        image_names = []
        for image in images:
            image_names.append(image.name)
        self.assertTrue(image_name in image_names)


    def test_list_images(self):
        """
        test list images
        """
        existing_image_id = "m-zW3TjV7h"
        response = self.client.list_images()
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)
        ids = []
        for image in response.images:
            ids.append(image.id)
        self.assertTrue(existing_image_id in ids)




    def test_get_image(self):
        """
        test get the detailed information of the specified image
        """
        response = self.client.get_image(image_id=image_id)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)
        self.assertEqual(image_id, response.image.id)


    def test_delete_image(self):
        """
        test delete image
        """
        test_delete_image_id = "m-QMy52OqH"
        response = self.client.delete_image(image_id=test_delete_image_id)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)
        time.sleep(5)
        images = self.client.list_images().images
        image_ids = []
        for image in images:
            image_ids.append(image.id)
        self.assertTrue(test_delete_image_id not in image_ids)



    def test_get_operation_log(self):
        """
        test get operation log
        """

        response = self.client.get_operation_log()
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_create_deploy_set(self):
        """
        test create deploy set
        """
        concurrency = 1
        strategy = "tor_ha"
        desc = "test deploy set"
        name = "test_deploy_set"
        response = self.client.create_deploy_set(concurrency=concurrency, strategy=strategy,
                                                 desc=desc, name=name)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_list_deploy_sets(self):
        """
        test list deploy sets
        """
        existing_deploy_set_id = "dset-8j5RpRsO"
        response = self.client.list_deploy_sets()
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)
        deploy_set_ids = []
        for deploy_set in response.deploy_set_list:
            deploy_set_ids.append(deploy_set.deploy_set_id)
        self.assertTrue(existing_deploy_set_id in deploy_set_ids)

    def test_get_deploy_set(self):
        """
        test get deploy set
        """
        deploy_set_id = "dset-8j5RpRsO"
        response = self.client.get_deploy_set(deploy_set_id=deploy_set_id)
        print(response)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        self.assertEqual(response.deploy_set_id, deploy_set_id)

    def test_delete_deploy_set(self):
        """
        test delete deploy sets
        """
        delete_deploy_set_id = "dset-8j5RpRsO"
        response = self.client.delete_deploy_set(deploy_set_id=delete_deploy_set_id)
        print(response)
        deploy_sets = self.client.list_deploy_sets().deploy_set_list
        deploy_set_ids = []
        for deploy_set in deploy_sets:
            deploy_set_ids.append(deploy_set.deploy_set_id)
        self.assertTrue(delete_deploy_set_id not in deploy_set_ids)














