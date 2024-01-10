from menglingtool.goodlib import ThreadDictGoods
from menglingtool_redis.redis_tool import RedisExecutor

RCONF = {

}

TDG = ThreadDictGoods({'r': [RedisExecutor, RCONF]})


def original() -> list:
    pass
    return []
