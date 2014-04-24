# coding: UTF-8
def appendLines(source, target):
    if source == None or source == '' :
        return target
    if target != '':
        return source +'\n' + target
    else:
        return source