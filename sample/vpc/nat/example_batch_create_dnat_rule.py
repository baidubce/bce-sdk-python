# !/usr/bin/env python
# coding=utf-8
"""
Samples for nat client.
"""

from baidubce import exception
from baidubce.services.vpc.nat_client import NatClient
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials

def test_batch_create_dnat_rule(nat_client, nat_id, rules):
    """
    batch create dnat rules of a specified nat gateway.

    :param nat_id:
        The id of specified nat-gateway.
    :type nat_id: string

    :param dnat_rules:
        Dnat rules, every rule contains ruleName, publicIpAddress, privateIpAddress, protocol, privatePort, publicPort.
    :type snat_rules: list<dict>

    :return:
    :rtype baidubce.bce_response.BceResponse

    Raise:
        BceHttpClientError: http request error
    """
    try:
        res = nat_client.batch_create_dnat_rule(nat_id=nat_id, dnat_rules=rules)
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
    
    rules = [
        {
            'ruleName': 'test_dnat_rule1',
            'publicIpAddress': "100.88.14.90",
            'privateIpAddress': "192.168.1.1",
            'protocol': 'TCP'
            'publicPort' '1212',
            'privatePort': '1212',
        },
        {
            'ruleName': 'test_dnat_rule2',
            'publicIpAddress': "100.88.14.52",
            'privateIpAddress': "192.168.1.2",
            'protocol': 'UDP'
            'publicPort' '65535',
            'privatePort': '65535',
        }
    ]
    # create dnat rule
    res = test_batch_create_dnat_rule(nat_client, nat_id=nat_id, rules=rules)
    print(res.rule_ids)