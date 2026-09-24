# AI-Agent 学习与实践

从 Python 基础出发，逐步学习 RAG、Agent、LangGraph、Deep Agents 与 FastAPI 服务开发，并扩展到 Dart / Flutter 客户端实践。

仓库按主题保存学习笔记、单文件示例、Notebook 和项目演练，适合边阅读、边运行、边修改。各模块按需配置环境，没有统一的应用启动入口；部分功能仍处于学习和开发阶段。

## 导航

- [学习路线](#学习路线)
- [目录索引](#目录索引)
- [技术栈](#技术栈)
- [环境与模型配置](#环境与模型配置)
- [项目运行](#项目运行)
- [Notebook 与单文件示例](#notebook-与单文件示例)
- [Dart 与 Flutter](#dart-与-flutter)
- [常见问题与当前限制](#常见问题与当前限制)

## 学习路线

| 阶段 | 学习内容 | 对应模块 |
| --- | --- | --- |
| 语言基础 | 数据类型、函数、面向对象、文件处理 | `01.Python` |
| 检索增强 | 模型调用、提示词、文档分块、嵌入与向量检索 | `02.RAG` → `03` 电商客服 → `04.LlamaIndex` |
| 智能体 | 工具调用、ReAct、状态、中间件、多智能体 | `06.Agent` 入门 → `05.langchain` 进阶 → `07` 智能客服 |
| 复杂编排 | 图工作流、检查点、长期记忆、规划、子代理 | `08.langGraph` → `13.Deep Agents` |
| 服务开发 | HTTP 接口、异步数据库、鉴权、缓存 | `09.fastApi` → `10` 新闻头条 |
| 低代码实践 | 工作流搭建、业务集成、DSL 导入 | `12.coze&dify` |
| 客户端扩展 | Dart、Flutter 组件、网络请求、状态管理 | `15.Fullter` |

初次接触 AI 应用可先完成 `02` 和 `03`，再进入 Agent 与图编排。Flutter 是独立的客户端学习方向；当前商城使用自己的教学接口，并未与新闻头条 API 集成。

## 目录索引

| 目录 | 主题 | 已有内容 |
| --- | --- | --- |
| [01.Python](01.Python/) | Python 基础 | 集合、函数、类、封装 / 继承 / 多态、爬虫、正则、CSV、Jupyter |
| [02.RAG](02.RAG/) | RAG 与 LangChain 入门 | OpenAI 兼容接口、流式输出、提示词模板、Chain、输出解析、记忆、文档加载、向量存储与检索 |
| [03.RAG项目演练---客服电商问答系统](03.RAG项目演练---客服电商问答系统/) | 电商客服项目 | TXT 上传、文本分块、MD5 去重、Chroma 持久化、带历史的问答、Streamlit 界面 |
| [04.LlamaIndex](04.LlamaIndex/) | LlamaIndex | 8 个 Notebook，覆盖提示词、模型、加载、索引、存储、查询和 RAG 评测 |
| [05.langchain](05.langchain/) | LangChain 进阶 | Tool、Memory、多模态、Context / State、多智能体、中间件、人工介入、动态 Agent、MCP 示例 |
| [06.Agent](06.Agent/) | Agent 入门 | 智能体创建、流式输出、ReAct 流程、中间件 |
| [07.Agent项目演练---智能客服系统](07.Agent项目演练---智能客服系统/) | ReAct 客服项目 | 知识库检索、工具调用、使用记录查询、报告提示词、YAML 配置、日志 |
| [08.langGraph](08.langGraph/) | LangGraph | 路由、状态与检查点、消息裁剪、并行、子图、MapReduce、Time Travel、长期记忆、研究助理 |
| [09.fastApi](09.fastApi/) | FastAPI 基础 | 中间件、依赖注入、SQLAlchemy 异步 ORM、图书 CRUD 示例 |
| [10.新闻头条---fastApi](10.新闻头条---fastApi/) | 新闻 API 项目 | 用户注册登录、JWT、新闻查询、Redis 缓存、统一响应、AI 对话与记忆代码 |
| [12.coze&dify](12.coze%26dify/) | 低代码案例 | 商品宣传视频、营销卖点、投诉分类（钉钉 / 飞书）、评论分析、Dify `.yml` 工作流 |
| [13.Deep Agents](13.Deep%20Agents/) | Deep Agents 原理实践 | 5 个 Notebook，逐步实现状态、待办清单、虚拟文件系统、子代理与综合研究助手 |
| [15.Fullter](15.Fullter/) | Dart / Flutter | Dart 基础、Flutter 组件练习、商城项目、Android / iOS / HarmonyOS 配置笔记 |
| [Config](Config/) | 共用模型配置 | `load_key.py` 提供 `open_key`、`base_url`、`base_model`，供部分 Notebook 导入 |

编号 `11` 未使用。`14.langchain&&langgraph&&deep Agent` 目前仅为本地空目录，暂无已提交内容；Git 克隆不会带出空目录。`15.Fullter`、`fluttter_base` 保留仓库现有拼写，执行命令时请按实际名称填写。

## 技术栈

以下为仓库已声明或使用的技术，并非各工具的最新版本清单。

| 类别 | 使用情况 |
| --- | --- |
| 模型接入 | 阿里云百炼 / DashScope、通义千问、OpenAI 兼容接口；部分示例使用 Ollama |
| Agent 与编排 | 根依赖包含 LangChain `1.2.15`、LangGraph `1.1.9` |
| RAG | LlamaIndex `0.14.23`、Chroma `1.5.8`、DashScope 文本嵌入模型 |
| Python 界面与服务 | Streamlit、FastAPI、Uvicorn、Pydantic |
| 数据与记忆 | MySQL、SQLAlchemy、aiomysql、Redis、SQLite、LangGraph Checkpointer / Store |
| 搜索与观测 | Tavily、LangSmith，按示例需要配置 |
| 客户端 | Dart、Flutter、Dio、GetX、SharedPreferences |
| 低代码 | Coze、Dify |

依赖以根目录 [requirements.txt](requirements.txt)、`09` / `10` 的 `pyproject.toml` 与 `uv.lock`、Flutter 子项目的 `pubspec.yaml` 与 `pubspec.lock` 为准。

## 环境与模型配置

### 1. 获取代码与选择环境

```bash
git clone https://github.com/ty0826/AI-Agent.git
cd AI-Agent
```

| 模块 | 环境说明 |
| --- | --- |
| 根目录 Python 示例 | 使用独立虚拟环境安装 `requirements.txt`；尚无统一的全仓库 Python 版本约束 |
| `09.fastApi`、`10.新闻头条---fastApi` | 各自声明 Python `>=3.14`，使用 uv 管理独立环境 |
| `04.LlamaIndex`、`13.Deep Agents` | 需要 Jupyter 或 IDE Notebook 支持，并选择安装了对应依赖的 Python 内核 |
| `15.Fullter/flutter_study` | `pubspec.yaml` 声明 Dart `^3.12.2` |
| `15.Fullter/hm_shop` | 当前声明 Dart `^3.9.2`，并使用适配 HarmonyOS 的插件来源 |

`08.langGraph/langgraph.json` 仍声明 Python `3.11`，与 FastAPI 子项目不同。请按所学模块选择解释器，不要将某个配置文件的版本视为全仓库兼容范围。

### 2. 安装 Python 示例依赖

在仓库根目录执行。Windows PowerShell：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

macOS / Linux：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

需要 Notebook 界面时另行安装：

```bash
python -m pip install jupyterlab
```

根依赖清单为 UTF-16 编码。它是学习环境的依赖快照，尚未覆盖所有示例额外使用的库；FastAPI 和 Flutter 子项目应分别安装依赖，具体见下文。

### 3. 配置模型与搜索服务

仓库尚未统一配置入口，运行前先确认目标脚本使用哪种方式：

| 入口 | 适用示例 | 配置方式 |
| --- | --- | --- |
| `DASHSCOPE_API_KEY` | `ChatTongyi`、`DashScopeEmbeddings`，包括 `03`、`07` 等 | 设置当前终端环境变量 |
| `OPENAI_API_KEY` | 未显式传入 `api_key` 的 `OpenAI` / `ChatOpenAI` | 填入与代码中 `base_url` 匹配的服务商密钥 |
| `Config/load_key.py` | `04.LlamaIndex`、`13.Deep Agents` 中的模型示例 | 设置 `open_key`、`base_url`、`base_model` |
| 脚本内的显式参数 | 部分 LangGraph 示例、`10` 的 `crud/chat.py` | 修改其模型初始化代码；只设置环境变量不会覆盖显式密钥 |
| Tavily / LangSmith | 搜索工具、研究助手、调用追踪 | 按示例配置 `TAVILY_API_KEY`、`LANGSMITH_API_KEY` 等 |

Windows PowerShell 示例，仅对当前终端及其子进程生效：

```powershell
$env:DASHSCOPE_API_KEY = "your-dashscope-api-key"
$env:OPENAI_API_KEY = "your-openai-compatible-api-key"
```

macOS / Linux 对应使用 `export`：

```bash
export DASHSCOPE_API_KEY="your-dashscope-api-key"
export OPENAI_API_KEY="your-openai-compatible-api-key"
```

`Config/load_key.py` 的三个变量应分别对应自己的密钥、服务接入地址和可用模型。若在本地改为读取环境变量，可采用以下形式；这属于配置修改示例，当前文件仍使用常量：

```python
import os

open_key = os.environ["OPENAI_API_KEY"]
base_url = os.environ["MODEL_BASE_URL"]
base_model = os.environ["MODEL_NAME"]
```

LangGraph CLI 的 `langgraph.json` 指向 `08.langGraph/.env`，其中使用 `LANGSMITH_PROJECT`、`LANGSMITH_API_KEY`、`LANGSMITH_TRACING`、`LANGSMITH_ENDPOINT` 和 `TAVILY_API_KEY`。直接执行 Python 脚本时，应检查脚本是否加载 `.env`，或改在启动终端设置这些变量。

> 部分已跟踪配置和脚本含有硬编码凭据。请使用自己的密钥；已公开的凭据应撤销或轮换，并清理代码及历史记录。仅加入 `.gitignore` 不会移除已跟踪文件或历史中的密钥。

## 项目运行

下列各节的 `cd` 命令均以仓库根目录为起点。Python 界面项目先激活根目录虚拟环境；FastAPI 子项目在各自目录使用 uv。

### 电商客服 RAG 问答系统

目录：[`03.RAG项目演练---客服电商问答系统`](03.RAG项目演练---客服电商问答系统/)。配置 `DASHSCOPE_API_KEY` 后，先启动上传界面：

```bash
cd "03.RAG项目演练---客服电商问答系统"
python -m streamlit run app_file_upload.py --server.port 8501
```

上传 UTF-8 编码的 `.txt` 文件，可先使用 `data/` 下的尺码、颜色和洗涤养护资料。在另一个已激活同一环境的终端进入该目录，再启动问答界面：

```bash
python -m streamlit run app_qa.py --server.port 8502
```

上传页为 `http://localhost:8501`，问答页为 `http://localhost:8502`。上传端负责分块、嵌入、MD5 去重与持久化；问答端读取同一向量库，结合历史消息生成流式回复。

配置文件为 [config_data.py](03.RAG项目演练---客服电商问答系统/config_data.py)：默认分块长度 `1000`、重叠 `50`，集合名 `rag-chroma-db`，数据目录 `chroma-rag-db/`，会话 ID 为 `user_001`。

### ReAct 智能客服系统

目录：[`07.Agent项目演练---智能客服系统`](07.Agent项目演练---智能客服系统/)。同样需要 `DASHSCOPE_API_KEY`：

```bash
cd "07.Agent项目演练---智能客服系统"
python -m streamlit run app.py
```

启动时会扫描 `data/` 中允许的知识文件，并按 MD5 去重入库。主要配置和实现位置：

| 位置 | 用途 |
| --- | --- |
| `config/rag.yaml` | 对话模型、嵌入模型；对话模型字段保留代码中的 `chart_model_name` 拼写 |
| `config/chroma.yaml` | 集合、持久化路径、检索数量、分块参数；默认允许 TXT / PDF / JSON |
| `config/agent.yaml` | 使用记录 CSV 路径 |
| `prompts/` | 主提示词、RAG 总结、报告提示词 |
| `agent/`、`rag/`、`model/` | Agent 编排、检索服务、模型工厂 |
| `logs/` | 运行日志 |

天气、定位、用户 ID 等工具包含固定或随机返回的演示数据，适合学习工具调用流程。

### FastAPI 基础示例

`09.fastApi/main.py` 使用 MySQL，运行前创建 `fastapi_test` 数据库，并调整代码中的连接参数。启动时会尝试创建图书表。

```bash
cd "09.fastApi"
uv sync
uv run --with sqlalchemy --with aiomysql uvicorn main:app --reload
```

这里使用 `--with` 补充 `main.py` 导入、但当前 `pyproject.toml` 未声明的 ORM 依赖。接口文档地址为 `http://127.0.0.1:8000/docs`。

### 新闻头条 API 服务

目录：[`10.新闻头条---fastApi`](10.新闻头条---fastApi/)。这是学习用的分层后端项目，运行前需要准备以下资源：

1. MySQL：创建 `news_app` 数据库，并在 `config/db_conf.py` 设置连接参数。
2. 数据表：根据 `models/user.py` 和 `models/news.py` 初始化 `user`、`user_token`、`news_category`、`news`。两份模型使用不同的 `Base`；当前入口没有自动建表流程，也未提供迁移和初始新闻数据脚本。
3. Redis：在 `config/cache_conf.py` 配置连接。AI 记忆使用 `RedisSaver` / `RedisStore`，需具备 JSON 与 Search 能力；详见 [langgraph-redis 的依赖说明](https://github.com/redis-developer/langgraph-redis#redis-modules-requirements)。
4. 模型：检查 `crud/chat.py` 的 `ChatOpenAI` 初始化，替换其中的显式密钥、服务地址和模型。
5. JWT：在启动终端设置自己的 `JWT_SECRET_KEY`，避免使用代码内的默认值。

在上述资源就绪后，Windows PowerShell 启动示例：

```powershell
cd "10.新闻头条---fastApi"
uv sync
$env:JWT_SECRET_KEY = "replace-with-your-own-random-secret"
uv run --with passlib --with "bcrypt<4" uvicorn main:app --reload
```

当前子项目未声明 `utils/security.py` 所需的 Passlib / bcrypt，因此命令临时补充依赖，并限制 bcrypt 版本以适配现有 Passlib 调用。上述额外依赖不会写回 `pyproject.toml` 或锁文件。

访问 `http://127.0.0.1:8000/docs` 查看实际接口定义。常用路由如下：

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| POST | `/api/users/register` | 用户注册 |
| POST | `/api/users/login` | 登录并取得 Token |
| POST | `/api/users/user_info` | 获取用户信息 |
| POST | `/api/news/category` | 新闻分类 |
| POST | `/api/news/news_list` | 新闻列表 |
| POST | `/api/news/news_details` | 新闻详情 |
| POST | `/chatAi/chat` | AI 对话入口，仍需完善和验证 |

受保护的 `/api` 请求需要 `Authorization: Bearer <token>`。`/chatAi/chat` 当前不在这一鉴权前缀内；其实现还存在对同步 `graph.invoke()` 使用 `await` 的问题，不能视为已验证可用的异步对话接口。服务导入聊天模块时就会初始化 Redis，启动前必须先准备 Redis。

`test_main.http` 仍是 `/`、`/hello/User` 模板请求，不能作为当前业务接口的测试集合。

## Notebook 与单文件示例

### LlamaIndex 与 Deep Agents

在仓库根目录、已激活的 Python 环境中启动 JupyterLab。Notebook 的工作目录通常在其所在文件夹，下面将根目录加入模块搜索路径，便于导入 `Config`。

Windows PowerShell：

```powershell
$repoRoot = (Get-Location).Path
$env:PYTHONPATH = "$repoRoot;$env:PYTHONPATH"
python -m jupyterlab
```

macOS / Linux：

```bash
export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}"
python -m jupyterlab
```

进入 `04.LlamaIndex` 或 `13.Deep Agents`，选择对应虚拟环境的 Python 内核，并按单元格顺序执行。部分 Notebook 的历史内核元数据仍为 Python 2.7，请勿据此选择运行环境。

`13.Deep Agents` 使用 LangChain / LangGraph 逐步实现 Deep Agents 的核心机制，当前 Notebook 没有直接导入 `deepagents` 包：

| Notebook | 学习重点 |
| --- | --- |
| `01.create_Agent.ipynb` | Agent 状态、工具调用、状态更新 |
| `02.todo_agent.ipynb` | 结构化待办清单、任务读写 |
| `03.file_agent.ipynb` | 状态内的虚拟文件系统：列出、读取和写入文件 |
| `04.sub_agent.ipynb` | 子代理定义、任务委托与上下文隔离 |
| `05.full_agent.ipynb` | 整合 Tavily 搜索、网页摘要、文件、待办与子代理 |

`02` 至 `04` 的搜索示例使用预设结果；`05` 才接入 Tavily。运行综合示例前补充依赖：

```bash
python -m pip install tavily-python markdownify
```

`05.full_agent.ipynb` 当前写有 `TavilyClient(api_key="")`，需先修改该单元格，例如导入 `os` 后改为 `TavilyClient(api_key=os.environ["TAVILY_API_KEY"])`，并在启动 Jupyter 的终端设置密钥。虚拟文件保存在 Agent 状态中，不等同于写入本地磁盘。

### 单文件与低代码案例

单文件示例先进入对应模块，检查模型、数据路径和额外依赖，再运行目标脚本，例如：

```bash
cd "08.langGraph"
python 04graph_agent.py
```

部分示例依赖外部文件、搜索服务、Ollama 或本地服务，不能假定每个脚本在仅安装根依赖后都能直接运行。

`12.coze&dify` 以案例说明、素材和工作流文件为主。按各案例 Markdown 操作；导入 Dify `.yml` 后，需要重新配置自己的模型供应商、知识库及钉钉 / 飞书等集成信息。

## Dart 与 Flutter

| 子目录 | 内容 | 使用方式 |
| --- | --- | --- |
| [fluttter_base](15.Fullter/fluttter_base/) | 变量、空安全、集合、流程控制、函数、类、混入、泛型、异步及语言对比笔记 | 使用 Dart 执行单文件 |
| [flutter_study](15.Fullter/flutter_study/) | 组件、生命周期、布局、滚动、父子通信、Dio、路由 | 默认入口或 `--target` 指定练习 |
| [hm_shop](15.Fullter/hm_shop/) | 商城首页、登录、个人中心、请求封装、Token 存储、GetX 状态管理 | Flutter 项目，含 HarmonyOS 配置 |

### Dart 基础

```bash
dart run "15.Fullter/fluttter_base/01.声明变量_var.dart"
```

### Flutter 组件练习

先安装满足该子项目 Dart 约束的 Flutter SDK，确认 Chrome 可用后执行：

```bash
cd "15.Fullter/flutter_study"
flutter doctor -v
flutter pub get
flutter run -d chrome
```

`lib/main.dart` 当前是路由练习。也可以在同一目录指定其他包含 `main()` 的练习文件：

```bash
flutter run -d chrome --target "lib/01.materialapp_基本使用.dart"
```

### 商城项目

先阅读 [hm_shop 环境说明](15.Fullter/hm_shop/README.md)。当前 `pubspec.yaml` 的 `shared_preferences` 来自 OpenHarmony 适配仓库，需按目标平台准备匹配的 Flutter SDK、原生工具链和依赖。

```bash
cd "15.Fullter/hm_shop"
flutter doctor -v
flutter pub get
flutter devices
flutter run -d <device-id>
```

将 `<device-id>` 替换为设备列表中的实际 ID。Windows 上运行 HarmonyOS 版本时，还需按子项目说明配置与项目同盘的 `PUB_CACHE`。

接口地址集中在 `lib/viewmodels/api.dart`，请求封装位于 `lib/api/request.dart`。当前首页、登录和个人中心已有实现，分类与购物车页面仍以占位内容为主，尚未形成完整下单流程。

## 常见问题与当前限制

| 现象 | 检查方向 |
| --- | --- |
| 模型鉴权失败或模型不可用 | 检查实际初始化入口；显式 `api_key` 不会被环境变量替换，密钥、服务地址与模型需匹配 |
| `No module named Config` | 从根目录设置 `PYTHONPATH` 后启动 Notebook；已运行的内核需重启 |
| 安装后仍提示缺少模块 | 确认终端和 IDE 使用同一解释器；根依赖与子项目依赖并未覆盖所有示例 |
| TXT 上传解码失败 | 将文件转为 UTF-8；上传界面当前只接受 `.txt` |
| 知识库为空或新资料未入库 | 检查资料路径、允许的扩展名、MD5 记录和向量库路径；重建时应同步处理对应索引与去重记录 |
| MySQL 报连接或表不存在 | 检查数据库账号、库名与表结构；新闻项目不会在启动时自动建表 |
| Redis 报 JSON / Search 相关命令或索引错误 | 确认服务具备 AI 记忆组件所需能力，并与 `config/cache_conf.py` 配置一致 |
| Flutter 依赖或构建失败 | 核对所在子项目的 Dart 约束、Flutter SDK 来源、目标平台和插件适配情况 |

仓库目前保留了部分向量库、会话记录、日志和 Notebook 输出；复现实验时应检查这些已有状态。调用模型或搜索服务会使用自己的服务额度。

后续可继续完善各模块的最小依赖、无敏感值的配置模板、新闻项目的迁移与接口测试，以及商城的分类、购物车和交易流程。欢迎通过 Issue 反馈问题；提交时请附上模块名称、运行命令、解释器或 SDK 版本及已脱敏的错误信息。
