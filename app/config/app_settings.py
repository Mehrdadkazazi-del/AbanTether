import json

with open("config.json", "r") as file:
    config = json.load(file)

APP_NAME = config['app']['name']
DEBUG = config['app']['debug']
DATABASE_URL = config['database']['url']
JOBS_ENABLED = config['jobs']['enable']
CRONE_EXPRESSION = config['jobs']['crone_expression']
OFFSET = config['jobs']['offset']
LIMIT = config['jobs']['limit']
SECRET_KEY = config['oauth2']['SECRET_KEY']
ALGORITHM = config['oauth2']['ALGORITHM']
ACCESS_TOKEN_EXPIRE_MINUTES = config['oauth2']['ACCESS_TOKEN_EXPIRE_MINUTES']
LIMIT_FOR_EXCHANGE = config['order_amount']['limit_for_exchange']
REDIS_HOST = config['redis']['host']
REDIS_PORT = config['redis']['port']
REDIS_DB = config['redis']['db']
