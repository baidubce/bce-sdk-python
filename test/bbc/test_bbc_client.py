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
from baidubce.services.bbc import bbc_client

PY2 = sys.version_info[0]==2
if PY2:
    reload(sys)
    sys.setdefaultencoding('utf8')

HOST = b'http://bbc.bj.baidubce.com'
AK = b'031def8902d346c6a28719948d11e024'
SK = b'00fd30dfac894cae92e16eefaf33fbe0'

instance_id = 'i-wUHUDrhI'
image_id = 'm-BPwwiJYh'
flavor_id = 'BBC-I2-01'
raid_id = 'raid-malo48xg'
snapshot_id = 's-Ro9vAnQE'
system_snapshot_id = 's-hnsVUGIw'
security_group_id = 'g-hweloYd8'
#subnet_id = "604cebcd-740d-49d1-a1ac-72a91f5e34aa"
subnet_id = "sbn-e7dp3hmvvv43"


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
        response = self.client.create_instance(flavor_id=flavor_id, image_id=image_id,
                                               raid_id=raid_id, zone_name=zone_name,
                                               client_token=client_token, name=name,
                                               admin_pass=admin_pass, subnet_id=subnet_id)
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

    def test_start_instance(self):
        """
        test start instance.
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
        test release the specified instance
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
        test get the information of subnet/vpc of the specified instance
        """
        bbc_ids = [instance_id]
        response = self.client.get_vpc_subnet(bbc_ids=bbc_ids)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_unbind_tags(self):
        """
        test unbind the existing label of the instance
        """

        response = self.client.unbind_tags(instance_id=instance_id, change_tags=change_tags)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)



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
        test get the  raid of the specified flavor
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









