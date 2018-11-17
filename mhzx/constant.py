# 官方邮件
EMAIL_TITLE = "官方"
EMAIL_TEXT = "这是您在官方论坛领取的奖励，请查收！"
PRODUCT_IMAGE = "/static/images/weixin.jpg"
# 金币奖励类型
AWARD_TYPE_ADD_BBS = "add_bbs"
AWARD_TYPE_REPLY_BBS = "reply_bbs"
AWARD_TYPE_DAILY_SIGN = "daily_sign"
AWARD_TYPE_REGISTER = "register"
AWARD_COIN_NUMBER = {
    AWARD_TYPE_ADD_BBS: 0,
    AWARD_TYPE_REPLY_BBS: 0,
    AWARD_TYPE_DAILY_SIGN: 1,
    AWARD_TYPE_REGISTER: 7
}

RESTRICT_AWARD_ONE = [
    AWARD_TYPE_ADD_BBS,
    AWARD_TYPE_REPLY_BBS,
]

# 短信类型
SMS_TYPE_REGISTER = 1           # 用户注册
SMS_TYPE_BACK_PASS = 2          # 找回密码


# 商品类型
PRODUCT_TYPE_GIFT = "礼包"

# 商品状态
PRODUCT_STATUS_NORMAL = "已上架"
PRODUCT_STATUS_EDIT = "上架中"
PRODUCT_STATUS_OUT = "已下架"

# 订单状态
ORDER_STATUS_INIT = "未使用"
ORDER_STATUS_USED = "已使用"
ORDER_STATUS_CANCEL = "已废弃"
ORDER_STATUS_VALID = [
    ORDER_STATUS_INIT,
    ORDER_STATUS_USED
]

# 权限列表
PERM_USER_GIFT_PROMO = "perm_promo"

# 金额类型
PRICE_TYPE_COIN = "金币"
PRICE_TYPE_CREDIT = "积分"

# 产品限制类型
LIMIT_TYPE_ONCE = "once"
LIMIT_TYPE_DAY = "day"
