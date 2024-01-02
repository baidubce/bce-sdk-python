# !/usr/bin/env python
# coding=utf-8
"""
Samples for nat client.
"""

from baidubce import exception
from baidubce.services.vpc.nat_client import NatClient
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials

def test_update_dnat_rule(nat_client, nat_id, dnat_rule_id, public_ip_address, private_ip_address,
                          protocol, rule_name=None, public_port=None, private_port=None):

    """
    update dnat rule of a specified nat gateway.

    :param nat_id:
        The id of specified nat-gateway.
    :type nat_id: string

    :param dnat_rule_id:
        The id of specified dnat rule.
    :type nat_id: string

    :param rule_name:
        The name of dnat rule.
    :type rule_name: string

    :param public_ip_address:
        The public ip address of this dnat rule.
    :type public_ip_address: string

    :param private_ip_address:
        The private ip address of this dnat rule.
    :type private_ip_address: string

    :param protocol:
        protocol
    :type protocol: string

    :param public_port:
        public port
    :type public_port: string

    :param private_port:
        private port
    :type private_port: string

    :return:
    :rtype baidubce.bce_response.BceResponse

    Raise:
        BceHttpClientError: http request error
    """
    try:
        res = nat_client.update_dnat_rule(
            nat_id=nat_id, dnat_rule_id=dnat_rule_id,
            public_ip_address=public_ip_address, private_ip_address=private_ip_address,
            rule_name=rule_name, protocol=protocol, public_port=public_port, private_port=private_port)
        return res
    except exception.BceHttpClientError as e:
        #异常处理
        print(e.last_error)
        print(e.request_id)
        print(e.code)
        return None    

if __name__ == "__main__":
    
    # create a nat client
    HOST = b''
    AK = b''
    SK = b''
    config = BceClientConfiguration(credentials=BceCredentials(AK, SK), endpoint=HOST)

    nat_client = NatClient(config)
    nat_id = 'nat-brkztytqzbh0'
    dnat_rule_id = 'rule-zrsaybxm7nrn'

    rule_name = 'update_dnat_rule'
    private_ip_address = '192.168.1.1'
    public_ip_address = '100.88.14.90'
    protocol = 'TCP'
    public_port = '1212'
    private_port = '1212'
    # update dnat rule
    res = test_update_dnat_rule(nat_client, nat_id=nat_id, 
                                dnat_rule_id=dnat_rule_id, 
                                public_ip_address=public_ip_address,
                                private_ip_address=private_ip_address,
                                rule_name=rule_name, protocol=protocol)
