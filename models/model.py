#!/usr/bin/env python
# -*- coding:utf8 -*-

import tornado.web
import tornado.gen
import json
import os

from views.index import BaseHandler
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

class DBHandler(BaseHandler):
    executor = ThreadPoolExecutor(15)
    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self,input):
        data = yield self.GetData(input)
        self.write(data)
        self.finish()

    @run_on_executor
    def GetData(self,input):
        if input == 'ips':
            ips = self.get_argument('ip')
            command = self.get_argument('command')
            data = os.popen('python models/command.py "%s" "%s"'%(ips,command)).read()
            array = (self.current_user,ips,command,data)
            sql = "insert into command_log values(null,'%s','%s','%s','%s')"%array
            self.application.data.Commit(sql)

        elif input == 'group':
            group = self.get_argument('group')
            command = self.get_argument('command')
            if group == 'wanda':
                sql = "select cinema_ip from cinema_wd"
                ips = ','.join([i['cinema_ip'] for i in self.application.data.GetDAll(sql)])
            else:
                sql = "select cinema_ip from cinema_ty where cinema_group = '%s'"%group
                ips = ','.join([i['cinema_ip'] for i in self.application.data.GetDAll(sql)])
            data = os.popen('python models/command.py "%s" "%s"'%(ips,command)).read()
            array = (self.current_user,group,command,data)
            sql = "insert into command_log values(null,'%s','%s','%s','%s')"%array
            self.application.data.Commit(sql)


        elif input not in ['report', 'error', 'log']:
            d = {'r':'reports', 'e':'errors' ,'l':'logs'}
            if input in d:
                data = '%d'%self.application.data.GetCount(d[input])
            else:
                data = '%d'%self.application.data.GetCount(input)

        else:
            d = {'report':'reports', 'error':'errors' ,'log':'logs'}
            sql = "select * from %s order by id desc limit 5"%d[input]
            data = json.dumps(self.application.data.GetDAll(sql))
        return data

class FileHandler(BaseHandler):
    executor = ThreadPoolExecutor(15)
    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self,input):
        data = yield self.GetData(input)
        self.write(data)

    @run_on_executor
    def GetData(self,input):
        if input == 'sync':
            array = (self.get_argument('ip'),self.get_argument('file'),self.get_argument('remote'))
            data = os.popen('python models/sftp.py "%s" "%s" "%s"'%(array)).read()
        elif input == 'del':
            for i in self.get_argument('delete').split(','):
                if os.path.exists(i):
                    os.remove(i)
                else:
                    data = "没有找到这个文件%s,请查看"%i
            else:
                data = "文件全部删除干净"
        return data
