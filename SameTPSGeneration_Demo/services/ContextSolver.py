#coding=utf-8

'''
context 选取的策略
'''

class ContextSolver(object):


    def between_changes_context(self,context_strs,change_points_nums):

        '''
        选取的规则是两个修改之间的内容，也就是该修改之前到上一个修改之后，该修改之后到下一个修改之前===》pass。。。pass。。。。pass
        :param context_str: 一个公共上下文的集合
        :param change_points_nums: 修改点有多少个
        :return: 返回和修改点个数对应的context的个数
        '''
        for index in range(change_points_nums):
            #为了对新的原型组数据更好的匹配，这里只是把修改的上下文做了一个数组合并
            context_strs[index] = (context_strs[index],context_strs[index+1])
        del context_strs[index+1]
        return context_strs
