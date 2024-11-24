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


def init_test_db():
    """Initialize test database with sample data"""
    conn = sqlite3.connect("data-dev.sqlite")
    cursor = conn.cursor()
    try:
        # Create users table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT,
                created_at TEXT
            )
        """)
        
        # Create a secondary table for UNION injection tests
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_user_details (
                user_id INTEGER PRIMARY KEY,
                address TEXT,
                phone TEXT,
                FOREIGN KEY (user_id) REFERENCES test_users (id)
            )
        """)
        
        # Insert sample data if table is empty
        cursor.execute("SELECT COUNT(*) FROM test_users")
        if cursor.fetchone()[0] == 0:
            sample_data = [
                ('admin', 'admin123', 'admin@example.com', datetime.now().isoformat()),
                ('user1', 'pass123', 'user1@example.com', datetime.now().isoformat()),
                ('test_user', 'test123', 'test@example.com', datetime.now().isoformat())
            ]
            cursor.executemany(
                "INSERT INTO test_users (username, password, email, created_at) VALUES (?, ?, ?, ?)",
                sample_data
            )
            
            # Insert sample user details
            cursor.execute("""
                INSERT INTO test_user_details (user_id, address, phone) 
                VALUES (1, '123 Admin St', '555-0123')
            """)
            
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")
    finally:
        conn.close()

@main.route('/sqli_demo', methods=['GET', 'POST'])
def vulnerable_search():
    results = []
    unsafe_query = ''
    
    if request.method == 'GET':
        init_test_db()
    
    if request.method == 'POST':
        username = request.form['username']
        
        # Record the start time for timing attacks
        start_time = time.time()
        
        unsafe_query = f"SELECT * FROM test_users WHERE username = '{username}'"
        
        try:
            conn = sqlite3.connect("data-dev.sqlite")
            cursor = conn.cursor()
            
            # Set a timeout for time-based attacks
            conn.execute("PRAGMA busy_timeout = 5000")  # 5 second timeout
            
            cursor.execute(unsafe_query)
            results = cursor.fetchall()
            
            # Handle time-based injection detection
            execution_time = time.time() - start_time
            if execution_time > 2:  # If query took more than 2 seconds
                flash(f'Query took {execution_time:.2f} seconds to execute', 'warning')
            
            # Detect potential UNION-based attacks
            if ' UNION ' in username.upper():
                flash('UNION-based query detected', 'warning')
            
            # Detect potential information schema queries
            if 'sqlite_master' in username.lower():
                flash('Attempt to query database schema detected', 'warning')
            
            flash(f'Found {len(results)} results', 'warning')
            
            # Log the query for demonstration purposes
            print(f"Executed query: {unsafe_query}")

        except sqlite3.Error as e:
            error_msg = str(e)
            flash(f'SQL Error: {error_msg}', 'danger')
            
            # Provide helpful hints for different types of errors
            if 'no such table' in error_msg.lower():
                flash('Hint: Table might not exist or database structure is different', 'info')
            elif 'syntax error' in error_msg.lower():
                flash('Hint: SQL syntax error in injection attempt', 'info')
            elif 'no such column' in error_msg.lower():
                flash('Hint: Column name might be incorrect or database structure is different', 'info')
                
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
        # Demonstrate proper parameter binding
        results = session.query(User).filter(User.username == username).all()
        
        if results:
            flash(f'Found {len(results)} results securely', 'info')
        else:
            flash('No results found', 'info')
            
        # Show how the secure query is constructed
        flash(f'Secure query used parameterized binding: User.username == ?', 'info')
        
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        results = []
    finally:
        session.close()

    return render_template('sqli_test.html', safe_results=results)