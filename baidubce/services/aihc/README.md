# AIHC SDK 开发说明

## 概述

AIHC SDK采用模块化结构，提高了代码的可维护性和可扩展性。最新版本修复了IDE类型提示问题，确保开发体验更加友好。

### 项目结构
```
baidubce/services/aihc/
├── base/                          # 基础模块
│   ├── __init__.py
│   ├── aihc_base_client.py       # 基础客户端类
│   └── aihc_common.py            # 公共工具函数
├── modules/                       # 业务模块目录
│   ├── __init__.py
│   ├── job/                      # 任务模块
│   │   ├── __init__.py
│   │   └── job_client.py         # 任务相关接口
│   ├── dataset/                  # 数据集模块
│   │   ├── __init__.py
│   │   └── dataset_client.py     # 数据集相关接口
│   ├── model/                    # 模型模块
│   │   ├── __init__.py
│   │   └── model_client.py       # 模型相关接口
│   ├── service/                  # 在线服务模块
│   │   ├── __init__.py
│   │   └── service_client.py     # 服务相关接口
│   └── dev_instance/             # 开发机模块
│       ├── __init__.py
│       └── dev_instance_client.py # 开发机相关接口
├── aihc_client.py                # 重构后的主客户端文件
├── aihc_model.py                 # 保留原有模型文件
├── aihc_handler.py               # 保留原有处理器文件
├── aihc_client_original.py       # 原始文件备份
└── __init__.py                   # 主入口文件
```

## 模块说明

### 1. 基础模块 (base/)

#### aihc_base_client.py
- 提供基础客户端类 `AIHCBaseClient`
- 包含公共的请求发送方法
- 所有业务模块客户端都继承自此类

#### aihc_common.py
- 提供公共工具函数
- 包含请求参数和请求体构建的通用方法

### 2. 业务模块 (modules/)

#### 任务模块 (job/)
- **文件**: `job_client.py`
- **类**: `JobClient`
- **功能**: 训练任务相关接口
- **主要方法**:
  - `DescribeJobs()` - 查询训练任务列表
  - `DescribeJob()` - 查询训练任务详情
  - `CreateJob()` - 创建训练任务
  - `DeleteJob()` - 删除训练任务
  - `StopJob()` - 停止训练任务
  - `UpdateJob()` - 更新训练任务
  - `DescribeJobEvents()` - 查询训练任务事件
  - `DescribeJobLogs()` - 查询训练任务日志
  - `DescribeJobPodEvents()` - 查询训练任务Pod事件
  - `DescribeJobNodeNames()` - 查询训练任务所在节点列表
  - `GetJobWebTerminalUrl()` - 获取训练任务WebTerminal地址

#### 数据集模块 (dataset/)
- **文件**: `dataset_client.py`
- **类**: `DatasetClient`
- **功能**: 数据集相关接口
- **主要方法**:
  - `DescribeDatasets()` - 获取数据集列表
  - `DescribeDataset()` - 获取数据集详情
  - `CreateDataset()` - 创建数据集
  - `ModifyDataset()` - 修改数据集
  - `DeleteDataset()` - 删除数据集
  - `DescribeDatasetVersions()` - 获取数据集版本列表
  - `DescribeDatasetVersion()` - 获取数据集版本详情
  - `CreateDatasetVersion()` - 创建数据集版本
  - `DeleteDatasetVersion()` - 删除数据集版本

#### 模型模块 (model/)
- **文件**: `model_client.py`
- **类**: `ModelClient`
- **功能**: 模型相关接口
- **主要方法**:
  - `DescribeModels()` - 获取模型列表
  - `CreateModel()` - 创建模型
  - `DeleteModel()` - 删除模型
  - `ModifyModel()` - 修改模型
  - `DescribeModel()` - 获取模型详情
  - `DescribeModelVersions()` - 获取模型版本列表
  - `DescribeModelVersion()` - 获取模型版本详情
  - `CreateModelVersion()` - 新建模型版本
  - `DeleteModelVersion()` - 删除模型版本

#### 在线服务模块 (service/)
- **文件**: `service_client.py`
- **类**: `ServiceClient`
- **功能**: 在线服务部署相关接口
- **主要方法**:
  - `DescribeServices()` - 拉取服务列表
  - `DescribeService()` - 查询服务详情
  - `DescribeServiceStatus()` - 获取服务状态

