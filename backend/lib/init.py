# encoding=utf-8

import pickle
import sys
import os

from lib.handle_license_data import default_trial_period
from exam_system.settings import PICKLE_LICENSE_DATA

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.crypto import license_data_encrypt, license_data_decrypt

def init():
    '''此部分代码在用户执行 python manage.py runserver 命令时可能会被执行两遍，因此需要注意完善检测代码，防止重复执行导致非预期bug'''
    pickle_license_data_file_path = PICKLE_LICENSE_DATA
    if os.path.exists(pickle_license_data_file_path) == True:
        print("license.data已存在")
    else:
        init_trial_data = default_trial_period()
        s = pickle.dumps(init_trial_data)
        encrypto_bytes = license_data_encrypt(s)
        with open(pickle_license_data_file_path, 'wb') as f:
            f.write(encrypto_bytes)
        print("license.data已创建，可试用2天")

