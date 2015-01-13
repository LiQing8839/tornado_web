#!/usr/bin/env python
#-*- coding:utf8 -*-

import paramiko
import MySQLdb
import threading
import Queue
import sys

def MySQL(host,command):
    conn = MySQLdb.connect(host="localhost",port=3306,user="root",passwd="123qwe",db="yingyuan",charset="utf8")
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    if cursor.execute("select cinema_name,cinema_ip,cinema_passwd from cinema_ty where cinema_ip = '%s' union all select cinema_name,cinema_ip,cinema_passwd from cinema_wd where cinema_ip = '%s'"%(host,host)):
        out = cursor.fetchall()[0]
        reload(sys)
        sys.setdefaultencoding("utf-8")
        ip,name,passwd = out["cinema_ip"],out["cinema_name"],out["cinema_passwd"]
        com = Command(ip,passwd,name)
        cursor.close()
        conn.close()
        return com.Comm(command)
    else:
        cursor.close()
        conn.close()
        return u"消息来自 %s: \n\n这个IP地址: %s 不在数据里!\n"%(host,host)

class Command(object):
    def __init__(self,ip,passwd,name):
        self.ip = ip
        self.passwd = passwd
        self.cinema_name = name

    def Comm(self,command,port=22,user="root"):
        comlist = ['rm',':(){:|:&};:','>/dev/','mv','mkfs.ext','dd','reboot','halt','init','set','ln','sysctl','touch','mkdir','vi','exec','eval','export']
        i = command.split(' ')
        for j in i:
            if j in comlist:
                return u"消息来自 %s-%s: \n\n不允许在该主机IP:%s 中使用该命令!\n"%(self.cinema_name,self.ip,self.ip)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect('%s'%self.ip,port,user,'%s'%self.passwd,timeout=3306)
        except Exception as e:
            return u"消息来自%s-%s: \n\n无法连接当前IP: %s,错误信息: %s\n"%(self.cinema_name,self.ip,self.ip,e)
        stdin,stdout,stderr = ssh.exec_command("%s"%command)
        err = stderr.read()
        if err:
            return u"消息来自 %s-%s: \n\n%s\n"%(self.cinema_name,self.ip,err)
        else:
            return u"消息来自 %s-%s: \n\n%s\n"%(self.cinema_name,self.ip,stdout.read())

class MyThread(threading.Thread):
    def __init__(self,queue,command):
        self._jobq = queue
        self._comm = command
        threading.Thread.__init__(self)
    def run(self):
        while self.isAlive():
            try: 
                print MySQL(self._jobq.get(block=False,timeout=5),self._comm)
                self._jobq.task_done()
            except Exception as e:
                sys.exit(1)
                break

if __name__ == '__main__':
    ips = sys.argv[1].split(',')
    if len(ips) == 1:
        print MySQL(''.join(ips),sys.argv[2])
    else:
        q = Queue.Queue()
        l = len(ips) > 30 and 30 or len(ips)
        for i in ips:
            q.put(i)
        for i in range(l):
            t = MyThread(q,sys.argv[2])
            t.setDaemon(True)
            t.start()
        q.join()
