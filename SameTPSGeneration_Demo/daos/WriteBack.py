import xml.etree.ElementTree as ET
import sys
import os


import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#from GetXML import GetXML
from daos.GetXML import GetXML
'''

'''

class WriteBack():

    def newxml(self,item_info_list=[],filepath=None):
        '''
        item_info_list：传入item相关信息的列表，里面是一个个元组
        filepath：传入的原型xml的完整路径
        item_num: 传入修改的item的位置，第几个item被修改
        '''
        path1 = os.path.abspath('..')
        #path2 = path1 + '/output/' + item_info_list[0][0][0].location_info



        #global file_count
        for file_count in range(len(item_info_list)):

            path2 = path1 + '/output/' +str(file_count+1)
            print(path2)
            self.mkdir(path2)
            print(os.path.exists(path1))
            '''
            重写原型文件
            '''
            tree = ET.parse(filepath)
            root = tree.getroot()

            tree.write(path2 + '/newnormalcom.xml')
            first_item = root.find('channelinfo')
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



            # if os.path.exists(path2 + '/newnormalcom.xml') is not True:
            #     get_xml = GetXML()
            #     normalcount = 0
            #     # 插入新的标签score
            #     normal_itemlist = get_xml.read_file(filepath)
            #     for item in root.findall('item'):
            #         reponse_text = item.findall('response')
            #         templist = normal_itemlist[normalcount].responses
            #         for i in range(len(reponse_text)):
            #             if templist[i] == 'None':
            #                 reponse_text[i].text = ''
            #             else:
            #                 reponse_text[i].text = templist[i]
            #         tree.write(path2 + '/newnormalcom.xml')
            #         normalcount += 1
            '''
            本次修改的item对应的score
            '''


            #生成模型文件
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
                        if   templist[i]=='None':
                            reponse_text[i].text = ''
                        else:
                            reponse_text[i].text=templist[i]

                    tree.write(path2+'/com.xml')

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
    filepath = path1+'/datas/data/2/001_normalTest/uut_com.xml'
    get_xml = GetXML()
    itemlist = get_xml.read_file(filepath)
    writeback = WriteBack()
    writeback.newxml(itemlist, filepath, item_num)


if __name__=='__main__':
    main()