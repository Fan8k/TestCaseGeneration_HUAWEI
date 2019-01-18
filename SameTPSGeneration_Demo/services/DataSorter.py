#coding = utf-8

'''
规则排序器：目的是按照某些指标(比如：规则的score和频次的关系得到一个结果)作为输出XML的顺序的标准
'''


class DataSorter(object):
    '''
    负责生成的item数据排序
    '''
    @classmethod
    def sort_by_scoreAndFrequence(cls, datas_dict):
        '''
        为数据进行排序
        :param datas_dict: {数据:[修改的位置，指标]}
        :return: 排序之后的数据
        '''
        datas_info=sorted(datas_dict.items(),key=lambda item: item[1][1],reverse=True)
        return datas_info

    @classmethod
    class BenchMarker:
        '''
        专门负责为生成的xml数据进行排序生成指标
        '''
        @classmethod
        def single(cls,rule):
            return cls._single_sore_and_Frequence_equal(rule.score,rule.frequence)

        @classmethod
        def all(cls,rules):
            total = 0
            for rule in rules:
                total+=cls._all_sore_and_Frequence_equal(rule.score,rule.frequence)
            return total/len(rules)

        @classmethod
        def scores(cls,scores):
            total = 0
            for score in scores:
                total+=score
            return total/len(scores)

        '''
        获取指标的工具类
        '''
        @classmethod
        def _single_sore_and_Frequence_equal(clf, score, frequence):
            '''
            该方法用于单点修改的得分计算方式
            按照score和frequence相等的影响力计算出结果
            :param score: 得分
            :param frequence: 频次
            :return: 0.5*score + 0.5*frequence
            '''
            return 0.5 * score + 0.5 * frequence

        @classmethod
        def _all_sore_and_Frequence_equal(clf, score, frequence):
            '''
            该方法用于整个item修改的得分计算方式
            按照score和frequence相等的影响力计算出结果
            :param score: 得分
            :param frequence: 频次
            :return: 0.5*score + 0.5*frequence
            '''
            return 0.5 * score + 0.5 * frequence