from .models import R

# 通用
# SUCCESS = BaseResult(status=0, msg='操作成功')
SERVER_ERROR = R(status=500, msg='系统错误')
PARAM_ERROR = R(status=50001, msg='参数错误')
VERIFY_CODE_ERROR = R(status=50002, msg='验证码错误')
PERM_ERROR = R(status=50003, msg='对不起，您没有本次操作权限')

# 权限
USER_UN_LOGIN = R(status=403, msg='请先登录')
USER_UN_ACTIVE = R(status=403, msg='账号未激活')
USER_DISABLED = R(status=403, msg='账号已被禁用')
USER_UN_ACTIVE_OR_DISABLED = R(status=403, msg='账号未激活或已被禁用')
USER_UN_HAD_PERMISSION = R(status=403, msg='权限不足')

# 用户相关
CHANGE_PWD_SUCCESS = R(status=0, msg='密码修改成功')
PASSWORD_ERROR = R(status=50101, msg='密码错误')
USER_NOT_EXIST = R(status=50102, msg='用户不存在')
CHANGE_PWD_FAIL = R(status=50103, msg='密码修改失败，请联系管理员')
REPEAT_SIGNED = R(status=50105, msg='不能重复签到')
COIN_BALANCE_NOT_ENOUGH = R(status=50110, msg='您的账户金币不足')
CREDIT_BALANCE_NOT_ENOUGH = R(status=50110, msg='您的账户积分不足')

RE_PWD_MAIL_SEND = R(status=0, msg='密码重置邮件已发送，请前往邮箱查看')
RE_ACTIVATE_MAIL_SEND = R(status=0, msg='重新发送邮件成功, 请前往您的邮箱查看邮件激活你的账号')
REGISTER_SUCCESS = R(status=0, msg='用户注册成功, 请前往登录')
LOGIN_SUCCESS = R(status=0, msg='登录成功')

# 帖子
HAD_ACCEPTED_ANSWER = R(status=50201, msg='已有被采纳回答')
COMMENT_SUCCESS = R(status=0, msg='回帖成功')
COMMENT_SUCCESS_COIN = R(status=0, msg='回帖成功，奖励金币+1')
DELETE_SUCCESS = R(status=0, msg='删除成功')

# 参数校验相关 50001
# 用户
PASSWORD_LENGTH_ERROR = R(status=50001, msg='密码长度应该在6-16之间')
PASSWORD_REPEAT_ERROR = R(status=50001, msg='两次输入的密码不一致')
EMAIL_ERROR = R(status=50001, msg='邮箱格式不正确')
EMAIL_EMPTY = R(status=50001, msg='邮箱不能为空')
USER_ID_ERROR = R(status=50001, msg='用户名格式不正确')
USER_ID_EMPTY = R(status=50001, msg='用户名不能为空')
USER_ID_EXIST = R(status=50104, msg='该用户名已注册')
USER_ID_NOT_EXIST = R(status=50104, msg='该用户名未注册')
USERNAME_EMPTY = R(status=50001, msg='昵称不能为空')
QUESTION_EMPTY = R(status=50001, msg='密保问题不能为空')
QUESTION_ERROR = R(status=50001, msg='密保问题错误')
ANSWER_EMPTY = R(status=50001, msg='密保答案不能为空')
ANSWER_ERROR = R(status=50001, msg='密保答案错误')
NOW_PASSWORD_EMPTY = R(status=50001, msg='两次输入的密码不一致')
# 帖子
POST_TITLE_EMPTY = R(status=50001, msg='标题不能为空')
POST_CONTENT_EMPTY = R(status=50001, msg='内容不能为空')
POST_CATALOG_EMPTY = R(status=50001, msg='所属专栏不能为空')
POST_COIN_EMPTY = R(status=50001, msg='悬赏金币不能为空')
CATALOG_EMPTY = R(status=50001, msg='所属专栏不能为空')
# 文件
FILE_EMPTY = R(status=50001, msg='没有上传任何文件')
UPLOAD_UN_ALLOWED = R(status=50001, msg='不支持的文件格式')

# 短信
SMS_PHONE_ERROR = R(status=50201, msg='手机号错误')
SMS_PHONE_EXIST = R(status=50201, msg='手机号已被注册')
SMS_SEND_REPEAT = R(status=50201, msg='已发送短信验证码，不允许重复发送')
SMS_SEND_SUCCESS = R(status=0, msg='短信验证码发送成功')

# 订单
ORDER_NOT_EXIST = R(status=50301, msg='订单不存在')
ORDER_SURPASS_LIMIT = R(status=50302, msg='您已领取过该礼包，不可再次领取')

# 商品
PRODUCT_CODE_EMPTY = R(status=50401, msg='商品编号不能为空')
PRODUCT_NOT_EXIST = R(status=50402, msg='商品不存在')
