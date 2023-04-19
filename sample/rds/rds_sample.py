# -*- coding: utf-8 -*- 
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
Samples for scs client.
"""
import logging
import os
import sys

import rds_sample_conf
import baidubce.exception as ex
import baidubce.services.rds.rds_client as rds
from baidubce.services.rds import model

if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')

logging.basicConfig(level=logging.DEBUG, filename='./rds_sample.log', filemode='w')
LOG = logging.getLogger(__name__)
CONF = rds_sample_conf

if __name__ == '__main__':
    rds_client = rds.RdsClient(CONF.config)
    try:
        # create instance
        LOG.debug('\n\n\nSample 1: Create Instance\n\n\n')
        instance_name = 'rds-py-create'
        billing = model.Billing(pay_method='Postpaid')
        purchase_count = 1
        engine= 'MySql'
        engine_version = '5.7'
        category = 'Standard'
        cpu_count = 1
        memory_capacity = 2
        volume_capacity = 100
        disk_io_type = 'cloud_enha'
        vpc_id = 'vpc-ph7237ym686c'
        is_direct_pay = bool(1)
        subnets = [
            model.SubnetMap(u'cn-bj-d', u'sbn-p1va817v3qn0')
        ]
        #tags = [
        #    model.Tag(u'key', u'value'),
        #    model.Tag(u'zyh', u'haha')
        #]
        #parameter_template_id = "167"
        #initial_data_reference = model.InitialDataReference(instance_id='rds-gvQDRheI', reference_type='snapshot', snapshot_id='1681225244867371501')
        #data = [
        #    model.RecoveryToSourceInstanceModel(db_name='test2', new_dbname='test22', restore_mode='table',
        #                                        tables=[
        #                                            model.Tables(table_name='table1', new_tablename='table11')
        #                                        ]
        #                                        )
        #]
        response = rds_client.create_instance(instance_name=instance_name, billing=billing,
                                              purchase_count=purchase_count, engine=engine,
                                              engine_version=engine_version, category=category,
                                              cpu_count=cpu_count, memory_capacity=memory_capacity,
                                              volume_capacity=volume_capacity, disk_io_type=disk_io_type,
                                              vpc_id=vpc_id, subnets=subnets,
                                              is_direct_pay=is_direct_pay)
        LOG.debug('\n%s', response)
        # create readReplica instance
        LOG.debug('\n\n\nSample 2: Create readReplica Instance\n\n\n')
        instance_name = 'rds-py-create-read'
        source_instance_id='rds-6fGKPL1O'
        billing = model.Billing(pay_method='Postpaid')
        cpu_count = 1
        memory_capacity = 1
        volume_capacity = 100
        vpc_id = 'vpc-ph7237ym686c'
        is_direct_pay = bool(1)
        subnets = [
            model.SubnetMap(u'cn-bj-d', u'sbn-p1va817v3qn0')
        ]
        response = rds_client.create_read_instance(instance_name=instance_name, source_instance_id=source_instance_id,
                                                   billing=billing, vpc_id=vpc_id, is_direct_pay=is_direct_pay,
                                                   subnets=subnets,
                                                   cpu_count=cpu_count, memory_capacity=memory_capacity,
                                                   volume_capacity=volume_capacity)
        LOG.debug('\n%s', response)

        # create proxy instance
        LOG.debug('\n\n\nSample 3: Create proxy Instance\n\n\n')
        instance_name = 'rds-py-create-proxy'
        source_instance_id='rds-6fGKPL1O'
        billing = model.Billing(pay_method='Postpaid')
        node_amount = 2
        vpc_id = 'vpc-ph7237ym686c'
        is_direct_pay = bool(1)
        subnets = [
            model.SubnetMap(u'cn-bj-d', u'sbn-p1va817v3qn0')
        ]
        response = rds_client.create_proxy_instance(instance_name=instance_name, source_instance_id=source_instance_id,
                                                   billing=billing, vpc_id=vpc_id, is_direct_pay=is_direct_pay,
                                                   subnets=subnets, node_amount=node_amount)
        LOG.debug('\n%s', response)
        
        # get instance detail
        LOG.debug('\n\n\nSample 4: Get Instance Detail\n\n\n')
        response = rds_client.get_instance_detail("rds-6fGKPL1O")
        LOG.debug('\n%s', response)
        
        # list instances
        LOG.debug('\n\n\nSample 5: List Instance\n\n\n')
        response = rds_client.list_instances(max_keys=10)
        LOG.debug('\n%s', response)
        
        # resize instance
        LOG.debug('\n\n\nSample 6: Resize Instance\n\n\n')
        instance_id = 'rds-UK8i9we1'
        cpu_count = 1
        memory_capacity = 2
        volume_capacity = 100
        #node_amount = 4
        is_direct_pay = bool(1)

        response = rds_client.resize_instance(instance_id=instance_id, cpu_count=cpu_count,
                                              memory_capacity=memory_capacity, volume_capacity=volume_capacity,
                                              is_direct_pay=is_direct_pay)
        LOG.debug('\n%s', response)
        
        # delete instance
        LOG.debug('\n\n\nSample 7: delete Instance\n\n\n')
        response = rds_client.delete_instance("rds-l3rdRiud,rds-XzXSBkhc")
        LOG.debug('\n%s', response)

        # recycler list
        LOG.debug('\n\n\nSample 8: List Recycler\n\n\n')
        response = rds_client.recycler_list()
        LOG.debug('\n%s', response)

        # recycler recover
        LOG.debug('\n\n\nSample 9: Recover Recycler\n\n\n')
        instance_ids = ["rds-l3rdRiud", "rds-XzXSBkhc"]
        response = rds_client.recycler_recover(instance_ids)
        LOG.debug('\n%s', response)
        
        # delete recycler
        LOG.debug('\n\n\nSample 10: Delete Recycler\n\n\n')
        response = rds_client.delete_recycler("rds-XzXSBkhc")
        LOG.debug('\n%s', response)
        

        # delete recycler batch
        LOG.debug('\n\n\nSample 11: Delete Recycler Batch\n\n\n')
        response = rds_client.delete_recycler_batch("rds-PBQyGef3,rds-l3rdRiud")
        LOG.debug('\n%s', response)
        
        # reboot instance
        LOG.debug('\n\n\nSample 12: Reboot Instance\n\n\n')
        response = rds_client.reboot_instance("rds-cteusMhZ")
        LOG.debug('\n%s', response)
        
        # rename instance
        LOG.debug('\n\n\nSample 13: Rename Instance\n\n\n')
        instance_id = "rds-cteusMhZ"
        instance_name = "py-test"
        response = rds_client.rename_instance(instance_id=instance_id, instance_name=instance_name)
        LOG.debug('\n%s', response)
        
        # modifySyncMode instance
        LOG.debug('\n\n\nSample 14: ModifySyncMode Instance\n\n\n')
        instance_id = "rds-cteusMhZ"
        sync_mode = "Semi_sync"
        response = rds_client.modify_sync_mode_instance(instance_id=instance_id, sync_mode=sync_mode)
        LOG.debug('\n%s', response)
        
        # modifyEndpoint instance
        LOG.debug('\n\n\nSample 15: modifyEndpoint Instance\n\n\n')
        instance_id = "rds-cteusMhZ"
        address = "python"
        response = rds_client.modify_endpoint_instance(instance_id=instance_id, address=address)
        LOG.debug('\n%s', response)
        
        # modifyPublicAccess instance
        LOG.debug('\n\n\nSample 16: modifyPublicAccess Instance\n\n\n')
        instance_id = "rds-cteusMhZ"
        public_access = bool(1)
        response = rds_client.modify_public_access_instance(instance_id=instance_id, public_access=public_access)
        LOG.debug('\n%s', response)
        
        # autoRenew instance
        LOG.debug('\n\n\nSample 17: autoRenew Instance\n\n\n')
        instance_ids = ["rds-cteusMhZ"]
        auto_renew_time_unit = "month"
        auto_renew_time = 1

        response = rds_client.auto_renew_instance(instance_ids=instance_ids, auto_renew_time_unit=auto_renew_time_unit,
                                                  auto_renew_time=auto_renew_time)
        LOG.debug('\n%s', response)
        
        LOG.debug('\n\n\nSample 18: zone List\n\n\n')

        response = rds_client.zone()
        LOG.debug('\n%s', response)

        LOG.debug('\n\n\nSample 19: subnet List\n\n\n')

        response = rds_client.subnet()
        LOG.debug('\n%s', response)
        
        LOG.debug('\n\n\nSample 20: price\n\n\n')
        instance = model.Instance(engine='sqlserver', engine_version='2016', cpu_count=2, allocated_memory_in_g_b=8,
                                  allocated_storage_in_g_b=50, category='Singleton', disk_io_type='cloud_enha')
        duration = 1
        number = 1
        product_type = "prepay"
        response = rds_client.price_instance(instance=instance, duration=duration, number=number,
                                             product_type=product_type)
        LOG.debug('\n%s', response)
       
        # suspend instance
        LOG.debug('\n\n\nSample 21: suspend Instance\n\n\n')
        instance_id = "rds-cteusMhZ"
        response = rds_client.suspend_instance(instance_id=instance_id)
        LOG.debug('\n%s', response)
        
        # start instance
        LOG.debug('\n\n\nSample 21: suspend Instance\n\n\n')
        instance_id = "rds-cteusMhZ"
        response = rds_client.start_instance(instance_id=instance_id)
        LOG.debug('\n%s', response)

        order_id = "订单id"
        response = rds_client.order_status(order_id=order_id)
        LOG.debug('\n%s', response)

        duration = 1
        instance_ids=["rds-cteusMhZ"]
        response = rds_client.renew_instance(duration=duration, instance_ids=instance_ids)
        LOG.debug('\n%s', response)
        

        maintain_start_time = "19:00:00"
        maintain_duration= 1
        instance_id = "rds-cteusMhZ"
        response = rds_client.maintaintime_instance(instance_id=instance_id,
                                                    maintain_duration=maintain_duration,
                                                    maintain_start_time=maintain_start_time)
        LOG.debug('\n%s', response)


        response = rds_client.task_instance()
        LOG.debug('\n%s', response)

    except ex.BceHttpClientError as e:
        if isinstance(e.last_error, ex.BceServerError):
            LOG.error('send request failed. Response %s, code: %s, request_id: %s'
                      % (e.last_error.status_code, e.last_error.code, e.last_error.request_id))
            LOG.error('send request failed. exception: %s' % e)
        else:
            LOG.error('send request failed. Unknown exception: %s' % e)
