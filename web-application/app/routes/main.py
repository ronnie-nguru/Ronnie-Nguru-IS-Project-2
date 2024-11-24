from flask import Blueprint, render_template, flash, render_template_string, request
import sqlite3
import html
import os
from config import config
from app.models import storage
from app.models.user import User
import time
from datetime import datetime

config_name = os.environ.get('BANK_SPHERE_CONFIG') or 'default'

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def index():
    """Render the home page."""
    return render_template('main/index.html')


@main.route('/sqli_demo', methods=['GET', 'POST'])
def vulnerable_search():
    results = []
    unsafe_query = ''

    if request.method == 'POST':
        username = request.form['username']
        start_time = time.time()
        unsafe_query = f"SELECT * FROM users WHERE username = '{username}'"

        try:
            conn = sqlite3.connect("data-dev.sqlite")
            cursor = conn.cursor()
            conn.execute("PRAGMA busy_timeout = 5000")
            cursor.execute(unsafe_query)
            results = cursor.fetchall()
            execution_time = time.time() - start_time

            if execution_time > 2:
                flash(f'Query took {execution_time:.2f} seconds to execute', 'warning')

            if ' UNION ' in username.upper():
                flash('UNION-based query detected', 'warning')


            flash(f'Found {len(results)} results', 'warning')

        except sqlite3.Error as e:
            error_msg = str(e)
            flash(f'SQL Error: {error_msg}', 'danger')

        finally:
            if 'conn' in locals():
                conn.close()

    return render_template(
        'sqli_test.html',
        unsafe_results=results,
        unsafe_query=html.escape(unsafe_query)
    )


@main.route('/secure', methods=['GET', 'POST'])
def secure_search():
    if request.method == 'GET':
        return render_template('sqli_test.html')

    username = request.form['username']
    results = []

    session = storage.get_session()
    try:
        results = session.query(User).filter(User.username == username).all()

        if results:
            flash(f'Found {len(results)} results securely', 'info')
        else:
            flash('No results found', 'info')


    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        results = []
    finally:
        session.close()

    return render_template('sqli_test.html', safe_results=results)
