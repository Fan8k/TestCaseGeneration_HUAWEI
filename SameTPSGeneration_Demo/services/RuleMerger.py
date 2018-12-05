#coding=utf-8
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.CommonRule import CommonRule
'''
合并规则
'''

class RuleMerger:

     @classmethod
     def mergeredBy_contextOrigin(cls,rules):
         temp = {}
         for rule in rules:
             #按照上下文和修改点找对应的上下文
             if temp.get((rule.context,rule.original)) == None:
                 temp[(rule.context, rule.original)] = {rule.to:1}
             else:
                 #如果不为空，只能说明有了to加进来了，但是需要判断to是否一样
                 if temp.get((rule.context, rule.original)).get(rule.to) == None:
                    #没有就初始化
                    temp[(rule.context, rule.original)][rule.to] = 1
                 else:
                    #如果存在就加1
                    temp[(rule.context, rule.original)][rule.to] +=1
         rules = []
         for key,value in temp.items():
             #按照to出现的次数排序（从大到小和从小到大都行）
             values = sorted(value.items(),key=lambda times:times[1])
             value = {}
             for item in values:
                 value[item[0]] = item[1]
             rules.append(CommonRule(key[0],key[1],value))

         return  rules
