#!/usr/bin/python3
import os

from app import create_app, login_manager
from app.models import storage
from datetime import datetime

app = create_app(os.environ.get('BANK_SPHERE_CONFIG') or 'default')

host = os.environ.get('BANK_SPHERE_WEBHOST') or '0.0.0.0'
port = os.environ.get('BANK_SPHERE_WEBPORT') or 4000


@login_manager.user_loader
def load_user(user_id):
    return storage.get('User', user_id)


@app.teardown_appcontext
def teardown_db(exception):
    storage.close()

@app.template_filter('datetime')
def format_datetime(value):
    if value:
        return value.strftime('%Y-%m-%d %H:%M:%S')
    return ''

if __name__ == '__main__':
    app.run(host=host, port=port)
