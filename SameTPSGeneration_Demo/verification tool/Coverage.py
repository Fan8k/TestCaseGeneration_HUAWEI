#coding=utf-8
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.DataMatcher import DataMatcher
from services.ExtractRuler import ExtractRuler
from utils.ExtractLocationInfo import ExtractLocationInfo
from services.RuleDecorater import RuleDecorater
from services.RuleMerger import RuleMerger
from interactions.Predict import Predict



if __name__ =="__main__":
    path = "/home/inspur/li/SameTPSGeneration_Demo/datas/data/1/001_normalTest/com.xml"
    # tps下
    tps = ExtractLocationInfo.extract_location_and_type_info(r"/home/inspur/li/SameTPSGeneration_Demo/datas/data")
    # 某一个编码 比如编码1 下面的原型组 001_normalTest
    location = ['5', '2', '3', '4', '1']
    primary_rules = []
    for i in location:
    # 选择的目标编码
        aim_location = i
        proto_type, model_types = ExtractLocationInfo.filter_proto_type(tps[aim_location], '001_normalTest')
        extractRuler = ExtractRuler()
        # 整个编码下所有的规则
        encode_rules = extractRuler.get_encode_rules(aim_location, proto_type, model_types)
        primary_rules.extend(encode_rules)
        # 原始规则进行装饰和合并
        # 这里只是进行barcode 单词装饰
    rules = RuleDecorater.rule_word_decorater(r"\[barcode:", primary_rules)
    # 装饰之后需要进行按照上下文和from进行合并 提成更普通的规则
    common_rules = RuleMerger.mergeredBy_contextOrigin(rules)
    # print("规则")
    #     # for com in primary_rules:
    #     #     print(("from:%s\tTo:%s")%(com.original, com.to))
    #     # print("预测\n\n")

    print("通用规则")
    for com in common_rules:
        print(com)
    print("预测\n\n")

    predicter = Predict()
    count = 0
    for items in predicter.predict(path, common_rules):
        count += 1
        for item in items:
            print(item)
        print("\n\n")
    print(count)