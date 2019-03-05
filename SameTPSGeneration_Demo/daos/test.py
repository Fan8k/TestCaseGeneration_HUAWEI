

class test():
    def __init__(self):
        self.filecount = 0

    def newxml(self):
        temp=self.filecount
        for i in range(5):
            self.filecount+=1
            print(self.filecount)
        for j in range(temp,self.filecount):
            print("tmp:",j+1)
def main():

    get_xml = test()
    for i in range(5):
        get_xml.newxml()
    # itemlist,comlist = get_xml.read_file(filepath)
    # writeback = WriteBack()
    # writeback.newxml(itemlist, filepath, comlist)


if __name__=='__main__':
    main()