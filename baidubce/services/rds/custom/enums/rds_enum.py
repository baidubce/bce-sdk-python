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
 this is constant class
"""


class BackUpObject(object):
    """
    this is BackUpObject constant
    """
    SCHEMA = 'schema'
    TABLE = 'table'


class BackRecoveryModel(object):
    """
     this is BackRecoveryModel constant
    """
    DATABASE = 'database'
    TABLE = 'table'


class DbType(object):
    """
    this is DbType constant
    """
    MYSQL = 'MySQL'
    SQLSERVER = "sqlserver"
    POSTGRESQL = "postgresql"


class DBVersion(object):
    """
    this is DBVersion constant
    """
    # MYSQL
    MYSQL_55 = '5.5'
    MYSQL_56 = '5.6'
    MYSQL_57 = '5.7'
    MYSQL_80 = '8.0'
    # SQLSERVER
    SQLSERVER_2008_R2 = "2008r2"
    SQLSERVER_2012 = "2012"
    SQLSERVER_2016_SP1 = "2016sp1"
    # POSTGRESQL
    POSTGRESQL_10 = "10"
    POSTGRESQL_11 = "11"
    POSTGRESQL_12 = "12"
    POSTGRESQL_13 = "13"
    POSTGRESQL_14 = "14"
    POSTGRESQL_15 = "15"


class EffectiveTime(object):
    """
      this is EffectiveTime constant
    """
    TIMEWINDOW = "timewindow"
    IMMEDIATE = "immediate"


class BackupType(object):
    """
     this is BackupType constant
    """
    PHYSICAL = "physical"
    SNAPSHOT = "snapshot"


class AccountPrivileges(object):
    """
    this is AccountPrivileges constant
    """
    READ_ONLY = "ReadOnly"
    READ_WRITE = "ReadWrite"


class AccountType(object):
    """
    this is AccountType constant
    """
    COMMON = "Common"
    SUPER = "Super"


class AccountOwnershipInstance(object):
    """
    this is AccountOwnershipInstance constant
    """

    ONLY_MASTER = "OnlyMaster"
    RDS_PROXY = "RdsProxy"


class MYSQLCharSet(object):
    """
    this is MYSQLCharSet constant
    """
    UTF8 = "utf8"
    GBK = "gbk"
    LATIN1 = "latin1"
    UTF8M64 = "utf8mb4"


class SQLServerCharSet(object):
    """
    this is SQLServerCharSet constant
    """
    CHINESE_PRC_CI_AS = "Chinese_PRC_CI_AS"
    CHINESE_PRC_CS_AS = "Chinese_PRC_CS_AS"
    CHINESE_PRC_BIN = "Chinese_PRC_BIN"
    SQL_LATIN1_GENERAL_CP1_CI_AS = "SQL_Latin1_General_CP1_CI_AS"
    SQL_LATIN1_GENERAL_CP1_CS_AS = "SQL_Latin1_General_CP1_CS_AS"


class PostgresqlCharSet(object):
    """
    this is PostgresqlCharSet constant
    """
    UTF8 = "UTF8"
    SQL_ASCII = "SQL_ASCII"
    LATIN1 = "latin1"


class PostgresqlCTypeCharSet(object):
    """
     this is PostgresqlCTypeCharSet constant
    """
    ZH_CN_UTF8 = "zh_CN.utf-8"
    EN_US = "en_US"
    SQL_ASCII = "C"


class TemplateType(object):
    """
    this is TemplateType constant
    """
    USER = "user"
    SYSTEM = "system"


class Order(object):
    """
     this is Order constant
    """
    ASC = "asc"
    DESC = "desc"
