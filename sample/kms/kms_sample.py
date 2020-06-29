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
"""
Samples for kms client.
"""
import time
import logging
import base64
import sys
import os
# 从Python SDK导入KMS配置管理模块以及安全认证模块
from Crypto.Random._UserFriendlyRNG import RNGFile
from baidubce.auth import bce_credentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials
import kms_sample_conf
# 导入Kms相关模块
from baidubce import exception, bce_client_configuration
from baidubce.services.kms import kms_client
from baidubce.services.kms import keyspec_class
from baidubce.services.kms import origin_class
from baidubce.services.kms import protectedby_class
from baidubce.services.kms import publickeyencoding_class
from baidubce.utils import print_object
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Cipher import AES
from Crypto.Util.asn1 import DerSequence, DerObject
from Crypto import Random
 
case_result_list = []
 
class Python2SDKSample(object):
    tmp_result = {}
 
    def __init__(self):
        return
 
    def KMS_create_suit(self, cipher_type):
        action_type = "KMS"
        # 密钥管理-创建密钥
        self.create_key(cipher_type, action_type)
 
        # 密钥管理-列举MasterKey
        self.list_master_key(10, cipher_type, action_type)
 
        # 密钥管理-获取MasterKey详细信息
        tmp_master_key = Python2SDKSample.tmp_result["MasterKey"]
        self.get_master_key(tmp_master_key, cipher_type, action_type)
 
        # 密钥管理-加密数据
        self.encrypt_key(tmp_master_key, "testtest", cipher_type, action_type)
 
        # 密钥管理-解密数据
        encrypt_result = Python2SDKSample.tmp_result["CipherText"]
        self.decrpyt_key(tmp_master_key, encrypt_result, cipher_type, action_type)
 
        # 密钥管理-生成DataKey, 仅仅支持software的AES_128/AES_256
        if cipher_type == "AES_128" or cipher_type == "AES_256":
            self.create_data_key(tmp_master_key, 10, cipher_type, action_type)
 
        # 密钥管理-使MasterKey处于不可用状态
        self.disable_master_key(tmp_master_key, cipher_type, action_type)
 
        # 密钥管理-使MasterKey处于可用状态
        self.enable_master_key(tmp_master_key, cipher_type, action_type)
 
        # 密钥管理-删除MasterKey
        self.del_master_key(tmp_master_key, 17, cipher_type, action_type)
 
        # 密钥管理-取消删除MasterKey
        self.cancle_master_key(tmp_master_key, cipher_type, action_type)
        # 取消删除后是禁用状态，再次使MasterKey处于可用状态
        self.enable_master_key(tmp_master_key, cipher_type, action_type)
        return
 
    def external_create_suit(self, cipher_type):
        action_type = "external"
        # 密钥管理-创建密钥
        self.create_key(cipher_type, action_type)
 
        # 密钥管理-获取导入密钥参数
        tmp_master_key = Python2SDKSample.tmp_result["MasterKey"]
        self.get_param_list(tmp_master_key, cipher_type, action_type)
 
        # 密钥管理-导入对称密钥
        if "AES" in cipher_type:
            self.import_symmetric_key(tmp_master_key, cipher_type, action_type)
 
        # 密钥管理-导入非对称密钥
        if "RSA" in cipher_type:
            self.import_asymmetric_key(tmp_master_key, cipher_type, action_type)
 
        # #生成完整密钥后进行如下操作
        # 密钥管理-列举MasterKey
        self.list_master_key(10, cipher_type, action_type)
 
        # 密钥管理-获取MasterKey详细信息
        self.get_master_key(tmp_master_key, cipher_type, action_type)
 
        # 密钥管理-加密数据
        self.encrypt_key(tmp_master_key, "testtest", cipher_type, action_type)
 
        # 密钥管理-解密数据
        encrypt_result = Python2SDKSample.tmp_result["CipherText"]
        self.decrpyt_key(tmp_master_key, encrypt_result, cipher_type, action_type)
 
        # 密钥管理-生成DataKey, 外部导入不支持
 
        # 密钥管理-使MasterKey处于不可用状态
        self.disable_master_key(tmp_master_key, cipher_type, action_type)
 
        # 密钥管理-使MasterKey处于可用状态
        self.enable_master_key(tmp_master_key, cipher_type, action_type)
 
        # 密钥管理-删除MasterKey
        self.del_master_key(tmp_master_key, 17, cipher_type, action_type)
 
        # 密钥管理-取消删除MasterKey
        self.cancle_master_key(tmp_master_key, cipher_type, action_type)
 
        # 取消删除后是禁用状态，再次使MasterKey处于可用状态
        self.enable_master_key(tmp_master_key, cipher_type, action_type)
 
    def AES_ECB_fill(self, AES_plaintext):
        # AES ECB mode need Integral multiple of 16
        rem = len(AES_plaintext.encode('utf-8')) % 16
        if rem:
            fill_len = 16 - rem
        else:
            fill_len = 0
        ECB_filled = AES_plaintext + ("\0" * fill_len)
        return ECB_filled.encode('utf-8')
 
    def gcd(self, a, b):
        """
        gcd
        """
        while a != 0:
            a, b = b % a, a
        return b
 
    # 求模逆
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
 
    # 密钥管理-创建密钥
    # create_type == KMS | external
    def create_key(self, key_type, create_type):
        case = {"case_name": "create_key " + key_type + " : " + create_type}
        print("%s: %s : start create type key ... ... " % (create_type, key_type))
        try:
            if key_type == "BAIDU_AES_256":
                result = kmsClient.create_masterKey("BAIDU AES 256 test", protectedby_class.HSM,
                                                    keyspec_class.BAIDU_ASE_256, origin_class.BAIDU_KMS)
                print("--------result:", result)
            if key_type == "AES_128":
                if create_type == "KMS":
                    result = kmsClient.create_masterKey("KMS type: AES 128", protectedby_class.HSM,
                                                        keyspec_class.AES_128, origin_class.BAIDU_KMS)
                if create_type == "external":
                    result = kmsClient.create_masterKey("external: AES 128", protectedby_class.HSM,
                                                        keyspec_class.AES_128, origin_class.EXTERNAL)
            if key_type == "AES_256":
                if create_type == "KMS":
                    result = kmsClient.create_masterKey("KMS type: AES 256", protectedby_class.HSM,
                                                        keyspec_class.AES_256, origin_class.BAIDU_KMS)
                if create_type == "external":
                    result = kmsClient.create_masterKey("external: AES 256", protectedby_class.HSM,
                                                        keyspec_class.AES_256, origin_class.EXTERNAL)
            if key_type == "RSA_1024":
                if create_type == "KMS":
                    result = kmsClient.create_masterKey("KMS type: RSA 1024", protectedby_class.HSM,
                                                        keyspec_class.RSA_1024, origin_class.BAIDU_KMS)
                if create_type == "external":
                    result = kmsClient.create_masterKey("external: RSA 1024", protectedby_class.HSM,
                                                        keyspec_class.RSA_1024, origin_class.EXTERNAL)
            if key_type == "RSA_2048":
                if create_type == "KMS":
                    result = kmsClient.create_masterKey("KMS type: RSA 2048", protectedby_class.HSM,
                                                        keyspec_class.RSA_2048, origin_class.BAIDU_KMS)
                if create_type == "external":
                    result = kmsClient.create_masterKey("external: RSA 2048", protectedby_class.HSM,
                                                        keyspec_class.RSA_2048, origin_class.EXTERNAL)
            if key_type == "RSA_4096":
                if create_type == "KMS":
                    result = kmsClient.create_masterKey("KMS type: RSA 4096", protectedby_class.HSM,
                                                        keyspec_class.RSA_4096, origin_class.BAIDU_KMS)
                if create_type == "external":
                    result = kmsClient.create_masterKey("external: RSA 4096", protectedby_class.HSM,
                                                        keyspec_class.RSA_4096, origin_class.EXTERNAL)
        except Exception as err:
            print("can not match any cipher type:", err)
 
        # 记录测试结果
        case["case_type"] = create_type
        if result.metadata.bce_errmsg == 'Success':
            case["case_status"] = "pass"
            Python2SDKSample.tmp_result["MasterKey"] = str(result.key_metadata.key_id)
            # 等1秒，确保后面的case可以获取返回结果
            time.sleep(1)
        else:
            case["case_status"] = "false"
            case["detail"] = result
            # print "key_metadata:", result.key_metadata
            # print "metadata:", result.metadata
        global case_result_list
        case_result_list.append(case)
        return
 
    # 密钥管理-列举MasterKey
    @staticmethod
    def list_master_key(limitNum, key_type, action_type):
        case = {"case_name": "list_master_key"}
        print("%s: %s : start list_master_key test ... " % (action_type, key_type))
        result = kmsClient.list_masterKey(limitNum)
        # 打印所有密钥keyid
        # for index in range(len(result.keys)):
            #print result.keys[index].key_id
 
        # 记录测试结果
        case["case_type"] = action_type
        if result.metadata.bce_errmsg == 'Success':
            case["case_status"] = "pass"
        else:
            case["case_status"] = "false"
            case["detail"] = result
        global case_result_list
        case_result_list.append(case)
        return
 
    # 密钥管理-获取MasterKey详细信息
    @staticmethod
    def get_master_key(MasterKey, key_type, action_type):
        case = {"case_name": "get_master_key : " + MasterKey + ":" + key_type}
        print("%s: %s : start get master key detail info test ... " % (action_type, key_type))
        result = kmsClient.describe_masterKey(MasterKey)
        # result = result.key_metadata
        # print print_object(result)
        # print json.dumps(print_object(result))
 
        # 记录测试结果
        case["case_type"] = action_type
        if result.metadata.bce_errmsg == 'Success':
            case["case_status"] = "pass"
        else:
            case["case_status"] = "false"
            case["detail"] = result
        global case_result_list
        case_result_list.append(case)
        return
 
    # 密钥管理-加密数据
    def encrypt_key(self, masterKey, plainText, key_type, action_type):
        case = {"case_name": "encrypt_key :" + key_type}
        print("%s: %s : start encrypt_key test ... " % (action_type, key_type))
        # print "master key:", masterKey
        # print "plain text:", plainText
        plaintext = base64.b64encode(plainText)
        result = kmsClient.encrypt(masterKey, plaintext)
 
        # 记录测试结果
        case["case_type"] = action_type
        if result.metadata.bce_errmsg == 'Success':
            case["case_status"] = "pass"
            Python2SDKSample.tmp_result["CipherText"] = str(result.ciphertext)
        else:
            case["case_status"] = "false"
            case["detail"] = result
        global case_result_list
        case_result_list.append(case)
        return
 
    # 密钥管理-解密数据
    @staticmethod
    def decrpyt_key(masterKey, cipherText, key_type, action_type):
        case = {"case_name": "decrpyt_key"}
        print("%s: %s : start decrpyt_key test ... " % (action_type, key_type))
        result = kmsClient.decrypt(masterKey, cipherText)
        #print result.plaintext
 
        # 记录测试结果
        case["case_type"] = action_type
        if result.metadata.bce_errmsg == 'Success':
            case["case_status"] = "pass"
        else:
            case["case_status"] = "false"
            case["detail"] = result
        global case_result_list
        case_result_list.append(case)
        return
 
    # 密钥管理-生成DataKey
    def create_data_key(self, masterKey, dataKey_len, key_type, action_type):
        case = {"case_name": "create_data_key:" + key_type}
        print("%s: %s : start ceate_data_key test ... " % (action_type, key_type))
        if key_type == "AES_256":
            result = kmsClient.generate_dataKey(masterKey, keyspec_class.AES_256, dataKey_len)
        if key_type == "AES_128":
            result = kmsClient.generate_dataKey(masterKey, keyspec_class.AES_128, dataKey_len)
 
        # 记录测试结果
        case["case_type"] = action_type
        if result.metadata.bce_errmsg == 'Success':
            case["case_status"] = "pass"
        else:
            case["case_status"] = "false"
            case["detail"] = result
        global case_result_list
        case_result_list.append(case)
        return
 
    # 密钥管理-使MasterKey处于可用状态
    def enable_master_key(self, masterKey, key_type, action_type):
        case = {"case_name": "enable_master_key:" + key_type}
        print("%s: %s : start enable_master_key test ... " % (action_type, key_type))
        result = kmsClient.enable_masterKey(masterKey)
        # print result
 
        # 记录测试结果
        case["case_type"] = action_type
        if result.metadata.bce_errmsg == 'Success':
            case["case_status"] = "pass"
        else:
            case["case_status"] = "false"
            case["detail"] = result
        global case_result_list
        case_result_list.append(case)
        return
 
    # 密钥管理-使MasterKey处于不可用状态
    def disable_master_key(self, masterKey, key_type, action_type):
        case = {"case_name": "disable_master_key:" + key_type}
        print("%s: %s : start disable_master_key test ... " % (action_type, key_type))
        result = kmsClient.disable_masterKey(masterKey)
 
        # 记录测试结果
        case["case_type"] = action_type
        if result.metadata.bce_errmsg == 'Success':
            case["case_status"] = "pass"
        else:
            case["case_status"] = "false"
            case["detail"] = result
        global case_result_list
        case_result_list.append(case)
        return
 
    # 密钥管理-删除MasterKey
    def del_master_key(self, masterKey, scheduleDays, key_type, action_type):
        case = {"case_name": "del_master_key:" + key_type}
        print("%s: %s : start del_master_key test ... " % (action_type, key_type))
        result = kmsClient.scheduleDelete_masterKey(masterKey, scheduleDays)
 
        # 记录测试结果
        case["case_type"] = action_type
        if result.metadata.bce_errmsg == 'Success':
            case["case_status"] = "pass"
        else:
            case["case_status"] = "false"
            case["detail"] = result
        global case_result_list
        case_result_list.append(case)
        return
 
    # 密钥管理-取消删除MasterKey
    def cancle_master_key(self, masterKey, key_type, action_type):
        case = {"case_name": "cancle_master_key:" + key_type}
        print("%s: %s : start cancle_master_key test ... " % (action_type, key_type))
        result = kmsClient.cancelDelete_maaterKey(masterKey)
 
        # 记录测试结果
        case["case_type"] = action_type
        if result.metadata.bce_errmsg == 'Success':
            case["case_status"] = "pass"
        else:
            case["case_status"] = "false"
            case["detail"] = result
        global case_result_list
        case_result_list.append(case)
        return
 
    # 密钥管理-获取导入密钥参数
    def get_param_list(self, masterKey, key_type, action_type):
        case = {"case_name": "get_param_list"}
        print("%s: %s : start get_param_list test ... " % (action_type, key_type))
        publicKeyEncoding = publickeyencoding_class.PEM
        result = kmsClient.get_parameters_for_import(masterKey, publicKeyEncoding)
        # print "public_key:", result.public_key
        # print "import token:", result.import_token
 
        # 记录测试结果
        case["case_type"] = action_type
        if result.metadata.bce_errmsg == 'Success':
            case["case_status"] = "pass"
            Python2SDKSample.tmp_result["token"] = str(result.import_token)
            Python2SDKSample.tmp_result["encrypt_public_key"] = str(result.public_key)
        else:
            case["case_status"] = "false"
            case["detail"] = result
        global case_result_list
        case_result_list.append(case)
        return
 
    # 密钥管理-导入对称密钥
    @staticmethod
    def import_symmetric_key(masterKey, key_type, action_type):
        case = {"case_name": "import_symmetric_key"}
        print("%s: %s : start import_symmetric_key test ... " % (action_type, key_type))
        if key_type == "AES_128":
            # 128/8 = 16byte
            aeskey = "1122334455667788"
            #print "customer 128 AES key:", aeskey
        if key_type == "AES_256":
            # 256/8 = 32byte
            aeskey = "12345678901234567890123456789012"
            #print "customer 256 AES key:", aeskey
        # create import parameter for PEM temporary
        get_result = kmsClient.get_parameters_for_import(masterKey, publickeyencoding_class.PEM)
        # get token
        importToken = str(get_result.import_token)
        # get encrypted key with public key with base64
        pubKey = str(get_result.public_key)
        rsa_pubKey = RSA.importKey(pubKey)
        cipher = PKCS1_v1_5.new(rsa_pubKey)
        encryptedKey = base64.b64encode(cipher.encrypt(aeskey))
        if key_type == "AES_128":
            result = kmsClient.import_symmetricMasterKey(masterKey, importToken, encryptedKey, keySpec="AES_128")
        if key_type == "AES_256":
            result = kmsClient.import_symmetricMasterKey(masterKey, importToken, encryptedKey, keySpec="AES_256")
 
        # 记录测试结果
        case["case_type"] = action_type
        if result.metadata.bce_errmsg == 'Success':
            case["case_status"] = "pass"
        else:
            case["case_status"] = "false"
            case["detail"] = result
        global case_result_list
        case_result_list.append(case)
        return
 
    def formatRSA_pkey(self, key):
        str_key = hex(key)[2:-1]
        if len(str_key) % 2 != 0:
            key = ("0" + str_key).decode("hex")
        else:
            key = str_key.decode("hex")
        return key
 
    # 密钥管理-导入非对称密钥
    def import_asymmetric_key(self, masterKey, asymmetricKeySpec, action_type):
        case = {"case_name": "import_asymmetric_key"}
        print("%s: %s: start import_asymmetric_key test ... " % (action_type, asymmetricKeySpec))
 
        # 获取import Token
        importToken = Python2SDKSample.tmp_result["token"]
 
        # 获取加密公钥
        KMS_public_key = Python2SDKSample.tmp_result["encrypt_public_key"]
        rsa_pubKey = RSA.importKey(KMS_public_key)
        cipher = PKCS1_v1_5.new(rsa_pubKey)
 
        # 随机生成一个用户的RSA密钥
        # 生成iv偏移量，必须是16的倍数，即2字节的倍数
        random_generator = Random.new().read
        if asymmetricKeySpec == "RSA_1024":
            rsa = RSA.generate(1024, random_generator)
        if asymmetricKeySpec == "RSA_2048":
            rsa = RSA.generate(2048, random_generator)
        if asymmetricKeySpec == "RSA_4096":
            rsa = RSA.generate(4096, random_generator)
        #print "rsa export key:", rsa.exportKey()
        der = DerSequence()
        der.append(rsa.n)
        der.append(rsa.e)
 
        # RSA 公钥
        pub_key = base64.b64encode(der.encode())
 
        # RSA 6个私钥分量
        D = self.formatRSA_pkey(rsa.d)
        P = self.formatRSA_pkey(rsa.p)
        Q = self.formatRSA_pkey(rsa.q)
        Dp = self.formatRSA_pkey(rsa.d % (rsa.p - 1))
        Dq = self.formatRSA_pkey(rsa.d % (rsa.q - 1))
        Qinv = self.formatRSA_pkey(self.findModReverse(rsa.q, rsa.p))
 
        # customer's AES_128 key
        aeskey = "1122334455667788"
 
        # 使用用户的AES 128的密钥对RSA的6个私钥分量进行加密
        aes_obj = AES.new(aeskey, AES.MODE_ECB)
        D_b64 = base64.b64encode(aes_obj.encrypt(D))
        P_b64 = base64.b64encode(aes_obj.encrypt(P))
        Q_b64 = base64.b64encode(aes_obj.encrypt(Q))
        Dp_b64 = base64.b64encode(aes_obj.encrypt(Dp))
        Dq_b64 = base64.b64encode(aes_obj.encrypt(Dq))
        Qinv_b64 = base64.b64encode(aes_obj.encrypt(Qinv))
 
        # 用KMS生成的RSA密钥加密用户的128位非对称密钥，生成信封密钥
        encryptedKeyEncryptionKey = base64.b64encode(cipher.encrypt(aeskey))
 
        # create envelope cipher with
        result = kmsClient.import_asymmetricMasterKey(masterKey, importToken, asymmetricKeySpec,
                                                      encryptedKeyEncryptionKey,
                                                      asymmetricKeyUsage="ENCRYPT_DECRYPT",
                                                      publicKeyDer=pub_key,
                                                      encryptedD=D_b64,
                                                      encryptedP=P_b64,
                                                      encryptedQ=Q_b64,
                                                      encryptedDp=Dp_b64,
                                                      encryptedDq=Dq_b64,
                                                      encryptedQinv=Qinv_b64)
 
        # 记录测试结果
        case["case_type"] = action_type
        if result.metadata.bce_errmsg == 'Success':
            case["case_status"] = "pass"
        else:
            case["case_status"] = "false"
            case["detail"] = result
        global case_result_list
        case_result_list.append(case)
        return
 
if __name__ == "__main__":
    # 运行前请设置Client的Host，Access Key ID和Secret Access Key
    # online bdbl-fsg env
    # 设置日志文件的句柄和日志级别
    logger = logging.getLogger('baidubce.services.kms.kmsclient')
    fh = logging.FileHandler("sample.log")
    fh.setLevel(logging.DEBUG)
    # 设置日志文件输出的顺序、结构和内容
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    kmsClient = kms_client.KmsClient(kms_sample_conf.config)
    sample = Python2SDKSample()
    # 支持的加密方式
    cipher_type_list = ["BAIDU_AES_256", "AES_128", "AES_256", "RSA_1024", "RSA_2048", "RSA_4096"]
 
    # KMS生成方式用例
    for cipher in cipher_type_list:
        sample.KMS_create_suit(cipher)
 
    # external生成方式用例
    for cipher in cipher_type_list:
        if "BAIDU" not in cipher:
            sample.external_create_suit(cipher)
 
    # 显示整体测试结果
    pass_num = 0
    for case_result in case_result_list:
        print("case run result:", case_result)
        if case_result["case_status"] == "pass":
            pass_num = pass_num + 1
    print("total case:", len(case_result_list))
    print("passed case:", pass_num)