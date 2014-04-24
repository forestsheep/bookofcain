# encoding: UTF-8
'''
Created on 2014年4月21日

@author: bxu
'''

import re

#############
#返回命令的类型
#-1 不认识的命令
# 1 输入的是battle net tag
# 2 输入的是纯数字
#############
def commando(command):
    ptnBnTag = re.compile(r'(?u)\w+#\d+')
    matchBnTag = ptnBnTag.match(command)
    ptnNumber = re.compile(r'^\d+$')
    matchNumber = ptnNumber.match(command)
    if matchBnTag:
        return 1
    if matchNumber:
        return 2
    return -1
    