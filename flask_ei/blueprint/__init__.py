from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from models.models import db
from blueprint.routes.user import bp_user
from blueprint.routes.commodity import bp_commodity
from blueprint.routes.employees import bp_employees
from blueprint.routes.redis import bp_redis


def create_app():
    app = Flask(__name__)

    CORS(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    app.config['SECRET_KEY'] = '123_secret_key_here'
    app.config.from_pyfile('D:\\package\\code\\flask_ei\\config.py')

    db.init_app(app)

    # 注册蓝图，并传递mail对象
    register_blueprint(app)

    return app


# 注册蓝图
def register_blueprint(app: Flask):
    app.register_blueprint(bp_user)
    app.register_blueprint(bp_commodity)
    app.register_blueprint(bp_employees)
    app.register_blueprint(bp_redis)
