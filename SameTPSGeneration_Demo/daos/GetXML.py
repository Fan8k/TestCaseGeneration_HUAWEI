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

    def read_file(self, filepath):
        #filepath是待提取的XML的绝对路径
        path1 = os.path.abspath('..')

        #xmlpath =filepath+ '.xml'
        #print(xmlpath)
        item_list = []

        try:

            tree = ET.parse(filepath)
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
                    response_list.append(self.str_process(response_text[i].text, 0))
                    # if response_text[i].text != None:
                    #     if response_text[i].text.find('\n') != -1 or response_text[i].text.find('..') != -1:
                    #         response_content = response_text[i].text.replace('\n', '\\n').replace('..', '')
                    #         response_list.append(response_content)
                    #     #responsestr = responsestr + response_content
                    #     else:
                    #         response_list.append(response_text[i].text)
                    #
                    # else:
                    #     response_list.append(response_text[i].text)

                cmd_text = item.findall('cmd')
                for childText in cmd_text:
                    cmd_list.append(self.str_process(childText.text, 0))  # 0不删除...
                S_info = Item.Item(cmds=cmd_list, responses=response_list, score=0, location_info=None, num=count)

                item_list.append(S_info)

                count += 1

        except Exception as e:
            print("open exception: %s: %s\n" % (e.message, e.strerror))
        return item_list


    def str_process(self, str1,flag):
        resStr = ''

        if str1 != None:
            if str1.find('\n') != -1 or str1.find('..') != -1:
                if flag == 1:
                    response_content = str1.replace('\n', '\\n').replace('..', '')
                    resStr = resStr + response_content
                else:
                    response_content = str1.replace('\n', '\\n')
                    resStr = resStr + response_content
            else:
                resStr = resStr + str1

        else:
            resStr = resStr + 'None'
        return resStr


def main():
    path1 = os.path.abspath('..')

    rootdir = path1 + '/datas/data' + '/1'+'/001_normalTest'


    get_xml = GetXML()
    get_xml.read_file(rootdir)


if __name__=='__main__':
    main()
