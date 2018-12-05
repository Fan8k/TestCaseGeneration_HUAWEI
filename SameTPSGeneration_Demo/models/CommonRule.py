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

@Tper.AddTypeCheckerDecorator(_context=tuple,_original=str,_to=dict)
class CommonRule(object):

    def __init__(self,context=None,original=None,to=None):
        '''
        :param contexts: 一个规则的上下文 <前文，后文>
        :param original: 原始的字符
        :param to: {to1:4,to2:3,to3:2} 按照context和from混合之后的to就会得出相应to的频率
        :param location 表示该规则来自哪个tps下哪个编码
        '''
        self._context = context
        self._original = original
        self._to = to


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

    def random_choice_to(self):
        num_list=[]
        last = 0
        current = 0
        for value in self._to.values():
            current+=value
            num_list.append([last,current])
            last = value
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
        return list(self._to.keys())[middle]

    def __str__(self):
        return "rule [context=%s,original=%s,to=%s]" % (
         self._context, self._original, self._to)
