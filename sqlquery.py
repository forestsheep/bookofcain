#coding:UTF-8
import sys
import sae.const
import MySQLdb
import mysqlconn
import logsql

def saveLastQuery(cursor, wx_id, bntag):
    sql = "insert into last_bntag(weixin_id, battlenet_tag) values(%s, %s) ON DUPLICATE KEY UPDATE battlenet_tag =%s"
    prm = (wx_id, bntag, bntag)
    rows = mysqlconn.execute(cursor, sql, prm)
    return rows

def delHeroes(cursor, bntag):
    sql = "delete from `heroes` WHERE battlenet_tag=%s"
    prm = (bntag)
    rows = mysqlconn.execute(cursor, sql, prm)
    return rows

def saveHeroes(cursor, bntag, bnRegion, heroNo):
    sql = "insert into `heroes`(`seq_id`,`battlenet_tag`,`bn_region`,`hero`) values ((select ct from(SELECT count(battlenet_tag) as ct FROM `heroes` WHERE battlenet_tag=%s) as tmp)+1,%s,%s,%s)"
    prm = (bntag,bntag,bnRegion,heroNo)
    rows = mysqlconn.execute(cursor, sql, prm)
    return rows

def getHeroesSeq(cursor, bntag, bnRegion, heroNo):
    sql = "select seq_id from `heroes` WHERE battlenet_tag=%s and bn_region=%s and hero=%s"
    prm = (bntag, bnRegion, heroNo)
    rows = mysqlconn.select(cursor, sql, prm)
    return rows

def selectHero(cursor, weixin_id,seqNo):
    sql = "select `heroes`.`battlenet_tag`,`bn_region`,`hero` from `heroes`,`last_bntag` where `heroes`.`battlenet_tag`=`last_bntag`.`battlenet_tag` and `weixin_id` = %s and `seq_id`= %s"
    prm = (weixin_id,seqNo)
    rows = mysqlconn.select(cursor, sql, prm)
    bntag = rows[0][0]
    region = rows[0][1]
    heroid = rows[0][2]

    sql1 = "update `heroes` set `last_visited` = 0 where `battlenet_tag` = %s"
    prm1 = (bntag)
    mysqlconn.execute(cursor, sql1, prm1)

    sql2 = "update `heroes` set `last_visited` = 1 where `battlenet_tag` = %s and `bn_region` = %s and `hero` = %s"
    prm2 = (bntag, region, heroid)
    mysqlconn.execute(cursor, sql2, prm2)
    return rows

def selectLastHero(cursor, weixin_id):
    sql = "select `heroes`.`battlenet_tag`,`heroes`.`bn_region`,`heroes`.`hero` from `heroes`,`last_bntag` where `last_bntag`.`weixin_id` = %s and `last_bntag`.`battlenet_tag` = `heroes`.`battlenet_tag` and `heroes`.`last_visited`"
    prm =(weixin_id)
    rows = mysqlconn.select(cursor, sql, prm)
    return rows

def saveUnknownCommand(cursor, weixin_id, content):
    sql = "insert into `unknown_cmd`(`weixin_id`,`command`) values (%s, %s)"
    prm = (weixin_id, content)
    rows = mysqlconn.execute(cursor, sql, prm)
    return rows

def addOneUser():
    conn=MySQLdb.connect(host=sae.const.MYSQL_HOST, user=sae.const.MYSQL_USER, passwd=sae.const.MYSQL_PASS, db=sae.const.MYSQL_DB, port=int(sae.const.MYSQL_PORT), charset='utf8')
    cursor=conn.cursor()
    sql = "update `user_info` set `amount` = `amount` + 1 where `name` = %s"
    prm = ('user_amount')
    rows = mysqlconn.execute(cursor, sql, prm)
