import os
import json
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.MySqlConnectionFactory import MysqlConnectFactory
'''
返回用于抽取规则的xml文件的location和type字典
格式：{'1':[xx,xx],'2':[xx,xx],'3':[xx,xx]}
'''

class FindallFiletype(object):
    def __init__(self):
        pass
    def filetype_dic(self):
        Mysql_factory = MysqlConnectFactory()
        conn = Mysql_factory.get_connect()
        conn.set_charset('utf8')
        cur = conn.cursor()
        cur.execute('SET NAMES utf8;')
        cur.execute('SET CHARACTER SET utf8;')
        cur.execute('SET character_set_connection=utf8;')
        sql = "SELECT location,ANY_VALUE(type)  FROM testdemo.tsp_full_info order by location asc"
        cur.execute(sql)
        data = cur.fetchall()
        tempDict={}
        //print(type(data[0][0]))
        for i in range(len(data)):
             #if data[i][0] == data[i+1][0]:
                 tempDict.setdefault(data[i][0], []).append(data[i][1])
                 #tempDict.update({"response": response_list})
        print(tempDict)
        cur.close()
        conn.close()
        return tempDict


def main():
        findall_filetype=FindallFiletype()
        findall_filetype.filetype_dic()


if __name__ == '__main__':
        main()
