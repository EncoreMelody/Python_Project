import os
import pymysql
from dotenv import load_dotenv
import charts

# 自動載入 .env 檔案
load_dotenv()


def get_db_connection():
    """建立 MySQL 連線物件"""
    host = os.getenv("DB_HOST", "127.0.0.1")
    port = int(os.getenv("DB_PORT", "3306"))
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    database = os.getenv("DB_NAME", "Fjbc")
    charset = os.getenv("DB_CHARSET", "utf8mb4")

    if not password:
        print("[警告] 未在 .env 設定 DB_PASSWORD，將使用空白密碼嘗試連線。")

    return pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        charset=charset
    )


def save_chart_tracks_to_db(chart_id="DXR0Mb-EHhl4ulxCZ3"):
    """抓取指定排行榜的曲目並存入資料庫"""
    print(f"正在抓取排行榜 ID [{chart_id}] 的曲目...")
    track_list = charts.get_charts_tracks(chart_id)
    print(f"共取得 {len(track_list)} 首歌曲，準備寫入資料庫...")

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            insert_sql = "INSERT INTO charts(id, name, artist) VALUES (%s, %s, %s)"
            count = 0
            for item in track_list:
                track_id = item.get("id")
                track_name = item.get("name")
                artist_name = item.get("album", {}).get("artist", {}).get("name", "未知藝人")

                cursor.execute(insert_sql, (track_id, track_name, artist_name))
                count += 1

            conn.commit()
            print(f"寫入成功！已成功新增 {count} 筆歌曲至資料庫 charts 表格。")
    finally:
        conn.close()


def main():
    try:
        # 預設華語單曲日榜 ID: DXR0Mb-EHhl4ulxCZ3
        target_chart_id = os.getenv("DEFAULT_CHART_ID", "DXR0Mb-EHhl4ulxCZ3")
        save_chart_tracks_to_db(target_chart_id)
    except Exception as ex:
        print(f"執行發生錯誤: {ex}")


if __name__ == "__main__":
    main()
