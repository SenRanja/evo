# encoding=utf-8
import os
from unittest import TestCase

import requests as rq
# 设置 DJANGO_SETTINGS_MODULE 环境变量
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
settings.configure()


class Test(TestCase):
    # url = reverse('home_works_list')

    # response = self.client.get(url)
    # self.assertEqual(response.status_code, 403)

    # self.client.force_login(self.user)
    # response = self.client.get(url)
    # self.assertEqual(response.status_code, 200)
    # data = response.json()
    # self.assertEqual(len(data), len(self.random_home_works))

    # data_fields = [key for key in data[0].keys()]

    # self.assertIn('school_name', data_fields)
    # self.assertIn('class_name', data_fields)
    # self.assertIn('student_name', data_fields)
    # self.assertIn('name', data_fields)复制代码
    def test_register(self):
        test_cases = [
            {
                "password": "abc123",
                "name": "John Doe",
                "stu_id": "987654321",
                "tel": "1234567890",
                "id_card": "123456789012345678",
                "email": "john.doe@example.com"
            },
            {
                "password": "password123",
                "name": "Jane Smith",
                "stu_id": "123456789",
                "tel": "9876543210",
                "id_card": "987654321012345678",
                "email": "jane.smith@example.com"
            },
            {
                "password": "securepass",
                "name": "Alice Johnson",
                "stu_id": "876543210",
                "tel": "5551234567",
                "id_card": "876543210987654321",
                "email": "alice.johnson@example.com"
            },
            {
                "password": "admin",
                "name": "申晏键",
                "stu_id": "001",
                "tel": "18536864913",
                "id_card": "141181199904230017",
                "email": "shenyanjian@gmail.com",
                "super": True
            }
        ]

        url = "http://127.0.0.1:8000/api/register/"

        for i in test_cases:
            rsp = rq.post(url, json=i)
            self.assertEqual(rsp.status_code, 200)
            self.assertEqual(rsp.json()['err_code'], 0)

    def test_login(self):
        url = "http://127.0.0.1:8000/api/login/"
        test_case_1 = {
            "login_name": "申晏键",
            "password": "admin"
        }
        session = rq.Session()
        rsp = session.post(url, json=test_case_1)
        self.assertEqual(rsp.status_code, 200)
        self.assertEqual(rsp.json()['err_code'], 0)

    def test_logout(self):
        url_login = "http://127.0.0.1:8000/api/login/"
        test_case_1 = {
            "login_name": "申晏键",
            "password": "admin"
        }
        session = rq.Session()
        session.post(url_login, json=test_case_1)

        url_logout = "http://127.0.0.1:8000/api/logout/"
        rsp = session.get(url_logout)
        print(rsp.text)
        self.assertEqual(rsp.status_code, 200)
        self.assertEqual(rsp.json()['err_code'], 0)
