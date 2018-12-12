#coding=utf-8
import os
import sys
import difflib
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.Rule import Rule
'''
规则处理器：组装context和《原数据点，修改点》成为特定规则的rule
这个模块负责接收ContextSolver发送过来的context集合，已经ExtractRules传递过来的修改点
'''

class RulesSolver:


    def pack_rules(self,change_contexts,change_points,rule_location_info,file_name):
       '''
       将context和rule分装到rules对象中
       :param change_contexts:[('一个前context','后context')]
       :param change_points:
       :return: rules规则
       '''
       rules = []
       for index,change_context in enumerate(change_contexts):
           rules.append(Rule(change_context,change_points[index][0],change_points[index][1],rule_location_info,file_name))
       return rules