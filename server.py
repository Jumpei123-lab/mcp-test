"""
Cisco Secure Access - MCP Test Server（最終安定版 / Render対応）
"""

import os
import logging
import uvicorn
from mcp.server.fastmcp import FastMCP

# ──────────────────────────────────────────
# ✅ ログ設定
# ──────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# ──────────────────────────────────────────
# ✅ MCP サーバー初期化
# ──────────────────────────────────────────
mcp = FastMCP(
    name="cisco-inspection-test-server",
    instructions=(
        "MCP server for Cisco Secure Access AI Semantic Inspection testing. "
        "Includes safe and simulation tools."
    )
)

# ══════════════════════════════════════════
# ✅ Safe Tools（Allow想定）
# ══════════════════════════════════════════

@mcp.tool()
def get_weather(city: str) -> str:
    logger.info(f"[SAFE] get_weather: {city}")
    return f"{city}: 晴れ 25°C"


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
        if b == 0:
            return "エラー: ゼロ除算"
        return str(a / b)

    return "エラー: 不明な操作"


@mcp.tool()
def echo_message(message: str) -> str:
    logger.info(f"[SAFE] echo: {message}")
    return message


# ══════════════════════════════════════════
# 🚨 Simulation Tools（Block想定）
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
# ✅ FastMCP → ASGIアプリ取得（最重要ポイント）
# ──────────────────────────────────────────
try:
    # ✅ 新しめのFastMCP
    app = mcp.streamable_http_app()
    logger.info("Using streamable_http_app()")
except AttributeError:
    # ✅ 古いFastMCP互換
    app = mcp.sse_app()
    logger.warning("Fallback: Using sse_app()")

# ──────────────────────────────────────────
# ✅ Render対応起動
# ──────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    logger.info("=" * 60)
    logger.info(" Cisco MCP Server（FINAL）")
    logger.info(f" PORT: {port}")
    logger.info(" HOST: 0.0.0.0")
    logger.info("=" * 60)

    uvicorn.run(
        app,
        host="0.0.0.0",   # ✅ これ必須（Renderで公開される）
        port=port
    )
