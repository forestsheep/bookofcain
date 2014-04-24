#coding:UTF-8
import mysqlconn

def writeLog(cursor, message):
    try :
        sql = "insert into log(message) values(%s)"
        prm = (message)
        rows = mysqlconn.execute(cursor, sql, prm)
        return rows
    except e :
        return e
