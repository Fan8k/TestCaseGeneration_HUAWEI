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
            #com_list=self.get_filedir(filepath)
            print(com_list)
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
                        #print(item_list[1].location_info)
                        yield item_list
                    except FileNotFoundError as e:
                        print(e)



    # def parse_xml(self,xmlpath,info_dir):
    #     item_list=[]
    #     preprocess = StrProcess()
    #     tree = ET.parse(xmlpath)
    #     root = tree.getroot()
    #     tree2 = ET.parse(info_dir)
    #     root2 = tree2.getroot()
    #
    #     # print("com_dir:"+os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(com_dir)))))
    #     # print("tmp:"+os.path.basename(os.path.dirname(com_dir)))
    #     # tmppath = os.path.join(os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(com_dir)))),
    #     #                        os.path.dirname(os.path.dirname(os.path.dirname(com_dir))))
    #     # print("tmppath:"+tmppath)
    #     # location =os.path.join(tmppath , os.path.basename(os.path.dirname(filepath)))
    #     # print("location:"+location)
    #     first_item = root2.find('sceneinfo')
    #     score_list = first_item.findall('score')
    #     if len(score_list) == 0:
    #         _score = 0.0
    #     else:
    #         for i in range(len(score_list)):
    #             _score = float(score_list[i].text)
    #     count = 0
    #
    #     for item in root.findall('item'):
    #         cmd_list = []
    #         response_list = []
    #
    #         response_text = item.findall('response')
    #         lenth = len(response_text)
    #         for i in range(lenth):
    #             # print(tmp.text)
    #             response_list.append(preprocess.str_process(response_text[i].text, 0))
    #             '''
    #               0不删除...
    #               1表示去除....
    #            '''
    #
    #         cmd_text = item.findall('cmd')
    #         for childText in cmd_text:
    #             cmd_list.append(preprocess.str_process(childText.text, 0))
    #             '''
    #             0不删除...
    #             1表示去除....
    #             '''
    #         S_info = Item.Item(cmds=cmd_list, responses=response_list, score=_score, location_info=xmlpath, num=count)
    #
    #         item_list.append(S_info)
    #
    #         count += 1
    #     return item_list


def main():
    path1 = os.path.abspath('..')
    rootdir = path1 + '/datas/data/tps1/1' + '/001_normalTest'
    get_xml = GetXML()

    for items in get_xml.read_file(rootdir):#获取文件夹下所有com.xml文件内容
          print(type(items))
          print(len(items))
          print(items[1])

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
