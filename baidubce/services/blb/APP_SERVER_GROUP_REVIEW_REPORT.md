# 应用型BLB服务器组相关接口 SDK Review 报告

## 1. 概述

**Review 时间**: 2026-03-11  
**Review 范围**: 应用型BLB服务器组相关接口 (Python SDK)  
**API 文档位置**: `/blb-master-279ba9446476728257b2db5fab7c6a5701beb5ce/API参考/应用型blb接口/应用型BLB服务器组相关接口.md`  
**SDK 文件位置**: `python/baidubce/services/blb/app_blb_client.py`

---

## 2. Review 结果汇总

### 2.1 整体结论

| 指标 | 数量 |
|------|------|
| API文档定义接口数 | 13 |
| SDK已实现接口数 | 13 |
| 发现问题数 | 2 |
| P0级问题 (已修复) | 1 |
| P1级问题 (已修复) | 1 |

### 2.2 问题汇总表

| 接口功能 | SDK 与 API 是否一致 | 主要问题说明 | 修复状态 |
|---------|-------------------|-------------|---------|
| CreateAppServerGroup | 是 | 无问题 | - |
| UpdateAppServerGroup | 是 | 无问题 | - |
| DescribeAppServerGroup | 是 | 无问题 | - |
| DeleteAppServerGroup | 是 | 无问题 | - |
| **CreateAppServerGroupPort** | **否→是** | **缺少 enableHealthCheck 和 healthCheckHost 参数** | **已修复** |
| **UpdateAppServerGroupPort** | **否→是** | **缺少 enableHealthCheck 和 healthCheckHost 参数** | **已修复** |
| DeleteAppServerGroupPort | 是 | 无问题 | - |
| CreateBlbRs | 是 | 无问题 | - |
| UpdateBlbRs | 是 | 无问题 | - |
| DescribeBlbRs | 是 | 无问题 | - |
| DeleteBlbRs | 是 | 无问题 | - |
| DescribeRsMount | 是 | 无问题 | - |
| DescribeRsUnMount | 是 | 无问题 | - |

---

## 3. 接口详细分析

### 3.1 CreateAppServerGroup (创建服务器组)

| 对比维度 | API 文档 | SDK 实现 | 一致性 |
|---------|---------|---------|--------|
| HTTP Method | POST | POST | ✅ |
| URL Path | /v1/appblb/{blbId}/appservergroup | /v1/appblb/{blbId}/appservergroup | ✅ |
| Query参数: clientToken | 是 | 是 | ✅ |
| Body参数: name | String, 可选 | String, 可选 | ✅ |
| Body参数: desc | String, 可选 | String, 可选 | ✅ |
| Body参数: backendServerList | List, 可选 | List, 可选 | ✅ |

**结论**: 无问题

---

### 3.2 UpdateAppServerGroup (更新服务器组)

| 对比维度 | API 文档 | SDK 实现 | 一致性 |
|---------|---------|---------|--------|
| HTTP Method | PUT | PUT | ✅ |
| URL Path | /v1/appblb/{blbId}/appservergroup | /v1/appblb/{blbId}/appservergroup | ✅ |
| Query参数: clientToken | 是 | 是 | ✅ |
| Body参数: sgId | String, 必填 | String, 必填 | ✅ |
| Body参数: name | String, 可选 | String, 可选 | ✅ |
| Body参数: desc | String, 可选 | String, 可选 | ✅ |

**结论**: 无问题

---

### 3.3 DescribeAppServerGroup (查询服务器组)

| 对比维度 | API 文档 | SDK 实现 | 一致性 |
|---------|---------|---------|--------|
| HTTP Method | GET | GET | ✅ |
| URL Path | /v1/appblb/{blbId}/appservergroup | /v1/appblb/{blbId}/appservergroup | ✅ |
| Query参数: name | String, 可选 | String, 可选 | ✅ |
| Query参数: exactlyMatch | Boolean, 可选 | Boolean, 可选 | ✅ |
| Query参数: marker | String, 可选 | String, 可选 | ✅ |
| Query参数: maxKeys | Integer, 可选 | Integer, 可选 | ✅ |

