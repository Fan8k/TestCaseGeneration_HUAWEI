#coding=utf-8
import re
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.Rule import Rule
from services.RuleMerger import RuleMerger
import re
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
    def orinial_rule_decorater(cls,stop_masks,rules):
        '''
        根据停止标记符，进行规则提取，而且停止标识符不区分大小写
        :param stop_masks: [(':','['),('[','P')] 一个元祖中最后一个代表停止标识符，前面的比如':'表示满足停止的条件就是停止标识前面的字符串有：才能停止
        :param rule: 所有原始的规则
        :return: 提取barcode这种context为空，from为 barcode:\w{10}这种这几把word的个数定死的新型规则
        '''
        for rule in RuleDecorater._comfirm_from(stop_masks,rules):
            #拿到已经抽出了bacode这种前缀之后的rule，做一个正则表达式转换
            result = re.search(":",rule.original)
            if result:
                _nums = len(rule.original[result.span()[1]:])
                if RuleDecorater.change_all_num_word(rule.original[result.span()[1]:]):
                   rule.original = rule.original[:result.span()[1]]+("\d{%s}"%_nums)
                else:
                   rule.original = rule.original[:result.span()[1]] + ("\w{%s}" % _nums)
            else:
                result = re.search("\[",rule.original)
                if result:
                    _nums = len(rule.original[result.span()[1]:])
                    if RuleDecorater.change_all_num_word(rule.original[result.span()[1]:]):
                       rule.original = rule.original[:result.span()[1]] + ("\d{%s}" % _nums)
                    else:
                       rule.original = rule.original[:result.span()[1]] + ("\w{%s}" % _nums)
        return rules

    @classmethod
    def change_all_num_word(cls,original):
        is_allNums = False
        for i in original:
          try:
              if int(i)>=0 and int(i) <=9:
                 continue
          except Exception as e:
              break
        else:
           is_allNums = True
        return is_allNums

    @classmethod
    def _comfirm_from(cls,stop_masks,rules):
        # 先找出所有停止点
        stop_labels = []
        for mask in stop_masks:
            stop_labels.append(mask[-1])

        # 找出rule中from为纯数字这种，因为这种就是from不定的规则
        for rule in rules:
            try:
                # 如果能转换成int肯定是纯整数
                int(rule.original)
                before_context = rule.context[0]
                temp_str = ""
                stop_flag = False
                for i in range(1, len(before_context) + 1):
                    _label = before_context[-i]
                    for index, stop_label in enumerate(stop_labels):
                        if _label.lower() == stop_label.lower():
                            _verify_start = 0
                            for mask_index, premise_label in enumerate(stop_masks[index]):
                                # 只要不满足立马结束循环
                                if mask_index + 1 == len(stop_masks[index]):
                                    continue
                                # 只要第一个匹配上就行
                                result = re.search(premise_label, temp_str[_verify_start:])
                                if result:
                                    _verify_start = result.span()[1]
                                else:
                                    break
                            else:
                                # 上面只要能正确执行完，说明这个停止点满足前面的各种限制符的顺序存在的要求。
                                stop_flag = True
                                break
                    else:
                        temp_str += _label
                    if stop_flag:
                        temp_str += _label
                        break
            except Exception as e:
                continue
            #修改rule的original和to
            rule.original = temp_str[::-1]+rule.original
            #对于from 为[210 是因为前面的pass做了修改 所以它的context为[ 但是为了避免到处改特此加上pass
            if re.match(r"\d*\[$",temp_str.strip()):
                rule.original = "Pass"+rule.original
            rule.to = temp_str[::-1]+rule.to
            rule.context = ("","")
            yield rule


if __name__ =="__main__":
    before_context ="\\r\\nOK\\r\\r\\n\\r\\r\\n  \\(1)\\UUT_SWT(1)\\Qbarcode(1).........................Pass [00:00:00.000]\\r\\r\\n  qbarcode............................................Pass [barcode:023DUA0147258"
    after_context = "]\\r\\r\\n  \\(1)\\UUT_SWT(1)\\Qbarcode(*).........................Pass [00:00:00.000]\\r\\r\\n\\UUT_SWT&gt; "
    rules = [Rule((before_context,after_context),'369','963','1'),Rule((before_context,after_context),'369','963','1'),Rule((before_context,after_context),'369','964','1'),Rule((before_context,after_context),'368','963','1')]
    #上面假设来自提取规则ExtractRules 这个类拿到的所有的原始规则集合。

    rules = RuleDecorater.orinial_rule_decorater([(':',"[")],rules)
    for rule in rules:
        print(rule)
    rules = RuleMerger.mergeredBy_contextOrigin(rules)
    for rule in rules:
        print(rule)
    print(rules[0])
    print(rules[0].random_choice_to())
    print(re.search("b",'fadfabrrr').span()[1])