import os
import sys
from pathlib import Path
import requests
from dotenv import load_dotenv

# 優先載入專案根目錄或同層的 .env
root_env = Path(__file__).resolve().parent.parent / ".env"
local_env = Path(__file__).resolve().parent / ".env"

if root_env.exists():
    load_dotenv(dotenv_path=root_env)
else:
    load_dotenv(dotenv_path=local_env)


def get_access_token():
    """取得 KKBOX OAuth 2.0 存取憑證 (Client Credentials Flow)"""
    client_id = os.getenv("KKBOX_CLIENT_ID")
    client_secret = os.getenv("KKBOX_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise ValueError(
            "未偵測到 KKBOX API 憑證！請於專案根目錄的 .env 設定 KKBOX_CLIENT_ID 與 KKBOX_CLIENT_SECRET。"
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
    """取得音樂排行榜列表"""
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
    """取得指定音樂排行榜的歌曲列表"""
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


def interactive_main():
    try:
        print("================= KKBOX 音樂排行榜清單 =================")
        charts_list = get_charts()
        for idx, item in enumerate(charts_list, 1):
            print(f"[{idx:02d}] ID: {item.get('id')} | 標題: {item.get('title')}")

        print("\n================= 查詢特定榜單歌曲 =================")
        chart_id = input("請貼上欲查詢的音樂排行榜 ID: ").strip()
        if not chart_id:
            print("未輸入 ID，程式結束。")
            return

        tracks = get_charts_tracks(chart_id)
        print(f"\n成功取得 {len(tracks)} 首歌曲：")
        for idx, track in enumerate(tracks, 1):
            name = track.get("name", "未知歌名")
            artist = track.get("album", {}).get("artist", {}).get("name", "未知歌手")
            print(f"{idx:02d}. {name} - {artist}")

    except requests.HTTPError as http_err:
        print(f"API 請求失敗: {http_err}")
    except Exception as ex:
        print(f"發生錯誤: {ex}")


if __name__ == "__main__":
    interactive_main()