**结论**: 无问题

---

### 3.4 DeleteAppServerGroup (删除服务器组)

| 对比维度 | API 文档 | SDK 实现 | 一致性 |
|---------|---------|---------|--------|
| HTTP Method | PUT | PUT | ✅ |
| URL Path | /v1/appblb/{blbId}/appservergroup?delete | /v1/appblb/{blbId}/appservergroup?delete | ✅ |
| Query参数: clientToken | 是 | 是 | ✅ |
| Body参数: sgId | String, 必填 | String, 必填 | ✅ |

**结论**: 无问题

---

### 3.5 CreateAppServerGroupPort (创建服务器组端口) ⚠️ **已修复**

| 对比维度 | API 文档 | SDK 实现(修复前) | SDK 实现(修复后) | 一致性 |
|---------|---------|-----------------|-----------------|--------|
| HTTP Method | POST | POST | POST | ✅ |
| URL Path | /v1/appblb/{blbId}/appservergroupport | /v1/appblb/{blbId}/appservergroupport | /v1/appblb/{blbId}/appservergroupport | ✅ |
| Body参数: sgId | String, 必填 | ✅ | ✅ | ✅ |
| Body参数: port | Integer, 必填 | ✅ | ✅ | ✅ |
| Body参数: type | String, 必填 | ✅ | ✅ | ✅ |
| **Body参数: enableHealthCheck** | **Boolean, 可选** | **❌ 缺失** | **✅ 已添加** | ✅ |
| Body参数: healthCheck | String, 可选 | ✅ | ✅ | ✅ |
| Body参数: healthCheckPort | Integer, 可选 | ✅ | ✅ | ✅ |
| Body参数: healthCheckUrlPath | String, 可选 | ✅ | ✅ | ✅ |
| Body参数: healthCheckTimeoutInSecond | Integer, 可选 | ✅ | ✅ | ✅ |
| Body参数: healthCheckIntervalInSecond | Integer, 可选 | ✅ | ✅ | ✅ |
| Body参数: healthCheckDownRetry | Integer, 可选 | ✅ | ✅ | ✅ |
| Body参数: healthCheckUpRetry | Integer, 可选 | ✅ | ✅ | ✅ |
| Body参数: healthCheckNormalStatus | String, 可选 | ✅ | ✅ | ✅ |
| **Body参数: healthCheckHost** | **String, 可选** | **❌ 缺失** | **✅ 已添加** | ✅ |
| Body参数: udpHealthCheckString | String, 可选 | ✅ | ✅ | ✅ |

#### 问题描述 (P1)
- **问题1**: 缺少 `enableHealthCheck` 参数 (Boolean类型，是否启用健康检查，默认为true)
- **问题2**: 缺少 `healthCheckHost` 参数 (String类型，7层健康检查请求的Host头)

#### 修复方案
```python
# 在方法签名中添加参数
def create_app_server_group_port(self, blb_id, sg_id,
                                 port, protocol_type,
                                 enable_health_check=None,  # 新增
                                 health_check=None,
                                 ...
                                 health_check_host=None,    # 新增
                                 ...):

# 在body构建中添加逻辑
if enable_health_check is not None:
    body['enableHealthCheck'] = enable_health_check
if health_check_host is not None:
    body['healthCheckHost'] = compat.convert_to_string(health_check_host)
```

**修复状态**: ✅ 已修复

---

### 3.6 UpdateAppServerGroupPort (更新服务器组端口) ⚠️ **已修复**

