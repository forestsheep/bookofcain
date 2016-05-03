# encoding: UTF-8

import stringutil
import httplib
import json
import sqlquery
import logsql
import herostatus
import httperror
import bs4
import urllib2

def echoHeroDetail(battlenettagString, region, hreoid):
    try:
        httpsClient = httplib.HTTPSConnection(region + '.api.battle.net', 80, timeout=30)
        httpsClient.request('GET','/d3/profile/' + battlenettagString.replace('#','-') + '/hero/' + hreoid + '?locale=ZH_TW&apikey=vkdwrvv5kan62fd7qdhu35z2z4tt6cad')
        logsql.log('/api/d3/profile/' + battlenettagString.replace('#','-') + '/hero/' + hreoid + '?locale=ZH_TW')
        response = httpsClient.getresponse()
        jsonString = response.read()
        resultJson = json.loads(jsonString)
        herodetail = resultJson.get(u'stats')
        heroname = resultJson.get(u'name')
        heroclass = resultJson.get(u'class')
        herolv = str(resultJson.get(u'level'))
        killsDict = resultJson.get(u'kills')
        modeBool = resultJson.get(u'hardcore')
        paragonInt = resultJson.get(u'paragonLevel')
        seasonalBool = resultJson.get(u'seasonal')
        o = heroname + ' [' + heroclass + '] [' + herolv + ']'
        o = stringutil.appendLines(o, u'模式:' + ('hardcore' if modeBool else 'softcore'))
        o = stringutil.appendLines(o, u'巔峰等級:' + str(paragonInt))
        o = stringutil.appendLines(o, u'赛季英雄:' + (u'是' if seasonalBool else u'否'))
        if u'elites' in killsDict:
            elitesKill = str(killsDict[u'elites'])
            o = stringutil.appendLines(o, u'精英擊殺:' + elitesKill)
        o = stringutil.appendLines(o, herostatus.echoHeroStatus(herodetail))
        legendaryPowersList = resultJson.get(u'legendaryPowers')
        logsql.log(str(legendaryPowersList))
        o = stringutil.appendLines(o, u"萃取:")
        for i in range(len(legendaryPowersList)):
                powername = ''
                if legendaryPowersList[i] == None:
                    powerName = u'無'
                    continue
                powerName = legendaryPowersList[i].get(u'name')
                if powerName == None:
                    powerName = u'無'
                o = o + powerName + ";"
        return o
    except Exception, e:
        logsql.log('echoHeroDetail Error:' + str(e) + jsonString + battlenettagString)
    finally:
        if httpsClient:
            httpsClient.close()

def echoYourHeroes(cursor, battlenettagString):
    # 先删除现有英雄
    error = sqlquery.delHeroes(cursor, battlenettagString)
    rtnString = ''
    echoString = ''
    try:
        rtnString = echoYourHeroesByServer(cursor, battlenettagString, 'kr', u'亚服')
        if rtnString != '':
            echoString = u'亚服'
        if rtnString == None or rtnString == '':
            rtnString = echoYourHeroesByServer(cursor, battlenettagString, 'us', u'美服')
            if rtnString != '':
                echoString = u'美服'
        if rtnString == None or rtnString == '':
            rtnString = echoYourHeroesByServer(cursor, battlenettagString, 'eu', u'欧服')
            if rtnString != '':
                echoString = u'欧服'
        echoString = stringutil.appendLines(echoString, rtnString)
        heroesTuple = sqlquery.getHeroes(cursor, battlenettagString)
        for heroRow in heroesTuple:
            heroId = heroRow[0]
            heroName = heroRow[1]
            heroClass = heroRow[2]
            heroLv = heroRow[3]
            heroRegionId = heroRow[4]
            heroRegionName = herostatus.getRegionName(heroRegionId)
            echoString = stringutil.appendLines(echoString, str(heroId) + ' ' + heroName + ' ' + str(heroLv) + u'級' + heroClass)
    except httperror.HttpError, he:
        logsql.writeLog(cursor, 'echoYourHeroes Error:' + str(he))
        return u'battle.net繁忙，请稍后再试。'
    except Exception, e:
        return str(e)
    if echoString != '':
        echoString = stringutil.appendLines(echoString, u'输入编号查询英雄状态')
    return echoString

