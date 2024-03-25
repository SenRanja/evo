# 后端

### 部署

```shell
makemigrations user video notice question_manage exam_manage exam_score license subject_manage module system_manage system_monitor ftp message_handle
migrate
```

### 技术架构

django
DRF

需求：姓名、性别、学号、手机号、身份证、邮箱、密码、所属组

### 用户操作

##### 用户模型操作

`http://127.0.0.1:8000/api/user/`

DRF的rest api

##### 注册普通用户

`http://127.0.0.1:8000/api/register/`

```json
{
  "password": "password123",
  "name": "Jane Smith",
  "stu_id": "123456789",
  "tel": "9876543210",
  "id_card": "987654321012345678",
  "email": "jane.smith@example.com"
}
```

##### 注册超级用户

`http://127.0.0.1:8000/api/register/`

```json
{
  "password": "admin",
  "name": "申晏键",
  "stu_id": "001",
  "tel": "18536864913",
  "id_card": "141181199904230017",
  "email": "shenyanjian@gmail.com",
  "super": true
}
```

### video DRF操作model

DELETE方法，**不要忘记api的pk后面需要带斜杠**：

```DELETE /api/video/14/ HTTP/1.1
Host: 127.0.0.1:8000
User-Agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0
Accept: text/html; q=1.0, */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://127.0.0.1:8000/api/video/
Content-Type: application/json
X-CSRFTOKEN: 5C5YQ5f14fJ7UO0QSnSqet01i2mKiIqh2DJtsryA1Z3juT2LR7Fy2cuOCwrsJ9nn
X-Requested-With: XMLHttpRequest
Content-Length: 0
Origin: http://127.0.0.1:8000
Connection: close
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin

```

### 菜单管理

参考飞书文档

### 防止源码泄露

使用pyarmor进行源码加密，再部署。

### 容器部署

python:3.7  903MB
后需要改为更小的ubuntu来部署

### license

使用license生成器生成1-719天的license（超过此范围天数，license无效）

系统可运行时间是多license累计天数，超过提交过的license累计天数，系统过期。系统若过期，仅允许管理员用户登录，管理员需要提交新的license运行系统。

系统部署后，如果由于使用者逆向、停机等原因，导致系统license失效（即可能系统检测自己有36小时未运行），此时管理员需要提交一个新的license来重新激活系统（此情况建议给一两天的license即可）

### 定时任务脚本

每小时运行`/scripts/time_add.py`










