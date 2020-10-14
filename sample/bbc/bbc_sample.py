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
Samples for bbc client.
"""

# !/usr/bin/env python
# coding=utf-8

import bbc_sample_conf
from baidubce.exception import BceHttpClientError
from baidubce.exception import BceServerError
from baidubce.services.bbc import bbc_model
from baidubce.services.bbc.bbc_client import BbcClient

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    __logger = logging.getLogger(__name__)

    instance_id = 'i-lxhfzmm5'
    image_id = 'm-gpsiCYAx'
    flavor_id = 'BBC-I3-01S'
    raid_id = 'raid-KOh4qTRC'
    security_group_id = 'g-1utufn3mtg1y'
    subnet_id = "f42b9393-e721-4693-a1ab-2d67fe2f4d65"
    zone_name = 'cn-bj-a'
    name = 'test_bbc_instance'
    admin_pass = 'testbbc123@baidu'
    billing = bbc_model.Billing('Prepaid')
    deploy_set_id = 'dset-Ut1FNWme'
    private_ips = ['192.168.1.53']
    new_name = 'new_test_bbc_instance2'
    new_desc = 'example desc'
    rebuild_image_id = 'm-BPwwiJYh'
    is_preserve_data = False
    new_admin_pass = "newpass@bbc123"
    bbc_ids = [instance_id]
    change_tags = [{"tagKey": "test_key", "tagValue": "test_val"}]
    image_name = "test_create_image"
    concurrency = 1
    strategy = "tor_ha"
    deploy_set_desc = "test deploy set"
    deploy_set_name = "test_deploy_set"
    deploy_set_id = "dset-8j5RpRsO"

    ######################################################################################################
    #            bcc operation samples
    ######################################################################################################

    # create a bcc client
    bbc_client = BbcClient(bbc_sample_conf.config)

    # create a bbc only
    try:
        response = bbc_client.create_instance(flavor_id=flavor_id, image_id=image_id,
                                              raid_id=raid_id, zone_name=zone_name,
                                              name=name, admin_pass=admin_pass,
                                              subnet_id=subnet_id)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create a bbc with deploySet id
    try:
        response = bbc_client.create_instance(flavor_id=flavor_id, image_id=image_id,
                                              raid_id=raid_id, zone_name=zone_name,
                                              name=name, deploy_set_id=deploy_set_id,
                                              admin_pass=admin_pass, subnet_id=subnet_id)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create a bbc with autoRenew
    try:
        response = bbc_client.create_instance(flavor_id=flavor_id, image_id=image_id,
                                              raid_id=raid_id, zone_name=zone_name,
                                              name=name, admin_pass=admin_pass,
                                              security_group_id=security_group_id, auto_renew_time_unit='month',
                                              auto_renew_time=1, billing=billing)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list the instances
    try:
        response = bbc_client.list_instances()
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get the instance detail
    try:
        response = bbc_client.get_instance(instance_id=instance_id)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get the instance detail which contains the failed message
    try:
        response = bbc_client.get_instance(instance_id=instance_id, contains_failed=True)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # start the instance
    try:
        bbc_client.start_instance(instance_id=instance_id)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # stop the instance
    try:
        bbc_client.stop_instance(instance_id=instance_id)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # reboot the instance
    try:
        bbc_client.reboot_instance(instance_id=instance_id)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # batch add private ip
    try:
        response = bbc_client.batch_add_ip(instance_id=instance_id, private_ips=private_ips)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # batch delete private ip
    try:
        response = bbc_client.batch_delete_ip(instance_id=instance_id, private_ips=private_ips)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # modify the instance's name
    try:
        bbc_client.modify_instance_name(instance_id=instance_id, name=new_name)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # modify the instance's desc
    try:
        bbc_client.modify_instance_desc(instance_id=instance_id, desc=new_desc)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # rebuild the instance
    try:
        bbc_client.rebuild_instance(instance_id=instance_id, image_id=rebuild_image_id,
                                    admin_pass=admin_pass, is_preserve_data=is_preserve_data,
                                    raid_id=raid_id)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # release the instance
    try:
        bbc_client.release_instance(instance_id=instance_id)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # modify the instance's password
    try:
        bbc_client.modify_instance_password(instance_id=instance_id, admin_pass=new_admin_pass)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get vpc subnet
    try:
        response = bbc_client.get_vpc_subnet(bbc_ids=bbc_ids)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # unbind the tag
    try:
        bbc_client.unbind_tags(instance_id=instance_id, change_tags=change_tags)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list flavors
    try:
        response = bbc_client.list_flavors()
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get flavor
    try:
        response = bbc_client.get_flavor(flavor_id=flavor_id)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get the raid of the specified flavor
    try:
        response = bbc_client.get_flavor_raid(flavor_id=flavor_id)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create auto renew rules
    try:
        bbc_client.create_auto_renew_rules(instance_id=instance_id, auto_renew_time_unit='month', auto_renew_time=1)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # delete auto renew rules
    try:
        bbc_client.delete_auto_renew_rules(instance_id=instance_id)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create image from instance
    try:
        response = bbc_client.create_image_from_instance_id(image_name=image_name, instance_id=instance_id)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list images
    try:
        response = bbc_client.list_images()
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get the image detail
    try:
        response = bbc_client.get_image(image_id=image_id)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # delete image
    try:
        bbc_client.delete_image(image_id=image_id)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get operation log
    try:
        response = bbc_client.get_operation_log()
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create deploy set
    try:
        response = bbc_client.create_deploy_set(concurrency=concurrency, strategy=strategy,
                                                desc=deploy_set_desc, name=deploy_set_name)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list deploy sets
    try:
        response = bbc_client.list_deploy_sets()
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get deploy set
    try:
        response = bbc_client.get_deploy_set(deploy_set_id=deploy_set_id)
        print response
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # delete deploy sets
    try:
        bbc_client.delete_deploy_set(deploy_set_id=deploy_set_id)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)