def echoYourHeroesByServer(cursor, battlenettagString, region, regionName):
    jsonString = ''
    try:
        httpsClient = httplib.HTTPSConnection(region + '.api.battle.net', 80, timeout=30)
        httpsClient.request('GET','/d3/profile/' + battlenettagString.replace('#','-') + '/?locale=zh_TW&apikey=vkdwrvv5kan62fd7qdhu35z2z4tt6cad')
        response = httpsClient.getresponse()
        # if response.status != 200:
        logsql.writeLog(cursor, 'status code is:' + str(response.status))
        #     raise httperror.HttpError('not 200')
        jsonString = response.read()
        logsql.writeLog(cursor, jsonString)
        resultJson = json.loads(jsonString)
        errorcode = resultJson.get(u'code')
        rtnString = ''
        if errorcode == None:
            guildString = resultJson.get(u'guildName')
            # logsql.log(guildString)
            rtnString = u'氏族:' + guildString
            rtnString = stringutil.appendLines(rtnString, u'巔峰:' + str(resultJson.get(u'paragonLevel')))
            rtnString = stringutil.appendLines(rtnString, u'专家巔峰:' + str(resultJson.get(u'paragonLevelHardcore')))
            rtnString = stringutil.appendLines(rtnString, u'赛季巔峰:' + str(resultJson.get(u'paragonLevelSeason')))
            rtnString = stringutil.appendLines(rtnString, u'赛季专家巔峰:' + str(resultJson.get(u'paragonLevelSeasonHardcore')))
            # rtnString = u'您在' + regionName + u'有以下英雄'
            heroList = resultJson.get(u'heroes')
            for i in range(len(heroList)):
                heroid = heroList[i].get(u'id')
                heroName = heroList[i].get(u'name')
                heroClass = heroList[i].get('class')
                heroLv = heroList[i].get('level')
                heroClassId = herostatus.getClassId(heroClass)
                error = sqlquery.saveHeroes(cursor, battlenettagString, region, heroid, heroName, heroClassId, heroLv)
                res = sqlquery.getHeroesSeq(cursor, battlenettagString, region, heroid)
                # rtnString = rtnString + '\n' +str(res[0][0]) + ') ' + heroList[i].get(u'name') + u' ' + heroList[i].get('class') + u' lv' + str(heroList[i].get('level'))
        elif errorcode == u'NOTFOUND':
            return u''
        return rtnString
    except httperror.HttpError, he:
        logsql.writeLog(cursor, 'echoYourHeroesByServer Error:' + str(he))
        raise he
    except Exception, e:
        logsql.writeLog(cursor, 'echoYourHeroesByServer Error:' + str(e))
        return ''
    finally:
        if httpsClient:
            httpsClient.close()

def echoHeroSkills(battlenettagString, region, hreoid):
    try:
        httpsClient = httplib.HTTPSConnection(region + '.api.battle.net', 80, timeout=30)
        httpsClient.request('GET','/d3/profile/' + battlenettagString.replace('#','-') + '/hero/' + hreoid + '?locale=ZH_TW&apikey=vkdwrvv5kan62fd7qdhu35z2z4tt6cad')
        response = httpsClient.getresponse()
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
        if httpsClient:
            httpsClient.close()

