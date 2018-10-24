import datetime
from mongoengine import *


class PhoneCode(DynamicDocument):
    """
    Telephone verification code.
    """
    meta = {"db_alias": "mhzx",
            "indexes": ["code", "phone_number"]}

    phone_number = StringField(required=True)
    code = StringField(required=True)
    sms_type = IntField(default=1)
    verified = DateTimeField()

    created = DateTimeField(default=datetime.datetime.now)


class AwardRestrict(DynamicDocument):
    """
    award restrict model.
    """
    meta = {"db_alias": "mhzx",
            "indexes": ["user_id", "restrict_key"]}

    user_id = StringField(required=True)
    restrict_key = StringField(required=True)
    restrict_type = IntField(default=1)
    created = DateTimeField(default=datetime.datetime.now)
