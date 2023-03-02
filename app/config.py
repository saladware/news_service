from os import getenv


# application config
APP_HOST = getenv("APP_HOST")
APP_PORT = getenv("APP_PORT")
SECRET_K = getenv("SECRET_K")

# database config
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_USER = getenv("DB_USER")
DB_PSWD = getenv("DB_PSWD")
DB_NAME = getenv("DB_NAME")

# auth config
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"  # edit, if you want to use in production
