
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
Unit tests for rds client.
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
from baidubce.services.rds import rds_model
from baidubce.services.rds import rds_client
from baidubce import compat
from imp import reload

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')
reload(sys)

if compat.PY2:
    sys.setdefaultencoding('utf8')
# sys.setdefaultencoding('utf-8')
HOST = b'http://rds.bj.baidubce.com'
AK = b''
SK = b''

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


class TestRdsClient(unittest.TestCase):
    """
    Test class for bcc sdk client
    """

    def setUp(self):
        config = BceClientConfiguration(credentials=BceCredentials(AK, SK),
                                        endpoint=HOST)
        self.client = rds_client.RDSClient(config)
        self.instance_id = 'rds-6f17R5R3'
        self.vpc_id = 'vpc-70pxg3pmv8rv'
        self.subnets = [
            rds_model.SubnetMap(u'cn-bj-d', u'sbn-dqafncqsy3y4')
        ]
        self.post_billing = rds_model.Billing(pay_method='Postpaid')
        self.engine = 'MySql'
        self.engine_version = '5.7'
        self.category = 'Standard'
        self.cpu_count = 1
        self.memory_capacity = 2
        self.volume_capacity = 100
        self.disk_io_type = 'cloud_enha'
        self.zone_name = ['cn-bj-d']
        config = BceClientConfiguration(credentials=BceCredentials(AK, SK),
                                        endpoint=HOST)
        self.rds_client1 = rds_client.RDSClient(config)

    def test_create_instance(self):
        # 设置实例名称
        instance_name = 'rds-py-create'
        # 支付方式
        billing = self.post_billing
        # 批量创建云数据库 RDS 实例个数, 最大不超过10个， 默认为1
        purchase_count = 1
        # 数据库类型
        engine = self.engine
        # 数据库版本
        engine_version = self.engine_version
        # 实例类别，basic：单机版本，Standard：双机高可用版本
        category = self.category
        # cpu 核数
        cpu_count = self.cpu_count
        # 内存大小 单位GB
        memory_capacity = self.memory_capacity
        # 磁盘大小 单位GB
        volume_capacity = self.volume_capacity
        # 磁盘类型，cloud_ssd：SSD云硬盘，cloud_essd：ESSD云硬盘，local_hdd_pro：本地
        disk_io_type = self.disk_io_type
        # vpc_id
        vpc_id = self.vpc_id
        # 是否直接付费 0：否，1：是
        is_direct_pay = bool(1)
        # 子网列表
        subnets = self.subnets
        zone_name = self.zone_name
        # 调用接口
        response = self.rds_client1.create_instance(instance_name=instance_name,
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
                                                    zone_names=zone_name,
                                                    is_direct_pay=is_direct_pay)
        # 设置实例节点id
        self.instance_id = response.instance_ids[0]

    def test_create_read_instance(self):
        # 设置只读实例名称
        instance_name = 'rds-py-create-read'
        # 主实例id
        source_instance_id = self.instance_id
        # 支付方式
        billing = self.post_billing
        # cpu 核数
        cpu_count = self.cpu_count
        # 内存大小 单位GB
        memory_capacity = self.memory_capacity
        # 磁盘大小 单位GB
        volume_capacity = self.volume_capacity
        # vpc_id
        vpc_id = self.vpc_id
        # 是否直接付费 0：否，1：是
        is_direct_pay = bool(1)
        # 子网列表
        subnets = self.subnets
        # 调用接口
        response = self.rds_client1.create_read_instance(instance_name=instance_name,
                                                         source_instance_id=source_instance_id,
                                                         billing=billing,
                                                         vpc_id=vpc_id,
                                                         is_direct_pay=is_direct_pay,
                                                         subnets=subnets,
                                                         cpu_count=cpu_count,
                                                         memory_capacity=memory_capacity,
                                                         volume_capacity=volume_capacity)
        # 设置只读节点id
        instance_read_id = response.instance_ids[0]

    def test_create_proxy_instance(self):
        # 创建代理实例
        instance_name = 'rds-py-create-proxy'
        # 主实例id
        source_instance_id = self.instance_id
        # 支付方式
        billing = self.post_billing
        # 节点数量
        node_amount = 2
        # vpc_id
        vpc_id = self.vpc_id
        # 是否直接付费 0：否，1：是
        is_direct_pay = bool(1)
        # 子网列表
        subnets = self.subnets
        # 调用接口
        response = self.rds_client1.create_proxy_instance(instance_name=instance_name,
                                                          source_instance_id=source_instance_id,
                                                          billing=billing,
                                                          vpc_id=vpc_id,
                                                          is_direct_pay=is_direct_pay,
                                                          subnets=subnets,
                                                          node_amount=node_amount)
        # 设置代理节点id
        instance_proxy_id = response.instance_ids[0]

    def test_instance_detail(self):
        # 实例详情
        response = self.rds_client1.get_instance_detail(self.instance_id)

    def test_instance(self):
        # 实例列表
        self.rds_client1.list_instances(max_keys=10)

    # 变配实例
    def test_resize_instance(self):
        # 实例id
        instance_id = self.instance_id
        # cpu 核数
        cpu_count = 1
        # 内存大小 单位GB
        memory_capacity = 4
        # 磁盘大小 单位GB
        volume_capacity = 100
        # node_amount = 4
        # 是否直接付费 0：否，1：是
        is_direct_pay = bool(1)
        # 调用接口
        self.rds_client1.resize_instance(instance_id=instance_id,
                                         cpu_count=cpu_count,
                                         memory_capacity=memory_capacity,
                                         volume_capacity=volume_capacity,
                                         is_direct_pay=is_direct_pay)

    # 重启实例
    def test_reboot_instance(self):
        # 调用接口
        self.rds_client1.reboot_instance(self.instance_id)

    # 更新实例名称
    def test_rename_instance(self):
        # 实例id
        instance_id = self.instance_id
        # 实例名称
        instance_name = "py-test"
        # 调用接口
        self.rds_client1.rename_instance(instance_id=instance_id,
                                         instance_name=instance_name)

    # 更新实例同步模式
    def test_modify_sync_mode_instance(self):
        # 实例id
        instance_id = self.instance_id
        # 同步模式（异步复制：Async，半同步复制：Semi_sync）
        sync_mode = "Semi_sync"
        # 调用接口
        self.rds_client1.modify_sync_mode_instance(instance_id=instance_id,
                                                   sync_mode=sync_mode)

    def test_modify_endpoint_instance(self):
        # 更新实例连接信息
        instance_id = self.instance_id
        # 地址
        address = "python"
        # 调用接口
        self.rds_client1.modify_endpoint_instance(instance_id=instance_id,
                                                  address=address)

    def test_modify_public_access_instance(self):
        # 更新实例公网访问状态
        instance_id = self.instance_id
        # 公网访问状态 0：关闭公网访问，1：开启公网访问
        public_access = bool(1)
        # 调用接口
        self.rds_client1.modify_public_access_instance(instance_id=instance_id,
                                                       public_access=public_access)

    # 实例开启自动续费
    def test_auto_renew_instance(self):
        # 实例id
        instance_ids = [self.instance_id]
        # 自动续费周期单位（年：year；月：month）
        auto_renew_time_unit = "month"
        # 续费周期按月（不超过9个月）按年付费（不超过3年）
        auto_renew_time = 1
        # 调用接口
        self.rds_client1.auto_renew_instance(instance_ids=instance_ids,
                                             auto_renew_time_unit=auto_renew_time_unit,
                                             auto_renew_time=auto_renew_time)

    # 查询可用区列表
    def test_zone_list(self):
        # 调用接口
        self.rds_client1.zone()

    # 查询查询子网列表
    def test_subnet_list(self):
        # 调用接口
        self.rds_client1.subnet()

    # 获取价格
    def test_price_instance(self):
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
        # 支付类型
        product_type = "prepay"
        # 调用接口
        self.rds_client1.price_instance(instance=instance,
                                        duration=duration,
                                        number=number,
                                        product_type=product_type)

    # 释放实例
    def test_delete_instance(self):
        # 调用接口
        self.rds_client1.delete_instance(self.instance_id)

    # 更新时间窗口
    def test_maintaintime_instance(self):
        # 实例id
        self.instance_id = "rds-6f17R5R3"
        # 实例维护时间窗口的持续时间，单位是小时，如：1；
        maintain_duration = 1
        # 维护时间
        maintain_start_time = "05:00:00"
        # 调用接口
        self.rds_client1.maintaintime_instance(self.instance_id, maintain_start_time, maintain_duration)

    def test_create_database(self):
        data = {
            "characterSetName": "utf8",
            "dbName": "test1234",
            "remark": "pysdk",
        }

        # 调用接口
        self.rds_client1.create_database(self.instance_id, data)

    # 获取数据库列表
    def test_query_database_list(self):
        # 调用接口
        self.rds_client1.query_database_list(self.instance_id)

    # 修改描述信息
    def test_update_database_remark(self):
        # postgresql 不支持修改备注
        # 数据库名称,由大小写字母、数字、下划线组成、字母开头，字母或数字结尾，最长64个字符
        db_name = "test_db"
        # 数据库备注
        remark = "123"
        # 调用接口
        self.rds_client1.update_database_remark(self.instance_id, db_name, remark)

    # 修改数据库端口
    def test_update_database_port(self):
        # 数据库端口（sqlserver、postgresql数据库端口不支持修改）
        db_port = 3306
        # 调用接口
        self.rds_client1.update_database_port(self.instance_id, db_port)

    # 删除数据库
    def test_delete_database(self):
        # 数据库名称,由大小写字母、数字、下划线组成、字母开头，字母或数字结尾，最长64个字符
        db_name = "test_db"
        # 调用接口
        self.rds_client1.delete_database(self.instance_id, db_name)

    def test_backup_detail(self):
        # 实例id
        instance_id = self.instance_id
        # 备份id
        backup_id = "1702325499881950802"
        # 调用接口
        self.rds_client1.backup_detail(instance_id, backup_id)

    # 备份列表
    def test_backup_list(self):
        # 实例id
        instance_id = self.instance_id
        # 查找内容
        marker = None
        # 每页条数
        max_keys = 10
        # 调用接口
        self.rds_client1.backup_list(instance_id, marker, max_keys)

    # 备份策略
    def test_modify_backup_policy(self):
        # 实例id
        instance_id = self.instance_id
        # 自动备份备份天数
        backup_days = "0,1,2,3,5,6"
        # 这里的时间是指的UTC时间，北京时间比UTC时间早8小时S
        backup_time = "20:00:00Z"
        # 是否持久化
        persistent = True
        # 备份保留天数
        expire_in_days = 7
        # 调用接口
        self.rds_client1.modify_backup_policy(instance_id, backup_days, backup_time, persistent,
                                              expire_in_days)

    # 全量备份
    def test_full_backup(self):
        # 实例id
        instance_id = self.instance_id

        # 窗口字段。操作执行方式，有两种取值：timewindow表示在时间窗口内执行，
        # immediate表示立即执行。
        # 默认为immediate
        effective_time = 'immediate'

        # 备份类型，支持physical/snapshot， 取值为：snapshot，
        # 磁盘类型为ssd将不支持快照备份

        data_backup_type = 'physical'
        # 这里是备份库的枚举类型
        data_base = 'schema'

        # 这里是备份库的名称
        database_name = "test_db"

        # 这里是备份表枚举类型
        database_table_type = 'table'

        # 这里是备份表的名称
        database_table_name = "test_info"
        # 调用接口
        self.rds_client1.full_backup(instance_id, effective_time, data_backup_type)

    # 删除指定备份
    def test_delete_specified_backup(self):
        # 实例id
        instance_id = self.instance_id
        # 备份id
        snapshot_id = "1701950306675099301"
        # 调用接口
        self.rds_client1.delete_specified_backup(instance_id, snapshot_id)

    # 获取binlog列表(仅支持mysql）
    def test_binlog_list(self):
        # 实例id
        instance_id = self.instance_id
        # 日志时间点
        date_time = "2023-12-08T16:00:00Z"
        # 调用接口
        self.rds_client1.binlog_list(instance_id, date_time)

    # 获取binlog信息(仅支持mysql）
    def test_binlog_detail(self):
        # 实例id
        instance_id = self.instance_id
        # binlog_id
        binlog_id = "1702137922451510901"
        # 下载有效时间，单位为秒，默认1800
        download_valid_time_in_sec = 1800
        # 调用接口
        self.rds_client1.binlog_detail(instance_id, binlog_id, download_valid_time_in_sec)

    def test_slow_log_detail(self):
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
        self.rds_client1.slow_log_detail(self.instance_id, start_time, end_time, page_no,
                                         page_size, db_name, host_ip, user_name, sql)

    # 错日志详情
    def test_error_log_detail(self):
        # 开始时间
        start_time = "2023-12-13T06:00:00Z"
        # 结束时间
        end_time = "2023-12-13T18:00:00Z"
        # 当前页码
        page_no = 3
        # 每页条数
        page_size = 10
        # 搜索关键词 ，模糊条件
        key_word = "test_name1"
        # 调用接口
        self.rds_client1.error_log_detail(self.instance_id, start_time, end_time,
                                          page_no, page_size, key_word)

    # 慢日志下载详情
    def test_slow_log_download_detail(self):
        # 慢日志id
        log_id = "slowlog.202312130005"
        # 下载有效时间（单位：秒)
        download_valid_time_in_sec = 1800
        # 调用接口
        self.rds_client1.slow_log_download_detail(self.instance_id, log_id,
                                                  download_valid_time_in_sec)

    # 错误日志下载详情
    def test_error_log_download_detail(self):
        # 慢日志id
        log_id = "errorlog.202312131549"
        # 下载有效时间（单位：秒)
        download_valid_time_in_sec = "1800"
        # 调用接口
        self.rds_client1.error_log_download_detail(self.instance_id, log_id,
                                                   download_valid_time_in_sec)
    def test_force_change_instance(self):
        # 热活实例组id
        group_id = 'self.group_id'
        # 需要切换的主角色的实例id
        leader_id = 'self.leader_id'
        # force：0 - 非故障（非故障状态时使用）1 - 故障
        force = 1
        # 最大允许备库Behind_Master值（0 表示要求备库和故障主库数据完全一致，
        # 建议业务从0开始逐步增加，直至最大容忍值，force=0时，该参数不生效 ）
        max_behind = 10
        # 调用接口
        self.rds_client1.force_change_instance(group_id, leader_id, force, max_behind)

    # 批量加入热活实例组
    def test_group_batch_join(self):
        # leader_id和 follower_ids 的 id都不加入任何实例组中慢，方可成功
        # 从角色短实例ids列表
        follower_ids = ['self.follower_id']
        # 热活实例组名称
        name = "test_hot_rds"
        # 主角色短实例id
        leader_id = 'self.leader_id'
        # 调用接口
        self.rds_client1.group_batch_join(follower_ids, name, leader_id)

    # 创建热活实例组
    def test_create_group(self):
        # 创建热活实例组名称
        name = "test_hot_rds"
        # 主角色短实例id
        leader_id = 'self.leader_id'
        # 调用接口
        self.rds_client1.create_group(name, leader_id)

    # 查询热活实例组列表（需要修改参数）
    def test_group_list(self):
        # 排序规则：asc(升序)/desc（降序）
        order = 'asc'
        # 排序字段
        order_by = "name"
        # 当前页数
        page_no = 1
        # 每页条数
        page_size = 10
        # 过滤字符串 从groupId、groupName、instanceStatus 三个key过滤
        # filter_map_str = "{\"groupId\":\"rdcqzga9i4s\"}"
        # filter_map_str = "{\"groupName\":\"acount-test\"}"
        # filter_map_str = "{\"instanceStatus\":\"topoModifying\"}"
        filter_map_str = None
        # 截止日期
        days_to_expiration = -1
        # 调用接口
        self.rds_client1.group_list(order, order_by, page_no, page_size, filter_map_str,
                                    days_to_expiration)

    # 热活实例组详情
    def test_detail_group(self):
        # 热活实例组id
        group_id = 'self.group_id'
        # 调用接口
        self.rds_client1.detail_group(group_id)

    # 实例组前置检查（GTID检查）
    def test_check_gtid_group(self):
        # 短实例id
        instance_id = 'self.follower_id'
        # 调用接口
        self.rds_client1.check_gtid_group(instance_id)

    # 实例组前置检查（实例连通性检查）
    # 双角色id不在任何实例组中，且在同一地域，返回结果才是true
    def test_check_ping_group(self):
        # source_id实例短id
        source_id = 'self.leader_id'
        # target_id实例短id
        target_id = 'self.follower_id'
        # 调用接口
        self.rds_client1.check_ping_group(source_id, target_id)

    # 实例组前置检查（数据检查）
    # 双角色id不在任何实例组中，且在同一地域，返回结果才是true
    def test_check_data_group(self):
        # 实例短id
        instance_id = 'self.leader_id'
        # 调用接口
        self.rds_client1.check_data_group(instance_id)

    # 加入某个实例组
    def test_add_instance_to_group(self):
        # 热活实例组的id
        group_id = 'self.group_id'
        # 从角色短实例id
        follower_id = 'self.follower_id'
        # 调用接口
        self.rds_client1.add_instance_to_group(group_id, follower_id)

    # 修改热活实例组名称
    def test_modify_instances_group_name(self):
        # 修改热活实例组的id
        group_id = 'self.group_id'
        # 修改的热活实例组名称
        group_name = "test_hot_rds_group"
        # 调用接口
        self.rds_client1.modify_instances_group_name(group_id, group_name)

    # 删除热活实例组
    def test_delete_instances_group(self):
        # 热活实例组id
        group_id = 'self.group_id'
        # 调用接口
        self.rds_client1.delete_instances_group(group_id)

    # 主角色变更
    def test_master_role_change(self):
        # 热活实例组id
        group_id = 'self.group_id'
        # 主角色短实例id
        leader_id = 'self.leader_id'
        # 调用接口
        self.rds_client1.master_role_change(group_id, leader_id)

    # 退出某个实例组
    def test_quit_instance_to_group(self):
        # 热活实例组id
        group_id = 'self.group_id'
        # 退出热活实例组中的短实例id
        instance_id = 'self.follower_id'
        # 调用接口
        self.rds_client1.quit_instances_group(group_id, instance_id)

    # 小版本前置检查
    def test_check_min_version(self):
        # 主角色短实例id
        leader_id = 'self.leader_id'
        # 从角色短实例id
        follower_id = 'self.follower_id'
        # 调用接口
        self.rds_client1.check_min_version(leader_id, follower_id)

    def test_parameter_list(self):
        # 搜索参数关键字，可以为空，非必须传
        keyword = None
        # keyword = "wait_timeout"
        # 调用接口
        self.rds_client1.parameter_list(self.instance_id, keyword)

    # 修改配置参数
    def test_modify_config_parameter(self):
        effective_time = 'immediate'
        # 参数名称
        parameter_name = "wait_timeout"
        # 参数值
        parameter_value = "86300"
        # 修改版本号，从获取参数列表的返回结果项中的etag字段获取
        e_tag = "v6"
        ParameterList = [
            {"name": "wait_timeout",
             "value": "86300",
             "etag": e_tag,
             "applyMethod": "immediate"
         }]
        # 调用接口
        self.rds_client1.modify_config_parameter(self.instance_id, e_tag, effective_time,
                                                 ParameterList)

    # 查询修改参数历史
    def test_query_modify_parameter_history_list(self):
        # 实例id
        instance_id = self.instance_id
        # 调用接口
        self.rds_client1.query_modify_parameter_history_List(instance_id)

    # 查询参数模板列表
    def test_query_parameter_template_list(self):
        # 当前页数
        page_no = 1
        # 每页条数
        page_size = 10
        # 模板类型，支持user/system，不传默认为user。user：返回自定义参数列表；
        # system：返回系统参数列表
        template_type = 'user'
        # 数据库引擎 支持MySQL (驼峰命名）
        # db_type = None
        db_type = 'MySQL'
        # 数据库版本 如：mysql(5.0, 5.6, 5.7, 8.0)等
        db_version = '5.7'
        # db_version = None
        # 调用接口
        self.rds_client1.query_parameter_template_list(page_no, page_size, template_type, db_type,
                                                       db_version)

    # 查询参数模板详情
    def test_query_parameter_detail(self):
        # 模版id
        template_id = "503"
        # 调用接口
        self.rds_client1.query_parameter_template_detail(template_id)

    # 复制参数模版
    def test_copy_parameter_template(self):
        # 模版名称
        name = "503_template_copy"
        # 模版描述
        desc = ""
        # 模板id
        template_id = "503"
        # 调用接口
        self.rds_client1.copy_parameter_template(template_id, name, desc)

    def test_recycler_list(self):
        # 调用接口
        self.rds_client1.recycler_list()

    # 从回收站恢复实例（单个、批量均通过同一个接口）
    def test_recycler_recover(self):
        # 从回收站恢复的实例id，多个用英文逗号分隔开
        instance_ids = ["rds-dWRnnVn9", "rds-V9Crmhez"]
        # 调用接口
        self.rds_client1.recycler_recover(instance_ids)

    # 从回收站中释放单个实例
    def test_delete_recycler(self):
        # 从回收站释放单个实例id
        instance_id = self.instance_id
        # 调用接口
        self.rds_client1.delete_recycler(instance_id)

    def test_whit_list(self):
        # 调用接口
        self.rds_client1.get_white_list(self.instance_id)

    # 更新白名单
    def test_update_whit_list(self):
        # 创建白名单
        security_ips = ['127.0.0.1']
        # 修改版本号, 这个参数值是从查询白名单的返回头域字段x-bce-if-match获取
        # 或者从返回结果的etag字段获取
        e_tag = "v1"
        # 调用接口
        self.rds_client1.update_white_list(self.instance_id, security_ips, e_tag)

    # 设置SSL状态
    def test_set_ssl_status(self):
        # 实例id
        instance_id = self.instance_id
        # 公网状态
        status = False
        # 调用接口
        self.rds_client1.get_ssl_status(instance_id, status)

    # 获取ca证书
    def test_obtain_ssl_ca(self):
        # 调用接口
        self.rds_client1.obtain_ssl_ca()

    # 查询任务列表
    def test_instance_task(self):
        # 调用接口
        self.rds_client1.task_instance()

    def test_create_readonly_group(self):
        # 实例id
        instance_id = self.instance_id
        # vpcId
        vpc_id = "vpc-70pxg3pmv8rv"
        # 子网Id
        subnet_id = "sbn-dqafncqsy3y4"
        # 只读组名称（可选参数）
        ro_group_name = "test_name_group"
        # 是否启用延迟剔除，默认为关闭（可选参数）
        enable_delay_off = True
        # 组内最少保留实例数目，取值为0~5之间的整数。默认为1（可选参数）
        least_app_amount = 5
        # 是否启用重新负载均衡开关（可选参数）
        balance_reload = True
        # 分配到共享集群还是专属集群（可选参数）
        bgw_group_exclusive = False
        # 集群id（可选参数）
        bgw_groupId = None
        # 服务端口,MySQL默认为3306（可选参数）
        entry_port = 3306
        # 内网ip（可选参数，建议获取同一个子网的内网IP，否则创建后在控制台不可见）
        vnet_ip = None
        # 延迟阈值，取值为大于等于0的整数，默认为10（可选参数）
        delay_threshold = 11
        # 调用接口
        self.rds_client1.create_readonly_group(instance_id,
                                               vpc_id,
                                               subnet_id,
                                               ro_group_name,
                                               enable_delay_off,
                                               least_app_amount,
                                               balance_reload,
                                               bgw_group_exclusive,
                                               bgw_groupId,
                                               entry_port,
                                               vnet_ip,
                                               delay_threshold
                                               )

    # 只读组详情
    def test_readonly_group_detail(self):
        # 实例id
        instance_id = self.instance_id
        # 只读组id
        ro_group_id = "rdsmrg-rn6xw3h2"
        # 调用接口
        self.rds_client1.readonly_group_detail(instance_id, ro_group_id)

    # 只读实例组列表
    def test_master_instance_associated_readonly_List(self):
        # 实例id
        instance_id = self.instance_id
        # 调用接口
        self.rds_client1.master_instance_associated_readonly_List(instance_id)

    # 加入只读组
    def test_join_readonly_group(self):
        # 实例id
        instance_id = self.instance_id
        # 只读组id
        ro_group_id = "rdsmrg-rn6xw3h2"
        # 只实例短id或者长id都可以
        app_id = "rds-ewfD4Bts"
        # 只实例短id
        app_id_short = "rds-ewfD4Bts"
        # app_name
        app_name = "test"
        # 权重
        weight = 1

        # 主实例id
        source_app_id = "rds-rWLm6n4e"
        # 只读实例状态
        status = "available"
        # 创建时间
        create_time = "2023-12-11T15:15:00Z"
        # 更新时间
        update_time = "2023-12-11T15:15:00Z"
        # 只读组状态
        app_status = "online"

        readReplicaList =  [
            {
                "appId": "rds-wI2F7KOC",
                "appName": "mysql56",
                "weight": 50,
                "roGroupId": "rdsmrg-s71pji95",
                "sourceAppId": "rdsmap2ojzds5od",
                "status": "online",
                "createTime": "2021-09-20 11:00:31",
                "updateTime": "2021-09-20 11:00:31",
                "appStatus": "available",
                "appIdShort": "rds-wI2F7KOC"
            }
        ]
        # 调用接口
        self.rds_client1.join_readonly_group(instance_id, ro_group_id,
                                             readReplicaList)

    # 负载重新均衡
    def test_readonly_group_load_balance(self):
        # 实例id
        instance_id = self.instance_id
        # 只读组id
        ro_group_id = "rdsmrg-x0r5ed2e"
        # 调用接口
        self.rds_client1.readonly_group_load_balance(instance_id, ro_group_id)

    # 批量修改只读组名称、延迟剔除开关、延迟阈值、重新负载均衡开关、组内只读实例权重。
    def test_batch_modify_readonly_group_properties(self):
        # 实例id
        instance_id = self.instance_id
        # 只读组id
        ro_group_id = "rdsmrg-x0r5ed2e"
        # 只读组名称（可选参数）
        ro_group_name = None
        # 只读组的延迟自动剔除开关（可选参数）
        enable_delay_off = False
        # 延迟阈值，取值为大于等于0的整数，范围1-2147483646,enable_delay_off开启有效（可选参数）
        delay_threshold = 90
        # 只读组的重新负载均衡开关（可选参数）
        balance_reload = None
        # 组内最少保留实例数目，取值为0~5之间的整数。默认为1（可选参数）
        least_app_amount = None
        # 只读实例id
        app_id = "rds-ewfD4Bts"
        readReplicaList = [
            {
                "appId": "rdsmbjfibahi3mc",
                "weight": 22
            }
        ]
        # 调用接口
        self.rds_client1.batch_modify_readonly_group_properties(instance_id,
                                                                ro_group_id,
                                                                ro_group_name,
                                                                enable_delay_off,
                                                                delay_threshold,
                                                                balance_reload,
                                                                least_app_amount,
                                                                readReplicaList)

    # 只读组开启/关闭公网
    def test_update_publicly_accessible(self):
        # 实例id
        instance_id = self.instance_id
        # 只读组id
        ro_group_id = "rdsmrg-x0r5ed2e"
        # 是否开启状态，true：开启，false：关闭
        publicly_accessible = False
        # 调用接口
        self.rds_client1.update_publicly_accessible(instance_id, ro_group_id,
                                                    publicly_accessible)

    # 只读组修改连接信息
    def test_update_endpoint(self):
        # 实例id
        instance_id = self.instance_id
        # 只读组id
        ro_group_id = "rdsmrg-x0r5ed2e"
        # 只读组名，（可选参数）
        ro_group_name = "test_name"
        # 组内最少保留实例数目，取值为0~5之间的整数。默认为1，（可选参数）
        least_app_amount = 1
        # 延迟阈值，取值为大于等于0的整数，默认为10（可选参数）
        delay_threshold = 10
        # 连接信息，address必填,其他参数选填
        endpoint = {
                "address":"rdsmrg",
                "port":3306,
                "inetIp":"113.24.230.172",
                "vnetIp":"192.168.0.62"
        }
        # 调用接口
        self.rds_client1.update_endpoint(instance_id,
                                         ro_group_id,
                                         endpoint,
                                         ro_group_name,
                                         least_app_amount,
                                         delay_threshold)

    # 只读实例离开只读组（离开字读组后，只读组没有只读实例，将自动删除只读组）
    def test_level_readonly_group(self):
        # 实例id
        instance_id = self.instance_id
        # 只读组id
        ro_group_id = "rdsmrg-x0r5ed2e"
        # 要离开的只读实例id列表 ,多个逗号分隔
        read_replica_list = ["rds-ewfD4Bts"]
        # 调用接口
        self.rds_client1.level_readonly_group(instance_id, ro_group_id,
                                              read_replica_list)

    # 删除只读组
    def test_delete_readonly_group(self):
        # 实例id
        instance_id = self.instance_id
        # 只读组id
        ro_group_id = "rdsmrg-zyhrfm3j"
        # 调用接口
        self.rds_client1.delete_readonly_group(instance_id, ro_group_id)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    # suite.addTest(TestRdsClient("test_create_instance"))
    # suite.addTest(TestRdsClient("test_create_read_instance"))
    # suite.addTest(TestRdsClient("test_create_proxy_instance"))
    suite.addTest(TestRdsClient("test_instance_detail"))
    # suite.addTest(TestRdsClient("test_instance"))
    # suite.addTest(TestRdsClient("test_resize_instance"))
    # suite.addTest(TestRdsClient("test_reboot_instance"))
    # suite.addTest(TestRdsClient("test_rename_instance"))
    # suite.addTest(TestRdsClient("test_modify_sync_mode_instance"))
    # suite.addTest(TestRdsClient("test_modify_endpoint_instance"))
    # suite.addTest(TestRdsClient("test_modify_public_access_instance"))
    # suite.addTest(TestRdsClient("test_auto_renew_instance"))
    # suite.addTest(TestRdsClient("test_zone_list"))
    # suite.addTest(TestRdsClient("test_subnet_list"))
    # suite.addTest(TestRdsClient("test_price_instance"))
    # suite.addTest(TestRdsClient("test_delete_instance"))
    suite.addTest(TestRdsClient("test_maintaintime_instance"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
