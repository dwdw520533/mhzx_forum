import datetime
import hashlib
import logging
from mhzx.ops.mssql import Mysql
from mhzx.config import SQL_CONF

logger = logging.getLogger(__name__)


class ZxUser(object):
    def __init__(self, config):
        self.ms = Mysql(config)

    def get_user_credit(self, uid):
        return self.ms.first("select count(num) as credit from [dbo].[usercashnow] where ID=%s;" % uid)

    def get_user_by_uid(self, uid):
        return self.ms.first("select * from [dbo].[users] where ID=%s;" % uid)

    def get_user_by_name(self, name):
        return self.ms.first("select * from [dbo].[users] where name='%s';" % name)

    def get_user_by_question(self, name, question, answer):
        return self.ms.first("select * from [dbo].[users] where name='%s' and prompt='%s' and answer='%s';" %
                        (name, question, answer))

    def get_user_by_name_pwd(self, name, passwd):
        return self.ms.first("select * from [dbo].[users] where name='%s' and passwd=%s;" % (name, passwd))

    def get_latest_user_id(self):
        result = self.ms.first("select max(id) as id from [dbo].[users];")
        return result["id"] if result else None

    def register_user(self, name, passwd, question, answer, qq):
        user = self.get_user_by_name(name)
        if user:
            return False, "用户名已存在"
        latest_id = self.get_latest_user_id()
        if not latest_id:
            latest_id = 1
        uid = latest_id + 16
        passwd, email = self.get_password(name, passwd), "%s@qq.com" % qq
        values = ",".join([("%s" if idx == 2 else "'%s'") % i for idx, i in enumerate([
            uid, name, passwd, question, answer, name, name, email, qq,
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])])
        sql = "INSERT INTO [dbo].[users] (ID,name,passwd,prompt,answer," \
              "truename,idnumber,email,qq,creatime) VALUES(%s)" % values
        self.ms.execute_non_query(sql)
        return True, self.get_user_by_uid(uid)

    def get_password(self, name, pwd):
        return "0x" + hashlib.md5((name + pwd).encode("utf-8")).hexdigest().upper()

    def update_password(self, name, password):
        password = self.get_password(name, password)
        sql = "UPDATE [dbo].[users] SET passwd=%s where name='%s'" % (password, name)
        self.ms.execute_non_query(sql)

    def recharge_yb(self, name, cash, zone_id=1):
        cash = int(cash) * 100
        user = self.get_user_by_name(name)
        if not user:
            return False, "用户不存在"
        values = ",".join([str(user["ID"]), str(zone_id),
                           "0", "1", "0", str(cash), "1", "0"])
        sql = "exec usecash %s" % values
        self.ms.execute_non_query(sql)
        return True, None


user_sql = ZxUser(SQL_CONF)


def register_zx_user(*args, **kwargs):
    ret = user_sql.register_user(*args, **kwargs)
    logger.info("regist zx user ret: %s", ret)


def update_zx_user_password(*args, **kwargs):
    user_sql.update_password(*args, **kwargs)
