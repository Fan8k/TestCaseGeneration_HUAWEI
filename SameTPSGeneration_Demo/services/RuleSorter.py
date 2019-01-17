#coding=utf-8

'''
规则排序器：目的是按照某些指标(比如：规则的score和频次的关系得到一个结果)作为排序的标准
'''

class RuleSorter(object):

      @classmethod
      def sort_by_scoreAndFrequence(cls,commonRules):

          temp = []
          for common_rule in commonRules:
              indicate = RuleSorter._BenchMarker.sore_and_Frequence_equal(common_rule.score, common_rule.frequence)
              temp.append((common_rule,indicate))
          temp = sorted(temp,key= lambda _v:_v[1],reverse=True)
          _commonRules = [_temp[0] for _temp in temp ]
          return _commonRules

      @classmethod
      class _BenchMarker:

           '''
           获取指标的工具类
           '''

           @classmethod
           def sore_and_Frequence_equal(clf,score,frequence):
               '''
               该方法按照score和frequence相等的影响力计算出结果
               :param score: 得分
               :param frequence: 频次
               :return: 0.5*score + 0.5*frequence
               '''
               return 0.5*score+0.5*frequence
