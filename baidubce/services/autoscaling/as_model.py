"""
This module provides a model class for AS.
"""


class Config(dict):
    """
    This class defines the Config object within AutoScalingGroupConfig.
    """

    def __init__(self, min_node_num, expect_num, max_node_num, cooldown_in_sec):
        """
        :param min_node_num: Minimum number of nodes in the auto scaling group
        :type min_node_num: int
        :param expect_num: Expected number of nodes in the auto scaling group
        :type expect_num: int
        ...
        :param cooldown_in_sec: Cooldown period in seconds for the auto scaling group
        :type cooldown_in_sec: int
        """
        super(Config, self).__init__()
        self["minNodeNum"] = min_node_num
        self["expectNum"] = expect_num
        self["maxNodeNum"] = max_node_num
        self["cooldownInSec"] = cooldown_in_sec


class HealthCheck(dict):
    """
    This class defines the HealthCheck object within AutoScalingGroupConfig.
    """

    def __init__(self, health_check_interval, grace_time):
        """
        :param health_check_interval: Interval for health checks in seconds
        :type health_check_interval: int
        :param grace_time: Grace period for health checks in seconds
        :type grace_time: int
        """
        super(HealthCheck, self).__init__()
        self["healthCheckInterval"] = health_check_interval
        self["graceTime"] = grace_time


class ZoneInfo(dict):
    """
    This class defines the ZoneInfo object.
    """

    def __init__(self, zone, subnet_id):
        """
        :param zone: Zone information
        :type zone: str
        :param subnet_id: Subnet ID
        :type subnet_id: str
        """
        super(ZoneInfo, self).__init__()
        self["zone"] = zone
        self["subnetId"] = subnet_id


class AssignTagInfo(dict):
    """
    This class defines the AssignTagInfo object.
    """

    def __init__(self, relation_tag, tags):
        """
        :param relation_tag: Relation tag
        :type relation_tag: str
        :param tags: Tags
        :type tags: list
        """
        super(AssignTagInfo, self).__init__()
        self["relationTag"] = relation_tag
        self["tags"] = tags


class Tag(dict):
    """
    This class defines the Tag object.
    """

    def __init__(self, tag_key, tag_value):
        """
        :param tag_key: Tag Key
        :type tag_key: str
        :param tag_value: Tag Value
        :type tag_value: str
        """
        super(Tag, self).__init__()
        self["tagKey"] = tag_key
        self["tagValue"] = tag_value


class Node(dict):
    """
    This class defines the Node object.
    """

    def __init__(self, cpu_count, memory_capacity_in_gb, sys_disk_type, sys_disk_in_gb, instance_type, product_type,
                 image_id, image_type, os_type, security_group_id, spec, ephemeral_disks, asp_id, priorities,
                 zone_subnet, total_count, bid_model, bid_price, cds):
        """
        :param cpu_count: The number of CPU cores
        :type cpu_count: int
        :param memory_capacity_in_gb: The capacity of the memory in GB
        :type memory_capacity_in_gb: int
        :param sys_disk_type: The type of the system disk
        :type sys_disk_type: str
        :param sys_disk_in_gb: The capacity of the system disk in GB
        :type sys_disk_in_gb: int
        :param instance_type: The type of the instance
        :type instance_type: str
        :param product_type: The type of the product
        :type product_type: str
        :param image_id: The ID of the image
        :type image_id: str
        :param image_type: The type of the image
        :type image_type: str
        :param os_type: The type of the operating system
        :type os_type: str
        :param security_group_id: The ID of the security group
        :type security_group_id: str
        :param spec: The specification
        :type spec: str
        :param ephemeral_disks: The ephemeral disks
        :type ephemeral_disks: list
        :param asp_id: The ID of the ASP
        :type asp_id: str
        :param priorities: The priorities
        :type priorities: list
        :param zone_subnet: The subnet of the zone
        :type zone_subnet: str
        :param total_count: The total count
        :type total_count: int
        :param bid_model: The model of the bid
        :type bid_model: str
        :param bid_price: The price of the bid
        :type bid_price: float
        :param cds: The CDS
        :type cds: list
        """
        super(Node, self).__init__()
        self["cpuCount"] = cpu_count
        self["memoryCapacityInGB"] = memory_capacity_in_gb
        self["sysDiskType"] = sys_disk_type
        self["sysDiskInGB"] = sys_disk_in_gb
        self["instanceType"] = instance_type
        self["productType"] = product_type
        self["imageId"] = image_id
        self["imageType"] = image_type
        self["osType"] = os_type
        self["securityGroupId"] = security_group_id
        self["spec"] = spec
        self["ephemeralDisks"] = ephemeral_disks
        self["aspId"] = asp_id
        self["priorities"] = priorities
        self["zoneSubnet"] = zone_subnet
        self["totalCount"] = total_count
        self["bidModel"] = bid_model
        self["bidPrice"] = bid_price
        self["cds"] = cds


