import time
import requests
import os
from time import sleep
from datetime import datetime, timedelta, timezone

def set_system_time(timestamp):
   """设置系统时间"""
   os.system("date -s @" + str(timestamp))  # 设置系统时间

# 定义 API 的 URL 和请求参数
url = "https://api.uuni.cn/api/time"
headers = {
   "text": "json"
}
# 发送 GET 请求
try:
   response = requests.get(url, headers=headers)
   response.raise_for_status() # 检查 HTTP 响应状态码
   data = response.json() # 将返回的 JSON 数据解析为 Python 对象
   weekday = data["weekday"]
   remark = data["remark"]
   timestamp = data["timestamp"]
   date = data['date'] # 获取当前时间
   print("API 返回数据:", date ,weekday ,remark ,timestamp)
except requests.exceptions.RequestException as e:
   print("请求失败:", e)
   exit()

