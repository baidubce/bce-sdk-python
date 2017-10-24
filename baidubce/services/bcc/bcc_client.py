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

_logger = logging.getLogger(__name__)


default_billing_to_purchase_created = bcc_model.Billing('Postpaid')
default_billing_to_purchase_reserved = bcc_model.Billing()


class BccClient(bce_base_client.BceBaseClient):
    """
    Bcc base sdk client
    """

    prefix = '/v2'

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
                      config=None, body_parser=None):
        config = self._merge_config(config)
        if body_parser is None:
            body_parser = handler.parse_json

        return bce_http_client.send_request(
            config, bce_v1_signer.sign, [handler.parse_error, body_parser],
            http_method, BccClient.prefix + path, body, headers, params)

    @required(cpu_count=int,
              memory_capacity_in_gb=int,
              image_id=(str, unicode))
    def create_instance(self, cpu_count, memory_capacity_in_gb, image_id, instance_type=None,
                        billing=None, local_disk_size_in_gb=0, create_cds_list=None,
                        network_capacity_in_mbps=0, purchase_count=1, name=None, admin_pass=None,
                        zone_name=None, subnet_id=None, security_group_id=None,
                        client_token=None, config=None):
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

        :param local_disk_size_in_gb: 
            The optional parameter to specify the temporary disk size in GB.
            The temporary disk excludes the system disk, available is 0-500GB.
        :type local_disk_size_in_gb: int

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

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = '/instance'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        if billing is None:
            billing = default_billing_to_purchase_created
        body = {
            'cpuCount': cpu_count,
            'memoryCapacityInGB': memory_capacity_in_gb,
            'imageId': image_id,
            'billing': billing.__dict__
        }
        if instance_type is not None:
            body['instanceType'] = instance_type
        if local_disk_size_in_gb != 0:
            body['localDiskSizeInGB'] = local_disk_size_in_gb
        if create_cds_list is not None:
            body['createCdsList'] = create_cds_list
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
            body['securityGroupId'] = subnet_id
        return self._send_request(http_methods.POST, path, json.dumps(body),
                                  params=params, config=config)

    @required(cpu_count=int, memory_capacity_in_gb=int, dedicated_host_id=(str, unicode),
              image_id=(str, unicode))
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
        path = '/instance'
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
            body['securityGroupId'] = subnet_id
        return self._send_request(http_methods.POST, path, json.dumps(body), params=params,
                                  config=config)

    def list_instances(self, marker=None, max_keys=None, internal_ip=None, dedicated_host_id=None,
                       zone_name=None, config=None):
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

        :return:
        :rtype baidubce.bce_response.BceResponse 
        """
        path = '/instance'
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
        
        return self._send_request(http_methods.GET, path, params=params, config=config)

    @required(instance_id=(str, unicode))
    def get_instance(self, instance_id, config=None):
        """
        Get the detail information of specified instance.

        :param instance_id: 
            The id of instance.
        :type instance_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse 
        """
        path = '/instance/%s' % instance_id
        return self._send_request(http_methods.GET, path, config=config)

    @required(instance_id=(str, unicode))
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
        path = '/instance/%s' % instance_id
        params = {
            'start': None
        }
        return self._send_request(http_methods.PUT, path, params=params, config=config)

    @required(instance_id=(str, unicode))
    def stop_instance(self, instance_id, force_stop=False, config=None):
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
        path = '/instance/%s' % instance_id
        body = {
            'forceStop': force_stop
        }
        params = {
            'stop': None
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body), 
                                  params=params, config=config)

    @required(instance_id=(str, unicode))
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
        path = '/instance/%s' % instance_id
        body = {
            'forceStop': force_stop
        }
        params = {
            'reboot': None
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body), 
                                  params=params, config=config)

    @required(instance_id=(str, unicode),
              admin_pass=(str, unicode))
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
        secret_access_key = self.config.credentials.secret_access_key
        cipher_admin_pass = aes128_encrypt_16char_key(admin_pass, secret_access_key)
        path = '/instance/%s' % instance_id
        body = {
            'adminPass': cipher_admin_pass
        }
        params = {
            'changePass': None
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body), 
                                  params=params, config=config)

    @required(instance_id=(str, unicode),
              name=(str, unicode))
    def modify_instance_attributes(self, instance_id, name, config=None):
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

        :return:
        :rtype baidubce.bce_response.BceResponse 
        """
        path = '/instance/%s' % instance_id
        body = {
            'name': name
        }
        params = {
            'modifyAttribute': None
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body), 
                                  params=params, config=config)

    @required(instance_id=(str, unicode),
              image_id=(str, unicode),
              admin_pass=(str, unicode))
    def rebuild_instance(self, instance_id, image_id, admin_pass, config=None):
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

        :return:
        :rtype baidubce.bce_response.BceResponse 
        """
        secret_access_key = self.config.credentials.secret_access_key
        cipher_admin_pass = aes128_encrypt_16char_key(admin_pass, secret_access_key)
        path = '/instance/%s' % instance_id
        body = {
            'imageId': image_id,
            'adminPass': cipher_admin_pass
        }
        params = {
            'rebuild': None
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body), 
                                  params=params, config=config)

    @required(instance_id=(str, unicode))
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
        path = '/instance/%s' % instance_id
        return self._send_request(http_methods.DELETE, path, config=config)

    @required(instance_id=(str, unicode),
              cpu_count=int,
              memory_capacity_in_gb=int)
    def resize_instance(self, instance_id, cpu_count, memory_capacity_in_gb,
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
        path = '/instance/%s' % instance_id
        body = {
            'cpuCount': cpu_count,
            'memoryCapacityInGB': memory_capacity_in_gb
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
        return self._send_request(http_methods.PUT, path, json.dumps(body), 
                                  params=params, config=config)

    @required(instance_id=(str, unicode),
              security_group_id=(str, unicode))
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
        path = '/instance/%s' % instance_id
        body = {
            'securityGroupId': security_group_id
        }
        params = {
            'bind': None
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body), 
                                  params=params, config=config)

    @required(instance_id=(str, unicode),
              security_group_id=(str, unicode))
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
        path = '/instance/%s' % instance_id
        body = {
            'securityGroupId': security_group_id
        }
        params = {
            'unbind': None
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body), 
                                  params=params, config=config)

    @required(instance_id=(str, unicode))
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
        path = '/instance/%s/vnc' % instance_id
        return self._send_request(http_methods.GET, path, config=config)

    @required(instance_id=(str, unicode))
    def purchase_reserved_instance(self, 
                                   instance_id, 
                                   billing=None, 
                                   client_token=None, 
                                   config=None):
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
        path = '/instance/%s' % instance_id
        if billing is None:
            billing = default_billing_to_purchase_reserved
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
        path = '/instance/spec'
        return self._send_request(http_methods.GET, path, config=config)

    @required(cds_size_in_gb=int)
    def create_volume_with_cds_size(self, cds_size_in_gb, billing=None, purchase_count=1,
                                    storage_type='hp1', zone_name=None, client_token=None,
                                    config=None):
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
            Billing information.
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

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = '/volume'
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

        return self._send_request(http_methods.POST, path, json.dumps(body), 
                                  params=params, config=config)

    @required(snapshot_id=(str, unicode))
    def create_volume_with_snapshot_id(self, snapshot_id, billing=None, purchase_count=1,
                                       storage_type='hp1', zone_name=None, client_token=None,
                                       config=None):
        """
        Create a volume with the specified options.
        You can use this method to create a new empty volume by specified options
        or you can create a new volume from customized volume snapshot but not system disk snapshot.
        By using the cdsSizeInGB parameter you can create a newly empty volume.
        By using snapshotId parameter to create a volume form specific snapshot.

        :param snapshot_id: 
            The id of snapshot.
            By specifying the snapshotId,
            it will create volume from the specified snapshot and the parameter cdsSizeInGB will be ignored.
        :type snapshot_id: string

        :param billing: 
            Billing information.
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

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = '/volume'
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

        return self._send_request(http_methods.POST, path, json.dumps(body), 
                                  params=params, config=config)

    def list_volumes(self, instance_id=None, zone_name=None, marker=None, max_keys=None,
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

        :return:
        :rtype baidubce.bce_response.BceResponse 
        """
        path = '/volume'
        params = {}
        if instance_id is not None:
            params['instanceId'] = instance_id
        if zone_name is not None:
            params['zoneName'] = zone_name
        if marker is not None:
            params['marker'] = marker
        if max_keys is not None:
            params['maxKeys'] = max_keys
        
        return self._send_request(http_methods.GET, path, params=params, config=config)

    @required(volume_id=(str, unicode))
    def get_volume(self, volume_id, config=None):
        """
        Get the detail information of specified volume.

        :param volume_id: 
            The id of the volume.
        :type volume_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse 
        """
        path = '/volume/%s' % volume_id
        return self._send_request(http_methods.GET, path, config=config)

    @required(volume_id=(str, unicode),
              instance_id=(str, unicode))
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
        path = '/volume/%s' % volume_id
        body = {
            'instanceId': instance_id
        }
        params = {
            'attach': None
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body), 
                                  params=params, config=config)

    @required(volume_id=(str, unicode),
              instance_id=(str, unicode))
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
        path = '/volume/%s' % volume_id
        body = {
            'instanceId': instance_id
        }
        params = {
            'detach': None
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body), 
                                  params=params, config=config)

    @required(volume_id=(str, unicode))
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
        path = '/volume/%s' % volume_id
        return self._send_request(http_methods.DELETE, path, config=config)

    @required(volume_id=(str, unicode),
              new_cds_size=int)
    def resize_volume(self, volume_id, new_cds_size, client_token=None, config=None):
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
        path = '/volume/%s' % volume_id
        body = {
            'newCdsSizeInGB': new_cds_size
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
        return self._send_request(http_methods.PUT, path, json.dumps(body), 
                                  params=params, config=config)

    @required(volume_id=(str, unicode),
              snapshot_id=(str, unicode))
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
        path = '/volume/%s' % volume_id
        body = {
            'snapshotId': snapshot_id
        }
        params = {
            'rollback': None,
        }
        return self._send_request(http_methods.PUT, path, json.dumps(body), 
                                  params=params, config=config)

    @required(volume_id=(str, unicode))
    def purchase_reserved_volume(self, 
                                 volume_id, 
                                 billing=None, 
                                 client_token=None, 
                                 config=None):
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
        path = '/volume/%s' % volume_id
        if billing is None:
            billing = default_billing_to_purchase_reserved
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

    @required(image_name=(str, unicode),
              instance_id=(str, unicode))
    def create_image_from_instance_id(self,
                                      image_name,
                                      instance_id,
                                      client_token=None,
                                      config=None):
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
        path = '/image'
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

        return self._send_request(http_methods.POST, path, json.dumps(body), 
                                  params=params, config=config)

    @required(image_name=(str, unicode),
              snapshot_id=(str, unicode))
    def create_image_from_snapshot_id(self,
                                      image_name,
                                      snapshot_id,
                                      client_token=None,
                                      config=None):
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
        path = '/image'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token
        body = {
            'imageName': image_name,
            'snapshotId': snapshot_id
        }

        return self._send_request(http_methods.POST, path, json.dumps(body), 
                                  params=params, config=config)

    def list_images(self, image_type='All', marker=None, max_keys=None, config=None):
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

        :return:
        :rtype baidubce.bce_response.BceResponse 
        """
        path = '/image'
        params = {
            'imageType': image_type
        }
        if marker is not None:
            params['marker'] = marker
        if max_keys is not None:
            params['maxKeys'] = max_keys
        
        return self._send_request(http_methods.GET, path, params=params, config=config)

    @required(image_id=(str, unicode))
    def get_image(self, image_id, config=None):
        """
        Get the detail information of specified image.

        :param image_id: 
            The id of image.
        :type image_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse 
        """
        path = '/image/%s' % image_id
        return self._send_request(http_methods.GET, path, config=config)

    @required(image_id=(str, unicode))
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
        path = '/image/%s' % image_id
        return self._send_request(http_methods.DELETE, path, config=config)

    @required(volume_id=(str, unicode),
              snapshot_name=(str, unicode))
    def create_snapshot(self,
                        volume_id,
                        snapshot_name,
                        desc=None,
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
        path = '/snapshot'
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
        path = '/snapshot'
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

    @required(snapshot_id=(str, unicode))
    def get_snapshot(self, snapshot_id, config=None):
        """
        Get the detail information of specified snapshot.

        :param snapshot_id: 
            The id of snapshot.
        :type snapshot_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse 
        """
        path = '/snapshot/%s' % snapshot_id
        return self._send_request(http_methods.GET, path, config=config)

    @required(snapshot_id=(str, unicode))
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
        path = '/snapshot/%s' % snapshot_id
        return self._send_request(http_methods.DELETE, path, config=config)

    @required(name=(str, unicode),
              rules=list)
    def create_security_group(self,
                              name,
                              rules,
                              vpc_id=None,
                              desc=None,
                              client_token=None,
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
        path = '/securityGroup'
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
        path = '/securityGroup'
        params = None
        if instance_id is not None or marker is not None or max_keys is not None:
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

    @required(security_group_id=(str, unicode))
    def delete_security_group(self, security_group_id, config=None):
        """
        Deleting the specified SecurityGroup.

        :param security_group_id: 
            The id of SecurityGroup that will be deleted.
        :type security_group_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse 
        """
        path = '/securityGroup/%s' % security_group_id
        return self._send_request(http_methods.DELETE, path, config=config)

    @required(security_group_id=(str, unicode),
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
        path = '/securityGroup/%s' % security_group_id
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

    @required(security_group_id=(str, unicode),
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
        path = '/securityGroup/%s' % security_group_id
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

    def list_zones(self, config=None):
        """
        Get zone detail list within current region
        :param config:
        :return:
        """
        path = '/zone'
        return self._send_request(http_methods.GET, path, config=config)


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


generate_client_token = generate_client_token_by_uuid


