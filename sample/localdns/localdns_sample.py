# !/usr/bin/env python
# coding=utf-8
"""
Samples for ld client.
"""

import localdns_sample_conf
from baidubce.services.localdns.ld_client import LdClient

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    __logger = logging.getLogger(__name__)

    # create a ld client
    ld_client = LdClient(localdns_sample_conf.config)

    # zone list
    print(ld_client.list_private_zone())

    # create zone
    create_private_zone_request = {
        'zoneName': 'ccqTest0711.com'
    }
    ld_client.create_private_zone(create_private_zone_request=create_private_zone_request)

    # delete zone
    ld_client.delete_private_zone(zone_id='zone-7ssiavcjqi90')

    # zone detail
    print(ld_client.get_private_zone(zone_id='zone-nqa0uqyse51z'))

    # bind vpc
    bind_vpc_request = {
        'region': 'bj',
        'vpcIds': ['vpc-4kzjwxgvx4fi']
    }
    ld_client.bind_vpc(zone_id='zone-nqa0uqyse51z', bind_vpc_request=bind_vpc_request)

    # unbind vpc
    unbind_vpc_request = {
        'region': 'bj',
        'vpcIds': ['vpc-4kzjwxgvx4fi']
    }
    ld_client.unbind_vpc(zone_id='zone-nqa0uqyse51z', unbind_vpc_request=unbind_vpc_request)

    # add record
    add_record_request = {
        'rr': 'www',
        'type': 'A',
        'value': '2.2.2.2'
    }
    ld_client.add_record(zone_id='zone-nqa0uqyse51z', add_record_request=add_record_request)

    # update record
    update_record_request = {
        'rr': 'www',
        'type': 'A',
        'value': '2.2.2.3'
    }
    ld_client.update_record(record_id='rc-v9nc88nm0te2', update_record_request=update_record_request)

    # enable record
    ld_client.enable_record(record_id='rc-v9nc88nm0te2')

    # disable record
    ld_client.disable_record(record_id='rc-v9nc88nm0te2')

    # list record
    print(ld_client.list_record(zone_id='zone-nqa0uqyse51z'))

    # delete record
    ld_client.delete_record(record_id='rc-v9nc88nm0te2')

