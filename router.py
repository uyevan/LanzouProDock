import secrets
from datetime import timedelta

from flask import Flask

app = Flask(__name__,
            template_folder='./templates',
            static_folder='./templates/static',
            static_url_path='')
# app.secret_key = secrets.token_hex(16) 等同于下面一行
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=5)  # 存储五秒
