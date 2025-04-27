from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
import httpx  # ⭐ 需要安裝 httpx: pip install httpx
import secrets
import base64
import hashlib


# 你的Channel設定
CLIENT_ID = "2007334823"
# CLIENT_SECRET = "261b730985e4afb0466c06604787cf96"  # ❌ 現在不使用，PKCE取代
REDIRECT_URI = "http://127.0.0.1:8000/callback"

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-very-secret-key")


def generate_state():
    return secrets.token_urlsafe(16)  # 產生一個安全的亂數字串

def generate_code_verifier():
    return secrets.token_urlsafe(64)  # 產生強隨機亂數

def generate_code_challenge(code_verifier):
    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(code_challenge).decode("utf-8").rstrip("=")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    state = generate_state()
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    request.session["state"] = state
    request.session["code_verifier"] = code_verifier

    line_login_url = (
        "https://access.line.me/oauth2/v2.1/authorize"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&state={state}"
        f"&scope=profile%20openid%20email"
        f"&code_challenge={code_challenge}"
        f"&code_challenge_method=S256"
    )

    return f"""
    <html>
        <head>
            <title>LINE Login Demo</title>
        </head>
        <body>
            <h1>Hello LINE Login</h1>
            <a href="{line_login_url}">使用 LINE 登入</a>
        </body>
    </html>
    """


@app.get("/callback", response_class=HTMLResponse)
async def callback(request: Request):
    params = dict(request.query_params)
    code = params.get("code")
    returned_state = params.get("state")
    error = params.get("error")

    if error:
        return f"<h1>授權失敗: {error}</h1>"

    session_state = request.session.get("state")
    if not returned_state or not session_state or returned_state != session_state:
        return "<h1>無效的 state，可能有攻擊風險！</h1>"
    if not code:
        return "<h1>沒有收到授權資訊</h1>"

    # ⭐⭐ 這裡開始進行 Token 兌換 ⭐⭐
    token_url = "https://api.line.me/oauth2/v2.1/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    code_verifier = request.session.get("code_verifier")
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "code_verifier": code_verifier,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, headers=headers, data=data)

    if response.status_code != 200:
        return f"<h1>兌換 token 失敗</h1><p>{response.text}</p>"

    token_response = response.json()
    access_token = token_response.get("access_token")

    profile_url = "https://api.line.me/v2/profile"
    headers = {"Authorization": f"Bearer {access_token}"}

    async with httpx.AsyncClient() as client:
        profile_response = await client.get(profile_url, headers=headers)

    if profile_response.status_code != 200:
        return f"<h1>取得使用者資料失敗</h1><p>{profile_response.text}</p>"

    profile_data = profile_response.json()

    user_id = profile_data.get("userId")
    display_name = profile_data.get("displayName")
    picture_url = profile_data.get("pictureUrl")

    # profile_data 是剛剛從 LINE拿到的資料
    request.session["user"] = {
        "user_id": user_id,
        "display_name": display_name,
        "picture_url": picture_url,
    }

    return """
    <h1>登入成功！</h1>
    <p><a href='/me'>查看我的資料</a></p>
    """


@app.get("/me", response_class=HTMLResponse)
async def me(request: Request):
    user = request.session.get("user")
    if not user:
        return "<h1>尚未登入</h1><p><a href='/'>回首頁</a></p>"

    return f"""
    <h1>我的資料</h1>
    <ul>
        <li>User ID: {user['user_id']}</li>
        <li>名字: {user['display_name']}</li>
        <li><img src="{user['picture_url']}" alt="大頭貼" width="100"></li>
    </ul>
    <p><a href='/'>回首頁</a></p>
    """
