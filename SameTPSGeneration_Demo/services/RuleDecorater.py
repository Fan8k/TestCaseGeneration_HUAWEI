#coding=utf-8
import re
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.Rule import Rule
from services.RuleMerger import RuleMerger
'''
规则装饰器：提取的规则比较细<<before_context,after_context>,from,to>，直接考虑的是修改点的整个前后部分的所有字母作为上下文
所以比较细（比如没有很好的分词）比如barcode:23432324jj97 barcode:23432324jj88 这两个barcode只有末端两个词做了修改，所以这个from和to
需要进行扩充两边都要加上23432324jj才行，这是分词问题，需要慢慢总结！
'''

class RuleDecorater:

    @classmethod
    def rule_word_decorater(cls,word_patern,rules):
        '''
        过时方法
        把已有规则的前部分context的最后部分所包含的word进行模式匹配先找到，先后把word词之后进行rule拼接改造
        :param word:
        :param rules:
        :return:
        '''
        if  'barcode' in word_patern:
            '第一种情况，处理barcode word=r"\[barcode:"'
            re_compile = re.compile(word_patern)
            for rule in rules:
                #必须在尾巴处匹配到barcode，这样说明这个rule就是修改了barcode
                before_context = rule.context[0]
                result = re_compile.search(before_context, len(before_context) - 23)
                if result:
                    #修改点拼接
                    common_str = before_context[result.span()[1]:]
                    rule.original = common_str+rule.original
                    rule.to = common_str+rule.to
                    # 去除上下文多余的
                    before_context = before_context[0:result.span()[1]]
                    rule.context = (before_context,rule.context[1])
        return rules

    @classmethod
    def orinial_rule_decorater(cls):
        pass

if __name__ =="__main__":
    before_context ="\\r\\nOK\\r\\r\\n\\r\\r\\n  \\(1)\\UUT_SWT(1)\\Qbarcode(1).........................Pass [00:00:00.000]\\r\\r\\n  qbarcode............................................Pass [barcode:023DUA0147258"
    after_context = "]\\r\\r\\n  \\(1)\\UUT_SWT(1)\\Qbarcode(*).........................Pass [00:00:00.000]\\r\\r\\n\\UUT_SWT&gt; "
    rules = [Rule((before_context,after_context),'369','963','1'),Rule((before_context,after_context),'369','963','1'),Rule((before_context,after_context),'369','964','1'),Rule((before_context,after_context),'368','963','1')]
    #上面假设来自提取规则ExtractRules 这个类拿到的所有的原始规则集合。
    rules = RuleDecorater.rule_word_decorater(r"\[barcode:",rules)
    print(rules)
    rules = RuleMerger.mergeredBy_contextOrigin(rules)
    print(rules[1])
    print(rules[0].random_choice_to())

