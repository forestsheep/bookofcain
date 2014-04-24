# encoding: UTF-8
import stringutil

def echoHeroStatus(statusDict):
    outputKeys = ({'damage':u'伤害'},
                  {'armor':u'护甲'},
                  {'life':u'生命'},
                  {'physicalResist':u'物防'},
                  {'fireResist':u'火防'},
                  {'coldResist':u'冷防'},
                  {'lightningResist':u'电防'},
                  {'arcaneResist':u'秘防'},
                  {'poisonResist':u'毒防'})
    rtn = ''
    for i in range(len(outputKeys)):
        dict1 = outputKeys[i]
        list1 = dict1.keys()
        key = list1[0]
        zhname = dict1[key]
        line = zhname + ":" + str(statusDict[key])
        rtn = stringutil.appendLines(rtn, line)
    return rtn
