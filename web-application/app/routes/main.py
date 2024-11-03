from flask import Blueprint, render_template, flash, render_template_string, request
import sqlite3
import html
import os
from config import config
from app.models import storage
from app.models.user import User

config_name = os.environ.get('BANK_SPHERE_CONFIG') or 'default'

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def index():
    """Render the home page."""
    return render_template('main/index.html')


@main.route('/about')
def about():
    """Render the about page with information about the bank."""
    return render_template('main/about.html')


@main.route('/contact')
def contact():
    """Render the contact page for user inquiries."""
    return render_template('main/contact.html')


@main.route('/faq')
def faq():
    """Render the FAQ page."""
    return render_template('main/faq.html')


@main.route('/sqli_demo', methods=['GET', 'POST'])
def vulnerable_search():
    results = []
    unsafe_query = ''

    if request.method == 'POST':
        username = request.form['username']

        unsafe_query = f"SELECT * FROM users WHERE username = '{username}'"

        try:
            print(config[config_name].SQLALCHEMY_DATABASE_URI)
            conn = sqlite3.connect("data-dev.sqlite")
            cursor = conn.cursor()
            cursor.execute(unsafe_query)
            results = cursor.fetchall()
            flash(
                f'Found {len(results)} results', 'warning')

        except sqlite3.Error as e:
            flash(f'SQL Error: {str(e)}', 'danger')

        finally:
            if 'conn' in locals():
                conn.close()

    return render_template(
        'sqli_test.html',
        unsafe_results=results,
        unsafe_query=html.escape(unsafe_query)
    )


@main.route('/secure', methods=['POST'])
def secure_search():
    username = request.form['username']

    session = storage.get_session()
    try:
        results = session.query(User).filter(User.username == username).all()
        flash(f'Found {len(results)} results', 'info')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        results = []
    finally:
        session.close()

    return render_template('sqli_test.html', safe_results=results)
