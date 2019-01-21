#coding=utf-8
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.CommonRule import CommonRule
from models.RuleKind import RuleKind
'''
合并规则
'''

class RuleMerger:

     @classmethod
     def mergeredBy_contextOrigin(cls,rules):
         '''
         方法过时
         该方法是按照如果(上下文,from)都相同才算一个规则
         :param rules:
         :return:
         '''
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


     @classmethod
     def mergeredBy_origin_igonreCase(cls, rules,least_nums):
         '''
         该方法按照from(且大小写不敏感)合并，满足至少出现least_nums次才算合并成功
         :param rules: 需要合并的规则
         :param least_nums 匹配from相同至少出现的次数
         :return: 合并之后的规则
         '''
         temp_times = {}
         for rule in rules:
             #大小写不敏感
             if temp_times.get(rule.original.lower()) == None:
                 temp_times[rule.original.lower()] = 1
             else:
                 temp_times[rule.original.lower()] += 1

         _satisfied_mergeRules,_not_satisfied_mergeRules = RuleMerger._filter(temp_times,least_nums)
         temp = {}
         _rule_scores = {}
         #需要合并的名字
         for merge_name in _satisfied_mergeRules:
             for rule in rules:
                 _original = rule.original.lower()
                 #不在合并范围之内直接跳
                 if _original != merge_name:
                     continue
                 else:
                     #这边规则肯定是要merge
                     if _rule_scores.get(_original) == None:
                        _rule_scores[_original] = rule.score
                     else:
                        _rule_scores[_original] +=rule.score

                     if temp.get(_original) == None:
                         temp[_original] = {rule.to:1}
                     else:
                         if temp.get(_original).get(rule.to) == None:
                             # 没有就初始化
                             temp[_original][rule.to] = 1
                         else:
                             # 如果存在就加1
                             temp[_original][rule.to] += 1
         _rules = []
         for key, value in temp.items():
             # 按照to出现的次数排序（从大到小和从小到大都行）
             values = sorted(value.items(), key=lambda times: times[1])
             value = {}
             for item in values:
                 value[item[0]] = item[1]
             _rules.append(CommonRule(("",""),key,value,RuleKind.CONFIRM_AND_UNCONFIRM,_rule_scores[key]/temp_times[key],temp_times[key]/len(rules)))
         #处理没有进行合并的rule
         for rule in rules:
             if rule.original in _not_satisfied_mergeRules:
                 temp = RuleKind.REMINDER
                 if len(rule.context[0])==0 and len(rule.context[1])==0:
                       temp = RuleKind.CONFIRM_AND_UNCONFIRM
                 _rules.append(CommonRule(rule.context, rule.original,{rule.to: 1},temp,rule.score,1.0/len(rules)))
         return _rules

     @classmethod
     def _filter(cls,temp_items,least_nums):
         temp = []
         not_temp = []
         for key,value in temp_items.items():
             if value >= least_nums:
                 temp.append(key)
             else:
                 not_temp.append(key)
         return temp,not_temp




