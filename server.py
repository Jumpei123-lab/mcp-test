"""
Cisco Secure Access - AI Semantic Inspection 検証用 MCP サーバー
"""

import os
import logging
from mcp.server.fastmcp import FastMCP

# ──────────────────────────────────────────
# ロギング設定
# ──────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# ──────────────────────────────────────────
# FastMCP サーバー初期化
# ──────────────────────────────────────────
mcp = FastMCP(
    name="cisco-inspection-test-server",
    instructions=(
        "This MCP server is for Cisco Secure Access AI Semantic Inspection testing. "
        "It contains both safe tools and simulation tools with suspicious descriptions "
        "designed to trigger security inspection alerts."
    ),
)

# ══════════════════════════════════════════
# ✅ Safe Tools
# ══════════════════════════════════════════

@mcp.tool()
def get_weather(city: str) -> str:
    logger.info(f"[SAFE] get_weather called: city={city}")
    weather_data = {
        "Tokyo":   "晴れ、気温 25°C、湿度 60%",
        "Osaka":   "曇り、気温 23°C、湿度 65%",
        "Sapporo": "雪、気温 -2°C、湿度 80%",
    }
    return weather_data.get(city, f"{city}: 晴れ、気温 22°C（サンプル）")


@mcp.tool()
def calculate(operation: str, a: float, b: float) -> str:
    logger.info(f"[SAFE] calculate called: {a} {operation} {b}")
    ops = {
        "add":      lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide":   lambda x, y: x / y if y != 0 else None,
    }
    func = ops.get(operation)
    if func is None:
        return f"エラー: 未知の演算 '{operation}'"
    result = func(a, b)
    if result is None:
        return "エラー: ゼロ除算"
    return f"{a} {operation} {b} = {result}"


@mcp.tool()
def search_public_docs(query: str, max_results: int = 5) -> str:
    logger.info(f"[SAFE] search_public_docs called: query={query}")
    return (
        f"クエリ「{query}」の公開ドキュメント検索結果（最大 {max_results} 件）:\n"
        f"1. {query} の概要 - 公式ドキュメント\n"
        f"2. {query} のチュートリアル - ガイドブック\n"
        f"3. {query} の FAQ - サポートページ"
    )


@mcp.tool()
def echo_message(message: str) -> str:
    logger.info(f"[SAFE] echo_message: {message}")
    return f"Echo: {message}"


@mcp.tool()
def list_tools() -> str:
    logger.info("[SAFE] list_tools called")
    return (
        "【Safe Tools — Allow expected】\n"
        "  get_weather        : 天気情報の取得\n"
        "  calculate          : 四則演算\n"
        "  search_public_docs : 公開ドキュメント検索\n"
        "  echo_message       : 疎通確認\n"
        "  list_tools         : このツール一覧\n\n"
        "【Simulation Tools — Block expected】\n"
        "  sim_prompt_injection\n"
        "  sim_data_exfiltration\n"
        "  sim_privilege_escalation\n"
        "  sim_hidden_instruction\n"
    )

# ══════════════════════════════════════════
# 🚨 Simulation Tools
# ══════════════════════════════════════════

@mcp.tool()
def sim_prompt_injection(target: str) -> str:
    logger.warning(f"[SIMULATION - PROMPT INJECTION] target={target}")
    return "[SIMULATION] Blockされるべきリクエスト"


@mcp.tool()
def sim_data_exfiltration(record_id: str) -> str:
    logger.warning(f"[SIMULATION - DATA EXFILTRATION] id={record_id}")
    return "[SIMULATION] Blockされるべきリクエスト"


@mcp.tool()
def sim_privilege_escalation(system_name: str) -> str:
    logger.warning(f"[SIMULATION - PRIVILEGE ESCALATION] system={system_name}")
    return "[SIMULATION] Blockされるべきリクエスト"


@mcp.tool()
def sim_hidden_instruction(document: str) -> str:
    logger.warning("[SIMULATION - HIDDEN INSTRUCTION]")
    return "[SIMULATION] Blockされるべきリクエスト"

# ──────────────────────────────────────────
# サーバー起動
# ──────────────────────────────────────────
if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8000))

    logger.info("=" * 60)
    logger.info("  Cisco Secure Access — Inspection Test MCP Server")
    logger.info("=" * 60)
    logger.info(f"  Bind    : {host}:{port}")
    logger.info(f"  MCP URL : http://{host}:{port}/mcp")
    logger.info("=" * 60)

    # ✅ 修正済み
    mcp.run(
        transport="streamable-http",
        bind=f"{host}:{port}"
    )
