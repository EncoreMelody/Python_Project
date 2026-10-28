import os
import requests
from dotenv import load_dotenv

# 自動載入 .env 檔案
load_dotenv()


def get_access_token():
    """取得 KKBOX OAuth 2.0 存取憑證 (Client Credentials Flow)"""
    client_id = os.getenv("KKBOX_CLIENT_ID")
    client_secret = os.getenv("KKBOX_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise ValueError(
            "未偵測到 KKBOX API 憑證！請建立 .env 檔案並設定 KKBOX_CLIENT_ID 與 KKBOX_CLIENT_SECRET。"
        )

    url = "https://account.kkbox.com/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "account.kkbox.com"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json().get("access_token")


def get_charts(territory="TW"):
    """取得指定地區的音樂排行榜列表"""
    access_token = get_access_token()
    url = "https://api.kkbox.com/v1.1/charts"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {access_token}"
    }
    params = {
        "territory": territory
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json().get("data", [])


def get_charts_tracks(chart_id, territory="TW"):
    """取得指定排行榜的歌曲清單"""
    access_token = get_access_token()
    url = f"https://api.kkbox.com/v1.1/charts/{chart_id}/tracks"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {access_token}"
    }
    params = {
        "territory": territory
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json().get("data", [])


if __name__ == "__main__":
    print("=== 取得 KKBOX 台灣排行榜列表 ===")
    try:
        charts_list = get_charts()
        for item in charts_list:
            print(f"ID: {item.get('id')} | 標題: {item.get('title')}")
    except Exception as e:
        print(f"執行失敗: {e}")