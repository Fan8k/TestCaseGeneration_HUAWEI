#-*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
import errno
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Item
from preprocess.StrProcess import StrProcess

'''
cll:对于新的xml文件进行item提取
flag:("是否保留'.'(0全部保留，1只保留保一个.")
'''
class GetXML:

    def read_file(self, filepath):
        #filepath是待提取的XML的绝对路径
        path1 = os.path.abspath('..')


        item_list = []
        preprocess = StrProcess()
        try:

            tree = ET.parse(filepath)
            root = tree.getroot()
            #print(root.tag)
            tmppath = os.path.basename(os.path.dirname(os.path.dirname(filepath)))
            location=tmppath + os.path.basename(os.path.dirname(filepath))
            #print(location)
            count = 0
            print("是否保留'.'(0全部保留，1只保留保一个.")
            flag = input()
            for item in root.findall('item'):
                cmd_list = []
                response_list = []

                response_text = item.findall('response')
                lenth = len(response_text)
                for i in range(lenth):
                    # print(tmp.text)
                    response_list.append(preprocess.str_process(response_text[i].text, flag))
                    '''
                      0不删除...
                      1表示去除....
                   '''


                cmd_text = item.findall('cmd')
                for childText in cmd_text:
                    cmd_list.append(preprocess.str_process(childText.text, flag))
                    '''
                    0不删除...
                    1表示去除....
                    '''
                S_info = Item.Item(cmds=cmd_list, responses=response_list, score=0, location_info=location, num=count)

                item_list.append(S_info)

                count += 1

        except FileNotFoundError as e:
            print(e)
        return item_list





def main():
    path1 = os.path.abspath('..')

    rootdir = path1 + '/datas/data' + '/5'+'/001_normalTest/uut-com.xml'


    get_xml = GetXML()
    items = get_xml.read_file(rootdir)
    print(items)
    mnum=0
    nmum=0
    for item in items:
        responselist=item.responses
        for i in range(len(responselist)):
            mnum+=responselist[i].count("Pass")
            nmum+=responselist[i].count("PASS")

    print(nmum)
    print(mnum+nmum)
if __name__=='__main__':
    main()
