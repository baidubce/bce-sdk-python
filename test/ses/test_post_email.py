#!/usr/bin/env python
#coding:utf-8
"""
@author wanglinqing01@baidu.com
@date 2014/10/08
@brief post Email
"""

import os
import sys
import json
import time
import traceback

_NOW_PATH = os.path.dirname(os.path.abspath(__file__)) + '/'
_BCE_PATH = _NOW_PATH + '../'
sys.path.insert(0, _BCE_PATH)

import bes_base_case
from baidubce.services.ses import client
from baidubce.services.ses import exception as ses_exception
from baidubce import exception


class TestPostEmail(bes_base_case.BaseTest):
    def __init__(self):
        super(self.__class__, self).__init__()

    def setUp(self):
        time.sleep(1)

    def tearDown(self):
        pass

    #verified email:wanglinqing01@baidu.com, verified domain:126.com

    def test_post_email_normal(self):
        #print self.host
        cli = client.SesClient(self.host, self.ak, self.sk)
        email = 'wanglinqing01@baidu.com'
        attach_list = ['1']
        attach_list[0] = _NOW_PATH + 'bms_api_test.py'
        resp = cli.send_mail(mail_from=email, to_addr=["wanglinqing01@baidu.com"], cc_addr=["wanglinqing2010@126.com"], bcc_addr=["zhuimeng_2006jsj@126.com"], subject="test post email normal", text="test ses python sdk email normal", attachments=attach_list, priority=1)
        #print resp
        assert resp.status == 200, 'status is not 200'

    def test_post_email_attachmentPdf(self):
        #print self.host
        cli = client.SesClient(self.host, self.ak, self.sk)
        email = 'wanglinqing01@baidu.com'
        attach_list = ['1']
        attach_list[0] = _NOW_PATH + 'personal_plan.pdf'
        resp = cli.send_mail(mail_from=email, to_addr=["wanglinqing01@baidu.com", "zhangzheyuan@baidu.com"], subject="test post email pdf", text="test ses python sdk pdf", attachments=attach_list, priority=1)
        #print resp
        assert resp.status == 200, 'status is not 200'

    def test_post_email_attachmentPdfLongTitle(self):
        cli = client.SesClient(self.host, self.ak, self.sk)
        email = 'wanglinqing01@baidu.com'
        attach_list = ['1']
        attach_list[0] = _NOW_PATH + 'personal_plan_personal_plan_personal_plan_personal_plan_personal_plan.pdf'
        resp = cli.send_mail(mail_from=email, to_addr=["wanglinqing01@baidu.com"], subject="test post email pdf long title", text="test ses python sdk pdf long title", attachments=attach_list, priority=1)
        assert resp.status == 200, 'status is not 200'

    def test_post_email_attachmentTxt(self):
        #print self.host
        cli = client.SesClient(self.host, self.ak, self.sk)
        email = 'wanglinqing01@baidu.com'
        attach_list = ['1']
        attach_list[0] = _NOW_PATH + 'bes_sdk_test.txt'
        resp = cli.send_mail(mail_from=email, to_addr=["wanglinqing01@baidu.com"], subject="test post email txt", text="test ses python sdk txt", attachments=attach_list, priority=1)
        #print resp
        assert resp.status == 200, 'status is not 200'

    def test_post_email_attachmentDoc(self):
        #print self.host
        cli = client.SesClient(self.host, self.ak, self.sk)
        email = 'wanglinqing01@baidu.com'
        attach_list = ['1']
        attach_list[0] = _NOW_PATH + 'ses_api_v1.7.docx'
        resp = cli.send_mail(mail_from=email, to_addr=["wanglinqing01@baidu.com"], subject="test post email doc", text="test ses python sdk doc", attachments=attach_list, priority=1)
        #print resp
        assert resp.status == 200, 'status is not 200'

    def test_post_email_ChineseSubject(self):
        cli = client.SesClient(self.host, self.ak, self.sk)
        email = 'wanglinqing01@baidu.com'
        resp = cli.send_mail(mail_from=email, to_addr=["wanglinqing01@baidu.com"], subject="我是中文主题邮件", text="测试中文主题")
        assert resp.status == 200, 'status is not 200'

    def test_post_email_onlyCc(self):
        #print self.host
        cli = client.SesClient(self.host, self.ak, self.sk)
        email = 'wanglinqing01@baidu.com'
        resp = cli.send_mail(mail_from=email, cc_addr=["wanglinqing2010@126.com"], subject="test post email only CC_addr", text=" email only cc_addr")
        assert resp.status == 200, 'status is not 200'

    def test_post_email_onlyBcc(self):
        #print self.host
        cli = client.SesClient(self.host, self.ak, self.sk)
        email = 'wanglinqing01@baidu.com'
        resp = cli.send_mail(mail_from=email, bcc_addr=["wanglinqing01@baidu.com"], subject="test post email only bcc_addr", text=" email only bcc_addr")
        assert resp.status == 200, 'status is not 200'

    def test_post_email_emptyAttachments(self):
        #print self.host
        cli = client.SesClient(self.host, self.ak, self.sk)
        email = 'wanglinqing01@baidu.com'
        resp = cli.send_mail(mail_from=email, to_addr=["wanglinqing01@baidu.com"], subject="test post email without attachments", text="test ses python sdk without attachments")
        #print resp
        assert resp.status == 200, 'status is not 200'

    def test_post_email_emptySender(self):
        cli = client.SesClient(self.host, self.ak, self.sk)
        flag = False
        try:
            resp = cli.send_mail("''", to_addr=['wanglinqing01@baidu.com'])
        except exception.ServerError as e:
            flag = True
            print "it have an exception"
            tracemsg = traceback.format_exc()
            print e
        finally:
            assert flag == True, 'it should throw exception'

    def test_post_email_emptyReceiver(self):
        cli = client.SesClient(self.host, self.ak, self.sk)
        flag = False
        try:
            resp = cli.send_mail('wanglinqing01@baidu.com', subject="test post email, no receiver", text="test ses python sdk, no receiver")
        except ses_exception.InvalidParam as e:
            flag = True
            print "it have an exception"
            tracemsg = traceback.format_exc()
            print e
        finally:
            assert flag == True, 'it should throw exception'

    def test_post_email_receiverFormatInvalid(self):
        cli = client.SesClient(self.host, self.ak, self.sk)
        flag = False
        try:
            resp = cli.send_mail('wanglinqing01@baidu.com', to_addr=['wanglinqing01'], subject="test post email, receiver format invalid", text="test ses python sdk, receiver format invalid")
        except exception.ServerError as e:
            flag = True
            print "it have an exception"
            tracemsg = traceback.format_exc()
            print e
        finally:
            assert flag == True, 'it should throw exception'

    def test_post_email_senderNotVerified(self):
        cli = client.SesClient(self.host, self.ak, self.sk)
        flag = False
        try:
            resp = cli.send_mail('wanglinqingtest@baidu.com', to_addr=['wanglinqing01@baidu.com'], subject="test post email, sender not verified", text="test ses python sdk, sender not verified")
        except exception.ServerError as e:
            flag = True
            print "it have an exception"
            tracemsg = traceback.format_exc()
            print e
        finally:
            assert flag == True, 'it should throw exception'

    def test_post_email_senderDomainNotVerified(self):
        cli = client.SesClient(self.host, self.ak, self.sk)
        flag = False
        try:
            resp = cli.send_mail('wanglinqing2013@163.com', to_addr=['wanglinqing01@baidu.com'], subject="test post email, senderDomain not verified", text="test ses python sdk, senderDomain not verified")
        except exception.ServerError as e:
            flag = True
            print "it have an exception"
            tracemsg = traceback.format_exc()
            print e
        finally:
            assert flag == True, 'it should throw exception'

    def test_post_email_senderFormatNotVerified(self):
        cli = client.SesClient(self.host, self.ak, self.sk)
        flag = False
        try:
            resp = cli.send_mail('wanglinqing01', to_addr=['wanglinqing01@baidu.com'], subject="test post email, sender format not valid", text="test ses python sdk, sender format not valid")
        except exception.ServerError as e:
            flag = True
            print "it have an exception"
            tracemsg = traceback.format_exc()
            print e
        finally:
            assert flag == True, 'it should throw exception'

    def test_post_email_emptySubject(self):
        cli = client.SesClient(self.host, self.ak, self.sk)
        flag = False
        try:
            resp = cli.send_mail('wanglinqing01@baidu.com', to_addr=['wanglinqing01@baidu.com'], text="test ses python sdk, subject empty")
        except exception.ServerError as e:
            flag = True
            print "it have an exception"
            tracemsg = traceback.format_exc()
            print e
        finally:
            assert flag == True, 'it should throw exception'

    def test_post_email_moreReceiver(self):
        cli = client.SesClient(self.host, self.ak, self.sk)
        resp = cli.send_mail('wanglinqing01@baidu.com', 
                to_addr=['wanglinqing01@baidu.com', 'wanglinqing2010@126.com'], 
                subject="test post email, more receiver", 
                text="test ses python sdk, more receiver")
        assert resp.status == 200, 'status is not 200'

    def test_post_email_receiverDuplicate(self):
        cli = client.SesClient(self.host, self.ak, self.sk)
        resp = cli.send_mail('wanglinqing01@baidu.com', 
                to_addr=['wanglinqing01@baidu.com', 'wanglinqing01@baidu.com'], 
                subject="test post email, receiver duplicate", 
                text="test ses python sdk, receiver duplicate")
        assert resp.status == 200, 'status is not 200'

    def test_post_email_longTitle(self):
        cli = client.SesClient(self.host, self.ak, self.sk)
        resp = cli.send_mail('wanglinqing01@baidu.com', to_addr=['wanglinqing01@baidu.com'], subject="test post email long title long title long title long title long title long title long title long title long title long title long title long title long title long title", text="test ses python sdk, receiver duplicate")
        assert resp.status == 200, 'status is not 200'

    def test_post_email_domainVerified(self):
        cli = client.SesClient(self.host, self.ak, self.sk)
        resp = cli.send_mail('wanglinqing2010@126.com', to_addr=['wanglinqing01@baidu.com'], subject="test post email, sender not verified but domain verified", text="test ses python sdk,  sender not verified but domain verified")
        assert resp.status == 200, 'status is not 200'

    def test_post_email_noParam(self):
        cli = client.SesClient(self.host, self.ak, self.sk)
        flag = False
        try:
            resp = cli.send_mail()
        except ses_exception.InvalidParam as e:
            flag = True
            print "it have an exception"
            tracemsg = traceback.format_exc()
            print e
        finally:
            assert flag == True, 'it should throw exception'

    def test_post_email_htmlFormat(self):
        cli = client.SesClient(self.host, self.ak, self.sk)
        resp = cli.send_mail('wanglinqing2010@126.com', to_addr=['wanglinqing01@baidu.com'], subject="test post email, html format", html='<html><body><div><h3  align=\"center\">资源总数统计</h3><table border=\"1\" cellpadding=\"0\" cellspacing=\"0\" width=\"80%\" align=\"center\"> <tr><th bgColor=\"426ab3\">type</th><th bgColor=\"426ab3\">count</th></tr><tr> <td align=\"center\" bgColor=\"#9b95c9\">BCC云主机</td><td align=\"center\"  bgColor=\"#9b95c9\">15</td></tr><tr> <td align=\"center\" bgColor=\"#9b95c9\">RDS关系型数据库</td><td align=\"center\"  bgColor=\"#9b95c9\">15</td></tr><tr> <td align=\"center\" bgColor=\"#867892\">SCS缓存服务</td><td align=\"center\"  bgColor=\"#867892\">15</td></tr><tr> <td align=\"center\" bgColor=\"#fab27b\">BOS对象存储服务</td><td align=\"center\"  bgColor=\"#fab27b\">15</td></tr><tr> <td align=\"center\" bgColor=\"#c88400\">BMR百度MapReduce</td><td align=\"center\"  bgColor=\"#c88400\">15</td></tr><tr> <td align=\"center\" bgColor=\"#b7ba6b\">CDN服务</td><td align=\"center\"  bgColor=\"#b7ba6b\">15</td></tr><tr> <td align=\"center\" bgColor=\"#769149\">SES邮件服务</td><td align=\"center\"  bgColor=\"#769149\">15</td></tr><tr> <td align=\"center\" bgColor=\"#78a355\">SMS短信服务</td><td align=\"center\"  bgColor=\"#78a355\">15</td></tr></table></div><div><h3  align=\"center\">资源数量top10用户统计</h3><table border=\"1\" cellpadding=\"0\" cellspacing=\"0\" width=\"100%\" align=\"center\"> <tr><th bgColor=\"426ab3\">type</th><th bgColor=\"426ab3\">iam_account_id</th> <th bgColor=\"426ab3\">count</th></tr><tr> <td align=\"center\" bgColor=\"#9b95c9\">BCC云主机</td><td align=\"center\"  bgColor=\"#9b95c9\">dcf5a8476ba443988322ed577d67b8ef</td><td align=\"center\"  bgColor=\"#9b95c9\"> 10</td></tr><tr> <td align=\"center\" bgColor=\"#9b95c9\">BCC云主机</td><td align=\"center\"  bgColor=\"#9b95c9\">dcf5a8476ba443988322ed577d67b8ef</td><td align=\"center\"  bgColor=\"#9b95c9\"> 10</td></tr><tr> <td align=\"center\" bgColor=\"#9b95c9\">BCC云主机</td><td align=\"center\"  bgColor=\"#9b95c9\">1734317d-40c6-4950-b1f1-f45393970f63</td><td align=\"center\"  bgColor=\"#9b95c9\"> 9</td></tr><tr> <td align=\"center\" bgColor=\"#9b95c9\">BCC云主机</td><td align=\"center\"  bgColor=\"#9b95c9\">bbe13106ecaa4a9aa73188720f0e1193</td><td align=\"center\"  bgColor=\"#9b95c9\"> 6</td></tr><tr> <td align=\"center\" bgColor=\"#9b95c9\">BCC云主机</td><td align=\"center\"  bgColor=\"#9b95c9\">33ee9b2d-228b-42c2-aae5-b1f1841374fb</td><td align=\"center\"  bgColor=\"#9b95c9\"> 6</td></tr><tr> <td align=\"center\" bgColor=\"#867892\">SCS缓存服务</td><td align=\"center\"  bgColor=\"#867892\">0a784fe6cc4d49879b882645023aaa73</td><td align=\"center\"  bgColor=\"#867892\"> 10</td></tr><tr> <td align=\"center\" bgColor=\"#867892\">SCS缓存服务</td><td align=\"center\"  bgColor=\"#867892\">dcf5a8476ba443988322ed577d67b8ef1</td><td align=\"center\"  bgColor=\"#867892\"> 10</td></tr><tr> <td align=\"center\" bgColor=\"#867892\">SCS缓存服务</td><td align=\"center\"  bgColor=\"#867892\">1734317d-40c6-4950-b1f1-f45393970f63</td><td align=\"center\"  bgColor=\"#867892\"> 7</td></tr><tr> <td align=\"center\" bgColor=\"#867892\">SCS缓存服务</td><td align=\"center\"  bgColor=\"#867892\">bbe13106ecaa4a9aa73188720f0e1193</td><td align=\"center\"  bgColor=\"#867892\"> 5</td></tr><tr> <td align=\"center\" bgColor=\"#867892\">SCS缓存服务</td><td align=\"center\"  bgColor=\"#867892\">33ee9b2d-228b-42c2-aae5-b1f1841374fb</td><td align=\"center\"  bgColor=\"#867892\"> 5</td></tr><tr> <td align=\"center\" bgColor=\"#fab27b\">BOS对象存储服务</td><td align=\"center\"  bgColor=\"#fab27b\">bbe13106ecaa4a9aa73188720f0e1193</td><td align=\"center\"  bgColor=\"#fab27b\"> 5</td></tr><tr> <td align=\"center\" bgColor=\"#fab27b\">BOS对象存储服务</td><td align=\"center\"  bgColor=\"#fab27b\">bbe13106ecaa4a9aa73188720f0e1193</td><td align=\"center\"  bgColor=\"#fab27b\"> 5</td></tr><tr> <td align=\"center\" bgColor=\"#fab27b\">BOS对象存储服务</td><td align=\"center\"  bgColor=\"#fab27b\">bbe13106ecaa4a9aa73188720f0e1193</td><td align=\"center\"  bgColor=\"#fab27b\"> 5</td></tr><tr> <td align=\"center\" bgColor=\"#b7ba6b\">CDN服务</td><td align=\"center\"  bgColor=\"#b7ba6b\">bbe13106ecaa4a9aa73188720f0e1193</td><td align=\"center\"  bgColor=\"#b7ba6b\"> 5</td></tr><tr> <td align=\"center\" bgColor=\"#b7ba6b\">CDN服务</td><td align=\"center\"  bgColor=\"#b7ba6b\">bbe13106ecaa4a9aa73188720f0e1193</td><td align=\"center\"  bgColor=\"#b7ba6b\"> 5</td></tr><tr> <td align=\"center\" bgColor=\"#b7ba6b\">CDN服务</td><td align=\"center\"  bgColor=\"#b7ba6b\">bbe13106ecaa4a9aa73188720f0e1193</td><td align=\"center\"  bgColor=\"#b7ba6b\"> 5</td></tr><tr> <td align=\"center\" bgColor=\"#769149\">SES邮件服务</td><td align=\"center\"  bgColor=\"#769149\">bbe13106ecaa4a9aa73188720f0e1193</td><td align=\"center\"  bgColor=\"#769149\"> 5</td></tr><tr> <td align=\"center\" bgColor=\"#769149\">SES邮件服务</td><td align=\"center\"  bgColor=\"#769149\">bbe13106ecaa4a9aa73188720f0e1193</td><td align=\"center\"  bgColor=\"#769149\"> 5</td></tr></table></div></body></html>')
        assert resp.status == 200, 'status is not 200'
