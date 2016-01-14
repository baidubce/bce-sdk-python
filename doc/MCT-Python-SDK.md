# Media SDK for Python

# 简介

本文档主要介绍Media Python SDK的安装和使用。在使用本文档前，您需要先了解音视频转码的一些基本知识，并已开通了音视频转码服务。若您还不了解音视频转码，可以参考[产品描述](ProductDescription.html)和[入门指南](GettingStarted_new.html)。

# 安装Media SDK for Python

**运行环境**

Python SDK工具包支持在Python 2.7环境下运行。


## 安装步骤

1. 在[官方网站](http://bce.baidu.com/doc/SDKTool/index.html)下载Media Python SDK（ZIP包）。

2. 进入下载目录，解压缩。

3. 找到README.txt文件，在该目录下运行安装命令，即可以使用SDK包：


	python setup.py install


关于配置文件的引用请参考下文中的[配置MediaClient](# 配置MediaClient)。

## SDK目录结构

	baidubce
	       ├── auth                    //公共权限目录
	       ├── services                //服务公共目录
	       │   └── media              //media目录
	       └── http                    //Http请求模块


#	快速入门

1.初始化一个MediaClient。

MediaClient是与Media服务交互的客户端，所有Media操作都是通过MediaClient完成的。用户可以参考[新建MediaClient](# 新建MediaClient)，完成初始化客户端的操作。

2.新建一个Pipeline(任务队列)。

通过Pipeline，用户可以更灵活地管理转码任务。当用户创建一个Job(任务)时，用户必须指定一个队列。

用户在创建队列时，需要为队列指定队列的名称、队列的类型（免费型或私有型）、一组源多媒体资源所属的Bucket与目标多媒体资源所属的的Bucket。输入和输出的Bucket可以是不同的。

3.查看Preset(多媒体模板)

查看系统预设的多媒体模板。模板是一个视频资源在做转码计算时所需参数的集合。用户可以更简便的将一个模板应用于一个和多个视频的转码任务，以使这些任务输出相同规格的目标多媒体资源。

音视频转码为用户预设了丰富且完备的系统模板，以满足用户对于目标规格在格式、码率、分辨率、加解密、水印等诸多方向上的普遍需求，对于不希望过多了解音视频复杂技术背景的用户来说，是最佳的选择。

4.新建一个Job(任务)。

创建一个Job执行多媒体转码任务。每个任务将一个原始的多媒体资源转码成目标规格的多媒体资源。因此，任务和转码的目标是一一对应的，也就是说如果用户需要将一个原始视频规格转换成三种目标规格，比如从AVI格式转码成FLV/MP4/HLS格式，那么用户将会需要创建三个任务。

用户在创建任务时，需要为任务指定所属的队列、所需应用的转码模板以及原始音视频资源的BOS Key以及目标音视频资源BOS Key。

5.查询指定Object多媒体格式信息

用户通过BOS Bucket+Key获取指定多媒体文件的媒体信息。

# MediaClient

## 配置MediaClient

MediaClient是Media服务的Python客户端，为调用者与Media服务进行交互提供了一系列的方法。

在新建MediaClient之前，需要先创建配置文件对MediaClient进行配置，以下将此配置文件命名为`conf.py`，具体配置信息如下所示：


	#!/usr/bin/env python
	#coding=utf-8
	
	#导入Python标准日志模块
	import logging
	
	#从Python SDK导入Media配置管理模块以及安全认证模块
	from baidubce.bce_client_configuration import BceClientConfiguration
	from baidubce.auth.bce_credentials import BceCredentials
	
	#设置MediaClient的Host，Access Key ID和Secret Access Key
	media_host = "http://media.bj.baidubce.com"
	access_key_id = "your-access-key-id"
	secret_access_key = "your-secret-access-key"
	
	#设置日志文件的句柄和日志级别
	logger = logging.getLogger('baidubce.services.media.mediaclient')
	fh = logging.FileHandler("sample.log")
	fh.setLevel(logging.DEBUG)
	
	#设置日志文件输出的顺序、结构和内容
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	fh.setFormatter(formatter)
	logger.setLevel(logging.DEBUG)
	logger.addHandler(fh)
	
	#创建BceClientConfiguration
	config = BceClientConfiguration(credentials=BceCredentials(access_key_id, secret_access_key), endpoint = media_host)



注意：

1.在上面的代码中，变量AK与SK是系统分配给用户的，用于标识用户，为访问Media做签名验证。其中AK对应控制台中的“Access Key ID”，SK对应控制台中的“Access Key Secret”，获取方式请参考《操作指南 [管理ACCESSKEY](../BOS/GettingStarted.html#管理ACCESSKEY)》。

2.ENDPOINT参数只能用指定的包含Region的域名来进行定义，目前Media只提供北京一个Region，因此ENDPOINT只支持` http://media.bj.baidubce.com `这一个域名，随着Region的增加将会开放其他可以支持的域名。

## 新建MediaClient

在完成上述配置之后，参考如下代码新建一个MediaClient。


	import conf
	import sys
	from baidubce import exception
	from baidubce.services import media
	from baidubce.services.media.media_client import MediaClient
	
	# create new MediaClient
	client = MediaClient(conf.config)
	reload(sys)
	sys.setdefaultencoding('utf-8')
	print client.list_pipelines()



## 参数说明
Python SDK在`baidubce\bce_client_configuration.py`中默认设置了一些基本参数，若用户想要对参数的值进行修改，可以参考此文件创建自身的参数配置函数，并在构造MediaClient的时候传入，传入代码参考如下：


	from baidubce.retry_policy import BackOffRetryPolicy
	from baidubce.bce_client_configuration import BceClientConfiguration
	from baidubce.auth.bce_credentials import BceCredentials
	from baidubce.protocol import HTTP
	from baidubce.region import BEIJING
	
	my_policy = BackOffRetryPolicy(max_error_retry = 3,
	        max_delay_in_millis=20 * 1000,
		    base_interval_in_millis=300)
	
	my_config = BceClientConfiguration(
	        credentials = BceCredentials('your-access-key-id', 'your-secret-access-key'),
			endpoint = media_host,
			protocol = baidubce.protocol.HTTP,
			region = baidubce.region.BEIJING,
			connection_timeout_in_mills = 50 * 1000,
			send_buf_size = 1024 * 1024,
			recv_buf_size = 10 * 1024 * 1024,
			retry_policy = my_policy)
	
	
	# create MediaClient with my config
	my_client = MediaClient(my_config)
	
	pipelines = client.list_pipelines()
	for pipeline in pipelines.pipelines:
	  print pipeline



参数说明如下：

参数 | 说明 | 默认值
---|---|---
PROTOCOL | 协议 | baidubce.protocol.HTTP
REGION | 区域 | baidubce.region.BEIJING（目前只支持北京地区）
CONNECTION_TIMEOUT_IN_MILLIS | 请求超时时间（单位：毫秒） | 120 * 1000
SOCKET_TIMEOUT_IN_MILLIS | 通过打开的连接传输数据的超时时间（单位：毫秒） | 300 * 1000（0指的是无限等待，若设置非0数值需要对文件大小和网速进行评估，否则上传大文件时会产生超时）
SEND_BUF_SIZE | 发送缓冲区大小 | 5 * 1024 * 1024
RECV_BUF_SIZE | 接收缓冲区大小 | 5 * 1024 * 1024
retry_policy | 重试逻辑 | 最大重试次数3次, 超时时间为20 * 1000毫秒，重试间隔300毫秒

## 相关说明

MediaClient将可选的参数封装到`config`中，每一个方法具有的可选参数详见具体的接口使用方法介绍，现以`create_pipeline`方法为例，参考如下代码实现设置可选参数：


	#利用options在通过创建Pipeline传入指定可选参数
	my_config = BceClientConfiguration(
	        credentials = BceCredentials('your-access-key-id', 'your-secret-access-key'),
			endpoint = media_host,
			send_buf_size = 5 * 1024 * 1024)
	client.create_pipeline('your_pipeline', 'your_source_bucket', 'your_source_bucket', config=my_config);


# Pipeline（队列）

队列分为免费型与私有型：

* 免费型队列中的转码任务分享百度开放云为音视频转码所提供的约400路720P转码计算资源。
* 私有型队列需额外采购，以便更好的满足那些对于转码时效性和稳定性有更高要求的用户的业务需求。

用户可以利用队列实现任务优先级。用户通过创建多个队列达到区分任务优先级的目的，将大部分任务创建至普通优先级队列，将高优的任务放入高优先级的队列，以利用队列先到先服务的工作原理来实现任务的优先级调整。

## 新建Pipeline

如下代码可以新建一个Pipeline，默认的capacity值为20：


	pipeline_name = "your_pipeline";
	source_bucket = "your_source_bucket";
	target_bucket = "your_target_bucket";
	# create a new pipeline
	client.create_pipeline(pipeline_name, source_bucket, target_bucket);


## 列出全部Pipeline

如下代码可以列出用户所有的Pipeline：



	response = client.list_pipelines()
	for pipeline in response.pipelines:
	  print pipeline



## 查询指定的Pipeline
若只是查询某个Pipeline，则使用如下代码：


	pipeline_name = "your_pipeline"
	response = client.get_pipeline(pipeline_name)
	print response



## 删除Pipeline
如下代码可以删除一个Pipeline：


	pipeline_name = "your_pipeline"
	response = client.delete_pipeline(pipeline_name)
	print response



需要注意的是，如果Pipeline有关联的Job未完成，则Pipeline无法被删除，必须等Job执行结束后才能成功删除。


# Job（任务）

Job(任务)是音视频转码中最基本的执行单元，每个任务将一个原始的音视频资源转码成目标规格的音视频资源。因此，任务和转码的目标是一一对应的，也就是说如果用户需要将一个原始多媒体文件转换成三种目标规格，比如从AVI格式转码成FLV/MP4/HLS格式，那么用户将会需要创建三个任务。

## 创建Job


用户在创建任务时，需要为任务指定所属的Pipeline、所需应用的Preset以及原始音视频资源的BOS Key以及目标音视频资源BOS Key。

如下代码创建一个Job, 并获取新创建的jobID：


	pipeline_name = "your_pipeline"
	source = {'sourceKey': 'your_source_key'}
	target = {'targetKey': 'your_target_key', 'presetName': 'your_preset'}		
	response = client.create_job(pipeline_name, source, target)
	print response


## 列出指定Pipeline的所有Job

如下代码通过指定pipelineName查询该Pipeline下的所有Job：


	pipeline_name = "your_pipeline"
	response = client.list_jobs(pipeline_name)
	for job in response.jobs:
	  print job



## 查询指定的Job信息

用户可以通过如下代码通过jobId读取某个Job：


	job_id = "your_job"
	response = client.get_job(job_id)
	print response


# Preset(模板)

模板是系统预设的对于一个视频资源在做转码计算时所需定义的集合。用户可以更简便的将一个模板应用于一个和多个视频的转码任务，以使这些任务输出相同规格的目标视频资源。

音视频转码为用户预设了丰富且完备的系统模板，以满足用户对于目标规格在格式、码率、分辨率、加解密、水印等诸多方向上的普遍需求，对于不希望过多了解音视频复杂技术背景的用户来说，是最佳的选择。百度为那些在音视频技术上有着丰富积累的用户，提供了可定制化的转码模板，以帮助他们满足复杂业务条件下的转码需求。

当用户仅需对于音视频的容器格式做变化时，百度提供Transmux模板帮助用户以秒级的延迟快速完成容器格式的转换，比如从MP4转换成HLS，而保持原音视频的属性不变。

## 查询当前用户Preset及所有系统Preset

用户可以通过如下代码查询所有的Preset：


	response = client.list_presets()
	
	for preset in response.presets:
	  print preset


## 查询指定的Preset信息
用户可以通过如下代码指定的某个Preset：


	preset_name = "your_preset"
	response = client.get_preset(preset_name)
	print response


## 创建Preset
如果系统预设的Preset无法满足用户的需求，用户可以自定义自己的Preset。根据不同的转码需求，可以使用不同的接口创建Preset。

### 创建仅支持容器格式转换的Preset
如下代码创建仅执行容器格式转换Preset：


	preset_name = "your_preset"
	container = "hls"
	response = client.create_preset(preset_name, container)
	print response


### 创建音频文件的转码Preset，不需要截取片段和加密
如果创建一个不需要截取片段和加密的音频文件转码Preset，可以参考如下代码：

	preset_name = "your_preset"
	container = "mp3"
	audio = {'bitRateInBps': 25600, 'sampleRateInHz': 32000, 'channels': 1}
	response = client.create_preset(preset_name, container, audio=audio)
	print response


### 创建音频文件转码Preset，需要设置片段截取属性和加密属性
如果创建一个支持截取片段和加密的音频文件转码Preset，可以参考如下代码：


	preset_name = "your_preset"
	container = "mp4"
	
	clip = {'startTimeInSecond':0, 'durationInSecond': 50}
	audio = {'bitRateInBps': 1980, 'sampleRateInHz': 32000, 'channels': 1}
	encryption = {'aesKey': 'abcdefghij123456','strategy': 'Fixed'}
	response = client.create_preset(preset_name, container, clip=clip, audio=audio, encryption=encryption)
	print response



### 创建视频文件转码Preset，不需要截取片段和加密
如果创建一个不需要截取片段和加密的音频文件转码Preset，可以参考如下代码：


	preset_name = "your_preset"
	container = "mp4"
	codecOptions = {'profile': 'baseline'}
	video = {
	    'codec': 'h264',
	    'codecOptions': codecOptions,
	    'bitRateInBps': 32000,
	    'maxFrameRate': 30,
	    'maxWidthInPixel': 4096,
	    'maxHeightInPixel': 96,
	    'sizingPolicy': 'stretch'
	}
	audio = {'bitRateInBps': 1980, 'sampleRateInHz': 32000, 'channels': 1}
	response = client.create_preset(preset_name, container, video=video, audio=audio)
	print response



### 创建视频文件转码Preset，需要设置片段截取属性和加密属性
如果创建一个截取片段和加密的音频文件转码Preset，可以参考如下代码：


	preset_name = "your_preset"
	container = "mp4"
	codecOptions = {'profile': 'baseline'}
	video = {
	    'codec': 'h264',
	    'codecOptions': codecOptions,
	    'bitRateInBps': 32000,
	    'maxFrameRate': 30,
	    'maxWidthInPixel': 4096,
	    'maxHeightInPixel': 96,
	    'sizingPolicy': 'stretch'
	}
	clip = {'startTimeInSecond':0, 'durationInSecond': 50}
	audio = {'bitRateInBps': 1980, 'sampleRateInHz': 32000, 'channels': 1}
	encryption = {'aesKey': 'abcdefghij123456','strategy': 'Fixed'}
	response = client.create_preset(preset_name, container, video=video, clip=clip, audio=audio, encryption=encryption)
	print response


### 创建Preset，指定所有的参数
如果需要定制所有配置参数，可以参考如下代码：


	preset_name = "your_preset"
	
	container = "mp4"
	desc = 'My Desc'
	transmux = True
	codecOptions = {'profile': 'baseline'}
	video = {
	    'codec': 'h264',
	    'codecOptions': codecOptions,
	    'bitRateInBps': 32000,
	    'maxFrameRate': 30,
	    'maxWidthInPixel': 4096,
	    'maxHeightInPixel': 96,
	    'sizingPolicy': 'stretch'
	}
	clip = {'startTimeInSecond':0, 'durationInSecond': 50}
	audio = {'bitRateInBps': 1980, 'sampleRateInHz': 32000, 'channels': 1}
	encryption = {'aesKey': 'abcdefghij123456','strategy': 'Fixed'}
	response = client.create_preset(preset_name, container, transmux=transmux, description=desc, video=video, clip=clip, audio=audio, encryption=encryption)
	print response



# Mediainfo(媒体信息)
对于BOS中某个Object，可以通过下面代码获其媒体信息：


	bucket = "your_bucket"
	key = "your_key"
	response = client.get_mediainfo_of_file(bucket, key)
	print response


# Thumbnail Job(缩略图任务)

## 创建缩略图任务
如果要创建一个缩略图任务，可以参考如下代码：


	pipeline_name = 'a3'
	source = {'key': '36A2014.mp4'}
	response = client.create_thumbnail_job(pipeline_name,  source)
	print response

接口返回的是包含了jobId的一个对象。

## 查询指定缩略图任务
如果需要获取一个已创建的缩略图任务的信息，可以参考如下代码：


	job_id = "your jobId"
	response = client.get_thumbnail_job(job_id)
	print response

## 查询指定队列的缩略图任务信息
如果需要获取一个队列里的全部缩略图任务的信息，可以参考如下代码：


	pipeline_name = "your pipeline"
	response = client.list_thumbnail_jobs_by_pipeline(pipeline_name)
	print response


# Watermark(水印)

## 创建水印
如果需要创建一个水印，可以参考如下代码：


	bucket = "your_bucket"
	key = "your_key"
	response = client.create_watermark(bucket, key)
	print response

接口返回的是包含了watermarkId的一个对象。

## 查询指定水印
如果需要查询已创建的水印，可以参考如下代码：


	watermark_id = "your_watermark_id"
	response = client.get_watermark(watermark_id)
	print response


## 查询当前用户水印
如果需要查询出本用户所创建的全部水印，可以参考如下代码：


	response = client.list_watermarks()
	print response


## 删除水印
如果需要删除某个已知watermarkId的水印，可以参考如下代码：


	watermark_id = "your watermark id"
	response = client.delete_watermark(watermark_id)
	print response


# 异常处理

##  系统异常
Media异常提示有如下三种方式：

异常方法 | 说明
---|---
BceHttpClientError | 重试时抛出的异常
--last_error | 最后一次重试时抛出的异常
----BceClientError | Media客户端产生的异常
----BceInvalidArgumentError | 传递参数产生的异常
----BceServerError | Media服务器产生的异常


用户可以使用try获取某个事件所产生的异常：

	from baidubce.exception import BceHttpClientError
	from baidubce.exception import BceServerError
	from baidubce.exception import BceClientError
	try:
	    watermark_id = "non_exist"
	    client.delete_watermark(watermark_id)
	except BceHttpClientError as e:
	    print "Cannot delete the watermark: ", e.message


返回为：

	Cannot delete the watermark:  Unable to execute HTTP request. Retried 0 times. A
	ll trace backs:
	>>>>Traceback (most recent call last):
	>>>>  File "C:\tools\Python27\lib\site-packages\baidubce\http\bce_http_client.py
	", line 183, in send_request
	>>>>    if handler_function(http_response, response):
	>>>>  File "C:\tools\Python27\lib\site-packages\baidubce\http\handler.py", line
	71, in parse_error
	>>>>    raise bse
	>>>>BceServerError: watermark: non_exist does not exist
	
	也可以用这种方式直接获取原始错误信息：
	print "Cannot delete the watermark: ", e.last_error.message
	得到：
	Cannot delete the watermark: watermark: non_exist does not exist

##  参数异常

Media Python SDK的每个调用都有一些类型固定不可以为空的参数，若该参数传入为空值则返回BceClientError，若该参数传入类型错误则返回TypeError。
