import logging
import datetime
from mhzx.extensions import mongo
from mhzx.constant import *

logger = logging.getLogger(__name__)


def award_coin(user, object_id, award_type=AWARD_TYPE_ADD_BBS):
    coin = AWARD_COIN_NUMBER.get(award_type)
    if not coin:
        return
    mongo.db.users.update({"_id": user["_id"]}, {"$inc": {"coin": coin}})
    logger.info("#award user %s coin: %s, %s", user["loginname"], award_type, coin)
    record = {
        'loginname': user['loginname'],
        'object_id': object_id,
        'award_type': award_type,
        'coin': coin,
        'create_at': datetime.datetime.utcnow()
    }
    mongo.db.award_record.insert_one(record)


def recharge_coin(user, coin):
    if not coin:
        return True
    balance = user.get("coin", 0)
    if balance < 0:
        mongo.db.users.update({"_id": user["_id"]}, {"coin": 0})
        balance = 0
    if not (balance > 0 and coin <= balance):
        return False
    mongo.db.users.update({"_id": user["_id"]}, {"$inc": {"coin": -coin}})
    return True
