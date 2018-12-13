import xml.etree.ElementTree as ET
import os
import os.path
import json
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(sys.path)
from utils.MySqlConnectionFactory import MysqlConnectFactory
from preprocess.StrProcess import StrProcess

'''
author:cll
'''

class Insert:
    def read_file(self):
        #path1 = os.path.abspath('..')
        #print(path1)

        filetypelist=[]
        rootdir, filetypelist=self.filetype()
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
        loca=str(5)
        for i in range(0, lenth):
                xmlpath =rootdir + '/' + filetypelist[i] + '/' + 'uut-com.xml'
                #print(filetypelist[i])

                tree = ET.parse(xmlpath)
                root = tree.getroot()

                count = 0
                tempDict = {}

                for item in root.findall('item'):
                    response_list = []
                    cmd_list = []
                    # tempDict['id']=str(count)
                    responseText = item.findall('response')
                    cmdText = item.findall('cmd')

                    for childText in responseText:  # 利用getchildren方法得到子节点
                        # print(childNode.tag)
                        response_list.append(preprocess.str_process(childText.text, 1))


                    for childText in cmdText:
                        cmd_list.append(preprocess.str_process(childText.text, 1))#0不删除...

                    tempDict.update({count: {"cmd": cmd_list}})
                    tempDict[count].update({"response": response_list})
                    #print(tempDict[count])
                    count += 1

                tempJson = json.dumps(tempDict, ensure_ascii=False)#字典转str
                value = (loca,filetypelist[i],tempJson)
                print(tempJson)

                #cur.execute('insert into tsp_full_info values(null,%s,%s,%s,0)', value)

                #conn.commit()

               # conn.rollback()

        cur.close()
        conn.close()



    def filetype(self):
        path1 = os.path.abspath('..')
        #print(path1)
        rootdir = path1 + '/datas/data'+'/5'
        #print(rootdir)
        namelist = []

        for dirs in os.listdir(rootdir):
            namelist.append(dirs)

        return rootdir, namelist



def main():
    # print("是否执行此程序")
    # command = input()

    insert = Insert()
    insert.read_file()




if __name__=='__main__':
    main()