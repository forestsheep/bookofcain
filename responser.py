# encoding: UTF-8

import stringutil
import httplib
import json
import sqlquery
import logsql
import herostatus

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
        o = heroname + ' [' + heroclass + '] [' + herolv + ']'
        o = stringutil.appendLines(o, herostatus.echoHeroStatus(herodetail))
        return o
    except Exception, e:
        pass
    finally:
        if httpClient:
            httpClient.close()

def echoYourHeroes(cursor, battlenettagString):
    # 先删除现有英雄
    error = sqlquery.delHeroes(cursor, battlenettagString)
    rtnString = echoYourHeroesByServer(cursor, battlenettagString, 'tw', u'亚服')
    usString = echoYourHeroesByServer(cursor, battlenettagString, 'us', u'美服')
    rtnString = stringutil.appendLines(rtnString, usString)
    euString = echoYourHeroesByServer(cursor, battlenettagString, 'eu', u'欧服')
    rtnString = stringutil.appendLines(rtnString, euString)
    if rtnString != '':
        rtnString = stringutil.appendLines(rtnString, u'输入编号查询英雄状态')
    else:
        rtnString = u'没找到您的账号，请确认输入的是正确的战网TAG'
    return rtnString

def echoYourHeroesByServer(cursor, battlenettagString, region, regionName):
    try:
        httpClient = httplib.HTTPConnection(region + '.battle.net', 80, timeout=30)
        httpClient.request('GET','/api/d3/profile/' + battlenettagString.replace('#','-') + '/')
        response = httpClient.getresponse()
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
    except Exception, e:
        str(e)
        pass
    finally:
        if httpClient:
            httpClient.close()
    