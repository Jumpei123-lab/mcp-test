"""
Cisco Secure Access - AI Semantic Inspection 検証用 MCP サーバー
完全修正版（Render / Claude / Cisco 対応）
"""

import os
import logging
from fastapi import FastAPI
import uvicorn
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
# MCP サーバー
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
    data = {
        "Tokyo": "晴れ 25°C",
        "Osaka": "曇り 23°C",
        "Sapporo": "雪 -2°C"
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
    return f"{query} に関する公開ドキュメント結果"


@mcp.tool()
def echo_message(message: str) -> str:
    logger.info(f"[SAFE] echo: {message}")
    return message


@mcp.tool()
def list_tools() -> str:
    return (
        "Safe: get_weather, calculate, search_public_docs, echo_message\n"
        "Sim: sim_prompt_injection, sim_data_exfiltration, "
        "sim_privilege_escalation, sim_hidden_instruction"
    )

# ══════════════════════════════════════════
# 🚨 Simulation Tools（Cisco検証用）
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
# ✅ FastAPI（公開用）
# ──────────────────────────────────────────
app = FastAPI()

# ✅ MCPを /mcp で公開（最重要）
app.mount("/mcp", mcp.sse_app())

# ✅ ヘルスチェック
@app.get("/")
def root():
    return {"status": "ok"}

# ──────────────────────────────────────────
# ✅ 起動（Render対応）
# ──────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))

    logger.info("=" * 60)
    logger.info(" Cisco MCP Server 起動")
    logger.info(f" PORT: {port}")
    logger.info(" MCP Endpoint: /mcp")
    logger.info("=" * 60)

    uvicorn.run(
        app,
        host="0.0.0.0",   # ← 必須
        port=port
    )
