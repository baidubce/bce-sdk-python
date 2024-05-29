# -*- coding: utf-8 -*-
"""
example for create probe.
"""

import uuid

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.probe import probe_client

if __name__ == "__main__":
    ak = "Your AK"  # 账号的AK
    sk = "Your SK"  # 账号的SK
    endpoint = "bcc.bj.baidubce.com"  # 服务对应region的域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    probe_client = probe_client.ProbeClient(config)
    try:
        resp = probe_client.create_probe(name='test',  # 探测名称
                                         vpc_id='test_vpc_id',  # 探测所在的vpc id
                                         subnet_id='test_subnet_id',  # 探测所在的子网id
                                         protocol='UDP',  # 探测协议,可选ICMP、UDP、TCP或DNS
                                         frequency=10,  # 探测频率(次/分钟)，可选10、20或30，默认值为20
                                         dst_ip='10.254.38.4',  # 探测目的ip
                                         dst_port='3306',  # 探测目的端口，当协议为UDP、TCP或DNS时需填写
                                         source_ips=['10.254.38.10', '10.254.38.11'],  # 探测指定源ip
                                         source_ip_num=1,  # 探测自动生成源ip个数，当未指定源ip时，source_ip_num必须大于0
                                         description='probe create example',  #探测描述
                                         payload='test',  # 协议为UDP时，需填写探测字符串；协议为DNS时，需填写探测域名
                                         client_token=str(uuid.uuid4()))
        probe_id = resp.probe_id
        print("Create probe response: %s" % probe_id)
    except BceHttpClientError as e:
        print("Exception when calling api: %s" % e)