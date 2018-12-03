#coding=utf-8
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from daos.SelectObject import SelectObject
from utils.MD5 import MD5
from models.Rule import Rule

'''
从items中提取规则
'''

class ExtractRules:

    st = SelectObject()
    md5 = MD5()

    def get_items(self,location,type):
        '''
        :param location: 测试数据中的编码
        :param type: 模型组和原型组数据所在文件夹的名字
        :return: 从数据库中获取到的item对象
        '''
        return ExtractRules.st.selected_object(location,type)


    def get_rules(self,proto_items,model_items):

        '''
        原型组和模型组提取的item正常情况下等大小，而且是一对一的关系
        :param proto_items: 获取到的原型组item对象的集合
        :param model_items: 获取到的模型组item对象的集合
        :return: <context,from,to,location>
        '''
        #获取修改过的item对象
        for index in range(len(proto_items)):
            pri_item = proto_items[index]
            model_item = proto_items[index]
            for response_index in range(len(pri_item.responses)):
                #对应的item对象的response字符串
                pri_response_str = ExtractRules.md5.encode(pri_item.responses[response_index])
                model_response_str = ExtractRules.md5.encode(model_item.responses[response_index])
                if pri_response_str != model_response_str:
                     #找出修改点及其在原来字符串中的位置信息
                     self.find_change_points(pri_response_str,model_response_str)

    def find_change_points(self,pri_response_str,model_response_str):
        '''
        根据两个item的reponse 字符串找出所有的更改点

        :param pri_response_str:  原字符串
        :param model_response_str: 新字符串
        :return:
        '''

        pass




if __name__ =="__main__":
  extract = ExtractRules()
  print(extract.get_items())