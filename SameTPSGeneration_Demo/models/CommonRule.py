#coding=utf-8
import os
import sys
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import TypeChecker as Tper
import random
'''
从Rule中提取的更普通的规则context,from都一致to按照频率汇集
'''

@Tper.AddTypeCheckerDecorator(_context=tuple,_original=str,_to=dict,_kind=str,_score=float,_frequence=float)
class CommonRule(object):

    def __init__(self,context=None,original=None,to=None,_kind=None,score=0.0,frequence=0.0):
        '''
        :param contexts: 一个规则的上下文 <前文，后文>
        :param original: 原始的字符
        :param to: {to1:4,to2:3,to3:2} 按照context和from混合之后的to就会得出相应to的频率
        :param location 表示该规则来自哪个tps下哪个编码
        '''
        self._context = context
        self._original = original
        self._to = to
        self._random_choiced = []
        self._kind = _kind
        self._score = score
        self._frequence = frequence

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self,context):
        self._context = context

    @property
    def original(self):
        return self._original

    @original.setter
    def original(self, original):
        self._original = original

    @property
    def to(self):
        return self._to

    @to.setter
    def to(self, to):
        self._to = to

    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, kind):
        self._kind = kind

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        self._score = score

    @property
    def frequence(self):
        return self._frequence

    @frequence.setter
    def frequence(self, frequence):
        self._frequence = frequence

    def random_choice_to(self,repeat=False):
        if repeat==False:
            num_list=[]
            last = 0
            current = 0
            for value in self._to.values():
                current+=value
                num_list.append([last,current])
                last = current
            #权重空间
            num_list = np.array(num_list)/current
            num_list = num_list.tolist()
            random_value = random.uniform(0,1)
            high = len(num_list)
            low = 0
            while(True):
                middle = (low+high)//2
                if num_list[middle][0]<= random_value and num_list[middle][1] > random_value:
                    break
                elif random_value < num_list[middle][0]:
                    high = middle
                elif random_value > num_list[middle][1]:
                    low = middle
            self._random_choiced.append(middle)
        else:
            last_index = self._random_choiced[0]
            middle = last_index + 1 if last_index!=(len(self._to.keys())-2) else last_index-1
            self._random_choiced = []
        return list(self._to.keys())[middle]

    def __str__(self):
        return "rule [context=%s,original=%s,to=%s,_kind=%s,socre=%s,frequence=%s]" % (
         self._context, self._original, self._to,self._kind,self._score,self._frequence)

