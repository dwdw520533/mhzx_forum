# -*- coding=utf-8 -*-
"""
Verify user"s mobile phone.
"""
import re
import random
import datetime
from mhzx.util import sms
from mhzx.util import cache
from mhzx.constant import *
from mhzx.mongo import PhoneCode

CODE_TIMEOUT = 3600


def filter_phone(phone_number):
    """
    过滤手机号特殊字符
    :param phone_number: 手机号
    """
    if not phone_number:
        return None
    for i in phone_number:
        if not i.isdigit():
            phone_number = phone_number.replace(i, "")
    regex = re.compile(r"^1[3456789][\d]{9}$", re.IGNORECASE)
    match = re.search(regex, phone_number)
    return match.group() if match else None


def generate_verify_code(phone_number, sms_type=SMS_TYPE_REGISTER):
    phone_key = "phone_verify_%s_%s" % (phone_number, sms_type)
    if not cache.add(phone_key, 1, 60):
        return None
    phone_code = PhoneCode.objects(
        verified=None, phone_number=phone_number,
        sms_type=sms_type).order_by("-created").first()
    if phone_code and phone_code.created + datetime.timedelta(0, CODE_TIMEOUT) >= \
            datetime.datetime.now():
        code = phone_code.code
    else:
        code = "%06d" % random.randint(0, 100000)
    phone_code = PhoneCode.get(code=code, phone_number=phone_number)
    if not phone_code:
        phone_code = PhoneCode(code=code, phone_number=phone_number)
    phone_code.verified = None
    phone_code.sms_type = sms_type
    phone_code.save()
    return phone_code


def send_sms_phone_code(phone_code):
    """
    Send the sms, phone_code is the PhoneCode object.
    """
    sms.aliyun_send(phone_code.phone_number, phone_code.code)
    print("Send verify code %s to %s" % (phone_code.code, phone_code.phone_number))


def verify_phone_code(phone_number, code, sms_type=SMS_TYPE_REGISTER):
    phone_code = PhoneCode.objects(code=code, sms_type=sms_type,
                                   phone_number=phone_number).first()
    if not phone_code:
        return None
    if phone_code.created + datetime.timedelta(0, CODE_TIMEOUT)\
            < datetime.datetime.now():
        return None
    if phone_code.verified:
        return None
    phone_code.verified = datetime.datetime.now()
    phone_code.save()
    return phone_code
