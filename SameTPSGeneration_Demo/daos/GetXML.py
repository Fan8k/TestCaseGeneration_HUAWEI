# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
import errno
import sys
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Item
from preprocess.StrProcess import StrProcess
from preprocess.GetFileDir import GetFileDir
from preprocess.ParseXml import ParseXml
'''f
cll:对于新的xml文件进行item提取
flag:("是否保留'.'(0全部保留，1只保留保一个.")
'''

file_filter = [".xml"]
class GetXML:

    def read_file(self, filepath):
        # filepath是待提取的XML的绝对路径
            getfiledir=GetFileDir()
            com_list=getfiledir.get_filedir(filepath)


            parsexml=ParseXml()
            for info_dir in com_list:
                ext = os.path.splitext(info_dir)[1]#取文件后缀，找到.info
                if ext==".info":
                    break
            print(info_dir)

            for com_dir  in com_list :
                item_list = []
                if com_dir is not info_dir:
                    try:
                        item_list=parsexml.parse_xml(com_dir,info_dir)

                        yield item_list,com_list
                    except FileNotFoundError as e:
                        print(e)






def main():
    path1 = os.path.abspath('..')
    rootdir = path1 + '/datas/data/tps1/1' + '/001_normalTest'
    get_xml = GetXML()

    for items,comlist in get_xml.read_file(rootdir):#获取文件夹下所有com.xml文件内容
          print(type(items))
          print(len(items))
          print(items[0].location_info)

    #
    # mnum = 0
    # nmum = 0
    # for item in items:
    #     responselist = item.responses
    #     for i in range(len(responselist)):
    #         mnum += responselist[i].count("Pass")
    #         nmum += responselist[i].count("PASS")
    #
    # print(nmum)
    # print(mnum + nmum)


if __name__ == '__main__':
    main()
