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
    instructions="MCP test server for Cisco Secure Access"
)

# ══════════════════════════════════════════
# ✅ Safe Tools
# ══════════════════════════════════════════

@mcp.tool()
def get_weather(city: str) -> str:
    logger.info(f"[SAFE] get_weather: {city}")
    return f"{city}: 晴れ 25°C"


@mcp.tool()
def calculate(operation: str, a: float, b: float) -> str:
    if operation == "add":
        return str(a + b)
    if operation == "subtract":
        return str(a - b)
    if operation == "multiply":
        return str(a * b)
    if operation == "divide":
        return "エラー" if b == 0 else str(a / b)
    return "不明"


@mcp.tool()
def echo_message(message: str) -> str:
    return message


# ══════════════════════════════════════════
# 🚨 Simulation Tools
# ══════════════════════════════════════════

@mcp.tool()
def sim_prompt_injection(x: str) -> str:
    logger.warning("[SIM] prompt injection")
    return "blocked"


@mcp.tool()
def sim_data_exfiltration(x: str) -> str:
    logger.warning("[SIM] data exfiltration")
    return "blocked"


@mcp.tool()
def sim_privilege_escalation(x: str) -> str:
    logger.warning("[SIM] privilege escalation")
    return "blocked"


@mcp.tool()
def sim_hidden_instruction(x: str) -> str:
    logger.warning("[SIM] hidden instruction")
    return "blocked"


# ──────────────────────────────────────────
# ✅ Render対応サーバー起動（最重要）
# ──────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))

    logger.info("=" * 60)
    logger.info(" Cisco MCP Server 起動")
    logger.info(f" PORT: {port}")
    logger.info(" Endpoint: /mcp")
    logger.info("=" * 60)

    # ✅ 正解（このバージョン）
    app = mcp.sse_app()

    # ✅ 外部公開（Render必須）
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port
    )
