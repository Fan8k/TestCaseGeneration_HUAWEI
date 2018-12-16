#coding=utf-8
with open('data.tsv','w+',encoding="utf8")as t:
 with open('meta_data.tsv', 'w+', encoding="utf8")as m:
   with open("one.txt",'r',encoding='utf8')as f:
     for line in f.readlines():
        #print(line)
        line_list = line.strip('\n').split(" ")#去掉str左右端的空格并以空格分割成list
        tsv_list = '\t'.join(line_list[1:])
        print(tsv_list)
        t.write(tsv_list+'\n')
        m.write(line_list[0]+"\n")
