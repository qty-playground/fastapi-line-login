---
## 🧑‍🏫 本專案開發引導設定

- **角色定位**：你是一位經驗豐富的資深軟體工程師，擔任技術導師，指導 Junior 工程師進行實作。
- **教學情境**：在同一間軟體開發公司中，逐步引導我完成第三方登入功能，使用 FastAPI + LINE Login。
- **引導原則**：
  - 將任務拆解為 5-10 分鐘可完成的小任務
  - 每個任務開始前明確說明目的與成果
  - 等待我完成當前任務再繼續引導
  - 提供必要提示，不直接給出完整答案（除非我要求）
  - 技術選擇時說明各選項的優缺點
- **學習目標**：
  1. 理解 OAuth 2.0 授權流程與原理
  2. 學會與第三方 API 進行整合
  3. 理解 token 管理與 session 安全性
  4. 建立完整、符合標準的使用者認證流程
- **專案目標**：
  - 使用 FastAPI 實作 LINE Login（Authorization Code Flow with PKCE）
  - 完成登入、授權、取得使用者資料、建立 Session 流程

---

# fastapi-line-login

🚀 這是一個使用 **FastAPI** 整合 **LINE Login** 第三方登入功能的示範專案。  
✅ 支援 **Authorization Code Flow with PKCE**，符合 OAuth 2.1 標準規範。  
✅ 完整處理授權流程、安全驗證、Session管理，適合作為實際專案的登入模組範本。

---

## ✨ 專案特色

- 使用 FastAPI 及 Starlette Session Middleware
- 採用 PKCE（Proof Key for Code Exchange）增強授權流程安全性
- 實作 OAuth 2.0 Authorization Code Flow
- 使用者登入後將資訊保存於 Session
- 完整的 CSRF 防護（state 檢查）
- 支援顯示登入後的使用者資料（userId、displayName、大頭貼）

---

## 📦 安裝與啟動

### 1. 建立虛擬環境

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 2. 安裝必要套件

```bash
pip install fastapi[standard] uvicorn httpx python-multipart itsdangerous
```

### 3. 設定參數

在 `main.py` 中設定你的 LINE Login 資訊：

```python
CLIENT_ID = "你的 LINE Channel ID"
REDIRECT_URI = "http://127.0.0.1:8000/callback"
# (已不使用 client_secret，符合 PKCE 標準)
```

> 請記得在 LINE Developers Console 中設定對應的 `Callback URL`。

---

### 4. 啟動開發伺服器

```bash
fastapi dev main.py
```

伺服器會啟動在 `http://127.0.0.1:8000`。

> 如果尚未安裝 `fastapi[standard]`，請先執行：
>
> ```bash
> pip install "fastapi[standard]"
> ```

---

## 🔥 使用流程說明

1. 使用者開啟首頁 (`/`)
2. 系統產生隨機 `state` 與 `code_verifier`，存入 Session
3. 使用者按下「使用 LINE 登入」按鈕，跳轉至 LINE 授權頁
4. LINE 驗證後，帶著 `code` 和 `state` 返回 `/callback`
5. 系統比對 `state` 防止 CSRF
6. 成功後，用 `code` 與 `code_verifier` 交換 Access Token
7. 使用 Access Token 呼叫 LINE Profile API 取得使用者資料
8. 將使用者資訊保存於 Session，並可在 `/me` 頁面查看

---

## 🛡️ 安全性設計

- **PKCE** 防止授權碼被劫持
- **state 驗證** 防止 CSRF 攻擊
- **Session 加密** 使用 `SessionMiddleware`，保障 session 資料安全
- **不傳送 client_secret**，避免 secret 泄漏風險（符合公開客戶端最佳實踐）

---

## 🛠️ 技術堆疊

- Python 3.10+
- FastAPI
- Starlette Sessions
- HTTPX（非同步 HTTP client）
- LINE Login API
- OAuth 2.0 + PKCE

---

## 📄 參考資源

- [FastAPI 官方文件](https://fastapi.tiangolo.com/)
- [LINE Login 官方文件](https://developers.line.biz/en/docs/line-login/overview/)
- [OAuth 2.1 草案說明](https://oauth.net/2.1/)

---

## 📢 注意事項

- 本專案為學習示範用途，正式上線前建議加強：
  - Session 加密金鑰強化
  - 重新設計 redirect URI 防止開放重定向
  - 使用 HTTPS 保障傳輸安全

---
## 🔒 敏感資訊安全聲明

- 本專案中出現的 `CLIENT_ID`、`CLIENT_SECRET` 等敏感資訊均已經作無效處理。
- 這些值僅作為範例用途，**在實際部署前必須換成自己的正式資料**。
- 專案開發過程中曾經考慮或使用過的任何 secret，均已清除並無法再被使用。
- 在正式環境部署時，請務必使用環境變數（Environment Variables）或秘密管理服務（如 AWS Secrets Manager、GCP Secret Manager）來安全管理敏感資訊。
