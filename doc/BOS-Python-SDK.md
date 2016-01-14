# BOS Python SDK文档 

# 简介

本文档主要介绍BOS Python SDK的安装和使用。在使用本文档前，您需要先了解BOS的一些基本知识，并已开通了BOS服务。若您还不了解BOS，可以参考[产品描述](ProductDescription.html)和[入门指南](GettingStarted-new.html)。

# 安装SDK工具包

**运行环境**

Python SDK工具包支持在Python 2.7环境下运行。


**安装步骤**

1. 在[官方网站](http://bce.baidu.com/doc/SDKTool/index.html)下载BOS Python SDK。

2. 进入下载目录。

3. 在脚本文件中添加以下代码，即可以使用SDK包：

  ```python
   python setup.py install
    ```

**SDK目录结构**

   ```
    baidubce
           ├── auth                    //公共权限目录
           ├── services                //服务公共目录
           │   └── bos                 //BOS目录
           └── http                    //Http请求模块
  ```

# 快速入门

1. 初始化一个BOSClient。

  bos_client是与BOS服务交互的客户端，BOS Python SDK的BOS操作都是通过bos_client完成的。用户可以参考[BOSClient](# BOSClient)。完成初始化客户端的操作。

2. 新建一个Bucket。

  Bucket是BOS上的命名空间，相当于数据的容器，可以存储若干数据实体（Object）。用户可以参考[新建Bucket](# 新建Bucket)来完成新建一个Bucket的操作。针对Bucket的命名规范，可以参考[Bucket命名规范](# Bucket命名规范)。

3. 上传Object。

  Object是BOS中最基本的数据单元，用户可以把Object简单的理解为文件。用户可以参考[上传Object](# 上传Object)完成对Object的上传。

4. 列出指定Bucket中的全部Object。

  当用户完成一系列上传后，可以参考[查看Bucket中Object列表](# 查看Bucket中Object列表)来查看指定Bucket下的全部Object。

5. 获取指定Object

  用户可以参考[获取Object](# 获取Object)来实现对一个或者多个Object的获取。

#  BOSClient
## 	配置BOSClient
BOSClient是BOS服务的Python客户端，为调用者与BOS服务进行交互提供了一系列的方法。

在新建BOSClient之前，需要先创建配置文件对BOSClient进行配置，以下将此配置文件命名为`bos_sample_conf.py`，具体配置信息如下所示：
    
    #!/usr/bin/env python
	#coding=utf-8

	#导入Python标准日志模块
	import logging

	#从Python SDK导入BOS配置管理模块以及安全认证模块
	from baidubce.bce_client_configuration import BceClientConfiguration
	from baidubce.auth.bce_credentials import BceCredentials

	#设置访问BOS服务的代理
	PROXY_HOST = 'localhost:8080'

	#设置BosClient的Host，Access Key ID和Secret Access Key
	bos_host = "BOS_HOST"
	access_key_id = "AK"
	secret_access_key = "SK"

	#设置日志文件的句柄和日志级别
	logger = logging.getLogger('baidubce.services.bos.bosclient')
	fh = logging.FileHandler("sample.log")
	fh.setLevel(logging.DEBUG)

	#设置日志文件输出的顺序、结构和内容
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	fh.setFormatter(formatter)
	logger.setLevel(logging.DEBUG)
	logger.addHandler(fh)

	#创建BceClientConfiguration
	config = BceClientConfiguration(credentials=BceCredentials(access_key_id, secret_access_key), endpoint = bos_host)

**注意：**

1. 访问BOS服务的代理参数PROXY_HOST可缺省。

2. 针对日志文件，Logging有如下级别：DEBUG，INFO，WARNING，ERROR，CRITICAL。

## 新建BOSClient

在完成上述配置之后，参考如下代码新建一个BosClient。

	#导入BOSClient配置文件
	import bos_sample_conf 
	
	#导入BOS相关模块
	from baidubce import exception
	from baidubce.services import bos
	from baidubce.services.bos import canned_acl
	from baidubce.services.bos.bos_client import BosClient

	#新建BOSClient
	bos_client = BosClient(bos_sample_conf.config)


###  设置网络参数
用户可以设置一些网络参数：
	
    #设置请求超时时间
    bos_sample_conf.config.connection_timeout_in_mills = TIMEOUT
    
    #设置接收缓冲区大小
    bos_sample_conf.config.recv_buf_size(BUF_SIZE)

    #设置发送缓冲区大小
    bos_sample_conf.config.send_buf_size(BUF_SIZE)

	#设置连接重试策略
	#三次指数退避重试
	bos_sample_conf.config.retry_policy = BackOffRetryPolicy()
	#不重试
	bos_sample_conf.config.retry_policy = NoRetryPolicy()

**参数说明**

通过bos_client_configuration能指定的所有参数如下表所示：

参数 | 说明
---|---
port | BOS端口号
send_buf_size | 发送缓冲区大小
recv_buf_size | 接收缓冲区大小
connection_timeout_in_mills| 请求超时时间（单位：毫秒）
retry_policy | 连接重试策略，初始化Client时默认为三次指数退避


# Bucket
## Bucket命名规范
Bucket既是BOS上的命名空间，也是计费、权限控制、日志记录等高级功能的管理实体。

* Bucket名称在所有区域中具有全局唯一性，且不能修改。
**说明：**
  * 百度开放云目前开放了多区域支持，请参考[区域选择说明](../Reference/Regions.html)。
  * 目前支持“华北-北京”和“华南-广州”两个区域。
* 存储在BOS上的每个Object都必须包含在一个Bucket中。
* 一个用户最多可创建100个Bucket，但每个Bucket中存放的Object的数量和大小总和没有限制，用户不需要考虑数据的可扩展性。

Bucket的命名有以下规范：

* 只能包括小写字母，数字，短横线（-）。
* 必须以小写字母或者数字开头。
* 长度必须在3-63字节之间。

##  新建Bucket
如下代码可以新建一个Bucket：
	
	if not bos_client.does_bucket_exist(bucket_name):
        bos_client.create_bucket(bucket_name)

**注意：**由于Bucket的名称在所有区域中是唯一的，所以需要保证bucket_name不与其他区域上的Bucket名称相同。

## 查看Bucket列表
用如下方式可以列出用户所有的Bucket：
```
response = bos_client.list_buckets()
for bucket in response.buckets:
	 print bucket.name
```

`list_bucket`方法返回的解析类中可供调用的参数如下：

参数 | 说明
---|---
owner | Bucket Owner信息
--id | Bucket Owner的用户ID
--display_name | Bucket Owner的名称
buckets | 存放多个Bucket信息的容器
--bucket | 存放一个Bucket信息的容器
----name | Bucket名称
----creation_date | Bucket创建时间
----location | Bucket所属的区域

## 删除Bucket
如下代码可以删除一个Bucket：
	
	bos_client.delete_bucket(bucket_name)

**注意：**如果Bucket不为空（即Bucket中有Object存在），则Bucket无法被删除，必须清空Bucket后才能成功删除。

## Bucket权限控制

### 设置Bucket的访问权限

如下代码将Bucket的权限设置为了private：

	bos_client.set_bucket_canned_acl(bucket_name, canned_acl.PRIVATE)

其中canned_acl中包含三个参数：`PRIVATE`、`PUBLIC_READ`、`PUBLIC_READ_WRITE`，它们分别对应的相关权限为：`private`、`public-read`、`public-read-write`。关于权限的具体内容可以参考《BOS API文档 [使用CannedAcl方式的权限控制](API.html# 使用CannedAcl方式的权限控制)》。

###  设置指定用户对Bucket的访问权限

BOS提供set_bucket_acl方法来实现指定用户对Bucket的访问权限设置，可以参考如下代码实现：

    bos_client.set_bucket_acl(
        bucket_name,
        [{'grantee': [{'id': 'b124deeaf6f641c9ac27700b41a350a8'},
                      {'id': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'}],
          'permission': ['FULL_CONTROL']}])

**注意：**
1. `id`为用户ID，您可在用户信息中查看。
2. `permission`中的权限设置包含三个值：`READ`、`WRITE`、`FULL_CONTROL`，它们分别对应相关权限。具体内容可以参考《BOS API文档 [上传ACL文件方式的权限控制](API.html# 上传ACL文件方式的权限控制)》。

###  查看Bucket的权限
如下代码可以查看Bucket的权限：

    response = bos_client.get_bucket_acl(bucket_name)

    bos_client.set_bucket_acl(bucket_name, response.access_control_list)

`get_bucket_acl`方法返回的解析类中可供调用的参数有：

参数 | 说明
---|---
owner | Bucket owner信息
--id | Bucket owner的用户ID
access_control_list | 标识Bucket的权限列表
--grantee | 标识被授权人
----id | 被授权人ID
--permission | 标识被授权人的权限

##  检查Bucket是否存在

请参考如下代码：

	bos_client.does_bucket_exist(bucket_name)
	
##  查看Bucket所属的区域

请参考如下代码

	bos_client.get_bucket_location(bucket_name)

#  Object
##  Object命名规范
在BOS中，用户操作的基本数据单元是Object。Bucket中的Object数量不限，但单个Object最大允许存储5TB的数据。Object包含Key、Meta和Data。其中，Key是Object的名字；Meta是用户对该Object的描述，由一系列Name-Value对组成；Data是Object的数据。

Object的命名规范如下：

* 使用UTF-8编码。
* 长度必须在1-1023字节之间。
* 首字母不能为'/'。

##  上传Object
如下代码可以进行Object上传：
```
bos_client.put_object(bucket_name, object_key, data)
```
其中，data为流对象，不同类型的Object采用不同的处理方法，从字符串中的上传使用StringIO的返回，从文件中的上传使用open()的返回，因此BOS提供了封装好的接口方便用户进行快速上传。

1. 从字符串中上传，参考如下代码：

	bos_client.put_object_from_string(bucket_name, object_key, string)

2. 或者从文件中直接上传，参考如下代码：

    bos_client.put_object_from_file(bucket_name, object_key, file_name)

**注意：**put_object相关接口均支持不超过5GB的Object上传。

这些接口均有可选参数:

参数 | 说明
---|---
content_type | 上传文件或字符串的类型
content_md5 | 用于进行文件校验
user_metadata | 用户自定义meta数据

在put_object_from_string或者put_object_from_file请求处理成功后，BOS会在Header中返回Object的ETag作为文件标识。

##  分块上传

BOS允许用户将一个Object分成多个请求上传到后台服务器中，关于分块上传的内容，将在[Object的分块上传](# Object的分块上传) 这一章中做详细介绍。

##  查看Bucket中Object列表
当用户完成一系列上传后，可能会需要查看在指定Bucket中的全部Object，可以通过如下代码实现：
```
response = bos_client.list_objects(bucket_name)
for object in response.contents:
    print object.key
```
```
for object in bos_client.list_all_objects(bucket_name):
    print object.key
```

`list_objects`方法其他可选的参数有：

参数 | 说明
---|---
prefix | 限定返回的object key必须以Prefix作为前缀。
delimiter | 是一个用于对Object名字进行分组的字符。所有名字包含指定的前缀且第一次出现Delimiter字符之间的object作为一组元素: CommonPrefixes。
max_keys | 限定此次返回object的最大数，此数值不能超过1000，如果不设定，默认为1000。
marker | 设定结果从Marker之后按字母排序的第一个开始返回。

`list_objects`方法返回的解析类中可供调用的参数有：

参数 | 说明
---|---
common_prefixes | 仅当指定delimiter，才会返回此项
prefix | 匹配以prefix开始到第一次出现Delimiter字符之间的object作为一组元素返回
is_truncated | 指明是否所有查询都返回了；false-本次已经返回所有结果，true-本次还没有返回所有结果
max_keys | 请求返回的最大数目
marker | 本次查询的起点
name | Bucket名称
next_marker | 只要IsTruncated为true，就会返回next_marker，作为下次查询marker的值
contents | 返回的一个Object的容器
--key | Object名称
--last_modified | 此Object最后一次被修改的时间
--e_tag | Object的HTTP协议实体标签
--size |  Object的内容的大小（字节数）
--owner | Object对应Bucket所属用户信息
----id | Bucket Owner的用户ID
----display_name | Bucket Owner的名称

`list_all_objects`方法返回contents的生成器（Generator），并且不受单次最大返回1000个结果的限制，会返回所有的结果。

##  获取Object

### 简单的读取Object
用户可以通过如下代码将Object读取到一个流中：

```
print bos_client.get_object_as_string(bucket_name, object_key)
```
### 直接下载Object到文件

用户可以参考如下代码将Object下载到指定文件：

	bos_client.get_object_to_file(bucket_name, object_key, file_name)

###  获取Object的Meta信息
用户可以通过如下代码获得Object的Meta信息。

	response = bos_client.get_object_meta_data(bucket_name, object_key)

`get_object_meta_data`方法返回的解析类中可供调用的参数有：

参数 | 说明
---|---
content_length | Object的大小
e_tag | Object的HTTP协议实体标签
bce_meta | 如果在PutObject指定了user_metadata自定义meta，则返回此项（）


## 获取Object的URL

用户可以通过如下示例代码获取指定Object的URL：

```
url = bos_client.generate_pre_signed_url(bucket_name, object_key, timestamp, expiration_in_seconds)

```
说明：

* 用户在调用该函数前，需要手动设置`endpoint`为所属区域域名。百度开放云目前开放了多区域支持，请参考[区域选择说明](../Reference/Regions.html)。目前支持“华北-北京”和“华南-广州”两个区域。
  * 北京区域：`http://bj.bcebos.com`
  * 广州区域：`http://gz.bcebos.com`
* `timestamp`为时间戳，标识URL有效起始时间，`timestamp=int(time.time())`，并需要`* import time`。
* `timestamp`为可选参数，不配置时，默认值为当前时间。
* `expriation_in_seconds`用来设置URL的有效时长，为可选参数，不配置时，默认值为1800秒。如果要设置为永久不失效的时间，可以将`expirationInSeconds`参数设置为 -1，不可设置为其他负数。

##  拷贝Object
用户可以通过copyObject方法拷贝一个Object，如下代码所示：
	
	bos_client.copy_object(source_bucket_name, source_object_key, target_bucket_name, target_object_key)

##  删除Object
如下代码删除了一个Object：

	bos_client.delete_object(bucket_name, object_key)

#  Object的分块上传
## 分块上传简介
除了通过putObject接口上传文件到BOS以外，BOS还提供了另外一种上传模式 —— Multipart Upload。用户可以在如下的应用场景内（但不仅限于此），使用Multipart Upload上传模式，如：

* 需要支持断点上传。
* 上传超过5GB大小的文件。
* 网络条件较差，和BOS的服务器之间的连接经常断开。
* 需要流式地上传文件。
* 上传文件之前，无法确定上传文件的大小。

下面将介绍分步实现Multipart Upload。

##  初始化Multipart Upload

BOS使用initiate_multipart_upload方法来初始化一个分块上传事件：

	upload_id = bos_client.initiate_multipart_upload(bucket_name, object_key).upload_id

该方法会返回InitMultipartUploadResponse对象，此对象中包含uploadId参数，用来表示此次的上传事件。

## 上传分块

初始化完成后，进行分块上传：

	#设置分块开始位置
	left_size = os.path.getsize(file_name)
	#设置分块的开始偏移位置
    offset = 0

    part_number = 1
    part_list = []
    
    while left_size > 0:
    	#设置每块为5MB
        part_size = 5 * 1024 * 1024
        if left_size < part_size:
            part_size = left_size

        response = bos_client.upload_part_from_file(
            bucket_name, object_key, upload_id, part_number, part_size, file_name, offset)


        left_size -= part_size
        offset += part_size
        part_list.append({
            "partNumber": part_number,
            "eTag": response.metadata.e_tag
        })


        part_number += 1

**注意：**

1. offset参数以字节为单位，为分块的开始偏移位置。

2. size参数以字节为单位，定义每个分块的大小，除最后一个Part以外，其他的Part大小都要大于5MB。

##  完成分块上传

	bos_client.complete_multipart_upload(bucket_name, object_key, upload_id, part_list)

其中，part_list类型是list里面每个元素是个dict，每个dict包含两个关键字，一个是partNumber, 一个是eTag。

示例如下：

	[{'partNumber': 1, 'eTag': 'f1c9645dbc14efddc7d8a322685f26eb'}, {'partNumber': 2, 'eTag': 'f1c9645dbc14efddc7d8a322685f26eb'}, {'partNumber': 3, 'eTag': '93b885adfe0da089cdf634904fd59f71'}]

该方法返回的解析类中可供调用的参数有：

参数 | 说明
---|---
bucket | Bucket名称
key | Object名称
e_tag | 每个上传分块的ETag
location | Object的URL

**注意：**此对象中包含的ETag是上传分块过程中每个Part的ETag，BOS收到用户提交的Part列表后，会逐一验证每个数据Part的有效性。当所有的数据Part验证通过后，BOS将把这些数据part组合成一个完整的Object。

##  取消分块上传事件

用户可以使用abort_multipart_upload方法取消分块上传：

	bos_client.abort_multipart_upload(bucket_name, object_key, upload_id = upload_id)

##  获取未完成的分块上传事件

用户可以使用如下两种方法获取Bucket中未完成的分块上传事件：
```
bos_client.list_multipart_uploads(bucket_name)
```
```
for item in list_all_multipart_uploads(bucket_name):
    print item.upload_id
```
`list_multipart_uploads`方法返回的解析类中可供调用的参数有：

参数 | 说明
---|---
bucket | Bucket名称
key_marker | 开始上传的分块Object名称
next_key_marker | 当指定了delimiter且IsTruncated true时，才返回此项，作为下次查询marker的值
is_truncated | 指明是否所有查询都返回了；false-本次已经返回所有结果，true-本次还没有返回所有结果
prefix | 匹配以prefix开始到第一次出现Delimiter字符之间的object作为一组元素返回
common_prefixes | 仅当指定delimiter，才会返回此项
delimiter | 查询的结束符
max_uploads | 请求返回的最大数目
uploads | 全部未完成的分快上传事件容器
--owner | 对应Bucket所属用户信息
----id | Bucket Owner的用户id
----display_name | Bucket Owner的名称
--key | 分块所属Object名称
--upload_id | 分块上传id
--initiated | 分块上传开始时间

`list_all_multipart_uploads`方法返回uploads的生成器（Generator），并且不受单次最大返回1000个结果的限制，会返回所有的结果。

##  获取所有已上传的块信息

用户可以使用如下两种方法获取某个上传事件中所有已上传的块：
```
bos_client.list_parts(bucket_name, object_key, upload_id = upload_id)
```
```
for item in list_all_parts(bucket_name, object_key, upload_id = upload_id):
    print item.part_number
```
`list_parts`方法返回的解析类中可供调用的参数有：

参数 | 说明
---|---
bucket | Bucket名称
key | Object名称
initiated | 本次分块上传开始时间
max_parts | 请求返回的最大数目
is_truncated | 指明是否所有查询都返回了；false-本次已经返回所有结果，true-本次还没有返回所有结果
part_number_marker | 分块开始标记位
parts | 分块列表，list类型
--part_number | 分块编号
--last_modified | 此分块最后一次被修改的时间
--e_tag | 每个上传分块的ETag
--size | 分块内容的大小（字节数）
upload_id | 本次分块上传的id
owner | 对应bucket所属用户信息
--id | Bucket owner的用户id
--display_name | Bucket owner的名称
next_part_number_marker | 本次请求返回的最后一条记录的partNumber，可以作为下一次请求的_part_number_marker

`list_all_parts`方法返回parts的生成器（Generator），并且不受单次最大返回1000个结果的限制，会返回所有的结果。

#  异常处理

##  系统异常

BOS系统异常提示有如下三种方式：

异常方法 | 说明
---|---
BceHttpClientError | 重试时抛出的异常
--last_error | 最后一次重试时抛出的异常
----BceClientError | BOS客户端产生的异常
----BceInvalidArgumentError | 传递参数产生的异常
----BceServerError | BOS服务器产生的异常

用户可以使用try获取某个事件所产生的异常：

	try:
        bos_client.delete_object(bucket_name, object_key)
    except exception.BceHttpError as e:
        print e.message

返回为：
```
BceHttpClientError: Unable to execute HTTP request. Retried 0 times. All trace backs:
>>>>Traceback (most recent call last):
>>>>  File "/home/work/python-2.7/lib/python2.7/site-packages/baidubce/http/bce_http_client.py", line 184, in send_request
>>>>    if handler_function(http_response, response):
>>>>  File "/home/work/python-2.7/lib/python2.7/site-packages/baidubce/http/handler.py", line 71, in parse_error
>>>>    raise bse
>>>>BceServerError: The specified key does not exist.
```

##  参数异常

BOS Python SDK的每个调用都有一些类型固定不可以为空的参数，若该参数传入为空值则返回ValueError，若该参数传入类型错误则返回TypeError。

参数与调用的对应关系如下：

<table>
 <tr><th>BOS调用</th><th>参数</th><th>说明</th><th>类型</th></tr>
 <tr><td>create_bucket, does_bucket_exist, delete_bucket, list_objects, list_all_objects, delete_object, get_bucket_acl, list_multipart_uploads, list_all_multipart_uploads</td><td>bucket_name</td><td>Bucket名称</td><td>string, unicode</td></tr>
 <tr><td rowspan=2>set_bucket_acl</td><td>bucket_name</td><td>Bucket名称</td><td>string, unicode</td></tr>
  <tr><td>acl</td><td>ACL主体包含被授权人及权限</td><td>list, dict</td></tr>
 <tr><td rowspan=2>set_bucket_canned_acl</td><td>bucket_name</td><td>Bucket名称</td><td>string, unicode</td></tr>
  <tr><td>canned_acl</td><td>CannedAcl权限</td><td>string</td></tr>
 <tr><td rowspan=2>get_object, get_object_as_string, get_object_meta_data, initiate_multipart_upload</td><td>bucket_name</td><td>Bucket名称</td><td>string, unicode</td></tr>
  <tr><td>key</td><td>Object名称</td><td>string</td></tr>
 <tr><td rowspan=3>get_object_to_file, put_object_from_file</td><td>bucket_name</td><td>Bucket名称</td><td>string, unicode</td></tr>
  <tr><td>key</td><td>Object名称</td><td>string</td></tr>
  <tr><td>file_name</td><td>文件名</td><td>string</td></tr>
 <tr><td rowspan=5>put_object</td><td>bucket_name</td><td>Bucket名称</td><td>string, unicode</td></tr>
  <tr><td>key</td><td>Object名称</td><td>string</td></tr>
  <tr><td>data</td><td>流对象</td><td>object</td></tr>
  <tr><td>content_length</td><td>上传Object的大小</td><td>int, long</td></tr>
  <tr><td>content_md5</td><td>上传Object的MD5</td><td>string</td></tr>
 <tr><td rowspan=3>put_object_from_string</td><td>bucket_name</td><td>Bucket名称</td><td>string, unicode</td></tr>
  <tr><td>key</td><td>Object名称</td><td>string</td></tr>
  <tr><td>data</td><td>上传字符串</td><td>string, unicode</td></tr>
 <tr><td rowspan=2>copy_object</td><td>source_bucket_name, target_bucket_name</td><td>源Bucket和目标Bucket名称</td><td>string, unicode</td></tr>
  <tr><td>source_key, target_key</td><td>源Object和目标Object名称</td><td>string</td></tr>
 <tr><td rowspan=5>upload_part</td><td>bucket_name, upload_id</td><td>Bucket名称，标识MultUpload操作全局ID</td><td>string, unicode</td></tr>
  <tr><td>key</td><td>Object名称</td><td>string</td></tr>
  <tr><td>part_number</td><td>分块编号</td><td>int</td></tr>
  <tr><td>part_size</td><td>上传分块的大小</td><td>int, long</td></tr>
  <tr><td>part_fp</td><td>上传分块对象</td><td>object</td></tr>
 <tr><td rowspan=6>upload_part_from_file</td><td>bucket_name, upload_id</td><td>Bucket名称，标识MultUpload操作全局ID</td><td>string, unicode</td></tr>
  <tr><td>key</td><td>Object名称</td><td>string</td></tr>
  <tr><td>part_number</td><td>分块编号</td><td>int</td></tr>
  <tr><td>part_size</td><td>上传分块的大小</td><td>int, long</td></tr>
  <tr><td>file_name</td><td>文件名</td><td>string</td></tr>
  <tr><td>offset</td><td>分块的开始偏移位置</td><td>int</td></tr>
 <tr><td rowspan=3>complete_multipart_upload</td><td>bucket_name, upload_id</td><td>Bucket名称，标识MultUpload操作全局ID</td><td>string, unicode</td></tr>
  <tr><td>key</td><td>Object名称</td><td>string</td></tr>
  <tr><td>part_list</td><td>分块列表</td><td>list</td></tr>
 <tr><td rowspan=2>abort_multipart_upload, list_parts, list_all_parts</td><td>bucket_name, upload_id</td><td>Bucket名称，标识MultUpload操作全局ID</td><td>string, unicode</td></tr>
  <tr><td>key</td><td>Object名称</td><td>string</td></tr>

</table>



# 版本变更记录

* Python SDK开发包[2015-10-13] 版本号 0.8.7

  变更记录：
  
  内部优化，功能无新增。

* Python SDK开发包[2015-09-06] 版本号 0.8.6

  变更记录：
  
  支持多区域选择。

* Python SDK开发包 [2015-07-23] 版本号 0.8.5

  变更记录：
  
  BOS本次无新功能增加。

* Python SDK开发包 [2015-07-09] 版本号 0.8.4

  变更记录：
  
 1. 在访问路径中去掉v1。

 2. 修正了sdk不能操作以斜杠“/”结尾的object的bug。
  

* Python SDK开发包 [2015-05-28] 版本号 0.8.3

  变更记录：
  
  BOS本次无新功能增加。

* Python SDK开发包 [2015-04-02] 版本号 0.8.2.1

  首次发布：

  * 支持创建、查看、罗列、删除 Bucket
  * 修改、获取Bucket的访问权限
  * 上传、查看、罗列、删除Object

