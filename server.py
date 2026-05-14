#!/usr/bin/env python3
"""
同花顺问财 — 通用 MCP Server（零依赖，纯 Python 标准库）

将以下 12 个技能封装为 MCP 工具，通过 JSON-RPC 2.0 over stdio 对外暴露：
  Pattern A (query2data — 10 个):
    hithink_market_query      行情数据
    hithink_finance_query     财务数据
    hithink_event_query       事件数据
    hithink_management_query  股东股本
    hithink_business_query    公司经营
    hithink_industry_query    行业数据
    hithink_zhishu_query      指数数据
    hithink_sector_selector   选板块
    hithink_astock_selector   选A股
    hithink_macro_query       宏观数据
  Pattern B (comprehensive/search — 2 个):
    news_search               财经资讯搜索
    announcement_search       公告搜索

数据来源：同花顺问财 (https://www.iwencai.com)
"""

import json
import os
import secrets
import sys
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional

# ── 工具注册表 ──────────────────────────────────────────────────────────
# 每个条目: (tool_name, skill_id, description, inputSchema)

TOOLS: List[Dict[str, Any]] = []

SERVER_NAME = "iwencai-mcp"
SERVER_VERSION = "1.0.0"
API_BASE = "https://openapi.iwencai.com"

# ── 辅助函数 ─────────────────────────────────────────────────────────────

def _trace_id() -> str:
    return secrets.token_hex(32)


def _api_key() -> str:
    key = os.environ.get("IWENCAI_API_KEY", "")
    if not key:
        raise RuntimeError(
            "IWENCAI_API_KEY 环境变量未设置。"
            "请访问 https://www.iwencai.com/skillhub 获取 API Key 后设置。"
        )
    return key


def _claw_headers(skill_id: str, call_type: str = "normal") -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {_api_key()}",
        "Content-Type": "application/json",
        "X-Claw-Call-Type": call_type,
        "X-Claw-Skill-Id": skill_id,
        "X-Claw-Skill-Version": "1.0.0",
        "X-Claw-Plugin-Id": "none",
        "X-Claw-Plugin-Version": "none",
        "X-Claw-Trace-Id": _trace_id(),
    }


def _post_json(url: str, payload: dict, headers: dict, timeout: int = 60) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
            if not body.strip():
                return {"text_response": ""}
            return json.loads(body)
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        return {"error": f"HTTP {e.code}: {e.reason}", "detail": err_body}
    except urllib.error.URLError as e:
        return {"error": f"网络错误: {e.reason}"}


# ── Pattern A: query2data 通用调用 ───────────────────────────────────────

def _query2data(skill_id: str, query: str, page: str = "1", limit: str = "10",
                call_type: str = "normal", timeout: int = 60) -> dict:
    url = f"{API_BASE}/v1/query2data"
    payload = {
        "query": query,
        "page": page,
        "limit": limit,
        "is_cache": "1",
        "expand_index": "true",
    }
    headers = _claw_headers(skill_id, call_type)
    result = _post_json(url, payload, headers, timeout)

    # 透传网关错误
    if isinstance(result, dict) and "datas" not in result and "error" not in result:
        # 可能是纯文本或网关层响应，直接透传
        return result

    return result


# ── Pattern B: comprehensive/search 通用调用 ──────────────────────────────

def _comprehensive_search(channel: str, query: str, call_type: str = "normal",
                          timeout: int = 60) -> dict:
    url = f"{API_BASE}/v1/comprehensive/search"
    payload = {
        "channels": [channel],
        "app_id": "AIME_SKILL",
        "query": query,
    }
    headers = _claw_headers(
        "news-search" if channel == "news" else "announcement-search",
        call_type,
    )
    # 将 skill_id 修正为正确的值
    if channel == "news":
        headers["X-Claw-Skill-Id"] = "news-search"
    elif channel == "announcement":
        headers["X-Claw-Skill-Id"] = "announcement-search"

    return _post_json(url, payload, headers, timeout)


# ── 12 个 Tool 函数 ──────────────────────────────────────────────────────

def hithink_market_query(query: str, page: str = "1", limit: str = "10",
                         timeout: int = 60) -> dict:
    """行情数据：股票/ETF/指数实时价格、涨跌幅、成交量、主力资金流向、技术指标"""
    return _query2data("hithink-market-query", query, page, limit, timeout=timeout)


def hithink_finance_query(query: str, page: str = "1", limit: str = "10",
                          timeout: int = 60) -> dict:
    """财务数据：营业收入、净利润、ROE、负债率、现金流、毛利率、净利率等"""
    return _query2data("hithink-finance-query", query, page, limit, timeout=timeout)


def hithink_event_query(query: str, page: str = "1", limit: str = "10",
                        timeout: int = 60) -> dict:
    """事件数据：业绩预告、增发配股、股权质押、限售解禁、机构调研、监管函等"""
    return _query2data("hithink-event-query", query, page, limit, timeout=timeout)


