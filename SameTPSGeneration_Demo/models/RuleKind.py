#coding=utf-8

class RuleKind:
      '''
      规则的类别
      '''
      #context 不保留
      CONFIRM_AND_UNCONFIRM = "CONFIRM_AND_UNCONFIRM"
      #context 保留
      REMINDER = "REMINDER"


if __name__ == '__main__':
    print(RuleKind.CONFIRM_AND_UNCONFIRM)

