import datetime
from mongoengine import *
from mhzx.constant import *


class NewObjectMixin(object):
    @classmethod
    def create_new(cls, **kwargs):
        obj = cls(**kwargs)
        obj.save()
        return obj


class PhoneCode(DynamicDocument):
    """
    Telephone verification code.
    """
    meta = {"db_alias": "mhzx",
            "indexes": ["code", "phone_number"]}

    login_name = StringField(required=True)
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


class Product(DynamicDocument):
    """
    product model.
    """
    meta = {"db_alias": "mhzx",
            "indexes": ["product_code", "created"]}

    product_code = StringField(required=True)
    product_name = StringField(required=True)
    product_type = StringField(default=PRODUCT_TYPE_GIFT)
    product_image = StringField(default=PRODUCT_IMAGE)
    price = IntField(default=1)
    price_type = StringField(default=PRICE_TYPE_COIN)
    item = IntField(default=0)
    num = IntField(default=1)
    title = StringField(default=EMAIL_TITLE)
    text = StringField(default=EMAIL_TEXT)
    limit = IntField(default=1)
    limit_type = StringField(default=LIMIT_TYPE_ONCE)
    inventory = IntField(default=9999)
    require_perm = StringField()
    sale_num = IntField(default=0)
    content = StringField()
    view_count = IntField(default=0)
    status = StringField(default=PRODUCT_STATUS_NORMAL)

    created = DateTimeField(default=datetime.datetime.now)
    lut = DateTimeField(default=datetime.datetime.now)

    @property
    def dict_data(self):
        return {
            "product_id": str(self.id),
            "product_name": self.product_name,
            "product_code": self.product_code,
            "product_type": self.product_type,
            "product_image": self.product_image,
            "inventory": self.inventory,
            "sale_num": self.sale_num,
            "view_count": self.view_count,
            "price": self.price,
            "limit": self.limit,
            "price_type": self.price_type,
            "content": self.content,
            "status": self.status
        }


class Order(DynamicDocument):
    """
    order model.
    """
    meta = {"db_alias": "mhzx",
            "indexes": ["user_id", "product", "created"]}

    user_id = StringField(required=True)
    product = ReferenceField(Product)
    price = IntField(default=0)
    cd_key = StringField()
    num = IntField(default=1)
    status = StringField(default=ORDER_STATUS_INIT)

    created = DateTimeField(default=datetime.datetime.now)
    lut = DateTimeField(default=datetime.datetime.now)

    @property
    def dict_data(self):
        return {
            "order_id": str(self.id),
            "user_id": self.user_id,
            "cd_key": self.cd_key,
            "product": self.product.dict_data
        }


class UserRole(DynamicDocument, NewObjectMixin):
    """
    user role model.
    """
    meta = {"db_alias": "mhzx",
            "indexes": ["login_name", "game_user_id", "created"]}

    login_name = StringField(required=True)
    role_id = IntField(required=True)
    game_user_id = IntField()
    role_name = StringField()

    created = DateTimeField(default=datetime.datetime.now)
    lut = DateTimeField(default=datetime.datetime.now)

    @property
    def dict_data(self):
        return {
            "role_id": self.role_id,
            "role_name": self.role_name
        }
