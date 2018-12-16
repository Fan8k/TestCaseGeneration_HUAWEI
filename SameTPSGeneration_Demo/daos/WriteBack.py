import xml.etree.ElementTree as ET
import sys
import os
import uuid

import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from GetXML import GetXML
#from daos.GetXML import GetXML
class WriteBack():

    def newxml(self,itemlist=[],filepath=None):
        '''
        itemlist[]：传入itemlist集合
        filepath：传入的原型xml的完整路径
        '''

        path1 = os.path.abspath('..')
        path2=path1+'/datas/data/predict_data'
        self.mkdir(path2)
        # print(path1)
        # print(path1)
        rootdir = filepath
        tree = ET.parse(filepath)
        root = tree.getroot()
        count = 0
        uuid_str = uuid.uuid4().hex
        for item in root.findall('item'):
            reponse_text=item.findall('response')
            templist=itemlist[count].responses
            for i in range(len(reponse_text)):

                reponse_text[i].text = templist[i]

            tree.write(path2+'/new'+uuid_str+os.path.basename(filepath))
            count += 1


    def mkdir(self,path1):
        isExists=os.path.exists(path1)
        if not isExists:
            #b不存在路径就创建
            os.makedirs(path1)




def main():
    # print("是否执行此程序")
    # command = input()
    path1 = os.path.abspath('..')
    print(path1)
    filepath = path1+'/datas/data/1/001_normalTest/com.xml'
    #filepath='C:\\Users\\Thinkpad\\PycharmProjects\\TestCaseGeneration_HUAWEI_12_3\\SameTPSGeneration_Demo\\datas\\data\\test\\0new.xml'
    uuid_str = uuid.uuid4().hex
    #getxml = GetXML()
    # print(os.path.basename(filepath))
    # itemlist=getxml.read_file(filepath)
    # print(os.path.basename(filepath))
    # print(path1+'/datas/data/new'+uuid_str+os.path.basename(filepath))
    get_xml =GetXML()
    itemlist = get_xml.read_file(filepath)
    #itemlist = GetXML.read_file(filepath)
    writeback= WriteBack()
    writeback.newxml(itemlist, filepath)




if __name__=='__main__':
    main()