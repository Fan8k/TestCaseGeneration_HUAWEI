#coding=utf-8
'''
建立数据库信息，收集stackoverflow上面关于poi项目的所有帖子的：标题（title),帖子内容（body),回复内容(answer），最高评分赞的回复内容

建立：poi项目所有的方法的实体名字（entity）,方法的解释(explain)
'''

import pymysql


class MysqlConnectFactory(object):
    def __init__(self):
        self.INFO_1 = {'MYSQL_IPADDRESS': "10.141.221.85", 'MYSQL_USER': "root",
                       'MYSQL_PASSWORD': "root", 'MYSQL_DATABASENAME': "testdemo"}

    def get_connect(self):
        connection = None
        try:
            # 本质建立和mysql-server 建立socket通信
            connection = pymysql.connect(self.INFO_1['MYSQL_IPADDRESS'], self.INFO_1['MYSQL_USER'],
                                         self.INFO_1['MYSQL_PASSWORD'], self.INFO_1['MYSQL_DATABASENAME'], port=3306)
        except Exception as e:
            print(e)
        return connection

    @classmethod
    def close_connect(cls, connection):
        if connection:
            connection.close()
