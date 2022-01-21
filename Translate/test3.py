#!/usr/bin/env python
# encoding: utf-8
'''
@author: JHC
@license: None
@contact: JHC000abc@gmail.com
@file: 将英文填写回源代码处.py
@time: 2022/1/21 18:26
@desc:
'''

import re


with open('./tran_result.txt','r',encoding='utf-8')as fp:
    word_list = fp.readlines()
for i in word_list:
    with open('./test.py','r',encoding='utf-8') as fp:
        code = fp.read()
        # print(code)
        regex = "[']{3}\D*[']{3}"
        # print(regex)
        word = re.sub(regex,"\'\'\'\\n\\t\\t"+str(i)+"\\t\\t\'\'\'",code)
        # print(word)
        with open('./result.py','w',encoding='utf-8')as fp:
            fp.write(word)
print('注释写入成功,文件夹路径为"./result.py"')