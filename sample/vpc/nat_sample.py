# !/usr/bin/env python
# coding=utf-8
"""
Samples for nat client.
"""
import uuid

import nat_sample_conf
from baidubce.services.vpc.nat_client import NatClient
from baidubce.services.vpc import nat_model


def generate_client_token_by_uuid():
    """
    The default method to generate the random string for client_token
    if the optional parameter client_token is not specified by the user.

    :return:
    :rtype string
    """
    return str(uuid.uuid4())


if __name__ == "__main__":
    import logging

    post_paid_billing = nat_model.Billing('Postpaid')
    VPC_ID = b'vpc-wqg0urr96be3'
    logging.basicConfig(level=logging.DEBUG)
    __logger = logging.getLogger(__name__)

    # create a nat client
    nat_client = NatClient(nat_sample_conf.config)

    # nat list
    print(nat_client.list_nats(vpc_id=VPC_ID))

    # create a nat
    client_token = generate_client_token_by_uuid()
    name = 'enhance_nat_' + client_token
    bce_response = nat_client.create_nat(client_token=client_token, name=name,
                                         vpc_id=VPC_ID,
                                         billing=post_paid_billing, cu_num=10)
    print (type(bce_response))
    print(bce_response)
    print(bce_response.nat_id)
