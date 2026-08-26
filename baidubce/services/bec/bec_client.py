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
This module provides a client class for BEC.
"""

from __future__ import unicode_literals

import copy
import json
import logging
import uuid

from baidubce import bce_base_client
from baidubce import compat
from baidubce.auth import bce_v1_signer
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce.http import http_content_types
from baidubce.http import http_headers
from baidubce.http import http_methods
from baidubce.utils import required

_logger = logging.getLogger(__name__)


class BecClient(bce_base_client.BceBaseClient):
    """
    Bec sdk client
    """

    prefix = b'/v1'

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
        if headers is None:
            headers = {}
        if body is not None and http_headers.CONTENT_TYPE not in headers:
            headers[http_headers.CONTENT_TYPE] = http_content_types.JSON

        return bce_http_client.send_request(
            config, bce_v1_signer.sign, [handler.parse_error, body_parser],
            http_method, BecClient.prefix + path, body, headers, params)

    # ======================================================================
    #  VM Service (虚机服务) APIs  —  POST/GET/PUT/DELETE /v1/vm/service
    # ======================================================================

    def create_vm_service(self, deploy_instances, image_id=None,
                          image_type=None, system_volume=None, key_config=None,
                          vm_name=None, spec=None, cpu=None, memory=None,
                          need_public_ip=False, bandwidth=0,
                          data_volume_list=None, dns_config=None,
                          need_ipv6_public_ip=False, disable_intranet=False,
                          disable_cloud_init=False, security_group_ids=None,
                          hostname=None, reservation=None,
                          auto_renew=None, template_id=None,
                          deployset_id_list=None, user_data=None, tags=None,
                          service_name=None, service_id=None,
                          network_config_list=None,
                          gpu=None, payment_method=None, direct_pay=None,
                          hostname_gen_method=None, action_type=None,
                          back_url=None, cuda_version=None,
                          cudnn_version=None, driver_version=None,
                          client_token=None, config=None):
        """
        Create a BEC VM service.

        :param deploy_instances: Deployment region list.
        :type deploy_instances: list<bec_model.DeploymentInstance>

        :param image_id: Image ID. Not needed when template_id is used.
        :param image_type: Image type ("bec" or "bcc").
            Not needed when template_id is used.
        :param system_volume: System disk configuration.
            Not needed when template_id is used.
        :type system_volume: bec_model.SystemVolumeConfig

        :param key_config: Password or key pair configuration.
        :type key_config: bec_model.KeyConfig

        :param vm_name: VM instance name.
        :param spec: Instance spec (e.g. "bec.g5.c1m4"). If specified, cpu/memory not needed.
        :param cpu: CPU count. Required if spec is not provided.
        :param memory: Memory in GB. Required if spec is not provided.
        :param need_public_ip: Whether to enable public IP.
        :param bandwidth: Public bandwidth in Mbps.
        :param data_volume_list: Data disk list.
        :type data_volume_list: list<bec_model.VolumeConfig>

        :param dns_config: DNS configuration.
        :type dns_config: bec_model.DnsConfig

        :param reservation: Prepaid reservation config.
        :type reservation: bec_model.Reservation

        :param auto_renew: Auto-renew config.
        :type auto_renew: bec_model.AutoRenew

        :param template_id: VM template ID.
        :param deployset_id_list: Deploy set ID list.
        :param user_data: User data (base64 encoded).
        :param tags: Resource tags.
        :type tags: list<bec_model.Tag>

        :param service_name: Service name.
        :param service_id: Existing service ID to add instances to (optional).
        :param network_config_list: NIC naming/ordering configuration.
        :type network_config_list: list<bec_model.NetworkConfig>

        :param gpu: GPU configuration.
        :type gpu: bec_model.GpuRequest

        :param payment_method: Payment method ("postpay" or "prepay").
        :param direct_pay: Whether to pay directly for prepaid orders.
        :param hostname_gen_method: Hostname generation method.
        :param action_type: Action type.
        :param back_url: Callback URL.
        :param cuda_version: CUDA version (GPU images).
        :param cudnn_version: cuDNN version (GPU images).
        :param driver_version: GPU driver version.

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/vm/service'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token

        body = {
            'deployInstances': [d.__dict__ for d in deploy_instances]
        }

        if image_id is not None:
            body['imageId'] = image_id
        if image_type is not None:
            body['imageType'] = image_type
        if system_volume is not None:
            body['systemVolume'] = system_volume.__dict__
        if key_config is not None:
            body['keyConfig'] = key_config.__dict__
        if vm_name is not None:
            body['vmName'] = vm_name
        if spec is not None:
            body['spec'] = spec
        if cpu is not None:
            body['cpu'] = cpu
        if memory is not None:
            body['memory'] = memory
        if need_public_ip:
            body['needPublicIp'] = need_public_ip
        if bandwidth != 0:
            body['bandwidth'] = bandwidth
        if data_volume_list is not None:
            body['dataVolumeList'] = [v.__dict__ for v in data_volume_list]
        if dns_config is not None:
            body['dnsConfig'] = dns_config.__dict__
        if need_ipv6_public_ip:
            body['needIpv6PublicIp'] = need_ipv6_public_ip
        if disable_intranet:
            body['disableIntranet'] = disable_intranet
        if disable_cloud_init:
            body['disableCloudInit'] = disable_cloud_init
        if security_group_ids is not None:
            body['securityGroupIds'] = security_group_ids
        if hostname is not None:
            body['hostname'] = hostname
        if reservation is not None:
            body['reservation'] = reservation.__dict__
        if auto_renew is not None:
            body['autoRenew'] = auto_renew.__dict__
        if template_id is not None:
            body['templateId'] = template_id
        if deployset_id_list is not None:
            body['deploysetIdList'] = deployset_id_list
        if user_data is not None:
            body['userData'] = user_data
        if tags is not None:
            body['tags'] = [t.__dict__ for t in tags]
        if service_name is not None:
            body['serviceName'] = service_name
        if service_id is not None:
            body['serviceId'] = service_id
        if network_config_list is not None:
            body['networkConfigList'] = [n.__dict__
                                         for n in network_config_list]
        if gpu is not None:
            body['gpu'] = gpu.__dict__
        if payment_method is not None:
            body['paymentMethod'] = payment_method
        if direct_pay is not None:
            body['directPay'] = direct_pay
        if hostname_gen_method is not None:
            body['hostnameGenMethod'] = hostname_gen_method
        if action_type is not None:
            body['actionType'] = action_type
        if back_url is not None:
            body['backUrl'] = back_url
        if cuda_version is not None:
            body['cudaVersion'] = cuda_version
        if cudnn_version is not None:
            body['cudnnVersion'] = cudnn_version
        if driver_version is not None:
            body['driverVersion'] = driver_version

        return self._send_request(http_methods.POST, path, json.dumps(body),
                                  params=params, config=config)

    def list_vm_services(self, page_no=None, page_size=None,
                         keyword_type=None, keyword=None,
                         order=None, order_by=None, status=None,
                         region=None, os_name=None, service_id=None,
                         config=None):
        """
        List BEC VM services.

        :param order: Sort direction ("asc" or "desc").
        :param order_by: Field to sort by.
        :param status: Filter by service status.
        :param region: Filter by region.
        :param os_name: Filter by OS name.
        :param service_id: Filter by service ID.
        """
        path = b'/vm/service'
        params = {}
        if page_no is not None:
            params['pageNo'] = page_no
        if page_size is not None:
            params['pageSize'] = page_size
        if keyword_type is not None:
            params['keywordType'] = keyword_type
        if keyword is not None:
            params['keyword'] = keyword
        if order is not None:
            params['order'] = order
        if order_by is not None:
            params['orderBy'] = order_by
        if status is not None:
            params['status'] = status
        if region is not None:
            params['region'] = region
        if os_name is not None:
            params['osName'] = os_name
        if service_id is not None:
            params['serviceId'] = service_id

        return self._send_request(http_methods.GET, path,
                                  params=params, config=config)

    @required(service_id=(bytes, str))
    def get_vm_service(self, service_id, config=None):
        """
        Get BEC VM service details.

        :param service_id: The service ID.
        """
        path = b'/vm/service/%s' % compat.convert_to_bytes(service_id)
        return self._send_request(http_methods.GET, path, config=config)

    @required(service_id=(bytes, str))
    def update_vm_service(self, service_id, update_type,
                          vm_name=None, service_name=None,
                          deploy_instances=None,
                          data_volume_list=None, system_volume=None,
                          dns_config=None, spec=None, cpu=None, memory=None,
                          bandwidth=None,
                          need_ipv6_public_ip=None,
                          security_group_ids=None, key_config=None,
                          admin_pass=None,
                          need_restart=None, image_id=None, image_type=None,
                          hostname=None, vm_id=None,
                          network_config_list=None, replica_template=None,
                          client_token=None, config=None):
        """
        Update a BEC VM service.

        :param service_id: The service ID.
        :param update_type: Update type, one of:
            "password" — update password/keypair,
            "replicas" — update deploy replicas,
            "resource" — resize cpu/memory/spec/volume,
            "serviceName" — update service name,
            "securityGroup" — bind/unbind security groups.
        :param vm_name: New VM name (for "resource" type).
        :param service_name: New service name (for "serviceName" type).
        :param deploy_instances: Deployment instances list (for "replicas" type).
        :param security_group_ids: Security group IDs (for "securityGroup" type).
        :param key_config: Key config (required, for password/keypair configuration).
        :param admin_pass: New admin password (for "password" type).
        :param need_restart: Whether to restart the instances after the update.
        :param image_id: New image ID (for image replacement).
        :param image_type: Image type ("bec" or "bcc").
        :param hostname: New hostname (for "hostname" type).
        :param vm_id: Target VM instance ID when updating a single instance.
        :param network_config_list: NIC naming/ordering configuration.
        :type network_config_list: list<bec_model.NetworkConfig>

        :param replica_template: Replica template config.
        :type replica_template: bec_model.ReplicaTemplate
        """
        path = b'/vm/service/%s' % compat.convert_to_bytes(service_id)
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token

        body = {'type': update_type}

        if vm_name is not None:
            body['vmName'] = vm_name
        if service_name is not None:
            body['serviceName'] = service_name
        if deploy_instances is not None:
            body['deployInstances'] = [d.__dict__ for d in deploy_instances]
        if data_volume_list is not None:
            body['dataVolumeList'] = [v.__dict__ for v in data_volume_list]
        if system_volume is not None:
            body['systemVolume'] = system_volume.__dict__
        if dns_config is not None:
            body['dnsConfig'] = dns_config.__dict__
        if spec is not None:
            body['spec'] = spec
        if cpu is not None:
            body['cpu'] = cpu
        if memory is not None:
            body['memory'] = memory
        if bandwidth is not None:
            body['bandwidth'] = bandwidth
        if need_ipv6_public_ip is not None:
            body['needIpv6PublicIp'] = need_ipv6_public_ip
        if security_group_ids is not None:
            body['securityGroupIds'] = security_group_ids
        if key_config is not None:
            body['keyConfig'] = key_config.__dict__
        if admin_pass is not None:
            body['adminPass'] = admin_pass
        if need_restart is not None:
            body['needRestart'] = need_restart
        if image_id is not None:
            body['imageId'] = image_id
        if image_type is not None:
            body['imageType'] = image_type
        if hostname is not None:
            body['hostname'] = hostname
        if vm_id is not None:
            body['vmId'] = vm_id
        if network_config_list is not None:
            body['networkConfigList'] = [n.__dict__
                                         for n in network_config_list]
        if replica_template is not None:
            body['replicaTemplate'] = replica_template.__dict__

        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(service_id=(bytes, str))
    def delete_vm_service(self, service_id, client_token=None, config=None):
        """
        Delete a BEC VM service.

        :param service_id: The service ID.
        """
        path = b'/vm/service/%s' % compat.convert_to_bytes(service_id)
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token

        return self._send_request(http_methods.DELETE, path,
                                  params=params, config=config)

    @required(service_id=(bytes, str), action=(bytes, str))
    def vm_service_action(self, service_id, action,
                          client_token=None, config=None):
        """
        Start or stop a BEC VM service. (PUT /v1/vm/service/{serviceId}/{action})

        :param service_id: The service ID.
        :param action: The action to perform, 'start' or 'stop'.
        """
        path = b'/vm/service/%s/%s' % (compat.convert_to_bytes(service_id),
                                       compat.convert_to_bytes(action))
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token

        return self._send_request(http_methods.PUT, path,
                                  params=params, config=config)

    @required(service_id=(bytes, str))
    def get_vm_service_metrics(self, service_id, metrics_type,
                               service_provider=None, start=None, end=None,
                               step_in_min=None, config=None):
        """
        Get VM service monitoring metrics. (GET /v1/monitor/service/vm/{serviceId})
        """
        path = b'/monitor/service/vm/%s' % compat.convert_to_bytes(service_id)
        params = {'serviceId': service_id, 'metricsType': metrics_type}
        if service_provider is not None:
            params['serviceProvider'] = service_provider
        if start is not None:
            params['start'] = start
        if end is not None:
            params['end'] = end
        if step_in_min is not None:
            params['stepInMin'] = step_in_min

        return self._send_request(http_methods.GET, path,
                                  params=params, config=config)

    @required(service_ids=list)
    def batch_delete_vm_services(self, service_ids,
                                 client_token=None, config=None):
        """
        Batch delete BEC VM services. (POST /v1/vm/service/batch/delete)
        """
        path = b'/vm/service/batch/delete'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token

        body = json.dumps(service_ids)

        return self._send_request(http_methods.POST, path, body,
                                  params=params, config=config)

    @required(action=(bytes, str), service_ids=list)
    def batch_operate_vm_services(self, action, service_ids,
                                  client_token=None, config=None):
        """
        Batch operate (start/stop) BEC VM services. (PUT /v1/vm/service/batch/operate)
        """
        path = b'/vm/service/batch/operate'
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token

        body = {
            'action': action,
            'idList': service_ids
        }

        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    # ======================================================================
    #  VM Instance (虚机实例) APIs  —  /v1/vm/instance
    # ======================================================================

    @required(service_id=(bytes, str), deploy_instances=list)
    def create_vm_service_instance(self, service_id, deploy_instances,
                                   image_id=None, image_type=None,
                                   system_volume=None, key_config=None,
                                   vm_name=None, spec=None, cpu=None, memory=None,
                                   need_public_ip=False, bandwidth=0,
                                   data_volume_list=None, dns_config=None,
                                   need_ipv6_public_ip=False,
                                   disable_intranet=False,
                                   disable_cloud_init=False,
                                   security_group_ids=None, hostname=None,
                                   reservation=None, auto_renew=None,
                                   template_id=None, deployset_id_list=None,
                                   user_data=None, tags=None,
                                   service_name=None,
                                   network_config_list=None, gpu=None,
                                   payment_method=None, direct_pay=None,
                                   hostname_gen_method=None, action_type=None,
                                   back_url=None, cuda_version=None,
                                   cudnn_version=None, driver_version=None,
                                   client_token=None, config=None):
        """
        Create VM instances under an existing VM service.
        (POST /v1/vm/service/{serviceId}/instance)

        :param service_id: The parent service ID.
        :param deploy_instances: Deployment region list.
        :type deploy_instances: list<bec_model.DeploymentInstance>

        The remaining parameters have the same meaning as in
        :func:`create_vm_service`.
        """
        path = b'/vm/service/%s/instance' % compat.convert_to_bytes(service_id)
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token

        body = {
            'deployInstances': [d.__dict__ for d in deploy_instances]
        }

        if image_id is not None:
            body['imageId'] = image_id
        if image_type is not None:
            body['imageType'] = image_type
        if system_volume is not None:
            body['systemVolume'] = system_volume.__dict__
        if key_config is not None:
            body['keyConfig'] = key_config.__dict__
        if vm_name is not None:
            body['vmName'] = vm_name
        if spec is not None:
            body['spec'] = spec
        if cpu is not None:
            body['cpu'] = cpu
        if memory is not None:
            body['memory'] = memory
        if need_public_ip:
            body['needPublicIp'] = need_public_ip
        if bandwidth != 0:
            body['bandwidth'] = bandwidth
        if data_volume_list is not None:
            body['dataVolumeList'] = [v.__dict__ for v in data_volume_list]
        if dns_config is not None:
            body['dnsConfig'] = dns_config.__dict__
        if need_ipv6_public_ip:
            body['needIpv6PublicIp'] = need_ipv6_public_ip
        if disable_intranet:
            body['disableIntranet'] = disable_intranet
        if disable_cloud_init:
            body['disableCloudInit'] = disable_cloud_init
        if security_group_ids is not None:
            body['securityGroupIds'] = security_group_ids
        if hostname is not None:
            body['hostname'] = hostname
        if reservation is not None:
            body['reservation'] = reservation.__dict__
        if auto_renew is not None:
            body['autoRenew'] = auto_renew.__dict__
        if template_id is not None:
            body['templateId'] = template_id
        if deployset_id_list is not None:
            body['deploysetIdList'] = deployset_id_list
        if user_data is not None:
            body['userData'] = user_data
        if tags is not None:
            body['tags'] = [t.__dict__ for t in tags]
        if service_name is not None:
            body['serviceName'] = service_name
        if network_config_list is not None:
            body['networkConfigList'] = [n.__dict__
                                         for n in network_config_list]
        if gpu is not None:
            body['gpu'] = gpu.__dict__
        if payment_method is not None:
            body['paymentMethod'] = payment_method
        if direct_pay is not None:
            body['directPay'] = direct_pay
        if hostname_gen_method is not None:
            body['hostnameGenMethod'] = hostname_gen_method
        if action_type is not None:
            body['actionType'] = action_type
        if back_url is not None:
            body['backUrl'] = back_url
        if cuda_version is not None:
            body['cudaVersion'] = cuda_version
        if cudnn_version is not None:
            body['cudnnVersion'] = cudnn_version
        if driver_version is not None:
            body['driverVersion'] = driver_version

        return self._send_request(http_methods.POST, path, json.dumps(body),
                                  params=params, config=config)

    def list_vm_instances(self, page_no=None, page_size=None,
                          keyword_type=None, keyword=None,
                          order=None, order_by=None, status=None,
                          region=None, os_name=None, service_id=None,
                          city=None, service_provider=None,
                          region_id=None, vpc_id=None, config=None):
        """
        List BEC VM instances. (GET /v1/vm/instance)

        :param order: Sort direction ("asc" or "desc").
        :param order_by: Field to sort by.
        :param status: Filter by instance status.
        :param region: Filter by region.
        :param os_name: Filter by OS name.
        :param service_id: Filter by parent service ID.
        :param city: Filter by city.
        :param service_provider: Filter by service provider.
        :param region_id: Filter by node (region) ID.
        :param vpc_id: Filter by VPC ID.
        """
        path = b'/vm/instance'
        params = {}
        if page_no is not None:
            params['pageNo'] = page_no
        if page_size is not None:
            params['pageSize'] = page_size
        if keyword_type is not None:
            params['keywordType'] = keyword_type
        if keyword is not None:
            params['keyword'] = keyword
        if order is not None:
            params['order'] = order
        if order_by is not None:
            params['orderBy'] = order_by
        if status is not None:
            params['status'] = status
        if region is not None:
            params['region'] = region
        if os_name is not None:
            params['osName'] = os_name
        if service_id is not None:
            params['serviceId'] = service_id
        if city is not None:
            params['city'] = city
        if service_provider is not None:
            params['serviceProvider'] = service_provider
        if region_id is not None:
            params['regionId'] = region_id
        if vpc_id is not None:
            params['vpcId'] = vpc_id

        return self._send_request(http_methods.GET, path,
                                  params=params, config=config)

    @required(vm_id=(bytes, str))
    def get_vm_instance(self, vm_id, config=None):
        """
        Get BEC VM instance details. (GET /v1/vm/instance/{vmId})
        """
        path = b'/vm/instance/%s' % compat.convert_to_bytes(vm_id)
        return self._send_request(http_methods.GET, path, config=config)

    @required(vm_id=(bytes, str))
    def delete_vm_instance(self, vm_id, client_token=None, config=None):
        """
        Delete a BEC VM instance. (DELETE /v1/vm/instance/{vmId})
        """
        path = b'/vm/instance/%s' % compat.convert_to_bytes(vm_id)
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token

        return self._send_request(http_methods.DELETE, path,
                                  params=params, config=config)

    @required(vm_id=(bytes, str), update_type=(bytes, str))
    def update_vm_instance(self, vm_id, update_type,
                           admin_pass=None, vm_name=None,
                           hostname=None, bandwidth=None,
                           spec=None, cpu=None, memory=None,
                           image_id=None, image_type=None,
                           need_restart=False, data_volume_list=None,
                           system_volume=None, key_config=None,
                           dns_config=None, need_ipv6_public_ip=None,
                           security_group_ids=None, network_config=None,
                           client_token=None, config=None):
        """
        Update a BEC VM instance. (PUT /v1/vm/instance/{vmId})

        :param vm_id: The VM instance ID.
        :param update_type: Update type, one of:
            "vmName" — change VM name,
            "hostname" — change hostname,
            "password" — change admin password,
            "resource" — resize cpu/memory/spec/volume,
            "replicas" — change replicas,
            "securityGroup" — bind/unbind security group,
            "serviceName" — change service name.
        :param admin_pass: New admin password (for "password" type).
        :param vm_name: New VM name (for "vmName" type).
        :param hostname: New hostname (for "hostname" type).
        :param bandwidth: New bandwidth in Mbps.
        :param spec: New spec (for "resource" type).
        :param cpu: New CPU count (for "resource" type).
        :param memory: New memory in GB (for "resource" type).
        :param image_id: New image ID.
        :param image_type: Image type.
        :param need_restart: Whether to restart after update.
        :param data_volume_list: Data disk list.
        :param system_volume: System disk config.
        :param key_config: Key config.
        :param dns_config: DNS configuration.
        :param security_group_ids: Security group IDs (for "securityGroup" type).
        :param network_config: Network (public/private NIC) configuration.
        :type network_config: bec_model.NetworkConfigUpdateVmInstance
        """
        path = b'/vm/instance/%s' % compat.convert_to_bytes(vm_id)
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token

        body = {'type': update_type}

        if admin_pass is not None:
            body['adminPass'] = admin_pass
        if vm_name is not None:
            body['vmName'] = vm_name
        if hostname is not None:
            body['hostname'] = hostname
        if bandwidth is not None:
            body['bandwidth'] = bandwidth
        if spec is not None:
            body['spec'] = spec
        if cpu is not None:
            body['cpu'] = cpu
        if memory is not None:
            body['memory'] = memory
        if image_id is not None:
            body['imageId'] = image_id
        if image_type is not None:
            body['imageType'] = image_type
        if need_restart:
            body['needRestart'] = need_restart
        if data_volume_list is not None:
            body['dataVolumeList'] = [v.__dict__ for v in data_volume_list]
        if system_volume is not None:
            body['systemVolume'] = system_volume.__dict__
        if key_config is not None:
            body['keyConfig'] = key_config.__dict__
        if dns_config is not None:
            body['dnsConfig'] = dns_config.__dict__
        if need_ipv6_public_ip is not None:
            body['needIpv6PublicIp'] = need_ipv6_public_ip
        if security_group_ids is not None:
            body['securityGroupIds'] = security_group_ids
        if network_config is not None:
            body['networkConfig'] = network_config.__dict__

        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(vm_id=(bytes, str), action=(bytes, str))
    def operate_vm_deployment(self, vm_id, action,
                              client_token=None, config=None):
        """
        Start, stop or restart a BEC VM instance.
        (PUT /v1/vm/instance/{vmId}/{action})

        :param vm_id: The VM instance ID.
        :param action: The action to perform, 'start', 'stop' or 'restart'.
        """
        path = b'/vm/instance/%s/%s' % (compat.convert_to_bytes(vm_id),
                                        compat.convert_to_bytes(action))
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token

        return self._send_request(http_methods.PUT, path,
                                  params=params, config=config)

    @required(vm_id=(bytes, str), image_id=(bytes, str))
    def reinstall_vm_instance(self, vm_id, image_id, image_type='bec',
                              key_config=None, admin_pass=None,
                              reset_data_disk=None, user_data=None,
                              cuda_version=None, cudnn_version=None,
                              driver_version=None,
                              client_token=None, config=None):
        """
        Reinstall OS of a BEC VM instance. (PUT /v1/vm/instance/{vmId}/system/reinstall)

        :param reset_data_disk: Whether to also reset (format) the data disks.
        :param user_data: User data (base64 encoded).
        :param cuda_version: CUDA version (GPU images).
        :param cudnn_version: cuDNN version (GPU images).
        :param driver_version: GPU driver version.
        """
        # The BEC API requires keyConfig. Keep admin_pass as a compatibility
        # shortcut, but normalize it to the documented request shape instead
        # of sending the legacy top-level adminPass field.
        if key_config is not None and admin_pass is not None:
            raise ValueError('key_config and admin_pass are mutually exclusive')
        if key_config is None and admin_pass is None:
            raise ValueError('key_config or admin_pass is required')
        gpu_args = (cuda_version, cudnn_version, driver_version)
        if any(value is not None for value in gpu_args) \
                and not all(value is not None for value in gpu_args):
            raise ValueError(
                'cuda_version, cudnn_version and driver_version must be '
                'provided together')

        path = b'/vm/instance/%s/system/reinstall' % compat.convert_to_bytes(vm_id)
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token

        body = {
            'imageId': image_id,
            'imageType': image_type
        }
        if key_config is not None:
            body['keyConfig'] = key_config.__dict__
        else:
            body['keyConfig'] = {
                'type': 'password',
                'adminPass': admin_pass
            }
        if reset_data_disk is not None:
            body['resetDataDisk'] = reset_data_disk
        if user_data is not None:
            body['userData'] = user_data
        if cuda_version is not None:
            body['cudaVersion'] = cuda_version
        if cudnn_version is not None:
            body['cudnnVersion'] = cudnn_version
        if driver_version is not None:
            body['driverVersion'] = driver_version

        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(action=(bytes, str))
    def bind_security_group(self, action, instance_ids=None,
                            security_group_id=None, instances=None,
                            client_token=None, config=None):
        """
        Bind or unbind security groups for VM instances.
        (PUT /v1/vm/instance/securityGroup/{action})

        :param action: The action to perform, 'bind' or 'unbind'.
        :param instance_ids: List of VM instance IDs, all bound to
                             security_group_id.
        :param security_group_id: Security group ID to bind/unbind.
        :param instances: Per-instance bindings, allowing a different set of
                          security groups per instance. Takes precedence over
                          instance_ids/security_group_id.
        :type instances: list<bec_model.InstancesBinding>
        """
        path = b'/vm/instance/securityGroup/%s' % compat.convert_to_bytes(action)
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token

        body = {
            'instances': _build_instances_binding(
                instance_ids, security_group_id, instances)
        }

        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)

    @required(region=(bytes, str), service_provider=(bytes, str), city=(bytes, str))
    def list_node_vm_instances(self, region, service_provider, city,
                               page_no=None, page_size=None,
                               keyword_type=None, keyword=None, config=None):
        """
        List VM instances by node. (GET /v1/vm/instance/regions/{r}/sps/{sp}/cities/{c})
        """
        path = (b'/vm/instance/regions/%s/sps/%s/cities/%s'
                % (compat.convert_to_bytes(region),
                   compat.convert_to_bytes(service_provider),
                   compat.convert_to_bytes(city)))
        params = {}
        if page_no is not None:
            params['pageNo'] = page_no
        if page_size is not None:
            params['pageSize'] = page_size
        if keyword_type is not None:
            params['keywordType'] = keyword_type
        if keyword is not None:
            params['keyword'] = keyword

        return self._send_request(http_methods.GET, path,
                                  params=params, config=config)

    @required(vm_id=(bytes, str))
    def get_vm_instance_metrics(self, vm_id, metrics_type,
                                service_provider=None, start=None, end=None,
                                step_in_min=None, config=None):
        """
        Get VM instance monitoring metrics. (GET /v1/monitor/vm/{vmId})
        """
        path = b'/monitor/vm/%s' % compat.convert_to_bytes(vm_id)
        params = {'metricsType': metrics_type}
        if service_provider is not None:
            params['serviceProvider'] = service_provider
        if start is not None:
            params['start'] = start
        if end is not None:
            params['end'] = end
        if step_in_min is not None:
            params['stepInMin'] = step_in_min

        return self._send_request(http_methods.GET, path,
                                  params=params, config=config)

    @required(vm_id=(bytes, str))
    def get_vm_instance_config(self, vm_id, config=None):
        """
        Get VM instance configuration. (GET /v1/vm/instance/{vmId}/config)
        """
        path = b'/vm/instance/%s/config' % compat.convert_to_bytes(vm_id)
        return self._send_request(http_methods.GET, path, config=config)

    @required(vm_id=(bytes, str))
    def create_vm_private_ip(self, vm_id, secondary_private_ip_address_count=None,
                             private_ips=None, client_token=None, config=None):
        """
        Create private IP for a VM instance. (POST /v1/vm/instance/{vmId}/privateIp)
        """
        path = b'/vm/instance/%s/privateIp' % compat.convert_to_bytes(vm_id)
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token

        body = {}
        if secondary_private_ip_address_count is not None:
            body['secondaryPrivateIpAddressCount'] = secondary_private_ip_address_count
        if private_ips is not None:
            body['privateIps'] = private_ips

        return self._send_request(http_methods.POST, path, json.dumps(body),
                                  params=params, config=config)

    @required(vm_id=(bytes, str), private_ips=list)
    def delete_vm_private_ip(self, vm_id, private_ips,
                             client_token=None, config=None):
        """
        Delete (release) private IPs from a VM instance.
        (PUT /v1/vm/instance/{vmId}/privateIp/release)
        """
        path = b'/vm/instance/%s/privateIp/release' % compat.convert_to_bytes(vm_id)
        params = {}
        if client_token is None:
            params['clientToken'] = generate_client_token()
        else:
            params['clientToken'] = client_token

        body = {'privateIps': private_ips}

        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)


def _build_instances_binding(instance_ids, security_group_id, instances):
    """
    Build the "instances" body field for the security group bind/unbind APIs.

    Either instances (list<bec_model.InstancesBinding>) or both instance_ids
    and security_group_id must be provided.
    :return:
    :rtype list<dict>
    """
    if instances is not None:
        return [i.__dict__ for i in instances]
    if instance_ids is None or security_group_id is None:
        raise ValueError('either instances or both instance_ids and '
                         'security_group_id must be specified')
    return [{'instanceId': iid, 'securityGroupIds': [security_group_id]}
            for iid in instance_ids]


def generate_client_token_by_uuid():
    """
    The default method to generate the random string for client_token
    if the optional parameter client_token is not specified by the user.
    :return:
    :rtype string
    """
    return str(uuid.uuid4())


generate_client_token = generate_client_token_by_uuid
