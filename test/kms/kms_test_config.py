#!/usr/bin/env python
#coding=utf-8

#导入Python标准日志模块
"""
KMS Test
"""
import logging

#从Python SDK导入KMS配置管理模块以及安全认证模块
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials

#设置KmsClient的Host，Access Key ID和Secret Access Key
kms_host = b"<your Host>"
access_key_id = b"<your AK>"
secret_access_key = b"<your SK>"

#设置日志文件的句柄和日志级别
logger = logging.getLogger('baidubce.services.kms.kmsclient')
fh = logging.FileHandler("sample.log")
fh.setLevel(logging.DEBUG)

#设置日志文件输出的顺序、结构和内容
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)

#创建BceClientConfiguration
config = BceClientConfiguration(credentials=BceCredentials(access_key_id, secret_access_key),
                                endpoint=kms_host)