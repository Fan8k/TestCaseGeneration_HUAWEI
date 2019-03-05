#coding=utf-8
from sys import argv
from os import path as op
from sys import path as sp
sp.append(op.dirname(op.dirname(op.abspath(__file__))))

from daos.GetXML import GetXML
#from daos.WriteBack import WriteBack
from daos.SampleItemSet import SampleItemSet
from services.ExtractRuler import ExtractRuler
from interactions.Predict import Predict
from services.RuleDecorater import RuleDecorater
from services.RuleMerger import RuleMerger
from services.RuleSorter import RuleSorter
from daos.WriteBack import WriteBack

'''
argv[1]: 多通道的原型组文件夹路径 比如C://de （de下存储的是info文件和多个com文件）
argv[2]: 已有的规则文件夹路径 形如: C://数据 (数据下存储的是领域/tps/编码/原型组等)
argv[3]: flag 标志：1=使用最小编辑距离匹配 2=使用context为空匹配
argv[4]: 提取的规则是否进行存储 1=否 2=是
'''
if __name__ == '__main__':
    if(len(argv))<=1:
        print("请输入脚本需要的参数")
    else:
        #提取规则
        sampler = SampleItemSet()
        primary_rules = []
        extractRuler = ExtractRuler()
        for item_set in sampler.insert_cmd_response(argv[2]):
            #一个编码下所有的多通道规则[[com1_原型组.xml,com1_模型组.xml],[],[]]
            for item_list in item_set:
                for i in range(1,len(item_list)):
                    primary_rules.extend(extractRuler.get_rules_from_items(item_list[0],item_list[i]))
        #规则处理
        rules = RuleDecorater.orinial_rule_decorater([(':', "["), ('\[', 'P')], primary_rules)

        if argv[3]==2:
           # 装饰之后需要进行按照上下文和from进行合并 提成更普通的规则
           common_rules = RuleMerger.mergeredBy_origin_igonreCase(rules,2)
        else:
           common_rules = RuleMerger.mergeredBy_contextOrigin(rules)
        common_rules = RuleSorter.sort_by_scoreAndFrequence(common_rules)

        #if argv[4]==2:
            #sampler.insert_common_rules(common_rules)

        #预测
        parse_prototype = GetXML()
        predicter = Predict()
        wb = WriteBack()
        for items, comlist in parse_prototype.read_file(argv[1]):  # 获取文件夹下所有com.xml文件内容
            #每次返回一个通道的一个com.xml文件的item集合
            aim = predicter.predict(items, common_rules)
            wb.newxml(aim, comlist)

        if argv[4]==2:
            sampler.delete_all();