import redis

from app.config.app_settings import REDIS_HOST, REDIS_PORT, REDIS_DB

REDIS = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=None,
    decode_responses=True,
)