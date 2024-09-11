#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions
# and limitations under the License.

"""
Sample for rds example.
"""

import os
import sys
import logging

from imp import reload

import rds_sample_conf
import baidubce.exception as ex
from baidubce.services.rds import rds_model
from baidubce.services.rds.rds_client import RDSClient


if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')

logging.basicConfig(level=logging.DEBUG, filename='./rds_sample.log', filemode='w')
LOG = logging.getLogger(__name__)
CONF = rds_sample_conf


if __name__ == '__main__':
    # create a rds client
    rds_client = RDSClient(rds_sample_conf.config)
    try:
        # create instance
        LOG.debug('\n\n\nSample 1: Create Instance\n\n\n')
        # 实例名称
        instance_name = 'rds-py-create'
        # 付费方式
        billing = rds_model.Billing(pay_method='Postpaid')
        # 批量创建云数据库 RDS 实例个数, 最大不超过10个， 默认为1
        purchase_count = 1
        # 数据库类型
        engine = 'MySql'
        # 数据库版本
        engine_version = '5.7'
        # 实例类型 Standard：双机高可用，basic：单机版
        category = 'Standard'
        # cpu 核数
        cpu_count = 1
        # 内存大小 单位 GB
        memory_capacity = 2
        # 磁盘大小 单位 GB
        volume_capacity = 100
        # 磁盘类型
        disk_io_type = 'cloud_enha'
        # vpc_id
        vpc_id = 'vpc-70pxg3pmv8rv'
        # 是否直接付费 0：否，1：是
        is_direct_pay = bool(1)
        # 子网列表
        subnets = [
            {
                "zoneName": "cn-bj-d",
                "subnetId": "sbn-dqafncqsy3y4"
            }
        ]
        zoneNames=["cn-bj-d"]

        # 调用接口
        response = rds_client.create_instance(instance_name=instance_name,
                                              billing=billing,
                                              purchase_count=purchase_count,
                                              engine=engine,
                                              engine_version=engine_version,
                                              category=category,
                                              cpu_count=cpu_count,
                                              memory_capacity=memory_capacity,
                                              volume_capacity=volume_capacity,
                                              disk_io_type=disk_io_type,
                                              vpc_id=vpc_id,
                                              subnets=subnets,
                                              zone_names=zoneNames,
                                              is_direct_pay=is_direct_pay)
        # 日志输出
        LOG.debug('create instance is %s\n', response)
        # create readReplica instance
        LOG.debug('\n\n\nSample 2: Create readReplica Instance\n\n\n')
        # 只读实例名称
        instance_name = 'rds-py-create-read'
        # 主实例ID
        source_instance_id = 'rds-6I57IUIn'
        # 付费方式
        billing = rds_model.Billing(pay_method='Postpaid')
        # cpu 核数
        cpu_count = 1
        # 内存大小 单位 GB
        memory_capacity = 2
        # 磁盘大小 单位 GB
        volume_capacity = 100
        # vpc_id
        vpc_id = 'vpc-70pxg3pmv8rv'
        # 是否直接付费 0：否，1：是
        is_direct_pay = bool(1)
        # 子网列表
        subnets = [
            rds_model.SubnetMap(u'cn-bj-d', u'sbn-dqafncqsy3y4')
        ]
        # 调用接口
        response = rds_client.create_read_instance(
            instance_name=instance_name,
            source_instance_id=source_instance_id,
            billing=billing,
            vpc_id=vpc_id,
            is_direct_pay=is_direct_pay,
            subnets=subnets,
            cpu_count=cpu_count,
            memory_capacity=memory_capacity,
            volume_capacity=volume_capacity)
        # 日志输出
        LOG.debug('create read replica intance %s\n', response)

        # create proxy instance
        LOG.debug('\n\n\nSample 3: Create proxy Instance\n\n\n')
        # 代理实例名称
        instance_name = 'rds-py-create-proxy'
        # 主实例id
        source_instance_id = 'rds-6fGKPL1O'
        # 付费方式
        billing = rds_model.Billing(pay_method='Postpaid')
        # 代理节点数
        node_amount = 2
        # vpc_id
        vpc_id = 'vpc-ph7237ym686c'
        # 是否直接付费 0：否，1：是
        is_direct_pay = bool(1)
        # 子网列表
        subnets = [
            rds_model.SubnetMap(u'cn-bj-d', u'sbn-p1va817v3qn0')
        ]
        # 调用接口
        response = rds_client.create_proxy_instance(instance_name=instance_name,
                                                    source_instance_id=source_instance_id,
                                                    billing=billing,
                                                    vpc_id=vpc_id,
                                                    is_direct_pay=is_direct_pay,
                                                    subnets=subnets,
                                                    node_amount=node_amount)
        # 日志输出
        LOG.debug('\n%s', response)

        # list instances
        LOG.debug('\n\n\nSample 5: List Instance\n\n\n')
        # 调用接口
        response = rds_client.list_instances(max_keys=10)
        # 日志输出
        LOG.debug('list response is %s\n', response)

        # get instance detail
        LOG.debug('\n\n\nSample 4: Get Instance Detail\n\n\n')
        # 调用接口
        response = rds_client.get_instance_detail("rds-39wL4xtZ")
        # 日志输出
        LOG.debug('instance detail is %s\n', response)

        # resize instance
        LOG.debug('\n\n\nSample 6: Resize Instance\n\n\n')
        # 实例id
        instance_id = 'rds-6I57IUIn'
        # cpu 核数
        cpu_count = 1
        # 内存大小 单位 GB
        memory_capacity = 2
        # 磁盘大小 单位 GB
        volume_capacity = 100
        # node_amount = 4
        # 是否直接付费 0：否，1：是
        is_direct_pay = bool(1)
        # 调用接口
        response = rds_client.resize_instance(
            instance_id=instance_id,
            cpu_count=cpu_count,
            memory_capacity=memory_capacity,
            volume_capacity=volume_capacity,
            is_direct_pay=is_direct_pay)
        # 日志输出
        LOG.debug('Resize Instance %s \n', response)

        # delete instance
        LOG.debug('\n\n\nSample 7: delete Instance\n\n\n')
        # 调用接口
        response = rds_client.delete_instance("rds-7xnVLzpb")
        # 日志输出
        LOG.debug('delete Instance %s\n', response)

        # reboot instance
        LOG.debug('\n\n\nSample 8: Reboot Instance\n\n\n')
        # 调用接口
        response = rds_client.reboot_instance("rds-30mXTKjC")
        # 日志输出
        LOG.debug('reboot instance id is : %s\n', response)

        # rename instance
        LOG.debug('\n\n\nSample 9: Rename Instance\n\n\n')
        # 实例id
        instance_id = "rds-cteusMhZ"
        # 实例名称
        instance_name = "py-test"
        # 调用接口
        response = rds_client.rename_instance(instance_id=instance_id,
                                              instance_name=instance_name)
        # 日志输出
        LOG.debug('\n%s', response)

        # modifySyncMode instance
        LOG.debug('\n\n\nSample 10: ModifySyncMode Instance\n\n\n')
        # 实例id
        instance_id = "rds-cteusMhZ"
        # 同步模式（异步复制：Async，半同步复制：Semi_sync）
        sync_mode = "Semi_sync"
        # 调用接口
        response = rds_client.modify_sync_mode_instance(instance_id=instance_id,
                                                        sync_mode=sync_mode)
        # 日志输出
        LOG.debug('\n%s', response)

        # modifyEndpoint instance
        LOG.debug('\n\n\nSample 11: modifyEndpoint Instance\n\n\n')
        # 实例id
        instance_id = "rds-cteusMhZ"
        # 地址
        address = "python"
        # 调用接口
        response = rds_client.modify_endpoint_instance(instance_id=instance_id,
                                                       address=address)
        # 日志输出
        LOG.debug('\n%s', response)

        # modifyPublicAccess instance
        LOG.debug('\n\n\nSample 12: modifyPublicAccess Instance\n\n\n')
        # 实例id
        instance_id = "rds-cteusMhZ"
        # 公网访问状态 0：关闭，1：开启
        public_access = bool(1)
        # 调用接口
        response = rds_client.modify_public_access_instance(instance_id=instance_id,
                                                            public_access=public_access)
        # 日志输出
        LOG.debug('\n%s', response)

        # autoRenew instance
        LOG.debug('\n\n\nSample 13: autoRenew Instance\n\n\n')
        # 实例id 数组
        instance_ids = ["rds-cteusMhZ"]
        # 自动续费周期单位 （年：year；月：month）
        auto_renew_time_unit = "month"
        # 续费周期按月（不超过9个月）按年付费（不超过3年）
        auto_renew_time = 1
        # 调用接口
        response = rds_client.auto_renew_instance(instance_ids=instance_ids,
                                                  auto_renew_time_unit=auto_renew_time_unit,
                                                  auto_renew_time=auto_renew_time)
        # 日志输出
        LOG.debug('\n%s', response)

        LOG.debug('\n\n\nSample 14: zone List\n\n\n')
        # 调用接口
        response = rds_client.zone()
        # 日志输出
        LOG.debug('\n%s', response)

        LOG.debug('\n\n\nSample 15: subnet List\n\n\n')
        # 调用接口
        response = rds_client.subnet()
        # 日志输出
        LOG.debug('\n%s', response)

        LOG.debug('\n\n\nSample 16: price\n\n\n')
        # 实例
        instance = rds_model.Instance(engine='MySQL',
                                               engine_version='5.7',
                                               cpu_count=2,
                                               allocated_memory_in_g_b=8,
                                               allocated_storage_in_g_b=50,
                                               category='Singleton',
                                               disk_io_type='cloud_enha')
        # 时长。支付方式为后支付时不需要设置，预支付时必须设置。时间单位默认为month。
        duration = 1
        # 购买数量，默认值为1。
        number = 1
        # 实例类型
        product_type = "prepay"
        # 调用接口
        response = rds_client.price_instance(instance=instance,
                                             duration=duration,
                                             number=number,
                                             product_type=product_type)
        # 日志输出
        LOG.debug('\n%s', response)

        # suspend instance
        LOG.debug('\n\n\nSample 17: suspend Instance\n\n\n')
        # 实例id
        instance_id = "rds-cteusMhZ"
        # 调用接口
        response = rds_client.suspend_instance(instance_id=instance_id)
        # 日志输出
        LOG.debug('\n%s', response)

        # start instance
        LOG.debug('\n\n\nSample 18: start instance\n\n\n')
        # 实例id
        instance_id = "rds-cteusMhZ"
        # 调用接口
        response = rds_client.start_instance(instance_id=instance_id)
        # 日志输出
        LOG.debug('\n%s', response)

        LOG.debug('\n\n\nSample 19: order status\n\n\n')
        order_id = "订单id"
        # 调用接口
        response = rds_client.order_status(order_id=order_id)
        # 日志输出
        LOG.debug('\n%s', response)

        LOG.debug('\n\n\nSample 20: renew instance\n\n\n')
        # 续费周期，单位为月
        duration = 1
        instance_ids = ["rds-cteusMhZ"]
        # 调用接口
        response = rds_client.renew_instance(duration=duration,
                                             instance_ids=instance_ids)
        # 日志输出
        LOG.debug('\n%s', response)

        LOG.debug('\n\n\nSample 21: maintaintime instance\n\n\n')
        # 更新窗口执行时间
        maintain_start_time = "19:00:00"
        # 实例维护时间窗口的持续时间，单位是小时，如：1；
        maintain_duration = 1
        # 实例id
        instance_id = "rds-7xabvFUH"
        # 调用接口
        response = rds_client.maintaintime_instance(instance_id=instance_id,
                                                    maintain_duration=maintain_duration,
                                                    maintain_start_time=maintain_start_time)
        # 日志输出
        LOG.debug('\n%s', response)

        # 2.database manager
        LOG.debug('\n\n\nSample 1: delete database\n\n\n')
        # 数据库名称,由大小写字母、数字、下划线组成、字母开头，字母或数字结尾，最长64个字符
        db_name = "db_test2"
        # 调用接口
        response = rds_client.delete_database("rds-6I57IUIn", db_name)
        # 日志输出
        LOG.debug('delete database %s \n', response)

        # create_database
        LOG.debug('\n\n\nSample 2: create_database\n\n\n')
        body = {
              "characterSetName":"utf8",
              "dbName":"test1234",
              "remark":"pysdk",
        }
        response = rds_client.create_database("rds-uhZ8GPAr", body)
        # 日志输出
        LOG.debug('\n%s', response)

        LOG.debug('\n\n\nSample 3: slow log detail\n\n\n')
        # 开始时间
        start_time = "2023-12-10T09:50:04Z"
        # 结束时间
        end_time = "2023-12-10T09:59:04Z"
        # 当前页数
        page_no = 1
        # 每页条数
        page_size = 10
        # 数据库名称，数组
        db_name = []
        # IP地址，数组
        host_ip = ["127.0.0.1"]
        # 用户名，数组
        user_name = ["test_name1"]
        # SQL语句 ，模糊条件
        sql = "select"
        # 调用接口
        response = rds_client.slow_log_detail('rds-uhZ8GPAr', start_time, end_time, page_no,
                                         page_size, db_name, host_ip, user_name, sql)
        LOG.debug('\n%s', response)

        LOG.debug('\n\n\nSample 3.1: slow log download detail\n\n\n')
        # 慢日志id
        log_id = "slowlog.202408220005"
        # 下载有效时间（单位：秒)
        download_valid_time_in_sec = 1800
        # 调用接口
        response = rds_client.slow_log_download_detail('rds-uhZ8GPAr', log_id,
                                                  download_valid_time_in_sec)
        LOG.debug('\n%s', response)

        LOG.debug('\n\n\nSample 4: slow log list\n\n\n')
        # 慢日志时间点
        datetime = '2024-08-21T19:48:05Z'
        # 调用接口
        response = rds_client.error_log_list('rds-jHqrZCEk', datetime)
        LOG.debug('\n%s', response)

        # query_database_list
        LOG.debug('\n\n\nSample 3: query database list\n\n\n')
        # 调用接口
        response = rds_client.query_database_list("rds-6I57IUIn")
        # 日志输出
        LOG.debug('query database list %s\n', response)
        # update_database_port
        LOG.debug('\n\n\nSample 4: update database port\n\n\n')
        # 数据库端口（sqlserver、postgresql数据库端口不支持修改）
        db_port = 3309
        # 调用接口
        response = rds_client.update_database_port("rds-6I57IUIn", db_port)
        # 日志输出
        LOG.debug('update database port %s \n', response)

        # update_database_remark
        LOG.debug('\n\n\nSample 5: update database remark\n\n\n')
        # postgresql 不支持修改备注(没有此功能）
        # 数据库名称,由大小写字母、数字、下划线组成、字母开头，字母或数字结尾，最长64个字符
        db_name = "db_test2"
        # 数据库备注
        remark = "test_db_remark_11"
        # 调用接口
        response = rds_client.update_database_remark("rds-6I57IUIn", db_name, remark)
        # 日志输出
        LOG.debug('update database remark %s \n', response)

        # 3. backup manager
        LOG.debug('\n\n\nSample 1: backup list\n\n\n')
        # 查找内容
        marker = None
        # 每页条数
        max_keys = 10
        # 调用接口
        response = rds_client.backup_list("rds-6f17R5R3", marker, max_keys)
        # 日志输出
        LOG.debug('\n%s', response)

        # backup detail
        LOG.debug('\n\n\nSample 2: backup detail\n\n\n')
        # 备份id
        backup_id = "1723539961954444801"
        # 调用接口
        response = rds_client.backup_detail("rds-6f17R5R3", backup_id)
        # 日志输出
        LOG.debug('\n%s', response)

        # modify backup policy
        LOG.debug('\n\n\nSample 3: modify backup policy\n\n\n')
        # 自动备份备份天数
        backup_days = "5,6"
        # 这里的时间是指的UTC时间，北京时间比UTC时间早8小时S
        backup_time = "22:00:00Z"
        # 是否持久化
        persistent = True
        # 备份保留天数
        expire_in_days = 30
        # 调用接口
        response = rds_client.modify_backup_policy("rds-6f17R5R3", backup_days, backup_time, persistent,
                                                   expire_in_days)
        # 输出结果
        LOG.debug('\n%s', response)

        LOG.debug('\n\n\nSample 6: query parameter template list\n\n\n')
        # 当前页数
        page_no = 1
        # 每页条数
        page_size = 10
        # 模板类型，支持user/system，不传默认为user。user：返回自定义参数列表；system：返回系统参数列表
        template_type = 'user'
        # 数据库引擎 支持MySQL (驼峰命名）
        # db_type = None
        db_type = 'MySQL'
        # 数据库版本 如：mysql(5.0, 5.6, 5.7, 8.0)等
        db_version = '5.7'
        # db_version = None
        # 调用接口
        response = rds_client.query_parameter_template_list(page_no, page_size, template_type,
                                                            db_type, db_version)
        # 日志输出
        LOG.debug('\n%s', response)

        LOG.debug('\n\n\nSample 6.1: query white list\n\n\n')
        # 调用接口
        response = rds_client.get_white_list("rds-6f17R5R3")
        # 日志输出
        LOG.debug('\n%s', response)

        LOG.debug('\n\n\nSample 6.2: update white list\n\n\n')
        # 调用接口
        response = rds_client.update_white_list("rds-6f17R5R3", ["10.0.0.0/24", "192.168.0.0/16"], "v3")
        # 日志输出
        LOG.debug('\n%s', response)

        LOG.debug('\n\n\nSample 6.3: query white list\n\n\n')
        # 调用接口
        response = rds_client.get_white_list("rds-6f17R5R3")
        # 日志输出
        LOG.debug('\n%s', response)

        # full_backup
        LOG.debug('\n\n\nSample 5: binlog_list\n\n\n')
        # 查询时间
        date_time = "2023-12-08T16:00:00Z"
        # 调用接口
        response = rds_client.binlog_list(instance_id, date_time)
        # 日志输出
        LOG.debug('\n%s', response)

        # binlog_detail(仅支持mysql）
        LOG.debug('\n\n\nSample 6: binlog_detail\n\n\n')
        # binlog_id
        binlog_id = "1702137922451510901"
        # 下载有效时间，单位为秒，默认1800
        download_valid_time_in_sec = 1800
        # 调用接口
        response = rds_client.binlog_detail(instance_id, binlog_id, download_valid_time_in_sec)
        # 日志输出
        LOG.debug('\n%s', response)
    except ex.BceHttpClientError as e:
        if isinstance(e.last_error, ex.BceServerError):
            LOG.error('send request failed. Response %s, code: %s, request_id: %s'
                      % (e.last_error.status_code, e.last_error.code, e.last_error.request_id))
            LOG.error('send request failed. exception: %s' % e)
        else:
            LOG.error('send request failed. Unknown exception: %s' % e)

