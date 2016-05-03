#coding:UTF-8
import hashlib
import web
import lxml
import time
import os
from lxml import etree
import rex
import cmd
import logsql
import sqlquery

class WeixinInterface:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        return 'fff'
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
        # return self.render.reply_text(fromUser,toUser,int(time.time()), u'服务维护中')
        content=''
        if msgType == 'event':
            event=xml.find("Event").text
            if event == 'subscribe':
                sqlquery.addOneUser()
                return self.render.reply_text(fromUser,toUser,int(time.time()), u'欢迎关注。输入自己的battlenet TAG查询英雄。然后可查询技能或者装备。具体命令可输入help或者?获得帮助。')
        elif msgType == 'text':
            try:
                content=xml.find("Content").text
            except Exception, e:
                return
            finally:
                pass

        # 对content进行trim
        content = content.strip()
        # 对content进行分析，如果是battle net tag，则保存，并显示英雄列表。
        # 如果是数字，则去查询具体英雄
        commandType = rex.commando(content)
        sayString = ''
        if commandType == 900 :
            sayString = cmd.cmdHelp()
        elif commandType == 901 :
            sayString = cmd.cmdHelpEquip()
        elif commandType == 902 :
            sayString = cmd.cmdSaveLeaveMessage(fromUser, content)
        elif commandType == 921 :
            sayString = cmd.cmdToj(content)
        elif commandType == 922 :
            sayString = cmd.cmdTof(content)
        elif commandType == 700 :
            sayString = cmd.cmdAdminHelp()
        elif commandType == 701 :
            sayString = cmd.cmdUserAmount()
        elif commandType == 702 :
            sayString = cmd.cmdaddUserAmount(content)
        elif commandType == 703 :
            sayString = cmd.cmdEchoLeaveMessage(content)
        elif commandType == 1 :
            sayString = cmd.cmdBntag(fromUser, content)
        elif commandType == 2 :
            sayString = cmd.cmdHeroSeq(fromUser, content)
        elif commandType == 3 :
            sayString = cmd.cmdHeroSkill(fromUser)
        elif commandType == 4 :
            sayString = cmd.cmdHeroList(fromUser)
        elif commandType > 100 and commandType < 200 :
            sayString = cmd.cmdHeroItem(fromUser, commandType)
        elif commandType == 201 :
            sayString = cmd.cmdHeroRnak(fromUser)
        else :
            sayString = u'恕在下未能领会大侠的神意图。这位可敬的涅法雷姆，您可以输入help或者?便可知在下能为您做些什么。非常愿意为您效劳。'
            sayString = sayString + rex.knownBadCommand(content)
            cmd.cmdUnknown(fromUser, content)
        return self.render.reply_text(fromUser,toUser,int(time.time()), sayString)