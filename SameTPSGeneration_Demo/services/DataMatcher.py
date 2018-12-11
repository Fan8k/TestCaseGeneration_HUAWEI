#coding=utf-8
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import copy
import re

from daos.GetXML import GetXML
'''
数据匹配:该模块拿到对应的规则集合，然后进行原数据规则匹配.
'''

class DataMatcher(object):

    def __init__(self,new_proto_type_path):
        #这个就是需要预测生成的原型组路径
        self._proto_type = new_proto_type_path
        self._getXml = GetXML()

    def match(self,rules=[]):
        '''
        生成器的写法
        将原模型数据组织成items对象集合，然后每个item的responses和规则进行匹配，看看原数据是否有item需要修改
        1.改动一个位置就立马生成xml
        2.改动整个response就立马返回
        3.改动整个item的所有response就返回
        
        先按照3来做 改动一整个item就返回
        :param rules: 提取的CommonRule规则（经过抽象的规则）集合
        :param items: 原数据的item集合
        :return: 包装好的items集合
        '''
        # 需要预测的原型组数据items
        proto_items = self._getXml.read_file(self._proto_type)
        yield from self._match_item(proto_items,rules)

    def _translate_original(self,original:str):
        '''
        因为匹配方式是先找修改点，然后从修改点左右来匹配context，从response中找修改点（但是修改点中有[,],(,)等元字符）就把他们当成了有意义的元字符了，而不是咱们想要的
        普通字符，所以需要把[替换成'\['才行，但是这又有一个问题就是引入了\,\
        :param original: ^ $ * + ? {} [] | () \ .  包含元字符
        :return: 把元字符前加上转义符号\，变成非转义字符\
        '''
        meta_words = ['\\',']','{','}','^','$','*','+','?','(',')','.','[']
        for meta_word in meta_words:
            original = original.replace(meta_word,'\%s'%meta_word)
        return original

    def _match_item(self,proto_items,rules=[]):
        # 开始每个item的每个response进行匹配任务
        for index, item in enumerate(proto_items):
            #默认没有修改过
            item_changed_flag = False
            # 先深度拷贝一份
            temp = copy.deepcopy(item)
            for response_index, _response in enumerate(temp.responses):
                # 应用规则 先找有无修改点，然后匹配上下文，最后随机选择一个to
                if _response=='None':
                    continue
                _commonRule_point={}
                _change_point_location = []
                # 默认没有response修改过
                response_changed_flag = False
                for _commonRule in rules:
                    # 所有修改点集合
                    _originals = [i for i in re.finditer(self._translate_original(_commonRule.original), _response)]
                    if len(_originals)>0:
                      _commonRule_point[_commonRule] = _originals
                _response_len = len(_response)
                for _commonRule,_originals in _commonRule_point.items():
                    for _original in _originals:
                        start_index, stop_index = _original.span()
                        # 前上下文长度
                        b_context_len = len(_commonRule.context[0])
                        # 不符合无需匹配
                        if b_context_len > start_index:
                            continue
                        else:
                            a_context_len = len(_commonRule.context[1])
                            # 后面的上下文都不够长，说明肯定不匹配
                            if a_context_len > ((_response_len + 1) - stop_index):
                                continue
                            else:
                                if _commonRule.context[0] == _response[start_index - b_context_len:start_index] and \
                                        _commonRule.context[1] == _response[stop_index:stop_index + a_context_len]:
                                    #不能立马就改，因为后来的修改也是按照之前的模式匹配找到的位置，一改位置就乱了，只能先记住那些点要改
                                    _change_point_location.append((start_index, stop_index,_commonRule.random_choice_to()))
                                    if response_changed_flag ==False:
                                        response_changed_flag = True
                                        item_changed_flag = True
                if response_changed_flag:
                   _change_point_location = sorted(_change_point_location,key=lambda a:a[0])
                   _response = self._change_strValue(_response,_change_point_location)
                   temp.responses[response_index] = _response
                   print("修改第%s个item的%s的response"%(temp.num,response_index))
            if item_changed_flag:
               pri_item = proto_items[index]
               proto_items[index] = temp
               yield proto_items
               proto_items[index] = pri_item
        #结束标记 不管有没有数据了
        return None

    def _change_strValue(self,pri_str,change_points_location):
        temp = []
        for index,char in enumerate(pri_str):
               #前提是有需要修改的点进来才行
               if len(change_points_location)>0:
                 if change_points_location[0][0] <= index and index < change_points_location[0][1]:
                   if index == change_points_location[0][0]:
                     temp.extend(change_points_location[0][2])
                   if index+1 == change_points_location[0][1]:
                     del change_points_location[0]
                 else:
                     temp.append(pri_str[index])
               else:
                  temp.append(pri_str[index])
        return "".join(temp)



if __name__ =="__main__":
    path = "/home/inspur/li/SameTPSGeneration_Demo/datas/data/1/001_normalTest/"
    #proto_items = GetXML.read_file("",path)
    #print(len(proto_items))
    l = re.finditer(r"shabi","\\rOK\\r\\r\\r\\rpass\\(1)\\UUT_SWT(1)\\Qbarcode(1).........................pass [00:00:00.000]\\r\\r  qbarcodePass [barcode:023DUA0147258")
    for i in l:
        print(i)
    response= "fdfdaifd"
    change_points_location = [(2,4,'wo'),(4,8,'ni')]
    da = DataMatcher("fd")
    print(da._change_strValue(response,change_points_location))
    print([i for i in re.finditer("Pass\[pass","fdafdfPass[pass]pass")])
    print(da._translate_original("[fadfdsaf]fdaf(fda)fdfsaf{fdafds}fdasf\fdsafdsa.\\"))
    print('Pass\[pass')