def hithink_management_query(query: str, page: str = "1", limit: str = "10",
                             timeout: int = 60) -> dict:
    """股东股本：股本结构、前十大股东、实控人、高管信息、股权质押等"""
    return _query2data("hithink-management-query", query, page, limit, timeout=timeout)


def hithink_business_query(query: str, page: str = "1", limit: str = "10",
                           timeout: int = 60) -> dict:
    """公司经营：主营业务构成、主要客户、供应商、参控股公司、重大合同等"""
    return _query2data("hithink-business-query", query, page, limit, timeout=timeout)


def hithink_industry_query(query: str, page: str = "1", limit: str = "10",
                           timeout: int = 60) -> dict:
    """行业数据：行业估值、财务、盈利、行情、板块排名等"""
    return _query2data("hithink-industry-query", query, page, limit, timeout=timeout)


def hithink_zhishu_query(query: str, page: str = "1", limit: str = "10",
                         timeout: int = 60) -> dict:
    """指数数据：上证指数、沪深300、创业板指、恒生指数、纳斯达克等"""
    return _query2data("hithink-zhishu-query", query, page, limit, timeout=timeout)


def hithink_sector_selector(query: str, page: str = "1", limit: str = "10",
                            timeout: int = 60) -> dict:
    """选板块：多条件组合筛选行业/概念/地域板块"""
    return _query2data("hithink-sector-selector", query, page, limit, timeout=timeout)


def hithink_astock_selector(query: str, page: str = "1", limit: str = "10",
                            timeout: int = 60) -> dict:
    """选A股：行情/技术形态/财务/行业概念等多条件筛选A股"""
    return _query2data("hithink-astock-selector", query, page, limit, timeout=timeout)


def hithink_macro_query(query: str, page: str = "1", limit: str = "10",
                        timeout: int = 60) -> dict:
    """宏观数据：GDP、CPI、PPI、利率、汇率、社融、M2、PMI等"""
    return _query2data("hithink-macro-query", query, page, limit, timeout=timeout)


def news_search(query: str, timeout: int = 60) -> dict:
    """财经资讯搜索：官媒/主流财经媒体/垂直行业网站/企业官网等"""
    return _comprehensive_search("news", query, timeout=timeout)


def announcement_search(query: str, timeout: int = 60) -> dict:
    """公告搜索：A股/港股/基金/ETF的定期报告、分红派息、回购增持、资产重组等"""
    return _comprehensive_search("announcement", query, timeout=timeout)


# ── Tool 调度表 ──────────────────────────────────────────────────────────

TOOL_DISPATCH = {
    "hithink_market_query": hithink_market_query,
    "hithink_finance_query": hithink_finance_query,
    "hithink_event_query": hithink_event_query,
    "hithink_management_query": hithink_management_query,
    "hithink_business_query": hithink_business_query,
    "hithink_industry_query": hithink_industry_query,
    "hithink_zhishu_query": hithink_zhishu_query,
    "hithink_sector_selector": hithink_sector_selector,
    "hithink_astock_selector": hithink_astock_selector,
    "hithink_macro_query": hithink_macro_query,
    "news_search": news_search,
    "announcement_search": announcement_search,
}

# ── Tool JSON Schema 定义 ────────────────────────────────────────────────

def _query_tool_schema(name: str, desc: str) -> dict:
    """生成 query2data 类工具的 inputSchema"""
    return {
        "name": name,
        "description": desc,
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "自然语言查询语句，如「同花顺最新价格」「ROE最高的股票」「上证指数涨跌幅」等",
                },
                "page": {
                    "type": "string",
                    "description": "分页页码，默认 '1'",
                    "default": "1",
                },
                "limit": {
                    "type": "string",
                    "description": "每页条数，默认 '10'",
                    "default": "10",
                },
                "timeout": {
                    "type": "integer",
                    "description": "请求超时秒数，默认 60",
                    "default": 60,
                },
            },
            "required": ["query"],
        },
    }


def _search_tool_schema(name: str, desc: str) -> dict:
    """生成 comprehensive/search 类工具的 inputSchema"""
    return {
        "name": name,
        "description": desc,
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "搜索关键词，如「人工智能」「贵州茅台 公告」等",
                },
                "timeout": {
                    "type": "integer",
                    "description": "请求超时秒数，默认 60",
                    "default": 60,
                },
            },
            "required": ["query"],
        },
    }


