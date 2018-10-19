from flask_mail import Message
from mhzx.config import MailConfig
import mhzx
def send_email(to, subject):
    msg = Message(subject=MailConfig.MAIL_SUBJECT_PREFIX + subject , sender=MailConfig.MAIL_SENDER, recipients=[to])
    msg.body = "测试测试"
    msg.html = "<a href='://baidu.com'>点击打开百度</a>"
    print(mhzx.mongodb)
    mhzx.mail.send(msg)
