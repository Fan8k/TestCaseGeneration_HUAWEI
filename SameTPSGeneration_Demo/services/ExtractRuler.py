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
from preprocess.StrProcess import StrProcess

'''
从items中提取规则
'''

class ExtractRuler:

    st = SelectObject()
    md5 = MD5()
    differ = difflib.Differ()
    cs = ContextSolver()
    rs = RulesSolver()
    sp = StrProcess()
    def __init__(self):
        self.location = '-1'
        self.type = '-1'

    def _get_items(self,location,type):
        '''
        :param location: 测试数据中的编码
        :param type: 模型组和原型组数据所在文件夹的名字
        :return: 从数据库中获取到的item对象
        '''
        self.location = location
        self.type = type
        return ExtractRuler.st.selected_object(location,type)

    def _get_rules(self,proto_items,model_items):
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
            model_item = model_items[index]
            for response_index in range(len(pri_item.responses)):
                #对应的item对象的response字符串
                pri_response_str = ExtractRuler.md5.encode(pri_item.responses[response_index])
                model_response_str = ExtractRuler.md5.encode(model_item.responses[response_index])
                if pri_response_str != model_response_str:
                     #找出修改点及其在原来字符串中的位置信息
                     results = self._find_change_points(ExtractRuler.sp.str_process(pri_item.responses[response_index],1),ExtractRuler.sp.str_process(model_item.responses[response_index],1))
                     _contexts = ExtractRuler.cs.between_changes_context(results[0],len(results[1]))
                     rules.extend(ExtractRuler.rs.pack_rules(_contexts,results[1],self.location,self.type,model_item.score))
        return rules

    def _find_change_points(self,pri_response_str,model_response_str):
        '''
        根据两个item的reponse 字符串找出所有的更改点
        :param pri_response_str:  原字符串 update service loopmode 1\\r||update pass ratio 2
        :param model_response_str: 新字符串 update service fail 1\\r||update pass ratio 2
        :return:（[common context，common context，common context],[<from:to>,<from,to>]）
        '''

        results = ExtractRuler.differ.compare(pri_response_str,model_response_str)
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

    def get_File_rules(self,location,pri_type,model_type):
        '''
        输入TPS下的某一个编码的原型组和某一个模型组提取规则(这仅仅是两个文件中提取的规则)
        :param location: 某一个编码的标识符（文件名字）
        :param pri_type: 原型组的标识符（文件名字）
        :param model_type:模型组的标识符（文件名字）
        :return:两个文件差异规则
        '''
        proto_items = self._get_items(location,pri_type)
        model_items = self._get_items(location,model_type)
        return self._get_rules(proto_items,model_items)

    def get_encode_rules(self,location,pri_type,model_types):
        rules = []
        '''
        输入TPS下的某一个编码的原型组和某一个模型组提取规则(这仅仅是两个文件中提取的规则)
        :param location: 某一个编码的标识符（文件名字）
        :param pri_type: 原型组的标识符（文件名字）默认一个编码下就一个原型组文件
        :param model_types:模型组的标识符（文件名字）的集合 ['002_check', '006_check']
        :return:整个编码下所有的规则
        '''
        for model_type in model_types:
            rules.extend(self.get_File_rules(location,pri_type,model_type))
        return rules

if __name__ =="__main__":
    ex = ExtractRuler()
    results=ex._find_change_points("\\r\\nOK\\r\\r\\n\\r\\r\\n  \\(1)\\UUT_SWT(1)\\Version(1)..........................Pass [00:00:00.000]\\r\\r\\n  Version.............................................Pass [713]\\r\\r\\n  \\(1)\\UUT_SWT(1)\\Version(*)..........................Pass [00:00:00.000]\\r\\r\\n\\UUT_SWT> ",
                                   r"\\r\\nOK\\r\\r\\n\\r\\r\\n  \\(1)\\UUT_SWT(1)\\Version(1)..........................Fail[00:00:00.000]\\r\\r\\n  Version.............................................Pass [714]\\r\\r\\n  \\(1)\\UUT_SWT(1)\\Version(*)..........................Fail[00:00:00.000]\\r\\r\\n\\UUT_SWT> ")
    print(results[0])
    print(results[1])