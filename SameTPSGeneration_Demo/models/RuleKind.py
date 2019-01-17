#coding=utf-8

class RuleKind:
      '''
      规则的类别
      '''
      #from确定且合并的和from不确定
      CONFIRM_AND_UNCONFIRM = "CONFIRM_AND_UNCONFIRM"
      #第三个类别
      REMINDER = "REMINDER"


if __name__ == '__main__':
    print(RuleKind.CONFIRM_AND_UNCONFIRM)

