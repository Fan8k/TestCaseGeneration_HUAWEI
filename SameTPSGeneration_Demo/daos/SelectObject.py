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
            sql="select location,cmd_response from tsp_full_info where location=%s and type=%s"
            cur.execute(sql,(location,type))
            data = cur.fetchone()
            location = data[0]

            cmd_response_Info = json.loads(data[1])#字符串转换为字典

            for i in range(len(cmd_response_Info)):


                S_info = Item.Item(cmds=cmd_response_Info[str(i)]["cmd"],
                                   responses=cmd_response_Info[str(i)]["response"], score=0, location_info=location,
                                   num=i)
                item_list.append(S_info)

            cur.close()
            conn.close()
            return item_list

def main():
    location = "1"
    filetype = "001_normalTest"
    itemlist = SelectObject()
    item = itemlist.selected_object(location, filetype)
    print(item)


if __name__=='__main__':
    main()


