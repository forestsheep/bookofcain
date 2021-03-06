# encoding: UTF-8
import stringutil

def echoHeroStatus(statusDict):
    outputKeys = ({'damage':u'傷害'},
                  {'attackSpeed':u'攻速'},
                  {'critDamage':u'爆傷'},
                  {'critChance':u'爆率'}, 
                  {'toughness':u'坚韧'},
                  {'armor':u'護甲'},
                  {'life':u'生命'},
                  {'physicalResist':u'物防'},
                  {'fireResist':u'火防'},
                  {'coldResist':u'冷防'},
                  {'lightningResist':u'電防'},
                  {'arcaneResist':u'秘防'},
                  {'poisonResist':u'毒防'},
                  {'lifeOnHit':u'擊回'},
                  {'lifePerKill':u'殺回'})
    rtn = ''
    for i in range(len(outputKeys)):
        dict1 = outputKeys[i]
        list1 = dict1.keys()
        key = list1[0]
        zhname = dict1[key]
        line = zhname + ":" + str(statusDict[key])
        rtn = stringutil.appendLines(rtn, line)
    return rtn

def getItemKey(itemid):
    itemDict = {
        '101':'head',
        '102':'neck',
        '103':'shoulders',
        '104':'torso',
        '105':'bracers',
        '106':'hands',
        '107':'leftFinger',
        '108':'rightFinger',
        '109':'mainHand',
        '110':'offHand',
        '111':'waist',
        '112':'legs',
        '113':'feet'
    }
    itemString = str(itemid)
    if itemString in itemDict :
        return itemDict[itemString]
    else :
        return None

def getClassId(className):
    classDict = {
        'barbarian':1,
        'crusader':2,
        'demon-hunter':3,
        'monk':4,
        'witch-doctor':5,
        'wizard':6,
    }
    try:
        id = classDict[className]
        return id
    except:
        return -1

def getRegionName(regionId):
    regionDict = {
        'kr':u'亞服',
        'tw':u'亞服',
        'us':u'美服',
        'eu':u'歐服'
    }
    try:
        id = regionDict[regionId]
        return id
    except:
        return u'未知服'