# encoding=utf-8

import pickle, time
import sys
import os

__doc__ = '主要用来每个小时增长时间计数'

# 为了令脚本直接import license_data_encrypt，需要此处workdir设置本文件父目录
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.crypto import license_data_encrypt, license_data_decrypt

PICKLE_LICENSE_DATA = "license.data"

__doc__ = '''
   init_trial_data = {
       'licnese': {
           'license_trial': 2 * 24,
       },
       # 比如 已经过了300天， 此处存储小时数
       'past_hours_count': 300 * 24,
       'last_modify_time': 1705894391.789333,
   }

   运行crontab，使得该脚本每小时向 PICKLE_LICENSE_DATA 写入 'past_hours_count'+1 的小时数
   cron命令： 20 * * * * cd /app/scripts/;/usr/local/bin/python /app/scripts/timer_add.py >> /var/log/timer.log 2>&1
   
   debian示意:
   apt install -y cron && /etc/init.d/cron start && /etc/init.d/cron status && echo "20 * * * * cd /app/scripts/;/usr/local/bin/python /app/scripts/timer_add.py >> /var/log/timer.log 2>&1" > /etc/cron.d/my-cron-job 
   
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

def main():
    # 运行此文件，要求WORKDIR切换至本目录，因为 PICKLE_LICENSE_DATA 非绝对路径
    data_dict = load_from_data_file()
    print(data_dict)
    past_hours_count = data_dict['past_hours_count']
    # 增加多少小时数
    past_hours_count = past_hours_count + 1
    data_dict['past_hours_count'] = past_hours_count
    dump_to_data_file(data_dict)

if __name__ == '__main__':
    main()