#!/usr/bin/env python
# -*- coding:utf8 -*-

import tornado.web
import MySQLdb
import sys
from index import BaseHandler
from tornado.options import options

reload(sys)
sys.setdefaultencoding("utf8")
class BlogHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        thead = ["标题","内容","分类","创建时间","修改时间","作者"]
        self.render("blog.html",web_title="运维管理平台",user=self.current_user,thead=thead,tbody=self.application.data.GetHost("blog"),page="文章列表")

class BlogACHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,input):
        if input == 'add':
            self.render("blog_action.html",web_title="运维管理平台",user=self.current_user,page="添加文章",group=self.application.data.GetAll('blog_group'),button="保存添加")
        elif input == 'edit':
            id = self.get_argument('id')
            data,group = self.application.data.GetOne('blog',id)
            self.render("blog_edit.html",web_title="运维管理平台",user=self.current_user,page="修改文章",data=data,group=group,button="保存修改")
        elif input == 'list':
            id = self.get_argument('id')
            data,group = self.application.data.GetOne('blog',id)
            tmp = data['content'].replace(" ","&nbsp;")
            data['content'] = tmp.split("\n")
            self.render("blog_list.html",web_title="运维管理平台",user=self.current_user,page="文章",data=data)
        elif input == 'del':
            id = self.get_argument('id')
            if self.application.data.DeleteOfid('blog',id):
                self.redirect("/blog")
            else:
                self.render("404.html",error="文章删除失败，可能文章已经在其他客户端被删")
        else:
            self.render("404.html",error="没有找到页面")

    def post(self,input):
        conn = MySQLdb.connect(host=options.dbhost,port=options.dbport,user=options.dbuser,passwd=options.dbpasswd,db=options.db,charset=options.charset)
        cursor = conn.cursor()
        if input == 'add':
            title = self.get_argument('title')
            content = self.get_argument('content')
            blog_class = self.get_argument('class')
            cursor.execute("insert into blog(id,title,content,class,mtime,ctime,email) values(null,'%s','%s','%s',now(),now(),'%s');"%(title,content,blog_class,self.current_user))
            conn.commit()
            cursor.close()
            conn.close()
            self.redirect("/blog")
        if input == 'edit':
            id = self.get_argument('rid')
            title = self.get_argument('title')
            content = self.get_argument('content')
            blog_class = self.get_argument('class')
            cursor.execute("update blog set title='%s',content='%s',class='%s',ctime=now() where id = %s"%(title,content,blog_class,id))
            conn.commit()
            cursor.close()
            conn.close()
            self.redirect("/blog/list?id=%s"%id)
        else:
            self.render("404.html",error="没有找到页面")