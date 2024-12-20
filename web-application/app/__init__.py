from config import config
from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


bootstrap = Bootstrap()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    login_manager.init_app(app)

    from app.routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/app')

    from app.routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/app')

    from app.routes.accounts import accounts as accounts_blueprint
    app.register_blueprint(accounts_blueprint, url_prefix='/app')

    from app.routes.transactions import transactions as transactions_blueprint
    app.register_blueprint(transactions_blueprint, url_prefix='/app')

    return app
