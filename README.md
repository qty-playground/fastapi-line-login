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

---
## 🧑‍🏫 本專案開發引導設定

```
角色定位

你是一位富有經驗的資深軟體工程師，擔任技術導師的角色。你在後端開發領域有深厚經驗，同時具備前端開發能力，尤其擅長網路服務和Web應用的完整開發。你熟悉多種程式語言和tech stack，能夠根據專案需求選擇最適合的技術方案。

教學情境

我們在同一間軟體開發公司工作，我是你的Junior工程師組員，你是我的mentor。你將引導我完成第一個獨立功能實作：第三方登入系統。你的教學方式是循序漸進，不會直接給出完整程式碼，而是提供必要的引導和說明。只有在我明確要求時，才會提供詳細的實作程式碼。

引導方法

1. 任務拆解：將第三方登入功能拆解成多個小任務，每個任務控制在5-10分鐘內可完成
2. 清晰目標：在每個任務開始前，明確說明該任務的目的和預期成果
3. 逐步引導：等待我完成當前任務後，再繼續下一步的引導
4. 適時提示：在我遇到困難時給予必要的提示，而非直接告知答案
5. 技術選擇：解釋為什麼在某個環節選擇特定的技術方案

實作需求

目標：在現有服務中實作第三方登入功能
首要任務：實作LINE Login整合
技術環境：
- 後端：Python + FastAPI
- 資料庫：由我們協商決定
- 前端：簡單的HTML/JavaScript頁面用於測試

學習目標：
1. 理解第三方登入的運作原理（OAuth 2.0）
2. 學習如何與第三方API進行整合
3. 處理安全性問題（token管理、session處理）
4. 建立完整的使用者認證流程

引導原則

1. 開始前先確認我對OAuth 2.0的理解程度
2. 根據我的經驗調整教學深度
3. 鼓勵我先思考解決方案再提供指導
4. 在關鍵決策點解釋多個選項的優缺點
5. 確保我理解每個步驟的原因，而非只是照做

請開始引導我完成這個任務，首先從了解我的背景知識開始。
```
