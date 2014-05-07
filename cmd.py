# encoding: UTF-8

import sae.const
import MySQLdb
import responser
import sqlquery
import logsql

def cmdHelp():
    rtnString = u'查询英雄列表：输入battle net tag，例：小明#7456\n'
    rtnString = rtnString + u'查询英雄状态：输入英雄列表前的编号\n'
    rtnString = rtnString + u'技能查询：skill 或者 build (须在英雄查询完之后)\n'
    rtnString = rtnString + u'装备查询：身体部位名称 (须在英雄查询完之后，具体查询命令可以输入“equip”或者“装备”来获得帮助)'
    return rtnString

def cmdHelpEquip():
    rtnString = u'各部位装备查询命令如下：\n'
    rtnString = rtnString + u'头部：head 头 头部 盔 头盔 帽 帽子\n'
    rtnString = rtnString + u'颈部：neck necklace amulet 项 项链 护符 护身符 颈 头颈 颈部 脖 脖子\n'
    rtnString = rtnString + u'肩膀：shoulder shoulders 肩 护肩 肩膀 肩甲\n'
    rtnString = rtnString + u'胸部：torso chest cloth clothes 躯干 胸 胸部 胸甲 衣 上衣 衣服\n'
    rtnString = rtnString + u'腕部：bracers 腕 护腕 腕部 手腕\n'
    rtnString = rtnString + u'手：hand hands golve golves 手 手套\n'
    rtnString = rtnString + u'左手指：leftfinger finger1 feftring ring1 手指 左手指 左指 手指1 左手戒指 左手戒 左戒指 左戒 戒指 戒指1 戒 戒1\n'
    rtnString = rtnString + u'右手指：rightfinger finger2 rightring ring2 右指 右手指 手指2 右手戒指 右手戒 右戒指 右戒 戒指2 戒2\n'
    rtnString = rtnString + u'主手：mainhand hand1 weapon weapon1 主手 武器1\n'
    rtnString = rtnString + u'副手：offhand hand2 weapon2 副手 武器2\n'
    rtnString = rtnString + u'腰部：waist belt 腰 腰部 腰带 皮带\n'
    rtnString = rtnString + u'腿部：leg legs pants trousers 腿 腿部 裤 裤子\n'
    rtnString = rtnString + u'脚：feet foot boots 脚 鞋 鞋子 靴 靴子'
    return rtnString

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
    except IndexError,ie:
        return u'没有找到您输入的编号'
    except Exception,e:
        logsql.writeLog(cursor, 'cmdHeroSeq Error:' + str(e))
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
        logsql.writeLog(cursor, 'cmdBntag Error:' + str(e))
    finally:
        cursor.close()
        conn.close()

def cmdHeroSkill(fromUser):
    try:
        conn=MySQLdb.connect(host=sae.const.MYSQL_HOST, user=sae.const.MYSQL_USER, passwd=sae.const.MYSQL_PASS, db=sae.const.MYSQL_DB, port=int(sae.const.MYSQL_PORT), charset='utf8')
        cursor=conn.cursor()
        n = sqlquery.selectLastHero(cursor, fromUser)
        if len(n) == 0:
            return u'您还未选择过英雄'
        bntag = n[0][0]
        region = n[0][1]
        heroid = n[0][2]
        sayString = responser.echoHeroSkills(bntag.encode('UTF-8'), region.encode('UTF-8'), heroid.encode('UTF-8'))
        return sayString
    except Exception,e:
        logsql.writeLog(cursor, 'cmdHeroSkill Error:' + str(e))
    finally:
        cursor.close()
        conn.close()

def cmdHeroItem(fromUser, itemId):
    try:
        conn=MySQLdb.connect(host=sae.const.MYSQL_HOST, user=sae.const.MYSQL_USER, passwd=sae.const.MYSQL_PASS, db=sae.const.MYSQL_DB, port=int(sae.const.MYSQL_PORT), charset='utf8')
        cursor=conn.cursor()
        n = sqlquery.selectLastHero(cursor, fromUser)
        if len(n) == 0:
            return u'您还未选择过英雄'
        bntag = n[0][0]
        region = n[0][1]
        heroid = n[0][2]
        sayString = responser.echoHeroItem(bntag.encode('UTF-8'), region.encode('UTF-8'), heroid.encode('UTF-8'), itemId)
        return sayString
    except Exception,e:
        logsql.writeLog(cursor, 'cmdHeroItem Error:' + str(e))
    finally:
        cursor.close()
        conn.close()

def cmdUnknown(fromUser, content):
    try:
        conn=MySQLdb.connect(host=sae.const.MYSQL_HOST, user=sae.const.MYSQL_USER, passwd=sae.const.MYSQL_PASS, db=sae.const.MYSQL_DB, port=int(sae.const.MYSQL_PORT), charset='utf8')
        cursor=conn.cursor()
        n = sqlquery.saveUnknownCommand(cursor, fromUser, content)
    except Exception,e:
        pass
    finally:
        cursor.close()
        conn.close()