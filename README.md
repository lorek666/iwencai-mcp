# iwencai-mcp

同花顺问财通用 MCP Server — 零依赖，纯 Python 标准库。

## 前置条件

- Python 3.8+
- `IWENCAI_API_KEY` 环境变量

## 安装

```bash
# 设置 API Key
export IWENCAI_API_KEY="your-api-key"
```

无需 pip install — 仅使用 Python 标准库。

## 在 MCP 客户端中配置

```json
{
  "mcpServers": {
    "iwencai": {
      "command": "python3",
      "args": ["/path/to/server.py"],
      "env": {
        "IWENCAI_API_KEY": "${IWENCAI_API_KEY}"
      }
    }
  }
}
```

## 手动测试

```bash
cd /Users/ronfee/.hermes/hermes-agent/skills/iwencai-mcp
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{}}}' | python3 server.py
```

## 可用工具

12 个金融数据查询/搜索工具，详见 SKILL.md。
