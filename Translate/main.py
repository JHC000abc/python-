#!/usr/bin/env python
# encoding: utf-8
'''
@author: JHC
@license: None
@contact: JHC000abc@gmail.com
@file: main.py
@time: 2022/1/21 18:36
@desc:
'''
import os

lst = os.listdir(os.getcwd())

for c in lst:
    if os.path.isfile(c) and c.endswith('.py') and c.find("main") == -1:  # 去掉AllTest.py文件
        print(c)
        os.system(os.path.join(os.getcwd(), c))  # E:\Python\mytest.py

os.remove('./annotation.txt')
os.remove('./tran_result.txt')