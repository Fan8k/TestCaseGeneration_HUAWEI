#-*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os

'''
cll:对于新的xml文件进行item提取
'''
class GetXML:

    @staticmethod
    def read_file(self, filepath):

        path1 = os.path.abspath('..')
        print(path1)
        xmlpath =filepath+ 'com.xml'
        print(xmlpath)
        item_list = []
        try:

            tree = ET.parse(xmlpath)
            root = tree.getroot()
            print(root.tag)

            count = 0
            for item in root.findall('item'):
                cmdstr = ''
                responsestr = ''

                response_text = item.findall('response')
                lenth = len(response_text)
                for i in range(lenth):
                    # print(tmp.text)

                    if response_text[i].text != None:
                        if response_text[i].text.find('\n') != -1 or response_text[i].text.find('..') != -1:
                            response_content = response_text[i].text.replace('\n', '\\n').replace('..', '')
                        responsestr = responsestr + response_content
                        if i > 0 and i < lenth - 1:
                            responsestr = responsestr + '||'

                    else:
                        responsestr = responsestr + 'None'
                        if lenth > 1 and i + 1 < lenth:
                            responsestr = responsestr + '||'
                cmd_text = item.find('cmd').text


                if cmd_text != None:
                    if cmd_text.find('\n') != -1:
                        cmd_text = cmd_text.replace('\n', '\\n')

                    cmdstr = cmdstr + cmd_text



                else:
                    cmdstr = cmdstr + 'None'
                S_info = Info(cmdstr, responsestr)
                item_list.append(S_info)

        except Exception as e:
            print("open exception: %s: %s\n" %(e.errno, e.strerror))
        return item_list


class Info(object):

    def __init__(self, cmd, response):
        self.cmd = cmd
        self.response = response

def main():
    print("请输入TSP:")
    location = input()
    print("请输入文件类型（模型组/原型组）：")
    filetype = input()
    get_xml = GetXML()
    get_xml.read_file(location, filetype)


if __name__=='__main__':
    main()
