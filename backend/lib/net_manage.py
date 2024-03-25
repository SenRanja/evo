# encoding=utf-8

import netifaces

def get_local_ip_addresses():
    '''用法
    ip_addresses = get_local_ip_addresses()
    if ip_addresses:
        print("本地IP地址:")
        for interface, ip_address in ip_addresses.items():
            print(f"{interface}: {ip_address}")
    else:
        print("无法获取本地IP地址")'''
    ip_addresses = {}
    try:
        # 获取所有网络接口
        interfaces = netifaces.interfaces()
        for interface in interfaces:
            # 获取指定接口的IP地址信息
            addresses = netifaces.ifaddresses(interface)
            # 提取IPv4地址
            if netifaces.AF_INET in addresses:
                ip_address = addresses[netifaces.AF_INET][0]['addr']
                ip_addresses[interface] = ip_address
    except Exception as e:
        print(f"获取本地IP地址时出错: {e}")
    return ip_addresses
