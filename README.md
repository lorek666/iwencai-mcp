<!-- iwencai-mcp -->
<h1 align="center">🔍 iwencai-mcp</h1>
<p align="center"><strong>同花顺问财 · 通用 MCP Server</strong></p>
<p align="center">让 AI 助手（Claude / DeepSeek / Cursor）直接帮你查股票、看财报、搜公告、筛板块</p>

---

## 🤔 这是什么？

**iwencai-mcp** 是一个"桥梁"——它把同花顺问财的 12 个金融数据查询能力，打包成 AI 助手能直接调用的工具。

简单说：配置好之后，你可以直接对 AI 说「帮我查一下茅台的最新财报」「今天涨幅超过 5% 的 AI 概念股有哪些」「最近有什么降息政策新闻」，AI 会实时从同花顺问财拉取数据回答你。

> 💡 **不需要写代码，不需要懂 API。** 跟着文档配置一次，之后直接用自然语言提问即可。

---

## 🎯 能做什么？（12 个工具一览）

### 📈 行情 & 指标类

| 工具 | 能查什么 | 你可以这样问 AI |
|------|---------|---------------|
| `hithink_market_query` | 实时价格、涨跌幅、成交量、主力资金流向、MACD / KDJ / RSI 等技术指标 | "同花顺今天多少钱""主力资金流入最多的股票""MACD 金叉的股票有哪些" |
| `hithink_zhishu_query` | 上证指数、沪深300、创业板指、恒生指数、纳斯达克等 | "上证指数现在多少点""恒生指数今天涨了多少""纳斯达克最近走势" |

### 💰 财务 & 估值类

| 工具 | 能查什么 | 你可以这样问 AI |
|------|---------|---------------|
| `hithink_finance_query` | 营业收入、净利润、ROE、ROA、负债率、毛利率、PE / PB 估值 | "茅台最新一期净利润多少""ROE 大于 20% 的股票""市盈率最低的银行股" |
| `hithink_macro_query` | GDP、CPI、PPI、PMI、LPR 利率、M2、社融 | "最新 CPI 数据""现在 LPR 利率是多少""M2 增速怎么样" |

### 🏢 公司深度信息

| 工具 | 能查什么 | 你可以这样问 AI |
|------|---------|---------------|
| `hithink_management_query` | 前十大股东、实控人、高管团队、股本结构 | "茅台十大股东是谁""这家公司实控人是谁""最近有哪些股东减持" |
| `hithink_business_query` | 主营业务构成、主要客户、供应商、参控股公司 | "同花顺主要做什么业务""茅台的前五大客户是谁""这家公司有哪些子公司" |
| `hithink_event_query` | 业绩预告、增发配股、股权质押、限售解禁、机构调研 | "最近有哪些公司发了业绩预告""下个月有哪些股票解禁""机构最近调研了哪些公司" |

### 🔍 筛选 & 搜索

| 工具 | 能查什么 | 你可以这样问 AI |
|------|---------|---------------|
| `hithink_astock_selector` | 多条件选股：行情 + 技术形态 + 财务 + 行业概念 | "选出今天涨超 5% 且市值大于 100 亿的科技股""均线多头的医药股有哪些" |
| `hithink_sector_selector` | 多条件选板块：估值 + 资金流向 + 涨跌幅 | "今天涨幅最大的板块""主力资金流入最多的概念板块" |
| `hithink_industry_query` | 行业估值排名、盈利对比、行情数据 | "哪个行业估值最低""银行业整体盈利如何" |
| `news_search` | 财经新闻：政策动态、行业革新、企业进展 | "最近 AI 行业有什么大新闻""央行最新货币政策""特斯拉有什么新动态" |
| `announcement_search` | 上市公司公告：财报、分红、回购、重组 | "茅台最新分红公告""最近有哪些公司回购股票""宁德时代发了什么公告" |

