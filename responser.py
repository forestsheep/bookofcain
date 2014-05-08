# encoding: UTF-8

import stringutil
import httplib
import json
import sqlquery
import logsql
import herostatus
import httperror

def echoHeroDetail(battlenettagString, region, hreoid):
    try:
        httpClient = httplib.HTTPConnection(region + '.battle.net', 80, timeout=30)
        httpClient.request('GET','/api/d3/profile/' + battlenettagString.replace('#','-') + '/hero/' + hreoid)
        response = httpClient.getresponse()
        jsonString = response.read()
        resultJson = json.loads(jsonString)
        herodetail = resultJson.get(u'stats')
        heroname = resultJson.get(u'name')
        heroclass = resultJson.get(u'class')
        herolv = str(resultJson.get(u'level'))
        killsDict = resultJson.get(u'kills')
        modeBool = resultJson.get(u'hardcore')
        paragonInt = resultJson.get(u'paragonLevel')
        o = heroname + ' [' + heroclass + '] [' + herolv + ']'
        o = stringutil.appendLines(o, u'模式:' + ('hardcore' if modeBool else 'softcore'))
        o = stringutil.appendLines(o, u'巔峰等級:' + str(paragonInt))
        if u'elites' in killsDict:
            elitesKill = str(killsDict[u'elites'])
            o = stringutil.appendLines(o, u'精英擊殺:' + elitesKill)
        o = stringutil.appendLines(o, herostatus.echoHeroStatus(herodetail))
        return o
    except Exception, e:
        logsql.log('echoHeroDetail Error:' + str(e))
    finally:
        if httpClient:
            httpClient.close()

def echoYourHeroes(cursor, battlenettagString):
    # 先删除现有英雄
    error = sqlquery.delHeroes(cursor, battlenettagString)
    rtnString = ''
    try:
        rtnString = echoYourHeroesByServer(cursor, battlenettagString, 'tw', u'亚服')
        usString = echoYourHeroesByServer(cursor, battlenettagString, 'us', u'美服')
        rtnString = stringutil.appendLines(rtnString, usString)
        euString = echoYourHeroesByServer(cursor, battlenettagString, 'eu', u'欧服')
        rtnString = stringutil.appendLines(rtnString, euString)
    except httperror.HttpError, he:
        return u'battle.net繁忙，请稍后再试。'
    if rtnString != '':
        rtnString = stringutil.appendLines(rtnString, u'输入编号查询英雄状态')
    else:
        rtnString = u'没找到您的账号，请确认输入的是正确的战网TAG'
    return rtnString

def echoYourHeroesByServer(cursor, battlenettagString, region, regionName):
    jsonString = ''
    try:
        httpClient = httplib.HTTPConnection(region + '.battle.net', 80, timeout=30)
        httpClient.request('GET','/api/d3/profile/' + battlenettagString.replace('#','-') + '/')
        response = httpClient.getresponse()
        if response.status != 200:
            raise httperror.HttpError('not 200')
        jsonString = response.read()
        resultJson = json.loads(jsonString)
        errorcode = resultJson.get(u'code')
        if errorcode == None:
            rtnString = u'您在' + regionName + u'有以下英雄'
            heroList = resultJson.get(u'heroes')
            for i in range(len(heroList)):
                heroid = heroList[i].get(u'id')
                error = sqlquery.saveHeroes(cursor, battlenettagString, region, heroid)
                res = sqlquery.getHeroesSeq(cursor, battlenettagString, region, heroid)
                rtnString = rtnString + '\n' +str(res[0][0]) + ') ' + heroList[i].get(u'name') + u' ' + heroList[i].get('class') + u' lv' + str(heroList[i].get('level'))
        elif errorcode == u'NOTFOUND':
            return ''
        return rtnString
    except httperror.HttpError, he:
        raise he
    except Exception, e:
        logsql.writeLog(cursor, 'echoYourHeroesByServer Error:' + str(e))
        pass
    finally:
        if httpClient:
            httpClient.close()

def echoHeroSkills(battlenettagString, region, hreoid):
    try:
        httpClient = httplib.HTTPConnection(region + '.battle.net', 80, timeout=30)
        httpClient.request('GET','/api/d3/profile/' + battlenettagString.replace('#','-') + '/hero/' + hreoid)
        response = httpClient.getresponse()
        if response.status != 200:
            raise httperror.HttpError('not 200')
        jsonString = response.read()
        resultJson = json.loads(jsonString)
        heroname = resultJson.get(u'name')
        skillsDict = resultJson.get(u'skills')
        rtnString = heroname
        rtnString = stringutil.appendLines(rtnString, u'主动技能：')
        activeList = skillsDict[u'active']
        for eleDict in activeList:
            if u'skill' in eleDict:
                skillDict = eleDict[u'skill']
                rtnString = stringutil.appendLines(rtnString, skillDict[u'name'])
            if u'rune' in eleDict:
                runeDict = eleDict[u'rune']
                rtnString = rtnString + u'[' + runeDict[u'name'] + u']'
        passiveList = skillsDict[u'passive']
        rtnString = stringutil.appendLines(rtnString, u'被动技能：')
        for eleDict in passiveList:
            if u'skill' in eleDict:
                skillDict = eleDict[u'skill']
                rtnString = stringutil.appendLines(rtnString, skillDict[u'name'])
        return rtnString
    except httperror.HttpError, he:
        return u'battle.net繁忙，请稍后再试。'
    except KeyError, ke:
        return rtnString
    except Exception, e:
        logsql.log('echoHeroSkills Error:' + str(e))
    finally:
        if httpClient:
            httpClient.close()

