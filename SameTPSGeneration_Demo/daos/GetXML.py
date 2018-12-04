#-*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os

'''
cll:对于新的xml文件进行item提取
'''
class GetXML:

    @staticmethod
    def read_file(self, filepath):
        pass
        # path1 = os.path.abspath('..')
        # print(path1)
        # xmlpath =filepath+ 'com.xml'
        # print(xmlpath)
        # try:
        #
        #     tree = ET.parse(xmlpath)
        #     root = tree.getroot()
        #     print(root.tag)
        #     value = []
        #
        #     cmdtent = []
        #     cmdstr = ''
        #
        #     responsestr = ''
        #     count = 0
        #     for item in root.findall('item'):
        #         count += 2
        #         response_text = item.find('response').text
        #         cmd_text = item.find('cmd').text
        #         if cmd_text is not None:
        #             if cmd_text.find('\n') != -1:
        #                 cmd_text = cmd_text.replace('\n', '\\n')
        #                 cmdstr = cmdstr + cmd_text + '||'
        #                 #cmdtent.append(cmd_text)
        #                 #cmdtent.append("==")
        #             else:
        #                 cmdstr = cmdstr + cmd_text + '||'
        #                  #cmdtent.append(cmd_text)
        #                  #cmdtent.append("==")
        #         else:
        #             cmdstr = cmdstr + 'none' + '||'
        #
        #             #cmdtent.append(cmd_text)
        #             #cmdtent.append("==")
        #         if response_text is not None:
        #             if response_text.find('\n') != -1:
        #                 response_text = response_text.replace('\n', '\\n').replace('..', '')
        #                 responsestr = responsestr + response_text + '||'
        #                 #value.append(response_text)
        #                 #value.append("==")
        #             else:
        #                 responsestr = responsestr + response_text + '||'
        #                 #value.append(response_text)
        #                 #value.append("==")
        #         else:
        #             responsestr = responsestr + response_text + '||'
        #             #value.append(response_text)
        #             #value.append("==")
        # except Exception as e:
        #     print("open exception: %s: %s\n" %(e.errno, e.strerror))
        # return cmdstr, responsestr


def main():
    print("请输入TSP:")
    location = input()
    print("请输入文件类型（模型组/原型组）：")
    filetype = input()
    get_xml = GetXML()
    get_xml.read_file(location, filetype)


if __name__=='__main__':
    main()
