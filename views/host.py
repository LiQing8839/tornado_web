#!/usr/bin/env python
# -*- coding:utf8 -*-

import tornado.web
import MySQLdb
import sys
from index import BaseHandler
from tornado.options import options

reload(sys)
sys.setdefaultencoding("utf8")
class HostTYHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        thead = ["编码","影院名称","影院编码","影院code","IP地址","密码","院线","鼎新版本","系统版本"]
        self.render("host.html",web_title="运维管理平台",user=self.current_user,thead=thead,tbody=self.application.data.GetHost("cinema_ty"),page="通用主机",host="host_ty")

class HostTYACHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,input):
        if input == 'add':
            self.render("host_action.html",web_title="运维管理平台",user=self.current_user,page="添加通用主机",group=self.application.data.GetAll('cinema_group'),action='host_ty')
        elif input == 'edit':
            id = self.get_argument('id')
            data,group = self.application.data.GetOne('cinema_ty',id)
            self.render("host_edit.html",web_title="运维管理平台",user=self.current_user,page="修改通用主机",data=data,group=group)
        else:
            self.render("404.html")

    def post(self,input):
        conn = MySQLdb.connect(host=options.dbhost,port=options.dbport,user=options.dbuser,passwd=options.dbpasswd,db=options.db,charset=options.charset)
        cursor = conn.cursor()
        if input == 'add':
            cinema_name = self.get_argument('cinema_name')
            cinema_num = self.get_argument('cinema_num')
            cinema_code = self.get_argument('cinema_code')
            cinema_ip = self.get_argument('cinema_ip')
            cinema_passwd = self.get_argument('cinema_passwd')
            cinema_group = self.get_argument('cinema_group')
            version_dx = self.get_argument('version_dx')
            version_sys = self.get_argument('version_sys')
            cursor.execute("insert into cinema_ty(id,cinema_name,cinema_num,cinema_code,cinema_ip,cinema_passwd,cinema_group,version_dx,version_sys) values(NULL,'%s','%s','%s','%s','%s','%s','%s','%s');"%(cinema_name,cinema_num,cinema_code,cinema_ip,cinema_passwd,cinema_group,version_dx,version_sys))
            conn.commit()
            cursor.close()
            conn.close()
            self.redirect("/host_ty")
        elif input == 'edit':
            id = self.get_argument('rid')
            cinema_name = self.get_argument('cinema_name')
            cinema_num = self.get_argument('cinema_num')
            cinema_code = self.get_argument('cinema_code')
            cinema_ip = self.get_argument('cinema_ip')
            cinema_passwd = self.get_argument('cinema_passwd')
            cinema_group = self.get_argument('cinema_group')
            version_dx = self.get_argument('version_dx')
            version_sys = self.get_argument('version_sys')
            cursor.execute("update cinema_ty set cinema_name='%s',cinema_num='%s',cinema_code='%s',cinema_ip='%s',cinema_passwd='%s',cinema_group='%s',version_dx='%s',version_sys='%s' where id = %s;"%(cinema_name,cinema_num,cinema_code,cinema_ip,cinema_passwd,cinema_group,version_dx,version_sys,id))
            conn.commit()
            cursor.close()
            conn.close()
            self.redirect("/host_ty")
        else:
            self.render("404.html")

class HostWDHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        thead = ["编码","影院名称","影院编码","影院code","IP地址","密码","鼎新版本","系统版本"]
        self.render("host.html",web_title="运维管理平台",user=self.current_user,thead=thead,tbody=self.application.data.GetHost("cinema_wd"),page="万达主机",host="host_wd")

class HostWDACHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,input):
        if input == 'add':
            self.render("host_action.html",web_title="运维管理平台",user=self.current_user,page="添加万达主机")
        elif input == 'edit':
            id = self.get_argument('id')
            self.render("host_edit.html",web_title="运维管理平台",user=self.current_user,page="修改万达主机",data=self.application.data.GetOne('cinema_wd',id),group='')
        else:
            self.render("404.html",error="没有找到页面")

    def post(self,input):
        conn = MySQLdb.connect(host=options.dbhost,port=options.dbport,user=options.dbuser,passwd=options.dbpasswd,db=options.db,charset=options.charset)
        cursor = conn.cursor()
        if input == 'add':
            cinema_name = self.get_argument('cinema_name')
            cinema_num = self.get_argument('cinema_num')
            cinema_code = self.get_argument('cinema_code')
            cinema_ip = self.get_argument('cinema_ip')
            cinema_passwd = self.get_argument('cinema_passwd')
            version_dx = self.get_argument('version_dx')
            version_sys = self.get_argument('version_sys')
            cursor.execute("insert into cinema_wd(id,cinema_name,cinema_num,cinema_code,cinema_ip,cinema_passwd,version_dx,version_sys) values(NULL,'%s','%s','%s','%s','%s','%s','%s');"%(cinema_name,cinema_num,cinema_code,cinema_ip,cinema_passwd,version_dx,version_sys))
            conn.commit()
            cursor.close()
            conn.close()
            self.redirect("/host_ty")
        elif input == 'edit':
            id = self.get_argument('rid')
            cinema_name = self.get_argument('cinema_name')
            cinema_num = self.get_argument('cinema_num')
            cinema_code = self.get_argument('cinema_code')
            cinema_ip = self.get_argument('cinema_ip')
            cinema_passwd = self.get_argument('cinema_passwd')
            version_dx = self.get_argument('version_dx')
            version_sys = self.get_argument('version_sys')
            cursor.execute("update cinema_wd set cinema_name='%s',cinema_num='%s',cinema_code='%s',cinema_ip='%s',cinema_passwd='%s',version_dx='%s',version_sys='%s' where id = %s;"%(cinema_name,cinema_num,cinema_code,cinema_ip,cinema_passwd,version_dx,version_sys,id))
            conn.commit()
            cursor.close()
            conn.close()
            self.redirect("/host_ty")
        else:
            self.render("404.html",error="没有找到页面")