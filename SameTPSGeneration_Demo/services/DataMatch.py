#coding=utf-8
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from daos.GetXML import GetXML
'''
数据匹配:该模块拿到对应的规则集合，然后进行原数据规则匹配.
'''

class DataMatch(object):

    def __init__(self,new_proto_type_path):
        #这个就是需要预测生成的原型组路径
        self._proto_type = new_proto_type_path

    def match(self,rules=[]):
        proto_items = GetXML.read_file(self._proto_type)  # 相应的原型组数据items
        '''
        生成器的写法
        将原模型数据组织成items对象集合，然后每个item的responses和规则进行匹配，看看原数据是否有item需要修改
        1.改动一个位置就立马生成xml
        2.改动整个response就立马返回
        3.改动整个item的所有response就返回
        
        先按照2来做 改动一整个response就返回
        :param rules: 提取的规则集合
        :param items: 原数据的item集合
        :return: 包装好的items集合
        '''
        yield


