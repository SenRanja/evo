# encoding=utf-8
from datetime import datetime
import pytz

def format_date(iso_time):
    parsed_time = datetime.fromisoformat(iso_time.replace('Z', '+00:00'))
    formatted_time = parsed_time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time

def date_delta(date_time_str):
    # 求时间差，单位 天
    # 将字符串表示的日期转换为datetime对象，如 "2024-02-29"
    early_time = datetime.strptime(date_time_str, "%Y-%m-%d")
    current_time = datetime.now()
    delta = current_time - early_time
    return delta.days

# UTC时间格式化转换
def UTC_2_CN_TIME(input_time):
    input_datetime = datetime.fromisoformat(input_time.replace("Z", "+00:00"))
    # 设置中国时区
    china_timezone = pytz.timezone('Asia/Shanghai')
    # 转换时区
    china_datetime = input_datetime.astimezone(china_timezone)
    # 格式化输出为字符串
    china_time_str = china_datetime.strftime("%Y-%m-%d %H:%M:%S")
    return china_time_str