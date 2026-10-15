import requests
import re
import json

'''
-------------------------------------------------------------------------
以下為獲取中租的發電資料
-------------------------------------------------------------------------
'''
# 定義目標 URL
url1 = "http://bigsun.ipvita.net/"

# 創建一個會話對象
session = requests.Session()

try:
    # 發送 GET 請求
    response = session.get(url1)

    # 檢查請求是否成功
    if response.status_code == 200:
        # 提取session_cookies['ASP.NET_SessionId']的值
        session_cookies = session.cookies.get_dict()
        #print(session_cookies['ASP.NET_SessionId'])
    else:
        print("Failed to retrieve the page. Status code:", response.status_code)

except requests.exceptions.RequestException as e:
    # 捕捉並打印任何請求異常
    print("An error occurred:", e)

# 目標網址
url2 = "http://bigsun.ipvita.net/InstantPower.aspx?KBJLTdmlql3MGEL882fWBw"



# 自訂 HTTP 標頭
headers2 = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Cookie": "ASP.NET_SessionId="+session_cookies['ASP.NET_SessionId']
}

try:
    # 發送GET請求
    response = requests.get(url2, headers=headers2)

    # 檢查響應狀態碼
    response.raise_for_status()

    # 獲取網頁內容
    html_content = response.text

    # 列印網頁原始碼
    #print(html_content)

    # 使用正則表達式提取ColumnValue的值
    pattern1 = re.compile(r'var ColumnValue = "(.*?)";')
    match = pattern1.search(html_content)
    if match:
      column_value = match.group(1).split('&')[1:]  # 過濾掉第一個空字串
      data1=column_value[:18]
      #發電無資料者自動補0
      while(len(data1)) < 18:
        data1.append('0')
      print(data1)
    else:
      print("ColumnValue not found")


except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except requests.exceptions.ConnectionError as conn_err:
    print(f"Connection error occurred: {conn_err}")
except requests.exceptions.Timeout as timeout_err:
    print(f"Timeout error occurred: {timeout_err}")
except requests.exceptions.RequestException as req_err:
    print(f"An error occurred: {req_err}")


'''
-------------------------------------------------------------------------
以下為獲取玉衡的發電資料
-------------------------------------------------------------------------
'''
# 目標網址
url3 = "https://dsegomspoc.azurewebsites.net/api/exhibit/stationChartData"
params3 = {"PassToken": "8AB10AD80670B5159CC90753BE39D0B4", "ZoneID": "2022195", "GetDayChart": "true"}

# 自訂 HTTP 標頭
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Cookie": "ARRAffinity=dedd2531989686e03c66fd7863b3e062f8afa7ae2784777b82ee4271c17b8d20; ARRAffinitySameSite=dedd2531989686e03c66fd7863b3e062f8afa7ae2784777b82ee4271c17b8d20",
    "Content-Type": "application/json",
    "Host": "dsegomspoc.azurewebsites.net",
    "Origin": "https://dsegomspoc.azurewebsites.net",
    "Referer": "https://dsegomspoc.azurewebsites.net/exhibit_free-login?2022195&8AB10AD80670B5159CC90753BE39D0B4&TW"
}


try:
    # 发送 POST 请求，將參數放到 `json` 中
    response = requests.post(url3, headers=headers, data=json.dumps(params3))

    # 獲取網頁內容
    root_json = response.json()

    # 打印 JSON 數據
    data2=root_json["Response"]["DayChart"]["value"][:18]
    #發電無資料者自動補0
    while(len(data2)) < 18:
        data2.append('0')
    print(data2)

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except requests.exceptions.ConnectionError as conn_err:
    print(f"Connection error occurred: {conn_err}")
except requests.exceptions.Timeout as timeout_err:
    print(f"Timeout error occurred: {timeout_err}")
except requests.exceptions.RequestException as req_err:
    print(f"An error occurred: {req_err}")


'''
-------------------------------------------------------------------------
以下為獲取錦群傑的發電資料
-------------------------------------------------------------------------
'''
from datetime import datetime
# 格式化日期時間為字串
now = datetime.now()
formatted_date = now.strftime("%Y-%m-%d")

# 目標網址
url4 = "https://mypowermanager.net/02PVI/server/api/CodeIgniter/index.php/PrimeVOLT/web/v1/Inverterapi/GroupDetailDayLine"
params4 = {"GroupAutoID": "6976", "date": formatted_date}

# 自訂 HTTP 標頭
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Cookie": "PHPSESSID=jm6j58ufbforp4t0c95chv0h07",
    "Content-Type": "application/json"
}


try:
    # 发送 POST 请求，將參數放到 `json` 中
    response = requests.post(url4, headers=headers, data=json.dumps(params4))

    # 獲取網頁內容
    root_json = response.json()

    # 打印 JSON 數據
    #print(root_json["data"])

    data = root_json["data"]
    #取出root_json["data"]中的pac數值
    pac_values = [item['pac'] for item in data]
 # 忽略20分及40的資料，只保留整點的值
 #   pac_values = [item['pac'] for index, item in enumerate(data) if index % 3 == 0]
 #5點以前的資料補0
    list1 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
    data3 = list1 + list(pac_values)
 #5點以前的資料不補0
 #   data3 = list(pac_values)

    # 確保資料長度不超過54，並在不足54個點時補0
    data3 = data3[:54]
    while(len(data3)) < 54:
        data3.append('0')
    print(data3)


