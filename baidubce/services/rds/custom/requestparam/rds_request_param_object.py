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
this is request object class
"""

from json import JSONEncoder


class RdsRequestParamObject(object):
    """
    this is request object no used
    """

    def __init__(self, request_param):
        self.request_param = request_param


class DataBackupObject(object):
    """
     this is request DataBackupObject
    """

    def __init__(self, backup_type, name, subObjects=None):
        """
        @param backup_type:
        @param name:
        @param subObjects:
        """

        super(DataBackupObject, self).__init__()
        # backup type is schema or table
        self.type = backup_type
        # backup type is schema or table name
        self.name = name
        # backup sub table list
        if subObjects is not None:
            self.subObjects = subObjects

    def to_json(self):
        """
         @return:
        """

        return self.__dict__


class SubTableObject(object):
    """
     this is request SubTableObject object
    """

    def __init__(self, backup_type, name):
        """
        @param backup_type:
        @param name:
        """

        super(SubTableObject, self).__init__()
        #  backup type is schema or table
        self.type = backup_type
        # backup type is schema or table name
        self.name = name

    def to_json(self):
        """
        @return:
        """

        return self.__dict__


class RecoveryToSourceInstance(object):
    """
     this is request RecoveryToSourceInstance object
    """

    def __init__(self, db_name, new_db_name, restore_mode, tables=None):
        """
        @param db_name:
        @param new_db_name:
        @param restore_mode:
        @param tables:
        """

        super(RecoveryToSourceInstance, self).__init__()
        self.dbName = db_name
        # need  Recovery table name
        self.newDbname = new_db_name
        # Recovery model
        self.restoreMode = restore_mode
        # Recovery tables collection objets
        if tables is not None:
            self.tables = tables

    def to_json(self):
        """
        @return:
        """

        return self.__dict__


class ApplyTemplate(object):
    """
     this is request ApplyTemplate object
    """

    def __init__(self, effective_time, switchover, instance_ids):
        """
        @param effective_time:
        @param switchover:
        @param instance_ids:
        """

        super(ApplyTemplate, self).__init__()
        self.effectiveTime = effective_time
        self.switchover = switchover
        self.instanceIds = instance_ids

    def to_json(self):
        """
         @return:
        """

        return self.__dict__


class RecoveryToSourceInstanceTable(object):
    """
    this is response RecoveryToSourceInstanceTableModel Model
    """

    def __init__(self, table_Name, new_table_name):
        """
        @param table_Name:
        @param new_table_name:
        """

        super(RecoveryToSourceInstanceTable, self).__init__()
        self.tableName = table_Name
        # need  Recovery table name
        self.newTablename = new_table_name

    def to_json(self):
        """
        @return:
        """

        return self.__dict__


class ParameterObject(object):
    """
     this is response ParameterObjectModel Model
    """

    def __init__(self, name, value, etag, applyMethod):
        """
         this is response ParameterObjectModel Model
        """

        super(ParameterObject, self).__init__()
        # need  paramter name
        self.name = name
        # need  paramter value
        self.value = value
        # need  etag
        self.etag = etag
        # need  applyMethod
        self.applyMethod = applyMethod

    def to_json(self):
        """
        @return:
        """

        return self.__dict__


class ParaTemplates(object):
    """
    this is request ParaTemplatesModel Model
    """

    def __init__(self, key, value):
        super(ParaTemplates, self).__init__()
        # need  key
        self.key = key
        # need  value value
        self.value = value

    def to_json(self):
        """
        @return:
        """

        return self.__dict__


class ParaTemplateUpdate(object):
    """
    this is request ParaTemplateUpdate Model
    """

    def __init__(self, key, oldValue, newValue):
        super(ParaTemplateUpdate, self).__init__()
        self.key = key
        self.oldValue = oldValue
        self.newValue = newValue

    def to_json(self):
        """
         @return:
        """

        return self.__dict__


class AccountPrivilege(object):
    """
     this is request AccountPrivilege object
    """

    def __init__(self, account_name, authType):
        """
         @param account_name:
         @param authType:
        """

        super(AccountPrivilege, self).__init__()
        self.accountName = account_name
        self.authType = authType

    def to_json(self):
        """
        @return:
        """

        return self.__dict__


class CreateDataBase(object):
    """
     this is request CreateDataBase object
    """

    def __init__(self, characterSetName, dbName, remark=None,
                 accountPrivileges=None, collate=None, c_type=None, owner=None):
        """
        @param characterSetName:
        @param dbName:
        @param remark:
        @param accountPrivileges:
        @param c_type:
        @param owner:
        """

        super(CreateDataBase, self).__init__()
        self.characterSetName = characterSetName
        self.dbName = dbName
        self.remark = remark
        self.accountPrivileges = accountPrivileges
        if c_type is not None:
            self.ctype = c_type
        if collate is not None:
            self.collate = collate
        if owner is not None:
            self.owner = owner

    def to_json(self):
        """
        @return:
        """

        return self.__dict__


class DatabasePrivilege(object):
    """
     this is request DatabasePrivilege object
    """

    def __init__(self, dbName, auth_type):
        """
         @param dbName:
         @param auth_type:
        """

        super(DatabasePrivilege, self).__init__()
        self.dbName = str(dbName)
        self.authType = auth_type

    def to_json(self):
        """
        @return:
        """

        return self.__dict__


class App(object):
    """
    this is request AppList object
    """

    def __init__(self, app_id, app_name, weight, ro_group_id, source_app_id, status, create_time, update_time,
                 app_status, app_id_short):
        """
        @param app_id:
        @param app_name:
        @param weight:
        @param ro_group_id:
        @param source_app_id:
        @param status:
        @param create_time:
        @param update_time:
        @param app_status:
        @param app_id_short:
        """

        self.appId = app_id
        self.appName = app_name
        self.weight = weight
        self.roGroupId = ro_group_id
        self.sourceAppId = source_app_id
        self.status = status
        self.createTime = create_time
        self.updateTime = update_time
        self.appStatus = app_status
        self.appIdShort = app_id_short

    def to_json(self):
        """
        @return:
        """

        return self.__dict__


class ReadReplica(object):
    """
     this is request ReadReplica object
    """

    def __init__(self, app_id, weight):
        """
        @param app_id:
        @param weight:
        """

        self.appId = app_id
        self.weight = weight

    def to_json(self):
        """
        @return:
        """

        return self.__dict__


class Endpoint(object):
    """
      this is request Endpoint object
    """

    def __init__(self, port, vnet_ip, inet_ip, address):
        """
        @param port:
        @param vnet_ip:
        @param inet_ip:
        @param address:
        """

        self.port = port
        self.vnetIp = vnet_ip
        self.inetIp = inet_ip
        self.address = address

    def to_json(self):
        """
        @return:
        """

        return self.__dict__


class JsonWrapper(JSONEncoder):
    """
    custom json encoder for class
    """


def default(self, obj):  # pylint: disable=E0202
    """
    @param self:
    @param obj:
    @return:
    """

    if isinstance(obj, RecoveryToSourceInstance):
        return {
            'restoreMode': obj.restoreMode,
            'dbName': obj.dbName,
            'newDbname': obj.newDbname,
            'tables': obj.tables
        }
    if isinstance(obj, RecoveryToSourceInstanceTable):
        return {
            'tableName': obj.tableName,
            'newTablename': obj.newTablename
        }
    if isinstance(obj, SubTableObject):
        return {
            'type': obj.type,
            'name': obj.name
        }
    if isinstance(obj, ParameterObject):
        return {
            "name": obj.name,
            "value": obj.value,
            "etag": obj.etag,
            "applyMethod": obj.applyMethod
        }
    if isinstance(obj, ParaTemplates):
        return {
            "key": obj.key,
            "value": obj.value
        }
    if isinstance(obj, ApplyTemplate):
        return {
            "effectiveTime": obj.effectiveTime,
            "switchover": obj.switchover,
            "instanceIds": obj.instanceIds
        }
    if isinstance(obj, AccountPrivilege):
        return {
            "accountName": obj.accountName,
            "authType": obj.authType
        }
    if isinstance(obj, CreateDataBase):
        return {
            "accountName": obj.dbName,
            "dbName": obj.dbName,
            "remark": obj.remark,
            "accountPrivileges": obj.accountPrivileges,
            "ctype": obj.ctype,
            "collate": obj.collate,
            "owner": obj.owner
        }
    return JSONEncoder.default(self, obj)