#### 开发机模块 (dev_instance/)
- **文件**: `dev_instance_client.py`
- **类**: `DevInstanceClient`
- **功能**: 开发机相关接口
- **主要方法**:
  - `DescribeDevInstances()` - 查询开发机列表
  - `DescribeDevInstance()` - 查询开发机详情
  - `StartDevInstance()` - 开启开发机实例
  - `StopDevInstance()` - 停止开发机实例

## 使用方式

### 1. 使用主客户端（推荐）
```python
from baidubce.services.aihc import AihcClient
from baidubce.bce_client_configuration import BceClientConfiguration

# 创建配置
config = BceClientConfiguration()
config.endpoint = 'https://aihc.bj.baidubce.com'

# 创建客户端
client = AihcClient(config)

# 使用各种接口
client.DescribeJobs(resourcePoolId='your-pool-id')
client.DescribeDatasets()
client.DescribeModels()
```

### 2. 使用独立模块客户端
```python
from baidubce.services.aihc.modules.job import JobClient
from baidubce.services.aihc.modules.dataset import DatasetClient

# 创建配置
config = BceClientConfiguration()
config.endpoint = 'https://aihc.bj.baidubce.com'

# 使用特定模块
job_client = JobClient(config)
dataset_client = DatasetClient(config)

# 调用模块特定方法
job_client.DescribeJobs(resourcePoolId='your-pool-id')
dataset_client.DescribeDatasets()
```

### 3. 直接访问子模块（新特性）
```python
from baidubce.services.aihc import AihcClient

# 创建客户端
client = AihcClient(config)

# 直接访问子模块
client.job.DescribeJobs(resourcePoolId='your-pool-id')
client.dataset.DescribeDatasets()
client.model.DescribeModels()
client.service.DescribeServices()
client.dev_instance.DescribeDevInstances()
```

## 最新改进

### 1. IDE类型提示优化
- **问题**: 之前IDE中方法参数显示为 `any`
- **解决方案**: 使用 `create_typed_proxy_method` 函数确保完整的类型信息传递
- **效果**: 现在IDE正确显示方法签名，如 `DescribeDataset(datasetId: str)`

### 2. 属性名称优化
- **变更**: 子模块属性名称更简洁
  - `job_client` → `job`
  - `dataset_client` → `dataset`
  - `model_client` → `model`
  - `service_client` → `service`
  - `dev_instance_client` → `dev_instance`

### 3. 避免重复注释
- **改进**: 使用代理方法自动继承子模块的完整注释和类型注解
- **优势**: 避免在 `AihcClient` 中重复子模块的注释，维护更简单

## 优势

### 1. 模块化
- 不同业务模块独立开发，降低耦合
- 单一职责，代码结构清晰

### 2. 可维护性
- 每个模块文件大小适中，易于维护
- 问题定位更精确

### 3. 可扩展性
- 新增模块只需添加新的子模块
- 不影响现有模块

### 4. 团队协作
- 不同团队可以并行开发不同模块
- 减少代码冲突

### 5. 可测试性
- 每个模块可以独立测试
- 测试覆盖更全面

### 6. 开发体验
- IDE类型提示完整准确
- 代码补全和错误检查更有效
- 文档字符串自动继承

## 开发规范

### 1. 新增模块
1. 在 `modules/` 目录下创建新的模块目录
2. 创建 `__init__.py` 和模块客户端文件
3. 在 `aihc_client.py` 中添加代理方法
4. 更新相关文档

### 2. 类型注解规范
- 所有公共方法必须包含完整的类型注解
- 使用 `typing` 模块的类型提示
- 确保文档字符串与类型注解一致

### 3. 代理方法规范
- 使用 `create_typed_proxy_method` 函数创建代理方法
- 确保类型信息和文档字符串正确传递
- 避免重复注释

### 4. 版本管理
- 每个模块可以独立版本管理
- 主客户端版本号反映所有模块的兼容性

## 故障排除

### IDE类型提示问题
如果IDE仍然显示 `any`，请尝试：
1. 重启IDE
2. 清除IDE缓存
3. 重新加载项目
4. 检查Python语言服务器状态

### 模块导入问题
确保正确导入模块：
```python
# 正确的导入方式
from baidubce.services.aihc import AihcClient
```

## 单元测试

运行测试脚本验证模块化改造：
```bash
python test_modular_aihc.py
```

## 更新日志

### v2.1.0 (最新)
- ✅ 修复IDE类型提示问题
- ✅ 优化子模块属性名称
- ✅ 避免重复注释
- ✅ 改进代理方法实现
- ✅ 更新文档和示例

### v2.0.0
- ✅ 完成模块化重构
- ✅ 实现代理方法机制
- ✅ 添加完整文档
