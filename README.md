# AI-Agent 学习路径

从 Python 基础到 RAG、Agent、LangGraph 与 Web 服务落地的渐进式学习仓库。每个目录是一个独立模块，按编号顺序循序渐进，其中 `03`、`07`、`10` 是可直接运行的完整项目演练。

---

## 技术栈

| 类别 | 选型 |
| --- | --- |
| 大模型 | 阿里云百炼 / DashScope（通义千问 `qwen` 系列） |
| Agent 框架 | LangChain 1.x、LangGraph 1.x、LlamaIndex 0.14 |
| 向量库 | Chroma（本地持久化） |
| 嵌入模型 | `text-embedding-v4`（DashScope） |
| Web / 界面 | Streamlit（演示界面）、FastAPI（后端服务） |
| 存储 | MySQL（SQLAlchemy 异步）、Redis、SQLite |
| 低代码平台 | Coze、Dify |

---

## 环境准备

### 1. Python 版本

```
Python 3.11+
```

> 注意：`09.fastApi` 与 `10.新闻头条---fastApi` 各自带有独立的 `pyproject.toml`，声明 `requires-python >= 3.14`，使用 [uv](https://docs.astral.sh/uv/) 单独管理依赖。

### 2. 创建虚拟环境并安装依赖

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

`09` / `10` 两个子项目单独安装：

```bash
cd 10.新闻头条---fastApi
uv sync
```

### 3. 配置模型密钥

本仓库有两套密钥入口，按模块不同使用：

**（A）DashScope 环境变量** — `ChatTongyi` / `DashScopeEmbeddings` 依赖，覆盖 `03`、`05`~`08`、`10` 等大部分模块：

```bash
# Windows PowerShell
setx DASHSCOPE_API_KEY "sk-xxxxxxxx"
```

**（B）`Config/load_key.py`** — OpenAI 兼容接口，供 `02.RAG`、`04.LlamaIndex` 使用：

```python
open_key  = 'sk-xxxxxxxx'                                    # 百炼 API Key
base_url  = 'https://xxx.aliyuncs.com/compatible-mode/v1'    # OpenAI 兼容地址
base_model = 'qwen3-max'                                     # 默认模型
```

**（C）可选** — `08.langGraph/.env` 用于 LangSmith 追踪与 Tavily 搜索：

```
LANGSMITH_PROJECT=
LANGSMITH_API_KEY=
LANGSMITH_TRACING=
LANGSMITH_ENDPOINT=
TAVILY_API_KEY=
```

> ⚠️ **安全提醒**：`Config/load_key.py` 和 `08.langGraph/.env` 目前含有真实密钥且已被 Git 跟踪。建议尽快撤销这些 Key，并把两者加入 `.gitignore`，改用 `load_key.example.py` / `.env.example` 作为模板提交。

---

## 目录结构

| 目录 | 内容 | 说明 |
| --- | --- | --- |
| `01.Python` | Python 基础 | 数据类型、函数、面向对象（封装/继承/多态）、爬虫、正则、CSV、Jupyter |
| `02.RAG` | RAG 与 LangChain 入门 | OpenAI 调用、流式输出、提示词模板、Chain 链、输出解析器、记忆、文档加载器、向量存储与检索 |
| `03.RAG项目演练---客服电商问答系统` | 🚀 **项目一** | 完整 RAG 问答系统：知识库入库去重（MD5）、Chroma 持久化、带历史的检索链、Streamlit 双页面 |
| `04.LlamaIndex` | LlamaIndex 组件 | Prompt / Models / Loading / Index / Storing / Querying 六大组件 + RAG 自动化评测（Notebook） |
| `05.langchain` | LangChain 进阶 | Tool、Memory、多模态、Context & State、Multi-Agent、Middleware、Human-in-the-loop、动态 Agent、MCP 服务 |
| `06.Agent` | Agent 基础 | 智能体初体验、流式输出、ReAct 流程、Middleware 中间件 |
| `07.Agent项目演练---智能客服系统` | 🚀 **项目二** | 分层架构的 ReAct 智能客服：`agent` / `model` 工厂 / `rag` / `config`(YAML) / `prompts` / `utils`(日志·配置·路径) |
| `08.langGraph` | LangGraph 全家桶 | 图构建、路由、状态管理与还原、消息裁剪、并行、子图、MapReduce、Time Travel、Store 长期记忆、研究助理 |
| `09.fastApi` | FastAPI 基础 | 中间件、依赖注入、异步 ORM（SQLAlchemy + aiomysql） |
| `10.新闻头条---fastApi` | 🚀 **项目三** | 生产级 FastAPI 服务：路由 / CRUD / Schema / 模型分层，JWT 鉴权、Redis 缓存、统一响应与异常处理、AI 对话接口 |
| `12.coze&dify` | 低代码平台案例 | Coze：商品宣传视频、营销卖点提炼；Dify：投诉分类助手（钉钉/飞书）、商品评论分析（含可导入 `.yml`） |
| `13.Deep Agents` | 规划中 | 目录为空，待补充 |
| `Config` | 全局配置 | `load_key.py`：模型 Key / base_url / 默认模型 |

> 编号 `11` 已跳过。

---

## 快速开始

### 项目一：电商客服 RAG 问答系统

```bash
cd 03.RAG项目演练---客服电商问答系统

streamlit run app_file_upload.py   # 知识库上传（txt），自动分块入库并 MD5 去重
streamlit run app_qa.py            # 问答界面，流式输出 + 会话记忆
```

关键参数在 `config_data.py`：`chunk_size=1000`、`chunk_overlap=50`、中英文混合分隔符、Chroma 集合 `rag-chroma-db`。

### 项目二：ReAct 智能客服系统

```bash
cd 07.Agent项目演练---智能客服系统
streamlit run app.py
```

模型与知识库配置在 `config/*.yaml`（`rag.yaml` 指定对话模型与嵌入模型），提示词在 `prompts/`，运行日志写入 `logs/`。

### 项目三：新闻头条 API 服务

前置依赖：MySQL（库名 `news_app`）与 Redis 均运行在本机默认端口。

```bash
cd 10.新闻头条---fastApi
uv run uvicorn main:app --reload
```

访问 `http://127.0.0.1:8000/docs` 查看接口文档，`test_main.http` 提供了可直接发起的请求样例。

> 数据库连接串与 Redis 地址目前硬编码在 `config/db_conf.py`、`config/cache_conf.py`，本机环境不一致时需自行修改。

### 单文件示例

`01`、`02`、`05`、`06`、`08` 下的脚本均可独立运行：

```bash
python 08.langGraph/04graph_agent.py
```

`04.LlamaIndex` 为 Notebook，用 Jupyter 打开：

```bash
jupyter notebook 04.LlamaIndex
```

---

## 建议学习顺序

```
01 Python 基础
      ↓
02 RAG / LangChain 入门 ──→ 03 项目演练：电商客服问答
      ↓
04 LlamaIndex（另一套 RAG 实现思路）
      ↓
05 LangChain 进阶 ──→ 06 Agent 基础 ──→ 07 项目演练：智能客服
      ↓
08 LangGraph（复杂编排 / 长期记忆）
      ↓
09 FastAPI 基础 ──→ 10 项目演练：新闻头条服务化
      ↓
12 Coze & Dify（低代码对照）
```

---

## 已知问题

- `Config/load_key.py`、`08.langGraph/.env`、`08.langGraph/15_research_assistant.py` 中存在明文密钥且已提交至版本库，需清理。
- `requirements.txt` 为 UTF-16 编码，用文本编辑器打开可能显示异常（pip 可正常读取）。
- `09` / `10` 声明的 Python 版本（3.14+）与根目录（3.11+）不一致。
- 部分模块的数据库地址、Redis 地址为硬编码，未走配置文件或环境变量。