| 对比维度 | API 文档 | SDK 实现(修复前) | SDK 实现(修复后) | 一致性 |
|---------|---------|-----------------|-----------------|--------|
| HTTP Method | PUT | PUT | PUT | ✅ |
| URL Path | /v1/appblb/{blbId}/appservergroupport | /v1/appblb/{blbId}/appservergroupport | /v1/appblb/{blbId}/appservergroupport | ✅ |
| Body参数: sgId | String, 必填 | ✅ | ✅ | ✅ |
| Body参数: portId | String, 必填 | ✅ | ✅ | ✅ |
| **Body参数: enableHealthCheck** | **Boolean, 可选** | **❌ 缺失** | **✅ 已添加** | ✅ |
| Body参数: healthCheck | String, 可选 | ✅ | ✅ | ✅ |
| Body参数: healthCheckPort | Integer, 可选 | ✅ | ✅ | ✅ |
| Body参数: healthCheckUrlPath | String, 可选 | ✅ | ✅ | ✅ |
| Body参数: healthCheckTimeoutInSecond | Integer, 可选 | ✅ | ✅ | ✅ |
| Body参数: healthCheckIntervalInSecond | Integer, 可选 | ✅ | ✅ | ✅ |
| Body参数: healthCheckDownRetry | Integer, 可选 | ✅ | ✅ | ✅ |
| Body参数: healthCheckUpRetry | Integer, 可选 | ✅ | ✅ | ✅ |
| Body参数: healthCheckNormalStatus | String, 可选 | ✅ | ✅ | ✅ |
| **Body参数: healthCheckHost** | **String, 可选** | **❌ 缺失** | **✅ 已添加** | ✅ |
| Body参数: udpHealthCheckString | String, 可选 | ✅ | ✅ | ✅ |

#### 问题描述 (P1)
与 CreateAppServerGroupPort 相同的问题：
- **问题1**: 缺少 `enableHealthCheck` 参数
- **问题2**: 缺少 `healthCheckHost` 参数

**修复状态**: ✅ 已修复

---

### 3.7 DeleteAppServerGroupPort (删除服务器组端口)

| 对比维度 | API 文档 | SDK 实现 | 一致性 |
|---------|---------|---------|--------|
| HTTP Method | PUT | PUT | ✅ |
| URL Path | /v1/appblb/{blbId}/appservergroupport?batchdelete | /v1/appblb/{blbId}/appservergroupport?batchdelete | ✅ |
| Query参数: clientToken | 是 | 是 | ✅ |
| Body参数: sgId | String, 必填 | String, 必填 | ✅ |
| Body参数: portIdList | List<String>, 必填 | List<String>, 必填 | ✅ |

**结论**: 无问题

---

### 3.8 CreateBlbRs (添加后端服务器)

| 对比维度 | API 文档 | SDK 实现 | 一致性 |
|---------|---------|---------|--------|
| HTTP Method | POST | POST | ✅ |
| URL Path | /v1/appblb/{blbId}/blbrs | /v1/appblb/{blbId}/blbrs | ✅ |
| Query参数: clientToken | 是 | 是 | ✅ |
| Body参数: sgId | String, 必填 | String, 必填 | ✅ |
| Body参数: backendServerList | List, 必填 | List, 必填 | ✅ |

**结论**: 无问题

---

### 3.9 UpdateBlbRs (更新后端服务器)

| 对比维度 | API 文档 | SDK 实现 | 一致性 |
|---------|---------|---------|--------|
| HTTP Method | PUT | PUT | ✅ |
| URL Path | /v1/appblb/{blbId}/blbrs | /v1/appblb/{blbId}/blbrs | ✅ |
| Query参数: clientToken | 是 | 是 | ✅ |
| Body参数: sgId | String, 必填 | String, 必填 | ✅ |
| Body参数: backendServerList | List, 必填 | List, 必填 | ✅ |

**结论**: 无问题

---

### 3.10 DescribeBlbRs (查询后端服务器)

