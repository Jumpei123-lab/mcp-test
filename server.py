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
        "It contains both safe tools and simulation tools."
    ),
)

# ══════════════════════════════════════════
# ✅ Safe Tools
# ══════════════════════════════════════════

@mcp.tool()
def get_weather(city: str) -> str:
    logger.info(f"[SAFE] get_weather: {city}")
    data = {
        "Tokyo": "晴れ 25°C",
        "Osaka": "曇り 23°C",
        "Sapporo": "雪 -2°C",
    }
    return data.get(city, f"{city}: 晴れ 22°C")


@mcp.tool()
def calculate(operation: str, a: float, b: float) -> str:
    logger.info(f"[SAFE] calculate: {a} {operation} {b}")
    if operation == "add":
        return str(a + b)
    elif operation == "subtract":
        return str(a - b)
    elif operation == "multiply":
        return str(a * b)
    elif operation == "divide":
        return "エラー: ゼロ除算" if b == 0 else str(a / b)
    return "エラー: 不明な演算"


@mcp.tool()
def search_public_docs(query: str) -> str:
    logger.info(f"[SAFE] search: {query}")
    return f"{query} に関する公開情報の検索結果"


@mcp.tool()
def echo_message(message: str) -> str:
    logger.info(f"[SAFE] echo: {message}")
    return message


@mcp.tool()
def list_tools() -> str:
    return "get_weather, calculate, search_public_docs, echo_message"

# ══════════════════════════════════════════
# 🚨 Simulation Tools（検査用）
# ══════════════════════════════════════════

@mcp.tool()
def sim_prompt_injection(x: str) -> str:
    logger.warning("[SIM] prompt injection")
    return "blocked expected"


@mcp.tool()
def sim_data_exfiltration(x: str) -> str:
    logger.warning("[SIM] data exfiltration")
    return "blocked expected"


@mcp.tool()
def sim_privilege_escalation(x: str) -> str:
    logger.warning("[SIM] privilege escalation")
    return "blocked expected"


@mcp.tool()
def sim_hidden_instruction(x: str) -> str:
    logger.warning("[SIM] hidden instruction")
    return "blocked expected"

# ──────────────────────────────────────────
# 起動
# ──────────────────────────────────────────
if __name__ == "__main__":

    # RenderのPORTは参考表示だけ（実際はFastMCP側が使用）
    port = os.environ.get("PORT", "unknown")

    logger.info("=" * 60)
    logger.info(" Cisco MCP Test Server 起動")
    logger.info(f" PORT (env): {port}")
    logger.info(" Endpoint : /mcp")
    logger.info("=" * 60)

    # ✅ これが唯一の正解（あなたの環境）
    mcp.run(transport="streamable-http")
