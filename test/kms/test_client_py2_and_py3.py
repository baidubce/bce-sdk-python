#!/usr/bin/env python
#coding=utf8

# Copyright 2014 Baidu, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
import os
import random
import string
import sys
import unittest
import uuid
import importlib
import base64
import json
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Cipher import AES
from Crypto.Util.asn1 import DerSequence, DerObject
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
HOST = b''
AK = b''
SK = b''
'''
HOST = b'<your Host>'
AK = b'<your AK>'
SK = b'<your SK>'

class TestKmsClient(unittest.TestCase):
    """
    Test class for kms sdk client
    """

    def setUp(self):
        self.client = kms_client.KmsClient(kms_test_config.config)

    def test_create_master_key(self):
        """
        test case for create_masterKey
        """
        result = self.client.create_masterKey("test", protectedby_class.HSM, 
                                    keyspec_class.RSA_4096, origin_class.BAIDU_KMS)
        

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
        keyId = "<your Key Id>"
        #keyId = "224a8c57-9a9f-0469-796b-01d4c93f56ef"
        plaintext = "testtest"
        result =  self.client.encrypt(keyId, plaintext)
        print self.client.decrypt(keyId, str(result.ciphertext))


    def test_decrypt(self):
        """
        test case for decrypt
        """
        keyId = "<your Key Id>"
        ciphertext = "CAESJDUxMWU3OWY2LTI2ZTktYjAzNy0xNTE0LTk4ZDVjMmEyOGE2MxogPIgjk/0r3ZIHFdikZbuoo6NBTgP8lkMp+V3eaXqQ22ggAP/2QYj73LZz/G2LKZhJM74="
        #keyId = "224a8c57-9a9f-0469-796b-01d4c93f56ef"
        #ciphertext = "CAESJDIyNGE4YzU3LTlhOWYtMDQ2OS03OTZiLTAxZDRjOTNmNTZlZhogN03xWdqNYrKWD6T8uMjWnRPqCAG9z/Cfy1ZE7JU9egkgB5GaIkhY2gKkX9qohiufp0o="
        print self.client.decrypt(keyId, ciphertext)

    def test_sign(self):
        """
        test case for sign
        """
        keyId = "<your Key Id>"
        keyVersion = "MjEzNTk0MTc4OA=="

        # Test RAW message type
        raw_message = base64.b64encode(b"aGVsbG8gd29ybGQh")

        # Test without keyVersion
        result = self.client.sign(
            keyId=keyId,
            algorithm="RSA_PKCS1_SHA_256",
            message=raw_message,
            messageType="RAW"
        )
        print "RAW signature:", str(result.signature)

        # Test with keyVersion
        result_with_version = self.client.sign(
            keyId=keyId,
            algorithm="RSA_PKCS1_SHA_256",
            message=raw_message,
            keyVersion=keyVersion,
            messageType="RAW"
        )
        print "RAW signature with version:", str(result_with_version.signature)

        # Test DIGEST message type (32 bytes)
        digest = hashlib.sha256(b"aGVsbG8gd29ybGQh").digest()
        digest_message = base64.b64encode(digest)

        digest_result = self.client.sign(
            keyId=keyId,
            algorithm="RSA_PKCS1_SHA_256",
            message=digest_message,
            messageType="DIGEST"
        )
        print "DIGEST signature:", str(digest_result.signature)

        # Test DIGEST with keyVersion
        digest_result_with_version = self.client.sign(
            keyId=keyId,
            algorithm="RSA_PKCS1_SHA_256",
            message=digest_message,
            keyVersion=keyVersion,
            messageType="DIGEST"
        )
        print "DIGEST signature with version:", str(digest_result_with_version.signature)

    def test_verify(self):
        """
        test case for verify
        """
        keyId = "<your Key Id>"
        message = base64.b64encode(b"aGVsbG8gd29ybGQh")
        keyVersion = "MjEzNTk0MTc4OA=="

        # First sign a message to get signature
        sign_result = self.client.sign(
            keyId=keyId,
            algorithm="RSA_PKCS1_SHA_256",
            message=message
        )

        # Ensure signature is str type (not unicode)
        signature = str(sign_result.signature)

        # Test verify without keyVersion
        verify_result = self.client.verify(
            keyId=str(keyId),
            algorithm=str("RSA_PKCS1_SHA_256"),
            signature=signature,
            message=str(message)
        )
        print str(verify_result.signature_valid)

        # Test verify with keyVersion
        verify_result_with_version = self.client.verify(
            keyId=str(keyId),
            algorithm=str("RSA_PKCS1_SHA_256"),
            signature=signature,
            message=str(message),
            keyVersion=str(keyVersion) if keyVersion else None
        )
        print str(verify_result_with_version.signature_valid)

    def test_generate_dataKey(self):
        """
        test case for generate_datakey
        """
        keyId = "<your Key Id>"
        print self.client.generate_dataKey(keyId, keyspec_class.AES_128, 128)
    
    def test_updaterotation_masterKey(self):
        """
        test case for updaterotation_masterKey
        """
        keyId = "<your Key Id>"
        print self.client.updaterotation_masterKey(keyId, 10)

    def test_enable_masterKey(self):
        """
        test case for enable_masterKey
        """
        keyId = "<your Key Id>"
        print self.client.enable_masterKey(keyId)
    
    def test_disable_masterKey(self):
        """
        test case for disable_masterKey
        """
        keyId = "<your Key Id>"
        print self.client.disable_masterKey(keyId)
    
    def test_scheduleDelete_masterKey(self):
        """
        test case for scheduleDelete_masterKey
        """
        keyId = "<your Key Id>"
        print self.client.scheduleDelete_masterKey(keyId, 7)

    def test_cancelDelete_maaterKey(self):
        """
        test case for cancelDelete_maaterKey
        """
        keyId = "<your Key Id>"
        print self.client.cancelDelete_maaterKey(keyId)

    def test_describe_masterKey(self):
        """
        test case for describe_masterKey
        """
        keyId = '<your Key Id>'
        result = self.client.describe_masterKey(keyId)
        print result.key_metadata.protected_by

    def test_get_parameters_for_import(self):
        """
        test case for get_parameters_for_import
        """
        keyId = "<your Key Id>"
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
        der = DerSequence()
        der.append(rsa.n)
        der.append(rsa.e)
        pub_key = base64.b64encode(der.encode())
        D = str(hex(rsa.d)[2:-1]).decode("hex")
        P = str(hex(rsa.p)[2:-1]).decode("hex")
        Q = str(hex(rsa.q)[2:-1]).decode("hex")
        Dp = str(hex(rsa.d % (rsa.p - 1))[2:-1]).decode("hex")
        Dq = str(hex(rsa.d % (rsa.q - 1))[2:-1]).decode("hex")
        Qinv = str(hex(self.findModReverse(rsa.q, rsa.p))[2:-1]).decode("hex")
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
        
        
        #print self.client.import_asymmetricMasterKey()

    def test_import_RSA_2048(self):
        """
        test case for test_RSA_2048
        """
        # create external key
        result = self.client.create_masterKey("test", protectedby_class.HSM, 
                                    keyspec_class.RSA_2048, origin_class.EXTERNAL)
        keyId = str(result.key_metadata.key_id)
        
        # get import parameter
        publicKeyEncoding = publickeyencoding_class.PEM
        result = self.client.get_parameters_for_import(keyId, publicKeyEncoding)
        pubKey = str(result.public_key)
        importToken = str(result.import_token)
        rsa_pubKey = RSA.importKey(pubKey)
        cipher = PKCS1_v1_5.new(rsa_pubKey)

        random_generator = Random.new().read
        rsa = RSA.generate(2048, random_generator)
        der = DerSequence()
        der.append(rsa.n)
        der.append(rsa.e)
        pub_key = base64.b64encode(der.encode())
        D = str(hex(rsa.d)[2:-1]).decode("hex")
        P = str(hex(rsa.p)[2:-1]).decode("hex")
        Q = str(hex(rsa.q)[2:-1]).decode("hex")
        Dp = str(hex(rsa.d % (rsa.p - 1))[2:-1]).decode("hex")
        Dq = str(hex(rsa.d % (rsa.q - 1))[2:-1]).decode("hex")
        Qinv = str(hex(self.findModReverse(rsa.q, rsa.p))[2:-1]).decode("hex")
        encryptedKey  = '1122334455667788'
        aes_obj = AES.new(encryptedKey, AES.MODE_ECB, Random.new().read(AES.block_size))
        D_b64 = base64.b64encode(aes_obj.encrypt(D))
        P_b64 = base64.b64encode(aes_obj.encrypt(P))
        Q_b64 = base64.b64encode(aes_obj.encrypt(Q))
        Dp_b64 = base64.b64encode(aes_obj.encrypt(Dp))
        Dq_b64 = base64.b64encode(aes_obj.encrypt(Dq))
        Qinv_b64 = base64.b64encode(aes_obj.encrypt(Qinv))
        encryptedKeyEncryptionKey = base64.b64encode(cipher.encrypt(encryptedKey))
        self.client.import_asymmetricMasterKey(keyId, importToken, keyspec_class.RSA_2048, encryptedKeyEncryptionKey,
                                            publicKeyDer=pub_key, encryptedD=D_b64, encryptedP=P_b64,
                                            encryptedQ=Q_b64, encryptedDp=Dp_b64, encryptedDq=Dq_b64,
                                            encryptedQinv=Qinv_b64)
        

    def test_import_RSA_4096(self):
        """
        test case for test_RSA_4096
        """
        result = self.client.create_masterKey("test", protectedby_class.HSM, 
                                    keyspec_class.RSA_4096, origin_class.EXTERNAL)
        keyId = str(result.key_metadata.key_id)
        
        # get import parameter
        publicKeyEncoding = publickeyencoding_class.PEM
        result = self.client.get_parameters_for_import(keyId, publicKeyEncoding)
        pubKey = str(result.public_key)
        importToken = str(result.import_token)
        rsa_pubKey = RSA.importKey(pubKey)
        cipher = PKCS1_v1_5.new(rsa_pubKey)

        random_generator = Random.new().read
        rsa = RSA.generate(4096, random_generator)
        der = DerSequence()
        der.append(rsa.n)
        der.append(rsa.e)
        pub_key = base64.b64encode(der.encode())
        D = str(hex(rsa.d)[2:-1]).decode("hex") if len(str(hex(rsa.d)[2:-1]))%2==0 else str("0"+hex(rsa.d)[2:-1]).decode("hex")
        P = str(hex(rsa.p)[2:-1]).decode("hex") if len(str(hex(rsa.p)[2:-1]))%2==0 else str("0"+hex(rsa.p)[2:-1]).decode("hex")
        Q = str(hex(rsa.q)[2:-1]).decode("hex") if len(str(hex(rsa.q)[2:-1]))%2==0 else str("0"+hex(rsa.q)[2:-1]).decode("hex")
        Dp = str(hex(rsa.d % (rsa.p - 1))[2:-1]).decode("hex") if len(str(hex(rsa.d % (rsa.p - 1))[2:-1]))%2==0 else str("0"+hex(rsa.d % (rsa.p - 1))[2:-1]).decode("hex")
        Dq = str(hex(rsa.d % (rsa.q - 1))[2:-1]).decode("hex") if len(str(hex(rsa.d % (rsa.q - 1))[2:-1]))%2==0 else str("0"+hex(rsa.d % (rsa.q - 1))[2:-1]).decode("hex")
        Qinv = str(hex(self.findModReverse(rsa.q, rsa.p))[2:-1]).decode("hex") if len(str(hex(self.findModReverse(rsa.q, rsa.p))[2:-1]))%2==0 else str("0"+hex(self.findModReverse(rsa.q, rsa.p))[2:-1]).decode("hex")
        encryptedKey  = '1122334455667788'
        aes_obj = AES.new(encryptedKey, AES.MODE_ECB)
        D_b64 = base64.b64encode(aes_obj.encrypt(D))
        P_b64 = base64.b64encode(aes_obj.encrypt(P))
        Q_b64 = base64.b64encode(aes_obj.encrypt(Q))
        Dp_b64 = base64.b64encode(aes_obj.encrypt(Dp))
        Dq_b64 = base64.b64encode(aes_obj.encrypt(Dq))
        Qinv_b64 = base64.b64encode(aes_obj.encrypt(Qinv))
        encryptedKeyEncryptionKey = base64.b64encode(cipher.encrypt(encryptedKey))
        self.client.import_asymmetricMasterKey(keyId, importToken, keyspec_class.RSA_4096, encryptedKeyEncryptionKey,
                                            publicKeyDer=pub_key, encryptedD=D_b64, encryptedP=P_b64,
                                            encryptedQ=Q_b64, encryptedDp=Dp_b64, encryptedDq=Dq_b64,
                                            encryptedQinv=Qinv_b64)

    def test_import_SM2_256(self):
        """
        test case for test_SM2_256
        """
        result = self.client.create_masterKey("test", protectedby_class.HSM, 
                                    keyspec_class.SM2_256, origin_class.EXTERNAL)
        keyId = str(result.key_metadata.key_id)
        
        # get import parameter
        publicKeyEncoding = publickeyencoding_class.PEM
        result = self.client.get_parameters_for_import(keyId, publicKeyEncoding)
        pubKey = str(result.public_key)
        importToken = str(result.import_token)
        rsa_pubKey = RSA.importKey(pubKey)
        cipher = PKCS1_v1_5.new(rsa_pubKey)

        sm2_public_key = bytes.fromhex("3059301306072a8648ce3d020106082a811ccf5501822d0342000449451af193e9b\
            d4d7d4329504a9f3a3bd9981318b8177535b02d02b361b579cda9d5eb0feb9980ed41cd159ef7036f5cacd7e018bacb5\
            ec854d3f575fdcc6182")
        sm2_private_key = bytes.fromhex("c227a82bf3ae6819d9f1d8179e9bbb5f2ce7f49acb1a64b0f6d1698b5ac0a160")

        base64_sm2_public_key = base64.b64encode(sm2_public_key).decode()
        
        encryptedKey  = '1122334455667788'
        aes_obj = AES.new(encryptedKey, AES.MODE_ECB)
        base64_sm2_private_key = base64.b64encode(aes_obj.encrypt(sm2_private_key)).decode()
        encryptedKeyEncryptionKey = base64.b64encode(cipher.encrypt(encryptedKey))
        self.client.import_asymmetricMasterKey(keyId, importToken, keyspec_class.SM2_256, encryptedKeyEncryptionKey,
                                                    publicKeyDer=base64_sm2_public_key, 
                                                    encryptedPrivateKey=base64_sm2_private_key)

def run_test():
    """start run test"""
    suite = unittest.TestSuite()
    suite.addTest(TestKmsClient("test_import_RSA_4096"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
 
run_test()
cov.stop()
cov.save()
cov.html_report()

