import xml.etree.ElementTree as ET
import os
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import CommonRule
from utils.MySqlConnectionFactory import MysqlConnectFactory
from preprocess.StrProcess import StrProcess


'''
author:cll
'''
s=0
class Insert:
    def insert_cmd_response(self):
        #path1 = os.path.abspath('..')
        #print(path1)

        filetypelist=[]
        rootdir, filetypelist,filelocation=self.file_type()
        #print(filetypelist)
        lenth=len(filetypelist)
        preprocess=StrProcess()
        Mysql_factory = MysqlConnectFactory()
        conn = Mysql_factory.get_connect()

        conn.set_charset('utf8')
        cur = conn.cursor()
        cur.execute('SET NAMES utf8;')
        cur.execute('SET CHARACTER SET utf8;')
        cur.execute('SET character_set_connection=utf8;')


        '''
        第几个文件夹数据
        '''
        #loca=str(2)
        for i in range(0, lenth):
                xmlpath =rootdir + '/' + filetypelist[i] + '/' + 'uut-com.xml'
                #print(filetypelist[i])

                tree = ET.parse(xmlpath)
                root = tree.getroot()

                count = 0
                num=0
                tempDict = {}
                #score需要
                #channels = root.find('channelinfo')
                #score=channels.find('score')
                for item in root.findall('item'):
                    response_list = []
                    cmd_list = []
                    # tempDict['id']=str(count)
                    responseText = item.findall('response')
                    cmdText = item.findall('cmd')

                    for childText in responseText:  # 利用getchildren方法得到子节点
                        # print(childNode.tag)
                        print(i)
                        print(childText.text)
                        response_list.append(preprocess.str_process(childText.text, 1))
                        print("=======after")
                        print(response_list)


                    for childText in cmdText:
                        cmd_list.append(preprocess.str_process(childText.text, 1))#0不删除...,1表示保留一个.

                    tempDict.update({count: {"cmd": cmd_list}})
                    tempDict[count].update({"response": response_list})
                    print(tempDict[count])
                    count += 1
                    num+=1

                tempJson = json.dumps(tempDict, ensure_ascii=False)#字典转str
                value = (filelocation,filetypelist[i],tempJson)
                #print(tempJson)

                cur.execute('insert into tsp_full_info values(null,%s,%s,%s,1.0)', value)

                conn.commit()

                conn.rollback()

        cur.close()
        conn.close()



    def file_type(self):
        path1 = os.path.abspath('..')
        #print(path1)
        filelocation=input()
        rootdir = path1 + '/datas/data/'+filelocation
        #print(rootdir)
        namelist = []

        for dirs in os.listdir(rootdir):
            namelist.append(dirs)

        return rootdir, namelist, filelocation


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

    path1 = os.path.abspath('..')
    print(path1)
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