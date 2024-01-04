"""
example for recommit et channel.
"""

import uuid

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.exception import BceHttpClientError
from baidubce.services.et import et_client


if __name__ == "__main__":
    ak = "Your AK"
    sk = "Your SK"
    endpoint = "bcc.bj.baidubce.com"
    config = BceClientConfiguration(credentials=BceCredentials(access_key_id=ak, secret_access_key=sk),
                                    endpoint=endpoint)
    et_client = et_client.EtClient(config)
    try:
        resp = et_client.recommit_et_channel(et_id="Your et_id", et_channel_id="Your et_channel_id",
                                            local_ip="BaiduAddress", name="name", networks=["Your cidr"],
                                            remote_ip="CustomerAddress", route_type="Your routeType", vlan_id=2,
                                            authorized_users=["Your user"], description="description", enable_ipv6=1,
                                            local_ipv6="BaiduIPv6Address", remote_ipv6="CustomerIPv6Address",
                                            ipv6_networks=["Your IPv6 cidr"], client_token=str(uuid.uuid4()))
        print("Recommit et response: %s" % resp)
    except BceHttpClientError as e:
        print("Exception when calling api: %s" % e)