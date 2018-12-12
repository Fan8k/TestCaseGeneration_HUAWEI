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

            count = 0
            for item in root.findall('item'):
                cmd_list = []
                response_list = []

                response_text = item.findall('response')
                lenth = len(response_text)
                for i in range(lenth):
                    # print(tmp.text)
                    response_list.append(preprocess.str_process(response_text[i].text, 0))
                    '''
                      0不删除...
                      1表示去除....
                     '''

                cmd_text = item.findall('cmd')
                for childText in cmd_text:
                    cmd_list.append(preprocess.str_process(childText.text, 0))
                    '''
                    0不删除...
                    1表示去除....
                    '''
                S_info = Item.Item(cmds=cmd_list, responses=response_list, score=0, location_info=None, num=count)

                item_list.append(S_info)

                count += 1

        except FileNotFoundError as e:
            print(e)
        return item_list





def main():
    path1 = os.path.abspath('..')

    rootdir = path1 + '/datas/data' + '/2'+'/001_normalTest/com.xml'


    get_xml = GetXML()
    items = get_xml.read_file(rootdir)
    for item in items:
        print(item)

if __name__=='__main__':
    main()
