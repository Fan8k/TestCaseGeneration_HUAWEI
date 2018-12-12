#coding=utf-8
import os
import sys
import difflib
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.DataMatcher import DataMatcher
from services.ExtractRuler import ExtractRuler
from utils.ExtractLocationInfo import ExtractLocationInfo
from services.RuleDecorater import RuleDecorater
from services.RuleMerger import RuleMerger
from interactions.Predict import Predict
from models.Item import Item
from daos.GetXML import GetXML
from daos.SelectObject import SelectObject

'''
手动测试
'''
def create_item():
    # proto_items = []
    # model_items = []
    # proto_items.append(Item([r'test BiosCheck\r'],[r'\r\nOK\r\r\n',r'\r\r\n  \(1)\UUT_SWT(1)\BiosCheck(1)Pass [00:00:00.000]\r\r\n  bios_checkPass [Pass]\r\r\n  \(1)\UUT_SWT(1)\BiosCheck(*)Pass [00:00:00.000]\r\r\n\UUT_SWT&gt; '],0,'1',1))
    # model_items.append(Item([r'test BiosCheck\r'],[r'\r\nOK\r\r\n',r'\r\r\n  \(1)\UUT_SWT(1)\BiosCheck(1)Fail [00:00:00.000]\r\r\n  bios_checkFail [.Fail ]\r\r\n  \(1)\UUT_SWT(1)\BiosCheck(*)Fail [00:00:00.000]\r\r\n\UUT_SWT&gt; '],0,'1',1))
    # proto_items.append(Item([r'test precision\r'],[r'\r\nOK\r\r\n\r\r\n  \(1)\UUT_SWT(1)\Precision(1)Pass [00:00:00.000]\r\r\n  precisionPass [date:2018-03-28 time:17:24:54]\r\r\n  \(1)\UUT_SWT(1)\Precision(*)Pass [00:00:00.000]\r\r\n\UUT_SWT&gt; '],0,'1',1))
    # model_items.append(Item([r'test precision\r'],[r'\r\nOK\r\r\n\r\r\n  \(1)\UUT_SWT(1)\Precision(1)Pass [00:00:00.000]\r\r\n  precisionPass [date:1000-03-28 time:17:24:54]\r\r\n  \(1)\UUT_SWT(1)\Precision(*)Pass [00:00:00.000]\r\r\n\UUT_SWT&gt; '],0, '1', 1))
    # proto_items.append(Item([r'test qbarcode\r'], [r'\r\nOK\r\r\n\r\r\n  \(1)\UUT_SWT(1)\Qbarcode(1)Pass [00:00:00.000]\r\r\n  qbarcodePass [barcode:023DUA0147258369]\r\r\n  \(1)\UUT_SWT(1)\Qbarcode(*)Pass [00:00:00.000]\r\r\n\UUT_SWT&gt; '], 0, '1', 1))
    # model_items.append(Item([r'test qbarcode\r'], [r'\r\nOK\r\r\n\r\r\n  \(1)\UUT_SWT(1)\Qbarcode(1)Pass [00:00:00.000]\r\r\n  qbarcodePass [barcode:023DUA0147258963]\r\r\n  \(1)\UUT_SWT(1)\Qbarcode(*)Pass [00:00:00.000]\r\r\n\UUT_SWT&gt; '], 0, '1', 1))
    # return proto_items,model_items
    st = SelectObject()
    proto_items = st.selected_object('1','001_normalTest')
    model_items = st.selected_object('1','002_checkTest_BiosCheck_Fail')
    return proto_items,model_items


def create_predict_item():
    predict_items = []
    predict_items.append(Item([r'test qbarcode\r'],[r'\r\nOK\r\r\n\r\r\n  \(1)\UUT_SWT(1)\Qbarcode(1)Pass [00:00:00.000]\r\r\n  qbarcodePass [barcode:023DUA0147258369]\r\r\n  \(1)\UUT_SWT(1)\Qbarcode(*)Pass [00:00:00.000]\r\r\n\UUT_SWT&gt; '],0,'1',1))
    predict_items.append(Item([r'test CpuPcieRW\r'], [r'\r\nOK\r\r\n\r\r\n  \(1)\UUT_SWT(1)\CpuPcieRW(1)Pass [00:00:00.000]\r\r\n  cpu_pcie_link_state_0Pass [1:1:0.0:0x14e4]\r\r\n  cpu_pcie_link_state_1Pass [1:1:0.1:0x14e4]\r\r\n  \(1)\UUT_SWT(1)\CpuPcieRW(*)Pass [00:00:00.000]\r\r\n\UUT_SWT&gt; '], 0, '1', 2))
    predict_items.append(Item([r'test multicore\r'], [r'\r\nOK\r\r\n\r\r\n  \(1)\UUT_SWT(1)\Multicore(1)Pass [00:00:00.000]\r\r\n  multi_core0Pass [Pass]\r\r\n  multi_core1Pass [Pass]\r\r\n  multi_core2Pass [Pass]\r\r\n  multi_core3Pass [Pass]\r\r\n  \(1)\UUT_SWT(1)\Multicore(*)Pass [00:00:00.000]\r\r\n\UUT_SWT&gt; '], 0, '1', 3))
    predict_items.append(Item([r'test BiosCheck\r'], [r'\r\nOK\r\r\n',r'\r\r\n  \(1)\UUT_SWT(1)\BiosCheck(1)Pass [00:00:00.000]\r\r\n  bios_checkPass [Pass]\r\r\n  \(1)\UUT_SWT(1)\BiosCheck(*)Pass [00:00:00.000]\r\r\n\UUT_SWT&gt; '], 0, '1', 4))
    return predict_items


if __name__ == "__main__":
    proto_items, model_items = create_item()
    extractRuler = ExtractRuler()
    # 整个编码下所有的规则
    encode_rules = extractRuler._get_rules(proto_items,model_items)
    print("原规则")
    for com in encode_rules:
        print(com)
    print("\n\n")
    # 原始规则进行装饰和合并
    # 这里只是进行barcode 单词装饰
    rules = RuleDecorater.rule_word_decorater(r"\[barcode:", encode_rules)
    # 装饰之后需要进行按照上下文和from进行合并 提成更普通的规则
    common_rules = RuleMerger.mergeredBy_contextOrigin(rules)
    print("通用规则")
    #print(common_rules)
    for com in common_rules:
        print(com)
    print("预测\n\n")
    # predicter = Predict()
    # gen = predicter.test(create_predict_item(),common_rules)
    # for items in gen:
    #     for item in items:
    #         print(item)
    #     print("\n\n")
    #
    # for i in create_predict_item():
    #     print(i)

    for item in proto_items:
        print(item)

    print("\n\n")

    for item in model_items:
        print(item)