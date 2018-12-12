import xml.etree.ElementTree as ET
import sys
import os
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.DataMatcher import DataMatcher
from services.ExtractRuler import ExtractRuler
from utils.ExtractLocationInfo import ExtractLocationInfo
from services.RuleDecorater import RuleDecorater
from services.RuleMerger import RuleMerger
from interactions.Predict import Predict
from models.Item import Item

class WriteBack():
    def newxml(self,itemlist[],filepath):
        '''
        itemlist[]：传入itemlist集合
        filepath：传入的原型xml的完整路径
        '''

        path1 = os.path.abspath('..')
        # print(path1)
        rootdir = filepath
        tree = ET.parse(filepath)
        root = tree.getroot()
        count = 0
        for item in root.findall('item'):
            reponse_text=item.findall('response')
            templist=itemlist[count].reponses
            for i in range(len(reponse_text)):
                reponse_text[i].text=templist[i]
            tree.write(path1+'\\new'+os.path.basename(filepath))
            count+=1