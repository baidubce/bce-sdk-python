#!/usr/bin/env python
# coding: utf-8

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
Unit test for rds backup manager interface
"""

import sys
import unittest

from imp import reload

from test_rds_conf import config1
from test_rds_conf import config2
from baidubce.services.rds.custom.enums import rds_enum
from baidubce.services.rds import rds_backup_manager as backup_manager
from baidubce.services.rds.custom.requestparam import rds_request_param_object as request_param

if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')


class TestRdsBackupManager(unittest.TestCase):
    def setUp(self):
        self.instance_id = 'rds-rWLm6n4e'
        self.rds_client1 = backup_manager.RdsBackupManager(config1)
        self.rds_client2 = backup_manager.RdsBackupManager(config2)

    # 备份详情
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
        effective_time = rds_enum.EffectiveTime.IMMEDIATE

        # 备份类型，支持physical/snapshot， 取值为：snapshot，
        # 磁盘类型为ssd将不支持快照备份

        data_backup_type = rds_enum.BackupType.PHYSICAL
        # 这里是备份库的枚举类型
        data_base = rds_enum.BackUpObject.SCHEMA

        # 这里是备份库的名称
        database_name = "test_db"

        # 这里是备份表枚举类型
        database_table_type = rds_enum.BackUpObject.TABLE

        # 这里是备份表的名称
        database_table_name = "test_info"

        # 封装备份表对象--可以构建多个对象放入subTableObjectList中
        subTableObject = request_param.SubTableObject(database_table_type, database_table_name)

        # 封装备份表数象
        subTableObjectList = [subTableObject.to_json()]

        # 封装备份库表对象
        # dataBackUpObject = request_param.DataBackupObject(data_base, database_name, subTableObjectList)

        dataBackUpObject = request_param.DataBackupObject(data_base, database_name)

        dataBackupObjectList = [dataBackUpObject.to_json()]
        # 调用接口
        self.rds_client1.full_backup(instance_id, effective_time, data_backup_type, dataBackupObjectList)

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

    # 按时间点进行库表恢复（仅支持mysql实例）
    def test_restore_at_backup_in_time(self):
        # 源实例id
        instance_id = self.instance_id
        # 恢复的目标实例--如果此项为空则恢复源有实例也可以指定为源实例id
        target_instance_id = None
        # 备份时间点
        date_time = "2023-12-12T07:25:36Z"
        # 备份库的表的名称
        table_name = "test_tb_t"
        # 还原库的表名称
        newTable_name = "test_tb_t1"
        # 备份库还原表信息
        recovery_table = request_param.RecoveryToSourceInstanceTable(table_name, newTable_name)
        # 备份库还原表集合
        # recovery_table_list = [recovery_table.to_json()]
        # 为空时，传递None
        recovery_table_list = None
        # 备份表的类型
        restore_mode = rds_enum.BackRecoveryModel.DATABASE
        # 备份库的数据库名称
        db_name = "test_tb"
        # 还原库的数据库名称
        new_db_name = "test_tb1"
        # 要还原的数据库信息对象
        recovery_database = request_param.RecoveryToSourceInstance(db_name, new_db_name, restore_mode,
                                                                   recovery_table_list)
        # 还原数据库集合
        data = [recovery_database.to_json()]
        # 调用接口
        self.rds_client1.restore_at_backup_in_time(
            instance_id, date_time, data, target_instance_id)

    # 按备份集进行库表恢复（仅支持mysql实例）
    def test_restore_at_backup_in_snap_short(self):
        # 源实例id（请求路径专用）
        instance_id = self.instance_id
        # 恢复的目标实例--如果此项为空则恢复源有实例也可以指定为源实例id
        target_instance_id = None
        # 备份时候备份集id
        snapshot_id = "1702364656962520302"
        # 备份库的表的名称
        table_name = "test_tb_one"
        # 还原库的表名称
        newTable_name = "test_tb_on1"
        # 备份库还原表信息
        recovery_table = request_param.RecoveryToSourceInstanceTable(table_name, newTable_name)
        # 备份库还原表集合
        # recovery_table_list = [recovery_table.to_json()]
        # 为空时，传递None
        recovery_table_list = None
        # 备份表的类型
        restore_mode = rds_enum.BackRecoveryModel.DATABASE
        # 备份库的数据库名称
        db_name = "test_tb"
        # 还原库的数据库名称
        new_db_name = "test_tb1"
        # 要还原的数据库信息对象
        recovery_database = request_param.RecoveryToSourceInstance(db_name, new_db_name, restore_mode,
                                                                   recovery_table_list)
        # 还原数据库集合
        data = [recovery_database.to_json()]
        # 调用接口
        self.rds_client1.restore_at_backup_in_snap_short(instance_id, snapshot_id, data,
                                                         target_instance_id)


if __name__ == '__main__':
    unittest.main()
