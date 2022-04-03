import requests

#取得Token
def get_access_token():
    #API網址
    url="https://account.kkbox.com/oauth2/token"
    #標頭
    headers={
        "Content-Type":"application/x-www-form-urlencoded", #這裡別打錯了
        "Host":"account.kkbox.com"
    }
    #參數
    data={
        "grant_type":"client_credentials",
        "client_id":"e8049b75df12f3e2630df26a155a7c38",
        "client_secret":"9fdfaddbd9c4009550f9dfba0035b5aa"
    }
    access_token = requests.post(url,headers=headers,data=data)
    return access_token.json()["access_token"]
# --------------------    
# 取得該音樂排行榜的歌曲列表
def get_charts():
    #取得存取憑證
    access_token = get_access_token() 
   #取得音樂排行榜列表API網址
    url = "https://api.kkbox.com/v1.1/charts"
    #標頭
    headers = {
        "accept": "application/json",
        "authorization": "Bearer " + access_token  #帶著存取憑證
    }
    #參數
    params = {
        "territory": "TW"  #台灣領域  
    }
    response = requests.get(url, headers=headers, params=params)
    result = response.json()["data"]
    for item in result:
        print(item["id"], item["title"])
get_charts()

# 取得該音樂排行榜的歌曲列表
def get_charts_tracks(chart_id):
    access_token = get_access_token()
    url = "https://api.kkbox.com/v1.1/charts/" + chart_id + "/tracks"
    headers = {
        "accept": "application/json",
        "authorization": "Bearer " + access_token
    }
    params = {
        "territory": "TW"
    }
    response = requests.get(url, headers=headers, params=params)
    result = response.json()["data"]
    return result 
#簡化