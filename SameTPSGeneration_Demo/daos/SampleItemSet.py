import xml.etree.ElementTree as ET
import os
import json
import sys
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.MySqlConnectionFactory import MysqlConnectFactory
from preprocess.StrProcess import StrProcess
from preprocess.ParseXml import ParseXml

'''
author:cll
'''

class SampleItemSet:
    def insert_cmd_response(self,rootdir):
        list1=[]
        dir_dict=self.file_type(rootdir)
        parsexml=ParseXml()
        dirlist,tpslist=self.list_all_dic(rootdir,dir_dict,list1)#列出所有编码的路径
        for i in range(len(dirlist)):#进入某个编码
                all_item_set=[]
                namelist, dir_dict1 =self.com_xml(dirlist[i])#所有编码下的文件夹名
                all_info_dir=[]
                for j in dir_dict1.keys():
                    count=len(dir_dict1[j])
                    break
                for testname in dir_dict1.keys():  # 多少个生成文件包括原型组

                    if os.path.splitext(dir_dict1[testname][0])[1] == ".info":
                        infopath = os.path.join(testname, dir_dict1[testname][0])
                        if os.path.basename(testname) == "001_normalTest":
                            all_info_dir.insert(0, infopath)


                        else:
                            all_info_dir.append(infopath)

                for k in range(1,count):#每个文件夹有多少个com文件
                    all_com_dir = []
                    for testname in dir_dict1.keys():
                            filepath=os.path.join(testname,dir_dict1[testname][k])
                            if os.path.basename(testname) == "001_normalTest":
                                all_com_dir.insert(0,filepath)
                            else:
                                all_com_dir.append(filepath)

                    all_item_list=[]

                    for m in range(len(all_com_dir)):#一个com
                            try:
                                item_list = parsexml.parse_xml2(all_com_dir[m], all_info_dir[m], tpslist[i])
                                all_item_list.append(item_list)

                            except FileNotFoundError as e:
                                print(e)
                    all_item_set.append(all_item_list)
                yield  all_item_set


    def list_all_dic(self,rootdir, dict_a, list1):
        if isinstance(dict_a, dict) and dict_a:
            for x in dict_a.keys():
                tmpdir = os.path.join(rootdir, x)
                temp_value = dict_a[x]
                self.list_all_dic(tmpdir, temp_value, list1)
        else:
            if dict_a:
                for info in dict_a:
                    list1.append(os.path.join(rootdir, info))
            else:
                list1.append(rootdir)
        list2=[]
        for i in list1:
            list2.append(i.replace(rootdir+"/",""))
        return list1,list2


    def file_type(self,rootdir):
        path1 = os.path.abspath('..')
        namelist = []
        dir_list = []
        tmp_list=[]
        tempDict = {}
        '''
        默认当前目录从领域开始
        rootdir/data/field/tps/encode
        Dict:{filed:{tps:{encode},filed2:{tps:{encode}}
        '''
        for dirs in os.listdir(rootdir):

            if os.path.isdir(os.path.join(rootdir,dirs)) :

                    tempDict.update({dirs: {}})#领域

        for root,dirs,files in os.walk(rootdir):
            if dirs :
                for file in os.listdir(os.path.join(root, dirs[0])):
                    if files is None :
                            flag=1
                    elif os.path.splitext(file)[1]==".xml":
                        flag=0
                        break
                    else:
                        flag=1
            else:
                flag=0

            if flag==1:
                for dir in dirs:
                    if tempDict.__contains__(os.path.basename(root)):
                        tempDict[os.path.basename(root)].update({dir:{}})
                    elif tempDict.__contains__(os.path.basename(os.path.dirname(root))):
                        tempDict[os.path.basename(os.path.dirname(root))].update({(os.path.basename(root)):dirs})
                    else:
                        break

        return tempDict


    def com_xml(self,rootdir):
        namelist=[]
        dir_dict={}
        i=0
        for dirs in os.listdir(rootdir):
            namelist.append(dirs)#namelist是编码下的生成文件的文件名
            item_path = os.path.join(rootdir, namelist[i])
            if os.path.isdir(item_path):
                files=os.listdir(item_path)
                files.sort(key=lambda x: (x.split('.')[1],x.split('.')[0]))
                for allDir in files:

                        if item_path not in dir_dict.keys():
                            dir_dict[item_path] = [allDir]
                        else:
                            dir_dict[item_path].append(allDir)
            i=i+1
        return namelist,dir_dict

    def insert_common_rules(self,common_rules):
        Mysql_factory = MysqlConnectFactory()
        conn = Mysql_factory.get_connect()

        conn.set_charset('utf8')
        cur = conn.cursor()
        cur.execute('SET NAMES utf8;')
        cur.execute('SET CHARACTER SET utf8;')
        cur.execute('SET character_set_connection=utf8;')
        context_dic={}
        for common_rule in common_rules:
            dict={}
            dict.update({"front": common_rule.context[0], "later": common_rule.context[1]})
            context_json = json.dumps(dict, ensure_ascii=False)
            to_json = json.dumps(common_rule.to, ensure_ascii=False)

            value = (context_json, common_rule.original, to_json,
                  common_rule.kind, common_rule.score, common_rule.frequence)
            cur.execute('insert into common_rule values(null,%s,%s,%s,%s,%s,%s)', value)
            conn.commit()

            conn.rollback()

        cur.close()
        conn.close()

    def delete_all(self):
        Mysql_factory = MysqlConnectFactory()
        conn = Mysql_factory.get_connect()

        conn.set_charset('utf8')
        cur = conn.cursor()
        cur.execute('SET NAMES utf8;')
        cur.execute('SET CHARACTER SET utf8;')
        cur.execute('SET character_set_connection=utf8;')
        cur.execute('DELETE FROM testdemo.common_rule WHERE (id >0 )')
        conn.commit()
        conn.rollback()
        cur.close()
        conn.close()


def main():

    File_name=SampleItemSet()
    path1 = os.path.abspath('..')
    root = path1 + '/datas'
    # 默认当前目录从领域开始
    # rootdir / data / field / tps / encode
    for item_set in File_name.insert_cmd_response(root):
        print(item_set[0])
        print("len(item_set)",len(item_set))


if __name__=='__main__':
    main()