#-*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
import errno
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Item
'''
cll:对于新的xml文件进行item提取
'''
class GetXML:

    @staticmethod
    def read_file(filepath):

        path1 = os.path.abspath('..')
        print(path1)
        xmlpath =filepath+ '/com.xml'
        print(xmlpath)
        item_list = []

        try:

            tree = ET.parse(xmlpath)
            root = tree.getroot()
            print(root.tag)

            count = 0
            for item in root.findall('item'):
                cmd_list = []
                response_list = []

                response_text = item.findall('response')
                lenth = len(response_text)
                for i in range(lenth):
                    # print(tmp.text)

                    if response_text[i].text != None:
                        if response_text[i].text.find('\n') != -1 or response_text[i].text.find('..') != -1:
                            response_content = response_text[i].text.replace('\n', '\\n').replace('..', '')
                            response_list.append(response_content)
                        #responsestr = responsestr + response_content
                        else:
                            response_list.append(response_text[i].text)

                    else:
                        response_list.append(response_text[i].text)

                cmd_text = item.find('cmd').text
                if cmd_text != None:
                    if cmd_text.find('\n') != -1:
                        cmd_text = cmd_text.replace('\n', '\\n')
                        cmd_list.append(cmd_text)
                    else:
                        cmd_list.append(cmd_text)

                else:
                    cmd_list.append(cmd_text)
                S_info = Item.Item(cmds=cmd_list, responses=response_list)
                item_list.append(S_info)

        except Exception as e:
            print("open exception: %s: %s\n" % (e.message, e.strerror))
        return item_list



def main():
    path1 = os.path.abspath('..')
    # print(path1)
    rootdir = path1 + '/datas/data' + '/1'+'/001_normalTest'


    get_xml = GetXML()
    get_xml.read_file(rootdir)


if __name__=='__main__':
    main()
