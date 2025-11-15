import time
import requests
import os
# 定义 API 的 URL 和请求参数
url = "https://api.xiaole.work/api/time/time.php?type=json"
headers = {
   "text": "json"
}
# 发送 GET 请求
try:
   response = requests.get(url, headers=headers)
   response.raise_for_status() # 检查 HTTP 响应状态码
   data = response.json() # 将返回的 JSON 数据解析为 Python 对象
   time = data['time'] # 获取当前时间
   print("API 返回数据:", time)
except requests.exceptions.RequestException as e:
   print("请求失败:", e)

# 更改系统时间
os.system("date " + time)
print("系统时间已更新为:", time)