except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except requests.exceptions.ConnectionError as conn_err:
    print(f"Connection error occurred: {conn_err}")
except requests.exceptions.Timeout as timeout_err:
    print(f"Timeout error occurred: {timeout_err}")
except requests.exceptions.RequestException as req_err:
    print(f"An error occurred: {req_err}")


'''
-------------------------------------------------------------------------
以下為將發電資料繪製折線圖
-------------------------------------------------------------------------
'''
# 創建圖表
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# 資料轉換
x_values_temp = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
x_values = []
for i in range(len(x_values_temp)):
    x_values.append(str(x_values_temp[i]))
    x_values.append(str(x_values_temp[i])+".3")
    x_values.append(str(x_values_temp[i])+".6")

number_data1_temp = [float(element) for element in data1]
number_data2_temp = [float(element) for element in data2]
number_data3 = [float(element) for element in data3]

#加上過渡資料值
number_data1 = []
for i in range(len(number_data1_temp)-1):
    number_data1.append(number_data1_temp[i])
    number_data1.append(number_data1_temp[i]+(number_data1_temp[i+1]-number_data1_temp[i])/3)
    number_data1.append(number_data1_temp[i]+(number_data1_temp[i+1]-number_data1_temp[i])*2/3)
number_data1.append(number_data1_temp[17])
number_data1.append(0)
number_data1.append(0)

number_data2 = []
for i in range(len(number_data2_temp)-1):
    number_data2.append(number_data2_temp[i])
    number_data2.append(number_data2_temp[i]+(number_data2_temp[i+1]-number_data2_temp[i])/3)
    number_data2.append(number_data2_temp[i]+(number_data2_temp[i+1]-number_data2_temp[i])*2/3)
number_data2.append(number_data2_temp[17])
number_data2.append(0)
number_data2.append(0)

'''
print(x_values)
print(number_data1)
print(number_data2)
print(number_data3)
'''
#繪製總表
y = [number_data1, number_data2, number_data3]
x = [x_values, x_values, x_values]

plt.figure(figsize=(9.5, 5))
plt.plot(x[0], y[0], color='deepskyblue', linewidth=3)   # 中租
plt.plot(x[1], y[1], color='deeppink', linewidth=3)   # 玉衡
plt.plot(x[2], y[2], color='orange', linewidth=3)   # 錦群傑

#x軸間距調整
x_spacing = 3 # x軸密集度
ax = plt.gca()  # Get the current Axes instance
ax.xaxis.set_major_locator(mticker.MultipleLocator(x_spacing))

plt.grid(True)
plt.xlabel("Hour")
plt.ylabel("kW")
plt.savefig("chart.png")
#plt.show()

#繪製中租圖表
plt.figure(figsize=(9.5, 5))
plt.plot(x[0], y[0], color='deepskyblue', linewidth=3)   # 中租
plt.bar(x[0][::3], y[0][::3], color='blue', linewidth=3, alpha=0.4 ,width=1.5)
x_spacing = 3 # x軸密集度
ax = plt.gca()  # Get the current Axes instance
ax.xaxis.set_major_locator(mticker.MultipleLocator(x_spacing))
plt.grid(True)
plt.xlabel("Hour")
plt.ylabel("kW")
plt.savefig("chart1.png")

#繪製玉衡圖表
plt.figure(figsize=(9.5, 5))
plt.plot(x[1], y[1], color='deeppink', linewidth=3)   # 玉衡
plt.bar(x[1][::3], y[1][::3], color='red', linewidth=3, alpha=0.4 ,width=2)
x_spacing = 3 # x軸密集度
ax = plt.gca()  # Get the current Axes instance
ax.xaxis.set_major_locator(mticker.MultipleLocator(x_spacing))
plt.grid(True)
plt.xlabel("Hour")
plt.ylabel("kW")
plt.savefig("chart2.png")

#繪製僅群傑圖表
plt.figure(figsize=(9.5, 5))
plt.plot(x[2], y[2], color='orange', linewidth=3)   # 錦群傑
plt.fill(x[2], y[2], color='cornflowerblue' ,alpha=0.4)
#plt.plot(x[2][15:], y[2][15:], color='orange', linewidth=3)   # 錦群傑
#plt.fill(x[2][15:], y[2][15:], color='cornflowerblue' ,alpha=0.4)
x_spacing = 3 # x軸密集度
ax = plt.gca()  # Get the current Axes instance
ax.xaxis.set_major_locator(mticker.MultipleLocator(x_spacing))
plt.grid(True)
plt.xlabel("Hour")
plt.ylabel("kW")
plt.savefig("chart3.png")