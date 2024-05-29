# !/usr/bin/env python
# coding=utf-8
"""
Samples for dns client.
"""

import dns_sample_conf
from baidubce.services.dns.dns_client import DnsClient

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    __logger = logging.getLogger(__name__)

    # create a dns client
    dns_client = DnsClient(dns_sample_conf.config)

    # zone list
    print(dns_client.list_zone(name='javasdk.com'))

    # create zone
    create_zone_request = {
        'name': 'ccqTest1101.com'
    }
    dns_client.create_zone(create_zone_request=create_zone_request)

    # delete zone
    dns_client.delete_zone(zone_name='ccqTest1101.com')

    # create paid zone
    create_paid_zone_request = {
        'names': ['ccqTest1101.com'],
        'productVersion': 'discount',
        'billing': {
            'paymentTiming': 'Prepaid',
            'reservation': {
                'reservationLength': 1
            }
        }
    }
    dns_client.create_paid_zone(create_paid_zone_request=create_paid_zone_request)

    # upgrade zone
    upgrade_zone_request = {
        'names': ['ccqbcd.com'],
        'billing': {
            'paymentTiming': 'Prepaid',
            'reservation': {
                'reservationLength': 1
            }
        }
    }
    dns_client.upgrade_zone(upgrade_zone_request=upgrade_zone_request)

    # renew zone
    renew_zone_request = {
        'billing': {
            'reservation': {
                'reservationLength': 1
            }
        }
    }
    dns_client.renew_zone(name='ccqbcd.com', renew_zone_request=renew_zone_request)

    # create record
    create_record_request = {
        'rr': 'ccc',
        'type': 'A',
        'value': '1.1.1.1'
    }
    dns_client.create_record(name='ccqbcd.com', create_record_request=create_record_request)

    # record list
    print(dns_client.list_record(zone_name='ccqbcd.com'))

    # update record
    update_record_request = {
        'rr': 'ccc',
        'type': 'A',
        'value': '1.1.1.1'
    }
    dns_client.update_record(name='ccqbcd.com', update_record_request=update_record_request, record_id='52082')

    # update record enable
    dns_client.update_record_enable(name='ccqbcd.com', record_id='52082')

    # update record disable
    dns_client.update_record_enable(name='ccqbcd.com', record_id='52082')

    # delete record
    dns_client.delete_record(name='ccqbcd.com', record_id='52082')

    # add line group
    add_line_group_request = {
        'name': 'ccqLineGroup',
        'lines': ["zhejiang.ct", "shanxi.ct"]
    }
    dns_client.add_line_group(add_line_group_request=add_line_group_request)

    # update line group
    update_line_group_request = {
        'name': 'ccqLineGroup',
        'lines': ["zhejiang.ct", "shanxi.ct"]
    }
    dns_client.update_line_group(line_id='6174', update_line_group_request=update_line_group_request)

    # line group list
    print(dns_client.list_line_group())

    # delete line group
    dns_client.delete_line_group(line_id='6174')
