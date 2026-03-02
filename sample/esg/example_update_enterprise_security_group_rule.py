# -*- coding: utf-8 -*-
"""
    Example for updating an enterprise security group rule from the specified enterprise security group.
"""
import uuid
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.esg import esg_client

if __name__ == '__main__':
    ak = "Your AK"  # 账号的Ak
    sk = "Your SK"  # 账号的Sk
    endpoint = "endpoint"  # 服务对应的Region域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    esg_client = esg_client.EsgClient(config)  # client 初始化
    try:
        # 使用新增参数的示例：remote_ip_set 和 remote_ip_group
        # remote_ip_set: 远程IP地址列表，可以指定多个IP地址
        # remote_ip_group: 远程IP组ID，引用预定义的IP组
        resp2 = esg_client.update_enterprise_security_group_rule(enterprise_security_group_rule_id='esgr-dyc175jcmbi0',
                                                                 remark='test with remote ip set',
                                                                 protocol='tcp',
                                                                 portrange='80-443',
                                                                 action='allow',
                                                                 priority=100,
                                                                 remote_ip_group='ipg-ie0hnjua54wh',
                                                                 client_token=str(uuid.uuid4())
                                                                 )
        print("[example] update esg rules with remote_ip_group response: %s" % resp2)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)