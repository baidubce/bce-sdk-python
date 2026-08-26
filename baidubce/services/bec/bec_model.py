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
This module provides models for BEC-SDK.
"""


class Reservation(object):
    """
    Prepaid reservation configuration.

    :param length: Reservation length.
    :param time_unit: Time unit, "month" or "year".
    """

    def __init__(self, length=1, time_unit='month'):
        self.length = length
        self.timeUnit = time_unit


class AutoRenew(object):
    """
    Auto-renew configuration.

    :param length: Auto-renew length.
    :param time_unit: Time unit, "month" or "year".
    """

    def __init__(self, length=1, time_unit='month'):
        self.length = length
        self.timeUnit = time_unit


class DeploymentInstance(object):
    """
    Deployment region configuration.

    :param region_id: Node region ID (e.g. "cn-hangzhou-cm", "cn-shenzhen-ix").
        If given, region/service_provider/city can be omitted.
    :param replicas: Number of replicas, minimum 1.
    :param network_type: Network type, "classic" or "vpc", default "vpc".
    :param vpc_id: VPC ID (optional).
    :param subnet_id: Subnet ID (optional).
    :param region: Region enum (e.g. "NORTH_CHINA"). Alternative to region_id.
    :param service_provider: Service provider enum (e.g. "CHINA_MOBILE",
        "CHINA_UNICOM", "CHINA_TELECOM", "TRIPLE_LINE"). Alternative to region_id.
    :param city: Deployment city (e.g. "BAODING1"). Alternative to region_id.
    :param sub_service_providers: Public IP service providers for a triple-line
        node, e.g. ["ct"]. Only one of sub_service_providers and
        network_config_list should be used to pin the provider.
    """

    def __init__(self, region_id=None, replicas=None,
                 network_type='vpc', vpc_id=None, subnet_id=None,
                 region=None, service_provider=None, city=None,
                 sub_service_providers=None):
        self.networkType = network_type
        if region_id is not None:
            self.regionId = region_id
        if replicas is not None:
            self.replicas = replicas
        if vpc_id is not None:
            self.vpcId = vpc_id
        if subnet_id is not None:
            self.subnetId = subnet_id
        if region is not None:
            self.region = region
        if service_provider is not None:
            self.serviceProvider = service_provider
        if city is not None:
            self.city = city
        if sub_service_providers is not None:
            self.subServiceProviders = sub_service_providers


class SystemVolumeConfig(object):
    """
    System disk configuration.

    :param volume_type: Disk type ("NVME", "SATA", "CDS_SSD", "CDS_HDD").
    :param size_in_gb: Disk size in GB.
    :param name: Disk name.
    :param pvc_name: PVC name (optional).
    """

    def __init__(self, volume_type='NVME', size_in_gb=40, name='sys',
                 pvc_name=None):
        self.volumeType = volume_type
        self.sizeInGB = size_in_gb
        self.name = name
        if pvc_name is not None:
            self.pvcName = pvc_name


class VolumeConfig(object):
    """
    Data disk configuration.

    :param volume_type: Disk type.
    :param size_in_gb: Disk size in GB.
    :param name: Disk name.
    :param pvc_name: PVC name (optional).
    :param passthrough_code: Passthrough disk code. Required together with
        volume_type "HDD_PASSTHROUGH"/"SSD_PASSTHROUGH" for exclusive disks.
    """

    def __init__(self, volume_type, size_in_gb, name, pvc_name=None,
                 passthrough_code=None):
        self.volumeType = volume_type
        self.sizeInGB = size_in_gb
        self.name = name
        if pvc_name is not None:
            self.pvcName = pvc_name
        if passthrough_code is not None:
            self.passthroughCode = passthrough_code


class KeyConfig(object):
    """
    Key/password configuration for VM login.

    :param type: Auth type, "password" or "bccKeyPair".
    :param admin_pass: Password (8-32 chars, letters+numbers+symbols required).
    :param bcc_key_pair_id_list: List of BCC key pair IDs.
    """

    def __init__(self, type='password', admin_pass=None, bcc_key_pair_id_list=None):
        self.type = type
        if admin_pass is not None:
            self.adminPass = admin_pass
        if bcc_key_pair_id_list is not None:
            self.bccKeyPairIdList = bcc_key_pair_id_list


class DnsConfig(object):
    """
    DNS configuration.

    :param dns_type: DNS type, "DEFAULT" or "CUSTOMIZE".
    :param dns_address: DNS address (comma-separated if multiple).
    """

    def __init__(self, dns_type='DEFAULT', dns_address=None):
        self.dnsType = dns_type
        if dns_address is not None:
            self.dnsAddress = dns_address


class Tag(object):
    """
    Resource tag.

    :param tag_key: Tag key.
    :param tag_value: Tag value.
    """

    def __init__(self, tag_key, tag_value=None):
        self.tagKey = tag_key
        if tag_value is not None:
            self.tagValue = tag_value


class IpAddress(object):
    """
    IP address configuration of a network interface.

    :param ip: IP address.
    :param gw: Gateway.
    :param cidr: CIDR.
    :param mask: Netmask.
    """

    def __init__(self, ip=None, gw=None, cidr=None, mask=None):
        if ip is not None:
            self.ip = ip
        if gw is not None:
            self.gw = gw
        if cidr is not None:
            self.cidr = cidr
        if mask is not None:
            self.mask = mask


class Networks(object):
    """
    Single network interface configuration.

    :param net_type: Network type, "INTERNAL_IP" for private network,
        "PUBLIC_IP" for public network, or "TRIPLE_CM"/"TRIPLE_CU"/"TRIPLE_CT"
        to pin the public IP to a specific carrier on a triple-line node.
    :param net_name: Network interface name.
    :param nic_index: Network interface index, defines the NIC order.
    :param eni_id: ENI ID.
    :param mac: MAC address.
    :param ipv4: IPv4 configuration.
    :type ipv4: IpAddress

    :param ipv6: IPv6 configuration.
    :type ipv6: IpAddress

    :param reserve_ips: Reserved IP list.
    """

    def __init__(self, net_type=None, net_name=None, nic_index=None,
                 eni_id=None, mac=None, ipv4=None, ipv6=None,
                 reserve_ips=None):
        if net_type is not None:
            self.netType = net_type
        if net_name is not None:
            self.netName = net_name
        if nic_index is not None:
            self.nicIndex = nic_index
        if eni_id is not None:
            self.eniId = eni_id
        if mac is not None:
            self.mac = mac
        if ipv4 is not None:
            self.ipv4 = ipv4.__dict__
        if ipv6 is not None:
            self.ipv6 = ipv6.__dict__
        if reserve_ips is not None:
            self.reserveIps = reserve_ips


class NetworkConfig(object):
    """
    Network interface naming and ordering configuration.

    :param node_type: Node type, "SINGLE" for a single-line node or
        "TRIPLE" for a triple-line node.
    :param networks_list: Network interface list.
    :type networks_list: list<Networks>
    """

    def __init__(self, node_type=None, networks_list=None):
        if node_type is not None:
            self.nodeType = node_type
        if networks_list is not None:
            self.networksList = [n.__dict__ for n in networks_list]


class NetworkConfigUpdateVmInstance(object):
    """
    Network interface configuration used when updating a VM instance.

    :param need_private_network: Whether the private network is needed.
    :param need_public_network: Whether the public network is needed.
    :param private_network_name: Private network interface name.
    :param public_network_name: Public network interface name.
    :param public_network_china_mobile_name: China Mobile public interface name.
    :param public_network_china_unicom_name: China Unicom public interface name.
    :param public_network_china_telecom_name: China Telecom public interface name.
    """

    def __init__(self, need_private_network=True, need_public_network=False,
                 private_network_name=None, public_network_name=None,
                 public_network_china_mobile_name=None,
                 public_network_china_unicom_name=None,
                 public_network_china_telecom_name=None):
        self.needPrivateNetwork = need_private_network
        self.needPublicNetwork = need_public_network
        if private_network_name is not None:
            self.privateNetworkName = private_network_name
        if public_network_name is not None:
            self.publicNetworkName = public_network_name
        if public_network_china_mobile_name is not None:
            self.publicNetworkChinaMobileName = public_network_china_mobile_name
        if public_network_china_unicom_name is not None:
            self.publicNetworkChinaUnicomName = public_network_china_unicom_name
        if public_network_china_telecom_name is not None:
            self.publicNetworkChinaTelecomName = public_network_china_telecom_name


class GpuRequest(object):
    """
    GPU configuration.

    :param type: GPU type.
    :param num: GPU count.
    """

    def __init__(self, type=None, num=None):
        if type is not None:
            self.type = type
        if num is not None:
            self.num = num


class ReplicaTemplate(object):
    """
    Template used when scaling out a VM service.

    :param type: Template type.
    :param template_id: VM template ID.
    """

    def __init__(self, type=None, template_id=None):
        if type is not None:
            self.type = type
        if template_id is not None:
            self.templateId = template_id


class InstancesBinding(object):
    """
    Security group binding of a single VM instance.

    :param instance_id: VM instance ID.
    :param security_group_ids: Security group ID list.
    """

    def __init__(self, instance_id, security_group_ids):
        self.instanceId = instance_id
        self.securityGroupIds = security_group_ids

