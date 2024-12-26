"""
This module provides a client class for VPN.
"""

import copy
import json
import logging
import uuid

from baidubce import bce_base_client
from baidubce.auth import bce_v1_signer
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce.http import http_methods

from baidubce import compat

_logger = logging.getLogger(__name__)


class VpnClient(bce_base_client.BceBaseClient):
    """
    VPN base sdk client
    """

    prefix = b'/v1'
    path = b'/vpn'

    def __init__(self, config=None):
        bce_base_client.BceBaseClient.__init__(self, config)

    def _merge_config(self, config=None):
        """
        :param config:
        :type config: baidubce.BceClientConfiguration
        :return:
        """
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
            headers = {b'Accept': b'*/*', b'Content-Type': b'application/json;charset=utf-8'}
        return bce_http_client.send_request(
            config, bce_v1_signer.sign, [handler.parse_error, body_parser],
            http_method, VpnClient.prefix + path, body, headers, params)

    def list_vpns(self, vpc_id, eip=None, marker=None, max_Keys=None, config=None, vpn_type=None):
        """
        return all vpn about vpc

        :param vpc_id:
            vpc id
        :type vpcId:string

        :param eip:
            eip
        :type eip:string

        :param marker:
            The optional parameter marker specified in the original request to specify
            where in the results to begin listing.
            Together with the marker, specifies the list result which listing should begin.
            If the marker is not specified, the list result will listing from the first one.
        :type marker: string

        :param max_Keys:
            The optional parameter to specifies the max number of list result to return.
            The default value is 1000.
        :type max_Keys: int

        :param config:
        :type config: baidubce.BceClientConfiguration

        :param vpn_type:
            type of vpn
        :type vpn_type: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        params = {b'vpcId': vpc_id}

        if marker is not None:
            params[b'marker'] = marker
        if max_Keys is not None:
            params[b'maxKeys'] = max_Keys
        if eip is not None:
            params[b'eip'] = eip
        if vpn_type is not None:
            params[b'type'] = vpn_type

        return self._send_request(http_methods.GET, VpnClient.path, params=params, config=config)

    def create_vpn(self, vpc_id, vpn_name, billing,
                   vpn_type=None, max_connections=None,
                   client_token=None, description=None,
                   eip=None, config=None, subnetId=None,
                   tags=None, resourceGroupId=None, delete_protect=False):
        """
        The method of vpn to be created.

        :param vpc_id:
            vpc id
        :type vpc_id: str

        :param vpn_name:
            the name of name
        :type vpn_name: str

        :param billing:
           order_configuration
        :type billing:Billing

        :param description:
            The description of the vpn.
        :type description: string

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if clientToken is provided.
            If the clientToken is not specified by the user, a random String generated by default algorithm will be used.
        :type client_token: string

        :param eip:
            bind eip
        :type eip:str

        :param config:
        :type config: baidubce.BceClientConfiguration

        :param subnetId:
            subnetId
        :type subnetId:str

        :param tags:
            The tags of the vpn.
        :type tags: list

        :param resourceGroupId:
            The resource group ID of the vpn.
        :type resourceGroupId: str

        :param delete_protect:
            Whether to enable deletion protection on the vpn.
        :type delete_protect: bool

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        params = {}
        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token

        body = {'vpcId': vpc_id,
                'vpnName': vpn_name,
                'billing': {
                    'paymentTiming': billing.payment_timing,
                    'billingMethod': billing.billing_method,
                    'reservation': {
                        'reservationLength': billing.reservation_length,
                        'reservationTimeUnit': billing.reservation_time_unit
                    }
                },
                'deleteProtect': delete_protect
                }

        if description is not None:
            body['description'] = description
        if eip is not None:
            body['eip'] = eip
        if vpn_type is not None:
            body['type'] = vpn_type
        if max_connections is not None:
            body['maxConnection'] = max_connections
        if subnetId is not None:
            body['subnetId'] = subnetId
        if tags is not None:
            tag_list = [tag.__dict__ for tag in tags]
            body['tags'] = tag_list
        if resourceGroupId is not None:
            body['resourceGroupId'] = resourceGroupId

        return self._send_request(http_methods.POST, VpnClient.path, body=json.dumps(body), params=params,
                                  config=config)

    def update_vpn(self, vpn_id, vpn_name=None, description=None, client_token=None, config=None):
        """
        The method of vpn to be update.

        :param vpn_id: vpn id
        :type vpn_id: string

        :param vpn_name: vpn name
        :type vpn_name: str

        :param description: the description of vpn
        :type description: str

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if clientToken is provided.
            If the clientToken is not specified by the user, a random String generated by default algorithm will be used.
        :type client_token: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        path = VpnClient.path + b'/' + compat.convert_to_bytes(vpn_id)

        params = {b'modifyAttribute': None}
        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token

        body = {}
        if description is not None:
            body['description'] = description
        if vpn_name is not None:
            body['vpnName'] = vpn_name

        return self._send_request(http_methods.PUT, path, body=json.dumps(body), params=params,
                                  config=config)

    def get_vpn(self, vpn_id, config=None):
        """
        Get the detail information of  vpn.

        :param vpn_id:
            The id of vpn.
        :type vpn_id: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = VpnClient.path + b'/' + compat.convert_to_bytes(vpn_id)

        return self._send_request(http_methods.GET, path, config=config)

    def delete_vpn(self, vpn_id, client_token=None, config=None):
        """
        release VPN

        :param vpn_id:
            The id of instance.
        :type vpn_id: string

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if clientToken is provided.
            If the clientToken is not specified by the user, a random String generated by default algorithm will
            be used.
        :type client_token: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = VpnClient.path + b'/' + compat.convert_to_bytes(vpn_id)

        params = {}
        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token

        return self._send_request(http_methods.DELETE, path, params=params, config=config)

    def bind_eip(self, vpn_id, eip=None, client_token=None, config=None):
        """
        bind eip

        :param vpn_id:
            The id of instance.
        :type vpn_id: string

        :param eip:
            The address of eip.
        :type eip: string

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if clientToken is provided.
            If the clientToken is not specified by the user, a random String generated by default algorithm will
            be used.
        :type client_token: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = VpnClient.path + b'/' + compat.convert_to_bytes(vpn_id)

        params = {b'bind': None}
        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token

        body = {'eip': eip}

        return self._send_request(http_methods.PUT, path, params=params, body=json.dumps(body), config=config)

    def unbind_eip(self, vpn_id, client_token=None, config=None):
        """
        unbind eip

        :param vpn_id:
            The id of instance.
        :type vpn_id: string

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if clientToken is provided.
            If the clientToken is not specified by the user, a random String generated by default algorithm will
            be used.
        :type client_token: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = VpnClient.path + b'/' + compat.convert_to_bytes(vpn_id)

        params = {b'unbind': None}
        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token

        return self._send_request(http_methods.PUT, path, params=params, config=config)

    def renew_vpn(self, vpn_id, billing, client_token=None, config=None):
        """
        renew vpn

        :param vpn_id:
            The id of instance.
        :type vpn_id: string

        :param billing:
           order_configuration
        :type billing:Billing

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if clientToken is provided.
            If the clientToken is not specified by the user, a random String generated by default algorithm will
            be used.
        :type client_token: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = VpnClient.path + b'/' + compat.convert_to_bytes(vpn_id)

        params = {b'purchaseReserved': None}
        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token

        body = {'billing': {
            'paymentTiming': billing.payment_timing,
            'billingMethod': billing.billing_method,
            'reservation': {
                'reservationLength': billing.reservation_length,
                'reservationTimeUnit': billing.reservation_time_unit
            }
        }}

        return self._send_request(http_methods.PUT, path, params=params, body=json.dumps(body), config=config)

    def create_vpn_conn(self, vpn_id, secret_key, local_subnets, remote_ip, remote_subnets, vpn_conn_name,
                        ike_config, ipsec_config, description=None, client_token=None, config=None):

        """
        :param vpn_id: vpn id
        :type vpn_id: string

        :param secret_key:shared  key,  8~17  characters,  english,  numbers  and  symbols  must  exist  at
                                 the  same  time,and  the  symbols  are  limited  to  @#$%^*()_
        :type secret_key: string

        :param local_subnets:local network cidr list
        :type local_subnets: list

        :param remote_ip:peer vpn gateway public network ip
        :type remote_ip: string

        :param remote_subnets:peer network cidr list
        :type remote_subnets: list

        :param vpn_conn_name:vpn tunnel name, uppercase and lowercase letters, numbers and -_/. special
                            characters, must start with a letter, length 1-6
        :type vpn_conn_name: string

        :param ike_config:IKE config
        :type ike_config: IkeConfig

        :param ipsec_config:IPSec config
        :type ipsec_config: IpsecConfig

        :param description:description
        :type description: description

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if clientToken is provided.
            If the clientToken is not specified by the user, a random String generated by default algorithm will
            be used.
        :type client_token: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = VpnClient.path + b'/' + compat.convert_to_bytes(vpn_id) + b'/vpnconn'

        params = {}
        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token

        body = {
            'secretKey': secret_key,
            'localSubnets': local_subnets,
            'remoteIp': remote_ip,
            'remoteSubnets': remote_subnets,
            'vpnConnName': vpn_conn_name,
            'ikeConfig': {
                'ikeVersion': ike_config.ike_version,
                'ikeMode': ike_config.ike_mode,
                'ikeEncAlg': ike_config.ike_enc_alg,
                'ikeAuthAlg': ike_config.ike_auth_alg,
                'ikePfs': ike_config.ike_pfs,
                'ikeLifeTime': ike_config.ike_lifeTime
            },
            'ipsecConfig': {
                'ipsecEncAlg': ipsec_config.ipsec_enc_alg,
                'ipsecAuthAlg': ipsec_config.ipsec_auth_alg,
                'ipsecPfs': ipsec_config.ipsec_pfs,
                'ipsecLifetime': ipsec_config.ipsec_lifetime
            },
            'description': description,
        }

        return self._send_request(http_methods.POST, path, params=params, body=json.dumps(body), config=config)

    def update_vpn_conn(self, vpn_conn_id, vpn_id, secret_key, local_subnets, remote_ip, remote_subnets, vpn_conn_name,
                        ike_config, ipsec_config, description=None, client_token=None, config=None):

        """
        :param vpn_conn_id:vpnconn id
        :type vpn_conn_id: string

        :param vpn_id: vpn id
        :type vpn_id: string

        :param secret_key:shared  key,  8~17  characters,  english,  numbers  and  symbols  must  exist  at
                                 the  same  time,and  the  symbols  are  limited  to  @#$%^*()_
        :type secret_key: string

        :param local_subnets:local network cidr list
        :type local_subnets: list

        :param remote_ip:peer vpn gateway public network ip
        :type remote_ip: string

        :param remote_subnets:peer network cidr list
        :type remote_subnets: list

        :param vpn_conn_name:vpn tunnel name, uppercase and lowercase letters, numbers and -_/. special
                            characters, must start with a letter, length 1-6
        :type vpn_conn_name: list

        :param ike_config:IKE config
        :type ike_config: IkeConfig

        :param ipsec_config:IPSec config
        :type ipsec_config: IpsecConfig

        :param description:description
        :type description: description

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if clientToken is provided.
            If the clientToken is not specified by the user, a random String generated by default algorithm will
            be used.
        :type client_token: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = VpnClient.path + b'/vpnconn/' + compat.convert_to_bytes(vpn_conn_id)

        params = {}
        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token

        body = {
            'vpnId': vpn_id,
            'secretKey': secret_key,
            'localSubnets': local_subnets,
            'remoteIp': remote_ip,
            'remoteSubnets': remote_subnets,
            'vpnConnName': vpn_conn_name,
            'ikeConfig': {
                'ike_version': ike_config.ike_version,
                'ike_mode': ike_config.ike_mode,
                'ike_enc_alg': ike_config.ike_enc_alg,
                'ike_auth_alg': ike_config.ike_auth_alg,
                'ike_pfs': ike_config.ike_pfs,
                'ike_lifeTime': ike_config.ike_lifeTime
            },
            'ipsecConfig': {
                'ipsec_enc_alg': ipsec_config.ipsec_enc_alg,
                'ipsec_auth_alg': ipsec_config.ipsec_auth_alg,
                'ipsec_pfs': ipsec_config.ipsec_pfs,
                'ipsec_lifetime': ipsec_config.ipsec_lifetime
            },
            'description': description,
        }

        return self._send_request(http_methods.PUT, path, params=params, body=json.dumps(body), config=config)

    def get_vpn_conn(self, vpn_id, client_token=None, config=None):
        """
        :param vpn_id: vpn id
        :type vpn_id: string

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if clientToken is provided.
            If the clientToken is not specified by the user, a random String generated by default algorithm will
            be used.
        :type client_token: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = VpnClient.path + b'/vpnconn/' + compat.convert_to_bytes(vpn_id)

        params = {}
        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token

        return self._send_request(http_methods.GET, path, params=params, config=config)

    def delete_vpn_conn(self, vpn_conn_id, client_token=None, config=None):
        """
        :param vpn_conn_id:vpn conn id
        :type vpn_conn_id: string

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if clientToken is provided.
            If the clientToken is not specified by the user, a random String generated by default algorithm will
            be used.
        :type client_token: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = VpnClient.path + b'/vpnconn/' + compat.convert_to_bytes(vpn_conn_id)

        params = {}
        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token

        return self._send_request(http_methods.DELETE, path, params=params, config=config)

    def create_vpn_sslservice(self, vpn_id=None, sslservice_name=None, local_routes=None, address_pool=None,
                              interface_type=None, client_dns=None, client_token=None, config=None):
        """
        :param vpn_id: vpn id
        :type vpn_id: string

        :param sslservice_name: ssl service name, uppercase and lowercase letters, numbers and -_/. special
                            characters, must start with a letter, length 1-6
        :type sslservice_name: string

        :param local_routes: these cidrs will be configured on the client, and the next hop points to the SSL tunnel. Usually vpc cidrs
        :type local_routes: list

        :param address_pool: Client IP address pool. The VPN gateway will assign an IP address to the client on this cidr.
        :type address_pool: string

        :param interface_type: l2 or l3, default is l3, l2 is tap, l3 is tun
        :type interface_type: string

        :param client_dns: DNS server address
        :type client_dns: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = VpnClient.path + b'/' + compat.convert_to_bytes(vpn_id) + b'/sslVpnServer'

        params = {}
        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token

        body = {
            'sslVpnServerName': sslservice_name,
            'localSubnets': local_routes,
            'remoteSubnet': address_pool,
        }
        if interface_type is not None:
            body[b'interfaceType'] = interface_type
        else:
            body[b'interfaceType'] = b'tun'

        if client_dns is not None:
            body[b'clientDns'] = client_dns

        return self._send_request(http_methods.POST, path, params=params, body=json.dumps(body), config=config)

    def update_vpn_sslservice(self, vpn_id=None, sslservice_id=None, sslservice_name=None, local_routes=None,
                              address_pool=None, client_dns=None, client_token=None, config=None):
        """
        :param vpn_id: vpn id
        :type vpn_id: string

        :param sslservice_id: id
        :type sslservice_id: string

        :param sslservice_name: ssl service name, uppercase and lowercase letters, numbers and -_/. special
                            characters, must start with a letter, length 1-6
        :type sslservice_name: string

        :param local_routes: these cidrs will be configured on the client, and the next hop points to the SSL tunnel. Usually vpc cidrs
        :type local_routes: list

        :param address_pool: Client IP address pool. The VPN gateway will assign an IP address to the client on this cidr.
        :type address_pool: string

        :param client_dns: DNS server address
        :type client_dns: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = VpnClient.path + b'/' + compat.convert_to_bytes(vpn_id) \
                              + b'/sslVpnServer' + b'/' + compat.convert_to_bytes(sslservice_id)

        params = {}
        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token

        body = {}
        if sslservice_name is not None:
            body[b'sslVpnServerName'] = sslservice_name
        if local_routes is not None:
            body[b'localSubnets'] = local_routes
        if address_pool is not None:
            body[b'remoteSubnet'] = address_pool
        if client_dns is not None:
            body[b'clientDns'] = client_dns

        return self._send_request(http_methods.PUT, path, params=params, body=json.dumps(body), config=config)

    def get_vpn_sslservice(self, vpn_id, client_token=None, config=None):
        """
        :param vpn_id: vpn id
        :type vpn_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = VpnClient.path + b'/' + compat.convert_to_bytes(vpn_id) \
                              + b'/sslVpnServer'

        params = {}
        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token


        return self._send_request(http_methods.GET, path, config=config)

    def delete_vpn_sslservice(self, vpn_id, sslservice_id, client_token=None, config=None):
        """
        :param vpn_id: vpn id
        :type vpn_id: string

        :param sslservice_id: sslservice id
        :type sslservice_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = VpnClient.path + b'/' + compat.convert_to_bytes(vpn_id) \
                              + b'/sslVpnServer' + b'/' + compat.convert_to_bytes(sslservice_id)

        params = {}
        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token


        return self._send_request(http_methods.DELETE, path, config=config)

    def create_vpn_sslusers(self, vpn_id, sslusers, client_token=None, config=None):
        """
        :param vpn_id: vpn id
        :type vpn_id: string

        :param sslusers: User information list
        :type sslusers: list

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = VpnClient.path + b'/' + compat.convert_to_bytes(vpn_id) + b'/sslVpnUser'

        params = {}
        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token

        body = {
            'sslVpnUsers': []
        }
        for ssluser in sslusers:
            body[b'sslVpnUsers'].append({
                'userName': ssluser.user_name,
                'password': ssluser.password,
                'description': ssluser.description
            })

        return self._send_request(http_methods.POST, path, params=params, body=json.dumps(body), config=config)

    def update_vpn_ssl_user(self, vpn_id, ssluser_id, password=None, description=None, client_token=None, config=None):
        """
        :param vpn_id: vpn id
        :type vpn_id: string

        :param ssluser_id: ssluser id
        :type ssluser_id: string

        :param password: password id
        :type password: string

        :param description: description
        :type description: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = VpnClient.path + b'/' + compat.convert_to_bytes(vpn_id) + b'/sslVpnUser' \
                              + b'/' + compat.convert_to_bytes(ssluser_id)
        params = {}
        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token

        body = {}

        if password is not None:
            body[b'password'] = password

        if description is not None:
            body[b'description'] = description

        return self._send_request(http_methods.PUT, path, params=params, body=json.dumps(body), config=config)

    def get_vpn_ssl_user(self, vpn_id, client_token=None, config=None, marker=None, max_keys=None, user_name=None):
        """
        :param vpn_id: vpn id
        :type vpn_id: string

        :param marker:
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

        :param user_name: user name
        :type user_name: string
        
        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = VpnClient.path + b'/' + compat.convert_to_bytes(vpn_id) + b'/sslVpnUser'
        params = {}
        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token
        if marker is not None:
            params[b'marker'] = marker
        if max_keys is not None:
            params[b'maxKeys'] = max_keys
        if user_name is not None:
            params[b'userName'] = user_name

        return self._send_request(http_methods.GET, path, params=params, config=config)

    def delete_vpn_ssl_user(self, vpn_id, ssluser_id, client_token=None, config=None):
        """
        :param vpn_id: vpn id
        :type vpn_id: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = VpnClient.path + b'/' + compat.convert_to_bytes(vpn_id) + b'/sslVpnUser' \
                              + b'/' + compat.convert_to_bytes(ssluser_id)
        params = {}
        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token

        return self._send_request(http_methods.DELETE, path, params=params, config=config)
    
    def update_vpn_delete_protect(self, vpn_id, delete_protect=False, client_token=None, config=None):
        """
        :param vpn_id: vpn id
        :type vpn_id: string

        :param delete_protect:
            Whether to enable deletion protection on the vpn.
        :type delete_protect: bool

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = VpnClient.path + b'/' + compat.convert_to_bytes(vpn_id) + b'/deleteProtect'
        params = {}
        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token
        body = {
            "deleteProtect": delete_protect
        }

        return self._send_request(http_methods.PUT, path, params=params, body=json.dumps(body), config=config)


def generate_client_token_by_uuid():
    """
    The default method to generate the random string for client_token
    if the optional parameter client_token is not specified by the user.

    :return:
    :rtype string
    """
    return str(uuid.uuid4())


generate_client_token = generate_client_token_by_uuid