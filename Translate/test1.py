#!/usr/bin/env python
# encoding: utf-8
'''ahjkfhka'''
import re

with open('./test.py','r',encoding='utf-8') as fp:
    code = fp.read()
    # print(code)
    regex = "[']{3}\D*[']{3}"
    # print(regex)
    annotation_list = re.findall(regex,code)
    # print(annotation_list)
    for i in annotation_list:
        # print(str(i).replace("[']{3}",""))
        with open('./annotation.txt','a',encoding='utf-8') as fp:
            fp.write(re.sub("[']{3}",'',str(i)).replace('\n','').replace('        ','').replace('    ','\n'))

print('注释读取成功')


