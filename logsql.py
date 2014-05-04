#coding:UTF-8
import sae.const
import MySQLdb
import mysqlconn

def writeLog(cursor, message):
    try :
        sql = "insert into log(message) values(%s)"
        prm = (message)
        rows = mysqlconn.execute(cursor, sql, prm)
        return rows
    except e :
        return e

def log(message):
    try :
        conn=MySQLdb.connect(host=sae.const.MYSQL_HOST, user=sae.const.MYSQL_USER, passwd=sae.const.MYSQL_PASS, db=sae.const.MYSQL_DB, port=int(sae.const.MYSQL_PORT), charset='utf8')
        cursor=conn.cursor()
        writeLog(cursor, message)
    except Exception, e :
        return str(e)