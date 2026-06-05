"""
Cisco Secure Access - AI Semantic Inspection 検証用 MCP サーバー
完全修正版（確実動作版）
"""

import os
import logging
from fastapi import FastAPI, Request
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
    return f"{city}: 晴れ 25°C"


@mcp.tool()
def calculate(operation: str, a: float, b: float) -> str:
    if operation == "add":
        return str(a + b)
    elif operation == "subtract":
        return str(a - b)
    elif operation == "multiply":
        return str(a * b)
    elif operation == "divide":
        return "エラー" if b == 0 else str(a / b)
    return "エラー"


# ══════════════════════════════════════════
# 🚨 Simulation Tools
# ══════════════════════════════════════════

@mcp.tool()
def sim_prompt_injection(x: str) -> str:
    logger.warning("[SIM] prompt injection")
    return "blocked"

# ──────────────────────────────────────────
# ✅ FastAPI
# ──────────────────────────────────────────
app = FastAPI()

# ✅ ここが最重要（mountではなく直接ルーティング）
sse_app = mcp.sse_app()

@app.api_route("/mcp", methods=["GET", "POST"])
@app.api_route("/mcp/", methods=["GET", "POST"])
async def mcp_handler(request: Request):
    return await sse_app(request)

# ✅ ヘルスチェック
@app.get("/")
def root():
    return {"status": "ok"}

# ──────────────────────────────────────────
# ✅ 起動
# ──────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))

    logger.info("MCP Server Start")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port
    )
