# DEVELOPMENT
# REDIS_URI = "redis://:137048@172.26.73.168:6379"
# SQLALCHEMY_DATABASE_URI = "postgresql://taxi:ExpressTaxi.@localhost/db_taxi"
# SECRET_KEY = "a10c108dd03e3709ab6c0497e6dba56dc9bdbd77f3f0fa00ac57eca21547ffd1"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 600

# PRODUCTION
REDIS_URI = "redis://:@localhost:6379"
SQLALCHEMY_DATABASE_URI = "postgresql://taxi:ExpressTaxi.@216.250.10.47/db_taxi"
SECRET_KEY = "a10c108dd03e3709ab6c0497e6dba56dc9bdbd77f3f0fa00ac57eca21547ffd1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Mail
MAIL_DEFAULT_SENDER = "testapp@local.host"
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = "elitetaxi1992@gmail.com"
MAIL_RECEIVERS = ["artykow.serdar@gmail.com"]
MAIL_PASSWORD = "EliteT@xi1992!"

