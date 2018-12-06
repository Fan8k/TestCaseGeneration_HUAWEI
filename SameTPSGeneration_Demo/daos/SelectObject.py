#coding=utf-8
import os
import json
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Item
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
            sql="select cmd_response from tsp_info where location='%s' and type='%s' " % (location, type)
            cur.execute(sql)
            data = cur.fetchone()

            cmd_response_Info=json.loads(data[0])#字符串转换为字典

            for i in range(len(cmd_response_Info)):
                #cmd_response_Info[i]['cmd']
                #print(cmd_response_Info[str(i)]["cmd"])
                S_info = Item.Item(cmds=cmd_response_Info[str(i)]["cmd"], responses=cmd_response_Info[str(i)]["response"])
                item_list.append(S_info)
            print(item_list[1].responses)
            return item_list


def main():
    location = "1"
    filetype = "001_normalTest"
    itemlist = SelectObject()
    item = itemlist.selected_object(location, filetype)



if __name__=='__main__':
    main()


