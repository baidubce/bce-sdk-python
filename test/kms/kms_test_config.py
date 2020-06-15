#!/usr/bin/env python
#coding=utf-8

#导入Python标准日志模块
"""
MVS Test
"""
import logging

#从Python SDK导入BOS配置管理模块以及安全认证模块
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials

#设置BosClient的Host，Access Key ID和Secret Access Key
kms_host = b"http://kms.gz.qasandbox.baidu-int.com"
access_key_id = b"b0c32bcfa987440eab823563c110dd8f"
secret_access_key = b"4c69d593d39e4ba5b8b3ddf11480821d"

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