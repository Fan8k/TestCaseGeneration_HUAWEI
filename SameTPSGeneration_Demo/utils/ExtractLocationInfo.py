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



if __name__ =="__main__":
    di = ExtractLocationInfo.extract_location_and_type_info(r"/home/inspur/li/SameTPSGeneration_Demo/datas/data")
    print(di['1'])
    #print("/home/inspur/li/SameTPSGeneration_Demo/datas/data")
    #print(os.walk("/home/inspur/li/SameTPSGeneration_Demo/datas/data").__next__())
