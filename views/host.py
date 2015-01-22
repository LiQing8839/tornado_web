#!/usr/bin/env python
# -*- coding:utf8 -*-

import tornado.web
import sys
from index import BaseHandler

reload(sys)
sys.setdefaultencoding("utf8")
class HostTYHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        thead = ["编码","影院名称","影院编码","影院code","IP地址","密码","院线","鼎新版本","系统版本"]
        sql = "select * from cinema_ty"
        self.render("host.html", web_title=self.title, user=self.current_user, thead=thead, tbody=self.application.data.GetDAll(sql), page="通用主机", host="host_ty")

class HostTYACHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,input):
        if input == 'add':
            sql = "select * from cinema_group"
            self.render("host_action.html",web_title=self.title,user=self.current_user, page="添加通用主机", group=self.application.data.GetAll(sql), action='host_ty')
        elif input == 'edit':
            id = self.get_argument('id')
            data = self.application.data.GetOne("select * from cinema_ty where id = '%s'"%id)
            group = self.application.data.Getnoself("select * from cinema_group where cinema_group != (select cinema_group from cinema_ty where id = %s);"%id)
            self.render("host_edit.html",web_title=self.title,user=self.current_user,page="修改通用主机",data=data,group=group)
        else:
            self.render("404.html",error="没有找到页面")

    @tornado.web.authenticated
    def post(self,input):
        if input == 'add':
            values = (self.get_argument('cinema_name'), self.get_argument('cinema_num'), self.get_argument('cinema_code'), self.get_argument('cinema_ip'), self.get_argument('cinema_passwd'), self.get_argument('cinema_group'), self.get_argument('version_dx'), self.get_argument('version_sys'))
            self.application.data.Commit("insert into cinema_ty(id,cinema_name,cinema_num,cinema_code,cinema_ip,cinema_passwd,cinema_group,version_dx,version_sys) values(NULL,'%s','%s','%s','%s','%s','%s','%s','%s');"%(values))
            self.redirect("/host_ty")
        elif input == 'edit':
            values = (self.get_argument('cinema_name'), self.get_argument('cinema_num'), self.get_argument('cinema_code'), self.get_argument('cinema_ip'), self.get_argument('cinema_passwd'), self.get_argument('cinema_group'), self.get_argument('version_dx'), self.get_argument('version_sys'), self.get_argument('rid'))
            self.application.data.Commit("update cinema_ty set cinema_name='%s',cinema_num='%s',cinema_code='%s',cinema_ip='%s',cinema_passwd='%s',cinema_group='%s',version_dx='%s',version_sys='%s' where id = %s;"%(values))
            self.redirect("/host_ty")
        else:
            self.render("404.html",error="没有找到页面")

class HostWDHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        thead = ["编码","影院名称","影院编码","影院code","IP地址","密码","鼎新版本","系统版本"]
        sql = "select * from cinema_wd"
        self.render("host.html",web_title=self.title,user=self.current_user,thead=thead,tbody=self.application.data.GetDAll(sql),page="万达主机",host="host_wd")

class HostWDACHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,input):
        if input == 'add':
            self.render("host_action.html",web_title=self.title,user=self.current_user,page="添加万达主机",action="cinema_wd")
        elif input == 'edit':
            id = self.get_argument('id')
            sql = "select * from cinema_wd where id = %s"%id
            self.render("host_edit.html",web_title=self.title,user=self.current_user,page="修改万达主机",data=self.application.data.GetOne(sql),group='')
        else:
            self.render("404.html",error="没有找到页面")

    @tornado.web.authenticated
    def post(self,input):
        if input == 'add':
            values = (self.get_argument('cinema_name'), self.get_argument('cinema_num'), self.get_argument('cinema_code'), self.get_argument('cinema_ip'), self.get_argument('cinema_passwd'), self.get_argument('version_dx'), self.get_argument('version_sys'))
            self.application.data.Commit("insert into cinema_wd(id,cinema_name,cinema_num,cinema_code,cinema_ip,cinema_passwd,version_dx,version_sys) values(NULL,'%s','%s','%s','%s','%s','%s','%s');"%(values))
            self.redirect("/host_ty")
        elif input == 'edit':
            values = (self.get_argument('cinema_name'), self.get_argument('cinema_num'), self.get_argument('cinema_code'), self.get_argument('cinema_ip'), self.get_argument('cinema_passwd'), self.get_argument('version_dx'), self.get_argument('version_sys'), self.get_argument('rid'))
            self.application.data.Commit("update cinema_wd set cinema_name='%s',cinema_num='%s',cinema_code='%s',cinema_ip='%s',cinema_passwd='%s',version_dx='%s',version_sys='%s' where id = %s;"%(values))
            self.redirect("/host_ty")
        else:
            self.render("404.html",error="没有找到页面")