#coding=utf-8

'''
规则匹配器：专门用于数据context（上下文）匹配
'''

class RuleMatcher:

    @classmethod
    def shortestEditDistance(cls,primary_context,current_context,level):
        '''
        最短可编辑距离
        :return:
        '''
        p_len = len(primary_context)
        c_len = len(current_context)

        edit = [[0 for i in range(p_len+1)] for i in range(c_len+1)]

        edit[0][:] = [i for i in range(p_len+1)]

        for i in range(c_len+1):
            edit[i][0] = i

        for i in range(1,c_len+1):
            for j in range(1,p_len+1):
                if primary_context[j-1] == current_context[i-1]:
                    _temp = edit[i-1][j-1]
                else:
                    _temp = edit[i-1][j-1]+1
                edit[i][j] = min(edit[i][j-1]+1,edit[i-1][j]+1,_temp)

        if edit[c_len][p_len]> level:
           _flag = False
        else:
           _flag = True

        return _flag
