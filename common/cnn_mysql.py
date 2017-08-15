#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-10 14:12:18
# @Author  : ditto (969956574@qq.com)
# @Link    : https://github.com/dittoyy
# @Version : $Id$
import MySQLdb
# import os
# os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

mysql_info = {"host": '127.0.0.1',
              "port": 3307,
              "user": 'root',
              "passwd": 'test',
              "db": 'test',
              "charset": 'utf8'}

class MysqlUtil():
    '''
    mysql数据库相关操作
    连接数据库信息：mysql_info
    创建游标：mysql_execute
    查询某个字段对应的字符串：mysql_getstring
    查询一组数据：mysql_getrows
    关闭mysql连接：mysql_close
    '''
    def __init__(self):
        self.db_info = mysql_info
        u'''连接池方式'''
        self.conn = MysqlUtil.__getConnect(self.db_info)

    @staticmethod
    def __getConnect(db_info):
        '''静态方法，从连接池中取出连接'''
        try:
            conn = MySQLdb.connect(host=db_info['host'],
                                   port=db_info['port'],
                                   user=db_info['user'],
                                   passwd=db_info['passwd'],
                                   db=db_info['db'],
                                   charset=db_info['charset'])
            return conn
        except Exception as a:
            print("数据库连接异常：%s"%a)

    def mysql_execute(self, sql):
        '''执行sql语句'''
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
        except Exception as a:
            self.conn.rollback()         # sql执行异常后回滚
            print("执行SQL语句出现异常：%s"%a)
        else:
            cur.close()
            self.conn.commit()          # sql无异常时提交

    def mysql_executemany(self, sql,list):
        '''执行sql语句'''
        cur = self.conn.cursor()
        try:
            cur.executemany(sql,list)
        except Exception as a:
            self.conn.rollback()         # sql执行异常后回滚
            print("执行SQL语句出现异常：%s"%a)
        else:
            cur.close()
            self.conn.commit()          # sql无异常时提交

    def mysql_getrows(self, sql):
        ''' 返回查询结果'''
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
        except Exception as a:
            print("执行SQL语句出现异常：%s"%a)
        else:
            rows = cur.fetchall()
            cur.close()
            return rows

    def mysql_getstring(self, sql):
        '''查询某个字段的对应值'''
        rows = self.mysql_getrows(sql)
        if rows != None:
            for row in rows:
                for i in row:
                    return i

    def mysql_close(self):
        ''' 关闭 close mysql'''
        try:
            self.conn.close()
        except Exception as a:
            print("数据库关闭时异常：%s"%a)

# MySQLdb.connect()     建立数据库连接
# cur = conn.cursor()    #通过获取到的数据库连接conn下的cursor()方法来创建游标。
# cur.execute()    #过游标cur 操作execute()方法可以写入纯sql语句。通过execute()方法中写如sql语句来对数据进行操作。
# cur.close()     # cur.close() 关闭游标
# conn.commit()   # conn.commit()方法在提交事物，在向数据库插入(或update)一条数据时必须要有这个方法，否则数据不会被真正的插入。
# conn.rollback() # 发生错误时候回滚
# conn.close()     # Conn.close()关闭数据库连接

if __name__ == "__main__":
    A = MysqlUtil()
    # sql = "SELECT  *FROM notify_request t where TEMPLATE_ID LIKE '16091%' ORDER BY t.REQUEST_TIME DESC  limit 0,1"#limitorderby查询
    # sql = "SELECT * FROM help_keyword limit 1,10"#查询
    # sql1='''create table if not exists honey4 (
    #         first_name char(20) primary key not null,
    #         last_name char(10) ,
    #         age int,
    #         sex char(10),
    #         income float)'''#创建数据表
    # sql='''insert into honey3(first_name,last_name,age,sex,income) values ('%s', '%s', '%d', '%c', '%d' ) '''\
    # %('7777c', 'M777an', 20, 'M', 2000)#插入可以多个直接传，也可以传指定的

    # sql='''UPDATE honey3 SET age = age + 1
    # WHERE sex = "%c"'''% ('M')#更新
    sqli="insert into honey3(first_name,last_name,age,sex,income) values (%s, %s, %r, %r, %r ) "
    list1=[
        ('737c', 'M477an', 77, 'M', 21),
        ('77447c', '377an', 77, 'M', 21),
        ('7755657c', '1777an', 23, 'M',21),
        ]
    A.mysql_executemany(sqli,list1)
    # A.mysql_execute(sql)
    # print A.mysql_getrows(sql)

    # print A.mysql_getstring(sql)
    A.mysql_close()

