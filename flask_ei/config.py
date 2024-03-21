#
# from tornado.options import define
#
# # Redis配置
# define("dev_redis_host", default="8.140.118.229", help="Redis主机")
# define("dev_redis_database", default="15", help="Redis数据库")
# define("dev_redis_password", default="sg@123456", help="Redis密码")

# Flask配置
SECRET_KEY = 'your_ei_key'
DEBUG = True

# SQLAlchemy配置
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:325325@localhost/test'
SQLALCHEMY_TRACK_MODIFICATIONS = False


# 发送邮件服务器：smtp.qq.com，使用SSL，端口号465或587
MAIL_SERVER = 'smtp.qq.com'
# 发送邮件的端口
MAIL_PORT = 587
# 传输安全服务器协议
MAIL_USE_TLS = True
# 用户名也就是qq邮箱账号
MAIL_USERNAME = '671219225@qq.com'
# 授权码
MAIL_PASSWORD = 'duodomoybnhjbgaa'
