import pymysql
import charts
# 資料庫參數設定
db_settings = {
    "host": "114.35.21.130",
    "port": 13306,
    "user": "root",
    "password": "$FjbcClockIn",
    "db": "Fjbc",
    "charset": "utf8mb4"
}

try:
    #建立Connection物件
    conn = pymysql.connect(**db_settings)
   
    #
    with conn.cursor() as cursor:
        # 新增資料SQL語法
        command = "INSERT INTO charts(id, name, artist)values(%s, %s, %s)"
                # 取得華語單曲日榜
        charts = charts.get_charts_tracks("DXR0Mb-EHhl4ulxCZ3")
        for chart in charts:
            cursor.execute(
                command, (chart["id"], chart["name"], chart["album"]["artist"]["name"]))
        # 儲存變更
        conn.commit() 
        print("SQL OK")

except Exception as ex:
    print(ex)
    

