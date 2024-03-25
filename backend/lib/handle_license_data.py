# encoding=utf-8
import binascii
import pickle, time

from hashlib import md5
from lib.crypto import encrypt_aes256gcm, format_string, license_data_encrypt, license_data_decrypt

from exam_system.settings import PICKLE_LICENSE_DATA, LICENSE_SHUTDOWN_TIME, LICENSE_LARGEST_DAYS, LICENSE_INIT_TRIAL_DAYS
from lib.net_manage import get_local_ip_addresses

__doc__ = '''
每过一个小时，将进行时间累加
如365天，小时数是8760

直接相关变量：
1. license累计增加小时数
2. 现有过去小时数

间接相关变量：
1. 文件修改时间（防止有人单纯替换该文件，直接绕过license时间校验）

判断
现有过去小时数 > license累计增加小时数 ?
如果大于，则系统停止运行，且暂停`现有过去小时数`的计数

为提高逆向破解难度，对两个相关变量进行隐秘的藏匿。
目前赶工，简单实用pickle序列化字符串，加密存储到本目录的license.data文件中。

license.data存储格式: dict，如下
{
    # 存储不论天，只论小时
    
    # 多license，需要检测，发现重复license无法使用
    'licnese':{
        'license1 -- adasdasdadsda': 365*24,
        'license2 -- adasddasdasda': 200*24,
        'license3 -- a21312asdasda': 300*24,
    },
    
    # 过去小时数，比如300天的小时数
    'past_hours_count': 300*24,
    
    # 文件的上次修改时间
    'last_modify_time': 1705894391.789333,
}
'''

def load_from_data_file() -> dict:
    # 读取 PICKLE_LICENSE_DATA
    with open(PICKLE_LICENSE_DATA, 'rb') as f:
        file_content = f.read()
    # 内容解密，读出为python数据格式 license_data_dict
    license_data_dict = pickle.loads(license_data_decrypt(file_content))
    return license_data_dict


def dump_to_data_file(license_data_dict:dict):
    # 导出至 PICKLE_LICENSE_DATA
    license_data_dict['last_modify_time'] = time.time()
    s = pickle.dumps(license_data_dict)
    encrypto_bytes = license_data_encrypt(s)
    with open(PICKLE_LICENSE_DATA, 'wb') as f:
        f.write(encrypto_bytes)


def default_trial_period()->dict:
    '默认试用2天'
    init_trial_data = {
            'licnese': {
                # 小时数
                'license_trial': LICENSE_INIT_TRIAL_DAYS,
            },
            'past_hours_count': 0,
            'last_modify_time': time.time(),
        }
    return init_trial_data

def check_license_data_valid() -> (bool, str):
    '''返回 license 是否有效。 如果返回False，则返回原因'''
    license_data_dict: dict = load_from_data_file()
    # last_modify_time 的单位是 秒数
    time_sec_sub = time.time() - license_data_dict["last_modify_time"]
    # license_data的改动时间距今应该不超过x天，否则返回 license失效
    if time_sec_sub > LICENSE_SHUTDOWN_TIME:
        return (False, "系统疑似发生长时间停机，请联系管理员")
    else:
        # license 给予的授权小时数
        granted_hours = 0
        # 源文件以小时数存储，直接相加
        for k,v in license_data_dict["licnese"].items():
            granted_hours = granted_hours + v
        # 系统运行过去的小时数：past_hours_count 原单位即小时
        past_hours_count = license_data_dict["past_hours_count"]
        if past_hours_count>granted_hours:
            # 过期
            return (False, "系统license失效，请联系管理员")
        else:
            # 未过期
            return (True, "")


def check_license_day_num(to_check_license) -> int:
    '''返回检查license的天数，不能输入大于719天的license
    返回0天表示license无效'''
    # 验证license部分，该部分未来要封装为函数，根据页面的license接口进行验证
    key = binascii.unhexlify('fd2d9fb0bb4bc7a7e5d36e0cce8d26573950c4461c4d29afd46214e37e686197')
    iv = binascii.unhexlify('29cd7489b0a30e28fb589377')

    # ip 黑名单，校验license不考虑此处ip
    ip_black_set = ('127.0.0.1', '0.0.0.0')

    ip_all_list = []
    ip_addresses = get_local_ip_addresses()
    if ip_addresses:
        for interface, ip_address in ip_addresses.items():
            # interface MAC地址 ip_address IP地址
            ip_all_list.append(ip_address)
    ip_list = [ip for ip in ip_all_list if ip not in ip_black_set]

    for day in range(1, LICENSE_LARGEST_DAYS):
        for single_ip in ip_list:
            plain = single_ip + "shenyanjian" + str(day)
            text = plain.encode()
            endata = encrypt_aes256gcm(key, text, iv)
            digest = md5(endata).hexdigest()
            license = digest[:16]
            if to_check_license == format_string(license):
                return day
    return 0

    # 加密
    # endata = encrypt_aes256gcm(key, text, iv)

    # # 解密
    # other_data = binascii.unhexlify("d271bebe89d0b7f2669cdc540c48dc12862b56f570eb168794b6c4")
    # plain_text = decrypt_aes256gcm(key, other_data, iv)
    # print(plain_text.decode())
