#!/usr/bin/env python
# -*- coding:utf8 -*-

import tornado.web
import os
import sys
import random
import datetime
from index import BaseHandler
import tornado.gen

reload(sys)
sys.setdefaultencoding("utf-8")

class UploadHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("upload.html", web_title="运维管理平台", user=self.current_user, page="上传文件")

    @tornado.web.asynchronous
    def post(self):
        upload_path=os.path.join(os.getcwd(),'uploads')
        upfile_meta = self.request.files['myfile']
        for meta in upfile_meta:
            rand = random.randint(1000,9999)
            now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            file_name = meta['filename']
            file_name = now+str(rand)+file_name[file_name.rfind("."):]
            file_path = os.path.join(upload_path,file_name)
            with open(file_path,'wb') as up:
                up.write(meta['body'])
        self.write(u"%s 文件上传成功"%file_name)
        self.finish()

class SyncHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        sql1 = "select * from cinema_ty"
        sql2 = "select * from cinema_wd"
        file_path=os.path.join(os.getcwd(),'uploads')
        file_list = os.listdir(file_path)
        d = {}
        for i in file_list:
            d[i] = round(os.path.getsize(os.path.join(file_path,i))/1024,2)
        self.render("sync.html", web_title="运维管理平台", user=self.current_user, page="同步文件", action="", tip=self.application.data.GetDAll(sql1), wip=self.application.data.GetDAll(sql2), path= file_path,data=d)
