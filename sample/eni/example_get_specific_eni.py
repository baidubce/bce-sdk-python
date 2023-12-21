# -*- coding: utf-8 -*-
"""
example for get eni details.
"""
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.eni import eni_client

if __name__ == '__main__':
    ak = "Your Ak"  # 账号的Ak
    sk = "Your Sk"  # 账号的Sk
    endpoint = "bcc.bj.baidubce.com"  # 服务对应的Region域名, 例如bj Region域名
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    client = eni_client.EniClient(config)  # client 初始化
    
    try:
        resp = client.get_eni_details(eni_id="eni-7bqg7jf0m88f")  # 查询指定的弹性网卡
        eni_id = resp.eni_id #  查询的弹性网卡ID
        name = resp.name #  查询的弹性网卡名称
        description = resp.description #  查询的弹性网卡描述
        vpc_id = resp.vpc_id # 查询的弹性网卡所属VPC ID
        subnet_id = resp.subnet_id # 查询的弹性网卡所属子网ID
        mac_address = resp.mac_address # 查询的弹性网卡MAC地址
        status = resp.status # 查询的弹性网卡状态
        zone_name = resp.zone_name # 查询的弹性网卡所在可用区
        instance_id = resp.instance_id # 查询的弹性网卡绑定的实例ID
        private_ip_set = resp.private_ip_set # 查询的弹性网卡绑定的内网IP列表
        ipv6_private_ip_set = resp.ipv6_private_ip_set # 查询的弹性网卡绑定的内网IPv6地址列表
        security_group_ids = resp.security_group_ids # 查询的弹性网卡绑定的安全组ID列表
        enterprise_security_group_ids = resp.enterprise_security_group_ids # 查询的弹性网卡绑定的企业安全组ID列表
        created_time = resp.created_time # 查询的弹性网卡创建时间
        print("get eni details response :%s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s\n" % e)
