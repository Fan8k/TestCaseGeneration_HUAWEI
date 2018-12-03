#coding=UTF-8

'''
类型检查器：负责所有对象属性的类型set检查
'''

class Typed(object):

    def __init__(self,key,type):
        '''
        :param key: 保存在instance中的变量名字
        :param type: 该变量期望的数据类型
        '''
        self.key = key
        self.type = type

    def __get__(self, instance, owner):
        return instance.__dict__[self.key]

    def __set__(self, instance, value):
        if isinstance(value, self.type) or value == None:
            instance.__dict__[self.key] = value
        else:
            raise AttributeError("%s的数据属性%s的值%s的类型不正确"%(instance,self.key,value))

    def __delete__(self, instance):
        del instance.__dict__[self.key]

'''
为类增加类型检查器
'''
def AddTypeCheckerDecorator(**kwargs):
    def add(obj):
        for k,v in kwargs.items():
            setattr(obj,k,Typed(k,v))
        return obj
    return add

