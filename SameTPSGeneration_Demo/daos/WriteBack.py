import xml.etree.ElementTree as ET
import sys
import os
import uuid
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class WriteBack():
    def newxml(self,itemlist=[],filepath=None):
        '''
        itemlist[]：传入itemlist集合
        filepath：传入的原型xml的完整路径
        '''

        path1 = os.path.abspath('..')
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

                reponse_text[i].text=templist[i]

            tree.write(path1+'datas\\data\\new'+uuid_str+os.path.basename(filepath))
            count+=1

def main():
    # print("是否执行此程序")
    # command = input()
    path1 = os.path.abspath('..')
    print(path1)
    # writeback= WriteBack()
    # writeback.newxml()




if __name__=='__main__':
    main()