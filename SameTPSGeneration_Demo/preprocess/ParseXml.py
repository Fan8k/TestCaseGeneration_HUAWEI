import xml.etree.ElementTree as ET
import os

import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Item
from preprocess.StrProcess import StrProcess
from preprocess.GetFileDir import GetFileDir

class ParseXml:
    def parse_xml(self,xmlpath,info_dir,flag):
        item_list=[]
        preprocess = StrProcess()
        tree = ET.parse(xmlpath)
        root = tree.getroot()
        tree2 = ET.parse(info_dir)
        root2 = tree2.getroot()
        first_item = root2.find('sceneinfo')
        score_list = first_item.findall('score')
        if len(score_list) == 0:
            _score = 0.0
        else:
            for i in range(len(score_list)):
                _score = float(score_list[i].text)
        count = 0

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
            S_info = Item.Item(cmds=cmd_list, responses=response_list, score=_score, location_info=xmlpath, num=count)

            item_list.append(S_info)

            count += 1
        return item_list

    def parse_xml2(self, xmlpath, info_dir,tpsdir,flag):
        item_list = []
        preprocess = StrProcess()
        tree = ET.parse(xmlpath)
        root = tree.getroot()
        tree2 = ET.parse(info_dir)
        root2 = tree2.getroot()
        first_item = root2.find('sceneinfo')
        score_list = first_item.findall('score')
        if len(score_list) == 0:
            _score = 0.0
        else:
            for i in range(len(score_list)):
                _score = float(score_list[i].text)
        count = 0

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
            S_info = Item.Item(cmds=cmd_list, responses=response_list, score=_score, location_info=tpsdir, num=count)

            item_list.append(S_info)

            count += 1
        return item_list


    def parse_xml3(self,xmlpath,flag):
        item_list=[]
        preprocess = StrProcess()
        tree = ET.parse(xmlpath)
        root = tree.getroot()

        count = 0

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
            S_info = Item.Item(cmds=cmd_list, responses=response_list, score=0.0, location_info=xmlpath, num=count)

            item_list.append(S_info)

            count += 1
        return item_list
