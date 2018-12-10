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

import xlwt
from datetime import datetime


# wb = xlwt.Workbook()
# ws = wb.add_sheet('1_code')
# ws.write(2, 0, 1)
# ws.write(2, 1, 1)
# ws.write(2, 2, xlwt.Formula("A3+B3"))
# wb.save('example.xls')

if __name__ == "__main__":
    path = "/home/inspur/li/SameTPSGeneration_Demo/datas/data/2/001_normalTest/uut_com.xml"
    #tps下
    tps = ExtractLocationInfo.extract_location_and_type_info(r"/home/inspur/li/SameTPSGeneration_Demo/datas/data")
    #某一个编码 比如编码1 下面的原型组 001_normalTest
    location = ['1','2','3','4','5']
    #excel 配置
    wb = xlwt.Workbook()
    #选择的目标编码
    for i in location:
        ws = wb.add_sheet('%s_code'%(i))
        aim_location = i
        proto_type, model_types=ExtractLocationInfo.filter_proto_type(tps[aim_location],'001_normalTest')
        extractRuler = ExtractRuler()
        #整个编码下所有的规则
        encode_rules = extractRuler.get_encode_rules(aim_location,proto_type,model_types)
        for index,rule in enumerate(encode_rules):
            ws.write(index,0,rule.context[0])
            ws.write(index, 1, rule.context[1])
            ws.write(index, 2, rule.original)
            ws.write(index, 3, rule.to)

    ws = wb.add_sheet('all_code')
    bias = 0
    for i in location:
        aim_location = i
        proto_type, model_types=ExtractLocationInfo.filter_proto_type(tps[aim_location],'001_normalTest')
        extractRuler = ExtractRuler()
        #整个编码下所有的规则
        encode_rules = extractRuler.get_encode_rules(aim_location,proto_type,model_types)
        for index,rule in enumerate(encode_rules):
            ws.write(bias,0,rule.context[0])
            ws.write(bias, 1, rule.context[1])
            ws.write(bias, 2, rule.original)
            ws.write(bias, 3, rule.to)
            bias+=1
    wb.save("all_primary_rules.xls")