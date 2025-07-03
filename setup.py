# Copyright 2014 Baidu, Inc.
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
The setup script to install BCE SDK for python
"""
from __future__ import absolute_import
import io
import os
import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with io.open(os.path.join("baidubce", "__init__.py"), "rt") as f:
    SDK_VERSION = re.search(r"SDK_VERSION = b'(.*?)'", f.read()).group(1)

setup(
    name='bce-python-sdk',
    version=SDK_VERSION,
    install_requires=['pycryptodome>=3.8.0',
                      'future>=0.6.0',
                      'six>=1.4.0'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, <4',
    packages=['baidubce',
              'baidubce.auth',
              'baidubce.http',
              'baidubce.retry',
              'baidubce.services',
              'baidubce.services.autoscaling',
              'baidubce.services.bos',
              'baidubce.services.bts',
              'baidubce.services.iam',
              'baidubce.services.sts',
              'baidubce.services.bmr',
              'baidubce.services.dumap',
              'baidubce.services.media',
              'baidubce.services.vcr',
              'baidubce.services.vca',
              'baidubce.services.mvs',
              'baidubce.services.mms',
              'baidubce.services.sms',
              'baidubce.services.cdn',
              'baidubce.services.blb',
              'baidubce.services.eip',
              'baidubce.services.eni',
              'baidubce.services.route',
              'baidubce.services.subnet',
              'baidubce.services.vpc',
              'baidubce.services.vpn',
              'baidubce.services.endpoint',
              'baidubce.services.cfc',
              'baidubce.services.infinite',
              'baidubce.services.bcc',
              'baidubce.services.bbc',
              'baidubce.services.tsdb',
              'baidubce.services.bcm',
              'baidubce.services.kms',
              'baidubce.services.cert',
              'baidubce.services.lbdc',
              'baidubce.services.bes',
              'baidubce.services.scs',
              'baidubce.services.ddc',
              'baidubce.services.dns',
              'baidubce.services.dns.api',
              'baidubce.services.rds',
              'baidubce.services.localdns',
              'baidubce.services.localdns.api',
              'baidubce.services.oos',
              'baidubce.services.ipv6gateway',
              'baidubce.services.et',
              'baidubce.services.csn',
              'baidubce.services.havip',
              'baidubce.services.esg',
              'baidubce.services.probe',
              'baidubce.services.etGateway',
              'baidubce.services.ca',
              'baidubce.services.bls'
              ],
    url='http://bce.baidu.com',
    license='Apache License 2.0',
    author='',
    author_email='',
    description='BCE SDK for python'
)
