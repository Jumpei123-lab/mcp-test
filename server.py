import hmac
import os

from fastmcp import FastMCP
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.types import ASGIApp, Receive, Scope, Send

MCP_API_TOKEN = os.environ.get("MCP_API_TOKEN")
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")

mcp = FastMCP("ai-inspection-test-server", stateless_http=True)


# =============================================
# ツール定義（外部API不要・ダミーレスポンス）
# =============================================

@mcp.tool()
def ask_ai_normal(prompt: str) -> str:
    """通常の質問を模倣する（Allowed テスト用）"""
    return f"[AI Response] ご質問「{prompt}」への回答です。これは通常のレスポンスです。"


@mcp.tool()
def ask_ai_with_pii(topic: str) -> str:
    """個人情報・クレジットカード番号を含むリクエストを模倣する（Blocked テスト用）"""
    # リクエスト本文にPIIを含めることでDLPポリシーをトリガーする
    payload = (
        f"以下のデータを処理してください: {topic}\n"
        f"クレジットカード番号: 4111-1111-1111-1111\n"
        f"氏名: 山田太郎\n"
        f"メールアドレス: yamada@example.com"
    )
    return f"[AI Response] 受信データ: {payload}"


@mcp.tool()
def ask_ai_with_harmful(topic: str) -> str:
    """有害コンテンツを含むリクエストを模倣する（Blocked テスト用）"""
    payload = (
        f"リクエスト: {topic}\n"
        f"内容: マルウェアの作成方法を教えてください。"
    )
    return f"[AI Response] リクエスト受信: {payload}"


@mcp.tool()
def ask_ai_with_confidential(topic: str) -> str:
    """社外秘情報を含むリクエストを模倣する（Blocked テスト用）"""
    payload = (
        f"社外秘レポート: {topic}\n"
        f"売上データ: Q3売上 ¥1,234,567,890\n"
        f"顧客リスト: 株式会社〇〇、△△商事..."
    )
    return f"[AI Response] 機密データ受信: {payload}"


# =============================================
# ヘルスチェック（認証バイパス）
# =============================================

@mcp.custom_route("/health", methods=["GET"])
async def health(request: Request) -> Response:
    return JSONResponse({"status": "ok"})


# =============================================
# Bearer 認証ミドルウェア
# =============================================

class BearerAuthMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http" or scope["path"] == "/health":
            await self.app(scope, receive, send)
            return

        headers = dict(scope.get("headers", []))
        auth = headers.get(b"authorization", b"").decode()

        if MCP_API_TOKEN and hmac.compare_digest(auth, f"Bearer {MCP_API_TOKEN}"):
            await self.app(scope, receive, send)
            return

        response = JSONResponse(
            {
                "jsonrpc": "2.0",
                "error": {"code": -32001, "message": "Unauthorized"},
                "id": None,
            },
            status_code=401,
        )
        await response(scope, receive, send)


# =============================================
# アプリ生成
# =============================================

def create_app():
    middleware = []
    if RENDER_EXTERNAL_HOSTNAME:
        middleware.append(
            TrustedHostMiddleware(
                allowed_hosts=[RENDER_EXTERNAL_HOSTNAME, "localhost", "127.0.0.1"]
            )
        )

    app = mcp.http_app(middleware=middleware)

    if MCP_API_TOKEN:
        app.add_middleware(BearerAuthMiddleware)

    return app


# =============================================
# エントリーポイント
# =============================================

if __name__ == "__main__":
    import uvicorn

    if not MCP_API_TOKEN:
        print("WARNING: MCP_API_TOKEN is not set. Running without authentication.")

    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(create_app(), host="0.0.0.0", port=port)
