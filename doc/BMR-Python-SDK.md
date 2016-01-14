# BMR Python SDK文档

# 简介

本文档主要介绍BMR Python SDK的安装和使用。在使用本文档之前，您需要先了解BMR的一些基本知识，并已经开通了BMR服务。若您还不了解BMR，可以参考[产品描述](ProductDescription.html)和[操作指南](GettingStarted.html)。

# 安装SDK工具包

**运行环境**

Python SDK工具包支持在Python 2.7环境下运行。

**安装步骤**

1. 在[官方网站](http://bce.baidu.com/doc/SDKTool/index.html)下载BMR Python SDK。

2. 进入下载目录。

3. 在脚本文件中添加以下代码，即可以使用SDK包：

```python
python setup.py install
```

**SDK目录结构**

 
     baidubce
      ├── auth                    //公共权限目录
      ├── services                //服务公共目录
      │   └── bmr                 //BMR目录
      └── http                    //Http请求模块

# 快速入门

1. 初始化一个BmrClient。

	BmrClient是与BMR服务交互的客户端，所有BMR操作都是通过BmrClient完成的。用户可以参考[新建BmrClient](##新建BmrClient)，完成初始化客户端的操作。

2. 新建一个BMR Cluster(集群)。

	用户创建一个BMR集群，用于提交并运行指定的作业。在提交作业之前，必须先创建出一个集群。创建集群的请求成功后，将返回新集群的ID，可用于后续对集群进行相关操作。

	用户在创建集群时，需要为集群指定集群中虚拟机实例采用的镜像类型、镜像版本号和虚拟机实例组配置。另外，可选的配置项包括集群的名字、需要安装的组件信息(如Hive，Pig，HBase)、上传运行日志的BOS路径以及需要运行的作业信息。用户可以参考[新建集群](##新建cluster)，进行具体的集群配置操作。

3. 查看集群的状态信息。

	用户通过集群ID可以查看集群的状态信息。创建集群需要等待一定时间后集群成为可用状态，此时提交至集群的作业开始被调度执行。

4. 添加一个或多个Step(作业)。

	向指定集群添加一个或多个作业任务。集群创建成功后，用户可以根据集群已安装的应用来添加不同类型的作业，包括Custom Jar、Streaming、Hive、Pig。添加作业请求成功后，将返回包含所有新作业ID的数组，作业ID可用于后续对作业进行相关操作。

5. 查看作业的运行状态信息。

	用户通过作业ID可以查看作业的运行状态信息。

6. 终止集群。

	在结束作业的运行后，用户可以通过集群ID发送终止集群的请求。终止集群将释放集群的虚拟机实例，结束计费。

# BmrClient

## 配置BmrClient

BmrClient是BMR服务的Python客户端，为调用者与BMR服务进行交互提供一系列的方法。

在新建BmrClient之前，需要先创建配置文件对BmrClient进行配置，以下将此配置文件命名为`bmr_client_conf.py`，具体配置信息如下所示：
    
	#!/usr/bin/env python
	#coding=utf-8

	#导入Python标准日志模块
	import logging

	#从Python SDK导入BMR配置管理模块以及安全认证模块
	from baidubce.bce_client_configuration import BceClientConfiguration
	from baidubce.auth.bce_credentials import BceCredentials

	#设置BmrClient的Host，Access Key ID和Secret Access Key
	host = "bmr.bce-api.baidu.com"
	access_key_id = "your-access-key-id"
	secret_access_key = "your-secret-access-key"

	#设置日志文件的句柄和日志级别
	logger = logging.getLogger('baidubce.services.bmr.bmrclient')
	fh = logging.FileHandler("sample.log")
	fh.setLevel(logging.DEBUG)

	#设置日志文件输出的顺序、结构和内容
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	fh.setFormatter(formatter)
	logger.setLevel(logging.DEBUG)
	logger.addHandler(fh)

	#创建BceClientConfiguration
	config = BceClientConfiguration(credentials=BceCredentials(access_key_id, secret_access_key), 
	                                endpoint=host)

**注意：**

1. 在上面的代码中，变量access_key_id与secret_access_key是系统分配给用户的，用于标识用户，为访问Media做签名验证。其中access_key_id对应控制台中的“Access Key ID”，secret_access_key对应控制台中的“Access Key Secret”，获取方式请参考《操作指南 [管理ACCESSKEY](../BOS/GettingStarted.html#管理ACCESSKEY)》。

2. BceClientConfiguration构造函数的endpoint参数只能用指定的包含Region的域名来进行定义，目前仅北京Region开放了BMR SDK服务，因此endpoint只支持` http://bmr.bj.baidubce.com `这一个域名，随着Region的增加将会开放其他可以支持的域名。

## 新建BmrClient

在完成上述配置后，用户可以参考如下代码新建一个BmrClient:

```python
import logging
import bmr_client_conf
from baidubce.services.bmr.bmr_client import BmrClient

logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)
CONF = bmr_client_conf

bmr_client = BmrClient(CONF.config)
```
## 参数说明
Python SDK在`baidubce/bce_client_configuration.py`中默认设置了一些基本参数，若用户想要对参数的值进行修改，可以参考此文件创建自身的参数配置函数，并在构造BmrClient的时候传入，传入代码参考如下：

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
						endpoint = 'bmr_service_host',
						protocol = baidubce.protocol.HTTP,
						region = baidubce.region.BEIJING,
						connection_timeout_in_mills = 50 * 1000,
						send_buf_size = 1024 * 1024,
						recv_buf_size = 10 * 1024 * 1024,
						retry_policy = my_policy)

	# create BmrClient with my config
	my_client = BmrClient(my_config)

参数说明如下：

参数 | 说明 | 默认值
---|---|---
`PROTOCOL` | 协议 | baidubce.protocol.HTTP
`REGION` | 区域 | baidubce.region.BEIJING（目前只支持北京地区）
`CONNECTION_TIMEOUT_IN_MILLIS` | 请求超时时间（单位：毫秒） | 120 * 1000
`SOCKET_TIMEOUT_IN_MILLIS` | 通过打开的连接传输数据的超时时间（单位：毫秒） | 300 * 1000（0指的是无限等待，若设置非0数值需要对文件大小和网速进行评估，否则上传大文件时会产生超时）
`SEND_BUF_SIZE` | 发送缓冲区大小 | 5 * 1024 * 1024
`RECV_BUF_SIZE` | 接收缓冲区大小 | 5 * 1024 * 1024
`retry_policy` | 重试逻辑 | 最大重试次数3次, 超时时间为20 * 1000毫秒，重试间隔300毫秒

# Cluster（集群）

## 新建cluster

如下代码可以新建一个集群，集群包含1个master节点和2个core节点，且安装了Hive、Pig、HBase应用。请注意：参考下面样例代码时，需要修改log_uri参数指定BOS路径为您的账户可用的BOS路径。

    
	# 配置集群的实例组
	instance_groups = [
	    BmrClient.create_instance_group(
	        'ig-master',
	        'Master',
	        'g.small',
	        1
	    ),
	    BmrClient.create_instance_group(
	        'ig-core',
	        'Core',
	        'g.small',
	        2
	    )
	]

	# 构造请求体
	request_body = {
	    'applications': [
	        {
	            "name": "hive",
	            "version": "0.13.0"
	        },
	        {
	            "name": "pig",
	            "version": "0.11.0"
	        },
	        {
	            "name": "hbase",
	            "version": "0.98.0"
	        }
	    ],
	    'auto_terminate': False,
	    'log_uri': 'bos://tester01/sdk/',
	    'name': 'sdk-cluster01'
	}

	try:
	    response = bmr_client.create_cluster(
	            'hadoop',
	            '0.1.0',
	            instance_groups,
	            **request_body)
	    cluster_id = response.cluster_id
	except BceHttpClientError as e:
	    if isinstance(e.last_error, BceServerError):
	        LOG.error('create_cluster failed. Response %s, code: %s, msg: %s'
	                  % (e.last_error.status_code, e.last_error.code, e.last_error.message))
	    else:
	        LOG.error('create_cluster failed. Unknown exception: %s' % e)


## 列出全部cluster

如下代码可以罗列出属于请求调用者的所有集群，用户可以通过配置查询参数max_keys来限制每次请求返回的集群数目:

```python
try:
    response = bmr_client.list_clusters(max_keys=5)
    LOG.debug('list total %s clusters' % len(response.clusters))
    # 输出各个集群的信息
    for cluster in response.clusters:
        LOG.debug('cluster: %s' % cluster)
except BceHttpClientError as e:
    if isinstance(e.last_error, BceServerError):
        LOG.error('list_clusters failed. Response %s, code: %s, msg: %s'
                  % (e.last_error.status_code, e.last_error.code, e.last_error.message))
    else:
        LOG.error('list_clusters failed. Unknown exception: %s' % e)
```

另外，也可以使用分页查询的方式来获取所有集群, 通过配置max_keys来限制每页查询返回的集群数目：

```python
try:
    page = 1
    next_marker = None
    max_keys = 5
    is_truncated = True
    while is_truncated:
        response = bmr_client.list_clusters(marker=next_marker, max_keys=max_keys)
        LOG.debug('list %s clusters on Page %s' % (len(response.clusters), page))
        page += 1
        is_truncated = response.is_truncated
        next_marker = response.next_marker
except BceHttpClientError as e:
    if isinstance(e.last_error, BceServerError):
        LOG.error('list_clusters failed. Response %s, code: %s, msg: %s'
                  % (e.last_error.status_code, e.last_error.code, e.last_error.message))
    else:
        LOG.error('list_clusters failed. Unknown exception: %s' % e)
```

## 查询指定的cluster

获取了集群ID后，可用如下代码查询指定集群的信息：

```python
try:
    response = bmr_client.get_cluster(cluster_id)
    # 输出集群的状态信息
    status = response.status.state
    LOG.debug('check cluster %s: status %s' % (cluster_id, status))
except BceHttpClientError as e:
    if isinstance(e.last_error, BceServerError):
        LOG.error('get_cluster failed. Response %s, code: %s, msg: %s'
                  % (e.last_error.status_code, e.last_error.code, e.last_error.message))
    else:
        LOG.error('describe_cluster failed. Unknown exception: %s' % e)
```

## 终止指定的cluster

如下代码可以终止指定的集群：

```python
try:
    response = bmr_client.terminate_cluster(cluster_id)
    LOG.debug('terminate cluster %s: status %s' % (cluster_id, response.status))
except BceHttpClientError as e:
    if isinstance(e.last_error, BceServerError):
        LOG.error('terminate_cluster failed. Response %s, code: %s, msg: %s'
                  % (e.last_error.status_code, e.last_error.code, e.last_error.message))
    else:
        LOG.error('terminate_cluster failed. Unknown exception: %s' % e)
```

# Step（作业）

作业是和集群相关联的资源，对作业的操作需要指定集群ID。

## 添加steps

BMR支持多种类型的作业，不同类型的作业有不同的配置项。如下代码可向指定的hadoop类型的集群添加Custom Jar、Streaming、Hive、Pig作业。请注意：参考下面样例代码时，需要修改作业参数指定的BOS路径为您的账户可用的BOS路径。

```python
steps =  [
    BmrClient.create_step(
            'Java',
            'sdk-job-01',
            'Continue',
            BmrClient.create_java_step_properties(
                'bos://benchmark/hadoop/hadoop-mapreduce-examples.jar',
                'org.apache.hadoop.examples.WordCount',
                'bos://helloworld/input/install.log bos://tester01/sdk/output_java/out1'
                )
            ),
    BmrClient.create_step(
            'Streaming',
            'sdk-job-02',
            'Continue',
            BmrClient.create_streaming_step_properties(
                'bos://helloworld/input/install.log',
                'bos://tester01/sdk/output_streaming/out1',
                'cat')
            ),
    BmrClient.create_step(
            'Hive',
            'sdk-job-03',
            'Continue',
            BmrClient.create_hive_step_properties(
                'bos://chy3/hive/hql/hive_src.hql',
                '--hivevar LOCAT=bos://chy3/hive/tables/src',
                'bos://chy3/hive/data/hive_src.data',
                'bos://tester01/sdk/output_hive/out1'
                )
            ),
    BmrClient.create_step(
            'Pig',
            'sdk-job-04',
            'Continue',
            BmrClient.create_pig_step_properties(
                'bos://chy3/pig/script/pig_grep.pig',
                input='bos://chy3/pig/data/pig_grep.data',
                output='bos://tester01/sdk/output_pig/out1'
                )
            )
]

try:
    response = bmr_client.add_steps(cluster_id, steps)
    LOG.debug('add steps response: %s' % response)
except BceHttpClientError as e:
    if isinstance(e.last_error, BceServerError):
        LOG.error('add_steps failed. Response %s, code: %s, msg: %s'
                  % (e.last_error.status_code, e.last_error.code, e.last_error.message))
    else:
        LOG.error('add_steps failed. Unknown exception: %s' % e)
```

## 列出全部steps

如下代码可以罗列出指定集群上的全部作业，用户可以通过指定max_keys来限制一次请求返回的最大作业数目：

```python
try:
    response = bmr_client.list_steps(cluster_id, max_keys=50)
    for step in response.steps:
        LOG.debug('list step %s: %s' % (step.id, step))
except BceHttpClientError as e:
    if isinstance(e.last_error, BceServerError):
        LOG.error('list_steps failed. Response %s, code: %s, msg: %s'
                  % (e.last_error.status_code, e.last_error.code, e.last_error.message))
    else:
        LOG.error('list_steps failed. Unknown exception: %s' % e)
```

同样，SDK也提供了分页查询的调用方式：

```python
try:
    page = 1
    next_marker = None
    max_keys = 5
    is_truncated = True
    while is_truncated:
        response = bmr_client.list_steps(cluster_id, marker=next_marker, max_keys=max_keys)
        LOG.debug('list %s steps on Page %s' % (len(response.steps), page))
        page += 1
        is_truncated = response.is_truncated
        next_marker = response.next_marker
except BceHttpClientError as e:
    if isinstance(e.last_error, BceServerError):
        LOG.error('list_steps failed. Response %s, code: %s, msg: %s'
                  % (e.last_error.status_code, e.last_error.code, e.last_error.message))
    else:
        LOG.error('list_steps failed. Unknown exception: %s' % e)
```

## 查询指定的step

如下代码可以查看指定作业的信息：

```python
try:
    response = bmr_client.get_step(cluster_id, step_id)
    LOG.debug('describe step response: %s' % response)
except BceHttpClientError as e:
    if isinstance(e.last_error, BceServerError):
        LOG.error('get_step failed. Response %s, code: %s, msg: %s'
                  % (e.last_error.status_code, e.last_error.code, e.last_error.message))
    else:
        LOG.error('get_step failed. Unknown exception: %s' % e)
```

# 异常处理

## 系统异常
BMR异常提示有如下几种方法：

异常方法 | 说明
---|---
BceHttpClientError | 重试时抛出的异常
last_error | 最后一次重试时抛出的异常
BceClientError | BMR客户端产生的异常
BceInvalidArgumentError | 传递参数产生的异常
BceServerError | BMR服务器产生的异常


用户可以使用try获取某个事件所产生的异常：

```python
from baidubce.exception import BceHttpClientError
from baidubce.exception import BceServerError

try:
    response = bmr_client.get_step(new_cluster_id, step_id)
    LOG.debug('describe steps response: %s' % response)
except BceHttpClientError as e:
    if isinstance(e.last_error, BceServerError):
        LOG.error('get_step failed. Response %s, code: %s, msg: %s'
                  % (e.last_error.status_code, e.last_error.code, e.last_error.message))
    else:
        LOG.error('get_step failed. Unknown exception: %s' % e)
```

# 版本变更记录

* Python SDK开发包[2016-01	-05]版本号0.8.8

  首次发布：

  * 支持创建、罗列、查看、终止 Cluster
  * 支持添加、罗列、查看 Step
