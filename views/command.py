#!/usr/bin/env python
# -*- coding:utf8 -*-

import tornado.web
from index import BaseHandler

class CommandHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        sql1 = "select * from cinema_ty"
        sql2 = "select * from cinema_wd"
        self.render("command.html",web_title="运维管理平台",user=self.current_user,page="命令提示符",action="",ty=self.application.data.GetDAll(sql1),wd=self.application.data.GetDAll(sql2))

class CommandACHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,input):
        if input == 'ips':
            sql1 = "select * from cinema_ty"
            sql2 = "select * from cinema_wd"
            self.render("command.html",web_title="运维管理平台",user=self.current_user,page="命令提示符",action="ips",ty=self.application.data.GetDAll(sql1),wd=self.application.data.GetDAll(sql2))
        elif input == 'group':
            self.render("command.html",web_title="运维管理平台",user=self.current_user,page="命令提示符",action="group",group=self.application.data.GetAll('select * from cinema_group'))
        else:
            self.render("404.html",error="没有找到页面")
