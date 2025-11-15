import os
from datetime import datetime, timedelta, timezone
import platform
import time
import requests
import asyncio
import aiohttp
from time import sleep
import ctypes
import sys

class bcolors:
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    NC = '\033[0m'  # 无颜色
    BLUE = '\033[36m'  # 天蓝色
    ZS = '\033[35m'  # 紫色

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def input_with_timeout(prompt, timeout):
    from threading import Thread
    from queue import Queue, Empty
    import sys
    def get_input(queue):
        try:
            line = input(prompt)
            queue.put(line.strip().lower())
        except:
            queue.put(None)
    q = Queue()
    thread = Thread(target=get_input, args=(q,))
    thread.daemon = True
    thread.start()
    
    try:
        return q.get(timeout=timeout)
    except Empty:
        # 清除输入缓冲区
        if platform.system() == 'Windows':
            import msvcrt
            while msvcrt.kbhit():
                msvcrt.getch()
        else:
            from termios import tcflush, TCIFLUSH
            tcflush(sys.stdin, TCIFLUSH)
        return None

async def get_internet_time_async(session):
    # 定义 API 的 URL 和请求参数
    url = "https://api.uuni.cn/api/time"
    headers = {
        "Accept": "application/json"  # 确保请求头正确
    }
    try:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()  # 检查 HTTP 响应状态码
            data = await response.json()  # 将返回的 JSON 数据解析为 Python 对象
            timestamp = data['timestamp']
            
            # 将 timestamp 转换为 datetime 对象
            internet_time = datetime.fromtimestamp(int(timestamp), timezone(timedelta(hours=8)))
            return internet_time
    except requests.exceptions.RequestException as e:
        print(f"{bcolors.RED}请求失败: {e}{bcolors.NC}")
        return None

async def main_async():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return
    print("已获取管理员权限！")
    sleep(0.5)
    # 切换至UNF8编码
    os.system("chcp 65001")
    os.system("title 时间同步系统 by tbnya")
    # 显示ASCII艺术字
    print("=================================================================")
    print("                                                                 ")
    print(" █████╗ ██╗   ██╗███╗   ██╗██╗   ██╗ █████╗     ██████╗ ██╗   ██╗")
    print("██╔══██╗██║   ██║████╗  ██║╚██╗ ██╔╝██╔══██╗    ██╔══██╗╚██╗ ██╔╝")
    print("███████║██║   ██║██╔██╗ ██║ ╚████╔╝ ███████║    ██████╔╝ ╚████╔╝ ")
    print("██╔══██║██║   ██║██║╚██╗██║  ╚██╔╝  ██╔══██║    ██╔═══╝   ╚██╔╝  ")
    print("██║  ██║╚██████╔╝██║ ╚████║   ██║   ██║  ██║    ██║        ██║   ")
    print("╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝    ╚═╝        ╚═╝   ")
    print("                                                                 ")
    print("=================================================================")
    print(f"{bcolors.YELLOW}欢迎使用AUNYA-PY!{bcolors.NC}")
    # 显示版本信息
    print(f"{bcolors.ZS}README.md查看{bcolors.NC}")
    print(f"{bcolors.ZS}作者: tbnya（github同步）{bcolors.NC}")
    print(f"{bcolors.ZS}开始开发日期: 2025-11-01{bcolors.NC}")
    print("=")
    sleep(0.5)
    print("=================================================================")

    # 获取本机时间
    local_time = datetime.now().astimezone()
    print(f"{bcolors.BLUE}当前系统时间: {local_time.strftime('%Y-%m-%d %H:%M:%S %Z')}{bcolors.NC}")

    # 获取网络时间
    print(f"{bcolors.ZS}正在获取网络时间...{bcolors.NC}")
    async with aiohttp.ClientSession() as session:
        internet_time = await get_internet_time_async(session)

    if internet_time:
        print(f"{bcolors.BLUE}标准网络时间: {internet_time.strftime('%Y-%m-%d %H:%M:%S %Z')}{bcolors.NC}")
        
        # 计算时间差
        time_diff = abs((local_time - internet_time).total_seconds())
        print(f"{bcolors.ZS}时间差异: {time_diff:.2f} 秒{bcolors.NC}")
        if time_diff > 1:
            print(f"{bcolors.YELLOW}检测到时间偏差较大，是否立即同步时间？{bcolors.NC}")
            user_input = input_with_timeout(
                f"{bcolors.ZS}请输入 Y 确认或等待5秒自动同步 (Y/n): {bcolors.NC}", 5
            )
            
            if user_input == 'n':
                print(f"{bcolors.RED}已取消时间同步。{bcolors.NC}")
            else:
                print(f"{bcolors.YELLOW}正在尝试同步时间...{bcolors.NC}")
                if set_system_time(internet_time):
                    print(f"{bcolors.GREEN}时间同步成功！新系统时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{bcolors.NC}")
                else:
                    print(f"{bcolors.RED}请使用管理员/root权限运行本程序{bcolors.NC}")
        else:
            print(f"{bcolors.GREEN}时间同步状态正常{bcolors.NC}")

    print("=================================================================")
    input("按任意键退出...")

def set_system_time(target_time):
    system = platform.system()
    try:
        if system == 'Windows':
            date_str = target_time.strftime('%Y-%m-%d')
            time_str = target_time.strftime('%H:%M:%S')
            os.system(f'date {date_str}')
            os.system(f'time {time_str}')
        elif system == 'Linux':
            time_str = target_time.strftime('%Y-%m-%d %H:%M:%S')
            os.system(f'sudo date -s "{time_str}"')
        elif system == 'Darwin':  # macOS
            time_str = target_time.strftime('%Y-%m-%d %H:%M:%S')
            os.system(f'sudo date -s "{time_str}"')
        return True
    except Exception as e:
        print(f"{bcolors.RED}错误：时间同步失败 - {str(e)}{bcolors.NC}")
        return False

if __name__ == '__main__':
    asyncio.run(main_async())
