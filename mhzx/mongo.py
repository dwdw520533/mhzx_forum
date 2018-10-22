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

    created = DateTimeField(required=True, default=datetime.datetime.now)
