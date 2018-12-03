#coding=utf-8

'''
数据匹配:该模块拿到对应的规则集合，然后进行原数据规则匹配.
'''

class DataMatch(object):

    def match(self,rules=[],items=[]):
        '''
        生成器的写法
        将原模型数据组织成items对象集合，然后每个item的responses和规则进行匹配，看看原数据是否有item需要修改
        :param rules: 提取的规则集合
        :param items: 原数据的item集合
        :return: 包装好的items集合
        '''
        yield items