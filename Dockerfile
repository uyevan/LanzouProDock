FROM python:3.10.10-alpine
WORKDIR /app
COPY LApi.py .
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["python","LApi.py"]