# -*- coding: utf-8 -*-
"""
cloudflow model module.

This module defines data structures and enumerations for CloudFlow OpenAPI.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import json
import six
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from baidubce import compat

public_key_pem = b"""-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQChKcFfV3FEDaOv2gTOOlRYm+Yk
fcKUtI81/B/klSidVRBtaL/d8s0nerJFv39gi42U5DFewKEMTJlWboAdvQfLshsH
D++x62x4XCFeFz7Uc4H30AXNVHLhB6S1oFlYWldjK+EQ/jpOFh+ct86cLf4pnMrp
tqG35j6d4hDDOtqY9wIDAQAB
-----END PUBLIC KEY-----"""

def _encrypt_ak_sk(public_key_pem, text):
    """
    :param public_key_pem: PEM format public key (str or bytes)
    :param text: Original AK/SK (str or unicode)
    :return: Base64 encoded encrypted string (str)
    """
    public_key_pem = compat.convert_to_bytes(public_key_pem)
    text_bytes = compat.convert_to_bytes(text)

    rsa_key = RSA.importKey(public_key_pem)
    cipher = PKCS1_v1_5.new(rsa_key)
    encrypted = cipher.encrypt(text_bytes)

    result = base64.b64encode(encrypted)
    return compat.convert_to_string(result)

class _EnumMeta(type):
    """
    Metaclass, used to define the enumeration base class
    """
    def __contains__(cls, item):
        return item in cls.__dict__.values()


class BaseEnum(six.with_metaclass(_EnumMeta)):
    """
    Enumeration base class, supporting member checking
    """
    pass

class MigrationInterface(BaseEnum):
    """
    Migration Enumeration
    """
    POSTMIGRATION         = b"migration"
    POSTMIGRATIONFROMLIST = b"migrationFromList"
    GETMIGRATION          = b"migration"
    LISTMIGRATION         = b"migrationList"
    GETMIGRATIONRESULT    = b"migrationResult"
    PAUSEMIGRATION        = b"pauseMigration"
    RESUMEMIGRATION       = b"resumeMigration"
    RETRYMIGRATION        = b"retryMigration"
    DELETEMIGRATION       = b"migration"

class RunningStatus(BaseEnum):
    """
    Task Status Enumeration
    """
    WAITING                   = "WAITING"
    READY_FOR_MIGRATION       = "READY_FOR_MIGRATION"
    MIGRATING                 = "MIGRATING"
    PAUSED                    = "PAUSED"
    FINISHED                  = "FINISHED"
    PARTIALLY_FAILED_FINISHED = "PARTIALLY_FAILED_FINISHED"
    FAILED                    = "FAILED"
    INCREMENTAL_MIGRATING     = "INCREMENTAL_MIGRATING"
    RETRYING                  = "RETRYING"


class MigrationTypeValue(BaseEnum):
    """
    Migration Type Enumeration
    """
    STOCK       = "STOCK"
    INCREMENTAL = "INCREMENTAL"


class MigrationMode(BaseEnum):
    """
    Migration Mode Enumeration
    """
    FULLY_MANAGED = "FULLY_MANAGED"
    SEMI_MANAGED  = "SEMI_MANAGED"


class Strategy(BaseEnum):
    """
    Enumeration of file processing policies with the same name
    """
    FORCE_OVERWRITE  = "FORCE_OVERWRITE"
    KEEP_DESTINATION = "KEEP_DESTINATION"


class StorageClass(BaseEnum):
    """
    Storage Type Enumeration
    """
    STANDARD        = "STANDARD"
    STANDARD_IA     = "STANDARD_IA"
    COLD            = "COLD"
    ARCHIVE         = "ARCHIVE"
    MAZ_STANDARD    = "MAZ_STANDARD"
    MAZ_STANDARD_IA = "MAZ_STANDARD_IA"
    SAME_AS_SOURCE  = "SAME_AS_SOURCE"


class Acl(BaseEnum):
    """
    Access enumeration
    """
    KEEP_BUCKET    = "KEEP_BUCKET"
    SAME_AS_SOURCE = "SAME_AS_SOURCE"


class DailySchedule(object):
    """
    Daily execution time interval
    """
    _fields = ('start', 'end')

    def __init__(self, start=None, end=None):
        self.start = start  # type: str, format "HH:mm"
        self.end   = end    # type: str, format "HH:mm"

    def __setattr__(self, name, value):
        if name.startswith('_') or name in self.__class__._fields:
            self.__dict__[name] = value
        else:
            raise AttributeError("'DailySchedule' object has no attribute '%s'" % name)

    def __delattr__(self, name):
        if name.startswith('_') or name in self.__class__._fields:
            del self.__dict__[name]
        else:
            raise AttributeError("'DailySchedule' object has no attribute '%s'" % name)

    def to_dict(self):
        """
        convert self to dict
        """
        return {k: getattr(self, k) for k in self.__class__._fields if getattr(self, k) is not None}


class SourceConfig(object):
    """
    Source side configuration
    """
    _fields = ('provider', 'endpoint', 'bucket', 'ak', 'sk',
               'prefixes', 'object_begin_time', 'object_end_time',
               'list_file_url', 'object_list_location', 'region')

    def __init__(self, provider, endpoint, bucket, ak, sk, prefixes=None,
                 object_begin_time=-1, object_end_time=-1, list_file_url=None,
                 object_list_location=None, region=None):
        self.provider             = provider                            # type: str
        self.endpoint             = endpoint                            # type: str
        self.bucket               = bucket                              # type: str
        self.ak                   = _encrypt_ak_sk(public_key_pem, ak)  # type: str
        self.sk                   = _encrypt_ak_sk(public_key_pem, sk)  # type: str
        self.prefixes             = prefixes or []                      # type: list[str]
        self.object_begin_time    = object_begin_time                   # type: int
        self.object_end_time      = object_end_time                     # type: int
        self.list_file_url        = list_file_url                       # type: list[str] or None
        self.object_list_location = object_list_location                # type: str
        self.region               = region                              # type: str

        if prefixes is not None and not isinstance(prefixes, list):
            raise ValueError("prefixes must be a list")

    def __setattr__(self, name, value):
        if name.startswith('_') or name in self.__class__._fields:
            self.__dict__[name] = value
        else:
            raise AttributeError("'SourceConfig' object has no attribute '%s'" % name)

    def __delattr__(self, name):
        if name.startswith('_') or name in self.__class__._fields:
            del self.__dict__[name]
        else:
            raise AttributeError("'SourceConfig' object has no attribute '%s'" % name)

    def to_dict(self):
        """
        convert self to dict
        """
        d = {}
        for k in self.__class__._fields:
            v = getattr(self, k)
            if v is not None:
                # conversion field name: underline to hump (according to API document)
                if k == 'object_begin_time':
                    key = 'objectBeginTime'
                elif k == 'object_end_time':
                    key = 'objectEndTime'
                elif k == 'list_file_url':
                    key = 'listFileURL'
                elif k == 'object_list_location':
                    key = 'objectListLocation'
                else:
                    key = k
                d[key] = v
        return d
    

class DestinationConfig(object):
    """
    Destination configuration
    """
    _fields = ('provider', 'endpoint', 'bucket', 'ak', 'sk',
               'prefix', 'region', 'storage_class', 'acl')

    def __init__(self, provider, endpoint, bucket, ak, sk, region,
                 storage_class, acl, prefix=None):
        self.provider      = provider                           # type: str
        self.endpoint      = endpoint      # type: str
        self.bucket        = bucket        # type: str
        self.ak            = _encrypt_ak_sk(public_key_pem, ak) # type: str
        self.sk            = _encrypt_ak_sk(public_key_pem, sk) # type: str
        self.prefix        = prefix                             # type: str
        self.region        = region                             # type: str
        self.storage_class = storage_class                      # type: str
        self.acl           = acl                                # type: str

        if storage_class not in StorageClass:
            raise ValueError("storage_class must be one of %s, got %s" %
                              (StorageClass.__dict__.keys(), storage_class))
        if acl not in Acl:
            raise ValueError("acl must be one of %s, got %s" %
                              (Acl.__dict__.keys(), acl))

    def __setattr__(self, name, value):
        if name.startswith('_') or name in self.__class__._fields:
            self.__dict__[name] = value
        else:
            raise AttributeError("'DestinationConfig' object has no attribute '%s'" % name)

    def __delattr__(self, name):
        if name.startswith('_') or name in self.__class__._fields:
            del self.__dict__[name]
        else:
            raise AttributeError("'DestinationConfig' object has no attribute '%s'" % name)

    def to_dict(self):
        """
        convert self to dict
        """
        d = {}
        for k in self.__class__._fields:
            v = getattr(self, k)
            if v is not None:
                if k == 'storage_class':
                    key = 'storageClass'
                else:
                    key = k
                d[key] = v
        return d


class MigrationType(object):
    """
    Migration Type Configuration
    """
    _fields = ('type', 'increase_scan_interval_in_hours', 'increase_times')

    def __init__(self, type, increase_scan_interval_in_hours=None, increase_times=None):
        self.type                            = type                             # type: str
        self.increase_scan_interval_in_hours = increase_scan_interval_in_hours  # type: int
        self.increase_times                  = increase_times                   # type: int

        if type not in MigrationTypeValue:
            raise ValueError("type must be one of %s, got %s" %
                              (MigrationTypeValue.__dict__.keys(), type))

    def __setattr__(self, name, value):
        if name.startswith('_') or name in self.__class__._fields:
            self.__dict__[name] = value
        else:
            raise AttributeError("'MigrationType' object has no attribute '%s'" % name)

    def __delattr__(self, name):
        if name.startswith('_') or name in self.__class__._fields:
            del self.__dict__[name]
        else:
            raise AttributeError("'MigrationType' object has no attribute '%s'" % name)

    def to_dict(self):
        """
        convert object to dict
        """
        d = {'type': self.type}
        if self.increase_scan_interval_in_hours is not None:
            d['increaseScanIntervalInHours'] = self.increase_scan_interval_in_hours
        if self.increase_times is not None:
            d['increaseTimes'] = self.increase_times
        return d


class PerformanceSetting(object):
    """
    Time phased performance configuration
    """
    _fields = ('start_time', 'end_time', 'band_width_in_mb')

    def __init__(self, start_time=None, end_time=None, band_width_in_mb=None):
        self.start_time       = start_time        # type: str
        self.end_time         = end_time          # type: str
        self.band_width_in_mb = band_width_in_mb  # type: int

    def __setattr__(self, name, value):
        if name.startswith('_') or name in self.__class__._fields:
            self.__dict__[name] = value
        else:
            raise AttributeError("'PerformanceSetting' object has no attribute '%s'" % name)

    def __delattr__(self, name):
        if name.startswith('_') or name in self.__class__._fields:
            del self.__dict__[name]
        else:
            raise AttributeError("'PerformanceSetting' object has no attribute '%s'" % name)

    def to_dict(self):
        """
        convert object to dict
        """
        d = {}
        if self.start_time is not None:
            d['startTime'] = self.start_time
        if self.end_time is not None:
            d['endTime'] = self.end_time
        if self.band_width_in_mb is not None:
            d['bandWidthInMB'] = self.band_width_in_mb
        return d


class ValidationMethodConfig(object):
    """
    Verification configuration
    """
    _fields = ('enable_crc64_ecma_validation', 'enable_md5_validation')

    def __init__(self, enable_crc64_ecma_validation=None, enable_md5_validation=None):
        self.enable_crc64_ecma_validation = enable_crc64_ecma_validation  # type: bool
        self.enable_md5_validation        = enable_md5_validation         # type: bool

    def __setattr__(self, name, value):
        if name.startswith('_') or name in self.__class__._fields:
            self.__dict__[name] = value
        else:
            raise AttributeError("'ValidationMethodConfig' object has no attribute '%s'" % name)

    def __delattr__(self, name):
        if name.startswith('_') or name in self.__class__._fields:
            del self.__dict__[name]
        else:
            raise AttributeError("'ValidationMethodConfig' object has no attribute '%s'" % name)

    def to_dict(self):
        """
        convert object to dict
        """
        d = {}
        if self.enable_crc64_ecma_validation is not None:
            d['enableCRC64ECMAValidation'] = self.enable_crc64_ecma_validation
        if self.enable_md5_validation is not None:
            d['enableMD5Validation'] = self.enable_md5_validation
        return d


class CreateTaskInfo(object):
    """
    Create task parameter information
    """

    _fields = ('task_name', 'schedule_start_time', 'daily_schedule',
               'source_config', 'destination_config', 'strategy',
               'migration_type', 'migration_mode', 'qps', 'performance_setting',
               'not_include_content', 'validation_method_config')

    def __init__(self, task_name, schedule_start_time, source_config,
                 destination_config, strategy, migration_type,
                 migration_mode, daily_schedule=None, qps=None,
                 performance_setting=None, not_include_content=None,
                 validation_method_config=None):
        self.task_name                  = task_name                 # type: str
        self.schedule_start_time        = schedule_start_time       # type: str
        self.daily_schedule             = daily_schedule            # type: str
        self.source_config              = source_config             # type: dict
        self.destination_config         = destination_config        # type: dict
        self.strategy                   = strategy                  # type: str
        self.migration_type             = migration_type            # type: dict
        self.migration_mode             = migration_mode            # type: str
        self.qps                        = qps                       # type: int
        self.performance_setting        = performance_setting       # type: list
        self.not_include_content        = not_include_content       # type: list[str]
        self.validation_method_config   = validation_method_config  # type: dict

        if self.source_config.region is not None:
            raise ValueError("source_config.region is the parameter of create_task_list, it must be empty")
        if self.source_config.list_file_url is not None:
            raise ValueError("source_config.listFileUrl is the parameter of create_task_list, it must be empty")

    def __setattr__(self, name, value):
        if name.startswith('_') or name in self.__class__._fields:
            self.__dict__[name] = value
        else:
            raise AttributeError("'CreateTaskInfo' object has no attribute '%s'" % name)

    def __delattr__(self, name):
        if name.startswith('_') or name in self.__class__._fields:
            del self.__dict__[name]
        else:
            raise AttributeError("'CreateTaskInfo' object has no attribute '%s'" % name)

    def _to_dict(self):
        """
        convert object to dict
        """
        d = {
            'name': self.task_name,
            'scheduleStartTime': self.schedule_start_time,
            'sourceConfig': self.source_config.to_dict(),
            'destinationConfig': self.destination_config.to_dict(),
            'strategy': self.strategy,
            'migrationType': self.migration_type.to_dict(),
            'migrationMode': self.migration_mode,
        }
        if self.daily_schedule is not None:
            d['dailySchedule'] = self.daily_schedule.to_dict()
        if self.qps is not None:
            d['qps'] = self.qps
        if self.performance_setting is not None:
            d['performanceSetting'] = [perf.to_dict() for perf in self.performance_setting]

        if self.not_include_content is not None:
            d['notIncludeContent'] = self.not_include_content
        if self.validation_method_config is not None:
            d['validationMethodConfig'] = self.validation_method_config.to_dict()
        return d

    def to_json_string(self):
        """
        Convert object to json string
        """
        return json.dumps(self._to_dict())
    
class CreateTaskListInfo(object):
    """
    Create task parameter information from list
    """
    _fields = ('task_name', 'schedule_start_time', 'daily_schedule',
               'source_config', 'destination_config', 'strategy',
               'migration_type', 'migration_mode', 'qps', 'validation_method_config')

    def __init__(self, task_name, schedule_start_time, source_config,
                 destination_config, strategy, migration_type,
                 migration_mode, daily_schedule=None, qps=None,
                 validation_method_config=None):
        self.task_name                  = task_name                 # type: str
        self.schedule_start_time        = schedule_start_time       # type: int
        self.daily_schedule             = daily_schedule            # type: str
        self.source_config              = source_config             # type: dict
        self.destination_config         = destination_config        # type: dict
        self.strategy                   = strategy                  # type: dict
        self.migration_type             = migration_type            # type: dict
        self.migration_mode             = migration_mode            # type: str
        self.qps                        = qps                       # type: int
        self.validation_method_config   = validation_method_config  # type: dict

        if self.source_config.prefixes:
            raise ValueError("source_config.prefixes is the parameter of create_task, it must be empty")
        if self.source_config.object_begin_time != -1:
            raise ValueError("source_config.object_begin_time is the parameter of create_task, it must be empty")
        if self.source_config.object_end_time != -1:
            raise ValueError("source_config.object_end_time is the parameter of create_task, it must be empty")

    def __setattr__(self, name, value):
        if name.startswith('_') or name in self.__class__._fields:
            self.__dict__[name] = value
        else:
            raise AttributeError("'CreateTaskListInfo' object has no attribute '%s'" % name)

    def __delattr__(self, name):
        if name.startswith('_') or name in self.__class__._fields:
            del self.__dict__[name]
        else:
            raise AttributeError("'CreateTaskListInfo' object has no attribute '%s'" % name)

    def _to_dict(self):
        """
        convert object to dict
        """
        d = {
            'name': self.task_name,
            'scheduleStartTime': self.schedule_start_time,
            'sourceConfig': self.source_config.to_dict(),
            'destinationConfig': self.destination_config.to_dict(),
            'strategy': self.strategy,
            'migrationType': self.migration_type.to_dict(),
            'migrationMode': self.migration_mode,
        }
        if self.daily_schedule is not None:
            d['dailySchedule'] = self.daily_schedule.to_dict()
        if self.qps is not None:
            d['qps'] = self.qps
        if self.validation_method_config is not None:
            d['validationMethodConfig'] = self.validation_method_config.to_dict()
        return d

    def to_json_string(self):
        """
        Convert object to json string
        """
        return json.dumps(self._to_dict())