def echoHeroItem(battlenettagString, region, hreoid, itemId):
    rtnString = None
    try:
        httpClient = httplib.HTTPConnection(region + '.battle.net', 80, timeout=30)
        httpClient.request('GET','/api/d3/profile/' + battlenettagString.replace('#','-') + '/hero/' + hreoid)
        responseHero = httpClient.getresponse()
        if responseHero.status != 200:
            raise httperror.HttpError('not 200')
        jsonHeroString = responseHero.read()
        resultHeroJson = json.loads(jsonHeroString)
        itemsDict = resultHeroJson[u'items']
        itemDict = itemsDict[herostatus.getItemKey(itemId)]
        tooptipString = itemDict[u'tooltipParams']
        
        httpClient.request('GET','/api/d3/data/' + tooptipString)
        responseItem = httpClient.getresponse()
        if responseItem.status != 200:
            raise httperror.HttpError('not 200')
        jsonItemString = responseItem.read()
        resultItemJson = json.loads(jsonItemString)
        rtnString = resultItemJson[u'name']
        rtnString = stringutil.appendLines(rtnString, resultItemJson[u'typeName'])
        isWeapon = u'dps' in resultItemJson
        if isWeapon:
            dpsDict = resultItemJson[u'dps']
            minFloat = dpsDict[u'min']
            maxFloat = dpsDict[u'max']
            dpsFloat = (minFloat + maxFloat) / 2
            dpsString = str(round(dpsFloat, 1))
            rtnString = stringutil.appendLines(rtnString, dpsString)
            rtnString = stringutil.appendLines(rtnString, u'每秒傷害')
            if u'minDamage' in resultItemJson:
                minDamageDict = resultItemJson[u'minDamage']
                minminFloat = minDamageDict[u'min']
                minmaxFloat = minDamageDict[u'max']
                minFloat = (minminFloat + minmaxFloat) / 2
                minString = str(int(minFloat))
                rtnString = stringutil.appendLines(rtnString, minString)
            if u'maxDamage' in resultItemJson:
                maxDamageDict = resultItemJson[u'maxDamage']
                maxminFloat = maxDamageDict[u'min']
                maxmaxFloat = maxDamageDict[u'max']
                maxFloat = (maxminFloat + maxmaxFloat) / 2
                maxString = str(int(maxFloat))
                rtnString = rtnString + '-' + maxString + u'點傷害'
            if u'attacksPerSecond' in resultItemJson:
                apsDict = resultItemJson[u'attacksPerSecond']
                minFloat = apsDict[u'min']
                maxFloat = apsDict[u'max']
                apsFloat = (minFloat + maxFloat) / 2
                apsString = str(round(apsFloat, 2))
                rtnString = stringutil.appendLines(rtnString, u'每秒攻擊次數：')
                rtnString = rtnString + apsString

        if u'armor' in resultItemJson:
            armorDict = resultItemJson[u'armor']
            minFloat = armorDict[u'min']
            maxFloat = armorDict[u'max']
            armorFloat  = (minFloat + maxFloat) / 2
            armorString = str(int(armorFloat))
            rtnString = stringutil.appendLines(rtnString, armorString)
            rtnString = stringutil.appendLines(rtnString, u'護甲值')
        attributesDict = resultItemJson[u'attributes']
        if u'primary' in attributesDict:
            primaryList = attributesDict[u'primary']
            if len(primaryList) > 0 :
                rtnString = stringutil.appendLines(rtnString, u'主要属性')
            for itemDict in primaryList:
                rtnString = stringutil.appendLines(rtnString, echoAff(itemDict) + itemDict[u'text'])
        if u'secondary' in attributesDict:
            secondaryList = attributesDict[u'secondary']
            if len(secondaryList) > 0 :
                rtnString = stringutil.appendLines(rtnString, u'次要属性')
            for itemDict in secondaryList:
                rtnString = stringutil.appendLines(rtnString, echoAff(itemDict) + itemDict[u'text'])
        if u'passive' in attributesDict:
            passiveList = attributesDict[u'passive']
            if len(passiveList) > 0 :
                rtnString = stringutil.appendLines(rtnString, u'被动属性')
            for itemDict in passiveList:
                rtnString = stringutil.appendLines(rtnString, echoAff(itemDict) + itemDict[u'text'])
        gemList = resultItemJson[u'gems']
        for gemDict in gemList:
            itemDict = gemDict[u'item']
            nameString = u'● ' + itemDict[u'name']
            rtnString = stringutil.appendLines(rtnString, nameString)
            attributesDict = gemDict[u'attributes']
            primaryList = attributesDict[u'primary']
            for primaryItemDict in primaryList:
                rtnString = stringutil.appendLines(rtnString, '   ' + primaryItemDict[u'text'])
            secondaryList = attributesDict[u'secondary']
            for secondaryItemDict in secondaryList:
                rtnString = stringutil.appendLines(rtnString, '   ' + secondaryItemDict[u'text'])
            passiveList = attributesDict[u'passive']
            for passiveItemDict in passiveList:
                rtnString = stringutil.appendLines(rtnString, '   ' + passiveItemDict[u'text'])
        if u'flavorText' in resultItemJson:
            flavorString = resultItemJson[u'flavorText']
            rtnString = stringutil.appendLines(rtnString, flavorString)
        return rtnString
    except httperror.HttpError, he:
        return u'battle.net繁忙，请稍后再试。'
    except KeyError, ke:
        return rtnString
    except Exception, e:
        logsql.log('echoHeroItem Error:' + str(e))
    finally:
        if httpClient:
            httpClient.close()

def echoAff(itemDict):
    affString = itemDict[u'affixType']
    if affString == 'default' :
        return u'☆ '
    elif affString == 'enchant' :
        return u'卐 '
    elif affString == 'utility' :
        return u'★ '
    else :
        return '  '