from datetime import timedelta

from flask import Flask
from flask_session import Session

app = Flask(__name__,
            template_folder='./templates',
            static_folder='./templates/static',
            static_url_path='')
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'fkdjsafjdkfdlkjfadskjfadskljdsfklj'
app.permanent_session_lifetime = timedelta(minutes=1)  # 存储5秒
Session(app)