class Eip(dict):
    """
    This class defines EIP information.
    """

    def __init__(self, if_bind_eip, bandwidth_in_mbps, eip_product_type):
        """
        :param if_bind_eip: if bind eip
        :type if_bind_eip: bool
        :param bandwidth_in_mbps: bandwidth_in_mbps
        :type bandwidth_in_mbps: int
        :param eip_product_type: eip_product_type
        :type eip_product_type: string
        """
        super(Eip, self).__init__()
        self["ifBindEip"] = if_bind_eip
        self["bandwidthInMbps"] = bandwidth_in_mbps
        self["eipProductType"] = eip_product_type


class Billing(dict):
    """
    This class defines the Billing object.
    """

    def __init__(self, payment_timing):
        """
        :param payment_timing: The timing of the payment
        :type payment_timing: str
        """
        super(Billing, self).__init__()
        self["paymentTiming"] = payment_timing


class CmdConfig(dict):
    """
    This class defines the CmdConfig object.
    """

    def __init__(self, has_decrease_cmd, dec_cmd_strategy, dec_cmd_data, dec_cmd_timeout, dec_cmd_manual,
                 has_increase_cmd, inc_cmd_strategy, inc_cmd_data, inc_cmd_timeout, inc_cmd_manual):
        """
        :param has_decrease_cmd: If has decrease command
        :type has_decrease_cmd: bool
        :param dec_cmd_strategy: The strategy of the decrease command
        :type dec_cmd_strategy: str
        :param dec_cmd_data: The data of the decrease command
        :type dec_cmd_data: str
        :param dec_cmd_timeout: The timeout of the decrease command
        :type dec_cmd_timeout: int
        :param dec_cmd_manual: If the decrease command is manual
        :type dec_cmd_manual: bool
        :param has_increase_cmd: If has increase command
        :type has_increase_cmd: bool
        :param inc_cmd_strategy: The strategy of the increase command
        :type inc_cmd_strategy: str
        :param inc_cmd_data: The data of the increase command
        :type inc_cmd_data: str
        :param inc_cmd_timeout: The timeout of the increase command
        :type inc_cmd_timeout: int
        :param inc_cmd_manual: If the increase command is manual
        :type inc_cmd_manual: bool
        """
        super(CmdConfig, self).__init__()
        self["hasDecreaseCmd"] = has_decrease_cmd
        self["decCmdStrategy"] = dec_cmd_strategy
        self["decCmdData"] = dec_cmd_data
        self["decCmdTimeout"] = dec_cmd_timeout
        self["decCmdManual"] = dec_cmd_manual
        self["hasIncreaseCmd"] = has_increase_cmd
        self["incCmdStrategy"] = inc_cmd_strategy
        self["incCmdData"] = inc_cmd_data
        self["incCmdTimeout"] = inc_cmd_timeout
        self["incCmdManual"] = inc_cmd_manual


class BccNameConfig(dict):
    """
    This class defines the BccNameConfig object.
    """

    def __init__(self, bcc_name, bcc_hostname):
        """
        :param bcc_name: The name of the BCC
        :type bcc_name: str
        :param bcc_hostname: The hostname of the BCC
        :type bcc_hostname: str
        """
        super(BccNameConfig, self).__init__()
        self["bccName"] = bcc_name
        self["bccHostname"] = bcc_hostname
