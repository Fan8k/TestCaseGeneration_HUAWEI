#coding=utf-8
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import copy
import re

from daos.GetXML import GetXML
from preprocess.StrProcess import StrProcess
from models.RuleKind import RuleKind
from services.DataUpdater import DataUpdater
from services.DataSorter import DataSorter
from utils.MD5 import MD5
'''
数据匹配:该模块拿到对应的规则集合，然后进行原数据规则匹配.
'''

class DataMatcher(object):

    def __init__(self,new_proto_type_path):
        #这个就是需要预测生成的原型组路径
        self._proto_type = new_proto_type_path
        self._getXml = GetXML()
        self._sp = StrProcess()
        #存储所有预测生成是数据信息
        self._result = {}

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
        for index, item in enumerate(proto_items):
            # 先深度拷贝一份
            temp = copy.deepcopy(item)
            item_changed_flag = False
            #因为item全部修改完才返回，每次修改一个response，都有相应的score
            scores = []
            #因为现在一个item的一个response可能有多次全局修改，所以先保存所有信息
            _all_points_all_responses = []
            for response_index, _response in enumerate(item.responses):
                if _response == 'None':
                    continue
                # 做过预处理的response信息
                _commonRule_point = {}
                temp_response = self._sp.str_process(_response, 1)
                for _commonRule in rules:
                    # 所有修改点集合
                    _originals = [i for i in re.finditer(self._translate_original(_commonRule.original), _response,re.IGNORECASE)]
                    # 多加一个在处理过干扰项比如点的response中的修改点位置信息，这样匹配到底改不改用这些修改点集合信息，然后具体修改时用上面的点的信息
                    _preprocess_originals = [i for i in
                                             re.finditer(self._translate_original(_commonRule.original), temp_response,re.IGNORECASE)]
                    if len(_originals) > 0:
                        _commonRule_point[_commonRule] = (_originals,_preprocess_originals)
                #找到了该response能应用的所有的规则及其可修改的位置点
                #一个response单点匹配
                for _new_response,score in singlePointMatch.match(_response,temp_response,_commonRule_point):
                    if _new_response != None:
                        temp.responses[response_index] = _new_response
                        print("修改第%s个item的%s的response" % (temp.num, response_index))
                        pri_item = proto_items[index]
                        proto_items[index] = temp
                        self._result[tuple(proto_items)] = [temp.num,score]
                        proto_items[index] = pri_item
                #一个response多点匹配
                if temp.num == 4:
                    print(temp.num)
                _new_responses = []
                for _new_response, score in allPointsMatch.match(_response, temp_response, _commonRule_point):
                    if _new_response != None:
                        item_changed_flag = True
                        _new_responses.append([_new_response,score])
                if len(_new_responses)>0:
                   _all_points_all_responses.append([response_index,allPointsMatch.remove_samevalue(_new_responses)])

            #只要所有点匹配做了修改，就要考虑组合问题了，因为一个response修改可能对应很多[response0,response1,response2]
            if item_changed_flag:
               print("全部点修改%s"%temp.num)
               pri_item = proto_items[index]
               for _temp,score in self._assemble_item(item,_all_points_all_responses):
                   proto_items[index] = _temp
                   self._result[tuple(proto_items)] = [_temp.num, score]
                   print("修改第%s个item" % (_temp.num))
               proto_items[index] = pri_item
        return self._result

    def _assemble_item(self,item,_all_points_all_responses):
        '''
        组合所有的(response_index,[response1,response2])

        :param item:
        :param _all_points_all_responses:
        :return:
        '''
        results = []
        temp_results = []
        self._search_responses(_all_points_all_responses,results,temp_results,0,len(_all_points_all_responses))
        for result in results:
            _temp = copy.deepcopy(item)
            _scores = 0
            for _response_index,_response in result:
                _temp.responses[_response_index] = _response[0]
                _scores+= _response[1]
            yield (_temp,_temp.score+_scores)
        return None

    def _search_responses(self,_all_points_all_responses,results,temp_results,index,_len):
        if index == _len:
            results.append(temp_results.copy())
        else:
          _response_index,_responses = _all_points_all_responses[index]
          for _response in _responses:
              temp_results.insert(index,(_response_index,_response))
              self._search_responses(_all_points_all_responses,results,temp_results,index+1,_len)
              del temp_results[index]

    def _translate_original(self,original:str):
        '''
        因为匹配方式是先找修改点，然后从修改点左右来匹配context，从response中找修改点（但是修改点中有[,],(,)等元字符）就把他们当成了有意义的元字符了，而不是咱们想要的
        普通字符，所以需要把[替换成'\['才行，但是这又有一个问题就是引入了\,\
        :param original: ^ $ * + ? {} [] | () \ .  包含元字符
        :return: 把元字符前加上转义符号\，变成非转义字符\
        '''
        meta_words = ['[']
        for meta_word in meta_words:
            original = original.replace(meta_word,'\%s'%meta_word)
        return original

    def _match_item_deprecated(self,proto_items,rules=[]):
        '''
        该方法的思路先找response有无一个修改规则的修改点，如果看是否上下文满足，满足先统计起来，
        所有修改点都统计完毕之后，统一的进行修改，这个方法没有考虑到规则的context和新来的response的context不同的情况
        比如：规则中context没有点，但是新来的response信息都是有点的，所以他们之间如何来回切换很重要
        :param proto_items:
        :param rules:
        :return:
        '''
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
                                    #这个地方增加一个修复，就是修改的位置不能喝random_choice_to一致
                                    _change_to_value = _commonRule.random_choice_to()
                                    if _change_to_value == _response[start_index:stop_index]:
                                        _change_to_value = _commonRule.random_choice_to(repeat=True)
                                    _change_point_location.append((start_index, stop_index,_change_to_value))
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

    def _match_item_deprecated_(self, proto_items, rules=[]):
        '''
        过时了
        该方法的思路先找response有无一个修改规则的修改点，如果有是否上下文满足，满足先统计起来，
        所有修改点都统计完毕之后，统一的进行修改.重要修改点，规则context没有点，预测response有点，怎么匹配的问题
        :param proto_items:
        :param rules:
        :return:
        '''
        # 开始每个item的每个response进行匹配任务
        for index, item in enumerate(proto_items):
            # 默认没有修改过
            item_changed_flag = False
            # 先深度拷贝一份
            temp = copy.deepcopy(item)
            for response_index, _response in enumerate(temp.responses):
                # 应用规则 先找有无修改点，然后匹配上下文，最后随机选择一个to
                if _response == 'None':
                    continue
                _commonRule_point = {}
                _change_point_location = []
                # 默认没有response修改过
                response_changed_flag = False
                #做过预处理的response信息
                temp_response = self._sp.str_process(_response, 1)
                for _commonRule in rules:
                    # 所有修改点集合
                    _originals = [i for i in re.finditer(self._translate_original(_commonRule.original), _response)]
                    #多加一个在处理过干扰项比如点的response中的修改点位置信息，这样匹配到底改不改用这些修改点集合信息，然后具体修改时用上面的点的信息
                    _preprocess_originals = [i for i in re.finditer(self._translate_original(_commonRule.original), temp_response)]
                    if len(_originals) > 0:
                        _commonRule_point[_commonRule] = (_originals,_preprocess_originals)

                #判断修改点到底要不要改,是利用的是去掉干扰字符的新的response信息
                _response_len = len(temp_response)
                for _commonRule, _change_points in _commonRule_point.items():
                    #修改点的索引
                    for _change_point_index,_preprocess_original in enumerate(_change_points[1]):
                        start_index, stop_index = _preprocess_original.span()
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
                                if _commonRule.context[0] == temp_response[start_index - b_context_len:start_index] and \
                                        _commonRule.context[1] == temp_response[stop_index:stop_index + a_context_len]:
                                    # 不能立马就改，因为后来的修改也是按照之前的模式匹配找到的位置，一改位置就乱了，只能先记住那些点要改
                                    _real_start_index,_real_stop_index = _change_points[0][_change_point_index].span()
                                    _change_point_location.append(
                                        (_real_start_index,_real_stop_index, _commonRule.random_choice_to()))
                                    if response_changed_flag == False:
                                        response_changed_flag = True
                                        item_changed_flag = True
                #这是整个response修改完毕才替换
                if response_changed_flag:
                    _change_point_location = sorted(_change_point_location, key=lambda a: a[0])
                    _response = self._change_strValue(_response, _change_point_location)
                    temp.responses[response_index] = _response
                    print("修改第%s个item的%s的response" % (temp.num, response_index))
            #整个item都修改完毕，才进行item替换
            if item_changed_flag:
                pri_item = proto_items[index]
                proto_items[index] = temp
                yield proto_items
                proto_items[index] = pri_item
        # 结束标记 不管有没有数据了
        return None

    def _change_strValue(self,pri_str,change_points_location):

        '''
        过时了
        修改相应的满足条件的位置的信息
        :param pri_str: 原型组的item的response信息
        :param change_points_location: 修改点的位置
        :return:
        '''
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

