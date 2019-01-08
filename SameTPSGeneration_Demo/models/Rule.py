#coding=utf-8
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import TypeChecker as Tper

'''
提取的规则
'''
@Tper.AddTypeCheckerDecorator(_context=tuple,_original=str,_to=str,_location=str,_file_name=str,_score=int)
class Rule(object):

    def __init__(self,context=None,original=None,to=None,location=None,file_name=None,score=0):
        '''
        :param contexts: 一个规则的上下文 <前文，后文>
        :param original: 原始的字符
        :param to: 原始字符串改成了什么字符串
        :param location 表示该规则来自哪个tps下哪个编码
        '''
        self._context = context
        self._original = original
        self._to = to
        self._location = location
        self._file_name = file_name
        self._score = score

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
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        self._location = location

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, file_name):
        self._file_name = file_name

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        self._score = score

    def __str__(self):
        return "rule [context=%s,original=%s,to=%s,location=%s,score=%s]" % (
         self._context, self._original, self._to,self._location,self._score)

