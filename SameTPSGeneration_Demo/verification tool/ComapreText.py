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


def _find_change_points(pri_response_str, model_response_str):
    '''
    根据两个item的reponse 字符串找出所有的更改点
    :param pri_response_str:  原字符串 update service loopmode 1\\r||update pass ratio 2
    :param model_response_str: 新字符串 update service fail 1\\r||update pass ratio 2
    :return:（[<from:to>,<from,to>],[common context，common context，common context]）
    '''

    results = ExtractRuler.differ.compare(pri_response_str, model_response_str)
    '''
      '- '	line unique to sequence 1
      '+ '	line unique to sequence 2
      '  '	line common to both sequences
      '? '	line not present in either input sequence
      公共context建立方法：
      修改点建立方法：（从碰到第一个不同处开始，到最后一个不同点）
    '''
    change_contexts = []
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
    for label in results:
        if label.startswith("-"):
            print("序列1特有：%s"%label[2:3])
        elif label.startswith("+"):
            print("序列2特有：%s" % label[2:3])
        elif label.startswith(" "):
            print("都有：%s" % label[2:3])
        elif label.startswith("?"):
            print("都不存在%s"%label)
    for index, label in enumerate(results):
        # 共同期
        if common_staus == True and label.startswith(" "):
            temp_change_context += label[2:3]
        # 只要碰到修改点就要切换状态，保留之前的共有上下文信息,重新下一轮
        if label.startswith("-") or label.startswith("+"):
            common_staus = False
            if len(temp_change_context) > 0:
                change_contexts.append(temp_change_context)
                temp_change_context = ""

        # 进入修改期
        if common_staus == False:
            if label.startswith("-"):
                temp_origin_str += label[2:3]
            if label.startswith("+"):
                temp_to_str += label[2:3]
            if label.startswith(" "):
                temp_origin_str += label[2:3]
                temp_to_str += label[2:3]

        # 修改期状态监测:默认规则是探测下两个是否都是共有的，如果是共有就切换成共有期
        if common_staus == False:
            if index + 2 < total:
                if results[index + 1].startswith(" ") and results[index + 2].startswith(" "):
                    common_staus = True
            elif index + 2 == total:
                # 倒数两个的话，看看最后一个是否需要切换
                if results[index + 1].startswith(" "):
                    common_staus = True
            if common_staus == True:
                changes_origin_to.append((temp_origin_str, temp_to_str))
                temp_to_str = ""
                temp_origin_str = ""
        # 结束操作
        if index + 1 == total:
            if common_staus == True:
                change_contexts.append(temp_change_context)
            if common_staus == False:
                changes_origin_to.append((temp_origin_str, temp_to_str))

    return (change_contexts, changes_origin_to)

if __name__ =="__main__":
    ex = ExtractRuler()
    results=_find_change_points("\\r\\r\\n  \\(1)\\UUT_SWT(1)\\LSWTableTest(1)Pass [00:00:00.000]\\r\\r\\n  KAPS_Chip0Pass [Pass]\\r\\r\\n  \\(1)\\UUT_SWT(1)\\LSWTableTest(*)Pass [00:00:00.000]\\r\\r\\n\\UUT_SWT> ",
                                   "\\r\\r\\n  \\(1)\\UUT_SWT(1)\\LSWTableTest(1)Pass [00:00:00.000]\\r\\r\\n  KAPS_Chip0Fail[Fail]\\r\\r\\n  \\(1)\\UUT_SWT(1)\\LSWTableTest(*)Pass [00:00:00.000]\\r\\r\\n\\UUT_SWT> ")
    print(results[0])
    print(results[1])