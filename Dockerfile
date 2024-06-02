FROM python:3.10.10-alpine
WORKDIR /app
COPY LApi.py .
COPY requirements.txt .

RUN echo "deb http://mirrors.aliyun.com/debian jessie main">>/etc/apt/sources.list
echo "deb http://mirrors.aliyun.com/debian jessie-updates main">>/etc/apt/sources.list
RUN apt update
# Install all system pre-reqs
RUN apt install git
# Using douban pipy mirror
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -U pip
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install -r requirements.txt
CMD ["python","LApi.py"]