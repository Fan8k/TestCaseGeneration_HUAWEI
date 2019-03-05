import xml.etree.ElementTree as ET
import sys
import os


import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from GetXML import GetXML
#from daos.GetXML import GetXML

'''

'''

class WriteBack():
    def __init__(self):
        self.filecount = 0

    def newxml(self,item_info_list=[],comlist=[]):
        '''
        item_info_list：传入item相关信息的列表，里面是一个个元组
        comlist：传入的原型xml的完整路径
        item_num: 传入修改的item的位置，第几个item被修改
        '''
        path1 = os.path.abspath('..')
        '''
        重写原型文件
        '''
        original_path = item_info_list[0][0][0].location_info
        path2 = path1 + '/output/001_normalTest'
        self.mkdir(path2)
        for comname  in comlist:
           tree = ET.parse(comname)
           tree.write(os.path.join(path2,os.path.basename(comname)))
        for infoname in comlist:
            if os.path.splitext(os.path.basename(comname)[1]) == ".info":
                tree_info = ET.parse(infoname)
                root_info = tree_info.getroot()
                break
        temp_count=self.filecount
        for file_count in range(len(item_info_list)):

            path2 = path1 + '/output/' + str(self.filecount+1)
            self.mkdir(path2)

            '''
            本次修改的item对应的score
            '''


            first_item = root_info.find('sceneinfo')
            score_list = first_item.findall('score')
            if len(score_list) == 0:
                score = ET.Element('score')
                score.text = str(item_info_list[file_count][1][1])
                score.tail = "\r\n"
                first_item.append(score)
                #root.append(first_item)
            else:
                for i in range(len(score_list)):
                    score_list[i].text = str(item_info_list[file_count][1][1])

            tree_info.write(os.path.join(path2,os.path.basename(infoname)))





            #生成模型文件
            tree = ET.parse(original_path)
            root = tree.getroot()
            num=0
            for item in root.findall('item'):
                num+=1
                if num==item_info_list[file_count][1][0]+1:
                    '''
                    item_info_list[file_count][1][0]为修改的item的index
                    修改loop
                    '''
                    loop_text = item.find('loop')
                    loop_text.text = '3'
                    reponse_text=item.findall('response')
                    templist=item_info_list[file_count][0][num-1].responses
                    for i in range(len(reponse_text)):
                        if templist[i]=='None':
                            reponse_text[i].text = ''
                        else:
                            reponse_text[i].text=templist[i]

                    tree.write(os.path.join(path2,os.path.basename(original_path)))
                    break
        for name in comlist:
            if name is not original_path:
                tree_other=ET.parse(name)
                for i in range(temp_count,self.filecount):
                    path3 = path1 + '/output/' + str(i + 1)
                    tree_other.write(os.path.join(path3,os.path.basename(name)))
        #return file_count

    def mkdir(self,path1):
        isExists=os.path.exists(path1)
        if not isExists:
            #不存在路径就创建
            os.makedirs(path1)



def main():
    path1 = os.path.abspath('..')
    print(path1)
    item_num=3
    filepath = path1+'/datas/data/tps1/1/001_normalTest'
    get_xml = GetXML()

    for itemlist,comlist in get_xml.read_file(filepath):
        print(comlist)


if __name__=='__main__':
    main()