import json
import uuid
import base64
import random
import datetime
from decimal import Decimal
from bson import ObjectId
from mhzx import models
from flask import session


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def verify_num(code):
    from ..code_msg import VERIFY_CODE_ERROR

    if code != session['ver_code']:
        raise models.GlobalApiException(VERIFY_CODE_ERROR)
    # return result


def gen_verify_num():
    a = random.randint(-20, 20)
    b = random.randint(0, 50)
    data = {'question': str(a) + ' + ' + str(b) + " = ?", 'answer': str(a + b)}
    session['ver_code'] = data['answer']
    return data


def generate_cd_key(salt="sgzx123123", com=16, off=3):
    user_password = uuid.uuid1().hex
    new = base64.b64encode((user_password + salt).encode("utf-8"))
    new = new.decode("utf-8")
    if len(new) < com:
        new = new.ljust(com, "a")
    return new[off: com + off]


def format_data(data_list):
    from bson.objectid import ObjectId
    from mongoengine.fields import DecimalField

    def _convert(data):
        if isinstance(data, dict):
            for key, value in data.items():
                data[key] = _convert(value)
        elif isinstance(data, list):
            for idx, value in enumerate(data):
                data[idx] = _convert(value)
        elif isinstance(data, datetime.datetime):
            data = datetime.datetime.strftime(data, "%Y-%m-%d %H:%M:%S")
        elif isinstance(data, ObjectId):
            data = str(data)
        elif isinstance(data, (Decimal, DecimalField)):
            data = float(data)
        return data

    return _convert(data_list)
