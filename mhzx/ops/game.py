import re
import paramiko
from mhzx.config import ZONE_SSH
from mhzx.extensions import mongo
from mhzx.mongo import UserRole


class CommandClient(object):
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def ssh_cmd(self, exe_cmd):
        paramiko.util.log_to_file("paramiko.log")
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(hostname=self.host, port=self.port,
                  username=self.user, password=self.password,
                  timeout=10)
        stdin, stdout, stderr = s.exec_command(exe_cmd)
        content = stdout.read()
        s.close()
        print(content)
        return content


def query_user_game_data(cmd_client, user):
    exe_cmd = "/root/gamedbd/gamedbd /root/gamedbd/gamesys.conf exportuser " + str(user["game_user_id"])
    content = cmd_client.ssh_cmd(exe_cmd).decode('gbk')
    if not content or content.startswith("err") or "NOTFOUND" in content:
        return None
    index = content.find("logicuid")
    return int("".join(re.findall(re.compile(r'[0-9]'), content[index:index + 40])))


def query_game_role_by_id(cmd_client, role_id):
    exe_cmd = "/root/gamedbd/gamedbd /root/gamedbd/gamesys.conf query " + str(role_id)
    content = cmd_client.ssh_cmd(exe_cmd).decode('gbk')
    if not content or content.startswith("err") or "NOTFOUND" in content:
        return {}
    data = dict()
    for i in content.split("\n\t"):
        line = i.split(":")
        if len(line) != 2:
            continue
        if line[0] == "ID":
            data["role_id"] = int(line[1])
        elif line[0] == "name":
            data["role_name"] = line[1]
        else:
            continue
    return data


def create_user_role(login_name, role_id, **kwargs):
    role = UserRole.objects(login_name=login_name, role_id=role_id).first()
    if not role:
        role = UserRole.create_new(login_name=login_name,
                                   role_id=role_id, **kwargs)
    return role


def query_user_game_roles(cmd_client, user):
    role_list = list(UserRole.objects(login_name=user["loginname"]).order_by("role_id"))
    if not role_list:
        query_role_id = user["role_cud"]
    elif len(role_list) < 8:
        query_role_id = role_list[-1].role_id + 1
    else:
        query_role_id = None
    if query_role_id:
        role = query_game_role_by_id(cmd_client, query_role_id)
        if role:
            role["game_user_id"] = user["game_user_id"]
            create_user_role(user["loginname"], **role)
    return True, [i.dict_data for i in UserRole.objects(
        login_name=user["loginname"]).order_by("role_id")]


def query_user_roles(zone_id, user):
    if not user.get("game_user_id"):
        return False, "游戏账号不存在"
    cfg = ZONE_SSH[zone_id]
    cmd_client = CommandClient(cfg["host"], cfg["port"],
                               cfg["user"], cfg["password"])
    if not user.get("role_cud"):
        role_cud = query_user_game_data(cmd_client, user)
        if not role_cud:
            return False, "账户角色信息获取失败"
        user["role_cud"] = role_cud
        mongo.db.users.update({"_id": user["_id"]}, {'$set': {"role_cud": role_cud}})
    return query_user_game_roles(cmd_client, user)


if __name__ == "__main__":
    cfg = ZONE_SSH["1"]
    cmd_client = CommandClient(cfg["host"], cfg["port"],
                               cfg["user"], cfg["password"])
    query_game_role_by_id(cmd_client, 2256)