| 对比维度 | API 文档 | SDK 实现 | 一致性 |
|---------|---------|---------|--------|
| HTTP Method | GET | GET | ✅ |
| URL Path | /v1/appblb/{blbId}/blbrs | /v1/appblb/{blbId}/blbrs | ✅ |
| Query参数: sgId | String, 必填 | String, 必填 | ✅ |
| Query参数: marker | String, 可选 | String, 可选 | ✅ |
| Query参数: maxKeys | Integer, 可选 | Integer, 可选 | ✅ |

**结论**: 无问题

---

### 3.11 DeleteBlbRs (删除后端服务器)

| 对比维度 | API 文档 | SDK 实现 | 一致性 |
|---------|---------|---------|--------|
| HTTP Method | PUT | PUT | ✅ |
| URL Path | /v1/appblb/{blbId}/blbrs?batchdelete | /v1/appblb/{blbId}/blbrs?batchdelete | ✅ |
| Query参数: clientToken | 是 | 是 | ✅ |
| Body参数: sgId | String, 必填 | String, 必填 | ✅ |
| Body参数: backendServerIdList | List<String>, 必填 | List<String>, 必填 | ✅ |

**结论**: 无问题

---

### 3.12 DescribeRsMount (查询已挂载服务器)

| 对比维度 | API 文档 | SDK 实现 | 一致性 |
|---------|---------|---------|--------|
| HTTP Method | GET | GET | ✅ |
| URL Path | /v1/appblb/{blbId}/blbrsmount | /v1/appblb/{blbId}/blbrsmount | ✅ |
| Query参数: sgId | String, 必填 | String, 必填 | ✅ |

**结论**: 无问题

---

### 3.13 DescribeRsUnMount (查询未挂载服务器)

| 对比维度 | API 文档 | SDK 实现 | 一致性 |
|---------|---------|---------|--------|
| HTTP Method | GET | GET | ✅ |
| URL Path | /v1/appblb/{blbId}/blbrsunmount | /v1/appblb/{blbId}/blbrsunmount | ✅ |
| Query参数: sgId | String, 必填 | String, 必填 | ✅ |

**结论**: 无问题

---

## 4. 修复记录

### 4.1 P1: 缺失参数修复

**修复文件**: `python/baidubce/services/blb/app_blb_client.py`

**修复内容**:
1. `create_app_server_group_port` 方法：添加 `enable_health_check` 和 `health_check_host` 参数
2. `update_app_server_group_port` 方法：添加 `enable_health_check` 和 `health_check_host` 参数

**代码变更位置**:
- `create_app_server_group_port`: 约第1993行
- `update_app_server_group_port`: 约第2114行

### 4.2 示例文件更新

**更新文件**:
- `python/sample/appblb/example_create_app_server_group_port.py`
- `python/sample/appblb/example_update_app_server_group_port.py`

**更新内容**:
- 添加了新参数 `enable_health_check` 和 `health_check_host` 的使用示例
- 展示了 TCP 和 HTTP 两种不同健康检查协议的配置方式

### 4.3 单元测试更新

**更新文件**: `python/test/blb/test_app_blb_client.py`

**更新内容**:
- `test_create_app_server_group_port`: 新增 HTTP 健康检查测试用例，覆盖 `enable_health_check` 和 `health_check_host` 参数
- `test_update_app_server_group_port`: 新增参数完整性测试用例

---

## 5. 结论

本次 Review 针对应用型BLB服务器组相关的 13 个接口进行了全面分析：

1. **接口覆盖率**: 100% (13/13 接口均已实现)
2. **发现问题**: 2 个 P1 级别问题 (均已修复)
   - `CreateAppServerGroupPort` 缺少 2 个 API 参数
   - `UpdateAppServerGroupPort` 缺少 2 个 API 参数
3. **修复完成率**: 100%
4. **配套更新**: 示例文件和单元测试均已同步更新

**当前状态**: SDK 实现与 API 文档完全一致 ✅