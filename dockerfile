FROM artifactory.homelab.com/docker.io/python:3.12.6-slim
LABEL  maintainer Xi Siyuan "yokoxsy@msn.com"

WORKDIR /app
EXPOSE 5000

COPY requirements /tmp

RUN cd  /tmp \
    && pip install -r requirements  -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com \
    && rm requirements \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

COPY . /app

CMD ["python"]
