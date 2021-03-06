import logging
import datetime
from mhzx.constant import *
from mhzx.extensions import mongo
from mhzx.mongo import AwardRestrict

logger = logging.getLogger(__name__)


def restrict_award_daily_one(user, award_type):
    if award_type not in RESTRICT_AWARD_ONE:
        return False
    date = datetime.datetime.now().strftime('%Y-%m-%d')
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
        'create_at': datetime.datetime.now()
    }
    mongo.db.award_record.insert_one(record)
    return True


def add_credit(user, credit=None):
    if not credit:
        return False
    mongo.db.users.update({"_id": user["_id"]}, {"$inc": {"credit": credit}})
    logger.info("#add user %s credit: %s", user["loginname"], credit)
    record = {
        'loginname': user['loginname'],
        'object_id': "",
        'award_type': "",
        'credit': credit,
        'create_at': datetime.datetime.now()
    }
    mongo.db.award_record.insert_one(record)
    return True


def recharge_coin(user, amount):
    if not amount:
        raise ValueError("amount value not allow empty!")
    balance = user.get("coin", 0)
    if balance < 0:
        mongo.db.users.update({"_id": user["_id"]}, {'$set': {"coin": 0}})
        balance = 0
    if not (balance > 0 and amount <= balance):
        return False
    mongo.db.users.update({"_id": user["_id"]}, {"$inc": {"coin": -amount}})
    return True


def recharge_credit(user, amount):
    if not amount:
        raise ValueError("amount value not allow empty!")
    balance = user.get("credit_balance", 0)
    if not (balance and amount <= balance):
        return False
    mongo.db.users.update({"_id": user["_id"]}, {
        "$inc": {"credit_used": amount}})
    return True
