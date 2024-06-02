FROM python:3.10.10-alpine
WORKDIR /app
COPY LApi.py .
COPY requirements.txt .
RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install -r requirements.txt
CMD ["python","LApi.py"]