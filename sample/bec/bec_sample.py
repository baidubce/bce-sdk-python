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
Samples for bec client.
"""

# !/usr/bin/env python
# coding=utf-8

import bec_sample_conf
from baidubce.exception import BceHttpClientError
from baidubce.exception import BceServerError
from baidubce.services.bec import bec_model
from baidubce.services.bec.bec_client import BecClient

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    __logger = logging.getLogger(__name__)

    # create a bec client
    bec_client = BecClient(bec_sample_conf.config)

    ######################################################################################################
    #            VM Service (虚机服务) samples
    ######################################################################################################

    # create a vm service
    try:
        deploy_instances = [
            bec_model.DeploymentInstance(
                region_id='cn-hangzhou-cm',
                replicas=1
            )
        ]
        system_volume = bec_model.SystemVolumeConfig(
            volume_type='NVME',
            size_in_gb=40,
            name='sys'
        )
        key_config = bec_model.KeyConfig(
            type='password',
            admin_pass='your-admin-password'
        )

        response = bec_client.create_vm_service(
            deploy_instances=deploy_instances,
            image_id='m-xxxxxxxx',
            image_type='bec',
            system_volume=system_volume,
            key_config=key_config,
            vm_name='test-bec-service',
            cpu=2,
            memory=4,
            payment_method='postpay'
        )
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list vm services
    try:
        response = bec_client.list_vm_services(page_no=1, page_size=10)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get vm service detail
    try:
        response = bec_client.get_vm_service(service_id='s-xxxxxxxx')
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # update vm service
    try:
        response = bec_client.update_vm_service(
            service_id='s-xxxxxxxx',
            update_type='resource',
            cpu=4,
            memory=8
        )
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # stop vm service
    try:
        response = bec_client.vm_service_action(service_id='s-xxxxxxxx',
                                                action='stop')
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # start vm service
    try:
        response = bec_client.vm_service_action(service_id='s-xxxxxxxx',
                                                action='start')
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get vm service metrics
    try:
        response = bec_client.get_vm_service_metrics(
            service_id='s-xxxxxxxx',
            metrics_type='CPU',
            start=1690000000,
            end=1690003600,
            step_in_min=5
        )
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # batch delete vm services
    try:
        response = bec_client.batch_delete_vm_services(
            service_ids=['s-xxxxxxxx', 's-yyyyyyyy']
        )
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # batch operate vm services
    try:
        response = bec_client.batch_operate_vm_services(
            action='stop',
            service_ids=['s-xxxxxxxx', 's-yyyyyyyy']
        )
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # delete vm service
    try:
        response = bec_client.delete_vm_service(service_id='s-xxxxxxxx')
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    ######################################################################################################
    #            VM Instance (虚机实例) samples
    ######################################################################################################

    # create vm service instance (under existing service)
    try:
        deploy_instances = [
            bec_model.DeploymentInstance(
                region_id='cn-hangzhou-cm',
                replicas=1
            )
        ]
        system_volume = bec_model.SystemVolumeConfig(
            volume_type='NVME',
            size_in_gb=40,
            name='sys'
        )
        key_config = bec_model.KeyConfig(
            type='password',
            admin_pass='your-admin-password'
        )

        response = bec_client.create_vm_service_instance(
            service_id='s-xxxxxxxx',
            deploy_instances=deploy_instances,
            image_id='m-xxxxxxxx',
            image_type='bec',
            system_volume=system_volume,
            key_config=key_config,
            vm_name='test-bec-vm',
            cpu=2,
            memory=4
        )
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list vm instances
    try:
        response = bec_client.list_vm_instances(page_no=1, page_size=10)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get vm instance detail
    try:
        response = bec_client.get_vm_instance(vm_id='vm-xxxxxxxx')
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # update vm instance
    try:
        response = bec_client.update_vm_instance(
            vm_id='vm-xxxxxxxx',
            update_type='vmName',
            vm_name='new-vm-name',
        )
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # start vm instance
    try:
        response = bec_client.operate_vm_deployment(vm_id='vm-xxxxxxxx',
                                                    action='start')
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # stop vm instance
    try:
        response = bec_client.operate_vm_deployment(vm_id='vm-xxxxxxxx',
                                                    action='stop')
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # restart vm instance
    try:
        response = bec_client.operate_vm_deployment(vm_id='vm-xxxxxxxx',
                                                    action='restart')
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # reinstall OS of vm instance
    try:
        key_config = bec_model.KeyConfig(type='password', admin_pass='your-admin-password')
        response = bec_client.reinstall_vm_instance(
            vm_id='vm-xxxxxxxx',
            image_id='m-xxxxxxxx',
            image_type='bec',
            key_config=key_config
        )
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # bind security group
    try:
        response = bec_client.bind_security_group(
            action='bind',
            instance_ids=['vm-xxxxxxxx'],
            security_group_id='sg-xxxxxxxx'
        )
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # unbind security group
    try:
        response = bec_client.bind_security_group(
            action='unbind',
            instance_ids=['vm-xxxxxxxx'],
            security_group_id='sg-xxxxxxxx'
        )
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list node vm instances
    try:
        response = bec_client.list_node_vm_instances(
            region='EAST_CHINA',
            service_provider='CHINA_UNICOM',
            city='HANGZHOU',
            page_no=1,
            page_size=10
        )
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get vm instance metrics
    try:
        response = bec_client.get_vm_instance_metrics(
            vm_id='vm-xxxxxxxx',
            metrics_type='CPU',
            start=1690000000,
            end=1690003600,
            step_in_min=5
        )
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get vm instance config
    try:
        response = bec_client.get_vm_instance_config(vm_id='vm-xxxxxxxx')
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create vm private ip
    try:
        response = bec_client.create_vm_private_ip(
            vm_id='vm-xxxxxxxx',
            secondary_private_ip_address_count=1
        )
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # delete vm private ip
    try:
        response = bec_client.delete_vm_private_ip(
            vm_id='vm-xxxxxxxx',
            private_ips=['192.168.1.10']
        )
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # delete vm instance
    try:
        response = bec_client.delete_vm_instance(vm_id='vm-xxxxxxxx')
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)
