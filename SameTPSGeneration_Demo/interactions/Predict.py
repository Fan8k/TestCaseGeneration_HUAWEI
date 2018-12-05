#coding=utf-8
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.DataMatch import DataMatch
from services.ExtractRules import ExtractRules
from utils.ExtractLocationInfo import ExtractLocationInfo
'''
输入原型组数据预测生成相应的模型组数据
'''

class Predict:

    def predict(self,path,rules):
        '''
        输入想要预测的原型组文件的绝对路径，所用到的规则
        :param path: 原型组文件的绝对路径
        :param rules: 所用到的规则
        :yield 每次更新一个item就返回生成
        '''
        dataMatch = DataMatch(path)
        yield dataMatch.match(rules)


if __name__ == "__main__":
    path = "想要预测的文件的绝对路径"
    #tps下
    tps = ExtractLocationInfo.extract_location_and_type_info(r"/home/inspur/li/SameTPSGeneration_Demo/datas/data")
    #某一个编码 比如编码1 下面的原型组 001_normalTest
    location = ['1','2','3','4','5']
    #选择的目标编码
    aim_location = location[0]
    proto_type, model_types=ExtractLocationInfo.filter_proto_type(tps[aim_location],'001_normalTest')
    extractRuler = ExtractRules()
    #整个编码下所有的规则
    encode_rules = extractRuler.get_encode_rules(aim_location,proto_type,model_types)
    predicter = Predict()
    predicter.predict(path,encode_rules)