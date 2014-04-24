#coding:UTF-8
import hashlib
import web
import lxml
import time
import os
from lxml import etree
import rex
import cmd

class Test:
 
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        data = web.input()      # 获取输入参数  
        signature = data.signature  
        timestamp = data.timestamp  
        nonce = data.nonce  
        echostr = data.echostr  
        token="dorabmon"             # 自己的token  
        list=[token,timestamp,nonce]    # 字典序排序  
        list.sort()  
        sha1=hashlib.sha1()             # sha1加密算法  
        map(sha1.update, list)  
        hashcode=sha1.hexdigest()  
        if hashcode == signature:       # 如果是来自微信的请求，则回复echostr  
            return echostr              # print "true"  

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
                return self.render.reply_text(fromUser,toUser,int(time.time()), u'欢迎关注。输入自己的battlenet TAG查询英雄。暂时只支持亚服。开发阶段，功能有限，功能会陆续放出，敬请谅解。')
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
            return self.render.reply_text(fromUser,toUser,int(time.time()), u'我不知道您想表达什么意思')

