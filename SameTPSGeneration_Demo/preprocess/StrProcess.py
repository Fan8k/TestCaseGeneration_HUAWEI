import re
'''
str1:传入需要处理的字符串
flag：是否需要进行'...'的去除，1为去除，0为不去除
'''
class StrProcess:
    def str_process(self, str1, flag):
        resStr = ''
        if str1 != None:
            if str1.find('\n') != -1 or str1.find('..') != -1:
                if flag == 1:
                    '''
                    去'..'只保留一个点
                    '''
                    response_content = str1.replace('\n', '\\n')
                    p = re.compile(r"[|\D](\.+)\D")
                    for com in p.finditer(response_content):
                        mm = com.group()
                        if mm[0] == '.':
                            response_content = response_content.replace(mm, mm.replace(".", "", len(mm) - 2), 1)
                        else:
                            response_content = response_content.replace(mm, mm.replace(".", "", len(mm) - 3), 1)

                    #         print ("sen_back:", sen, '\n')
                    #print(response_content)
                    #response_content = p.sub("", response_content)

                    resStr = resStr + response_content
                else:
                    '''
                    不去除'..'
                    '''
                    response_content = str1.replace('\n', '\\n')
                    resStr = resStr + response_content

            else:
                resStr = resStr + str1

        else:
            resStr = resStr + 'None'
        return resStr