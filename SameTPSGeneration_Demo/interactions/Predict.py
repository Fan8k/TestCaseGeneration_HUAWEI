#coding=utf-8
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(sys.path)
from services.DataMatcher import DataMatcher
from services.ExtractRuler import ExtractRuler
from utils.ExtractLocationInfo import ExtractLocationInfo
from services.RuleDecorater import RuleDecorater
from services.RuleMerger import RuleMerger
from services.RuleSorter import RuleSorter
from daos.GetXML import GetXML
from daos.WriteBack import WriteBack
from services.DataSorter import DataSorter

'''
输入原型组数据预测生成相应的模型组数据
'''

class Predict:

    def predict(self,path,rules):
        '''
        输入想要预测的原型组文件的绝对路径，所用到的规则
        :param path: 原型组文件的绝对路径
        :param rules: 所用到的规则
        :return 所有已经按照指标从高到底排好序的数据
        '''
        dataMatch = DataMatcher(path)
        data_info_dict = dataMatch.match(rules)
        data_info_list=DataSorter.sort_by_scoreAndFrequence(data_info_dict)
        return data_info_list

    def test(self,proto_items,rules):
        dataMatch = DataMatcher("")
        yield from dataMatch._match_item(proto_items,rules)


if __name__ == "__main__":
    path = "/home/inspur/li/SameTPSGeneration_Demo/datas/data/1/001_normalTest/com.xml"
    #tps下
    tps = ExtractLocationInfo.extract_location_and_type_info(r"/home/inspur/li/SameTPSGeneration_Demo/datas/data")
    #某一个编码 比如编码1 下面的原型组 001_normalTest
    location = ['1','2','3','4','5']
    #选择的目标编码
    aim_location = location[0]
    proto_type, model_types=ExtractLocationInfo.filter_proto_type(tps[aim_location],'001_normalTest')
    extractRuler = ExtractRuler()
    #整个编码下所有的规则
    encode_rules = extractRuler.get_encode_rules(aim_location,proto_type,model_types)
    print(type(encode_rules))
    #原始规则进行装饰和合并
    #这里只是进行barcode 单词装饰
    #rules = RuleDecorater.rule_word_decorater(r"\[barcode:", encode_rules)
    rules = RuleDecorater.orinial_rule_decorater([(':', "["), ('\[', 'P')], encode_rules)
    #装饰之后需要进行按照上下文和from进行合并 提成更普通的规则
    common_rules = RuleMerger.mergeredBy_contextOrigin(rules)
    common_rules = RuleSorter.sort_by_scoreAndFrequence(common_rules)
    print("通用规则")
    print(common_rules)
    for com in common_rules:
        print(com)

    print("预测\n\n")

    predicter = Predict()
    wb = WriteBack()
    for items in predicter.predict(path, common_rules):
         wb.newxml(items,path)
     #count = 0
    # for items in predicter.predict(path,common_rules):
    #     count+=1
    #     for item in items:
    #         print(item)
    #     print("\n\n")
    # print(count)
    #
    # print("\n\n")
    # get_xml = GetXML()
    # items = get_xml.read_file(path)
    # for item in items:
    #     print(item)