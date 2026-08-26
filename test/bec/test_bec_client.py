# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
"""
Unit tests for bec client.
"""

import unittest

import bec_test_config
from baidubce.exception import BceServerError
from baidubce.services.bec import bec_model
from baidubce.services.bec.bec_client import BecClient


class TestBecClient(unittest.TestCase):
    """
    Test class for bec sdk client
    """
    def setUp(self):
        self.bec_client = BecClient(bec_test_config.config)

    # ======================================================================
    #  VM Service tests
    # ======================================================================

    def test_create_vm_service(self):
        """test create vm service"""
        error = None
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
            response = self.bec_client.create_vm_service(
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
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_list_vm_services(self):
        """test list vm services"""
        error = None
        try:
            response = self.bec_client.list_vm_services(page_no=1, page_size=10)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_vm_service(self):
        """test get vm service detail"""
        error = None
        try:
            response = self.bec_client.get_vm_service(service_id='s-xxxxxxxx')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_update_vm_service(self):
        """test update vm service"""
        error = None
        try:
            response = self.bec_client.update_vm_service(
                service_id='s-xxxxxxxx',
                update_type='resource',
                cpu=4,
                memory=8
            )
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_delete_vm_service(self):
        """test delete vm service"""
        error = None
        try:
            response = self.bec_client.delete_vm_service(service_id='s-xxxxxxxx')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_start_vm_service(self):
        """test start vm service"""
        error = None
        try:
            response = self.bec_client.vm_service_action(
                service_id='s-xxxxxxxx', action='start')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_stop_vm_service(self):
        """test stop vm service"""
        error = None
        try:
            response = self.bec_client.vm_service_action(
                service_id='s-xxxxxxxx', action='stop')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_vm_service_metrics(self):
        """test get vm service metrics"""
        error = None
        try:
            response = self.bec_client.get_vm_service_metrics(
                service_id='s-xxxxxxxx',
                metrics_type='CPU',
                start=1690000000,
                end=1690003600,
                step_in_min=5
            )
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_batch_delete_vm_services(self):
        """test batch delete vm services"""
        error = None
        try:
            response = self.bec_client.batch_delete_vm_services(
                service_ids=['s-xxxxxxxx', 's-yyyyyyyy']
            )
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_batch_operate_vm_services(self):
        """test batch operate vm services"""
        error = None
        try:
            response = self.bec_client.batch_operate_vm_services(
                action='stop',
                service_ids=['s-xxxxxxxx', 's-yyyyyyyy']
            )
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    # ======================================================================
    #  VM Instance tests
    # ======================================================================

    def test_create_vm_service_instance(self):
        """test create vm service instance"""
        error = None
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
            response = self.bec_client.create_vm_service_instance(
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
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_list_vm_instances(self):
        """test list vm instances"""
        error = None
        try:
            response = self.bec_client.list_vm_instances(page_no=1, page_size=10)
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_vm_instance(self):
        """test get vm instance detail"""
        error = None
        try:
            response = self.bec_client.get_vm_instance(vm_id='vm-xxxxxxxx')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_update_vm_instance(self):
        """test update vm instance"""
        error = None
        try:
            response = self.bec_client.update_vm_instance(
                vm_id='vm-xxxxxxxx',
                update_type='vmName',
                vm_name='new-vm-name',
            )
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_start_vm_instance(self):
        """test start vm instance"""
        error = None
        try:
            response = self.bec_client.operate_vm_deployment(
                vm_id='vm-xxxxxxxx', action='start')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_stop_vm_instance(self):
        """test stop vm instance"""
        error = None
        try:
            response = self.bec_client.operate_vm_deployment(
                vm_id='vm-xxxxxxxx', action='stop')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_restart_vm_instance(self):
        """test restart vm instance"""
        error = None
        try:
            response = self.bec_client.operate_vm_deployment(
                vm_id='vm-xxxxxxxx', action='restart')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_reinstall_vm_instance(self):
        """test reinstall vm instance"""
        error = None
        try:
            key_config = bec_model.KeyConfig(type='password', admin_pass='your-admin-password')
            response = self.bec_client.reinstall_vm_instance(
                vm_id='vm-xxxxxxxx',
                image_id='m-xxxxxxxx',
                image_type='bec',
                key_config=key_config
            )
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_bind_security_group(self):
        """test bind security group"""
        error = None
        try:
            response = self.bec_client.bind_security_group(
                action='bind',
                instance_ids=['vm-xxxxxxxx'],
                security_group_id='sg-xxxxxxxx'
            )
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_unbind_security_group(self):
        """test unbind security group"""
        error = None
        try:
            response = self.bec_client.bind_security_group(
                action='unbind',
                instance_ids=['vm-xxxxxxxx'],
                security_group_id='sg-xxxxxxxx'
            )
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_list_node_vm_instances(self):
        """test list vm instances by node"""
        error = None
        try:
            response = self.bec_client.list_node_vm_instances(
                region='EAST_CHINA',
                service_provider='CHINA_UNICOM',
                city='HANGZHOU',
                page_no=1,
                page_size=10
            )
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_vm_instance_metrics(self):
        """test get vm instance metrics"""
        error = None
        try:
            response = self.bec_client.get_vm_instance_metrics(
                vm_id='vm-xxxxxxxx',
                metrics_type='CPU',
                start=1690000000,
                end=1690003600,
                step_in_min=5
            )
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_vm_instance_config(self):
        """test get vm instance config"""
        error = None
        try:
            response = self.bec_client.get_vm_instance_config(vm_id='vm-xxxxxxxx')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_create_vm_private_ip(self):
        """test create vm private ip"""
        error = None
        try:
            response = self.bec_client.create_vm_private_ip(
                vm_id='vm-xxxxxxxx',
                secondary_private_ip_address_count=1
            )
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_delete_vm_private_ip(self):
        """test delete vm private ip"""
        error = None
        try:
            response = self.bec_client.delete_vm_private_ip(
                vm_id='vm-xxxxxxxx',
                private_ips=['192.168.1.10']
            )
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_delete_vm_instance(self):
        """test delete vm instance"""
        error = None
        try:
            response = self.bec_client.delete_vm_instance(vm_id='vm-xxxxxxxx')
            print(response)
        except BceServerError as e:
            error = e
        finally:
            self.assertIsNone(error)


if __name__ == "__main__":
    unittest.main()
