# KKBOX Open API & MySQL 歌曲排行榜資料擷取

透過 Python 呼叫 KKBOX Open API 取得台灣音樂排行榜清單與榜單曲目，並可自動寫入 MySQL 資料庫儲存。

---

## 專案功能

- **排行榜查詢 (`charts.py`)**：使用 KKBOX OAuth 2.0 (Client Credentials Flow) 取得台灣熱門音樂排行榜及曲目列表。
- **資料庫匯入 (`getKKBOX.py`)**：自動將指定排行榜的所有歌曲（ID、歌名、演出者）批量存入 MySQL 的 `charts` 資料表。
- **終端互動查詢 (`KKBOXpy/charts Playlist.py`)**：列出所有排行榜並支援輸入 ID 查詢詳細歌曲清單。

---

## 系統需求

- Python 3.8+
- MySQL 5.7+ / 8.0+ / MariaDB

---

## 安裝與環境設定

### 1. 安裝依賴套件

建議建立虛擬環境後安裝：

```bash
# 建立並啟用虛擬環境 (Windows PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# 安裝依賴
pip install -r requirements.txt
```

### 2. 設定環境變數 (`.env`)

複製 `.env.example` 為 `.env`，並填入您的憑證：

```bash
cp .env.example .env
```

編輯 `.env` 檔案：

```env
# KKBOX Open API 憑證 (可至 https://developer.kkbox.com/ 申請)
KKBOX_CLIENT_ID=your_kkbox_client_id_here
KKBOX_CLIENT_SECRET=your_kkbox_client_secret_here

# MySQL 資料庫連線設定
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_db_password_here
DB_NAME=Fjbc
DB_CHARSET=utf8mb4
```

---

## 資料庫準備

請先在 MySQL 中建立目標資料表（預設名稱為 `charts`）：

```sql
CREATE DATABASE IF NOT EXISTS Fjbc CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE Fjbc;

CREATE TABLE IF NOT EXISTS charts (
    id VARCHAR(100) NOT NULL,
    name VARCHAR(255) NOT NULL,
    artist VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);
```

---

## 執行方式

### 1. 查詢排行榜列表
```bash
python charts.py
```

### 2. 爬取特定榜單並寫入 MySQL 資料庫
```bash
python getKKBOX.py
```

### 3. 命令列互動查詢曲目
```bash
python "KKBOXpy/charts Playlist.py"
```

---

## 安全性注意事項

- 請勿將帶有真實密碼與金鑰的 `.env` 檔案提交至 Git。
- 本專案已透過 `.gitignore` 自動忽略 `.env` 與 Python 快取檔案。
