import pymysql
import random
import string
import time
import json

db = pymysql.connect(host='localhost',port=3306,user='root',passwd='root',db='BIGWORK',charset='utf8')
 
#  执行sql语句
def sql_execute(sql):
    cursor = db.cursor()
    cursor.execute(sql)
    return cursor.fetchone()

# 生成token
def token_set(admin_name):
    sql = "SELECT id FROM admin_table where name = \'" + admin_name + "\'"
    admin_id = sql_execute(sql)
    # 获取id
    admin_id = admin_id[0]
    sql = (("SELECT user_id FROM user_token where user_id = %d") % (admin_id))
    data = sql_execute(sql)
    if data == None:
        # 生成token
        token = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(40))
        # 生成过期时间
        ex_time = time.time() + 24*3600
        sql = ("INSERT INTO user_token (user_id, user_token, expire_time) VALUES (%d, '%s', %d)" % (admin_id, token, ex_time))
        cursor = db.cursor()
        cursor.execute(sql)
        return token
    else:
        return None


# 处理接收到的信息
def msg_process(handle, type, admin_name, admin_pw):
    if type == 'login':
        sql = ("SELECT name FROM admin_table where name = '%s'" % (admin_name))
        data = sql_execute(sql)
        if data == None:
            print("用户不存在")
        else:
            sql = "SELECT passwd FROM admin_table where name = \'" + admin_name + "\' AND passwd = \'" + admin_pw +"\'";
            data = sql_execute(sql)
            if data == None:
                print("密码错误")
            else:
                token = token_set(admin_name)
                if token == None:
                    print("用户已登录")
                    msg = json.dumps({'cmd': 'login', 'status': 'REPEAT', 'data':  'None'})
                    # 发送
                    handle.write(msg)
                else:
                    msg = json.dumps({'cmd': 'login', 'status': 'SUCCESS', 'data':  token})
                    # 发送
                    handle.write(msg)
                    print("登录成功")
                    print ("token: %s " % token)
    elif type == 'register':
        sql = "SELECT name FROM admin_table where name = \'" + admin_name + "\'" 
        data = sql_execute(sql)
        if data == None:
            sql = "INSERT INTO admin_table (name,passwd) VALUES (\'" + admin_name + "\',\'" + admin_pw + "\')"
            cursor = db.cursor()
            cursor.execute(sql)
            print("注册成功")
            # handle.write("注册成功")
        else:
            print("用户已存在")
    else:
        print("不存在该类型")
    db.commit()