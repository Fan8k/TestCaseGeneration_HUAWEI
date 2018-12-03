#coding=UTF-8
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import TypeChecker as Tper

'''
Item对象:用来描述用例基本单元（命令及其回复信息）
'''


@Tper.AddTypeCheckerDecorator(_cmds=list,_responses=list,_score=int,_location_info=str,_num=int)
class Item(object):

    def __init__(self,cmds=[],responses=[],score=0,location_info=None,num=0):
        '''
        每个对象包含属性：
        1.cmds 所包含的所有命令
        2.responses 所包含的所有响应体
        3.score item的评分（后期作为规则的评分）
        4.location_info 这个item的位置信息
        5.该item在用例中的顺序号
        '''
        self._cmds = cmds
        self._responses = responses
        self._score = score
        self._location_info = location_info
        self._num = num

    @property
    def cmds(self):
        return self._cmds

    @cmds.setter
    def cmds(self,cmds):
        self._cmds = cmds

    @property
    def responses(self):
        return self._responses

    @responses.setter
    def responses(self, responses):
        self._responses = responses

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        self._score = score

    @property
    def location_info(self):
        return self._location_info

    @location_info.setter
    def location_info(self, location_info):
        self._location_info = location_info

    @property
    def num(self):
        return self._num

    @num.setter
    def num(self, num):
        self._num = num

    def __str__(self):
        return "item [cmds=%s,responses=%s,score=%s,location_info=%s,num=%s]"%(self.cmds,self.responses,self.score,self.location_info,self.num)
    

