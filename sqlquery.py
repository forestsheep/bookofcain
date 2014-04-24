#coding:UTF-8
import sys
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
    sql = "SELECT `heroes`.`battlenet_tag`,`bn_region`,`hero` FROM `heroes`,`last_bntag` WHERE `heroes`.`battlenet_tag`=`last_bntag`.`battlenet_tag` and `weixin_id` = %s and `seq_id`= %s"
    prm = (weixin_id,seqNo)
    rows = mysqlconn.select(cursor, sql, prm)
    return rows
