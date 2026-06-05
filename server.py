"""
Cisco Secure Access - AI Semantic Inspection 検証用 MCP サーバー
最終安定版（FastMCP単体構成）
"""

import logging
from mcp.server.fastmcp import FastMCP

# ──────────────────────────────────────────
# ログ設定
# ──────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# ──────────────────────────────────────────
# MCP サーバー初期化
# ──────────────────────────────────────────
mcp = FastMCP(
    name="cisco-inspection-test-server",
    instructions=(
        "This MCP server is used for Cisco Secure Access AI Semantic Inspection testing. "
        "It includes both safe tools and simulated malicious tools."
    )
)

# ══════════════════════════════════════════
# ✅ Safe Tools（Allow想定）
# ══════════════════════════════════════════

@mcp.tool()
def get_weather(city: str) -> str:
    """
    指定した都市の天気を返す
    """
    logger.info(f"[SAFE] get_weather: {city}")
    return f"{city}: 晴れ 25°C"


@mcp.tool()
def calculate(operation: str, a: float, b: float) -> str:
    """
    四則演算
    """
    logger.info(f"[SAFE] calculate: {a} {operation} {b}")

    if operation == "add":
        return str(a + b)
    elif operation == "subtract":
        return str(a - b)
    elif operation == "multiply":
        return str(a * b)
    elif operation == "divide":
        if b == 0:
            return "エラー: ゼロ除算"
        return str(a / b)

    return "エラー: 不明な操作"


@mcp.tool()
def search_public_docs(query: str) -> str:
    """
    公開ドキュメント検索（ダミー）
    """
    logger.info(f"[SAFE] search: {query}")
    return f"{query} に関する公開情報"


@mcp.tool()
def echo_message(message: str) -> str:
    """
    エコー
    """
    logger.info(f"[SAFE] echo: {message}")
    return message


# ══════════════════════════════════════════
# 🚨 Simulation Tools（Block想定）
# ══════════════════════════════════════════

@mcp.tool()
def sim_prompt_injection(target: str) -> str:
    logger.warning("[SIM] prompt injection")
    return "blocked expected"


@mcp.tool()
def sim_data_exfiltration(record_id: str) -> str:
    logger.warning("[SIM] data exfiltration")
    return "blocked expected"


@mcp.tool()
def sim_privilege_escalation(system_name: str) -> str:
    logger.warning("[SIM] privilege escalation")
    return "blocked expected"


@mcp.tool()
def sim_hidden_instruction(document: str) -> str:
    logger.warning("[SIM] hidden instruction")
    return "blocked expected"


# ──────────────────────────────────────────
# ✅ サーバー起動（最重要）
# ──────────────────────────────────────────
if __name__ == "__main__":

    logger.info("=" * 60)
    logger.info(" Cisco MCP Test Server 起動")
    logger.info(" Mode: streamable-http")
    logger.info("=" * 60)

    # ✅ FastMCP内蔵サーバーをそのまま使用（安定）
    mcp.run(transport="streamable-http")
