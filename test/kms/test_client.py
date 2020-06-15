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
Unit tests for bcc client.
"""
import os
import random
import string
import sys
import unittest
import uuid
import importlib
import base64
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Cipher import AES
from Crypto.Util.asn1 import DerSequence
from Crypto import Random

import coverage
import baidubce
import kms_test_config
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.kms import kms_client
from baidubce.services.kms import keyspec_class
from baidubce.services.kms import origin_class
from baidubce.services.kms import protectedby_class
from baidubce.services.kms import publickeyencoding_class
from baidubce import compat
from imp import reload

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')
reload(sys)

cov = coverage.coverage()
cov.start()

if compat.PY2:
    sys.setdefaultencoding('utf8')
# sys.setdefaultencoding('utf-8')
'''
HOST = b'http://10.133.65.15:8101'
AK = b''
SK = b''
'''
HOST = b'http://kms.gz.qasandbox.baidu-int.com'
AK = b'b0c32bcfa987440eab823563c110dd8f'
SK = b'4c69d593d39e4ba5b8b3ddf11480821d'

class TestBccClient(unittest.TestCase):
    """
    Test class for bcc sdk client
    """

    def setUp(self):
        self.client = kms_client.KmsClient(kms_test_config.config)

    def test_create_master_key(self):
        """
        test case for create_masterKey
        """
        self.client.create_masterKey("test", protectedby_class.HSM, 
                                    keyspec_class.AES_256, origin_class.EXTERNAL)
                                    
        

    def test_list_masterKey(self):
        """
        test case for list_master_key
        """
        result = self.client.list_masterKey(10)
        for index in range(len(result.keys)):
            print result.keys[index].key_id
        

    def test_encrypt(self):
        """
        test case for encrypt
        """
        keyId = "001f9ef4-0a4b-1333-db42-e79dbd80fd25"
        #keyId = "224a8c57-9a9f-0469-796b-01d4c93f56ef"
        plaintext = base64.b64encode("hellobaby")
        print self.client.encrypt(keyId, plaintext)

    def test_decrypt(self):
        """
        test case for decrypt
        """
        keyId = "001f9ef4-0a4b-1333-db42-e79dbd80fd25"
        ciphertext = "CAESJDAwMWY5ZWY0LTBhNGItMTMzMy1kYjQyLWU3OWRiZDgwZmQyNRogL1nho0D2tRyjwPUMGg41+S2ZqVyhbL2bRBahdlUvjqkgB7KY1mxI1ptluqM+2oRF908="
        #keyId = "224a8c57-9a9f-0469-796b-01d4c93f56ef"
        #ciphertext = "CAESJDIyNGE4YzU3LTlhOWYtMDQ2OS03OTZiLTAxZDRjOTNmNTZlZhogN03xWdqNYrKWD6T8uMjWnRPqCAG9z/Cfy1ZE7JU9egkgB5GaIkhY2gKkX9qohiufp0o="
        print self.client.decrypt(keyId, ciphertext)

    def test_generate_dataKey(self):
        """
        test case for generate_datakey
        """
        keyId = "001f9ef4-0a4b-1333-db42-e79dbd80fd25"
        print self.client.generate_dataKey(keyId, keyspec_class.AES_128, 128)

    def test_enable_masterKey(self):
        """
        test case for enable_masterKey
        """
        keyId = "001f9ef4-0a4b-1333-db42-e79dbd80fd25"
        print elf.client.enable_masterKey(keyId)
    
    def test_disable_masterKey(self):
        """
        test case for disable_masterKey
        """
        keyId = "001f9ef4-0a4b-1333-db42-e79dbd80fd25"
        print self.client.disable_masterKey(keyId)
    
    def test_scheduleDelete_masterKey(self):
        """
        test case for scheduleDelete_masterKey
        """
        keyId = "001f9ef4-0a4b-1333-db42-e79dbd80fd25"
        print self.client.scheduleDelete_masterKey(keyId, 7)

    def test_cancelDelete_maaterKey(self):
        """
        test case for cancelDelete_maaterKey
        """
        keyId = "001f9ef4-0a4b-1333-db42-e79dbd80fd25"
        print self.client.cancelDelete_maaterKey(keyId)

    def test_describe_masterKey(self):
        """
        test case for describe_masterKey
        """
        keyId = '001f9ef4-0a4b-1333-db42-e79dbd80fd25'
        result = self.client.describe_masterKey(keyId)
        print result.key_metadata.protected_by

    def test_get_parameters_for_import(self):
        """
        test case for get_parameters_for_import
        """
        keyId = "16f97e43-3bdc-c97d-903f-4d7f2bc5828e"
        publicKeyEncoding = publickeyencoding_class.PEM
        print self.client.get_parameters_for_import(keyId, publicKeyEncoding)

    def test_import_AES_256(self):
        """
        test case for test_import_AES_256
        """
        # create external key
        result = self.client.create_masterKey("test", protectedby_class.HSM, 
                                    keyspec_class.AES_256, origin_class.EXTERNAL)
        keyId = str(result.key_metadata.key_id)
        
        # get import parameter
        publicKeyEncoding = publickeyencoding_class.PEM
        result = self.client.get_parameters_for_import(keyId, publicKeyEncoding)

        pubKey = str(result.public_key)
        importToken = str(result.import_token)
        rsa_pubKey = RSA.importKey(pubKey)
        cipher = PKCS1_v1_5.new(rsa_pubKey)
        aeskey = "11223344556677881122334455667788"
        print len(aeskey)
        encryptedKey = base64.b64encode(cipher.encrypt(aeskey))
        self.client.import_symmetricMasterKey(keyId, importToken, encryptedKey, keySpec="AES_256")
        
    def test_import_AES_128(self):
        """
        test case for test_import_AES_128
        """
        # create external key
        result = self.client.create_masterKey("test", protectedby_class.HSM, 
                                    keyspec_class.AES_128, origin_class.EXTERNAL)
        keyId = str(result.key_metadata.key_id)
        
        # get import parameter
        publicKeyEncoding = publickeyencoding_class.PEM
        result = self.client.get_parameters_for_import(keyId, publicKeyEncoding)
        pubKey = str(result.public_key)
        importToken = str(result.import_token)
        rsa_pubKey = RSA.importKey(pubKey)
        cipher = PKCS1_v1_5.new(rsa_pubKey)
        aeskey = "1122334455667788"
        encryptedKey = base64.b64encode(cipher.encrypt(aeskey))
        print self.client.import_symmetricMasterKey(keyId, importToken, encryptedKey, keySpec="AES_128")

    def test_import_SM1_128(self):
        """
        test case for test_import_SM1_128
        """
        # create external key
        result = self.client.create_masterKey("test", protectedby_class.HSM, 
                                    "SM1_128", origin_class.EXTERNAL)
        keyId = str(result.key_metadata.key_id)
        
        # get import parameter
        publicKeyEncoding = publickeyencoding_class.PEM
        result = self.client.get_parameters_for_import(keyId, publicKeyEncoding)
        pubKey = str(result.public_key)
        importToken = str(result.import_token)
        rsa_pubKey = RSA.importKey(pubKey)
        cipher = PKCS1_v1_5.new(rsa_pubKey)
        aeskey = "1122334455667788"
        encryptedKey = base64.b64encode(cipher.encrypt(aeskey))
        print self.client.import_symmetricMasterKey(keyId, importToken, encryptedKey, keySpec="SM1_128")

    def test_import_SM4_128(self):
        """
        test case for test_import_AES_128
        """
        # create external key
        result = self.client.create_masterKey("test", protectedby_class.HSM, 
                                    "SM4_128", origin_class.EXTERNAL)
        keyId = str(result.key_metadata.key_id)
        
        # get import parameter
        publicKeyEncoding = publickeyencoding_class.PEM
        result = self.client.get_parameters_for_import(keyId, publicKeyEncoding)
        pubKey = str(result.public_key)
        importToken = str(result.import_token)
        rsa_pubKey = RSA.importKey(pubKey)
        cipher = PKCS1_v1_5.new(rsa_pubKey)
        aeskey = "1122334455667788"
        encryptedKey = base64.b64encode(cipher.encrypt(aeskey))
        print self.client.import_symmetricMasterKey(keyId, importToken, encryptedKey, keySpec="SM4_128")

    def gcd(self, a, b):
        """
        gcd
        """
        while a != 0:
            a, b = b % a, a
        return b

    def findModReverse(self, a, m):
        """
        ModReverse
        """
        if self.gcd(a, m) != 1:
            return None
        u1, u2, u3 = 1, 0, a
        v1, v2, v3 = 0, 1, m
        while v3 != 0:
            q = u3 // v3
            v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
        return u1 % m
    
    def longToBytes(self, value):
        result = []
        i = 0
        while value >> (i * 8) > 0:
            result.append(int(value >> (i * 8) & 0xff))
            i += 1
        result.reverse()
        result_bytes=bytes(result)
        return result_bytes

    def test_import_RSA_1024(self):
        """
        test case for import_RSA_1024
        """
         # create external key
        result = self.client.create_masterKey("test", protectedby_class.HSM, 
                                    keyspec_class.RSA_1024, origin_class.EXTERNAL)
        keyId = str(result.key_metadata.key_id)
        
        # get import parameter
        publicKeyEncoding = publickeyencoding_class.PEM
        result = self.client.get_parameters_for_import(keyId, publicKeyEncoding)
        pubKey = str(result.public_key)
        importToken = str(result.import_token)
        rsa_pubKey = RSA.importKey(pubKey)
        cipher = PKCS1_v1_5.new(rsa_pubKey)

        random_generator = Random.new().read
        rsa = RSA.generate(1024, random_generator)
        pub_key = base64.b64encode(rsa.publickey().exportKey('DER'))
        D = self.longToBytes(rsa.d)
        P = self.longToBytes(rsa.p)
        Q = self.longToBytes(rsa.q)
        Dp = self.longToBytes(rsa.d % (rsa.p - 1))
        Dq = self.longToBytes(rsa.d % (rsa.q - 1))
        Qinv = self.longToBytes(self.findModReverse(rsa.q, rsa.p))
        encryptedKey  = '1122334455667788'
        aes_obj = AES.new(encryptedKey, AES.MODE_ECB, Random.new().read(AES.block_size))
        D_b64 = base64.b64encode(aes_obj.encrypt(D))
        P_b64 = base64.b64encode(aes_obj.encrypt(P))
        Q_b64 = base64.b64encode(aes_obj.encrypt(Q))
        Dp_b64 = base64.b64encode(aes_obj.encrypt(Dp))
        Dq_b64 = base64.b64encode(aes_obj.encrypt(Dq))
        Qinv_b64 = base64.b64encode(aes_obj.encrypt(Qinv))
        encryptedKeyEncryptionKey = base64.b64encode(cipher.encrypt(encryptedKey))
        self.client.import_asymmetricMasterKey(keyId, importToken, keyspec_class.RSA_1024, encryptedKeyEncryptionKey,
                                            publicKeyDer=pub_key, encryptedD=D_b64, encryptedP=P_b64,
                                            encryptedQ=Q_b64, encryptedDp=Dp_b64, encryptedDq=Dq_b64,
                                            encryptedQinv=Qinv_b64)
        ##
        
        #print self.client.import_asymmetricMasterKey()

    def test_import_RSA_2048(self):
        """
        test case for test_RSA_2048
        """
        print self.client.import_asymmetricMasterKey()

    def test_import_RSA_4096(self):
        """
        test case for test_RSA_4096
        """
        print self.client.import_asymmetricMasterKey()

    def test_import_SM2_256(self):
        """
        test case for test_RSA_4096
        """
        print self.client.import_asymmetricMasterKey()
    

def run_test():
    """start run test"""
    suite = unittest.TestSuite()
    suite.addTest(TestBccClient("test_import_RSA_1024"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
 
run_test()
cov.stop()
cov.save()
cov.html_report()