TOOL_SCHEMAS = [
    _query_tool_schema("hithink_market_query", "查询股票/ETF/指数实时行情数据：价格、涨跌幅、成交量、主力资金流向、技术指标（MACD/KDJ/RSI等）。数据来源：同花顺问财。"),
    _query_tool_schema("hithink_finance_query", "查询个股财务数据：营业收入、净利润、ROE、ROA、负债率、现金流、毛利率、净利率、PE/PB/PS等。数据来源：同花顺问财。"),
    _query_tool_schema("hithink_event_query", "查询个股事件数据：业绩预告、增发配股、股权质押、限售解禁、机构调研、监管函、股东大会等。数据来源：同花顺问财。"),
    _query_tool_schema("hithink_management_query", "查询公司股东股本信息：股本结构、前十大股东/流通股东、实控人、高管团队、股权质押情况等。数据来源：同花顺问财。"),
    _query_tool_schema("hithink_business_query", "查询公司经营数据：主营业务构成（产品/地区分布）、主要客户、供应商、参控股公司、股权投资、重大合同等。数据来源：同花顺问财。"),
    _query_tool_schema("hithink_industry_query", "查询行业数据：行业估值（PE/PB）、行业财务指标、行业盈利、行业行情、板块排名等。数据来源：同花顺问财。"),
    _query_tool_schema("hithink_zhishu_query", "查询指数行情：上证指数、沪深300、创业板指、恒生指数、纳斯达克、道琼斯等。支持点位、涨跌幅、成交量。数据来源：同花顺问财。"),
    _query_tool_schema("hithink_sector_selector", "智能筛选市场板块：按行业估值、资金流向、涨跌幅、成交量等多条件组合筛选行业/概念/地域板块。数据来源：同花顺问财。"),
    _query_tool_schema("hithink_astock_selector", "智能筛选A股：按行情指标、技术形态（均线多头/突破新高/K线形态）、财务指标、行业概念等多条件组合选股。数据来源：同花顺问财。"),
    _query_tool_schema("hithink_macro_query", "查询宏观经济数据：GDP、CPI、PPI、PMI、利率（LPR/基准利率）、汇率、社融、M2、工业增加值、消费、投资、进出口等。数据来源：同花顺问财。"),
    _search_tool_schema("news_search", "搜索财经资讯：覆盖官媒、主流财经媒体、垂直行业网站、知名企业官网。支持按关键词搜索最新财经新闻、政策动态、行业革新、企业进展。数据来源：同花顺问财。"),
    _search_tool_schema("announcement_search", "搜索金融公告：A股/港股/基金/ETF的定期财务报告、分红派息、回购增持、资产重组、重大合同、业绩预告等。数据来源：同花顺问财。"),
]


# ── JSON-RPC 2.0 协议处理 ────────────────────────────────────────────────

def _send(response: dict) -> None:
    """将 JSON-RPC 响应写入 stdout"""
    sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def _error(id_val, code: int, message: str) -> None:
    _send({"jsonrpc": "2.0", "id": id_val, "error": {"code": code, "message": message}})


def handle_initialize(req: dict) -> None:
    _send({
        "jsonrpc": "2.0",
        "id": req["id"],
        "result": {
            "protocolVersion": "2024-11-05",
            "serverInfo": {
                "name": SERVER_NAME,
                "version": SERVER_VERSION,
            },
            "capabilities": {
                "tools": {},
            },
        },
    })


def handle_tools_list(req: dict) -> None:
    _send({
        "jsonrpc": "2.0",
        "id": req["id"],
        "result": {
            "tools": TOOL_SCHEMAS,
        },
    })


def handle_tools_call(req: dict) -> None:
    params = req.get("params", {})
    tool_name = params.get("name", "")
    arguments = params.get("arguments", {})

    fn = TOOL_DISPATCH.get(tool_name)
    if fn is None:
        _error(req["id"], -32601, f"未知工具: {tool_name}")
        return

    try:
        result = fn(**arguments)
        # 将结果转为 MCP TextContent
        content_text = json.dumps(result, ensure_ascii=False, indent=2)
        _send({
            "jsonrpc": "2.0",
            "id": req["id"],
            "result": {
                "content": [
                    {"type": "text", "text": content_text}
                ],
            },
        })
    except TypeError as e:
        _error(req["id"], -32602, f"参数错误: {e}")
    except RuntimeError as e:
        _error(req["id"], -32000, str(e))
    except Exception as e:
        _error(req["id"], -32603, f"工具执行异常: {e}")


# ── 主循环 ───────────────────────────────────────────────────────────────

METHODS = {
    "initialize": handle_initialize,
    "tools/list": handle_tools_list,
    "tools/call": handle_tools_call,
}


def main() -> None:
    # 启动时写入 stderr 日志，不影响 stdio 协议
    print(f"[{SERVER_NAME}] v{SERVER_VERSION} starting on stdio", file=sys.stderr)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue

        # 通知类消息（无 id）不需要响应
        if req.get("method", "").startswith("notifications/") or "id" not in req:
            continue

        method = req.get("method", "")
        handler = METHODS.get(method)
        if handler is None:
            _error(req.get("id"), -32601, f"未知方法: {method}")
            continue

        try:
            handler(req)
        except Exception as e:
            _error(req.get("id"), -32603, f"内部错误: {e}")


if __name__ == "__main__":
    main()
