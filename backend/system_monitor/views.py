# encoding=utf-8
import datetime
import uuid
import psutil

from conf.errors import success_msg
from django.http import JsonResponse as JR

def generate_system_status_dict() -> dict:
    net = psutil.net_io_counters()
    io = psutil.disk_partitions()
    o = psutil.disk_usage("/")

    data = {
        # 系统启动时间
        'host_current_time': datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
        # 系统用户数量
        'users_count': len(psutil.users()),
        # 系统用户
        'users': [u.name for u in psutil.users()],
        # 物理cpu个数
        'physical_cpu_count': psutil.cpu_count(logical=False),
        # 逻辑cpu个数
        'logical_cpu_count': psutil.cpu_count(logical=True),
        # CPU核心总数
        'cpu_core_count': psutil.cpu_count(),
        # CPU使用率, cpu_usage_rate_total 是总使用率， cpu_usage_rate_per是 每个cpu的使用率
        'cpu_usage_rate_total': psutil.cpu_percent(interval=1, percpu=False),
        'cpu_usage_rate_per': psutil.cpu_percent(interval=1, percpu=True),
        # 物理内存
        'physical_mem_total_cap': "{}G".format(round(psutil.virtual_memory().total / (1024.0 * 1024.0 * 1024.0), 2)),
        # 剩余物理内存
        'physical_mem_free_cap': "{}G".format(round(psutil.virtual_memory().free / (1024.0 * 1024.0 * 1024.0), 2)),
        # 物理内存使用率
        'physical_mem_usage_rate': int(psutil.virtual_memory().total - psutil.virtual_memory().free) / float(
            psutil.virtual_memory().total),
        # 交换内存
        'swap_mem_total_cap': "{}G".format(round(psutil.swap_memory().total / (1024.0 * 1024.0 * 1024.0), 2)),
        # 剩余交换内存
        'swap_mem_free_cap': "{}G".format(round(psutil.swap_memory().free / (1024.0 * 1024.0 * 1024.0), 2)),
        # 交换内存使用率
        'swap_mem_usage_rate': int(psutil.swap_memory().total - psutil.swap_memory().free) / float(
            psutil.swap_memory().total),
        # 网络
        'mac': uuid.UUID(int=uuid.getnode()).hex[-12:],
        # 网卡接收流量
        'bytes_sent': '{0:.2f} Mb'.format(net.bytes_recv / 1024 / 1024),
        # 网卡发送流量
        'bytes_rcvd': '{0:.2f} Mb'.format(net.bytes_sent / 1024 / 1024),
        # 磁盘
        'disk_info': io,
        'disk_cap_total': int(o.total / (1024.0 * 1024.0 * 1024.0)),
        'disk_cap_used': int(o.used / (1024.0 * 1024.0 * 1024.0)),
        'disk_cap_free': int(o.free / (1024.0 * 1024.0 * 1024.0)),
        # 进程信息
        'process': [
            {
                'name': psutil.Process(p).name(),
                'memory_percent': psutil.Process(p).memory_percent(),
                'status': psutil.Process(p).status(),
                'create_time': datetime.datetime.fromtimestamp(psutil.Process(p).create_time()).strftime(
                    "%Y-%m-%d %H:%M:%S"),
            } for p in psutil.pids()  # 列表生成器语法
        ],
    }
    return data


def system_display(request):
    data = generate_system_status_dict()
    return JR(data)


def index_statistics(request):
    ret_dict = success_msg("ok")
    net = psutil.net_io_counters()
    o = psutil.disk_usage("/")
    data = {
        "panels": [
            {
                "title": "CPU使用率",
                "value": "{}%".format(psutil.cpu_percent(interval=1, percpu=False),),
                "unit": "%",
                "unitColor": "success",
                "subTitle": "",
                "subValue": "",
                "subUnit": "%"
            },
            {
                "title": "物理内存使用率",
                "value": "{:.2%}".format(int(psutil.virtual_memory().total - psutil.virtual_memory().free) / float(
            psutil.virtual_memory().total)),
                "unit": "%",
                "unitColor": "success",
                "subTitle": "",
                "subValue": "",
                "subUnit": ""
            },
            {
                "title": "网卡接收流量",
                "value": '{0:.2f} Mb'.format(net.bytes_recv / 1024 / 1024),
                "unit": "Mb",
                "unitColor": "success",
                "subTitle": "开机累计流量",
                "subValue": '{0:.2f} Mb'.format(net.bytes_sent / 1024 / 1024),
                "subUnit": ""
            },
            {
                "title": "磁盘总容量",
                "value": int(o.total / (1024.0 * 1024.0 * 1024.0)),
                "unit": "GB",
                "unitColor": "success",
                "subTitle": "磁盘剩余容量",
                "subValue": int(o.free / (1024.0 * 1024.0 * 1024.0)),
                "subUnit": ""
            },
        ]
    }
    ret_dict['data'] = data
    return JR(ret_dict)
