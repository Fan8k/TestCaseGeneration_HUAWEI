#coding=utf-8

'''
遍历目标文件夹，提取想要的文件名字信息
'''
import os


class ExtractLocationInfo:

    @classmethod
    def extract_location_and_type_info(cls,path):
        location_type_info = {}
        files = os.listdir(path)
        for file in files:
            file_abs_path = os.path.join(path,file)
            if os.path.isdir(file_abs_path):
                location_type_info[file] = os.walk(file_abs_path).__next__()[1]
        return location_type_info

    @classmethod
    def filter_proto_type(cls,types,proto_type):
        '''
        输入所有的编码下的模型组和原型组文件名字，和原型组文件名字，就能分开模型组和原型组文件
        :param types: 所有的文件名i在
        :param proto_type: 原型组文件名字
        :return: （原型组，模型组）
        '''
        for index,type in enumerate(types):
            if type == proto_type:
                del types[index]
        return (proto_type,types)


if __name__ =="__main__":
    di = ExtractLocationInfo.extract_location_and_type_info(r"/home/inspur/li/SameTPSGeneration_Demo/datas/data")
    l = di['1']
    del l[-2]
    print(l)
    #print("/home/inspur/li/SameTPSGeneration_Demo/datas/data")
    #print(os.walk("/home/inspur/li/SameTPSGeneration_Demo/datas/data").__next__())