def echoHeroItem(battlenettagString, region, hreoid, itemId):
    rtnString = None
    try:
        httpsClient = httplib.HTTPSConnection(region + '.api.battle.net', 80, timeout=30)
        httpsClient.request('GET','/d3/profile/' + battlenettagString.replace('#','-') + '/hero/' + hreoid + '?locale=ZH_TW&apikey=vkdwrvv5kan62fd7qdhu35z2z4tt6cad')
        responseHero = httpsClient.getresponse()
        logsql.log(str(responseHero.status))
        if responseHero.status != 200:
            raise httperror.HttpError('not 200')
        jsonHeroString = responseHero.read()
        resultHeroJson = json.loads(jsonHeroString)
        itemsDict = resultHeroJson[u'items']
        itemDict = itemsDict[herostatus.getItemKey(itemId)]
        tooptipString = itemDict[u'tooltipParams']
        
        httpsClient.request('GET','/d3/data/' + tooptipString + '?locale=ZH_TW')
        responseItem = httpsClient.getresponse()
        logsql.log(str(responseHero.status))
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
        attributesRawDict = resultItemJson[u'attributesRaw']
        socketMinInt = 0
        if u'Sockets' in attributesRawDict:
            socketsDict = attributesRawDict[u'Sockets']
            socketMinInt = int(socketsDict[u'min'])
        emptySocketInt = socketMinInt - len(gemList)
        for socketCount in range(0, emptySocketInt):
            rtnString = stringutil.appendLines(rtnString, u'○ 空的鑲孔' )
        if u'set' in resultItemJson:
            setDict = resultItemJson[u'set']
            setNameString = setDict[u'name']
            rtnString = stringutil.appendLines(rtnString, setNameString)
            setItemList = setDict[u'items']
            for setItemDict in setItemList:
                setItemNameString = setItemDict[u'name']
                rtnString = stringutil.appendLines(rtnString, '    ' + setItemNameString)
            setRankList = setDict[u'ranks']
            for setRankDict in setRankList:
                requiredString = str(setRankDict[u'required'])
                rtnString = stringutil.appendLines(rtnString, '(' + requiredString + u')件')
                rankAttributeDict = setRankDict[u'attributes']
                atbPrimaryList = rankAttributeDict[u'primary']
                for primaryDict in atbPrimaryList:
                    rtnString = stringutil.appendLines(rtnString, '    ' + primaryDict[u'text'])
                atbSecondaryList = rankAttributeDict[u'secondary']
                for secondaryDict in atbSecondaryList:
                    rtnString = stringutil.appendLines(rtnString, '    ' + secondaryDict[u'text'])
                atbpassiveList = rankAttributeDict[u'passive']
                for passiveDict in atbpassiveList:
                    rtnString = stringutil.appendLines(rtnString, '    ' + passiveDict[u'text'])
        if u'flavorText' in resultItemJson:
            flavorString = resultItemJson[u'flavorText']
            rtnString = stringutil.appendLines(rtnString, flavorString)
        return rtnString
    except httperror.HttpError, he:
        logsql.log('echoHeroItem Error:' + str(he))
        return u'battle.net繁忙，请稍后再试。'
    except KeyError, ke:
        return rtnString
    except Exception, e:
        pass
    finally:
        if httpsClient:
            httpsClient.close()

def echoHeroRank(battlenettagString, heroId, heroName):
    bntagString = battlenettagString.replace('#','-')
    pageString = "http://www.diabloprogress.com/hero/" + bntagString + "/" + heroName + "/" + heroId
    page = urllib2.urlopen(url = pageString, data = 'update=1')
    page = urllib2.urlopen(pageString).read()
    if page == '':
        return u'你的账号从未收录在diablo progress中。正在找对策可以自动请求收录。在没有找到对策之前，您可以手动登录http://www.diabloprogress.com来请求收录您的排名。'

    soup = bs4.BeautifulSoup(page)
    fd = soup.findAll(attrs={'style':'background-color:#1C1C1C;padding:10px;margin-top:7px;margin-right:2px'})
    lastCheckedKeyString = 'Last Checked: '
    fdLastCheckedTag = soup.find(text = lastCheckedKeyString).findNext('dd')
    rtnString = ''
    for item in fd:
        ch = item.children
        for i in ch:
            try:
                rtnString = stringutil.appendLines(rtnString, i.text)
            except:
                pass
    rtnString = stringutil.appendLines(rtnString, lastCheckedKeyString + fdLastCheckedTag.text)
    return rtnString

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