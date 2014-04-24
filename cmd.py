# encoding: UTF-8

import sae.const
import MySQLdb
import responser
import sqlquery
import logsql

def cmdHeroSeq(fromUser, content):
    try:
        conn=MySQLdb.connect(host=sae.const.MYSQL_HOST, user=sae.const.MYSQL_USER, passwd=sae.const.MYSQL_PASS, db=sae.const.MYSQL_DB, port=int(sae.const.MYSQL_PORT), charset='utf8')
        cursor=conn.cursor()
        n = sqlquery.selectHero(cursor, fromUser,content)
        bntag = n[0][0]
        region = n[0][1]
        heroid = n[0][2]
        sayString = responser.echoHeroDetail(bntag.encode('UTF-8'), region.encode('UTF-8'), heroid.encode('UTF-8'))
        return sayString
    except Exception,e:
        logsql.writeLog(cursor, str(e))
    finally:
        cursor.close()
        conn.close()

def cmdBntag(fromUser, content):
    try:
        conn=MySQLdb.connect(host=sae.const.MYSQL_HOST, user=sae.const.MYSQL_USER, passwd=sae.const.MYSQL_PASS, db=sae.const.MYSQL_DB, port=int(sae.const.MYSQL_PORT), charset='utf8')
        cursor=conn.cursor()
        sayString = responser.echoYourHeroes(cursor, content.encode('UTF-8'))
        # logsql.writeLog(cursor, sayString)
        if sayString == '' :
            sayString = u'没找到您的账号，请确认您的战网TAG'
        else :
            sqlquery.saveLastQuery(cursor, fromUser, content)
        return sayString;
    except Exception,e:
        logsql.writeLog(cursor, str(e))
    finally:
        cursor.close()
        conn.close()