#coding=utf-8

'''
md5加密工具类
'''

import hashlib

class MD5(object):

      def __init__(self):
          self.md = hashlib.md5()

      def encode(self,str):
          self.md.update(str.encode("utf-8"))
          return self.md.hexdigest()



if __name__=="__main__":
    m = MD5()
    print(m.encode("hhahhh"))