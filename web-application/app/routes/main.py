from flask import Blueprint, render_template

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
