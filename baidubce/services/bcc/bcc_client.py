# -*- coding: utf-8 -*-
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the
# License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.

"""
This module provides a client class for BCC.
"""

from __future__ import unicode_literals

import copy
import json
import logging
import random
import string
import uuid

from baidubce import bce_base_client
from baidubce.auth import bce_v1_signer
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce.http import http_methods
from baidubce.services.bcc import bcc_model
from baidubce.utils import aes128_encrypt_16char_key
from baidubce.utils import required
from baidubce import compat

_logger = logging.getLogger(__name__)

FETCH_MODE_SYNC = b"sync"
FETCH_MODE_ASYNC = b"async"

ENCRYPTION_ALGORITHM = "AES256"

default_billing_to_purchase_created = bcc_model.Billing('Postpaid')
default_billing_to_purchase_reserved = bcc_model.Billing()


class BccClient(bce_base_client.BceBaseClient):
    """
    Bcc base sdk client
    """

    prefix = b'/v2'
    prefix_v3 = b'/v3'

    def __init__(self, config=None):
        bce_base_client.BceBaseClient.__init__(self, config)

    def _merge_config(self, config=None):
        if config is None:
            return self.config
        else:
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    def _send_request(self, http_method, path,
                      body=None, headers=None, params=None,
                      config=None, body_parser=None, prefix=None):
        config = self._merge_config(config)
        if body_parser is None:
            body_parser = handler.parse_json
        if prefix is None:
            prefix = BccClient.prefix

        return bce_http_client.send_request(
            config, bce_v1_signer.sign, [handler.parse_error, body_parser],
            http_method, prefix + path, body, headers, params)

    @required(cpu_count=int,
              memory_capacity_in_gb=int,
              image_id=(bytes, str))  # ***Unicode***
    def create_instance(self, cpu_count, memory_capacity_in_gb, image_id, instance_type=None,
                        billing=None, create_cds_list=None, root_disk_size_in_gb=0, root_disk_storage_type=None,
                        ephemeral_disks=None, dedicate_host_id=None, auto_renew_time_unit=None, auto_renew_time=0,
                        deploy_id=None, bid_model=None, bid_price=None, key_pair_id=None, cds_auto_renew=False,
                        internet_charge_type=None, internal_ips=None, request_token=None, asp_id=None, tags=None,
                        network_capacity_in_mbps=0, purchase_count=1, cardCount=1, name=None, admin_pass=None,
                        zone_name=None, subnet_id=None, security_group_id=None, gpuCard=None, fpgaCard=None,
                        spec=None, eip_name=None, hostname=None, auto_seq_suffix=False, is_open_hostname_domain=False,
                        relation_tag=None, is_open_ipv6=None, enterprise_security_group_id=None,
                        security_group_ids=None, enterprise_security_group_ids=None, ehc_cluster_id=None,
                        kunlunCard=None, isomerismCard=None, file_systems=None, user_data=None, is_open_hosteye=False,
                        deletion_protection=None, res_group_id=None,
                        client_token=None, config=None, card_count=1, isomerism_card=None, is_keep_image_login=None):
        """
        Create a bcc Instance with the specified options.
        You must fill the field of clientToken,which is especially for keeping idempotent.
        This is an asynchronous interface,
        you can get the latest status by BccClient.get_instance.

        :param instance_type:
            The specified Specification to create the instance,
            See more detail on
            https://cloud.baidu.com/doc/BCC/API.html#InstanceType
        :type instance_type: string

        :param cpu_count:
            The parameter to specified the cpu core to create the instance.
        :type cpu_count: int

        :param memory_capacity_in_gb:
            The parameter to specified the capacity of memory in GB to create the instance.
        :type memory_capacity_in_gb: int

        :param image_id:
            The id of image, list all available image in BccClient.list_images.
        :type image_id: string

        :param billing:
            Billing information.
        :type billing: bcc_model.Billing

        :param create_cds_list:
            The optional list of volume detail info to create.
        :type create_cds_list: list<bcc_model.CreateCdsModel>

        :param network_capacity_in_mbps:
            The optional parameter to specify the bandwidth in Mbps for the new instance.
            It must among 0 and 200, default value is 0.
            If it's specified to 0, it will get the internal ip address only.
        :type network_capacity_in_mbps: int

        :param purchase_count:
            The number of instance to buy, the default value is 1.
        :type purchase_count: int

        :param name:
            The optional parameter to desc the instance that will be created.
        :type name: string

        :param admin_pass:
            The optional parameter to specify the password for the instance.
            If specify the adminPass,the adminPass must be a 8-16 characters String
            which must contains letters, numbers and symbols.
            The symbols only contains "!@#$%^*()".
            The adminPass will be encrypted in AES-128 algorithm
            with the substring of the former 16 characters of user SecretKey.
            If not specify the adminPass, it will be specified by an random string.
            See more detail on
            https://bce.baidu.com/doc/BCC/API.html#.7A.E6.31.D8.94.C1.A1.C2.1A.8D.92.ED.7F.60.7D.AF
        :type admin_pass: string

        :param zone_name:
            The optional parameter to specify the available zone for the instance.
            See more detail through list_zones method
        :type zone_name: string

        :param subnet_id:
            The optional parameter to specify the id of subnet from vpc, optional param
             default value is default subnet from default vpc
        :type subnet_id: string

        :param security_group_id:
            The optional parameter to specify the securityGroupId of the instance
            vpcId of the securityGroupId must be the same as the vpcId of subnetId
            See more detail through listSecurityGroups method
        :type security_group_id: string

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if client token is provided.
            If the clientToken is not specified by the user,
            a random String generated by default algorithm will be used.
            See more detail at
            https://bce.baidu.com/doc/BCC/API.html#.E5.B9.82.E7.AD.89.E6.80.A7
        :type client_token: string

        :param fpgaCard:
            This parameter is obsolete. Use parameter isomerism_card instead.
        :type fpgaCard: string

        :param gpuCard:
            This parameter is obsolete. Use parameter isomerism_card instead.
        :type gpuCard: string

        :param cardCount:
            This parameter is obsolete. Use parameter card_count instead.
        :type cardCount: int

        :param card_count:
            The parameter to specify the card count for creating GPU/FPGA instance.
        :type card_count: int

        :param root_disk_size_in_gb:
            The parameter to specify the root disk size in GB.
            The root disk excludes the system disk, available is 40-500GB.
        :type root_disk_size_in_gb: int

        :param root_disk_storage_type:
            The parameter to specify the root disk storage type.
            Default use of HP1 cloud disk.
        :type root_disk_storage_type: string

        :param ephemeral_disks:
            The optional list of ephemeral volume detail info to create.
        :type ephemeral_disks: list<bcc_model.EphemeralDisk>

        :param dedicate_host_id:
            The parameter to specify the dedicate host id.
        :type dedicate_host_id: string

        :param auto_renew_time_unit:
            The parameter to specify the unit of the auto renew time.
            The auto renew time unit can be "month" or "year".
            The default value is "month".
        :type auto_renew_time_unit: string

        :param auto_renew_time:
            The parameter to specify the auto renew time, the default value is 0.
        :type auto_renew_time: int

        :param tags:
            The optional list of tag to be bonded.
        :type tags: list<bcc_model.TagModel>

        :param deploy_id:
            The parameter to specify the id of the deploymentSet.
        :type deploy_id: string

        :param bid_model:
            The parameter to specify the bidding model.
            The bidding model can be "market" or "custom".
        :type bid_model: string

        :param bid_price:
            The parameter to specify the bidding price.
            When the bid_model is "custom", it works.
        :type bid_price: string

        :param key_pair_id:
            The parameter to specify id of the keypair.
        :type key_pair_id: string

        :param asp_id:
            The parameter to specify id of the asp.
        :type asp_id: string

        :param request_token:
            The parameter to specify the request token which will make the request idempotent.
        :type request_token: string

        :param internet_charge_type:
            The parameter to specify the internet charge type.
            See more detail on
            https://cloud.baidu.com/doc/BCC/API.html#InternetChargeType
        :type internet_charge_type: string

        :param internal_ips:
            The parameter to specify the internal ips.
        :type internal_ips: list<string>

        :param cds_auto_renew
            The parameter to specify whether the cds is auto renew or not.
            The default value is false.
        :type cds_auto_renew: boolean

        :param spec:
            spec
        :type spec: string

        :param eip_name:
            eip name
        :type eip_name: string

        :param hostname:
            The optional parameter to specify the host name of the instance virtual machine.
            By default, hostname is not specified.
            If hostname is specified: hostname is used as the prefix of the name in batches.
            The backend will add a suffix, and the suffix generation method is: name{-serial number}.
            If name is not specified, it will be automatically generated using the following method:
            {instance-eight-digit random string-serial number}.
            Note: The random string is generated from the characters 0-9 and a-z;
            the serial number increases sequentially according to the magnitude of count.
            If count is 100, the serial number increases from 000~100, and if it is 10, it increases from 00~10.
            Only lowercase letters, numbers and - . special characters are supported.
            They must start with a letter. Special symbols cannot be used continuously.
            Special symbols are not supported at the beginning or end. The length is 2-64.
        :type hostname: string

        :param auto_seq_suffix:
            The parameter to specify whether name and hostname order suffixes are automatically generated
        :type auto_seq_suffix: boolean

        :param is_open_hostname_domain:
            The parameter to specify whether hostname domain is automatically generated
        :type is_open_hostname_domain: boolean

        :param relation_tag:
            The parameter to specify whether the instance related to existing tags
        :type relation_tag: boolean

        :param is_open_ipv6:
            is_open_ipv6
        :type is_open_ipv6: boolean

        :param enterprise_security_group_id:
            enterprise_security_group_id
        :type enterprise_security_group_id: string

        :param security_group_ids:
            security_group_ids
        :type security_group_ids: list<string>

        :param enterprise_security_group_ids:
            enterprise_security_group_ids
        :type enterprise_security_group_ids: list<string>

        :param ehc_cluster_id:
            The id of ehcCluster.
        :type ehc_cluster_id: string

        :param kunlunCard:
            This parameter is obsolete. Use parameter isomerism_card instead.
        :type kunlunCard: string

        :param isomerismCard:
            type of isomerismCard, including kunlunCard, fpgaCard, gpuCard
        :type isomerismCard: string

        :param isomerism_card:
            type of isomerismCard, including kunlunCard, fpgaCard, gpuCard.
        :type isomerism_card: string

        :param file_systems:
            This parameter is obsolete.
        :type file_systems:list<bcc_model.FileSystemModel>

        :param user_data:
        :type user_data: string

        :param is_open_hosteye:
        :type is_open_hosteye: boolean

        :param deletion_protection:
        :type deletion_protection: int

        :param res_group_id:
            The optional parameter to specify the resGroupId of the instance
        :type res_group_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        if billing is None:
            billing = default_billing_to_purchase_created
        if card_count == 1 and cardCount > 1:
            card_count = cardCount
        if isomerism_card is None:
            isomerism_card = isomerismCard
        body = {
            'cpuCount': cpu_count,
            'memoryCapacityInGB': memory_capacity_in_gb,
            'imageId': image_id,
            'billing': billing.__dict__
        }
        if spec is not None:
            body['spec'] = spec
        if eip_name is not None:
            body['eipName'] = eip_name
        if hostname is not None:
            body['hostname'] = hostname
        if auto_seq_suffix is not None:
            body['autoSeqSuffix'] = auto_seq_suffix
        if is_open_hostname_domain is not None:
            body['isOpenHostnameDomain'] = is_open_hostname_domain
        if relation_tag is not None:
            body['relationTag'] = relation_tag
        if is_open_ipv6 is not None:
            body['isOpenIpv6'] = is_open_ipv6
        if file_systems is not None:
            file_system_list = [file_system.__dict__ for file_system in file_systems]
            body['fileSystems'] = file_system_list
        if user_data is not None:
            body['userData'] = user_data
        if is_open_hosteye is not None:
            body['isOpenHosteye'] = is_open_hosteye
        if deletion_protection is not None:
            body['deletionProtection'] = deletion_protection
        if instance_type is not None:
            body['instanceType'] = instance_type
        if root_disk_size_in_gb != 0:
            body['rootDiskSizeInGb'] = root_disk_size_in_gb
        if root_disk_storage_type is not None:
            body['rootDiskStorageType'] = root_disk_storage_type
        if create_cds_list is not None:
            body['createCdsList'] = [create_cds.__dict__ for create_cds in create_cds_list]
        if network_capacity_in_mbps != 0:
            body['networkCapacityInMbps'] = network_capacity_in_mbps
        if purchase_count > 0:
            body['purchaseCount'] = purchase_count
        if name is not None:
            body['name'] = name
        if admin_pass is not None:
            secret_access_key = self.config.credentials.secret_access_key
            cipher_admin_pass = aes128_encrypt_16char_key(admin_pass, secret_access_key)
            body['adminPass'] = cipher_admin_pass
        if zone_name is not None:
            body['zoneName'] = zone_name
        if subnet_id is not None:
            body['subnetId'] = subnet_id
        if security_group_id is not None:
            body['securityGroupId'] = security_group_id
        if enterprise_security_group_id is not None:
            body['enterpriseSecurityGroupId'] = enterprise_security_group_id
        if security_group_ids is not None:
            body['securityGroupIds'] = security_group_ids
        if enterprise_security_group_ids is not None:
            body['enterpriseSecurityGroupIds'] = enterprise_security_group_ids
        if ehc_cluster_id is not None:
            body['ehcClusterId'] = ehc_cluster_id
        if gpuCard is not None:
            body['gpuCard'] = gpuCard
            body['cardCount'] = card_count if card_count > 1 else 1
        if fpgaCard is not None:
            body['fpgaCard'] = fpgaCard
            body['cardCount'] = card_count if card_count > 1 else 1
        if kunlunCard is not None:
            body['kunlunCard'] = kunlunCard
            body['cardCount'] = card_count if card_count > 1 else 1
        if isomerism_card is not None:
            body['isomerismCard'] = isomerism_card
            body['cardCount'] = card_count if card_count > 1 else 1
        if is_keep_image_login is not None:
            body['keepImageLogin'] = is_keep_image_login
        if auto_renew_time != 0:
            body['autoRenewTime'] = auto_renew_time
        if auto_renew_time_unit is None:
            body['autoRenewTimeUnit'] = "month"
        else:
            body['autoRenewTimeUnit'] = auto_renew_time_unit
        if ephemeral_disks is not None:
            body['ephemeralDisks'] = [ephemeral_disk.__dict__ for ephemeral_disk in ephemeral_disks]
        if dedicate_host_id is not None:
            body['dedicatedHostId'] = dedicate_host_id
        if deploy_id is not None:
            body['deployId'] = deploy_id
        if bid_model is not None:
            body['bidModel'] = bid_model
        if bid_price is not None:
            body['bidPrice'] = bid_price
        if key_pair_id is not None:
            body['keypairId'] = key_pair_id
        if internet_charge_type is not None:
            body['internetChargeType'] = internet_charge_type
        if asp_id is not None:
            body['aspId'] = asp_id
        if request_token is not None:
            body['requestToken'] = request_token
        if tags is not None:
            tag_list = [tag.__dict__ for tag in tags]
            body['tags'] = tag_list
        if internal_ips is not None:
            body['internalIps'] = internal_ips
        if res_group_id is not None:
            body['resGroupId'] = res_group_id
        body['cdsAutoRenew'] = cds_auto_renew

        return self._send_request(http_methods.POST, path, json.dumps(body),
                                  params=params, config=config)

    @required(cpu_count=int, memory_capacity_in_gb=int, dedicated_host_id=(bytes, str),  # ***Unicode***
              image_id=(bytes, str))  # ***Unicode***
    def create_instance_from_dedicated_host_with_encrypted_password(self, cpu_count, memory_capacity_in_gb, image_id,
                                                                    dedicated_host_id, ephemeral_disks=None,
                                                                    purchase_count=1, name=None, admin_pass=None,
                                                                    subnet_id=None, security_group_id=None,
                                                                    client_token=None, config=None):
        """
        Create a Instance from dedicatedHost with the specified options.
        You must fill the field of clientToken,which is especially for keeping idempotent.
        This is an asynchronous interface,
        you can get the latest status by BccClient.get_instance.

        :param cpu_count:
            The specified number of cpu core to create the instance,
            is less than or equal to the remain of dedicated host.
        :type cpu_count: int

        :param memory_capacity_in_gb:
            The capacity of memory to create the instance,
            is less than or equal to the remain of dedicated host.
        :type memory_capacity_in_gb: int

        :param image_id:
            The id of image, list all available image in BccClient.list_images.
        :type image_id: string

        :param dedicated_host_id:
            The id of dedicated host, we can locate the instance in specified dedicated host.
        :type dedicated_host_id: string

        :param ephemeral_disks:
            The optional list of ephemeral volume detail info to create.
        :type ephemeral_disks: list<bcc_model.EphemeralDisk>

        :param purchase_count:
            The number of instance to buy, the default value is 1.
        :type purchase_count: int

        :param name:
            The optional parameter to desc the instance that will be created.
        :type name: string

        :param admin_pass:
            The optional parameter to specify the password for the instance.
            If specify the adminPass,the adminPass must be a 8-16 characters String
            which must contains letters, numbers and symbols.
            The symbols only contains "!@#$%^*()".
            The adminPass will be encrypted in AES-128 algorithm
            with the substring of the former 16 characters of user SecretKey.
            If not specify the adminPass, it will be specified by an random string.
            See more detail on
            https://bce.baidu.com/doc/BCC/API.html#.7A.E6.31.D8.94.C1.A1.C2.1A.8D.92.ED.7F.60.7D.AF
        :type admin_pass: string

        :param subnet_id:
            The optional parameter to specify the id of subnet from vpc, optional param
             default value is default subnet from default vpc
        :type subnet_id: string

        :param security_group_id:
            The optional parameter to specify the securityGroupId of the instance
            vpcId of the securityGroupId must be the same as the vpcId of subnetId
            See more detail through listSecurityGroups method
        :type security_group_id: string

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if client token is provided.
            If the clientToken is not specified by the user,
            a random String generated by default algorithm will be used.
            See more detail at
            https://bce.baidu.com/doc/BCC/API.html#.E5.B9.82.E7.AD.89.E6.80.A7
        :type client_token: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            'cpuCount': cpu_count,
            'memoryCapacityInGB': memory_capacity_in_gb,
            'imageId': image_id,
            'dedicatedHostId': dedicated_host_id
        }
        if ephemeral_disks is not None:
            body['ephemeralDisks'] = ephemeral_disks
        if purchase_count > 0:
            body['purchaseCount'] = purchase_count
        if name is not None:
            body['name'] = name
        if subnet_id is not None:
            body['subnetId'] = subnet_id
        if security_group_id is not None:
            body['securityGroupId'] = security_group_id
        if admin_pass is not None:
            secret_access_key = self.config.credentials.secret_access_key
            cipher_admin_pass = aes128_encrypt_16char_key(admin_pass, secret_access_key)
            body['adminPass'] = cipher_admin_pass
        return self._send_request(http_methods.POST, path, json.dumps(body), params=params,
                                  config=config)

    @required(cpu_count=int, memory_capacity_in_gb=int, dedicated_host_id=(bytes, str),  # ***Unicode***
              image_id=(bytes, str))  # ***Unicode***
    def create_instance_from_dedicated_host(self, cpu_count, memory_capacity_in_gb, image_id,
                                            dedicated_host_id, ephemeral_disks=None,
                                            purchase_count=1, name=None, admin_pass=None,
                                            subnet_id=None, security_group_id=None,
                                            client_token=None, config=None):
        """
        Create a Instance from dedicatedHost with the specified options.
        You must fill the field of clientToken,which is especially for keeping idempotent.
        This is an asynchronous interface,
        you can get the latest status by BccClient.get_instance.

        :param cpu_count:
            The specified number of cpu core to create the instance,
            is less than or equal to the remain of dedicated host.
        :type cpu_count: int

        :param memory_capacity_in_gb:
            The capacity of memory to create the instance,
            is less than or equal to the remain of dedicated host.
        :type memory_capacity_in_gb: int

        :param image_id:
            The id of image, list all available image in BccClient.list_images.
        :type image_id: string

        :param dedicated_host_id:
            The id of dedicated host, we can locate the instance in specified dedicated host.
        :type dedicated_host_id: string

        :param ephemeral_disks:
            The optional list of ephemeral volume detail info to create.
        :type ephemeral_disks: list<bcc_model.EphemeralDisk>

        :param purchase_count:
            The number of instance to buy, the default value is 1.
        :type purchase_count: int

        :param name:
            The optional parameter to desc the instance that will be created.
        :type name: string

        :param admin_pass:
            The optional parameter to specify the password for the instance.
            If specify the adminPass,the adminPass must be a 8-16 characters String
            which must contains letters, numbers and symbols.
            The symbols only contains "!@#$%^*()".
            The adminPass will be encrypted in AES-128 algorithm
            with the substring of the former 16 characters of user SecretKey.
            If not specify the adminPass, it will be specified by an random string.
            See more detail on
            https://bce.baidu.com/doc/BCC/API.html#.7A.E6.31.D8.94.C1.A1.C2.1A.8D.92.ED.7F.60.7D.AF
        :type admin_pass: string

        :param subnet_id:
            The optional parameter to specify the id of subnet from vpc, optional param
             default value is default subnet from default vpc
        :type subnet_id: string

        :param security_group_id:
            The optional parameter to specify the securityGroupId of the instance
            vpcId of the securityGroupId must be the same as the vpcId of subnetId
            See more detail through listSecurityGroups method
        :type security_group_id: string

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if client token is provided.
            If the clientToken is not specified by the user,
            a random String generated by default algorithm will be used.
            See more detail at
            https://bce.baidu.com/doc/BCC/API.html#.E5.B9.82.E7.AD.89.E6.80.A7
        :type client_token: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            'cpuCount': cpu_count,
            'memoryCapacityInGB': memory_capacity_in_gb,
            'imageId': image_id,
            'dedicatedHostId': dedicated_host_id
        }
        if ephemeral_disks is not None:
            body['ephemeralDisks'] = ephemeral_disks
        if purchase_count > 0:
            body['purchaseCount'] = purchase_count
        if name is not None:
            body['name'] = name
        if admin_pass is not None:
            body['adminPass'] = admin_pass
        if subnet_id is not None:
            body['subnetId'] = subnet_id
        if security_group_id is not None:
            body['securityGroupId'] = security_group_id
        return self._send_request(http_methods.POST, path, json.dumps(body), params=params,
                                  config=config)

    @required(cpu_count=int,
              memory_capacity_in_gb=int,
              image_id=(bytes, str))  # ***Unicode***
    def create_instance_of_bid(self, cpu_count, memory_capacity_in_gb, image_id, instance_type=None,
                               billing=None, create_cds_list=None, root_disk_size_in_gb=0, root_disk_storage_type=None,
                               ephemeral_disks=None, dedicate_host_id=None, auto_renew_time_unit=None,
                               auto_renew_time=0,
                               deploy_id=None, bid_model=None, bid_price=None, key_pair_id=None, cds_auto_renew=False,
                               internet_charge_type=None, internal_ips=None, request_token=None, asp_id=None, tags=None,
                               network_capacity_in_mbps=0, purchase_count=1, cardCount=1, name=None, admin_pass=None,
                               zone_name=None, subnet_id=None, security_group_id=None, gpuCard=None, fpgaCard=None,
                               client_token=None, config=None, spec=None, user_data=None,
                               eip_name=None, hostname=None, auto_seq_suffix=False, is_open_hostname_domain=False,
                               spec_id=None, relation_tag=False, is_open_ipv6=False, deletion_protection=None,
                               enterprise_security_group_id=None, security_group_ids=None, res_group_id=None,
                               enterprise_security_group_ids=None, isomerismCard=None, file_systems=None,
                               card_count=1, isomerism_card=None, is_eip_auto_related_delete=False
                               , is_keep_image_login=None):
        """
        Create a bcc Instance with the specified options.
        You must fill the field of clientToken,which is especially for keeping idempotent.
        This is an asynchronous interface,
        you can get the latest status by BccClient.get_instance.

        :param instance_type:
            The specified Specification to create the instance,
            See more detail on
            https://cloud.baidu.com/doc/BCC/API.html#InstanceType
        :type instance_type: string

        :param cpu_count:
            The parameter to specified the cpu core to create the instance.
        :type cpu_count: int

        :param memory_capacity_in_gb:
            The parameter to specified the capacity of memory in GB to create the instance.
        :type memory_capacity_in_gb: int

        :param image_id:
            The id of image, list all available image in BccClient.list_images.
        :type image_id: string

        :param billing:
            Billing information.
        :type billing: bcc_model.Billing

        :param create_cds_list:
            The optional list of volume detail info to create.
        :type create_cds_list: list<bcc_model.CreateCdsModel>

        :param network_capacity_in_mbps:
            The optional parameter to specify the bandwidth in Mbps for the new instance.
            It must among 0 and 200, default value is 0.
            If it's specified to 0, it will get the internal ip address only.
        :type network_capacity_in_mbps: int

        :param purchase_count:
            The number of instance to buy, the default value is 1.
        :type purchase_count: int

        :param name:
            The optional parameter to desc the instance that will be created.
        :type name: string

        :param admin_pass:
            The optional parameter to specify the password for the instance.
            If specify the adminPass,the adminPass must be a 8-16 characters String
            which must contains letters, numbers and symbols.
            The symbols only contains "!@#$%^*()".
            The adminPass will be encrypted in AES-128 algorithm
            with the substring of the former 16 characters of user SecretKey.
            If not specify the adminPass, it will be specified by an random string.
            See more detail on
            https://bce.baidu.com/doc/BCC/API.html#.7A.E6.31.D8.94.C1.A1.C2.1A.8D.92.ED.7F.60.7D.AF
        :type admin_pass: string

        :param zone_name:
            The optional parameter to specify the available zone for the instance.
            See more detail through list_zones method
        :type zone_name: string

        :param subnet_id:
            The optional parameter to specify the id of subnet from vpc, optional param
             default value is default subnet from default vpc
        :type subnet_id: string

        :param security_group_id:
            The optional parameter to specify the securityGroupId of the instance
            vpcId of the securityGroupId must be the same as the vpcId of subnetId
            See more detail through listSecurityGroups method
        :type security_group_id: string

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if client token is provided.
            If the clientToken is not specified by the user,
            a random String generated by default algorithm will be used.
            See more detail at
            https://bce.baidu.com/doc/BCC/API.html#.E5.B9.82.E7.AD.89.E6.80.A7
        :type client_token: string

        :param fpgaCard:
            This parameter is obsolete. Use parameter isomerism_card instead.
        :type fpgaCard: string

        :param gpuCard:
            This parameter is obsolete. Use parameter isomerism_card instead.
        :type gpuCard: string

        :param cardCount:
            This parameter is obsolete. Use parameter card_count instead.
        :type cardCount: int

        :param card_count:
            The parameter to specify the card count for creating GPU/FPGA instance.
        :type card_count: int

        :param root_disk_size_in_gb:
            The parameter to specify the root disk size in GB.
            The root disk excludes the system disk, available is 40-500GB.
        :type root_disk_size_in_gb: int

        :param root_disk_storage_type:
            The parameter to specify the root disk storage type.
            Default use of HP1 cloud disk.
        :type root_disk_storage_type: string

        :param ephemeral_disks:
            The optional list of ephemeral volume detail info to create.
        :type ephemeral_disks: list<bcc_model.EphemeralDisk>

        :param dedicate_host_id:
            This parameter is obsolete.
        :type dedicate_host_id: string

        :param auto_renew_time_unit:
            This parameter is obsolete.
        :type auto_renew_time_unit: string

        :param auto_renew_time:
            This parameter is obsolete.
        :type auto_renew_time: string

        :param tags:
            The optional list of tag to be bonded.
        :type tags: list<bcc_model.TagModel>

        :param deploy_id:
            This parameter is obsolete.
        :type deploy_id: string

        :param bid_model:
            The parameter to specify the bidding model.
            The bidding model can be "market" or "custom".
        :type bid_model: string

        :param bid_price:
            The parameter to specify the bidding price.
            When the bid_model is "custom", it works.
        :type bid_price: string

        :param key_pair_id:
            The parameter to specify id of the keypair.
        :type key_pair_id: string

        :param asp_id:
            The parameter to specify id of the asp.
        :type asp_id: string

        :param request_token:
            The parameter to specify the request token which will make the request idempotent.
        :type request_token: string

        :param internet_charge_type:
            The parameter to specify the internet charge type.
            See more detail on
            https://cloud.baidu.com/doc/BCC/API.html#InternetChargeType
        :type internet_charge_type: string

        :param internal_ips:
            This parameter is obsolete.
        :type internal_ips: list<string>

        :param cds_auto_renew:
            This parameter is obsolete.
        :type cds_auto_renew: boolean

        :param spec:
            The parameter to specify Specification to create the instance.
        :type spec: string

        :param user_data:
            The parameter to specify instance custom data.
        :type user_data string

        :param hostname:
            The optional parameter to specify the host name of the instance virtual machine.
            By default, hostname is not specified.
            If hostname is specified: hostname is used as the prefix of the name in batches.
            The backend will add a suffix, and the suffix generation method is: name{-serial number}.
            If name is not specified, it will be automatically generated using the following method:
            {instance-eight-digit random string-serial number}.
            Note: The random string is generated from the characters 0-9 and a-z;
            the serial number increases sequentially according to the magnitude of count.
            If count is 100, the serial number increases from 000~100, and if it is 10, it increases from 00~10.
            Only lowercase letters, numbers and - . special characters are supported.
            They must start with a letter. Special symbols cannot be used continuously.
            Special symbols are not supported at the beginning or end. The length is 2-64.
        :type hostname: string

        :param auto_seq_suffix:
            The parameter to specify whether name and hostname order suffixes are automatically generated.
        :type auto_seq_suffix: boolean

        :param is_open_hostname_domain:
            The parameter to specify whether hostname domain is automatically generated
        :type is_open_hostname_domain: boolean

        :param spec_id:
            Identify of the spec.
        :type spec_id: string

        :param relation_tag:
            The parameter to specify whether the instance related to existing tags
        :type relation_tag: boolean

        :param is_open_ipv6:
            The parameter indicates whether the instance to be created is enabled for IPv6.
            It can only be enabled when both the image and subnet support IPv6.
            True indicates enabled, false indicates disabled,
            and no transmission indicates automatic adaptation of the image and subnet's IPv6 support
        :type is_open_ipv6: boolean

        :param deletion_protection:
            The status of instance deletion protection. 1:enable, 0:disable.
        :type deletion_protection: int

        :param eip_name:
            eip name
        :type eip_name: string

        :param isomerismCard:
            This parameter is obsolete. Use parameter isomerism_card instead.
        :type isomerismCard: string

        :param isomerism_card:
            The parameter to specify the card type for creating GPU/FPGA instance.
        :type isomerism_card: string

        :param enterprise_security_group_id:
        :type enterprise_security_group_id: string

        :param security_group_ids:
            security_group_ids
        :type security_group_ids: list<string>

        :param res_group_id:
            The optional parameter to specify the resGroupId of the instance
        :type res_group_id: string

        :param enterprise_security_group_ids:
            enterprise_security_group_ids
        :type enterprise_security_group_ids: list<string>

        :param file_systems:
            This parameter is obsolete.
        :type file_systems: list<bcc_model.FileSystemModel>

        :param is_eip_auto_related_delete:
            The parameter to specify whether to delete the relevant EIP after the bidding instance is automatically deleted.
        :type is_eip_auto_related_delete: boolean

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/bid'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        if billing is None:
            billing = default_billing_to_purchase_created
        if card_count == 1 and cardCount > 1:
            card_count = cardCount
        if isomerism_card is None:
            isomerism_card = isomerismCard
        body = {
            'cpuCount': cpu_count,
            'memoryCapacityInGB': memory_capacity_in_gb,
            'imageId': image_id,
            'billing': billing.__dict__
        }
        if hostname is not None:
            body['hostname'] = hostname
        if auto_seq_suffix is not None:
            body['autoSeqSuffix'] = auto_seq_suffix
        if is_open_hostname_domain is not None:
            body['isOpenHostnameDomain'] = is_open_hostname_domain
        if spec_id is not None:
            body['specId'] = spec_id
        if relation_tag is not None:
            body['relationTag'] = relation_tag
        if is_open_ipv6 is not None:
            body['isOpenIpv6'] = is_open_ipv6
        if deletion_protection is not None:
            body['deletionProtection'] = deletion_protection
        if eip_name is not None:
            body['eipName'] = eip_name
        if enterprise_security_group_id is not None:
            body['enterpriseSecurityGroupId'] = enterprise_security_group_id
        if isomerism_card is not None:
            body['isomerismCard'] = isomerism_card
        if file_systems is not None:
            file_system_list = [file_system.__dict__ for file_system in file_systems]
            body['fileSystems'] = file_system_list
        if instance_type is not None:
            body['instanceType'] = instance_type
        if root_disk_size_in_gb != 0:
            body['rootDiskSizeInGb'] = root_disk_size_in_gb
        if root_disk_storage_type is not None:
            body['rootDiskStorageType'] = root_disk_storage_type
        if create_cds_list is not None:
            body['createCdsList'] = [create_cds.__dict__ for create_cds in create_cds_list]
        if network_capacity_in_mbps != 0:
            body['networkCapacityInMbps'] = network_capacity_in_mbps
        if purchase_count > 0:
            body['purchaseCount'] = purchase_count
        if name is not None:
            body['name'] = name
        if admin_pass is not None:
            secret_access_key = self.config.credentials.secret_access_key
            cipher_admin_pass = aes128_encrypt_16char_key(admin_pass, secret_access_key)
            body['adminPass'] = cipher_admin_pass
        if zone_name is not None:
            body['zoneName'] = zone_name
        if subnet_id is not None:
            body['subnetId'] = subnet_id
        if security_group_id is not None:
            body['securityGroupId'] = security_group_id
        if security_group_ids is not None:
            body['securityGroupIds'] = security_group_ids
        if enterprise_security_group_ids is not None:
            body['enterpriseSecurityGroupIds'] = enterprise_security_group_ids
        if gpuCard is not None:
            body['gpuCard'] = gpuCard
            body['cardCount'] = card_count if card_count > 1 else 1
        if fpgaCard is not None:
            body['fpgaCard'] = fpgaCard
            body['cardCount'] = card_count if card_count > 1 else 1
        if auto_renew_time != 0:
            body['autoRenewTime'] = auto_renew_time
        if auto_renew_time_unit is None:
            body['autoRenewTimeUnit'] = "month"
        else:
            body['autoRenewTimeUnit'] = auto_renew_time_unit
        if ephemeral_disks is not None:
            body['ephemeralDisks'] = [ephemeral_disk.__dict__ for ephemeral_disk in ephemeral_disks]
        if dedicate_host_id is not None:
            body['dedicatedHostId'] = dedicate_host_id
        if deploy_id is not None:
            body['deployId'] = deploy_id
        if bid_model is not None:
            body['bidModel'] = bid_model
        if bid_price is not None:
            body['bidPrice'] = bid_price
        if key_pair_id is not None:
            body['keypairId'] = key_pair_id
        if internet_charge_type is not None:
            body['internetChargeType'] = internet_charge_type
        if asp_id is not None:
            body['aspId'] = asp_id
        if request_token is not None:
            body['requestToken'] = request_token
        if tags is not None:
            tag_list = [tag.__dict__ for tag in tags]
            body['tags'] = tag_list
        if internal_ips is not None:
            body['internalIps'] = internal_ips
        body['cdsAutoRenew'] = cds_auto_renew
        if spec is not None:
            body['spec'] = spec
        if user_data is not None:
            body['userData'] = user_data
        if res_group_id is not None:
            body['resGroupId'] = res_group_id
        if is_keep_image_login is not None:
            body['keepImageLogin'] = is_keep_image_login
        body['isEipAutoRelatedDelete'] = is_eip_auto_related_delete

        return self._send_request(http_methods.POST, path, json.dumps(body),
                                  params=params, config=config)

    def list_instances(self, marker=None, max_keys=None, internal_ip=None, dedicated_host_id=None,
                       zone_name=None, instance_ids=None, instance_names=None, cds_ids=None, ehc_cluster_id=None,
                       deployset_ids=None, security_group_ids=None, payment_timing=None, status=None, tags=None,
                       vpc_id=None, private_ips=None, ipv6_addresses=None, auto_renew=None, fuzzy_instance_name=None,
                       config=None):
        """
        Return a list of instances owned by the authenticated user.

        :param marker:
            The optional parameter marker specified in the original request to specify
            where in the results to begin listing.
            Together with the marker, specifies the list result which listing should begin.
            If the marker is not specified, the list result will listing from the first one.
        :type marker: string

        :param max_keys:
            The optional parameter to specifies the max number of list result to return.
            The default value is 1000.
        :type max_keys: int

        :param internal_ip:
            The identified internal ip of instance.
        :type internal_ip: string

        :param dedicated_host_id:
            get instance list filtered by id of dedicated host
        :type dedicated_host_id: string

        :param zone_name:
            get instance list filtered by name of available zone
        :type zone_name: string

        :param instance_ids:
            filter instance list with multiple instance ids join by ','
        :type instance_ids: string

        :param instance_names:
            filter instance list with multiple instance names join by ','
        :type instance_names: string

        :param cds_ids:
            filter instance list with multiple cds ids join by ','
        :type cds_ids: string

        :param ehc_cluster_id:
            get instance list filtered by id of ehc cluster
        :type ehc_cluster_id: string

        :param deployset_ids:
            filter instance list with multiple deployset ids join by ','
        :type deployset_ids: string

        :param security_group_ids:
            filter instance list with multiple securityGroup ids join by ','
        :type security_group_ids: string

        :param payment_timing:
            filter instance list with multiple type of paymentTiming join by ','
        :type payment_timing: string

        :param status:
            filter instance list with multiple instance status join by ','
        :type status: string

        :param tags:
            filter instance list with multiple tags join by ',', the format of tag can be :
            tagKey:tagValue or tagKey
        :type tags: string

        :param vpc_id:
            filter instance list with vpc id, the parameter should be used with private_ips
        :type vpc_id: string

        :param private_ips:
            filter instance list with multiple private ips join by ',', the parameter should be used with
            vpc_id
        :type private_ips: string

        :param ipv6_addresses:
            filter instance list with multiple ipv6 private ips join by ',', the parameter should be used with
            vpc_id
        :type ipv6_addresses: string

        :param auto_renew:
        :type auto_renew: boolean

        :param fuzzy_instance_name:
            filter instance list with fuzzy instance name
        :type fuzzy_instance_name: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance'
        params = {}

        if marker is not None:
            params['marker'] = marker
        if max_keys is not None:
            params['maxKeys'] = max_keys
        if internal_ip is not None:
            params['internalIp'] = internal_ip
        if dedicated_host_id is not None:
            params['dedicatedHostId'] = dedicated_host_id
        if zone_name is not None:
            params['zoneName'] = zone_name
        if instance_ids is not None:
            params['instanceIds'] = instance_ids
        if instance_names is not None:
            params['instanceNames'] = instance_names
        if cds_ids is not None:
            params['cdsIds'] = cds_ids
        if ehc_cluster_id is not None:
            params['ehcClusterId'] = ehc_cluster_id
        if deployset_ids is not None:
            params['deploySetIds'] = deployset_ids
        if security_group_ids is not None:
            params['securityGroupIds'] = security_group_ids
        if payment_timing is not None:
            params['paymentTiming'] = payment_timing
        if status is not None:
            params['status'] = status
        if tags is not None:
            params['tags'] = tags
        if vpc_id is not None:
            params['vpcId'] = vpc_id
        if private_ips is not None:
            params['privateIps'] = private_ips
        if ipv6_addresses is not None:
            params['ipv6Addresses'] = ipv6_addresses
        if auto_renew is not None:
            params['autoRenew'] = auto_renew
        if fuzzy_instance_name is not None:
            params['fuzzyInstanceName'] = fuzzy_instance_name
        return self._send_request(http_methods.GET, path, params=params, config=config)

    @required(instance_id=(bytes, str))  # ***Unicode***
    def get_instance(self, instance_id, contains_failed=False, config=None):
        """
        Get the detail information of specified instance.

        :param instance_id:
            The id of instance.
        :type instance_id: string

        :param contains_failed:
            The optional parameters to get the failed message.If true, it means get the failed message.
        :type contains_failed: boolean

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        instance_id = instance_id.encode(encoding='utf-8')
        path = b'/instance/%s' % instance_id
        params = {}

        if contains_failed:
            params['containsFailed'] = contains_failed

        return self._send_request(http_methods.GET, path, params=params, config=config)

    @required(instance_id=(bytes, str))  # ***Unicode***s
    def start_instance(self, instance_id, config=None):
        """
        Starting the instance owned by the user.
        You can start the instance only when the instance is Stopped,
        otherwise, it's will get 409 errorCode.
        This is an asynchronous interface,
        you can get the latest status by BccClient.get_instance.

        :param instance_id: id of instance proposed to start
        :type instance_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        instance_id = compat.convert_to_bytes(instance_id)
        path = b'/instance/%s' % instance_id
        params = {
            'start': None
        }
        return self._send_request(http_methods.PUT, path, params=params, config=config)

    @required(instance_id=(bytes, str))  # ***Unicode***
    def stop_instance(self, instance_id, force_stop=False, stopWithNoCharge=False, config=None):
        """
        Stopping the instance owned by the user.
        You can stop the instance only when the instance is Running,
        otherwise, it's will get 409 errorCode.
        This is an asynchronous interface,
        you can get the latest status by BccClient.get_instance.

        :param instance_id:
            The id of instance.
        :type instance_id: string

        :param force_stop:
            The optional parameter to stop the instance forcibly.If true,
            it will stop the instance just like power off immediately
            and it may result in losing important data which have not been written to disk.
        :type force_stop: boolean

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        instance_id = compat.convert_to_bytes(instance_id)
        path = b'/instance/%s' % instance_id
        body = {
            'forceStop': force_stop,
            'stopWithNoCharge': stopWithNoCharge
        }
        params = {
            'stop': None
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(instance_id=(bytes, str))  # ***Unicode***
    def reboot_instance(self, instance_id, force_stop=False, config=None):
        """
        Rebooting the instance owned by the user.
        You can reboot the instance only when the instance is Running,
        otherwise, it's will get 409 errorCode.
        This is an asynchronous interface,
        you can get the latest status by BccClient.get_instance.

        :param instance_id:
            The id of instance.
        :type instance_id: string

        :param force_stop:
            The optional parameter to stop the instance forcibly.If true,
            it will stop the instance just like power off immediately
            and it may result in losing important data which have not been written to disk.
        :type force_stop: boolean

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        instance_id = compat.convert_to_bytes(instance_id)
        path = b'/instance/%s' % instance_id
        body = {
            'forceStop': force_stop
        }
        params = {
            'reboot': None
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(instance_id=str)
    def batch_add_ip(self, instance_id, private_ips=None, secondary_private_ip_address_count=None,
                     allocate_multi_ipv6_addr=None, config=None):
        """
        batch_add_ip

        :param instance_id:
            The id of instance.
        :type instance_id: string

        :param private_ips:
            The IPV6/IPV4 address that needs to be added must exist with secondary_private_ip_address_count.
        :type private_ips: list

        :param secondary_private_ip_address_count:
            The number of IPV6/IPV4 needs to be increased, and one with private_ips must exist.
        :type secondary_private_ip_address_count: list

        :param allocate_multi_ipv6_addr:
            The parameter indicates whether to support multiple IPV6.
            It must be true to create IPV6.
        :type allocate_multi_ipv6_addr: bool

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/batchAddIp'
        body = {
            'instanceId': instance_id,
        }
        if private_ips is not None:
            body['privateIps'] = private_ips
        if secondary_private_ip_address_count is not None:
            body['secondaryPrivateIpAddressCount'] = secondary_private_ip_address_count
        if allocate_multi_ipv6_addr is not None:
            body['allocateMultiIpv6Addr'] = allocate_multi_ipv6_addr
        params = {

        }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(instance_id=str, private_ips=list)
    def batch_delete_ip(self, instance_id, private_ips, config=None):
        """
        :param instance_id:
        :param private_ips:
        :param config:
        :return:
        """
        path = b'/instance/batchDelIp'
        body = {
            'instanceId': instance_id,
            'privateIps': private_ips,
        }
        params = {

        }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(instance_id=(bytes, str),  # ***Unicode***
              admin_pass=(bytes, str))  # ***Unicode***
    def modify_instance_password(self, instance_id, admin_pass, config=None):
        """
        Modifying the password of the instance.
        You can change the instance password only when the instance is Running or Stopped ,
        otherwise, it's will get 409 errorCode.
        This is an asynchronous interface,
        you can get the latest status by BccClient.get_instance.

        :param instance_id:
            The id of instance.
        :type instance_id: string

        :param admin_pass:
            The new password to update.
            The adminPass will be encrypted in AES-128 algorithm
            with the substring of the former 16 characters of user SecretKey.
        :type admin_pass: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        instance_id = compat.convert_to_bytes(instance_id)
        secret_access_key = self.config.credentials.secret_access_key
        cipher_admin_pass = aes128_encrypt_16char_key(admin_pass, secret_access_key)
        path = b'/instance/%s' % instance_id
        body = {
            'adminPass': cipher_admin_pass
        }
        params = {
            'changePass': None
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(instance_id=(bytes, str),  # ***Unicode***
              name=(bytes, str))  # ***Unicode***
    def modify_instance_attributes(self, instance_id, name=None, neteth_queuecount=None,
                                   enable_jumbo_frame=None, config=None):
        """
        Modifying the special attribute to new value of the instance.
        You can reboot the instance only when the instance is Running or Stopped ,
        otherwise, it's will get 409 errorCode.

        :param instance_id:
            The id of instance.
        :type instance_id: string

        :param name:
            The new value for instance's name.
        :type name: string

        :param neteth_queuecount:
            The new value for instance's neteth_queuecount.
        :type neteth_queuecount: string

        :param enable_jumbo_frame:
            The parameter indicates whether the instance is enabled for JumboFrame.
            It can only be enabled when the flavor support JumboFrame.
            True indicates enabled, false indicates disabled,
        :type enable_jumbo_frame: bool


        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        instance_id = compat.convert_to_bytes(instance_id)
        path = b'/instance/%s' % instance_id
        body = {
            'name': name,
            'netEthQueueCount': neteth_queuecount
        }
        if enable_jumbo_frame is not None:
            body['enableJumboFrame'] = enable_jumbo_frame
        params = {
            'modifyAttribute': None
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(instance_id=(bytes, str),
              desc=(bytes, str))
    def modify_instance_desc(self, instance_id, desc, config=None):
        """
        Modifying the description of the instance.
        You can reboot the instance only when the instance is Running or Stopped ,
        otherwise, it's will get 409 errorCode.

        :param instance_id:
            The id of instance.
        :type instance_id: string

        :param desc:
            The new value for instance's description.
        :type name: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        instance_id = compat.convert_to_bytes(instance_id)
        path = b'/instance/%s' % instance_id
        body = {
            'desc': desc
        }
        params = {
            'modifyDesc': None
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(instance_id=(bytes, str),  # ***Unicode***
              image_id=(bytes, str))  # ***Unicode***
    def rebuild_instance(self, instance_id, image_id, admin_pass=None, key_pair_id=None,
                         config=None):
        """
        Rebuilding the instance owned by the user.
        After rebuilding the instance,
        all of snapshots created from original instance system disk will be deleted,
        all of customized images will be saved for using in the future.
        This is an asynchronous interface,
        you can get the latest status by BccClient.get_instance.

        :param instance_id:
            The id of instance.
        :type instance_id: string

        :param image_id:
            The id of the image which is used to rebuild the instance.
        :type image_id: string

        :param admin_pass:
            The admin password to login the instance.
            The admin password will be encrypted in AES-128 algorithm
            with the substring of the former 16 characters of user SecretKey.
            See more detail on
            https://bce.baidu.com/doc/BCC/API.html#.7A.E6.31.D8.94.C1.A1.C2.1A.8D.92.ED.7F.60.7D.AF
        :type admin_pass: string

        :param key_pair_id:
            key_pair_id or admin_pass is required for rebuild instance.
        :type key_pair_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        instance_id = compat.convert_to_bytes(instance_id)
        path = b'/instance/%s' % instance_id
        body = {
            'imageId': image_id,
        }
        if key_pair_id is not None:
            body['keypairId'] = key_pair_id
        if admin_pass is not None:
            secret_access_key = self.config.credentials.secret_access_key
            cipher_admin_pass = aes128_encrypt_16char_key(admin_pass, secret_access_key)
            body['adminPass'] = cipher_admin_pass
        params = {
            'rebuild': None
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(instance_id=(bytes, str))  # ***Unicode***
    def release_instance(self, instance_id, config=None):
        """
        Releasing the instance owned by the user.
        Only the Postpaid instance or Prepaid which is expired can be released.
        After releasing the instance,
        all of the data will be deleted.
        all of volumes attached will be auto detached, but the volume snapshots will be saved.
        all of snapshots created from original instance system disk will be deleted,
        all of customized images created from original instance system disk will be reserved.

        :param instance_id:
            The id of instance.
        :type instance_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        instance_id = compat.convert_to_bytes(instance_id)
        path = b'/instance/%s' % instance_id
        return self._send_request(http_methods.DELETE, path, config=config)

    @required(instance_id=(bytes, str),  # ***Unicode***
              cpu_count=int,
              memory_capacity_in_gb=int)
    def resize_instance(self, instance_id, cpu_count, memory_capacity_in_gb,
                        live_resize=None, gpu_card_count=None, ephemeral_disk_in_gb=None,
                        enable_jumbo_frame=None,
                        client_token=None, config=None):
        """
        Resizing the instance owned by the user.
        The Prepaid instance can not be downgrade.
        Only the Running/Stopped instance can be resized, otherwise, it's will get 409 errorCode.
        After resizing the instance,it will be reboot once.
        This is an asynchronous interface,
        you can get the latest status by BccClient.get_instance.

        :param instance_id:
            The id of instance.
        :type instance_id: string

        :param cpu_count:
            The parameter of specified the cpu core to resize the instance.
        :type cpu_count: int

        :param memory_capacity_in_gb:
            The parameter of specified the capacity of memory in GB to resize the instance.
        :type memory_capacity_in_gb: int

        :param enable_jumbo_frame:
            The parameter of specified the instance enable/disable jumbo frame.
            True means enable jumbo frame, false means disable jumbo frame.
            enable_jumbo_frame default None which means:
            When you change to the spec which doesn't support jumbo frame, the jumbo frame will be disabled.
            When the original instance don't support jumbo frame and you change to the spec which support jumbo frame,
            the jumbo frame will be disabled.
            When the original spec of the instance support jumbo frame , then you change to the spec which support jumbo
            frame, if the original instance enable jumbo frame, the jumbo frame will be enabled, if the original instance
            disable jumbo frame, the jumbo frame will be disabled.
        :type enable_jumbo_frame: bool

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if client token is provided.
            If the clientToken is not specified by the user,
            a random String generated by default algorithm will be used.
            See more detail at
            https://bce.baidu.com/doc/BCC/API.html#.E5.B9.82.E7.AD.89.E6.80.A7
        :type client_token: string

        :param live_resize:
        :type live_resize: boolean

        :param gpu_card_count:
        :type gpu_card_count: int

        :param ephemeral_disk_in_gb:
        :type ephemeral_disk_in_gb: int

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        instance_id = compat.convert_to_bytes(instance_id)
        path = b'/instance/%s' % instance_id
        body = {
            'cpuCount': cpu_count,
            'memoryCapacityInGB': memory_capacity_in_gb
        }
        if live_resize is not None:
            body['liveResize'] = live_resize
        if gpu_card_count is not None:
            body['gpuCardCount'] = gpu_card_count
        if ephemeral_disk_in_gb is not None:
            body['ephemeralDiskInGb'] = ephemeral_disk_in_gb
        if enable_jumbo_frame is not None:
            body['enableJumboFrame'] = enable_jumbo_frame
        params = None
        if client_token is None:
            params = {
                'resize': None,
                'clientToken': generate_client_token()
            }
        else:
            params = {
                'resize': None,
                'clientToken': client_token
            }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(instance_id=(bytes, str),  # ***Unicode***
              security_group_id=(bytes, str))  # ***Unicode***
    def bind_instance_to_security_group(self, instance_id, security_group_id, config=None):
        """
        Binding the instance to specified securitygroup.

        :param instance_id:
            The id of the instance.
        :type instance_id: string

        :param securitygroup_id:
            The id of the securitygroup.
        :type securitygroup_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        instance_id = compat.convert_to_bytes(instance_id)
        path = b'/instance/%s' % instance_id
        body = {
            'securityGroupId': security_group_id
        }
        params = {
            'bind': None
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(instance_id=(bytes, str),  # ***Unicode***
              security_group_id=(bytes, str))  # ***Unicode***
    def unbind_instance_from_security_group(self, instance_id, security_group_id, config=None):
        """
        Unbinding the instance from securitygroup.

        :param instance_id:
            The id of the instance.
        :type instance_id: string

        :param securitygroup_id:
            The id of the securitygroup.
        :type securitygroup_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        instance_id = compat.convert_to_bytes(instance_id)
        path = b'/instance/%s' % instance_id
        body = {
            'securityGroupId': security_group_id
        }
        params = {
            'unbind': None
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(reserved_instance_ids=list,
              tags=list)
    def bind_reserved_instance_to_tags(self, reserved_instance_ids, tags, config=None):
        """
        :param reserved_instance_ids:
        :param tags:
        :param config:
        :return:
        """
        path = b'/bcc/reserved/tag'
        tag_list = [tag.__dict__ for tag in tags]
        body = {
            'changeTags': tag_list,
            'reservedInstanceIds': reserved_instance_ids
        }
        params = {
            'bind': None
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(reserved_instance_ids=list,
              tags=list)
    def unbind_reserved_instance_from_tags(self, reserved_instance_ids, tags, config=None):
        """
        :param reserved_instance_ids:
        :param tags:
        :param config:
        :return:
        """
        path = b'/bcc/reserved/tag'
        tag_list = [tag.__dict__ for tag in tags]
        body = {
            'changeTags': tag_list,
            'reservedInstanceIds': reserved_instance_ids
        }
        params = {
            'unbind': None
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    def bind_tags_batch_by_resource_type(self, resource_type, resource_ids, tags, is_relation_tag, config=None):
        """
        :param resource_type:
        :param resource_ids:
        :param tags:
        :param is_relation_tag:
        :param config:
        :return:
        """
        path = b'/bcc/tag'
        tag_list = [tag.__dict__ for tag in tags]
        body = {
            'resourceType': resource_type,
            'resourceIds': resource_ids,
            'tags': tag_list,
            'isRelationTag': is_relation_tag
        }
        params = {
            'action': 'AttachTags'
        }
        return self._send_request(http_methods.POST, path, json.dumps(body),
                                  params=params, config=config, prefix=self.prefix_v3)

    def unbind_tags_batch_by_resource_type(self, resource_type, resource_ids, tags, is_relation_tag, config=None):
        """
        :param resource_type:
        :param resource_ids:
        :param tags:
        :param is_relation_tag:
        :param config:
        :return:
        """
        path = b'/bcc/tag'
        tag_list = [tag.__dict__ for tag in tags]
        body = {
            'resourceType': resource_type,
            'resourceIds': resource_ids,
            'tags': tag_list,
            'isRelationTag': is_relation_tag
        }
        params = {
            'action': 'DetachTags'
        }
        return self._send_request(http_methods.POST, path, json.dumps(body),
                                  params=params, config=config, prefix=self.prefix_v3)

    @required(instance_id=(bytes, str),
              tags=list)
    def bind_instance_to_tags(self, instance_id, tags, config=None):
        """
        :param instance_id:
        :param tags:
        :param config:
        :return:
        """
        instance_id = compat.convert_to_bytes(instance_id)
        path = b'/instance/%s/tag' % instance_id
        tag_list = [tag.__dict__ for tag in tags]
        body = {
            'changeTags': tag_list
        }
        params = {
            'bind': None
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(instance_id=(bytes, str),
              tags=list)
    def unbind_instance_from_tags(self, instance_id, tags, config=None):
        """
        :param instance_id:
        :param tags:
        :param config:
        :return:
        """
        instance_id = compat.convert_to_bytes(instance_id)
        path = b'/instance/%s/tag' % instance_id
        tag_list = [tag.__dict__ for tag in tags]
        body = {
            'changeTags': tag_list
        }
        params = {
            'unbind': None
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(instance_id=(bytes, str))  # ***Unicode***
    def get_instance_vnc(self, instance_id, config=None):
        """
        Getting the vnc url to access the instance.
        The vnc url can be used once.

        :param instance_id:
            The id of the instance.
        :type instance_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        instance_id = compat.convert_to_bytes(instance_id)
        path = b'/instance/%s/vnc' % instance_id
        return self._send_request(http_methods.GET, path, config=config)

    @required(instance_id=(bytes, str))  # ***Unicode***
    def purchase_reserved_instance(self,
                                   instance_id,
                                   billing=None,
                                   related_renew_flag=None,
                                   client_token=None,
                                   config=None,
                                   cds_custom_period=None):
        """
        PurchaseReserved the instance with fixed duration.
        You can not purchaseReserved the instance which is resizing.
        This is an asynchronous interface,
        you can get the latest status by BccClient.get_instance.

        :param instance_id:
            The id of the instance.
        :type instance_id: string

        :param billing:
            Billing information.
        :type billing: bcc_model.Billing

        :param related_renew_flag:
            Detailed information see: https://cloud.baidu.com/doc/BCC/s/6jwvyo0q2#relatedrenewflag
        :type related_renew_flag: string

        :param cds_custom_period:
            Custom renew period for CDS.
        :type cds_custom_period: list

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if client token is provided.
            If the clientToken is not specified by the user,
            a random String generated by default algorithm will be used.
            See more detail at
            https://bce.baidu.com/doc/BCC/API.html#.E5.B9.82.E7.AD.89.E6.80.A7
        :type client_token: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        instance_id = compat.convert_to_bytes(instance_id)
        path = b'/instance/%s' % instance_id
        if billing is None:
            billing = default_billing_to_purchase_reserved
        cds_custom_period_list = []
        if cds_custom_period is not None:
            cds_custom_period_list = [custom_period.__dict__ for custom_period in cds_custom_period]
        body = {
            'billing': billing.__dict__,
            "cdsCustomPeriod": cds_custom_period_list
        }
        params = None
        if client_token is None:
            params = {
                'purchaseReserved': None,
                'clientToken': generate_client_token()
            }
        else:
            params = {
                'purchaseReserved': None,
                'clientToken': client_token
            }
        if related_renew_flag is not None:
            params['relatedRenewFlag'] = related_renew_flag
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    def list_instance_specs(self, config=None):
        """
        The interface will be deprecated in the future,
        we suggest to use triad (instanceType, cpuCount, memoryCapacityInGB) to specified the instance configuration.
        Listing all of specification for instance resource to buy.
        See more detail on
        https://bce.baidu.com/doc/BCC/API.html#.E5.AE.9E.E4.BE.8B.E5.A5.97.E9.A4.90.E8.A7.84.E6.A0.BC

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/spec'
        return self._send_request(http_methods.GET, path, config=config)

    @required(cds_size_in_gb=int)
    def create_volume_with_cds_size(self, cds_size_in_gb, billing=None, purchase_count=1,
                                    storage_type='hp1', zone_name=None,
                                    instance_id=None, encrypt_key=None, name=None,
                                    description=None, renew_time_unit=None, renew_time=None,
                                    cluster_id=None, relation_tag=False,
                                    tags=None, auto_snapshot_policy=None,
                                    client_token=None, config=None, charge_type=None):
        """
        Create a volume with the specified options.
        You can use this method to create a new empty volume by specified options
        or you can create a new volume from customized volume snapshot but not system disk snapshot.
        By using the cdsSizeInGB parameter you can create a newly empty volume.
        By using snapshotId parameter to create a volume form specific snapshot.

        :param cds_size_in_gb:
            The size of volume to create in GB.
            By specifying the snapshotId,
            it will create volume from the specified snapshot and the parameter cdsSizeInGB will be ignored.
        :type cds_size_in_gb: int

        :param billing:
            Billing information.Deprecated
        :type billing: bcc_model.Billing

        :param purchase_count:
            The optional parameter to specify how many volumes to buy, default value is 1.
            The maximum to create for one time is 5.
        :type purchase_count: int

        :param storage_type:
            The storage type of volume, see more detail in
            https://bce.baidu.com/doc/BCC/API.html#StorageType
        :type storage_type: menu{'hp1', 'std1'}

        :param zone_name:
            The optional parameter to specify the available zone for the volume.
            See more detail through list_zones method
        :type zone_name: string

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if client token is provided.
            If the clientToken is not specified by the user,
            a random String generated by default algorithm will be used.
            See more detail at
            https://bce.baidu.com/doc/BCC/API.html#.E5.B9.82.E7.AD.89.E6.80.A7
        :type client_token: string

        :param instance_id:
        :type instance_id: string

        :param encrypt_key:
        :type encrypt_key: string

        :param name:
        :type name: string

        :param description:
        :type description: string

        :param renew_time_unit:
        :type renew_time_unit: string

        :param renew_time:
        :type renew_time: int

        :param cluster_id:
            cds cluster id
        :type cluster_id: string

        :param relation_tag:
        :type relation_tag: boolean

        :param tags:
            The optional list of tag to be bonded.
        :type tags: list<bcc_model.TagModel>

        :param auto_snapshot_policy:
            The optional auto snapshot policy to be bonded.
        :type auto_snapshot_policy: bcc_model.AutoSnapshotPolicyModel

        :param charge_type:
            The optional parameter to specify the payment for the volume.
            The billing type and payment method, including Prepaid and Postpaid,
            need to be specified only when the instanceId is not empty and the corresponding instance type is prepaid.
            If instanceId is empty:
               create a post payment type CDS;
            If the instanceId is not empty:
              If the instance is prepaid, a chargeType needs to be specified;
              If the instance is post paid, create a post paid CDS
        :type charge_type: menu{'Prepaid', 'Postpaid'}

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/volume'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        if billing is None:
            billing = default_billing_to_purchase_created
        body = {
            'cdsSizeInGB': cds_size_in_gb,
            'billing': billing.__dict__
        }
        if purchase_count is not None:
            body['purchaseCount'] = purchase_count
        if storage_type is not None:
            body['storageType'] = storage_type
        if zone_name is not None:
            body['zoneName'] = zone_name
        if renew_time_unit is not None:
            body['renewTimeUnit'] = renew_time_unit
        if renew_time is not None:
            body['renewTime'] = renew_time
        if cluster_id is not None:
            body['clusterId'] = cluster_id
        if relation_tag is not None:
            body['relationTag'] = relation_tag
        if tags is not None:
            tag_list = [tag.__dict__ for tag in tags]
            body['tags'] = tag_list
        if auto_snapshot_policy is not None:
            body['autoSnapshotPolicy'] = auto_snapshot_policy.__dict__
        if name is not None:
            body['name'] = name
        if description is not None:
            body['description'] = description
        if encrypt_key is not None:
            body['encryptKey'] = encrypt_key
        if instance_id is not None:
            body['instanceId'] = instance_id
        if charge_type is not None:
            body['chargeType'] = charge_type
        return self._send_request(http_methods.POST, path, json.dumps(body),
                                  params=params, config=config)

    @required(snapshot_id=(bytes, str))  # ***Unicode***
    def create_volume_with_snapshot_id(self, snapshot_id, billing=None, purchase_count=1,
                                       storage_type='hp1', zone_name=None, client_token=None,
                                       instance_id=None, encrypt_key=None, name=None,
                                       description=None, renew_time_unit=None, renew_time=None,
                                       cluster_id=None, relation_tag=False,
                                       tags=None, auto_snapshot_policy=None,
                                       config=None, charge_type=None):
        """
        Create a volume with the specified options.
        You can use this method to create a new empty volume by specified options
        or you can create a new volume from customized volume snapshot but not system disk snapshot.
        By using the cdsSizeInGB parameter you can create a newly empty volume.
        By using snapshotId parameter to create a volume form specific snapshot.

        :param snapshot_id:xx
            The id of snapshot.
            By specifying the snapshotId,
            it will create volume from the specified snapshot and the parameter cdsSizeInGB will be ignored.
        :type snapshot_id: string

        :param billing:
            Billing information.Deprecated
        :type billing: bcc_model.Billing

        :param purchase_count:
            The optional parameter to specify how many volumes to buy, default value is 1.
            The maximum to create for one time is 5.
        :type purchase_count: int

        :param storage_type:
            The storage type of volume, see more detail in
            https://bce.baidu.com/doc/BCC/API.html#StorageType
        :type storage_type: menu{'hp1', 'std1'}

        :param zone_name:
            The optional parameter to specify the available zone for the volume.
            See more detail through list_zones method
        :type zone_name: string

        :param instance_id:
        :type instance_id: string

        :param encrypt_key:
        :type encrypt_key: string

        :param name:
        :type name: string

        :param description:
        :type description: string

        :param renew_time_unit:
        :type renew_time_unit: string

        :param renew_time:
        :type renew_time: int

        :param cluster_id:
            cds cluster id
        :type cluster_id: string

        :param relation_tag:
        :type relation_tag: boolean

        :param tags:
            The optional list of tag to be bonded.
        :type tags: list<bcc_model.TagModel>

        :param auto_snapshot_policy:
            The optional auto snapshot policy to be bonded.
        :type auto_snapshot_policy: bcc_model.AutoSnapshotPolicyModel

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if client token is provided.
            If the clientToken is not specified by the user,
            a random String generated by default algorithm will be used.
            See more detail at
            https://bce.baidu.com/doc/BCC/API.html#.E5.B9.82.E7.AD.89.E6.80.A7
        :type client_token: string

        :param charge_type:
            The optional parameter to specify the payment for the volume.
            The billing type and payment method, including Prepaid and Postpaid,
            need to be specified only when the instanceId is not empty and the corresponding instance type is prepaid.
            If instanceId is empty:
               create a post payment type CDS;
            If the instanceId is not empty:
              If the instance is prepaid, a chargeType needs to be specified;
              If the instance is post paid, create a post paid CDS
        :type charge_type: menu{'Prepaid', 'Postpaid'}

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/volume'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        if billing is None:
            billing = default_billing_to_purchase_created
        body = {
            'snapshotId': snapshot_id,
            'billing': billing.__dict__
        }
        if purchase_count is not None:
            body['purchaseCount'] = purchase_count
        if storage_type is not None:
            body['storageType'] = storage_type
        if zone_name is not None:
            body['zoneName'] = zone_name
        if renew_time_unit is not None:
            body['renewTimeUnit'] = renew_time_unit
        if renew_time is not None:
            body['renewTime'] = renew_time
        if cluster_id is not None:
            body['clusterId'] = cluster_id
        if relation_tag is not None:
            body['relationTag'] = relation_tag
        if tags is not None:
            tag_list = [tag.__dict__ for tag in tags]
            body['tags'] = tag_list
        if auto_snapshot_policy is not None:
            body['autoSnapshotPolicy'] = auto_snapshot_policy.__dict__
        if name is not None:
            body['name'] = name
        if description is not None:
            body['description'] = description
        if encrypt_key is not None:
            body['encryptKey'] = encrypt_key
        if instance_id is not None:
            body['instanceId'] = instance_id
        if charge_type is not None:
            body['chargeType'] = charge_type
        return self._send_request(http_methods.POST, path, json.dumps(body),
                                  params=params, config=config)

    def list_volumes(self, instance_id=None, zone_name=None, marker=None, max_keys=None,
                     cluster_id=None,
                     volume_ids=None,
                     config=None):
        """
        Listing volumes owned by the authenticated user.

        :param instance_id:
            The id of instance. The optional parameter to list the volume.
            If it's specified,only the volumes attached to the specified instance will be listed.
        :type instance_id: string

        :param zone_name:
            The name of available zone. The optional parameter to list volumes
        :type zone_name: string

        :param marker:
            The optional parameter marker specified in the original request to specify
            where in the results to begin listing.
            Together with the marker, specifies the list result which listing should begin.
            If the marker is not specified, the list result will listing from the first one.
        :type marker: string

        :param max_keys:
            The optional parameter to specifies the max number of list result to return.
            The default value is 1000.
        :type max_keys: int

        :param cluster_id:
        :type cluster_id: string

        :param volume_ids:
        :type volume_ids: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/volume'
        params = {}
        if instance_id is not None:
            params['instanceId'] = instance_id
        if zone_name is not None:
            params['zoneName'] = zone_name
        if marker is not None:
            params['marker'] = marker
        if max_keys is not None:
            params['maxKeys'] = max_keys
        if cluster_id is not None:
            params['clusterId'] = cluster_id
        if volume_ids is not None:
            params['volumeIds'] = volume_ids
        return self._send_request(http_methods.GET, path, params=params, config=config)

    @required(volume_id=(bytes, str))  # ***Unicode***
    def get_volume(self, volume_id, config=None):
        """
        Get the detail information of specified volume.

        :param volume_id:
            The id of the volume.
        :type volume_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        volume_id = compat.convert_to_bytes(volume_id)
        path = b'/volume/%s' % volume_id
        return self._send_request(http_methods.GET, path, config=config)

    @required(volume_id=(bytes, str),  # ***Unicode***
              instance_id=(bytes, str))  # ***Unicode***
    def attach_volume(self, volume_id, instance_id, config=None):
        """
        Attaching the specified volume to a specified instance.
        You can attach the specified volume to a specified instance only
        when the volume is Available and the instance is Running or Stopped,
        otherwise, it's will get 409 errorCode.

        :param volume_id:
            The id of the volume which will be attached to specified instance.
        :type volume_id: string

        :param instance_id:
            The id of the instance which will be attached with a volume.
        :type instance_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        volume_id = compat.convert_to_bytes(volume_id)
        path = b'/volume/%s' % volume_id
        body = {
            'instanceId': instance_id
        }
        params = {
            'attach': None
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(volume_id=(bytes, str),  # ***Unicode***
              instance_id=(bytes, str))  # ***Unicode***
    def detach_volume(self, volume_id, instance_id, config=None):
        """
        Detaching the specified volume from a specified instance.
        You can detach the specified volume from a specified instance only
        when the instance is Running or Stopped ,
        otherwise, it's will get 409 errorCode.

        :param volume_id:
            The id of the volume which will be attached to specified instance.
        :type volume_id: string

        :param instance_id:
            The id of the instance which will be attached with a volume.
        :type instance_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        volume_id = compat.convert_to_bytes(volume_id)
        path = b'/volume/%s' % volume_id
        body = {
            'instanceId': instance_id
        }
        params = {
            'detach': None
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    def describe_regions(self, region, config=None):
        """
        List all region's endpoint information with the specific parameters.
        Use global endpoint bcc.baidubce.com to get BCC,CDS,ReservedInstance's endpoint.

        :param region:
            The id of region.
        :type region: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        path = b'/region/describeRegions'
        body = {
            'region': region
        }
        params = {}
        return self._send_request(http_methods.POST, path, json.dumps(body),
                                  params=params, config=config)

    @required(volume_id=(bytes, str))  # ***Unicode***
    def release_volume(self, volume_id, config=None):
        """
        Releasing the specified volume owned by the user.
        You can release the specified volume only
        when the instance is among state of  Available/Expired/Error,
        otherwise, it's will get 409 errorCode.

        :param volume_id:
            The id of the volume which will be released.
        :type volume_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        volume_id = compat.convert_to_bytes(volume_id)
        path = b'/volume/%s' % volume_id
        return self._send_request(http_methods.DELETE, path, config=config)

    @required(volume_id=(bytes, str),  # ***Unicode***
              new_cds_size=int)
    def resize_volume(self, volume_id, new_cds_size, new_volume_type,
                      client_token=None, config=None):
        """
        Resizing the specified volume with newly size.
        You can resize the specified volume only when the volume is Available,
        otherwise, it's will get 409 errorCode.
        The prepaid volume can not be downgrade.
        This is an asynchronous interface,
        you can get the latest status by BccClient.get_volume.

        :param volume_id:
            The id of volume which you want to resize.
        :type volume_id: string

        :param new_cds_size:
            The new volume size you want to resize in GB.
        :type new_cds_size: int

        :param new_volume_type:
            detail information see: https://cloud.baidu.com/doc/BCC/s/6jwvyo0q2#storagetype
        :type new_volume_type: string

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if client token is provided.
            If the clientToken is not specified by the user,
            a random String generated by default algorithm will be used.
            See more detail at
            https://bce.baidu.com/doc/BCC/API.html#.E5.B9.82.E7.AD.89.E6.80.A7
        :type client_token: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        volume_id = compat.convert_to_bytes(volume_id)
        path = b'/volume/%s' % volume_id
        body = {
            'newCdsSizeInGB': new_cds_size
        }
        if new_volume_type is not None:
            body['newVolumeType'] = new_volume_type
        params = None
        if client_token is None:
            params = {
                'resize': None,
                'clientToken': generate_client_token()
            }
        else:
            params = {
                'resize': None,
                'clientToken': client_token
            }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(volume_id=(bytes, str),  # ***Unicode***
              snapshot_id=(bytes, str))  # ***Unicode***
    def rollback_volume(self, volume_id, snapshot_id, config=None):
        """
        Rollback the volume with the specified volume snapshot.
        You can rollback the specified volume only when the volume is Available,
        otherwise, it's will get 409 errorCode.
        The snapshot used to rollback must be created by the volume,
        otherwise,it's will get 404 errorCode.
        If rolling back the system volume,the instance must be Running or Stopped,
        otherwise, it's will get 409 errorCode.After rolling back the
        volume,all the system disk data will erase.

        :param volume_id:
            The id of volume which will be rollback.
        :type volume_id: string

        :param snapshot_id:
            The id of snapshot which will be used to rollback the volume.
        :type snapshot_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        volume_id = compat.convert_to_bytes(volume_id)
        path = b'/volume/%s' % volume_id
        body = {
            'snapshotId': snapshot_id
        }
        params = {
            'rollback': None,
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(volume_id=(bytes, str))  # ***Unicode***
    def purchase_reserved_volume(self,
                                 volume_id,
                                 billing=None,
                                 client_token=None,
                                 config=None,
                                 instance_id=None):
        """
        PurchaseReserved the instance with fixed duration.
        You can not purchaseReserved the instance which is resizing.
        This is an asynchronous interface,
        you can get the latest status by BccClient.get_volume.

        :param volume_id:
            The id of volume which will be renew.
        :type volume_id: string

        :param billing:
            Billing information.
        :type billing: bcc_model.Billing

        :param instance_id:
            The id of instance to align renew duarion.

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if client token is provided.
            If the clientToken is not specified by the user,
            a random String generated by default algorithm will be used.
            See more detail at
            https://bce.baidu.com/doc/BCC/API.html#.E5.B9.82.E7.AD.89.E6.80.A7
        :type client_token: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        volume_id = compat.convert_to_bytes(volume_id)
        path = b'/volume/%s' % volume_id
        if billing is None:
            billing = default_billing_to_purchase_reserved
        body = {
            'billing': billing.__dict__,
            'instanceId': instance_id
        }
        params = None
        if client_token is None:
            params = {
                'purchaseReserved': None,
                'clientToken': generate_client_token()
            }
        else:
            params = {
                'purchaseReserved': None,
                'clientToken': client_token
            }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(volume_id=(bytes, str),
              cds_name=(bytes, str),
              desc=(bytes, str))
    def modify_volume_Attribute(self,
                                volume_id,
                                cds_name,
                                desc,
                                config=None):
        """
        :param volume_id:
        :type volume_id: string

        :param cds_name:
        :type cds_name:string

        :param desc:
        :type desc: string

        :return:
        """
        volume_id = compat.convert_to_bytes(volume_id)
        path = b'/volume/%s' % volume_id

        body = {
            'cdsName': cds_name
        }
        if desc is not None:
            body['desc'] = desc
        params = {
            'modify': None
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(volume_id=(bytes, str))
    def modify_volume_charge_type(self,
                                  volume_id,
                                  billing=None,
                                  config=None):
        """
        :param volume_id: volume id
        :type volume_id: string
        :param billing: payment information
        :type billing: bcc_model.Billing
        :param config:

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        volume_id = compat.convert_to_bytes(volume_id)
        path = b'/volume/%s' % volume_id

        if billing is None:
            billing = default_billing_to_purchase_reserved
        body = {
            'billing': billing.__dict__
        }

        params = {
            'modifyChargeType': None
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(image_name=(bytes, str),  # ***Unicode***
              instance_id=(bytes, str))  # ***Unicode***
    def create_image_from_instance_id(self,
                                      image_name,
                                      instance_id,
                                      encrypt_key=None,
                                      relate_cds=False,
                                      client_token=None,
                                      config=None,
                                      detection=None):
        """
        Creating a customized image which can be used for creating instance.
        You can create an image from an instance with this method.
        While creating an image from an instance, the instance must be Running or Stopped,
        otherwise, it's will get 409 errorCode.
        This is an asynchronous interface,
        you can get the latest status by BccClient.get_image.

        :param image_name:
            The name for the image that will be created.
            The name length from 1 to 65,only contains letters,digital and underline.
        :type image_name: string

        :param instance_id:
            The optional parameter specify the id of the instance which will be used to create the new image.
            When instanceId and snapshotId are specified ,only instanceId will be used.
        :type instance_id: string

        :param encrypt_key:
        :type encrypt_key: string

        :param relate_cds:
        :type relate_cds: boolean

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if client token is provided.
            If the clientToken is not specified by the user,
            a random String generated by default algorithm will be used.
            See more detail at
            https://bce.baidu.com/doc/BCC/API.html#.E5.B9.82.E7.AD.89.E6.80.A7
        :type client_token: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/image'
        params = None
        if client_token is None:
            params = {
                'clientToken': generate_client_token()
            }
        else:
            params = {
                'clientToken': client_token
            }
        body = {
            'imageName': image_name,
            'instanceId': instance_id
        }
        if encrypt_key is not None:
            body['encryptKey'] = encrypt_key
        if relate_cds is not None:
            body['relateCds'] = relate_cds
        if detection:
            body['detection'] = detection
        return self._send_request(http_methods.POST, path, json.dumps(body),
                                  params=params, config=config)

    @required(image_name=(bytes, str),  # ***Unicode***
              snapshot_id=(bytes, str))  # ***Unicode***
    def create_image_from_snapshot_id(self,
                                      image_name,
                                      snapshot_id,
                                      encrypt_key=None,
                                      client_token=None,
                                      config=None,
                                      detection=None):
        """
        Creating a customized image which can be used for creating instance.
        You can create an image from an snapshot with tihs method.
        You can create the image only from system snapshot.
        While creating an image from a system snapshot,the snapshot must be Available,
        otherwise, it's will get 409 errorCode.
        This is an asynchronous interface,
        you can get the latest status by BccClient.get_image.

        :param image_name:
            The name for the image that will be created.
            The name length from 1 to 65,only contains letters,digital and underline.
        :type image_name: string

        :param snapshot_id:
            The optional parameter specify the id of the snapshot which will be used to create the new image.
            When instanceId and snapshotId are specified ,only instanceId will be used.
        :type snapshot_id: string

        :param encrypt_key:
        :type encrypt_key: string

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if client token is provided.
            If the clientToken is not specified by the user,
            a random String generated by default algorithm will be used.
            See more detail at
            https://bce.baidu.com/doc/BCC/API.html#.E5.B9.82.E7.AD.89.E6.80.A7
        :type client_token: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/image'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            'imageName': image_name,
            'snapshotId': snapshot_id
        }
        if encrypt_key is not None:
            body['encryptKey'] = encrypt_key
        if detection:
            body['detection'] = detection
        return self._send_request(http_methods.POST, path, json.dumps(body),
                                  params=params, config=config)

    def list_images(self, image_type='All', marker=None, max_keys=None, image_name=None,
                    config=None):
        """
        Listing images owned by the authenticated user.

        :param image_type:
            The optional parameter to filter image to list.
            See more detail at
            https://bce.baidu.com/doc/BCC/API.html#ImageType"
        :type image_type: menu{'All', System', 'Custom', 'Integration'}

        :param marker:
            The optional parameter marker specified in the original request to specify
            where in the results to begin listing.
            Together with the marker, specifies the list result which listing should begin.
            If the marker is not specified, the list result will listing from the first one.
        :type marker: string

        :param max_keys:
            The optional parameter to specifies the max number of list result to return.
            The default value is 1000.
        :type max_keys: int

        :param image_name:
            The optional parameter to query specified custom image by image name.
        :type image_name: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/image'
        params = {
            'imageType': image_type
        }
        if marker is not None:
            params['marker'] = marker
        if max_keys is not None:
            params['maxKeys'] = max_keys
        if image_name is not None:
            params['imageName'] = image_name
        return self._send_request(http_methods.GET, path, params=params, config=config)

    @required(image_id=(bytes, str))  # ***Unicode***
    def get_image(self, image_id, config=None):
        """
        Get the detail information of specified image.

        :param image_id:
            The id of image.
        :type image_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        image_id = compat.convert_to_bytes(image_id)
        path = b'/image/%s' % image_id
        return self._send_request(http_methods.GET, path, config=config)

    @required(image_id=(bytes, str))  # ***Unicode***
    def delete_image(self, image_id, config=None):
        """
        Deleting the specified image.
        Only the customized image can be deleted,
        otherwise, it's will get 403 errorCode.

        :param image_id:
            The id of image.
        :type image_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        image_id = compat.convert_to_bytes(image_id)
        path = b'/image/%s' % image_id
        return self._send_request(http_methods.DELETE, path, config=config)

    @required(image_id=(bytes, str),
              name=(bytes, str),
              destRegions=list)
    def remote_copy_image(self,
                          image_id,
                          name,
                          destRegions,
                          config=None):
        """
        :param image_id:
        :param name:
        :param destRegions:
        :param config:
        :return:
        """
        image_id = compat.convert_to_bytes(image_id)
        path = b'/image/%s' % image_id

        body = {
            'name': name,
            'destRegion': destRegions
        }
        params = {
            'remoteCopy': None
        }
        return self._send_request(http_methods.POST, path, json.dumps(body),
                                  params=params, config=config)

    @required(image_id=(bytes, str))
    def cancle_remote_copy_image(self,
                                 image_id,
                                 config=None):
        """
        :param image_id:
        :param config:
        :return:
        """
        image_id = compat.convert_to_bytes(image_id)
        path = b'/image/%s' % image_id

        params = {
            'cancelRemoteCopy': None
        }
        return self._send_request(http_methods.POST, path, params=params, config=config)

    @required(image_id=(bytes, str))
    def share_image(self,
                    image_id,
                    account=None,
                    account_id=None,
                    ucaccount=None,
                    config=None):
        """
        :param image_id: image id
        :type image_id: string
        :param account: share image to target account
        :type account: string
        :param account_id: share image to target account_id
        :type account_id: string
        :param ucaccount: share image to target ucaccount
        :type ucaccount: string
        :param config:

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        image_id = compat.convert_to_bytes(image_id)
        path = b'/image/%s' % image_id

        body = {}
        if account is not None:
            body['account'] = account
        if account_id is not None:
            body['accountId'] = account_id
        if ucaccount is not None:
            body['ucAccount'] = ucaccount

        params = {
            'share': None
        }
        return self._send_request(http_methods.POST, path, json.dumps(body),
                                  params=params, config=config)

    @required(image_id=(bytes, str))
    def unshare_image(self,
                      image_id,
                      account=None,
                      account_id=None,
                      ucaccount=None,
                      config=None):
        """
        :param image_id: image id
        :type image_id: string
        :param account: unshare image with target account
        :type account: string
        :param account_id: unshare image with target account_id
        :type account_id: string
        :param ucaccount: unshare image with target ucaccount
        :type ucaccount: string
        :param config:

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        image_id = compat.convert_to_bytes(image_id)
        path = b'/image/%s' % image_id

        body = {}
        if account is not None:
            body['account'] = account
        if account_id is not None:
            body['accountId'] = account_id
        if ucaccount is not None:
            body['ucAccount'] = ucaccount

        params = {
            'unshare': None
        }
        return self._send_request(http_methods.POST, path, json.dumps(body),
                                  params=params, config=config)

    @required(image_id=(bytes, str))
    def list_shared_user(self,
                         image_id,
                         config=None):
        """
        :param image_id:
        :param config:
        :return:
        """
        image_id = compat.convert_to_bytes(image_id)
        path = b'/image/%s/sharedUsers' % image_id
        return self._send_request(http_methods.GET, path, config=config)

    @required(instance_ids=list)
    def list_os(self,
                instance_ids=None,
                config=None):
        """
        :param instance_ids:
        :param config:
        :return:
        """
        path = b'/image/os'
        instance_id_list = instance_ids
        body = {
            'instanceIds': instance_id_list
        }
        return self._send_request(http_methods.POST, path, json.dumps(body), config=config)

    @required(volume_id=(bytes, str),  # ***Unicode***
              snapshot_name=(bytes, str))  # ***Unicode***
    def create_snapshot(self,
                        volume_id,
                        snapshot_name,
                        desc=None,
                        tags=None,
                        client_token=None,
                        config=None):
        """
        Creating snapshot from specified volume.
        You can create snapshot from system volume and CDS volume.
        While creating snapshot from system volume,the instance must be Running or Stopped,
        otherwise, it's will get 409 errorCode.
        While creating snapshot from CDS volume, the volume must be InUs or Available,
        otherwise, it's will get 409 errorCode.
        This is an asynchronous interface,
        you can get the latest status by BccClient.get_snapshot.

        :param volume_id:
            The id which specify where the snapshot will be created from.
            If you want to create an snapshot from a customized volume, a id of the volume will be set.
            If you want to create an snapshot from a system volume, a id of the instance will be set.
        :type volume_id: string

        :param snapshot_name:
            The name for the snapshot that will be created.
            The name length from 1 to 65,only contains letters,digital and underline.
        :type snapshot_name: string

        :param desc:
            The optional parameter to describe the information of the new snapshot.
        :type desc: string

        :param tags:
            The optional list of tag to be bonded.
        :type tags: list<bcc_model.TagModel>

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if client token is provided.
            If the clientToken is not specified by the user,
            a random String generated by default algorithm will be used.
            See more detail at
            https://bce.baidu.com/doc/BCC/API.html#.E5.B9.82.E7.AD.89.E6.80.A7
        :type client_token: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/snapshot'
        params = None
        if client_token is None:
            params = {
                'clientToken': generate_client_token()
            }
        else:
            params = {
                'clientToken': client_token
            }
        body = {
            'volumeId': volume_id,
            'snapshotName': snapshot_name
        }
        if desc is not None:
            body['desc'] = desc
        if tags is not None:
            tag_list = [tag.__dict__ for tag in tags]
            body['tags'] = tag_list
        return self._send_request(http_methods.POST, path, json.dumps(body),
                                  params=params, config=config)

    def list_snapshots(self, marker=None, max_keys=None, volume_id=None, config=None):
        """
        List snapshots

        :param marker:
            The optional parameter marker specified in the original request to specify
            where in the results to begin listing.
            Together with the marker, specifies the list result which listing should begin.
            If the marker is not specified, the list result will listing from the first one.
        :type params: string

        :param max_keys:
            The optional parameter to specifies the max number of list result to return.
            The default value is 1000.
        :type params: int

        :param volume_id:
            The id of the volume.
        :type volume_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/snapshot'
        params = None
        if marker is not None or max_keys is not None or volume_id is not None:
            params = {}
        if marker is not None:
            params['marker'] = marker
        if max_keys is not None:
            params['maxKeys'] = max_keys
        if volume_id is not None:
            params['volumeId'] = volume_id

        return self._send_request(http_methods.GET, path, params=params, config=config)

    @required(snapshot_id=(bytes, str))  # ***Unicode***
    def get_snapshot(self, snapshot_id, config=None):
        """
        Get the detail information of specified snapshot.

        :param snapshot_id:
            The id of snapshot.
        :type snapshot_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        snapshot_id = compat.convert_to_bytes(snapshot_id)
        path = b'/snapshot/%s' % snapshot_id
        return self._send_request(http_methods.GET, path, config=config)

    @required(snapshot_id=(bytes, str))  # ***Unicode***
    def delete_snapshot(self, snapshot_id, config=None):
        """
        Deleting the specified snapshot.
        Only when the snapshot is CreatedFailed or Available,the specified snapshot can be deleted.
        otherwise, it's will get 403 errorCode.

        :param snapshot_id:
            The id of snapshot.
        :type snapshot_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        snapshot_id = compat.convert_to_bytes(snapshot_id)
        path = b'/snapshot/%s' % snapshot_id
        return self._send_request(http_methods.DELETE, path, config=config)

    @required(name=(bytes, str),  # ***Unicode***
              rules=list)
    def create_security_group(self,
                              name,
                              rules,
                              vpc_id=None,
                              desc=None,
                              client_token=None,
                              tags=None,
                              config=None):
        """
        Creating a newly SecurityGroup with specified rules.

        :param name:
            The name of SecurityGroup that will be created.
        :type name: string

        :param rules:
            The list of rules which define how the SecurityGroup works.
        :type rules: list<bcc_model.SecurityGroupRuleModel>

        :param vpc_id:
            The optional parameter to specify the id of VPC to SecurityGroup
        :type vpc_id: string

        :param desc:
            The optional parameter to describe the SecurityGroup that will be created.
        :type desc: string

        :param tags:
            The optional list of tag to be bonded.
        :type tags: list<bcc_model.TagModel>

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if client token is provided.
            If the clientToken is not specified by the user,
            a random String generated by default algorithm will be used.
            See more detail at
            https://bce.baidu.com/doc/BCC/API.html#.E5.B9.82.E7.AD.89.E6.80.A7
        :type client_token: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/securityGroup'
        params = None
        if client_token is None:
            params = {
                'clientToken': generate_client_token()
            }
        else:
            params = {
                'clientToken': client_token
            }
        rule_list = [rule.__dict__ for rule in rules]
        body = {
            'name': name,
            'rules': rule_list
        }
        if vpc_id is not None:
            body['vpcId'] = vpc_id
        if desc is not None:
            body['desc'] = desc
        if tags is not None:
            tag_list = [tag.__dict__ for tag in tags]
            body['tags'] = tag_list
        return self._send_request(http_methods.POST, path, json.dumps(body),
                                  params=params, config=config)

    def list_security_groups(self, instance_id=None, vpc_id=None, marker=None, max_keys=None,
                             config=None):
        """
        Listing SecurityGroup owned by the authenticated user.

        :param instance_id:
            The id of instance. The optional parameter to list the SecurityGroup.
            If it's specified,only the SecurityGroup related to the specified instance will be listed
        :type instance_id: string

        :param vpc_id:
            filter by vpcId, optional parameter
        :type vpc_id: string

        :param marker:
            The optional parameter marker specified in the original request to specify
            where in the results to begin listing.
            Together with the marker, specifies the list result which listing should begin.
            If the marker is not specified, the list result will listing from the first one.
        :type marker: string

        :param max_keys:
            The optional parameter to specifies the max number of list result to return.
            The default value is 1000.
        :type max_keys: int

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/securityGroup'
        params = {}
        if instance_id is not None:
            params['instanceId'] = instance_id
        if vpc_id is not None:
            params['vpcId'] = vpc_id
        if marker is not None:
            params['marker'] = marker
        if max_keys is not None:
            params['maxKeys'] = max_keys

        return self._send_request(http_methods.GET, path,
                                  params=params, config=config)

    @required(security_group_id=(bytes, str))  # ***Unicode***
    def delete_security_group(self, security_group_id, config=None):
        """
        Deleting the specified SecurityGroup.

        :param security_group_id:
            The id of SecurityGroup that will be deleted.
        :type security_group_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        security_group_id = compat.convert_to_bytes(security_group_id)
        path = b'/securityGroup/%s' % security_group_id
        return self._send_request(http_methods.DELETE, path, config=config)

    @required(security_group_id=(bytes, str),  # ***Unicode***
              rule=bcc_model.SecurityGroupRuleModel)
    def authorize_security_group_rule(self, security_group_id, rule, client_token=None,
                                      config=None):
        """
        authorize a security group rule to the specified security group

        :param security_group_id:
            The id of SecurityGroup that will be authorized.
        :type security_group_id: string

        :param rule:
            security group rule detail.
            Through protocol/portRange/direction/sourceIp/sourceGroupId, we can confirmed only one rule.
        :type rule: bcc_model.SecurityGroupRuleModel

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if client token is provided.
            If the clientToken is not specified by the user,
            a random String generated by default algorithm will be used.
            See more detail at
            https://bce.baidu.com/doc/BCC/API.html#.E5.B9.82.E7.AD.89.E6.80.A7
        :type client_token: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        security_group_id = compat.convert_to_bytes(security_group_id)
        path = b'/securityGroup/%s' % security_group_id
        params = {'authorizeRule': ''}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            'rule': rule.__dict__
        }

        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(security_group_id=(bytes, str),  # ***Unicode***
              rule=bcc_model.SecurityGroupRuleModel)
    def revoke_security_group_rule(self, security_group_id, rule, client_token=None, config=None):
        """
        revoke a security group rule from the specified security group
        :param security_group_id:
            The id of SecurityGroup that will be revoked.
        :type security_group_id: string
        :param rule:
            security group rule detail.
            Through protocol/portRange/direction/sourceIp/sourceGroupId, we can confirmed only one rule.
        :type rule: bcc_model.SecurityGroupRuleModel
        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if client token is provided.
            If the clientToken is not specified by the user,
            a random String generated by default algorithm will be used.
            See more detail at
            https://bce.baidu.com/doc/BCC/API.html#.E5.B9.82.E7.AD.89.E6.80.A7
        :type client_token: string
        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        security_group_id = compat.convert_to_bytes(security_group_id)
        path = b'/securityGroup/%s' % security_group_id
        params = {'revokeRule': ''}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            'rule': rule.__dict__
        }

        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    def update_security_group_rule(self, security_group_rule_id,
                                   remark=None,
                                   direction=None,
                                   protocol=None,
                                   portrange=None,
                                   source_ip=None,
                                   sourcegroup_id=None,
                                   dest_ip=None,
                                   destgroup_id=None,
                                   config=None):
        """
            uodate a security group rule from the specified security group
            :param security_group_rule_id:
                security group rule id.
            :param: remark:
                The remark for the rule.
            :param: portrange:
                The port range to specify the port which the rule will work on.
                Available range is rang [0, 65535], the fault value is "" for all port.
            :param: protocol:
                The parameter specify which protocol will the rule work on, the fault value is "" for all protocol.
                Available protocol are tcp, udp and icmp.
            :param: source_ip:
                The source ip range with CIDR formats. The default value 0.0.0.0/0 (allow all ip address),
                other supported formats such as {ip_addr}/12 or {ip_addr}. Only supports IPV4.
                Only works for  direction = "ingress".
            :param: sourcegroup_id:
                The source security group id. Cannot coexist with sourceIP.
            :param: dest_ip:
                The destination ip range with CIDR formats. The default value 0.0.0.0/0 (allow all ip address),
                other supported formats such as {ip_addr}/12 or {ip_addr}. Only supports IPV4.
                Only works for  direction = "egress".
            :param: destgroup_id:
                The destination security group id. Cannot coexist with destIP.
            :param: priority:
                The parameter specify the priority of the rule(range 1-1000).
            :param config:
                :type config: baidubce.BceClientConfiguration
            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        path = b'/securityGroup/rule/update'
        body = {
            'securityGroupRuleId': security_group_rule_id,
            'remark': remark,
            'direction': direction,
            'protocol': protocol,
            'portRange': portrange,
            'sourceIp': source_ip,
            'sourceGroupId': sourcegroup_id,
            'destIp': dest_ip,
            'destGroupId': destgroup_id
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=None, config=config)

    @required(security_group_rule_id=(bytes, str))  # ***Unicode***
    def delete_security_group_rule(self, security_group_rule_id, config=None):
        """
            delete a security group rule from the specified security group
            :param security_group_rule_id:
                The id of SecurityGroupRule that will be deleted.
            :type security_group_id: string
            :param config:
            :type config: baidubce.BceClientConfiguration
            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        security_group_rule_id = compat.convert_to_bytes(security_group_rule_id)
        path = b'/securityGroup/rule/%s' % security_group_rule_id
        return self._send_request(http_methods.DELETE, path, params=None, config=config)

    @required(security_group_id=(bytes, str))  # ***Unicode***
    def get_security_group_detail(self, security_group_id, config=None):
        """
            get a security group detail from the specified security group
            :param security_group_id:
                The id of security_group that will be deleted.
            :type security_group_id: string
            :param config:
            :type config: baidubce.BceClientConfiguration
            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        security_group_id = compat.convert_to_bytes(security_group_id)
        path = b'/securityGroup/%s' % security_group_id
        return self._send_request(http_methods.GET, path, params=None, config=config)

    def list_zones(self, config=None):
        """
        Get zone detail list within current region
        :param config:
        :return:
        """
        path = b'/zone'
        return self._send_request(http_methods.GET, path, config=config)

    @required(asp_name=(bytes, str),
              time_points=list,
              repeat_week_days=list,
              retention_days=(bytes, str))
    def create_asp(self,
                   asp_name=None,
                   time_points=None,
                   repeat_week_days=None,
                   retention_days=None,
                   client_token=None,
                   config=None):
        """
        :param asp_name:
        :param time_points:
        :param repeat_week_days:
        :param retention_days:
        :param client_token:
        :param config:
        :return:
        """
        path = b'/asp'
        params = None
        if client_token is None:
            params = {
                'clientToken': generate_client_token()
            }
        else:
            params = {
                'clientToken': client_token
            }
        body = {
            'name': asp_name,
            'timePoints': time_points,
            'repeatWeekdays': repeat_week_days,
            'retentionDays': retention_days
        }
        return self._send_request(http_methods.POST, path, json.dumps(body),
                                  params=params, config=config)

    @required(asp_id=(bytes, str),
              volume_ids=list)
    def attach_asp(self,
                   asp_id=None,
                   volume_ids=None,
                   config=None):
        """
        :param asp_id:
        :param volume_ids:
        :param config:
        :return:
        """
        asp_id = compat.convert_to_bytes(asp_id)
        path = b'/asp/%s' % asp_id

        body = {
            'volumeIds': volume_ids
        }
        params = {
            'attach': None
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(asp_id=(bytes, str),
              volume_ids=list)
    def detach_asp(self,
                   asp_id=None,
                   volume_ids=None,
                   config=None):
        """
        :param asp_id:
        :param volume_ids:
        :param config:
        :return:
        """
        asp_id = compat.convert_to_bytes(asp_id)
        path = b'/asp/%s' % asp_id

        body = {
            'volumeIds': volume_ids
        }
        params = {
            'detach': None
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(asp_id=(bytes, str))
    def delete_asp(self,
                   asp_id=None,
                   config=None):
        """
        :param asp_id:
        :param config:
        :return:
        """
        asp_id = compat.convert_to_bytes(asp_id)
        path = b'/asp/%s' % asp_id
        return self._send_request(http_methods.DELETE, path, config=config)

    def list_asps(self, marker=None, max_keys=None, asp_name=None, volume_name=None, config=None):
        """
        :param marker:
        :param max_keys:
        :param asp_name:
        :param volume_name:
        :param config:
        :return:
        """
        path = b'/asp'
        params = None
        if marker is not None or max_keys is not None or asp_name is not None or volume_name is not None:
            params = {}
        if marker is not None:
            params['marker'] = marker
        if max_keys is not None:
            params['maxKeys'] = max_keys
        if asp_name is not None:
            params['aspName'] = asp_name
        if volume_name is not None:
            params['volumeName'] = volume_name
        return self._send_request(http_methods.GET, path, params=params, config=config)

    @required(asp_id=(bytes, str))
    def get_asp(self, asp_id=None, config=None):
        """
        :param asp_id:
        :param config:
        :return:
        """
        asp_id = compat.convert_to_bytes(asp_id)
        path = b'/asp/%s' % asp_id
        return self._send_request(http_methods.GET, path, config=config)

    @required(keypair_name=(bytes, str))
    def create_keypair(self,
                       keypair_name=None,
                       keypair_desc=None,
                       config=None):
        """
        :param keypair_name:
        :param keypair_desc:
        :param config:
        :return:
        """
        path = b'/keypair'
        body = {
            'name': keypair_name,
            'description': keypair_desc
        }
        params = {
            'create': None
        }
        return self._send_request(http_methods.POST, path, json.dumps(body),
                                  params=params, config=config)

    @required(keypair_name=(bytes, str),
              public_key=(bytes, str))
    def import_keypair(self,
                       keypair_name=None,
                       keypair_desc=None,
                       public_key=None,
                       config=None):
        """
        :param keypair_name:
        :param keypair_desc:
        :param public_key:
        :param config:
        :return:
        """
        path = b'/keypair'
        body = {
            'name': keypair_name,
            'publicKey': public_key
        }
        if keypair_desc is not None:
            body['description'] = keypair_desc

        params = {
            'import': None
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    def list_keypairs(self, marker=None, max_keys=None, name=None, config=None):
        """
        :param marker:
        :param max_keys:
        :param config:
        :return:
        """
        path = b'/keypair'
        params = None
        if marker is not None or max_keys is not None or name is not None:
            params = {}
        if marker is not None:
            params['marker'] = marker
        if max_keys is not None:
            params['maxKeys'] = max_keys
        if name is not None:
            params['name'] = name
        return self._send_request(http_methods.GET, path, params=params, config=config)

    @required(keypair_id=(bytes, str))
    def get_keypair(self, keypair_id=None, config=None):
        """
        :param keypair_id:
        :param config:
        :return:
        """
        keypair_id = compat.convert_to_bytes(keypair_id)
        path = b'/keypair/%s' % keypair_id
        return self._send_request(http_methods.GET, path, config=config)

    @required(keypair_id=(bytes, str),
              instance_ids=list)
    def attach_keypair(self,
                       keypair_id=None,
                       instance_ids=None,
                       config=None):
        """
        :param keypair_id:
        :param instance_ids:
        :param config:
        :return:
        """

        keypair_id = compat.convert_to_bytes(keypair_id)
        path = b'/keypair/%s' % keypair_id
        body = {
            'instanceIds': instance_ids
        }
        params = {
            'attach': None
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(keypair_id=(bytes, str),
              instance_id=list)
    def detach_keypair(self,
                       keypair_id=None,
                       instance_ids=None,
                       config=None):
        """
        :param keypair_id:
        :param instance_ids:
        :param config:
        :return:
        """

        keypair_id = compat.convert_to_bytes(keypair_id)
        path = b'/keypair/%s' % keypair_id
        body = {
            'instanceIds': instance_ids
        }
        params = {
            'detach': None
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(keypair_id=(bytes, str))
    def delete_keypair(self,
                       keypair_id=None,
                       config=None):
        """
        :param keypair_id:
        :param config:
        :return:
        """

        keypair_id = compat.convert_to_bytes(keypair_id)
        path = b'/keypair/%s' % keypair_id

        return self._send_request(http_methods.DELETE, path, config=config)

    @required(keypair_id=(bytes, str),
              keypair_name=(bytes, str))
    def rename_keypair(self,
                       keypair_id=None,
                       keypair_name=None,
                       config=None):
        """
        :param keypair_id:
        :param keypair_name:
        :param config:
        :return:
        """

        keypair_id = compat.convert_to_bytes(keypair_id)
        path = b'/keypair/%s' % keypair_id
        body = {
            'name': keypair_name
        }
        params = {
            'rename': None
        }

        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(keypair_id=(bytes, str),
              keypair_desc=(bytes, str))
    def update_keypair_desc(self,
                            keypair_id=None,
                            keypair_desc=None,
                            config=None):
        """
        :param keypair_id:
        :param keypair_desc:
        :param config:
        :return:
        """

        keypair_id = compat.convert_to_bytes(keypair_id)
        path = b'/keypair/%s' % keypair_id
        body = {
            'description': keypair_desc
        }
        params = {
            'updateDesc': None
        }

        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(cluster_size_in_gb=int)
    def create_volume_cluster(self, cluster_size_in_gb, purchase_count=1, storage_type='hp1', cluster_name=None,
                              paymentTiming='Prepaid', reservation_length=6, reservation_time_unit='month',
                              renew_time_unit=None, renew_time=None, zone_name=None, uuid_flag=None,
                              client_token=None, config=None):
        """
        create_volume_cluster.
        """
        path = b'/volume/cluster'
        params = {}
        if uuid_flag is not None:
            params['uuidFlag'] = uuid_flag
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token

        billing = bcc_model.Billing(paymentTiming=paymentTiming, reservationLength=reservation_length,
                                    reservationTimeUnit=reservation_time_unit)
        body = {
            'clusterSizeInGB': cluster_size_in_gb,
            'storageType': storage_type,
            'purchaseCount': purchase_count,
            'billing': billing.__dict__
        }
        if zone_name is not None:
            body['zoneName'] = zone_name
        if cluster_name is not None:
            body['clusterName'] = cluster_name
        if renew_time_unit is not None:
            body['renewTimeUnit'] = renew_time_unit
        if renew_time is not None:
            body['renewTime'] = renew_time

        return self._send_request(http_methods.POST, path, json.dumps(body), params=params, config=config)

    def list_volume_cluster(self, cluster_name=None, zone_name=None, marker=None, max_keys=None,
                            config=None):
        """
        list_volume_cluster.
        """
        path = b'/volume/cluster'
        params = {}
        if cluster_name is not None:
            params['clusterName'] = cluster_name
        if zone_name is not None:
            params['zoneName'] = zone_name
        if marker is not None:
            params['marker'] = marker
        if max_keys is not None:
            params['maxKeys'] = max_keys

        return self._send_request(http_methods.GET, path, params=params, config=config)

    @required(cluster_id=(bytes, str))  # ***Unicode***
    def get_volume_cluster(self, cluster_id, config=None):
        """
        Get cluster detail
        """
        cluster_id = compat.convert_to_bytes(cluster_id)
        path = b'/volume/cluster/%s' % cluster_id
        return self._send_request(http_methods.GET, path, config=config)

    @required(cluster_id=(bytes, str),  # ***Unicode***
              new_cluster_size=int)
    def resize_volume_cluster(self, cluster_id, new_cluster_size, client_token=None, config=None):
        """
        resize_volume_cluster
        """
        cluster_id = compat.convert_to_bytes(cluster_id)
        path = b'/volume/cluster/%s' % cluster_id
        body = {
            'newClusterSizeInGB': new_cluster_size
        }
        params = None
        if client_token is None:
            params = {
                'resize': None,
                'clientToken': generate_client_token()
            }
        else:
            params = {
                'resize': None,
                'clientToken': client_token
            }
        return self._send_request(http_methods.PUT, path, json.dumps(body), params=params, config=config)

    @required(cluster_id=(bytes, str))  # ***Unicode***
    def renew_volume_cluster(self, cluster_id, reservation_length=6, reservation_time_unit='month',
                             client_token=None, config=None):
        """
        renew_volume_cluster
        """
        cluster_id = compat.convert_to_bytes(cluster_id)
        path = b'/volume/cluster/%s' % cluster_id

        billing = bcc_model.Billing(reservationLength=reservation_length,
                                    reservationTimeUnit=reservation_time_unit)
        body = {
            'billing': billing.__dict__
        }
        params = None
        if client_token is None:
            params = {
                'purchaseReserved': None,
                'clientToken': generate_client_token()
            }
        else:
            params = {
                'purchaseReserved': None,
                'clientToken': client_token
            }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(cluster_id=(bytes, str))  # ***Unicode***
    def autoRenew_volume_cluster(self, cluster_id, renew_time=6, renew_time_unit='month',
                                 client_token=None, config=None):
        """
        autoRenew_volume_cluster
        """
        cluster_id = compat.convert_to_bytes(cluster_id)
        path = b'/volume/cluster/autoRenew'
        body = {
            'clusterId': cluster_id,
            'renewTimeUnit': renew_time_unit,
            'renewTime': renew_time,
        }
        params = None
        if client_token is None:
            params = {
                'clientToken': generate_client_token()
            }
        else:
            params = {
                'clientToken': client_token
            }
        return self._send_request(http_methods.POST, path, json.dumps(body),
                                  params=params, config=config)

    @required(cluster_id=(bytes, str))  # ***Unicode***
    def cancel_autoRenew_volume_cluster(self, cluster_id, client_token=None, config=None):
        """
        cancel_autoRenew_volume_cluster
        """
        cluster_id = compat.convert_to_bytes(cluster_id)
        path = b'/volume/cluster/cancelAutoRenew'
        body = {
            'clusterId': cluster_id
        }
        params = None
        if client_token is None:
            params = {
                'clientToken': generate_client_token()
            }
        else:
            params = {
                'clientToken': client_token
            }
        return self._send_request(http_methods.POST, path, json.dumps(body),
                                  params=params, config=config)

    def list_recycled_instances(self, marker=None, max_keys=None, instance_id=None, name=None, payment_timing=None,
                                recycle_begin=None, recycle_end=None, config=None):
        """
        Lists recycled instances.

        :param marker:
            The optional parameter marker specified in the original request to specify
            where in the results to begin listing.
            Together with the marker, specifies the list result which listing should begin.
            If the marker is not specified, the list result will listing from the first one.
        :type marker: string

        :param max_keys:
            The optional parameter to specifies the max number of list result to return.
            The default value is 1000.
        :type max_keys: int

        :param instance_id:
            The identified of instance to specifies one instance.
        :type instance_id: string

        :param name:
            The name of instance to specifies one instance.
        :type name: string

        :param payment_timing:
            The payment timing of instance order values: [prepay/postpay].
        :type payment_timing: string

        :param recycle_begin:
            The begintime of the recycled instances date range. FORMAT: yyyy-MM-dd'T'HH:mm:ss'Z'
        :type recycle_begin: string

        :param recycle_end:
            The endtime of the recycled instances date range. FORMAT: yyyy-MM-dd'T'HH:mm:ss'Z'
        :type recycle_end: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/recycle/instance'

        body = {}
        if marker is not None:
            body['marker'] = marker
        if max_keys is not None:
            body['maxKeys'] = max_keys
        if instance_id is not None:
            body['instanceId'] = instance_id
        if name is not None:
            body['name'] = name
        if payment_timing is not None:
            body['paymentTiming'] = payment_timing
        if recycle_begin is not None:
            body['recycleBegin'] = recycle_begin
        if recycle_end is not None:
            body['recycleEnd'] = recycle_end
        return self._send_request(http_methods.POST, path, body=json.dumps(body), config=config)

    @required(spec=str, image_id=(bytes, str))  # ***Unicode***
    def create_instance_by_spec(self, spec, image_id, root_disk_size_in_gb=0, root_disk_storage_type=None,
                                ephemeral_disks=None, create_cds_list=None, network_capacity_in_mbps=0, eip_name=None,
                                internet_charge_type=None, purchase_count=1, name=None, hostname=None,
                                auto_seq_suffix=None, is_open_hostname_domain=None, admin_pass=None, billing=None,
                                zone_name=None, subnet_id=None, security_group_id=None,
                                enterprise_security_group_id=None, security_group_ids=None,
                                enterprise_security_group_ids=None, relation_tag=None, ehc_cluster_id=None,
                                is_open_ipv6=None, tags=None, key_pair_id=None, auto_renew_time_unit=None,
                                auto_renew_time=0, cds_auto_renew=None, asp_id=None, bid_model=None, bid_price=None,
                                dedicate_host_id=None, deploy_id=None, deploy_id_list=None, enable_jumbo_frame=None,
                                cpu_thread_config=None, numa_config=None, eni_ids=None,
                                client_token=None, config=None):
        """
        Create a bcc Instance with the specified options.
        You must fill the field of clientToken,which is especially for keeping idempotent.
        This is an asynchronous interface,
        you can get the latest status by BccClient.get_instance.

        :param spec:
            The specification of the BBC package.
        :type spec: string

        :param image_id:
            The id of image, list all available image in BccClient.list_images.
        :type image_id: string

        :param billing:
            Billing information.
        :type billing: bcc_model.Billing

        :param create_cds_list:
            The optional list of volume detail info to create.
        :type create_cds_list: list<bcc_model.CreateCdsModel>

        :param network_capacity_in_mbps:
            The optional parameter to specify the bandwidth in Mbps for the new instance.
            It must among 0 and 200, default value is 0.
            If it's specified to 0, it will get the internal ip address only.
        :type network_capacity_in_mbps: int

        :param eip_name:
            eip name
        :type eip_name: string

        :param purchase_count:
            The number of instance to buy, the default value is 1.
        :type purchase_count: int

        :param name:
            The optional parameter to desc the instance that will be created.
        :type name: string

        :param hostname:
            The optional parameter to specify the host name of the instance virtual machine.
            By default, hostname is not specified.
            If hostname is specified: hostname is used as the prefix of the name in batches.
            The backend will add a suffix, and the suffix generation method is: name{-serial number}.
            If name is not specified, it will be automatically generated using the following method:
            {instance-eight-digit random string-serial number}.
            Note: The random string is generated from the characters 0-9 and a-z;
            the serial number increases sequentially according to the magnitude of count.
            If count is 100, the serial number increases from 000~100, and if it is 10, it increases from 00~10.
            Only lowercase letters, numbers and - . special characters are supported.
            They must start with a letter. Special symbols cannot be used continuously.
            Special symbols are not supported at the beginning or end. The length is 2-64.
        :type hostname: string

        :param auto_seq_suffix:
            The parameter to specify whether name and hostname order suffixes are automatically generated.
        :type auto_seq_suffix: boolean

        :param is_open_hostname_domain:
            The parameter to specify whether hostname domain is automatically generated
        :type is_open_hostname_domain: boolean

        :param admin_pass:
            The optional parameter to specify the password for the instance.
            If specify the adminPass,the adminPass must be a 8-16 characters String
            which must contains letters, numbers and symbols.
            The symbols only contains "!@#$%^*()".
            The adminPass will be encrypted in AES-128 algorithm
            with the substring of the former 16 characters of user SecretKey.
            If not specify the adminPass, it will be specified by an random string.
            See more detail on
            https://bce.baidu.com/doc/BCC/API.html#.7A.E6.31.D8.94.C1.A1.C2.1A.8D.92.ED.7F.60.7D.AF
        :type admin_pass: string

        :param zone_name:
            The optional parameter to specify the available zone for the instance.
            See more detail through list_zones method
        :type zone_name: string

        :param subnet_id:
            The optional parameter to specify the id of subnet from vpc, optional param
             default value is default subnet from default vpc
        :type subnet_id: string

        :param security_group_id:
            The optional parameter to specify the securityGroupId of the instance
            vpcId of the securityGroupId must be the same as the vpcId of subnetId
            See more detail through listSecurityGroups method
        :type security_group_id: string

        :param enterprise_security_group_id:
            enterprise_security_group_id
        :type enterprise_security_group_id: string

        :param security_group_ids:
            security_group_ids
        :type security_group_ids: list<string>

        :param enterprise_security_group_ids:
            enterprise_security_group_ids
        :type enterprise_security_group_ids: list<string>

        :param relation_tag:
            The parameter to specify whether the instance related to existing tags
        :type relation_tag: boolean

        :param ehc_cluster_id:
            The id of ehcCluster.
        :type ehc_cluster_id: string

        :param is_open_ipv6:
            The parameter indicates whether the instance to be created is enabled for IPv6.
            It can only be enabled when both the image and subnet support IPv6.
            True indicates enabled, false indicates disabled,
            and no transmission indicates automatic adaptation of the image and subnet's IPv6 support
        :type is_open_ipv6: boolean

        :param deploy_id_list:
            This parameter is the list of deployment set IDs where the specified instance is located.
        :type deploy_id_list: list<string>

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if client token is provided.
            If the clientToken is not specified by the user,
            a random String generated by default algorithm will be used.
            See more detail at
            https://bce.baidu.com/doc/BCC/API.html#.E5.B9.82.E7.AD.89.E6.80.A7
        :type client_token: string

        :param root_disk_size_in_gb:
            The parameter to specify the root disk size in GB.
            The root disk excludes the system disk, available is 40-500GB.
        :type root_disk_size_in_gb: int

        :param root_disk_storage_type:
            The parameter to specify the root disk storage type.
            Default use of HP1 cloud disk.
        :type root_disk_storage_type: string

        :param ephemeral_disks:
            The optional list of ephemeral volume detail info to create.
        :type ephemeral_disks: list<bcc_model.EphemeralDisk>

        :param dedicate_host_id
            The parameter to specify the dedicate host id.
        :type dedicate_host_id: string

        :param auto_renew_time_unit
            The parameter to specify the unit of the auto renew time.
            The auto renew time unit can be "month" or "year".
            The default value is "month".
        :type auto_renew_time_unit: string

        :param auto_renew_time
            The parameter to specify the auto renew time, the default value is 0.
        :type auto_renew_time: int

        :param tags
            The optional list of tag to be bonded.
        :type tags: list<bcc_model.TagModel>

        :param deploy_id
            The parameter to specify the id of the deploymentSet.
        :type deploy_id: string

        :param bid_model
            The parameter to specify the bidding model.
            The bidding model can be "market" or "custom".
        :type bid_model: string

        :param bid_price
            The parameter to specify the bidding price.
            When the bid_model is "custom", it works.
        :type bid_price: string

        :param key_pair_id
            The parameter to specify id of the keypair.
        :type key_pair_id: string

        :param asp_id
            The parameter to specify id of the asp.
        :type asp_id: string

        :param internet_charge_type
            The parameter to specify the internet charge type.
            See more detail on
            https://cloud.baidu.com/doc/BCC/API.html#InternetChargeType
        :type internet_charge_type: string

        :param cds_auto_renew
            The parameter to specify whether the cds is auto renew or not.
            The default value is false.
        :type cds_auto_renew: boolean

        :param enable_jumbo_frame:
            The parameter indicates whether the instance is enabled for JumboFrame.
            It can only be enabled when the flavor support JumboFrame.
            True indicates enabled, false indicates disabled,
        :type enable_jumbo_frame: bool

        :param cpu_thread_config:
            Manage hyper - threading, which is the same on both Intel and AMD platforms.
        :type cpu_thread_config: string

        :param numa_config:
            Manage NPS on AMD platforms. Manage NUMA on Intel platforms.
        :type numa_config: string

        :param eni_ids:
            The optional list of eni short ids to attach.
            The number of eniIds must be an integer multiple of the number of instances.
            The enis must in the same vpc and available zone with instance.
        :type eni_ids: list<string>

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instanceBySpec'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        if billing is None:
            billing = default_billing_to_purchase_created
        body = {
            'spec': spec,
            'imageId': image_id,
            'billing': billing.__dict__
        }
        if root_disk_size_in_gb != 0:
            body['rootDiskSizeInGb'] = root_disk_size_in_gb
        if root_disk_storage_type is not None:
            body['rootDiskStorageType'] = root_disk_storage_type
        if create_cds_list is not None:
            body['createCdsList'] = [create_cds.__dict__ for create_cds in create_cds_list]
        if network_capacity_in_mbps != 0:
            body['networkCapacityInMbps'] = network_capacity_in_mbps
        if eip_name is not None:
            body['eipName'] = eip_name
        if purchase_count > 0:
            body['purchaseCount'] = purchase_count
        if name is not None:
            body['name'] = name
        if hostname is not None:
            body['hostname'] = hostname
        if auto_seq_suffix is not None:
            body['autoSeqSuffix'] = auto_seq_suffix
        if is_open_hostname_domain is not None:
            body['isOpenHostnameDomain'] = is_open_hostname_domain
        if admin_pass is not None:
            secret_access_key = self.config.credentials.secret_access_key
            cipher_admin_pass = aes128_encrypt_16char_key(admin_pass, secret_access_key)
            body['adminPass'] = cipher_admin_pass
        if zone_name is not None:
            body['zoneName'] = zone_name
        if subnet_id is not None:
            body['subnetId'] = subnet_id
        if security_group_id is not None:
            body['securityGroupId'] = security_group_id
        if enterprise_security_group_id is not None:
            body['enterpriseSecurityGroupId'] = enterprise_security_group_id
        if security_group_ids is not None:
            body['securityGroupIds'] = security_group_ids
        if enterprise_security_group_ids is not None:
            body['enterpriseSecurityGroupIds'] = enterprise_security_group_ids
        if auto_renew_time != 0:
            body['autoRenewTime'] = auto_renew_time
        if auto_renew_time_unit is None:
            body['autoRenewTimeUnit'] = "month"
        else:
            body['autoRenewTimeUnit'] = auto_renew_time_unit
        if ephemeral_disks is not None:
            body['ephemeralDisks'] = [ephemeral_disk.__dict__ for ephemeral_disk in ephemeral_disks]
        if dedicate_host_id is not None:
            body['dedicatedHostId'] = dedicate_host_id
        if deploy_id is not None:
            body['deployId'] = deploy_id
        if deploy_id_list is not None:
            body['deployIdList'] = deploy_id_list
        if bid_model is not None:
            body['bidModel'] = bid_model
        if bid_price is not None:
            body['bidPrice'] = bid_price
        if key_pair_id is not None:
            body['keypairId'] = key_pair_id
        if internet_charge_type is not None:
            body['internetChargeType'] = internet_charge_type
        if asp_id is not None:
            body['aspId'] = asp_id
        if relation_tag is not None:
            body['relationTag'] = relation_tag
        if ehc_cluster_id is not None:
            body['ehcClusterId'] = ehc_cluster_id
        if is_open_ipv6 is not None:
            body['isOpenIpv6'] = is_open_ipv6
        if tags is not None:
            tag_list = [tag.__dict__ for tag in tags]
            body['tags'] = tag_list
        if enable_jumbo_frame is not None:
            body['enableJumboFrame'] = enable_jumbo_frame
        if cpu_thread_config is not None:
            body['cpuThreadConfig'] = cpu_thread_config
        if numa_config is not None:
            body['numaConfig'] = numa_config
        if eni_ids is not None:
            body['eniIds'] = eni_ids
        body['cdsAutoRenew'] = cds_auto_renew

        return self._send_request(http_methods.POST, path, json.dumps(body),
                                  params=params, config=config)

    @required(instance_id=(bytes, str))
    def auto_release_instance(self, instance_id, release_time=None, client_token=None, config=None):
        """
            set instance auto release.

        :param instance_id:
            The id of instance.
        :type instance_id: string

        :param release_time:
            The new value for instance's name.
        :type release_time: string in format yyyy-MM-dd'T'HH:mm:ss'Z'.

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if client token is provided.
            If the clientToken is not specified by the user,
            a random String generated by default algorithm will be used.
            See more detail at
            https://bce.baidu.com/doc/BCC/API.html#.E5.B9.82.E7.AD.89.E6.80.A7
        :type client_token: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        params = {
            'autorelease': None,
        }
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        instance_id = compat.convert_to_bytes(instance_id)
        # instance_id = instance_id.encode(encoding='utf-8')
        path = b'/instance/%s' % instance_id
        body = {
            'releaseTime': release_time
        }
        return self._send_request(http_methods.PUT, path, body=json.dumps(body), params=params, config=config)

    @required(instance_id=(bytes, str))  # ***Unicode***
    def release_instance_with_related_resources(self, instance_id, related_release_flag=None,
                                                delete_cds_snapshot_flag=None, delete_related_enis_flag=None,
                                                bcc_recycle_flag=None, client_token=None, config=None):
        """
        Releasing the instance owned by the user.
        Only the Postpaid instance or Prepaid which is expired can be released.
        After releasing the instance,
        all of the data will be deleted.
        all of volumes attached will be auto detached, but the volume snapshots will be saved.
        all of snapshots created from original instance system disk will be deleted,
        all of customized images created from original instance system disk will be reserved.

        :param instance_id:
            The id of instance.
        :type instance_id: string

        :param related_release_flag:
            Release or not related resources.
        :type related_release_flag: bool

        :param delete_cds_snapshot_flag:
            Delete or not cds snapshot.
        :type delete_cds_snapshot_flag: bool

        :param delete_related_enis_flag:
            Delete or not related enis.
        :type delete_related_enis_flag: bool

        :param bcc_recycle_flag:
            Recycle or not bcc instance.
        :type bcc_recycle_flag: bool

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        instance_id = compat.convert_to_bytes(instance_id)
        path = b'/instance/%s' % instance_id
        body = {}
        if related_release_flag is not None:
            body['relatedReleaseFlag'] = related_release_flag
        if delete_cds_snapshot_flag is not None:
            body['deleteCdsSnapshotFlag'] = delete_cds_snapshot_flag
        if delete_related_enis_flag is not None:
            body['deleteRelatedEnisFlag'] = delete_related_enis_flag
        if bcc_recycle_flag is not None:
            body['bccRecycleFlag'] = bcc_recycle_flag
        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params, config=config)

    @required(instance_id=(bytes, str))  # ***Unicode***
    def release_prepaid_instance_with_related_resources(self, instance_id, related_release_flag=None,
                                                        delete_cds_snapshot_flag=None, delete_related_enis_flag=None,
                                                        client_token=None, config=None):
        """
        Releasing the instance owned by the user.
        Only the Prepaid instance and the instance has not expired can be released.
        After releasing the instance,
        all of the data will be deleted.
        all of volumes attached will be auto detached, but the volume snapshots will be saved.
        all of snapshots created from original instance system disk will be deleted,
        all of customized images created from original instance system disk will be reserved.

        :param instance_id:
            The id of instance.
        :type instance_id: string

        :param related_release_flag:
            Release or not related resources.
        :type related_release_flag: bool

        :param delete_cds_snapshot_flag:
            Delete or not cds snapshot.
        :type delete_cds_snapshot_flag: bool

        :param delete_related_enis_flag:
            Delete or not related enis.
        :type delete_related_enis_flag: bool

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        path = b'/instance/delete'
        body = {}
        body['instanceId'] = instance_id
        if related_release_flag is not None:
            body['relatedReleaseFlag'] = related_release_flag
        if delete_cds_snapshot_flag is not None:
            body['deleteCdsSnapshotFlag'] = delete_cds_snapshot_flag
        if delete_related_enis_flag is not None:
            body['deleteRelatedEnisFlag'] = delete_related_enis_flag
        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params, config=config)

    @required(instance_id=(bytes, str))  # ***Unicode***
    def get_instance_with_deploy_set(self, instance_id, contains_failed=None, config=None):
        """
        Get the detail information of specified instance.

        :param instance_id:
            The id of instance.
        :type instance_id: string

        :param contains_failed:
            The optional parameters to get the failed message.If true, it means get the failed message.
        :type contains_failed: boolean

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        instance_id = instance_id.encode(encoding='utf-8')
        path = b'/instance/%s' % instance_id
        params = {
            'isDeploySet': True
        }

        if contains_failed:
            params['containsFailed'] = contains_failed

        return self._send_request(http_methods.GET, path, params=params, config=config)

    @required(instance_id=(bytes, str))  # ***Unicode***
    def get_instance_with_deploy_set_and_failed(self, instance_id, contains_failed=None, config=None):
        """
        Get the detail information of specified instance.

        :param instance_id:
            The id of instance.
        :type instance_id: string

        :param contains_failed:
            The optional parameters to get the failed message.If true, it means get the failed message.
        :type contains_failed: boolean

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        instance_id = instance_id.encode(encoding='utf-8')
        path = b'/instance/%s' % instance_id
        params = {
            'containsFailed': None
        }

        if contains_failed:
            params['containsFailed'] = contains_failed

        return self._send_request(http_methods.GET, path, params=params, config=config)

    @required(instance_id=(bytes, str), hostname=str)  # ***Unicode***
    def modify_instance_hostname(self, instance_id, hostname, reboot=None, is_open_hostname_domain=None,
                                 client_token=None, config=None):
        """
        modify instance hostname

        :param instance_id:
            The id of instance.
        :type instance_id: string

        :param hostname:
            new hostname
        :type hostname: string, FORMAT ^([a-z]+)((\.|-)?[a-z0-9]+)*$

        :param reboot:
            Auto reboot the instance after hostname changed.
        :type reboot: bool

        :param is_open_hostname_domain:
            Set hostname domain opening
        :type is_open_hostname_domain: bool

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        params = {
            "changeHostname": None
        }
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        instance_id = compat.convert_to_bytes(instance_id)
        path = b'/instance/%s' % instance_id
        body = {
            "hostname": hostname
        }
        if reboot is not None:
            body['reboot'] = reboot
        if is_open_hostname_domain is not None:
            body['isOpenHostnameDomain'] = is_open_hostname_domain
        return self._send_request(http_methods.PUT, path, body=json.dumps(body), params=params, config=config)

    @required(instance_id_list=(list))  # ***Unicode***
    def recovery_instances(self, instance_id_list, client_token=None, config=None):
        """
        Recovery multi instances

        :param instance_id_list:
            The id list of instances to recovery.
        :type instance_id_list: list of string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        path = b'/instance/recovery'
        list_of_item = []
        for instance_id in instance_id_list:
            list_of_item.append({'instanceId': instance_id})
        body = {
            "instanceIds": list_of_item
        }
        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params, config=config)

    @required(instance_ids=(list))
    def batch_refund_resources(self, instance_ids, related_release_flag=None,
                               delete_cds_snapshot_flag=None, delete_related_enis_flag=None,
                               client_token=None, config=None):
        """
        Releasing the instance owned by the user.
        Only the Prepaid instance and the instance has not expired can be released.
        After releasing the instance, all of the data will be deleted.

        :param instance_ids:
             The id list of instances.
        :type instance_ids: list of string


        :param related_release_flag:
            Release or not related resources.
        :type related_release_flag: bool

        :param delete_cds_snapshot_flag:
            Delete or not cds snapshot.
        :type delete_cds_snapshot_flag: bool

        :param delete_related_enis_flag:
            Delete or not related enis.
        :type delete_related_enis_flag: bool

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        path = b'/instance/batchRefundResource'
        body = {
            "instanceIds": instance_ids
        }
        if related_release_flag is not None:
            body['relatedReleaseFlag'] = related_release_flag
        if delete_cds_snapshot_flag is not None:
            body['deleteCdsSnapshotFlag'] = delete_cds_snapshot_flag
        if delete_related_enis_flag is not None:
            body['deleteRelatedEnisFlag'] = delete_related_enis_flag
        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params, config=config)

    @required(instance_type=str, cpu_count=int, memory_cap_in_gb=int)  # ***Unicode***
    def get_bid_instance_price(self, instance_type, cpu_count, memory_cap_in_gb,
                               root_disk_size_in_gb=None, root_disk_storage_type=None, create_cds_list=None,
                               purchase_count=1, name=None, admin_pass=None, key_pair_id=None, asp_id=None,
                               image_id=None, bid_model=None, bid_price=None, network_cap_in_mbps=None,
                               relation_tag=None, tags=None, security_group_id=None, subnet_id=None,
                               zone_name=None, internet_charge_type=None, client_token=None, config=None):
        """
        Query bid instance price in market.

        :param instance_type:
            The specified Specification to create the instance,
            See more detail on
            https://cloud.baidu.com/doc/BCC/API.html#InstanceType
        :type instance_type: string

        :param cpu_count:
            The parameter to specified the cpu core to create the instance.
        :type cpu_count: int

        :param memory_cap_in_gb:
            The parameter to specified the capacity of memory in GB to create the instance.
        :type memory_cap_in_gb: int

        :param image_id:
            The id of image, list all available image in BccClient.list_images.
        :type image_id: string

        :param create_cds_list:
            The optional list of volume detail info to create.
        :type create_cds_list: list<bcc_model.CreateCdsModel>

        :param network_cap_in_mbps:
            The optional parameter to specify the bandwidth in Mbps for the new instance.
            It must among 0 and 200, default value is 0.
            If it's specified to 0, it will get the internal ip address only.
        :type network_cap_in_mbps: int

        :param purchase_count:
            The number of instance to buy, the default value is 1.
        :type purchase_count: int

        :param name:
            The optional parameter to desc the instance that will be created.
        :type name: string

        :param admin_pass:
            The optional parameter to specify the password for the instance.
            If specify the adminPass,the adminPass must be a 8-16 characters String
            which must contains letters, numbers and symbols.
            The symbols only contains "!@#$%^*()".
            The adminPass will be encrypted in AES-128 algorithm
            with the substring of the former 16 characters of user SecretKey.
            If not specify the adminPass, it will be specified by an random string.
            See more detail on
            https://bce.baidu.com/doc/BCC/API.html#.7A.E6.31.D8.94.C1.A1.C2.1A.8D.92.ED.7F.60.7D.AF
        :type admin_pass: string

        :param zone_name:
            The optional parameter to specify the available zone for the instance.
            See more detail through list_zones method
        :type zone_name: string

        :param subnet_id:
            The optional parameter to specify the id of subnet from vpc, optional param
             default value is default subnet from default vpc
        :type subnet_id: string

        :param security_group_id:
            The optional parameter to specify the securityGroupId of the instance
            vpcId of the securityGroupId must be the same as the vpcId of subnetId
            See more detail through listSecurityGroups method
        :type security_group_id: string

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if client token is provided.
            If the clientToken is not specified by the user,
            a random String generated by default algorithm will be used.
            See more detail at
            https://bce.baidu.com/doc/BCC/API.html#.E5.B9.82.E7.AD.89.E6.80.A7
        :type client_token: string

        :param root_disk_size_in_gb:
            The parameter to specify the root disk size in GB.
            The root disk excludes the system disk, available is 40-500GB.
        :type root_disk_size_in_gb: int

        :param root_disk_storage_type:
            The parameter to specify the root disk storage type.
            Default use of HP1 cloud disk.
        :type root_disk_storage_type: string

        :param relation_tag
            Set whether the tags specified by the instance to ne queried needs
            to be associated with an existing tag key.
            The default value is false, this param is optional.
        :type relation_tag: bool

        :param tags
            The optional list of tag to be bonded.
        :type tags: list<bcc_model.TagModel>

        :param bid_model
            The parameter to specify the bidding model.
            The bidding model can be "market" or "custom".
        :type bid_model: string

        :param bid_price
            The parameter to specify the bidding price.
            When the bid_model is "custom", it works.
        :type bid_price: string

        :param key_pair_id
            The parameter to specify id of the keypair.
        :type key_pair_id: string

        :param asp_id
            The parameter to specify id of the asp.
        :type asp_id: string

        :param internet_charge_type
            The parameter to specify the internet charge type.
            See more detail on
            https://cloud.baidu.com/doc/BCC/API.html#InternetChargeType
        :type internet_charge_type: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/bidPrice'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token

        body = {
            'cpuCount': cpu_count,
            'memoryCapacityInGB': memory_cap_in_gb,
            'instanceType': instance_type
        }
        if image_id is not None:
            body['imageId'] = image_id
        if root_disk_size_in_gb != 0:
            body['rootDiskSizeInGb'] = root_disk_size_in_gb
        if root_disk_storage_type is not None:
            body['rootDiskStorageType'] = root_disk_storage_type
        if create_cds_list is not None:
            body['createCdsList'] = [create_cds.__dict__ for create_cds in create_cds_list]
        if purchase_count > 0:
            body['purchaseCount'] = purchase_count
        if name is not None:
            body['name'] = name
        if admin_pass is not None:
            secret_access_key = self.config.credentials.secret_access_key
            cipher_admin_pass = aes128_encrypt_16char_key(admin_pass, secret_access_key)
            body['adminPass'] = cipher_admin_pass
        if zone_name is not None:
            body['zoneName'] = zone_name
        if subnet_id is not None:
            body['subnetId'] = subnet_id
        if security_group_id is not None:
            body['securityGroupId'] = security_group_id
        if bid_model is not None:
            body['bidModel'] = bid_model
        if bid_price is not None:
            body['bidPrice'] = bid_price
        if key_pair_id is not None:
            body['keypairId'] = key_pair_id
        if internet_charge_type is not None:
            body['internetChargeType'] = internet_charge_type
        if asp_id is not None:
            body['aspId'] = asp_id
        if relation_tag is not None:
            body['relationTag'] = relation_tag
        if tags is not None:
            tag_list = [tag.__dict__ for tag in tags]
            body['tags'] = tag_list
        if network_cap_in_mbps is not None:
            body['networkCapacityInMbps'] = network_cap_in_mbps

        return self._send_request(http_methods.POST, path, json.dumps(body), params=params, config=config)

    def list_bid_flavor(self, client_token=None, config=None):
        """
        Get all bid flavors.

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        path = b'/instance/bidFlavor'
        return self._send_request(http_methods.POST, path, params=params, config=config)

    @required(instance_id=(bytes, str), deletion_protection=int)
    def modify_deletion_protection(self, instance_id, deletion_protection, client_token=None, config=None):
        """
        Set instance deleion protection.

        :param instance_id
            The id of instance.
        :type instance_id: string

        :param deletion_protection
            The status of instance deletion protection. 1:enable, 0:disable.
        :type deletion_protection: int

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        instance_id = instance_id.encode(encoding='utf-8')
        path = b'/instance/%s/deletionProtection' % instance_id
        body = {
            "deletionProtection": deletion_protection
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body), params=params, config=config)

    @required(instance_id=(bytes, str), is_eip_auto_related_delete=bool)
    def modify_related_delete_policy(self, instance_id, is_eip_auto_related_delete, client_token=None, config=None):
        """
        Set bid instance eip_auto_related_delete.

        :param instance_id
            The id of instance.
        :type instance_id: string

        :param is_eip_auto_related_delete
            Enables the deletion of the related EIP of bid instance when the instance is being deleted.
        :type is_eip_auto_related_delete: bool

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        instance_id = instance_id.encode(encoding='utf-8')
        path = b'/instance/%s/modifyRelatedDeletePolicy' % instance_id
        body = {
            "isEipAutoRelatedDelete": is_eip_auto_related_delete
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body), params=params, config=config)

    @required(volume_id=(bytes, str))  # ***Unicode***
    def release_volume_new(self, volume_id, auto_snapshot=None, manual_snapshot=None,
                           recycle=None, client_token=None, config=None):
        """
        Releasing the specified volume owned by the user.
        You can release the specified volume only
        when the instance is among state of  Available/Expired/Error,
        otherwise, it's will get 409 errorCode.

        :param volume_id:
            The id of the volume which will be released.
        :type volume_id: string

        :param auto_snapshot:
            Snapshot volume automatically. value: 'on'/'off'. Default value: 'off'.
        :type auto_snapshot: string

        :param manual_snapshot:
            Snapshot volume manually. value: 'on'/'off'. Default value: 'off'.
        :type manual_snapshot: string

        :param recycle:
            where recycle volume or not, value: 'on'/'off'. Default value: 'on'.
        :type recycle: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        volume_id = volume_id.encode(encoding='utf-8')
        path = b'/volume/%s' % volume_id
        body = {}
        if auto_snapshot is not None:
            body['autoSnapshot'] = auto_snapshot
        if manual_snapshot is not None:
            body['manualSnapshot'] = manual_snapshot
        if recycle is not None:
            body['recycle'] = recycle

        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params, config=config)

    @required(volume_id=str, renew_time=int, renew_time_unit=str)  # ***Unicode***
    def auto_renew_cds_volume(self, volume_id, renew_time, renew_time_unit, client_token=None, config=None):
        """
        set auto_renew_cds_volume

        :param volume_id:
            The id of the volume which will be renewed.
        :type volume_id: string

        :param renew_time:
            Auto renew start time.
            Value:
                - month: 1 ~ 9
                - year: 1 ~ 3
        :type renew_time: string

        :param renew_time_unit:
            Choose automatic monthly or annual renewals. value: 'month'/'year'
        :type renew_time_unit: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        path = b'/volume/autoRenew'
        body = {
            'volumeId': volume_id,
            'renewTime': renew_time,
            'renewTimeUnit': renew_time_unit
        }

        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params, config=config)

    @required(volume_id=str)  # ***Unicode***
    def cancel_auto_renew_cds_volume(self, volume_id, client_token=None, config=None):
        """
        cancel_auto_renew_volume_cluster

        :param volume_id:
            The id of the volume which will be renewed.
        :type volume_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/volume/cancelAutoRenew'
        body = {
            'volumeId': volume_id
        }
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        return self._send_request(http_methods.POST, path, json.dumps(body),
                                  params=params, config=config)

    @required(zone_name=str)  # ***Unicode***
    def get_available_disk_info(self, zone_name, client_token=None, config=None):
        """
        get_available_disk_info

        :param zone_name:
            The name of available zone for volume to use.
        :type zone_name: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/volume/disk'
        params = {
            'zoneName': zone_name
        }
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        return self._send_request(http_methods.GET, path, params=params, config=config)

    @required(volume_id=str)  # ***Unicode***
    def tag_volume(self, volume_id, relation_tag=None, tags=None, client_token=None, config=None):
        """
        bind tags to volume

        :param volume_id:
            The id of the volume which will be renewed.
        :type volume_id: string

        :param tags
            The optional list of tag to be bonded.
        :type tags: list<bcc_model.TagModel>

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        params = {
            'bind': None
        }
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        volume_id = volume_id.encode(encoding='utf-8')
        path = b'/volume/%s/tag' % volume_id
        body = {}
        if relation_tag is not None:
            body['relationTag'] = relation_tag
        if tags is not None:
            tag_list = [tag.__dict__ for tag in tags]
            body['changeTags'] = tag_list

        return self._send_request(http_methods.PUT, path, json.dumps(body), params=params, config=config)

    @required(volume_id=str)  # ***Unicode***
    def untag_volume(self, volume_id, relation_tag=None, tags=None, client_token=None, config=None):
        """
        unbind tags to volume

        :param volume_id:
            The id of the volume which will be renewed.
        :type volume_id: string

        :param tags
            The optional list of tag to be bonded.
        :type tags: list<bcc_model.TagModel>

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        params = {
            'unbind': None
        }
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        volume_id = volume_id.encode(encoding='utf-8')
        path = b'/volume/%s/tag' % volume_id
        body = {}
        if relation_tag is not None:
            body['relationTag'] = relation_tag
        if tags is not None:
            tag_list = [tag.__dict__ for tag in tags]
            body['changeTags'] = tag_list

        return self._send_request(http_methods.PUT, path, json.dumps(body), params=params, config=config)

    @required(volume_id=str)  # ***Unicode***
    def list_snapshot_chain(self, volume_id, order=None, order_by=None,
                            page_no=None, page_size=None, client_token=None, config=None):
        """
        list_snapshot_chain

        :param volume_id:
            The id of the volume which will be renewed.
        :type volume_id: string

        :param order
            The response list order. Value: asc/desc
        :type order: string

        :param order_by
            The response list order. Value: chainId(default)/chainSize/volumeSize
        :type order_by: string

        :param page_no
            page number. default value = 1
        :type page_no: int

        :param page_size
            page size. default value  = 1000
        :type page_size: int

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/snapshot/chain'
        params = {
            'volumeId': volume_id
        }
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        if order is not None:
            params['order'] = order
        if order_by is not None:
            params['orderBy'] = order_by
        if page_no is not None:
            params['pageNo'] = page_no
        if page_size is not None:
            params['pageSize'] = page_size

        return self._send_request(http_methods.GET, path, params=params, config=config)

    @required(chain_id=str)  # ***Unicode***
    def tag_snapshot_chain(self, chain_id, tags=None, client_token=None, config=None):
        """
        bind tags to snapshot chain

        :param chain_id:
            The id of the volume which will be renewed.
        :type chain_id: string

        :param tags
            The optional list of tag to be bonded.
        :type tags: list<bcc_model.TagModel>

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        params = {
            'bind': None
        }
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        chain_id = chain_id.encode(encoding='utf-8')
        path = b'/snapshot/chain/%s/tag' % chain_id
        body = {}
        if tags is not None:
            tag_list = [tag.__dict__ for tag in tags]
            body['changeTags'] = tag_list

        return self._send_request(http_methods.PUT, path, json.dumps(body), params=params, config=config)

    @required(chain_id=str)  # ***Unicode***
    def untag_snapshot_chain(self, chain_id, tags=None, client_token=None, config=None):
        """
        unbind tags to snapshot chain

        :param chain_id:
            The id of the volume which will be renewed.
        :type chain_id: string

        :param tags
            The optional list of tag to be bonded.
        :type tags: list<bcc_model.TagModel>

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        params = {
            'unbind': None
        }
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        chain_id = chain_id.encode(encoding='utf-8')
        path = b'/snapshot/chain/%s/tag' % chain_id
        body = {}
        if tags is not None:
            tag_list = [tag.__dict__ for tag in tags]
            body['changeTags'] = tag_list

        return self._send_request(http_methods.PUT, path, json.dumps(body), params=params, config=config)

    def update_asp(self, name=None, asp_id=None, time_points=None, repeat_week_days=None, retention_days=None,
                   client_token=None, config=None):
        """
        update asp
        Attention: Param name and asp_id can not both be none.

        :param name:
            The name of the asp.
        :type name: string

        :param asp_id:
            Identify of asp.
        :type asp_id: string

        :param time_points:
            Daily triggering time(hour of day, 0 ~ 23) of snapshot policy. e.g. [0, 6, 12, 18].
        :type time_points: list

        :param repeat_week_days:
            Weekly triggering time(day of week, 0 ~ 6, 0 means Sunday) of snapshot policy. e.g. [1, 3]
        :type repeat_week_days: list

        :param retention_days:
            Retention days of snapshot.
        :type retention_days: int

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/asp/update'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token

        body = {}
        if name is not None:
            body['name'] = name
        if asp_id is not None:
            body['aspId'] = asp_id
        if time_points is not None:
            body['timePoints'] = time_points
        if repeat_week_days is not None:
            body['repeatWeekdays'] = repeat_week_days
        if retention_days is not None:
            body['retentionDays'] = retention_days

        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    def get_price_by_spec(self, spec_id=None, spec=None, payment_timing=None, zone_name=None, purchase_num=None,
                          purchase_length=None, client_token=None, config=None):
        """
        Get price of instance flover by spec.
        Attention: Param spec_id and spec can not both be none.

        :param spec_id:
            Identify of the spec.
        :type spec_id: string

        :param spec:
            The name of spec.
        :type spec: string

        :param payment_timing:
            Payment timing of instance, prepay or postpay.
        :type payment_timing: string

        :param zone_name:
            Name of available zone.
        :type zone_name: string

        :param purchase_num:
            Number of purchase.
        :type purchase_num: int

        :param purchase_length:
            Reservation time.
        :type purchase_length: int

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/price'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token

        body = {}
        if spec_id is not None:
            body['specId'] = spec_id
        if spec is not None:
            body['spec'] = spec
        if payment_timing is not None:
            body['paymentTiming'] = payment_timing
        if zone_name is not None:
            body['zoneName'] = zone_name
        if purchase_num is not None:
            body['purchaseCount'] = purchase_num
        if purchase_length is not None:
            body['purchaseLength'] = purchase_length

        return self._send_request(http_methods.POST, path, json.dumps(body),
                                  params=params, config=config)

    def list_type_zones(self, spec_id=None, spec=None, product_type=None, instance_type=None,
                        client_token=None, config=None):
        """
        list the logicalZone from the bcc package specification.

        :param spec_id:
            Identify of the spec.
        :type spec_id: string

        :param spec:
            The name of spec.
        :type spec: string

        :param product_type:
            Payment timing of instance, prepay or postpay.
        :type product_type: string

        :param instance_type:
            The specified Specification to create the instance,
            See more detail on
            https://cloud.baidu.com/doc/BCC/API.html#InstanceType
        :type instance_type: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/flavorZones'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        if spec_id is not None:
            params['specId'] = spec_id
        if spec is not None:
            params['spec'] = spec
        if product_type is not None:
            params['productType'] = product_type
        if instance_type is not None:
            params['instanceType'] = instance_type

        return self._send_request(http_methods.GET, path, prefix=b"/v1", params=params, config=config)

    def instance_change_subnet(self, instance_id, subnet_id=None,
                               internal_ip=None, reboot=None,
                               security_group_ids=None, enterprise_security_group_ids=None,
                               client_token=None, config=None):
        """
        Change instance subnet by id.

        :param instance_id:
            Identify of the instance.
        :type instance_id: string

        :param subnet_id:
            New subnet id.
        :type subnet_id: string

        :param internal_ip:
            Ip address of internal network.
        :type internal_ip: string

        :param reboot:
        Reboot instance or not. Default value is False.
        :type reboot: bool

        :param security_group_ids:
        :type security_group_ids: list<string>

        :param enterprise_security_group_ids:
        :type enterprise_security_group_ids: list<string>

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/subnet/changeSubnet'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token

        body = {}
        if instance_id is not None:
            body['instanceId'] = instance_id
        if subnet_id is not None:
            body['subnetId'] = subnet_id
        if internal_ip is not None:
            body['internalIp'] = internal_ip
        if reboot is not None:
            body['reboot'] = reboot

        if security_group_ids is not None:
            body['securityGroupIds'] = security_group_ids

        if enterprise_security_group_ids is not None:
            body['enterpriseSecurityGroupIds'] = enterprise_security_group_ids

        return self._send_request(http_methods.PUT, path, body=json.dumps(body), params=params, config=config)

    def instance_change_vpc(self, instance_id, subnet_id=None,
                            internal_ip=None, reboot=None, security_group_ids=None, enterprise_security_group_ids=None,
                            client_token=None, config=None):
        """
        Change instance vpc by id.

        :param instance_id:
            Identify of the instance.
        :type instance_id: string

        :param subnet_id:
            New subnet id.
        :type subnet_id: string

        :param internal_ip:
            Ip address of internal network.
        :type internal_ip: string

        :param reboot:
        Reboot instance or not. Default value is False.
        :type reboot: bool

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/vpc/changeVpc'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token

        body = {}
        if instance_id is not None:
            body['instanceId'] = instance_id
        if subnet_id is not None:
            body['subnetId'] = subnet_id
        if internal_ip is not None:
            body['internalIp'] = internal_ip
        if reboot is not None:
            body['reboot'] = reboot
        if security_group_ids is not None:
            body['securityGroupIds'] = security_group_ids
        if enterprise_security_group_ids is not None:
            body['enterpriseSecurityGroupIds'] = enterprise_security_group_ids

        return self._send_request(http_methods.PUT, path, body=json.dumps(body), params=params, config=config)

    @required(chain_id=str)  # ***Unicode***
    def list_instance_enis(self, instance_id, client_token=None, config=None):
        """
        Change instance vpc by id.

        :param instance_id:
            Identify of the instance.
        :type instance_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        instance_id = instance_id.encode(encoding='utf-8')
        path = b'/eni/%s' % instance_id
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token

        return self._send_request(http_methods.GET, path, params=params, config=config)

    def list_flavor_spec(self, zone_name=None, client_token=None, config=None):
        """
        Change instance vpc by id.

        :param zone_name:
            Available zone name
        :type zone_name: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/flavorSpec'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        if zone_name is not None:
            params['zoneName'] = zone_name

        return self._send_request(http_methods.GET, path, params=params, config=config)

    def resize_instance_by_spec(self, instance_id, spec, enable_jumbo_frame=None, client_token=None, config=None):
        """
        Resize instance by spec.

        :param instance_id:
            Identify of the instance.
        :type instance_id: string

        :param spec:
            The name of spec.
        :type spec: string

        :param enable_jumbo_frame:
            The parameter of specified the instance enable/disable jumbo frame.
            True means enable jumbo frame, false means disable jumbo frame.
            enable_jumbo_frame default None which means:
            When you change to the spec which doesn't support jumbo frame, the jumbo frame will be disabled.
            When the original instance don't support jumbo frame and you change to the spec which support jumbo frame,
            the jumbo frame will be disabled.
            When the original spec of the instance support jumbo frame , then you change to the spec which support jumbo
            frame, if the original instance enable jumbo frame, the jumbo frame will be enabled, if the original instance
            disable jumbo frame, the jumbo frame will be disabled.
        :type enable_jumbo_frame: bool

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        instance_id = instance_id.encode(encoding='utf-8')
        path = b'/instanceBySpec/%s' % instance_id
        params = {
            "resize": None
        }
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            "spec": spec
        }
        if enable_jumbo_frame is not None:
            body['enableJumboFrame'] = enable_jumbo_frame

        return self._send_request(http_methods.PUT, path, body=json.dumps(body), params=params, config=config)

    def batch_rebuild_instances(self, image_id, admin_pass, instance_ids, keypair_id=None,
                                client_token=None, config=None):
        """
        Batch rebuild instances.

        :param image_id:
            Image id for rebuild.
        :type image_id: string

        :param admin_pass:
            The password of admin.
        :type admin_pass: string

        :param instance_ids:
            Identify list of instances need to rebuild.
        :type instance_ids: list of string

        :param keypair_id:
            Set the id of the keypair to be bound. (optional param)
        :type keypair_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/rebuild'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            "imageId": image_id,
            "instanceIds": instance_ids
        }
        if admin_pass is not None:
            secret_access_key = self.config.credentials.secret_access_key
            cipher_admin_pass = aes128_encrypt_16char_key(admin_pass, secret_access_key)
            body['adminPass'] = cipher_admin_pass
        if keypair_id is not None:
            body['keypairId'] = keypair_id
        return self._send_request(http_methods.PUT, path, body=json.dumps(body), params=params, config=config)

    def change_to_prepaid(self, instance_id, duration, relation_cds, auto_renew, auto_renew_period=None,
                          client_token=None, config=None):
        """
        Change instance pay timing to prepaid.

        :param instance_id:
            Identify of the instance to change
        :type instance_id: string

        :param duration:
            Set the duration time of prepayment, unit:month.
        :type duration: int

        :param relation_cds:
            Set whether to chagne the associated data disk. True - change; False - no change. Default is False.
        :type relation_cds: bool

        :param auto_renew:
            Whether to enable automatic renewal, defaults to False.
        :type auto_renew: bool


        :param auto_renew_period:
            Duration of each automatic renewal(Unit: months).
            Value range: 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 24, 36. If not specified, the default is 1.
            This parameter is effective only when auto_renew is set to true.
        :type auto_renew_period: int

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        instance_id = instance_id.encode(encoding='utf-8')
        path = b'/instance/%s' % instance_id
        params = {
            'toPrepay': None
        }
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            "duration": duration
        }
        if auto_renew is not None:
            body['autoRenew'] = auto_renew
            body['autoRenewPeriod'] = auto_renew_period
        if relation_cds is not None:
            body['relationCds'] = relation_cds
        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params, config=config)

    def list_instance_no_charge(self, marker=None, max_keys=None, internal_ip=None, keypair_id=None,
                                zone_name=None, client_token=None, config=None):
        """
        Return a list of no charge instances owned by the authenticated user.

        :param marker:
            The optional parameter marker specified in the original request to specify
            where in the results to begin listing.
            Together with the marker, specifies the list result which listing should begin.
            If the marker is not specified, the list result will listing from the first one.
        :type marker: string

        :param max_keys:
            The optional parameter to specifies the max number of list result to return.
            The default value is 1000.
        :type max_keys: int

        :param internal_ip:
            The identified internal ip of instance.
        :type internal_ip: string

        :param keypair_id:
            get instance list filtered by keypair
        :type keypair_id: string

        :param zone_name:
            get instance list filtered by name of available zone
        :type zone_name: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/noCharge'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        if marker is not None:
            params['marker'] = marker
        if max_keys is not None:
            params['maxKeys'] = max_keys
        if internal_ip is not None:
            params['internalIp'] = internal_ip
        if keypair_id is not None:
            params['keypairId'] = keypair_id
        if zone_name is not None:
            params['zoneName'] = zone_name
        return self._send_request(http_methods.GET, path, params=params, config=config)

    def cancel_bid_order(self, order_id, client_token=None, config=None):
        """
        Cancel a bid order

        :param order_id:
            Identify of the order to cancel
        :type order_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/cancelBidOrder'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            "orderId": order_id
        }
        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params, config=config)

    def batch_create_auto_renew_rules(self, instance_id, renew_time_unit="month", renew_time=1,
                                      renew_cds=None, renew_eip=None, client_token=None, config=None):
        """
        create auto renew rules for instance

        :param instance_id:
            Identify of the instance to auto renew
        :type instance_id: string

        :param renew_time_unit:
            Time unit for renew, values: 'month'/'year', default value: month
        :type renew_time_unit: string

        :param renew_time:
            renew time of year, values: 1/2/3, default value: 1
        :type renew_time: int
        :param renew_cds:
            renew cds, values: True/False, default value: True
        :param renew_eip:
            renew eip, values: True/False, default value: True

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/batchCreateAutoRenewRules'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            "instanceId": instance_id,
            "renewTimeUnit": renew_time_unit,
            "renewTime": renew_time
        }
        if renew_cds is not None:
            body["renewCds"] = renew_cds
        if renew_eip is not None:
            body["renewEip"] = renew_eip

        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params, config=config)

    def batch_delete_auto_renew_rules(self, instance_id, renew_cds=None, renew_eip=None,
                                      client_token=None, config=None):
        """
        delete auto renew rules for instance

        :param instance_id:
            Identify of the instance to auto renew
        :type instance_id: string
        :param renew_cds:
            renew cds, values: True/False, default value: True
        :param renew_eip:
            renew eip, values: True/False, default value: True
        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/batchDeleteAutoRenewRules'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            "instanceId": instance_id
        }

        if renew_cds is not None:
            body["renewCds"] = renew_cds
        if renew_eip is not None:
            body["renewEip"] = renew_eip

        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params, config=config)

    def delete_recycled_instance(self, instance_id, client_token=None, config=None):
        """
        delete auto renew rules for instance

        :param instance_id:
            Identify of the instance to delete
        :type instance_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        instance_id = instance_id.encode(encoding='utf-8')
        path = b'/recycle/instance/%s' % instance_id
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {}
        return self._send_request(http_methods.DELETE, path, body=json.dumps(body), params=params, config=config)

    def list_instance_by_instance_ids(self, instance_ids, marker=None, max_keys=None, client_token=None, config=None):
        """
        list instances by id list

        :param instance_ids:
            Identify of the instances to return info
        :type instance_ids: list of string

        :param marker:
            The optional parameter marker specified in the original request to specify
            where in the results to begin listing.
            Together with the marker, specifies the list result which listing should begin.
            If the marker is not specified, the list result will listing from the first one.
        :type marker: string

        :param max_keys:
            The optional parameter to specifies the max number of list result to return.
            The default value is 1000.
        :type max_keys: int
        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/listByInstanceId'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        if marker is not None:
            params['marker'] = marker
        if max_keys is not None:
            params['maxKeys'] = max_keys
        body = {
            "instanceIds": instance_ids
        }
        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params, config=config)

    def get_instance_delete_progress(self, instance_ids, client_token=None, config=None):
        """
        get instances delete progress

        :param instance_ids:
            Identify of the instances to return info
        :type instance_ids: list of string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/deleteProgress'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            "instanceIds": instance_ids
        }
        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params, config=config)

    def batch_delete_instance_with_related_resource(self, instance_ids, related_release_flag=None,
                                                    delete_cds_snapshot_flag=None, delete_related_enis_flag=None,
                                                    bcc_recycle_flag=None, client_token=None, config=None):
        """
        batch delete instance with related resource

        :param instance_ids:
            Identify of the instances to return info
        :type instance_ids: list of string

        :param related_release_flag:
            Release or not related resources.
        :type related_release_flag: bool

        :param delete_cds_snapshot_flag:
            Delete or not cds snapshot.
        :type delete_cds_snapshot_flag: bool

        :param delete_related_enis_flag:
            Delete or not related enis.
        :type delete_related_enis_flag: bool

        :param bcc_recycle_flag:
            Recycle or not bcc instance.
        :type bcc_recycle_flag: bool


        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/batchDelete'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            "instanceIds": instance_ids
        }
        if related_release_flag is not None:
            body['relatedReleaseFlag'] = related_release_flag
        if delete_cds_snapshot_flag is not None:
            body['deleteCdsSnapshotFlag'] = delete_cds_snapshot_flag
        if delete_related_enis_flag is not None:
            body['deleteRelatedEnisFlag'] = delete_related_enis_flag
        if bcc_recycle_flag is not None:
            body['bccRecycleFlag'] = bcc_recycle_flag
        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params, config=config)

    def batch_start_instance(self, instance_ids, client_token=None, config=None):
        """
        batch start instance

        :param instance_ids:
            Identify of the instances to return info
        :type instance_ids: list of string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/batchAction'
        params = {
            'start': None
        }
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            "instanceIds": instance_ids
        }
        return self._send_request(http_methods.PUT, path, body=json.dumps(body), params=params, config=config)

    def batch_stop_instance(self, instance_ids, force_stop=None, stop_with_no_charge=None,
                            client_token=None, config=None):
        """
        batch stop instance

        :param instance_ids:
            Identify of the instances to return info
        :type instance_ids: list of string

        :param force_stop:
            force stop instance
        :type force_stop: bool

        :param stop_with_no_charge:
            stop instance and stop billing
        :type stop_with_no_charge: bool

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/batchAction'
        params = {
            'stop': None
        }
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            "instanceIds": instance_ids
        }
        if force_stop is not None:
            body['forceStop'] = force_stop
        if stop_with_no_charge is not None:
            body['stopWithNoCharge'] = stop_with_no_charge
        return self._send_request(http_methods.PUT, path, body=json.dumps(body), params=params, config=config)

    def list_id_mappings(self, ids, id_type, object_type, client_token=None, config=None):
        """
        get short-long id mapping by short/long id list

        :param ids:
            short id list
        :type ids: list of string

        :param id_type:
            id type
        :type id_type: string. value: short|long

        :param object_type:
            object type
        :type object_type: value: bcc

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/id/mapping'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            "instanceIds": ids,
            "idType": id_type,
            "objectType": object_type
        }
        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params, config=config)

    def batch_resize_instance(self, instance_ids, spec, subnet_id=None, logical_zone=None, internal_ip_v4=None,
                              enable_jumbo_frame=None, client_token=None, config=None):
        """
        batch resize instance

        :param instance_ids:
            Identify of the instances to return info
        :type instance_ids: list of string

        :param spec:
            spec
        :type spec: string

        :param subnet_id:
            subnet id
        :type subnet_id: string

        :param logical_zone:
            logical zone name
        :type logical_zone: string

        :param internal_ip_v4:
            internal ip for ipv4
        :type internal_ip_v4: string

        :param enable_jumbo_frame:
            The parameter of specified the instance enable/disable jumbo frame.
            True means enable jumbo frame, false means disable jumbo frame.
            enable_jumbo_frame default None which means:
            When you change to the spec which doesn't support jumbo frame, the jumbo frame will be disabled.
            When the original instance don't support jumbo frame and you change to the spec which support jumbo frame,
            the jumbo frame will be disabled.
            When the original spec of the instance support jumbo frame , then you change to the spec which support jumbo
            frame, if the original instance enable jumbo frame, the jumbo frame will be enabled, if the original instance
            disable jumbo frame, the jumbo frame will be disabled.
        :type enable_jumbo_frame: bool

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instanceBatchBySpec'
        params = {
            'resize': None
        }
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            "instanceIdList": instance_ids,
            "spec": spec
        }
        if subnet_id is not None:
            body['subnetId'] = subnet_id
        if logical_zone is not None:
            body['logicalZone'] = logical_zone
        if internal_ip_v4 is not None:
            body['internalIpV4'] = internal_ip_v4
        if enable_jumbo_frame is not None:
            body['enableJumboFrame'] = enable_jumbo_frame

        return self._send_request(http_methods.PUT, path, body=json.dumps(body), params=params, config=config)

    def list_available_resize_specs(self, instance_ids, spec=None, spec_id=None, logical_zone=None,
                                    client_token=None, config=None):
        """
        list available specs of resize instance in specified zone

        :param instance_ids:
            Identify of the instances to return info
        :type instance_ids: list of string

        :param spec:
            spec
        :type spec: string

        :param spec_id:
            spec id
        :type spec_id: string

        :param logical_zone:
            logical zone name
        :type logical_zone: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance'
        params = {
            'resizeList': None
        }
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            "instanceIdList": instance_ids,
            "spec": spec
        }
        if spec_id is not None:
            body['specId'] = spec_id
        if logical_zone is not None:
            body['zone'] = logical_zone
        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params, config=config)

    def batch_change_instance_to_prepay(self, change_pay_timing_req_list, client_token=None, config=None):
        """
        batch change instance to prepay

        :param change_pay_timing_req_list:
            batch change req list
        :type change_pay_timing_req_list: list of PayTimingChangeReqModel

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/batch/charging'
        params = {
            'toPrepay': None
        }
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            "config": [change_pay_timing_req.__dict__ for change_pay_timing_req in change_pay_timing_req_list]
        }
        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params, config=config)

    def batch_change_instance_to_postpay(self, change_pay_timing_req_list, client_token=None, config=None):
        """
        batch change instance to postpay

        :param change_pay_timing_req_list:
            batch change req list
        :type change_pay_timing_req_list: list of PayTimingChangeReqModel

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/batch/charging'
        params = {
            'toPostpay': None
        }
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            "config": [change_pay_timing_req.__dict__ for change_pay_timing_req in change_pay_timing_req_list]
        }
        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params, config=config)

    def list_instance_roles(self, client_token=None, config=None):
        """
        list instance role

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/role/list'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        return self._send_request(http_methods.GET, path, params=params, config=config)

    def bind_instance_role(self, instance_ids, role_name, client_token=None, config=None):
        """
        bind_instance_role

        :param instance_ids:
            instance id list
        :type instance_ids: list of string

        :param role_name:
            name of role
        :type role_name: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/role'
        params = {
            'bind': None
        }
        instances = []
        for instance_id in instance_ids:
            instances.append({'instanceId': instance_id})
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            "instances": instances,
            "roleName": role_name
        }
        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params, config=config)

    def unbind_instance_role(self, instance_ids, role_name, client_token=None, config=None):
        """
        unbind_instance_role

        :param instance_ids:
            instance id list
        :type instance_ids: list of string

        :param role_name:
            name of role
        :type role_name: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/role'
        params = {
            'unbind': None
        }
        instances = []
        for instance_id in instance_ids:
            instances.append({'instanceId': instance_id})
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            "instances": instances,
            "roleName": role_name
        }
        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params, config=config)

    def add_ipv6(self, instance_id, ipv6_address, reboot=False, client_token=None, config=None):
        """
        add_ipv6

        :param instance_id:
            instance id
        :type instance_id: list of string

        :param ipv6_address:
            ipv6 address to bind instance
        :type ipv6_address: list of string

        :param reboot:
            reboot the instance
        :type reboot: list of string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/addIpv6'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            "instanceId": instance_id,
            "ipv6Address": ipv6_address,
            "reboot": reboot
        }
        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params, config=config)

    def delete_ipv6(self, instance_id, reboot=False, client_token=None, config=None):
        """
        delete_ipv6

        :param instance_id:
            instance id
        :type instance_id: list of string

        :param reboot:
            reboot the instance
        :type reboot: list of string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/delIpv6'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            "instanceId": instance_id,
            "reboot": reboot
        }
        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params, config=config)

    def bind_image_to_tags(self, image_id, tags, client_token=None, config=None):
        """
        bind_image_to_tags

        :param image_id:
            image id
        :type image_id: list of string

        :param tags
            The optional list of tag to be bonded.
        :type tags: list<bcc_model.TagModel>

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        image_id = image_id.encode(encoding='utf-8')
        path = b'/image/%s/tag' % image_id
        params = {
            'bind': None
        }
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        tag_list = [tag.__dict__ for tag in tags]
        body = {
            'changeTags': tag_list
        }
        return self._send_request(http_methods.PUT, path, body=json.dumps(body), params=params, config=config)

    def unbind_image_to_tags(self, image_id, tags, client_token=None, config=None):
        """
        unbind_image_to_tags

        :param image_id:
            image id
        :type image_id: list of string

        :param tags
            The optional list of tag to be bonded.
        :type tags: list<bcc_model.TagModel>

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        image_id = image_id.encode(encoding='utf-8')
        path = b'/image/%s/tag' % image_id
        params = {
            'unbind': None
        }
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        tag_list = [tag.__dict__ for tag in tags]
        body = {
            'changeTags': tag_list
        }
        return self._send_request(http_methods.PUT, path, body=json.dumps(body), params=params, config=config)

    def import_custom_image(self, os_name, os_arch, os_type, os_version, name, bos_url, client_token=None, config=None,
                            detection=None, generation_type=None):
        """
        import_custom_image

        :param os_name:
            name of os
        :type os_name: string

        :param os_arch:
        	archicture of os
        :type os_arch: string

        :param os_type:
            type of os
        :type os_type: string

        :param os_version:
            version of os
        :type os_version: string

        :param name:
            name of os
        :type name: string

        :param bos_url:
            boot script of os
        :type bos_url: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/image/import'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            'osName': os_name,
            'osArch': os_arch,
            'osType': os_type,
            'osVersion': os_version,
            'name': name,
            'bosUrl': bos_url
        }
        if detection:
            body['detection'] = detection
        if generation_type is not None:
            body['generationType'] = generation_type
        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params, config=config)

    def create_remote_copy_snapshot(self, snapshot_id, dest_region_infos, client_token=None, config=None):
        """
        create_remote_copy_snapshot

        :param snapshot_id:
            identify of snapshot
        :type snapshot_id: string

        :param dest_region_infos:
            information of destination region
        :type dest_region_infos: list of bcc_model.DestRegionInfoModel

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        snapshot_id = snapshot_id.encode(encoding='utf-8')
        path = b'/snapshot/remote_copy/%s' % snapshot_id
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            "destRegionInfos": [dest_region_info.__dict__ for dest_region_info in dest_region_infos]
        }
        return self._send_request(http_methods.PUT, path, body=json.dumps(body), params=params, config=config)

    def create_deploy_set(self, name=None, strategy=None, desc=None, concurrency=None, client_token=None, config=None):
        """
        create_deploy_set

        :param name:
            name of deploy set
        :type name: string

        :param strategy:
            deploy strategy HOST_HA | RACK_HA | TOR_HA
        :type strategy: string

        :param desc:
            description of deploy set
        :type desc: string

        :param concurrency:
            mark how many instances can created in one location
            location means host for HOST_HA, rack for RACK_HA, tor for TOR_HA
        :type concurrency: int

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/deployset/create'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {}
        if name is not None:
            body['name'] = name
        if strategy is not None:
            body['strategy'] = strategy
        if desc is not None:
            body['desc'] = desc
        if concurrency is not None:
            body['concurrency'] = concurrency

        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params, config=config)

    def list_deploy_sets(self, client_token=None, config=None, deployment_set_ids=None):
        """
        list_deploy_sets

        :param deployment_set_ids:
        :type deployment_set_ids: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/deployset/list'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        if deployment_set_ids is not None:
            params['deploymentSetIds'] = deployment_set_ids
        return self._send_request(http_methods.GET, path, params=params, config=config)

    def delete_deploy_set(self, deploy_set_id, client_token=None, config=None):
        """
        delete_deploy_set

        :param deploy_set_id:
            identify of deployset
        :type deploy_set_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        deploy_set_id = deploy_set_id.encode(encoding='utf-8')
        path = b'/instance/deployset/%s' % deploy_set_id
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        return self._send_request(http_methods.DELETE, path, params=params, config=config)

    def modify_deploy_set(self, deploy_set_id, name=None, desc=None, client_token=None, config=None):
        """
        modify_deploy_set

        :param deploy_set_id:
            identify of deployset
        :type deploy_set_id: string

        :param name:
            name of deploy set
        :type name: string

        :param desc:
            description of deploy set
        :type desc: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        deploy_set_id = deploy_set_id.encode(encoding='utf-8')
        path = b'/instance/deployset/%s' % deploy_set_id
        params = {
            'modifyAttribute': None
        }
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {}
        if name is not None:
            body['name'] = name
        if desc is not None:
            body['desc'] = desc
        return self._send_request(http_methods.PUT, path, body=json.dumps(body), params=params, config=config)

    def get_deploy_set(self, deploy_set_id, client_token=None, config=None):
        """
        get_deploy_set

        :param deploy_set_id:
            identify of deployset
        :type deploy_set_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        deploy_set_id = deploy_set_id.encode(encoding='utf-8')
        path = b'/deployset/%s' % deploy_set_id
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        return self._send_request(http_methods.GET, path, params=params, config=config)

    def update_instance_deploy(self, instance_id, deployset_id_list, force=None,
                               client_token=None, config=None):
        """
        update instance deploy relation

        :param instance_id:
            identify of instance
        :type instance_id: string

        :param deployset_id_list:
            identify list of deployset
        :type deployset_id_list: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/deployset/updateRelation'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            'instanceId': instance_id,
            'deploysetIdList': deployset_id_list
        }
        if force is not None:
            body['force'] = force
        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params, config=config)

    def del_instance_deploy(self, instance_id_list, deploy_set_id, client_token=None, config=None):
        """
        delete instance deploy relation

        :param instance_id_list:
            identify list of instance
        :type instance_id_list: string

        :param deploy_set_id:
            identify of deployset
        :type deploy_set_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/deployset/delRelation'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            'instanceIdList': instance_id_list,
            'deployId': deploy_set_id
        }
        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params, config=config)

    def create_ehc_cluster(self, name, zone_name, description=None, client_token=None, config=None):
        """
        create ehc cluster

        :param name:
            The name of the EHC cluster. This parameter is required.
        :type name: string

        :param zone_name:
            The availability zone name where the EHC cluster will be created.
        :type zone_name: string

        :param description:
            Optional. A brief description of the EHC cluster. Default is an empty string.
        :type description: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/ehc/cluster/create'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            'name': name,
            'zoneName': zone_name
        }
        if description is not None:
            body['description'] = description
        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params, config=config)

    def modify_ehc_cluster(self, ehc_cluster_id, name=None, description=None, client_token=None, config=None):
        """
        Modifies the name and description of an EHC cluster.

        :param ehc_cluster_id:
            The ID of the EHC cluster to be modified. This parameter is required.
        :type ehc_cluster_id: string

        :param name:
            Optional. The new name for the EHC cluster. If not specified, the name will not be changed.
        :type name: string

        :param description:
            Optional. The new description for the EHC cluster. If not specified, the description will not be changed.
        :type description: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/ehc/cluster/modify'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            'ehcClusterId': ehc_cluster_id
        }
        if name is not None:
            body['name'] = name
        if description is not None:
            body['description'] = description

        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params, config=config)

    def get_ehc_cluster_list(self, ehc_cluster_id_list=None, name_list=None, zone_name=None, config=None):
        """
        get ehc cluster list

        :param ehc_cluster_id_list:
            Optional. List of EHC cluster IDs to filter the results. If not specified, retrieves all clusters.
        :type ehc_cluster_id_list: list<string>

        :param name_list:
            Optional. List of EHC cluster names to filter the results. If not specified, retrieves all clusters.
        :type name_list: list<string>

        :param zone_name:
            Optional. The name of the availability zone to filter the results.
        :type zone_name: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/ehc/cluster/list'
        params = {}
        body = {}
        if ehc_cluster_id_list is not None:
            body['ehcClusterIdList'] = ehc_cluster_id_list
        if name_list is not None:
            body['nameList'] = name_list
        if zone_name is not None:
            body['zoneName'] = zone_name

        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params, config=config)

    def delete_ehc_cluster(self, ehc_cluster_id_list, client_token=None, config=None):
        """
        Modifies the name and description of an EHC cluster.

        :param ehc_cluster_id_list:
            A list of IDs of the EHC clusters to be deleted. This parameter is required.
        :type ehc_cluster_id_list: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/ehc/cluster/delete'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            'ehcClusterIdList': ehc_cluster_id_list
        }

        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params, config=config)

    def get_available_images_by_spec(self, marker=None, max_keys=None, spec=None, os_name=None, config=None):
        """
        :param marker:
            The optional parameter marker specified in the original request to specify
            where in the results to begin listing.
            Together with the marker, specifies the list result which listing should begin.
            If the marker is not specified, the list result will listing from the first one.
        :type marker: string

        :param max_keys:
            The optional parameter to specifies the max number of list result to return.
            The default value is 100.
        :type max_keys: int

        :param os_name:
            The optional parameter to query specified public image by os name.
        :type os_name: string

        :param spec:
            The required parameter to query specified public image by spec.
        :type spec: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/image/getAvailableImageBySpec'
        params = {}
        if marker is not None:
            params['marker'] = marker
        if max_keys is not None:
            params['maxKeys'] = max_keys
        if spec is not None:
            params['spec'] = spec
        if os_name is not None:
            params['osName'] = os_name

        return self._send_request(http_methods.GET, path, params=params, config=config)

    def create_reserved_instances(self, reserved_instance_name=None, scope=None, zone_name=None, spec=None,
                                  offering_type=None, instance_count=None, reserved_instance_count=None,
                                  reserved_instance_time=None, reserved_instance_time_unit=None,
                                  auto_renew_time_unit=None, auto_renew_time=None, auto_renew=None,
                                  effective_time=None, ehc_cluster_id=None, ticket_id=None,
                                  tags=None, client_token=None, config=None):

        """
        Create reserved instances.

        :param reserved_instance_name:
            The name of the reserved instance.
        :type reserved_instance_name: string

        :param scope:
            The scope.
        :type scope: string

        :param zone_name:
            The name of the availability zone.
        :type zone_name: string

        :param spec:
            The instance specification.
        :type spec: string

        :param offering_type:
            The offering type.
        :type offering_type: string

        :param instance_count:
            The number of instances.
        :type instance_count: int

        :param reserved_instance_count:
            The number of reserved instances.
        :type reserved_instance_count: int

        :param reserved_instance_time:
            The duration of the reserved instance.
        :type reserved_instance_time: int

        :param reserved_instance_time_unit:
            The time unit of the reserved instance.
        :type reserved_instance_time_unit: string

        :param auto_renew_time_unit:
            The time unit for automatic renewal.
        :type auto_renew_time_unit: string

        :param auto_renew_time:
            The duration for automatic renewal.
        :type auto_renew_time: int

        :param auto_renew:
            Whether to enable automatic renewal, defaults to False.
        :type auto_renew: bool

        :param effective_time:
            The effective time.
            It is immediately effective by default.
        :type effective_time: string

        :param ehc_cluster_id:
            The EHC cluster ID.
        :type ehc_cluster_id: string

        :param ticket_id:
            The ticket ID.
        :type ticket_id: string

        :param tags:
            The optional list of tag to be bonded.
        :type tags: list<bcc_model.TagModel>

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """

        path = b'/instance/reserved/create'  # 请替换为实际的请求路径
        params = {}
        if client_token is not None:
            params['clientToken'] = client_token

        body = {}

        if reserved_instance_name is not None:
            body['reservedInstanceName'] = reserved_instance_name
        if scope is not None:
            body['scope'] = scope
        if zone_name is not None:
            body['zoneName'] = zone_name
        if spec is not None:
            body['spec'] = spec
        if offering_type is not None:
            body['offeringType'] = offering_type
        if instance_count is not None:
            body['instanceCount'] = instance_count
        if reserved_instance_count is not None:
            body['reservedInstanceCount'] = reserved_instance_count
        if reserved_instance_time is not None:
            body['reservedInstanceTime'] = reserved_instance_time
        if reserved_instance_time_unit is not None:
            body['reservedInstanceTimeUnit'] = reserved_instance_time_unit
        if auto_renew_time_unit is not None:
            body['autoRenewTimeUnit'] = auto_renew_time_unit
        if auto_renew_time is not None:
            body['autoRenewTime'] = auto_renew_time
        if auto_renew is not False:
            body['autoRenew'] = str(auto_renew).lower()
        if effective_time is not None:
            body['effectiveTime'] = effective_time
        if ehc_cluster_id is not None:
            body['ehcClusterId'] = ehc_cluster_id
        if ticket_id is not None:
            body['ticketId'] = ticket_id
        if tags is not None:
            tag_list = [tag.__dict__ for tag in tags]
            body['tags'] = tag_list

        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params, config=config)

    def modify_reserved_instances(self, reserved_instances=None, client_token=None, config=None):

        """
        Modify the information of reserved instances.

        :param reserved_instances:
            A list of dictionaries containing the information of reserved instances to be updated.
        :type reserved_instances: list<bcc_model.ModifyReservedInstanceModel>

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/instance/reserved/modify'
        params = {}
        if client_token is not None:
            params['clientToken'] = client_token

        body = {}

        if reserved_instances is not None:
            reserved_instances_list = [reserved_instance.__dict__ for reserved_instance in reserved_instances]
            body['reservedInstances'] = reserved_instances_list

        return self._send_request(http_methods.PUT, path, body=json.dumps(body), params=params, config=config)

    def get_instance_user_data(self, instance_id, client_token=None, config=None):
        """
        get_instance_user_data
        """
        path = b'/instance/attribute/getUserdata'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            "instanceId": instance_id
        }
        return self._send_request(http_methods.POST, path, json.dumps(body),
                                  params=params, config=config)

    def enter_rescue_mode(self, instance_id, force_stop, password, client_token=None, config=None):
        """
                进入救援模式。

                :param enter_rescue_mode_req:
                :desc
                :type enter_rescue_mode_req: json

                :return:
                :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/rescue/mode/enter'

        params = {}

        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token

        body = {
            'instanceId': instance_id,
            'forceStop': force_stop,
            'password': password
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    def exit_rescue_mode(self, instance_id, client_token=None, config=None):
        """
                退出救援模式。

                :param exit_rescue_mode_req:
                :desc
                :type exit_rescue_mode_req: json

                :return:
                :rtype baidubce.bce_response.BceResponse
        """
        path = b'/instance/rescue/mode/exit'

        params = {}

        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token

        body = {
            'instanceId': instance_id
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)


    def bind_sg(self, instance_ids, security_group_ids, security_group_type, client_token=None, config=None):
        """
                绑定安全组。

                :param bind_sg:
                :desc
                :type bind_sg: json
                :return:
                :rtype baidubce.bce_response.BceResponse
        """
        path = b'/securitygroup/bind'

        params = {}

        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token

        body = {
            'instanceIds': instance_ids,
            'securityGroupIds': security_group_ids,
            'securityGroupType': security_group_type
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)


    def replace_sg(self, instance_ids, security_group_ids, security_group_type, client_token=None, config=None):
        """
                替换安全组。

                :param replace_sg:
                :desc
                :type replace_sg: json

                :return:
                :rtype baidubce.bce_response.BceResponse
        """
        path = b'/securitygroup/replace'

        params = {}

        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token

        body = {
            'instanceIds': instance_ids,
            'securityGroupIds': security_group_ids,
            'securityGroupType': security_group_type
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    def unbind_sg(self, instance_ids, security_group_ids, security_group_type, client_token=None, config=None):
        """
                解绑安全组。

                :param unbind_sg:
                :desc
                :type unbind_sg: json

                :return:
                :rtype baidubce.bce_response.BceResponse
        """
        path = b'/securitygroup/unbind'

        params = {}

        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token

        body = {
            'instanceIds': instance_ids,
            'securityGroupIds': security_group_ids,
            'securityGroupType': security_group_type
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)


def generate_client_token_by_uuid():
    """
    The default method to generate the random string for client_token
    if the optional parameter client_token is not specified by the user.
    :return:
    :rtype string
    """
    return str(uuid.uuid4())


def generate_client_token_by_random():
    """
    The alternative method to generate the random string for client_token
    if the optional parameter client_token is not specified by the user.
    :return:
    :rtype string
    """
    client_token = ''.join(random.sample(string.ascii_letters + string.digits, 36))
    return client_token


def get_cds_price(self, purchase_length, payment_timing, storage_type, cds_size_in_gb, purchase_count, zone_name,
                  encrypt_key=None, client_token=None, config=None):
    """
    get_deploy_set
    """
    path = b'/volume/getPrice'
    params = {}
    if client_token is None:
        params['clientToken'] = generate_client_token()
    else:
        params['clientToken'] = client_token
    body = {
        'purchaseLength': purchase_length,
        'paymentTiming': payment_timing,
        'storageType': storage_type,
        'cdsSizeInGB': cds_size_in_gb,
        'purchaseCount': purchase_count,
        'zoneName': zone_name
    }
    if encrypt_key is not None:
        body['encryptKey'] = encrypt_key
    return self._send_request(http_methods.POST, path, json.dumps(body),
                              params=params, config=config)


generate_client_token = generate_client_token_by_uuid
