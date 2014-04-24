# coding: UTF-8  
import os

import sae  
import web

from weixinInterface import WeixinInterface
from test import Test   
from webtest import WebTest

urls = (
    '/', 'Hello',  
    '/weixin','WeixinInterface',
    '/test','Test',
    '/webtest','WebTest'
)

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)

class Hello:
   def GET(self):
        return ("hello")

app = web.application(urls, globals()).wsgifunc()
application = sae.create_wsgi_app(app)