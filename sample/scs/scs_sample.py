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

import scs_sample_conf
import baidubce.services.scs.scs_client as scs
import baidubce.exception as ex
from baidubce.services.scs import model

if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')

logging.basicConfig(level=logging.DEBUG, filename='./scs_sample.log', filemode='w')
LOG = logging.getLogger(__name__)
CONF = scs_sample_conf

if __name__ == '__main__':
    scs_client = scs.ScsClient(CONF.config)
    try:
        # create instance
        LOG.debug('\n\n\nSample 1: Create Instance\n\n\n')

        instance_name = 'redis-py-create'
        billing = model.Billing(pay_method='Postpaid')
        node_type = 'cache.n1.micro'
        shard_num = 1
        proxy_num = 0
        cluster_type = 'master_slave'
        replication_num = 2
        port = 7001
        engine_version = '3.2'
        vpc_id = 'vpc-sqq7nuryepat'
        subnets = [
            model.SubnetMap(u'cn-bj-d', u'sbn-p5xq05kxfhsp'),
            model.SubnetMap(u'cn-bj-a', u'sbn-w1tw0787su6d')
        ]
        response = scs_client.create_instance(instance_name=instance_name, billing=billing, node_type=node_type,
                                              shard_num=shard_num, proxy_num=proxy_num, cluster_type=cluster_type,
                                              replication_num=2, port=port, engine_version=engine_version,
                                              vpc_id=vpc_id, subnets=subnets)
        LOG.debug('\n%s', response)
        instance_id = response.instance_ids[0]

        # resize instance
        LOG.debug('\n\n\nSample 2: Resize Instance\n\n\n')
        response = scs_client.resize_instance(instance_id, 'cache.n1.small')
        LOG.debug('\n%s', response)

        # list instances
        LOG.debug('\n\n\nSample 3: List Instance\n\n\n')
        response = scs_client.list_instances(max_keys=2)
        LOG.debug('\n%s', response)

        # get instance detail
        LOG.debug('\n\n\nSample 4: Get Instance Detail\n\n\n')
        response = scs_client.get_instance_detail(str(instance_id))
        LOG.debug('\n%s', response)

        # rename instance
        LOG.debug('\n\n\nSample 5: Rename Instance\n\n\n')
        response = scs_client.rename_instance(instance_id, instance_name='redis-rename')
        LOG.debug('\n%s', response)

        # restart instance
        # LOG.debug('\n\n\nSample 6: Restart Instance\n\n\n')
        # response = scs_client.restart_instance(instance_id)
        # LOG.debug('\n%s', response)

        # clear instance data
        LOG.debug('\n\n\nSample 7: Clear Instance Data\n\n\n')
        response = scs_client.flush_instance(instance_id)
        LOG.debug('\n%s', response)

        # list available zone
        LOG.debug('\n\n\nSample 8: List Available Zone\n\n\n')
        response = scs_client.list_available_zones()
        LOG.debug('\n%s', response)

        # list subnet
        LOG.debug('\n\n\nSample 9: List Subnet\n\n\n')
        response = scs_client.list_subnets()
        LOG.debug('\n%s', response)

        # list node type
        LOG.debug('\n\n\nSample 10: List NodeType\n\n\n')
        response = scs_client.list_nodetypes()
        LOG.debug('\n%s', response)

        # bind tags
        LOG.debug('\n\n\nSample 11: Bind Tags\n\n\n')
        resp = scs_client.bind_tags(
            instance_id, [model.Tag(u'Usage', u'sample'), model.Tag(u'category', u'tags')]
        )
        LOG.debug('\n%s', response)

        # unbind tags
        LOG.debug('\n\n\nSample 12: Unbind Tags\n\n\n')
        resp = scs_client.unbind_tags(
            instance_id, [model.Tag(u'category', u'tags')]
        )
        LOG.debug('\n%s', response)

        # add security ips
        LOG.debug('\n\n\nSample 13: Add Security Ips\n\n\n')
        response = scs_client.add_security_ips(instance_id, ['192.168.1.3', '192.168.1.2'])
        LOG.debug('\n%s', response)

        # delete security ips
        LOG.debug('\n\n\nSample 14: Delete Security Ips\n\n\n')
        response = scs_client.delete_security_ips(instance_id, ['192.168.1.2'])
        LOG.debug('\n%s', response)

        # list security ips
        LOG.debug('\n\n\nSample 15: List Security Ips\n\n\n')
        response = scs_client.list_security_ip(instance_id)
        LOG.debug('\n%s', response)

        # modify password
        LOG.debug('\n\n\nSample 16: Modify Password\n\n\n')
        response = scs_client.modify_password(instance_id, 'password')
        LOG.debug('\n%s', response)

        # list parameter
        LOG.debug('\n\n\nSample 17: List Parameter\n\n\n')
        response = scs_client.list_parameters(instance_id)
        LOG.debug('\n%s', response)

        # modify parameter
        LOG.debug('\n\n\nSample 18: Modify Parameter\n\n\n')
        response = scs_client.modify_parameter(instance_id, 'appendonly', 'yes')
        LOG.debug('\n%s', response)

        # list backup
        LOG.debug('\n\n\nSample 19: List Backup\n\n\n')
        response = scs_client.list_backups(instance_id)
        LOG.debug('\n%s', response)

        # get backup detail
        LOG.debug('\n\n\nSample 20: Get Backup Details\n\n\n')
        backup_record_id = model.BackupRecord(model.Backup(response.backups[0]).records[0]).backup_record_id
        response = scs_client.get_backup(instance_id, backup_record_id)
        LOG.debug('\n%s', response)

        # modify backup policy
        LOG.debug('\n\n\nSample 21: Modify Backup Policy\n\n\n')
        response = scs_client.modify_backup_policy(instance_id, 'Mon,Thu',
                                                   '01:05:00', 5)
        LOG.debug('\n%s', response)

        # set as master
        # LOG.debug('\n\n\nSample 22: Set As Master\n\n\n')
        # response = scs_client.set_as_master(instance_id)
        # LOG.debug('\n%s', response)
        #
        # # set as slave
        # LOG.debug('\n\n\nSample 23: Set As Slave\n\n\n')
        # response = scs_client.set_as_slave(
        #     'scs-bj-aixanaiajitc',
        #     'redis.nacgbwtlxguv.scs.bj.baidubce.com',
        #     master_port=6379
        # )
        # LOG.debug('\n%s', response)

        # delete instance
        LOG.debug('\n\n\nSample 24: Delete Instance\n\n\n')
        response = scs_client.delete_instance(instance_id)
        LOG.debug('\n%s', response)

    except ex.BceHttpClientError as e:
        if isinstance(e.last_error, ex.BceServerError):
            LOG.error('send request failed. Response %s, code: %s, request_id: %s'
                      % (e.last_error.status_code, e.last_error.code, e.last_error.request_id))
        else:
            LOG.error('send request failed. Unknown exception: %s' % e)
