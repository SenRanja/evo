# 使用官方的 Python 镜像作为基础镜像, 903MB
FROM python:3.7

# 设置环境变量，py的stdout和stderr被禁用缓冲，及时打印日志
ENV PYTHONUNBUFFERED 1

# 创建并切换到工作目录
WORKDIR /app

COPY . /app/
# COPY ./sources.list /etc/apt/sources.list

# 安装加密组件库
# 安装cron
# 暂时为了方便安装vim net-tools
RUN apt-get update -y && apt-get install -y build-essential libssl-dev libffi-dev python3-dev uwsgi-plugin-python3 cron vim net-tools

# 安装 Python 依赖
RUN pip install -r requirements.txt && pip install uwsgi && mkdir -p /var/log/uwsgi

# 防破解 crontab (手动)
# RUN echo "* * * * * root cd /app/scripts/;/usr/local/bin/python /app/scripts/timer_add.py >> /var/log/timer.log 2>&1" >> /etc/crontab && /etc/init.d/cron start && /etc/init.d/cron status

# docker network内部网络通信，内部可直接访问该端口，不需要保留端口
#EXPOSE 8000

# 运行 Django ,此处必须加参数0.0.0.0:8000（不可省略0.0.0.0），否则django在桥接网络环境中不对请求响应
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# 改用uwsgi启动 uwsgi --ini /path/to/your/uwsgi.ini
CMD ["uwsgi", "/app/uwsgi.ini"]