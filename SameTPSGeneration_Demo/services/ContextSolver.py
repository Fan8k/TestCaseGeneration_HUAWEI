#coding=utf-8

'''
context 选取的策略
'''

class ContextSolver(object):


    def between_changes_context(self,context_str,change_points_coordinates):

        '''
        选取的规则是两个修改之间的内容，也就是该修改之前到上一个修改之后，该修改之后到下一个修改之前===》pass。。。pass。。。。pass
        :param context_str: 一个item字符串
        :param change_points_coordinates: 所有修改点的位置坐标集合[<1,3>,<7,9>] 等
        :return: 提取的规则rule对象的集合
        '''
        pass