#单点匹配
class singlePointMatch:

    @classmethod
    def match(cls, response, preprocess_response, _commonRule_point):

        '''
        item的response 全体规则和修改点都修改完毕返回
        :param response: 原型组中对应的response
        :param preprocess_response:已处理的字符串
        :param _commonRule_point:{rule:(_originals,_preprocess_originals)}
        :return: (_new_response,score) 返回的是单点匹配修改之后的response和单个规则通过数据排序规则计算出来的得分
        '''

        # 判断修改点到底要不要改,是利用的是去掉干扰字符的新的response信息
        for _commonRule, _change_points in _commonRule_point.items():
            # 修改点的索引
            for _change_point_index, _preprocess_original in enumerate(_change_points[1]):
                _canUpdate_flag = False
                # 上下文都为空的这种,直接改
                if _commonRule.kind == RuleKind.CONFIRM_AND_UNCONFIRM:
                    # 修改为新的response
                    _canUpdate_flag = True
                else:
                    # 带有明确上下文的规则
                    start_index, stop_index = _preprocess_original.span()
                    # 前上下文长度
                    b_context_len = len(_commonRule.context[0])
                    # 不符合无需匹配
                    if b_context_len > start_index:
                        continue
                    else:
                        a_context_len = len(_commonRule.context[1])
                        # 后面的上下文都不够长，说明肯定不匹配
                        if a_context_len > ((len(preprocess_response) + 1) - stop_index):
                            continue
                        else:
                            if _commonRule.context[0] == preprocess_response[
                                                         start_index - b_context_len:start_index] and \
                                    _commonRule.context[1] == preprocess_response[
                                                              stop_index:stop_index + a_context_len]:
                                # 不能立马就改，因为后来的修改也是按照之前的模式匹配找到的位置，一改位置就乱了，只能先记住那些点要改
                                _canUpdate_flag = True
                # 只有能修改时，才进行修改和返回，要不然直接忽略这个点
                if _canUpdate_flag:
                    _real_start_index, _real_stop_index = _change_points[0][_change_point_index].span()
                    _new_response = DataUpdater.change_strValue(response, [
                        (_real_start_index, _real_stop_index, _commonRule.random_choice_to())])
                    # 这一次修改的得分，由数据排序模块单独决定
                    score = DataSorter.BenchMarker.single(_commonRule)
                    yield (_new_response, score)
        return None


