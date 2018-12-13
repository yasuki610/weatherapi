import requests
import json
import csv
import paramiko
import pandas as pd
import os

HOST = os.environ["HOST"]
PORT = 22
USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]
print(HOST)
print(PORT)
print(USERNAME)
print(PASSWORD)

remote_file = "/Import/weather.csv"
 
def sftp_upload(csvlist, remote_file):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, port=PORT, username=USERNAME, password=PASSWORD)
        sftp = client.open_sftp()
        # ファイルオープン
        #f = sftp.file(remote_file, mode='w+', bufsize = -1)
        csvlist.to_csv("weather_001.csv", index = False, encoding="utf_8_sig")
        sftp.put("weather_001.csv",remote_file)

        #csvlist.to_csv("desktop_bom.csv", index = False, encoding="utf_8_sig")
        #csvlist.to_csv("desktop_non_bom.csv", index = False, encoding="utf_8")
        # ファイルクローズ
        #f.close()

    except Exception as e:
        print(e)
 
    finally:
        sftp.close()
        client.close()

# APIキーの指定
apikey = "16b73354992f5e38d25a35b445ecee46"

# 天気を調べたい都市の一覧 
cities = ["Tokyo,JP", "London,UK", "New York,US"]
# APIのひな型
api = "http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}"

# 温度変換(ケルビン→摂氏)
k2c = lambda k: k - 273.15

csvlist = pd.DataFrame()
csvheader = ["City","Pressure"]
weatherlist = []

# 各都市の温度を取得する
for name in cities:
    # APIのURLを得る
    url = api.format(city=name, key=apikey)
    # 実際にAPIにリクエストを送信して結果を取得する
    r = requests.get(url)
    # 結果はJSON形式なのでデコードする
    data = json.loads(r.text)    
    # 結果を出力
    print("+ 都市=", data["name"])
    print("| 天気=", data["weather"][0]["description"])
    print("| 最低気温=", k2c(data["main"]["temp_min"]))
    print("| 最高気温=", k2c(data["main"]["temp_max"]))
    print("| 湿度=", data["main"]["humidity"])
    print("| 気圧=", data["main"]["pressure"])
    print("| 風速度=", data["wind"]["speed"])
    print("")

    # データをリストに保持
    weatherlist.append([data["name"],data["main"]["pressure"]])
    print(weatherlist)
    print(csvheader)

df = pd.DataFrame(weatherlist, columns=csvheader)
#df.to_csv("weather00.csv")
#df.to_csv("weather01.csv", encoding="cp932")
#df.to_csv("weather02.csv", encoding="utf_8_sig")
#df.to_csv("weather03.csv", index = False, encoding="utf_8_sig")
#df.to_csv("weather04.csv", sep=',',encoding='utf_8_sig')
#df.to_csv("weather05.csv", sep=",",encoding="utf_8_sig")

sftp_upload(df, remote_file)

