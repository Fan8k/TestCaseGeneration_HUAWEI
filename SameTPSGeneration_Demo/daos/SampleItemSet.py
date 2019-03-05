import xml.etree.ElementTree as ET
import os
import json
import sys
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import CommonRule
from utils.MySqlConnectionFactory import MysqlConnectFactory
from preprocess.StrProcess import StrProcess
from preprocess.ParseXml import ParseXml

'''
author:cll
'''
s=0
class SampleItemSet:
    def insert_cmd_response(self,rootdir):
        #path1 = os.path.abspath('..')
        #print(path1)

        filetypelist=[]
        list1=[]
        dir_dict=self.file_type(rootdir)

        parsexml=ParseXml()
        preprocess=StrProcess()
        dirlist,tpslist=self.list_all_dic(rootdir,dir_dict,list1)#列出所有编码的路径

        # Mysql_factory = MysqlConnectFactory()
        # conn = Mysql_factory.get_connect()
        #
        # conn.set_charset('utf8')
        # cur = conn.cursor()
        # cur.execute('SET NAMES utf8;')
        # cur.execute('SET CHARACTER SET utf8;')
        # cur.execute('SET character_set_connection=utf8;')


        for i in range(len(dirlist)):#进入某个编码
                all_item_set=[]
                namelist, dir_dict =self.com_xml(dirlist[i])

                all_info_dir=[]
                for j in dir_dict.keys():
                    count=len(dir_dict[j])
                    break
                me=0
                for testname in dir_dict.keys():  # 多少个生成文件包括原型组

                    if os.path.splitext(dir_dict[testname][0])[1] == ".info":
                        infopath = os.path.join(testname, dir_dict[testname][0])
                        if os.path.basename(testname) == "001_normalTest":
                            all_info_dir.insert(0, infopath)

                            me=me+1
                        else:
                            all_info_dir.append(infopath)
                for k in range(1,count):#每个文件夹有多少个com文件
                    all_com_dir=[]


                    filepath=os.path.join(testname,dir_dict[testname][k])
                    if os.path.basename(testname) == "001_normalTest":
                        all_com_dir.insert(0,filepath)
                    else:
                        all_com_dir.append(filepath)
                    # print(len(all_com_dir))
                    # print(len(all_info_dir))
                    # print(tpslist[i])
                all_item_list=[]
                for j in range(len(all_com_dir)):
                        try:
                            item_list = parsexml.parse_xml2(all_com_dir[j], all_info_dir[j], tpslist[i])
                            # print(item_list[1].location_info)
                            all_item_list.append(item_list)

                        except FileNotFoundError as e:
                            print(e)
                #print((all_item_list[0])[0].location_info)
                all_item_set.append(all_item_list)
                #print(all_item_set)
                yield  all_item_set


                             # root = tree.getroot()
                             #
                             # count = 0
                             # num = 0
                             # tempDict = {}
                             # # score需要
                             # # channels = root.find('channelinfo')
                             # # score=channels.find('score')
                             # for item in root.findall('item'):
                             #     response_list = []
                             #     cmd_list = []
                             #     # tempDict['id']=str(count)
                             #     responseText = item.findall('response')
                             #     cmdText = item.findall('cmd')
                             #
                             #     for childText in responseText:  # 利用getchildren方法得到子节点
                             #         # print(childNode.tag)
                             #         print(i)
                             #         print(childText.text)
                             #         response_list.append(preprocess.str_process(childText.text, 1))
                             #         print("=======after")
                             #         print(response_list)
                             #
                             #     for childText in cmdText:
                             #         cmd_list.append(preprocess.str_process(childText.text, 1))  # 0不删除...,1表示保留一个.
                             #
                             #     tempDict.update({count: {"cmd": cmd_list}})
                             #     tempDict[count].update({"response": response_list})
                             #     print(tempDict[count])
                             #     count += 1
                             #     num += 1


    def list_all_dic(self,rootdir, dict_a, list1):
        if isinstance(dict_a, dict) and dict_a:
            for x in dict_a.keys():
                # print(rootdir)
                # print(x)
                tmpdir = os.path.join(rootdir, x)
                temp_value = dict_a[x]
                # rootdir=os.path.join(rootdir,x)
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
        #print(path1)
        #filelocation=input()
        #rootdir = path1 + '/datas'
        #print(rootdir)
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
                #print(dirs)
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
                    #print(allDir)
                    #if re.search('.xml', allDir) != None:  # search()会扫描整个string查找匹配,会扫描整个字符串并返回第一个成功的匹配
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





def main():

    File_name=SampleItemSet()
    path1 = os.path.abspath('..')
    root = path1 + '/datas/data'
    # 默认当前目录从领域开始
    # rootdir / data / field / tps / encode
    for item_set in File_name.insert_cmd_response(root):
        print(item_set)
    #print("rootdir:", rootdir)

    # info_list=[]
    # for i in range(2):
    #     s_info=CommonRule.CommonRule(context=("(1)\\UUT_SWT(1)\\BiosCheck(1)Pass [00:00:01.000] bios_check",
    #                                           "] 100ge_i2cPass [Pass] 100ge_txdisPass [Pass] 100ge_txenPass "),
    #                                  original="Pass [Pass", to={"Fail[Fail": 3, "Fail[Fail]": 2}, _kind="121", score=2,
    #                                  frequence=i)
    #     info_list.append(s_info)
    # insertion=Insert()
    # insertion.insert_common_rules(info_list)






if __name__=='__main__':
    main()