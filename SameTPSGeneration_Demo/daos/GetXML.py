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
            if com_list:
                for info_dir in com_list:
                    ext = os.path.splitext(info_dir)[1]#取文件后缀，找到.info
                    if ext==".info":
                        break
                for com_dir  in com_list :
                    item_list = []
                    if com_dir is not info_dir:
                        try:
                            item_list=parsexml.parse_xml(com_dir,info_dir,0)

                            yield item_list,com_list
                        except FileNotFoundError as e:
                           print(e)
            else:
                print("路径不正确")






def main():
    path1 = os.path.abspath('..')
    rootdir = path1 + '/datas/data/tps1/1' + '/001_normalTest'
    get_xml = GetXML()
    count = 0
    for items,comlist in get_xml.read_file(rootdir):#获取文件夹下所有com.xml文件内容

          print(items[4].responses)
          tree = ET.parse(items[4].location_info)
          root = tree.getroot()

          num = 0
          for item in root.findall('item'):
              num += 1
              if num == 5:
                  '''
                  item_info_list[file_count][1][0]为修改的item的index
                  修改loop
                  '''
                  print(item)
                  loop_text = item.find('loop')
                  loop_text.text = '3'
                  reponse_text = item.findall('response')
                  templist = items[4].responses

                  for i in range(len(reponse_text)):
                      if templist[i] == 'None':
                          reponse_text[i].text = ''
                      else:
                          s="me"+templist[i]
                          reponse_text[i].text = s
                          print(s)

                  tree.write(os.path.join(rootdir,str(count+1)+"new.xml"))
                  count+=1
                  break



if __name__ == '__main__':
    main()
