# RULE.md

本文件记录项目架构规则、合并标准与不可协商的边界。

## 总则

代码可以慢慢长，但职责不能乱。

本项目优先保证：

- 文件职责清晰
- 依赖方向稳定
- 外部 SDK 被隔离
- core 保持纯净
- infra 的脏活集中在 adapter
- 可验证、可拒收、可写进 CI

## 核心边界

```text
core
  定义规则、schema、protocol、通用错误

infra/provider_catalog
  声明身份

infra/adapters
  连接外部世界

infra/bootstrap
  装配组件与默认 runtime

application
  编排应用，只消费 core 契约
```

不允许为了方便跨层写代码。

## application 铁律

`application` 是流程编排层，不是 schema 层，也不是 infra 装配层。
这是硬边界：下次谁看到 application 层定义 schema，就应该立刻拦住；否则项目会严重失控。

允许：

- 调用 `ProviderManager`、`ContextBuilderProtocol`、`VectorManager` 等 core 契约
- 把 core schema 转换成下一步 core schema
- 编排 chat、embedding、indexing、retrieval、RAG、tool feedback loop
- 在 `application/bootstrap.py` 里用已注入的 core 对象/协议组装 `CyreneAIRuntime`

禁止：

- 定义 `CyreneAISchema` 或任何 Pydantic model
- import `pydantic`
- import `cyreneAI.infra`
- 创建 SQLite store、filesystem loader、provider adapter 等具体实现
- 注册默认 provider adapter

应用请求/结果模型放在 `src/cyreneAI/core/schema/application.py`。
带默认 provider、SQLite、filesystem skill loader 的便利 runtime 装配入口放在 `src/cyreneAI/infra/bootstrap/runtime.py`。

## provider catalog 目录铁律

`src/cyreneAI/infra/provider_catalog/` 只准放格式为 `{provider_name}_info.py` 的 py 文件。

允许：

```text
__init__.py
openai_compatible_info.py
deepseek_info.py
ollama_info.py
```

禁止：

```text
builder.py
instance.py
mapper.py
errors.py
register.py
setup.py
client.py
任何子目录
```

若出现其他文件，本人恕不接收该 pull request。

## adapter 规则

adapter 是唯一可以承担外部现实复杂度的地方。

允许 adapter：

- import 外部 SDK
- 创建和关闭 client
- 发真实请求
- 捕获外部异常
- 转换请求 payload
- 转换响应对象

adapter 必须把外部细节转换回 core 类型，不能把 SDK 类型向上传播到 application。

## mapper 规则

mapper 只做数据形状转换。

允许：

- `ChatRequest -> OpenAI-compatible payload`
- `ChatCompletion -> ChatResponse`
- `ToolDefinition -> tool payload`
- `finish_reason -> ChatFinishReason`
- `usage -> TokenUsage`

禁止：

- 创建 client
- 发请求
- 读取环境变量
- 注册 provider
- 捕获 SDK 异常

## errors 规则

errors 只做异常翻译。

```text
外部 SDK 异常 -> core provider 异常
```

禁止在 errors 层做：

- 重试
- 降级
- 日志系统绑定
- 业务判断

## instance 规则

instance 是 adapter 的运行对象。

允许：

- 持有 `ProviderConfig`
- 持有 `ProviderInfo`
- 持有外部 SDK client
- 实现 `close()`
- 实现 `chat()`

禁止：

- 声明 provider 身份常量
- 注册 factory
- 注册 registry
- 读取 `.env`

## bootstrap 规则

infra bootstrap 只负责装配。

允许：

- 把 `ProviderInfo` 注册到 `ProviderRegistry`
- 把 adapter builder 注册到 `ProviderFactory`
- 组合默认 runtime 所需的 infra 实现，例如 SQLite store、filesystem skill loader、默认 provider 注册

禁止：

- 发请求
- 创建业务流程
- 读取用户输入

`application/bootstrap.py` 不属于 infra bootstrap，不能 import `cyreneAI.infra`。

## ProviderConfig 规则

`ProviderConfig` 属于 core schema，只做通用配置形状约束。

允许：

- `provider_id` 形状
- `provider_type` 类型
- `timeout` 使用 `timedelta`
- 通用空值约束

禁止：

- 在 core 写某个 provider 专属规则
- 在 core 判断 OpenAI-compatible 是否必须有 api_key

provider 专属配置要求应在 adapter builder 或 instance 中处理。

## 验收标准

基础验证：

```bash
uv run python -m compileall src
uv run python -m pytest src/cyreneAI/tests
```

真实调用验证：

```bash
uv run python -m pytest -s src/cyreneAI/tests/test_openai_compatible_real_chat.py
```

看到真实模型返回，并通过测试，才算 openai-compatible 实际链路验收完成。