> 📌 **所有数据均来源于 [同花顺问财](https://www.iwencai.com)**

---

## 📋 准备工作

在开始之前，你需要准备好两样东西：

### 1️⃣ Python 环境

本工具**零依赖**，不需要 `pip install` 任何东西，只需要电脑上有 Python。

**检查 Python 是否已安装：**

```bash
python3 --version
```

如果显示 `Python 3.8.x` 或更高版本（如 `3.9`、`3.10`、`3.11`、`3.12`），说明没问题。

如果没有安装，去 [python.org](https://www.python.org/downloads/) 下载安装即可（安装时勾选「Add Python to PATH」）。

### 2️⃣ 同花顺问财 API Key

这是调用问财数据的"钥匙"，免费获取：

**获取步骤：**

1. 浏览器打开 [同花顺问财 SkillHub](https://www.iwencai.com/skillhub)
2. 注册 / 登录你的同花顺账号
3. 点击页面上任意一个 Skill 卡片（比如「行情数据」）
4. 在弹出的详情窗口中，找到「安装方式 → Agent 用户」区域
5. 复制那段以 `IWENCAI_API_KEY=` 开头的配置文本中的 **Key 值**（一串字母数字）

> ⚠️ **Key 看起来像这样：** `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
>
> 妥善保管，不要泄露给他人。

---

## 🚀 安装与配置

### 第一步：下载项目

```bash
# 克隆仓库
git clone https://github.com/lorek666/iwencai-mcp.git
cd iwencai-mcp
```

或者直接 [下载 ZIP](https://github.com/lorek666/iwencai-mcp/archive/refs/heads/main.zip) 解压。

### 第二步：设置 API Key

**macOS / Linux（终端执行）：**

```bash
export IWENCAI_API_KEY="你的APIKey粘贴在这里"
```

> 💡 如果想让 Key 永久生效（不用每次打开终端都设置），把上面这行加到 `~/.zshrc` 或 `~/.bashrc` 文件末尾。

**Windows（PowerShell）：**

```powershell
$env:IWENCAI_API_KEY="你的APIKey粘贴在这里"
```

### 第三步：测试是否正常

在项目目录下运行：

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | python3 server.py 2>/dev/null
```

如果看到输出了一大段 JSON 且包含 12 个工具名（`hithink_market_query`、`hithink_finance_query` 等），说明一切正常。

> ⚠️ 如果没有 API Key，会看到错误提示 `IWENCAI_API_KEY 环境变量未设置`——回到第二步检查 Key 是否正确设置。

---

## 🔌 接入 AI 助手

下面是主流 MCP 客户端的配置方法，选你用的那个即可。

### Claude Desktop

1. 打开 Claude Desktop
2. 进入 **Settings → Developer → Edit Config**
3. 在配置文件中添加：

```json
{
  "mcpServers": {
    "iwencai": {
      "command": "python3",
      "args": ["/你的路径/iwencai-mcp/server.py"],
      "env": {
        "IWENCAI_API_KEY": "你的APIKey"
      }
    }
  }
}
```

> ⚠️ 把 `/你的路径/iwencai-mcp/server.py` 换成你电脑上的实际路径（可以用 `pwd` 命令查看）
>
> 把 `"你的APIKey"` 换成真实的 Key

4. 重启 Claude Desktop
5. 点击输入框旁边的 🔌 图标，应该能看到 12 个 `hithink_*` 和 `news_search`、`announcement_search` 工具

### DeepSeek Desktop

1. 打开 DeepSeek Desktop
2. 进入 **设置 → MCP 服务器 → 添加服务器**
3. 填写：

| 字段 | 值 |
|------|-----|
| 名称 | `iwencai` |
| 命令 | `python3` |
| 参数 | `/你的路径/iwencai-mcp/server.py` |
| 环境变量 | `IWENCAI_API_KEY=你的APIKey` |

4. 保存并启用

### Cursor

1. 打开 Cursor
2. 进入 **Settings → Features → MCP**
3. 点击 **Add new MCP server**
4. 填写：

```json
{
  "mcpServers": {
    "iwencai": {
      "command": "python3",
      "args": ["/你的路径/iwencai-mcp/server.py"],
      "env": {
        "IWENCAI_API_KEY": "你的APIKey"
      }
    }
  }
}
```

### Cherry Studio / 其他支持 MCP 的客户端

通用配置格式——在 MCP 设置中添加：

- **名称**：`iwencai`
- **命令**：`python3`
- **参数**：`你的完整路径/server.py`
- **环境变量**：`IWENCAI_API_KEY=你的APIKey`

---

## 💬 使用示例

配置好之后，直接在 AI 对话中输入自然语言即可。以下是一些实测可用的提问：

**查行情：**
> "帮我查一下贵州茅台今天股价、涨跌幅和成交量"
> "上证指数和沪深300今天分别多少点"
> "今天主力资金净流入最多的 5 只股票"

**查财务：**
> "宁德时代最新一期的营收和净利润是多少"
> "把 A 股 ROE 最高的 10 家公司列出来"
> "银行板块平均市盈率和市净率"

**选股 / 选板块：**
> "筛选出今天涨幅超过 5%、市值大于 100 亿的 AI 概念股"
> "最近一个月主力资金持续流入的板块有哪些"
> "均线多头排列的新能源股票"

**搜资讯 / 公告：**
> "最近关于人工智能有什么重要政策新闻"
> "贵州茅台最近发布了什么公告"
> "近期有哪些公司公告了回购计划"

---

## ❓ 常见问题

### Q: 提示 "IWENCAI_API_KEY 环境变量未设置" 怎么办？

A: API Key 没有正确配置。检查：
- 环境变量名是否拼写正确（大写 `IWENCAI_API_KEY`）
- 在 Claude / Cursor 等客户端的配置中是否填了 `env` 字段
- 如果直接在终端测试，需要先 `export IWENCAI_API_KEY="..."` 再运行

### Q: 查询返回空数据？

A: 问财后端可能没有匹配到你提问维度的数据。尝试：
- 换一种更通用的说法（如「茅台股价」而不是「贵州茅台 2024年3月15日下午2点价格」）
- 放宽条件（去掉过于具体的限制词）

### Q: 支持查港股、美股吗？

A: 指数查询支持恒生指数、纳斯达克等。个股查询主要覆盖 A 股，部分港股也可尝试。问财的数据范围会持续扩展。

### Q: 需要付费吗？

A: 同花顺问财 API Key 目前是免费获取的，没有调用费用。但注意不要过于频繁调用（正常 AI 对话完全够用）。

### Q: 会不会泄露我的数据？

A: 你的 API Key 和查询请求直接从你的电脑发往同花顺问财服务器。AI 助手（Claude/DeepSeek 等）只接收问财返回的结果数据，不会看到你的 Key。

---

## 🏗️ 技术架构（进阶）

<details>
<summary>点击展开架构说明</summary>

```
server.py (405 行，纯 Python 标准库，零外部依赖)
│
├── JSON-RPC 2.0 over stdio
│   ├── initialize      → MCP 握手
│   ├── tools/list      → 返回 12 个工具的 inputSchema
│   └── tools/call      → 调度到具体函数
│
├── Pattern A — query2data (10 个工具)
│   └── POST https://openapi.iwencai.com/v1/query2data
│       ├── 严格 8 个 X-Claw-* Header
│       ├── Bearer Token 认证
│       └── 每次请求新生成 64 字符 Trace ID
│
└── Pattern B — comprehensive/search (2 个工具)
    └── POST https://openapi.iwencai.com/v1/comprehensive/search
        ├── channels: ["news"] 或 ["announcement"]
        └── app_id: "AIME_SKILL"
```

**设计原则：**
- 零依赖：纯 Python 标准库（`json`、`urllib`、`os`、`secrets`），兼容 Python 3.8+
- 单文件：整个服务器只有一个 `server.py`
- 透明透传：API 原始响应不做二次加工，保证数据完整性
</details>

---

## 📄 协议

本项目代码为 MIT License。数据来源于同花顺问财，使用时请遵守其服务条款。

---

<p align="center">
  Made with ❤️ for A-share investors<br>
  <sub>如果觉得有用，给个 ⭐ Star 吧</sub>
</p>
