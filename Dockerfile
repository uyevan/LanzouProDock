FROM python:3.10.10-alpine
WORKDIR /app

# 复制必要的文件和目录
COPY application.py .
COPY router.py .
COPY requirements.txt .
COPY api ./api
COPY templates ./templates
COPY gunicorn_conf.py .

# 配置国内源，加速依赖安装
RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install -r requirements.txt

# 暴露端口
EXPOSE 3307

# 启动应用
CMD ["python", "application.py"]
