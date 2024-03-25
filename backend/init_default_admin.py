# encoding=utf-8

# 脚本外使用django代码需要初始化django环境
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exam_system.settings')
import django
django.setup()

import uuid
import random


# 执行django代码

# 创建默认用户（超级用户）
from user.models import User


def main():
    password = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(uuid.uuid1()) + str(random.random()))).replace('-','')
    default_admin_data = {
        'password': password,
        'name': 'admin',
        'stu_id': 'admin',
        'tel': '1234567',
        'id_card': '1234567',
        'email': 'admin@123.com',
        'role': 'admin',
    }
    try:
        # 若没有默认admin账户，则创建随机密码的admin账户
        if User.objects.filter(stu_id='admin').exists()==False:
            User.objects.create_superuser(
                password=default_admin_data['password'],
                name=default_admin_data['name'],
                stu_id=default_admin_data['stu_id'],
                tel=default_admin_data['tel'],
                id_card=default_admin_data['id_card'],
                email=default_admin_data['email'],
                role=default_admin_data['role'],
            )
            print("create super user successfully!")
            print("[!] default username & password: ", default_admin_data['stu_id'], default_admin_data['password'])
        else:
            # 存在admin默认账户
            print("[!] admin has existed!")
    except Exception as e:
        print("create super user failed!", str(e))

if __name__ == '__main__':
    main()