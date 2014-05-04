# encoding: UTF-8

import re

#############
#返回命令的类型
#-1 不认识的命令
# 0 help
# 1 输入的是battle net tag
# 2 输入的是纯数字
# 3 输入的是‘skill’　or 'build'
# 101 - 200 装备
#############
def commando(command):
    ptnHelp = re.compile(ur'^(?i)help|^\?|^？')
    matchHelp = ptnHelp.match(command)
    if matchHelp:
        return 900
    ptnHelpEquip = re.compile(ur'^(?i)equip|^装备$')
    matchEquip = ptnHelpEquip.match(command)
    if matchEquip:
        return 901
    ptnBnTag = re.compile(r'(?u)\w+#\d+')
    matchBnTag = ptnBnTag.match(command)
    if matchBnTag:
        return 1
    ptnNumber = re.compile(r'^\d+$')
    matchNumber = ptnNumber.match(command)
    if matchNumber:
        return 2
    ptnSkill = re.compile(ur'^(?i)skills{0,1}$|^(?i)build$|^技能$')
    matchSkill = ptnSkill.match(command)
    if matchSkill:
        return 3
    ptnItemHead = re.compile(ur'^(?i)head$|^头部{0,1}$|^頭$|^帽子{0,1}$')
    matchItemHead = ptnItemHead.match(command)
    if matchItemHead:
        return 101
    ptnItemNeck = re.compile(ur'^(?i)neck(lace){0,1}$|^(?i)amulet$|^护身符$|^项链{0,1}$|^头{0,1}颈部{0,1}$|^脖子{0,1}$')
    matchItemNeck = ptnItemNeck.match(command)
    if matchItemNeck:
        return 102
    ptnItemShoulder = re.compile(ur'^(?i)shoulders{0,1}$|^护{0,1}肩膀{0,1}甲{0,1}$')
    matchItemShoulder = ptnItemShoulder.match(command)
    if matchItemShoulder:
        return 103
    ptnItemTorso = re.compile(ur'^(?i)torso$|^(?i)chest$|^cloth(es){0,1}$|^胸甲{0,1}部{0,1}$|^上{0,1}衣服{0,1}$')
    matchItemTorso = ptnItemTorso.match(command)
    if matchItemTorso:
        return 104
    ptnItemBracers = re.compile(ur'^(?i)bracers$|^护{0,1}腕部{0,1}$|^手腕$')
    matchItemBracers = ptnItemBracers.match(command)
    if matchItemBracers:
        return 105
    ptnItemHands = re.compile(ur'^(?i)hands{0,1}$|^(?i)gloves{0,1}$|^手套$')
    matchItemHands = ptnItemHands.match(command)
    if matchItemHands:
        return 106
    ptnItemLeftFinger = re.compile(ur'^(?i)leftfinger$|^(?i)finger1$|^(left){0,1}ring1{0,1}$|^左手{0,1}戒指{0,1}$|^左{0,1}手指1{0,1}$|^左指$|^戒指{0,1}1{0,1}$')
    matchItemLeftFinger = ptnItemLeftFinger.match(command)
    if matchItemLeftFinger:
        return 107
    ptnItemRightFinger = re.compile(ur'^(?i)rightfinger$|^(?i)finger2$|^(right){0,1}ring2{0,1}$|^右手{0,1}戒指{0,1}$|^手指2$|^右手指$|^右指$|^戒指{0,1}2$')
    matchItemRightFinger = ptnItemRightFinger.match(command)
    if matchItemRightFinger:
        return 108
    ptnItemMainHand = re.compile(ur'^(?i)mainhand$|^(?i)hand1$|^(?i)weapon1{0,1}$|^主手$|^武器1{0,1}$')
    matchItemMainHand = ptnItemMainHand.match(command)
    if matchItemMainHand:
        return 109
    ptnItemOffHand = re.compile(ur'^(?i)offhand$|^(?i)hand2$|^(?i)weapon2$|^副手$|^武器2$')
    matchItemOffHand = ptnItemOffHand.match(command)
    if matchItemOffHand:
        return 110
    ptnItemWaist = re.compile(ur'^(?i)waist$|^(?i)belt$|^腰带{0,1}$|^皮带$|^腰部$')
    matchItemWaist = ptnItemWaist.match(command)
    if matchItemWaist:
        return 111
    ptnItemLegs = re.compile(ur'^(?i)legs{0,1}$|^(?i)pants$|^(?i)trousers$|^腿部{0,1}$|^裤子{0,1}$')
    matchItemLegs = ptnItemLegs.match(command)
    if matchItemLegs:
        return 112
    ptnItemFeet = re.compile(ur'^(?i)feet$|^foots{0,1}$|^(?i)boots$|^(?i)shoes$|^靴子{0,1}$|^脚$|^鞋子{0,1}$')
    matchItemFeet = ptnItemFeet.match(command)
    if matchItemFeet:
        return 113
    return -1
    