#整个item匹配
class allPointsMatch():

    @classmethod
    def match(cls, response, preprocess_response, _commonRule_point):
        '''
        item的response只要一个点匹配到就替换并返回
        :param response: 原型组中对应的response
        :param preprocess_response:已处理的字符串
        :param _commonRule_point:{rule:(_originals,_preprocess_originals)}
        :return: (_new_response,score) 返回的是单点匹配修改之后的response和单个规则通过数据排序规则计算出来的得分
        '''
        # 存储一个response 所有修改的点
        _change_point_location = []
        # 判断修改点到底要不要改,是利用的是去掉干扰字符的新的response信息
        for _commonRule, _change_points in _commonRule_point.items():
            # 修改点的索引
            for _change_point_index, _preprocess_original in enumerate(_change_points[1]):
                _canUpdate_flag = False
                # 上下文都为空的这种,直接改
                if _commonRule.kind == RuleKind.CONFIRM_AND_UNCONFIRM:
                    # 修改为新的response
                    _canUpdate_flag = True
                else:
                    # 带有明确上下文的规则
                    start_index, stop_index = _preprocess_original.span()
                    # 前上下文长度
                    b_context_len = len(_commonRule.context[0])
                    # 不符合无需匹配
                    if b_context_len > start_index:
                        continue
                    else:
                        a_context_len = len(_commonRule.context[1])
                        # 后面的上下文都不够长，说明肯定不匹配
                        if a_context_len > ((len(preprocess_response) + 1) - stop_index):
                            continue
                        else:
                            if _commonRule.context[0] == preprocess_response[
                                                         start_index - b_context_len:start_index] and \
                                    _commonRule.context[1] == preprocess_response[
                                                              stop_index:stop_index + a_context_len]:
                                # 不能立马就改，因为后来的修改也是按照之前的模式匹配找到的位置，一改位置就乱了，只能先记住那些点要改
                                _canUpdate_flag = True
                # 只有能修改时，才进行修改和返回，要不然直接忽略这个点
                if _canUpdate_flag:
                    _real_start_index, _real_stop_index = _change_points[0][_change_point_index].span()
                    _change_point_location.append(
                        (_real_start_index, _real_stop_index, _commonRule.random_choice_to(),_commonRule))
        if len(_change_point_location) != 0:
            _change_point_location = sorted(_change_point_location, key=lambda a: a[0])
            for _new_response,rules in  DataUpdater.change_strValues(response, _change_point_location):
                 score = DataSorter.BenchMarker.all(rules)
                 yield (_new_response,score)
        return None

    @classmethod
    def remove_samevalue(cls,_new_responses):
        '''
        因为同一个response可能不同点组合在一起修改的结果一样，这里只要一个作为结果
        :param _new_responses: [[response,score],[response,score]]
        :return: 不重复的[[response,score],[response,score]]
        '''
        _temp = []
        index = 0
        m = MD5()
        responses = []
        for _new_response,score in _new_responses:
            _new = _new_response.replace(r"\r","").replace(r"\n","").replace(".","").replace(" ","")
            _md_str = m.encode(_new)
            if _md_str not in _temp:
                _temp.append(_md_str)
                responses.append([_new_response,score])
            index+=1
        return responses



if __name__ =="__main__":
   s =r"Fail\\(1)\\UUT_SWT(1)\\Post(1)Fail[00:00:00000]cpu_ddrramFail[Fail]cpu_norflash"
   a=r"Fail\\(1)\\UUT_SWT(1)\\Post(1)Fail[00:00:00000]cpu_ddrramfail[Fail]cpu_norflash"
   s = s.replace(r"\r", "").replace(r"\n", "").replace(".", "").replace(" ", "")
   a = a.replace(r"\r", "").replace(r"\n", "").replace(".", "").replace(" ", "")
   print(s)
   print(a)
   m = MD5()
   print(m.encode(s))
   print(m.encode(a))
