#coding:UTF-8
import hashlib
import web
import lxml
import time
import os
from lxml import etree
import rex
import cmd

class WeixinInterface:
 
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)
     
    def GET(self):
        return ("get ok")

    def POST(self):
        str_xml=web.data()
        xml=etree.fromstring(str_xml)
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        content=''
        if msgType == 'event':
            event=xml.find("Event").text
            if event == 'subscribe':
                return self.render.reply_text(fromUser,toUser,int(time.time()), u'欢迎关注。输入自己的battlenet TAG查询英雄。开发阶段，功能有限，敬请谅解。如有建议或意见，请直接留言')
        elif msgType == 'text':
            try:
                content=xml.find("Content").text
            except Exception, e:
                return
            finally:
                pass
        # 对content进行分析，如果是battle net tag，则保存，并显示英雄列表。
        # 如果是数字，则去查询具体英雄
        commandType = rex.commando(content)
        if commandType == 1 :
            sayString = cmd.cmdBntag(fromUser, content)
            return self.render.reply_text(fromUser,toUser,int(time.time()), sayString)
        elif commandType == 2 :
            sayString = cmd.cmdHeroSeq(fromUser, content)
            return self.render.reply_text(fromUser,toUser,int(time.time()), sayString)
        else :
            return self.render.reply_text(fromUser,toUser,int(time.time()), u'我不知道您想做什么操作。目前只支持输入battle net tag查询英雄。然后输入编号查询英雄状态。如果您想要留言，那已经收到。')