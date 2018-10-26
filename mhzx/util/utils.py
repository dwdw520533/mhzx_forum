import json
import uuid
import base64
import random
from bson import ObjectId
from mhzx import models
from flask import session, request


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
