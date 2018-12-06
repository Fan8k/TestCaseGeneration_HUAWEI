#coding=utf-8

'''
md5加密工具类
'''

import hashlib

class MD5(object):

      def encode(self,str):
          self.md = hashlib.md5()
          self.md.update(str.encode("utf-8"))
          return self.md.hexdigest()



if __name__=="__main__":
    m = MD5()
    print(r"\r\nOK\r\r\n".encode("utf-8"))
    print(r"\r\nOK\r\r\n".encode("utf-8"))
    print(m.encode(r"\r\nOK\r\r\n"))
    print(m.encode(r"\r\nOK\r\r\n"))
    print(m.encode(r"\r\nOK\r\r\n"))