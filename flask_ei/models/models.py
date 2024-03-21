# models/models.py
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


# 用户表
class user_list(db.Model, UserMixin):
    __tablename__ = 'user_list'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    cell = db.Column(db.String(255), nullable=False)
    sex = db.Column(db.String(255))
    address = db.Column(db.String(255))
    user_type = db.Column(db.String(50))
    balance = db.Column(db.String(20))

    def user_type_text(self):
        if self.user_type == '1':
            return '普通用户'
        elif self.user_type == '2':
            return '会员'
        elif self.user_type == '3':
            return '管理员'
        elif self.user_type == '100':
            return '全部'
        else:
            return '未知参数'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


# 商品表
class commodity(db.Model, UserMixin):
    __tablename__ = 'commodity'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    price = db.Column(db.String(10))
    type = db.Column(db.String(100))
    serial = db.Column(db.String(6))
    inventory = db.Column(db.Integer)
    status = db.Column(db.String(10))
    create_time = db.Column(db.DATETIME(6), nullable=False)

    def status_text(self):
        if self.status == '1':
            return '上架'
        elif self.status == '2':
            return '下架'
        elif self.status == '100':
            return '全部'
        else:
            return '参数错误'


# 员工表
class employees(db.Model, UserMixin):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    number = db.Column(db.String(10))
    salary = db.Column(db.Integer)
    title = db.Column(db.String(10))
    date = db.Column(db.DATETIME(6), nullable=False)


# 购物车
class ShoppingCart(db.Model, UserMixin):
    __tablename__ = 'shopping_cart'
    id = db.Column(db.Integer, primary_key=True)
    serial = db.Column(db.String(6), db.ForeignKey('commodity.serial'), nullable=False)
    commodity = db.relationship('commodity', backref=db.backref('shopping_cart', lazy=True))
    quantity = db.Column(db.Integer, default=1)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    create_time = db.Column(db.DATETIME(6), nullable=False)
