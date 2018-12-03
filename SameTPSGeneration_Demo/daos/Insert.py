import xml.etree.ElementTree as ET
import os
import os.path


from utils import MySqlConnectionFactory
#class fileinfo:
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
        Mysql_factory = MySqlConnectionFactory.MysqlConnectFactory()
        conn = Mysql_factory.get_connect()

        conn.set_charset('utf8')
        cur = conn.cursor()
        cur.execute('SET NAMES utf8;')
        cur.execute('SET CHARACTER SET utf8;')
        cur.execute('SET character_set_connection=utf8;')


        '''
        sql='select * from tsp_info'
        cur.execute(sql)
        result=cur.fetchall()
        for row in result:
            print(row)
        #effectRow = cur.rowcount
        #print(effectRow)
        '''
        loca=str(5)#第一个文件夹数据
        for i in range(0, lenth):
                xmlpath =rootdir + '/' + filetypelist[i] + '/' + 'uut-com.xml'
                print(filetypelist[i])

                tree = ET.parse(xmlpath)
                root = tree.getroot()

                cmdstr = ''

                responsestr = ''
                #respontent = []
                #cmdtent = []
                count = 0
                for item in root.findall('item'):
                    count += 2
                    response_text = item.find('response').text
                    cmd_text = item.find('cmd').text
                    if cmd_text is not None:
                        if cmd_text.find('\n') != -1:
                            cmd_text = cmd_text.replace('\n', '\\n')
                            cmdstr = cmdstr + cmd_text + '||'
                            #cmdtent.append(cmd_text)
                            #cmdtent.append("==")
                        else:
                            cmdstr = cmdstr + cmd_text + '||'
                            #cmdtent.append(cmd_text)
                            #cmdtent.append("==")
                    else:
                        cmdstr = cmdstr + 'none' + '||'
                        #cmdtent.append(cmd_text)
                        #cmdtent.append("==")
                    if response_text is not None:
                        if response_text.find('\n') != -1 or response_text.find('..') !=-1:
                            response_text = response_text.replace('\n', '\\n').replace('..', '')
                            responsestr = responsestr + response_text + '||'
                            #respontent.append(response_text)
                            #respontent.append("==")
                        else:
                            responsestr = responsestr + response_text + '||'
                            #respontent.append(response_text)
                            #respontent.append("==")
                    else:
                        responsestr = responsestr + 'none' + '||'
                        #respontent.append(response_text)
                        #respontent.append("==")


                value = (loca,filetypelist[i],cmdstr,responsestr)
                print(cmdstr)
                cur.execute('insert into tsp_info values(null,%s,%s,%s,%s,0)', value)

                conn.commit()

               # conn.rollback()

        cur.close()
        conn.close()



                    #return cmdtent,value
              #except Exception, e:
                #print("open exception: %s: %s\n" %(e.errno, e.strerror))

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
    print("是否执行此程序")
    command = input()

    insert = Insert()
    insert.read_file()




if __name__=='__main__':
    main()