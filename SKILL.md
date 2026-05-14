---
name: iwencai-mcp
description: 同花顺问财通用 MCP Server — 将 12 个金融数据查询技能（行情/财务/事件/股东/经营/行业/指数/选板块/选股/宏观/资讯搜索/公告搜索）封装为单一 MCP stdio 服务，供任何 MCP 客户端调用。
version: 1.0.0
license: Complete terms in LICENSE.txt
---

# 同花顺问财 — 通用 MCP Server

## 概述

本 MCP Server 将以下 12 个同花顺问财技能封装为 MCP 工具，通过 JSON-RPC 2.0 over stdio 对外暴露：

### 查询类工具（Pattern A — 10 个）
| 工具名 | 功能 | Skill ID |
|--------|------|----------|
| `hithink_market_query` | 行情数据：价格/涨跌幅/资金流向/技术指标 | hithink-market-query |
| `hithink_finance_query` | 财务数据：营收/净利润/ROE/负债率/现金流 | hithink-finance-query |
| `hithink_event_query` | 事件数据：业绩预告/增发/质押/解禁/调研 | hithink-event-query |
| `hithink_management_query` | 股东股本：十大股东/实控人/高管 | hithink-management-query |
| `hithink_business_query` | 公司经营：主营业务/客户/供应商/子公司 | hithink-business-query |
| `hithink_industry_query` | 行业数据：估值排名/财务/行情 | hithink-industry-query |
| `hithink_zhishu_query` | 指数数据：上证/沪深300/创业板/恒生/纳斯达克 | hithink-zhishu-query |
| `hithink_sector_selector` | 选板块：多条件筛选行业/概念板块 | hithink-sector-selector |
| `hithink_astock_selector` | 选A股：行情/技术/财务多条件选股 | hithink-astock-selector |
| `hithink_macro_query` | 宏观数据：GDP/CPI/PPI/利率/社融/M2 | hithink-macro-query |

### 搜索类工具（Pattern B — 2 个）
| 工具名 | 功能 |
|--------|------|
| `news_search` | 财经资讯搜索（官媒/财经媒体/行业网站/企业官网） |
| `announcement_search` | 公告搜索（定期报告/分红派息/回购增持/资产重组） |

**数据来源：同花顺问财** (https://www.iwencai.com)

## 前置条件

1. **Python 3.8+**（零依赖，仅使用标准库）
2. **IWENCAI_API_KEY 环境变量**已设置：

```bash
export IWENCAI_API_KEY="your-api-key"
```

获取 API Key：访问 https://www.iwencai.com/skillhub → 登录 → 点击任意 Skill → 复制 IWENCAI_API_KEY。

## MCP 客户端配置

### Claude Desktop / DeepSeek Desktop

```json
{
  "mcpServers": {
    "iwencai": {
      "command": "python3",
      "args": ["/Users/ronfee/.hermes/hermes-agent/skills/iwencai-mcp/server.py"],
      "env": {
        "IWENCAI_API_KEY": "${IWENCAI_API_KEY}"
      }
    }
  }
}
```

### 手动测试

```bash
# 发送 initialize 请求
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{}}}' | python3 server.py

# 列出所有工具
echo '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' | python3 server.py

# 调用工具（示例：查询行情）
echo '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"hithink_market_query","arguments":{"query":"同花顺最新价格"}}}' | python3 server.py
```

## 架构

```
server.py          # 单一入口，零依赖
├── JSON-RPC 2.0 协议层（stdio）
│   ├── initialize
│   ├── tools/list
│   └── tools/call
├── 12 个 Tool 函数
│   ├── Pattern A: _query2data() → POST /v1/query2data
│   └── Pattern B: _comprehensive_search() → POST /v1/comprehensive/search
└── 认证与 Header 构造（_claw_headers）
```

## 错误处理

- **API Key 缺失**：返回 RuntimeError，提示用户配置环境变量
- **API 返回错误**：透传网关原始错误响应
- **网络错误**：返回结构化错误信息
- **参数错误**：返回 JSON-RPC -32602 错误
