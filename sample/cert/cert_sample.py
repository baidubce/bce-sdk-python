# Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

"""
Samples for cert client.
"""

import cert_sample_conf

from baidubce.services.cert.cert_client import CertClient
from baidubce.services.cert.cert_model import CertCreateRequest

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    __logger = logging.getLogger(__name__)

    # create a cert client
    cert_client = CertClient(cert_sample_conf.config)

    # certificate test data
    cert_name = 'certificate name'
    cert_type = 1
    cert_server_data = 'Fill certificate here'
    cert_private_data = 'Fill private key here'
    cert_link_data = "Fill certificate chain here"

    # SAMPLE1: create a certificate
    cert_create_request = CertCreateRequest(cert_name, cert_server_data, cert_private_data, cert_link_data, cert_type)
    response = cert_client.create_cert(cert_create_request)
    cert_id = response.certId

    # SAMPLE2: list your certificates
    cert_client.list_user_certs()

    # SAMPLE3: get certificate by id
    cert_client.get_cert_info('certificate id')

    # SAMPLE4: replace a certificate
    cert_name = 'new certificate name'
    cert_create_request = CertCreateRequest(cert_name, cert_server_data, cert_private_data, cert_link_data, cert_type)
    cert_client.replace_cert(cert_id, cert_create_request)

    # SAMPLE5: delete certificate by id
    cert_client.delete_cert(cert_id)
