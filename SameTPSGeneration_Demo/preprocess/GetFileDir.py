import os
import errno
import sys
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
file_filter = [".xml",".info"]
class GetFileDir:
    def get_filedir(self, filepath):
        path1 = os.path.abspath('..')
        com_list = []

        for maindir, subdir, file_name_list in os.walk(filepath):
            for filename in file_name_list:
                apath = os.path.join(maindir, filename)  # 合并成一个完整路径
                ext = os.path.splitext(apath)[1]  # 获取文件后缀 [0]获取的是除了文件名以外的内容

                if ext in file_filter:
                    com_list.append(apath)  # 需要解析的com.xml完整路径
        return com_list
