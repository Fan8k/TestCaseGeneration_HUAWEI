#coding=utf-8
import os
import sys
import difflib
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from daos.SelectObject import SelectObject
from utils.MD5 import MD5
from models.Rule import Rule
from services.ContextSolver import ContextSolver
from services.RulesSolver import RulesSolver

'''
从items中提取规则
'''

class ExtractRules:

    st = SelectObject()
    md5 = MD5()
    differ = difflib.Differ()
    cs = ContextSolver()
    rs = RulesSolver()

    def get_items(self,location,type):
        '''
        :param location: 测试数据中的编码
        :param type: 模型组和原型组数据所在文件夹的名字
        :return: 从数据库中获取到的item对象
        '''
        self.location = location
        return ExtractRules.st.selected_object(location,type)


    def get_rules(self,proto_items,model_items):
        rules = []
        '''
        原型组和模型组提取的item正常情况下等大小，而且是一对一的关系
        :param proto_items: 获取到的原型组item对象的集合
        :param model_items: 获取到的模型组item对象的集合
        :return: <context,from,to,location>
        '''
        #获取修改过的item对象
        for index in range(len(proto_items)):
            pri_item = proto_items[index]
            model_item = proto_items[index]
            for response_index in range(len(pri_item.responses)):
                #对应的item对象的response字符串
                pri_response_str = ExtractRules.md5.encode(pri_item.responses[response_index])
                model_response_str = ExtractRules.md5.encode(model_item.responses[response_index])
                if pri_response_str != model_response_str:
                     #找出修改点及其在原来字符串中的位置信息
                     results = self.find_change_points(pri_response_str,model_response_str)
                     results[0] = ExtractRules.cs.between_changes_context(results[0],len(results[1]))
                     rules.extend(ExtractRules.rs.pack_rules(results[0],results[1],self.location))

        return rules

    def find_change_points(self,pri_response_str,model_response_str):
        '''
        根据两个item的reponse 字符串找出所有的更改点
        :param pri_response_str:  原字符串 update service loopmode 1\\r||update pass ratio 2
        :param model_response_str: 新字符串 update service fail 1\\r||update pass ratio 2
        :return:（[<from:to>,<from,to>],[common context，common context，common context]）
        '''

        results = ExtractRules.differ.compare(pri_response_str,model_response_str)
        '''
          '- '	line unique to sequence 1
          '+ '	line unique to sequence 2
          '  '	line common to both sequences
          '? '	line not present in either input sequence
          公共context建立方法：
          修改点建立方法：（从碰到第一个不同处开始，到最后一个不同点）
        '''
        change_contexts=[]
        changes_origin_to = []
        temp_change_context = ""
        temp_origin_str = ""
        temp_to_str = ""
        '''
        这个状态变量会提示当前字符处于修改期还是共同期
        '''
        results = list(results)
        total = len(results)
        common_staus = True
        for index,label in enumerate(results):
            #共同期
            if common_staus==True and label.startswith(" "):
                temp_change_context+=label[2:3]
            #只要碰到修改点就要切换状态，保留之前的共有上下文信息,重新下一轮
            if label.startswith("-") or label.startswith("+"):
               common_staus = False
               if len(temp_change_context)>0:
                  change_contexts.append(temp_change_context)
                  temp_change_context = ""

            #进入修改期
            if common_staus == False:
               if label.startswith("-"):
                   temp_origin_str+=label[2:3]
               if label.startswith("+"):
                   temp_to_str+=label[2:3]
               if label.startswith(" "):
                   temp_origin_str += label[2:3]
                   temp_to_str += label[2:3]

            #修改期状态监测:默认规则是探测下两个是否都是共有的，如果是共有就切换成共有期
            if common_staus == False:
                if index+2 < total:
                    if results[index+1].startswith(" ") and results[index+2].startswith(" "):
                        common_staus = True
                elif index+2 == total :
                    #倒数两个的话，看看最后一个是否需要切换
                    if results[index+1].startswith(" "):
                        common_staus = True
                if common_staus == True:
                    changes_origin_to.append((temp_origin_str, temp_to_str))
                    temp_to_str = ""
                    temp_origin_str = ""
            #结束操作
            if index+1 == total:
                if common_staus == True:
                    change_contexts.append(temp_change_context)
                if common_staus == False:
                    changes_origin_to.append((temp_origin_str,temp_to_str))

        return (change_contexts,changes_origin_to)




if __name__ =="__main__":
    pass   #location _type = {}
   # ex = ExtractRules()
   # results=ex.find_change_points("update servicelaomme 3\\r||updte pass ratio 2","update servicelaomme 3\\r||updte fail ratio 2")
   # print(results[0],results[1])