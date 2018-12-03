#coding=utf-8
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.MySqlConnectionFactory import MysqlConnectFactory
'''
author:cll
location 就是指的哪一个文件夹1，2，3，4，5....
type指的是模型组和原型组的文件夹名如：001_normalTest
返回itemlist,itemlist[0]为cmd, itemlist[1]为responde

'''


class SelectObject(object):

        def __init__(self):
            pass

        def selected_object(self,location,type):
            Mysql_factory = MysqlConnectFactory()
            conn=Mysql_factory.get_connect()
            cur=conn.cursor()
            item_list = []
            sql="select cmd,response from tsp_info where location='%s' and type='%s' " % (location, type)
            cur.execute(sql)
            data=cur.fetchone()
            #print(data[0])
            #print(data[1])
            item_list.append(data[0])
            item_list.append(data[1])
            return item_list


def main():
    location = input()
    filetype = input()
    itemlist = SelectObject()
    item = itemlist.selected_object(location, filetype)
    print(item[0])
    print(item[1])


if __name__=='__main__':
    main()


