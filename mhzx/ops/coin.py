import logging
import datetime
from mhzx.constant import *
from mhzx.extensions import mongo
from mhzx.mongo import AwardRestrict

logger = logging.getLogger(__name__)


def restrict_award_daily_one(user, award_type):
    if award_type not in RESTRICT_AWARD_ONE:
        return False
    date = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    restrict_key = "restrict_key_%s_%s" % (award_type, date)
    restrict = AwardRestrict.objects(user_id=str(user["_id"]),
                                     restrict_key=restrict_key,
                                     restrict_type=1).first()
    if restrict:
        return True
    restrict = AwardRestrict(user_id=str(user["_id"]),
                             restrict_key=date,
                             restrict_type=1)
    restrict.save()
    return False


def award_coin(user, object_id, award_type=AWARD_TYPE_ADD_BBS, coin=None):
    coin = coin or AWARD_COIN_NUMBER.get(award_type)
    if not coin:
        return False
    is_restrict = restrict_award_daily_one(user, award_type)
    if is_restrict:
        return False
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
    return True


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
