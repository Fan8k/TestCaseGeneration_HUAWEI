#coding=utf-8
from os import path as op
from sys import path as sp
sp.append(op.dirname(op.dirname(op.abspath(__file__))))

from services.ExtractRuler import ExtractRuler
from utils.ExtractLocationInfo import ExtractLocationInfo
from services.RuleDecorater import RuleDecorater
from services.RuleMerger import RuleMerger
from services.RuleSorter import RuleSorter
from daos.WriteBack import WriteBack
from interactions.Predict import Predict
from daos.FindallFiletype import FindallFiletype
from daos.GetXML import GetXML
from daos.Insert import Insert
'''
主入口
'''

if __name__ == "__main__":
    path = "/home/inspur/li/SameTPSGeneration_Demo/datas/data/2/001_normalTest/uut_com.xml"
    #tps下
    findall_filetype = FindallFiletype()
    tps = findall_filetype.filetype_dic()
    #tps = ExtractLocationInfo.extract_location_and_type_info(r"/home/inspur/li/SameTPSGeneration_Demo/datas/data")
    #某一个编码 比如编码1 下面的原型组 001_normalTest
    location = ['1','2','3','4','5']
    primary_rules = []
    for i in location:
        # 选择的目标编码
        # if i == '1':
        #     continue
        aim_location = i
        proto_type, model_types = ExtractLocationInfo.filter_proto_type(tps[aim_location], '001_normalTest')
        extractRuler = ExtractRuler()
        # 整个编码下所有的规则
        encode_rules = extractRuler.get_encode_rules(aim_location, proto_type, model_types)
        primary_rules.extend(encode_rules)
        # 原始规则进行装饰和合并
        # 这里只是进行barcode 单词装饰
    rules = RuleDecorater.orinial_rule_decorater([(':', "["), ('\[', 'P')], primary_rules)
    #装饰之后需要进行按照上下文和from进行合并 提成更普通的规则
    common_rules = RuleMerger.mergeredBy_origin_igonreCase(rules,2)
    common_rules = RuleSorter.sort_by_scoreAndFrequence(common_rules)

    #存储

    print("通用规则")
    print(common_rules)
    for com in common_rules:
        print(com)

    print("预测\n\n")

    predicter = Predict()
    wb = WriteBack()
    # for items in predicter.predict(path, common_rules):
    #      #wb.newxml(items,path)
    #      for com in items:
    #          print(com)
    #      print("\n\n")
    aim = predicter.predict(path, common_rules)
    wb.newxml(aim,path)

    # proto_items = GetXML().read_file(path)
    # for com in proto_items:
    #     print(com)
    # print("\n\n")