#!/usr/bin/env python
#-*- coding:utf8 -*-

import paramiko
import MySQLdb
import threading
import Queue
import sys
import os.path

def MySQL(host,files,remote):
    conn = MySQLdb.connect(host="localhost",user="root",passwd="123qwe",db="yingyuan",charset="utf8")
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    if cursor.execute("select cinema_name,cinema_ip,cinema_passwd from cinema_ty where cinema_ip = '%s' union all select cinema_name,cinema_ip,cinema_passwd from cinema_wd where cinema_ip = '%s'"%(host,host)):
        out = cursor.fetchall()[0]
        reload(sys)
        sys.setdefaultencoding("utf-8")
        ip,name,passwd = out["cinema_ip"],out["cinema_name"],out["cinema_passwd"]
        ftp = SFTP(ip,name,passwd)
        cursor.close()
        conn.close()
        return ftp.sftp(files,remote)
    else:
        cursor.close()
        conn.close()
        return u"消息来自 %s: \n这个IP地址: %s 不在数据库里!\n"%(sys.argv[0],host)

class SFTP(object):
    def __init__(self,ip,name,passwd):
        self.ip = ip
        self.passwd = passwd
        self.cinema_name = name

    def sftp(self,files,remote_dir,port=22,user="root"):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect('%s'%self.ip,port,user,'%s'%self.passwd,timeout=3306)
        except Exception as e:
            return u"消息来自 %s-%s: \n\n无法连接当前IP: %s,错误信息: %s\n"%(self.cinema_name,self.ip,self.ip,e)
        stdin,stdout,stderr = ssh.exec_command("[ -d %s ] && echo 'ok'"%(remote_dir))
        if not stdout.read():
            return u"消息来自 %s-%s: \n没有这个上传目录%s\n"%(self.cinema_name,self.ip,remote_dir)
        sftp = ssh.open_sftp()
        files = files.split(',')
        try:
            for i in files:
                remote = os.path.join(remote_dir,i.split('/')[-1])
                #remote = remote_dir+'/'+i.split('/')[-1]
                sftp.put(i,remote)
                sftp.chmod(remote,0644)
            sftp.close()
        except Exception as e:
            return u"消息来自 %s-%s: \n文件没有找到，上传失败! 错误消息: %s\n"%(self.cinema_name,self.ip,e)
        return u"消息来自 %s-%s: \n所有文件上传成功!\n"%(self.cinema_name,self.ip)
    
class MyThread(threading.Thread):
    def __init__(self,queue,files,remote_dir):
        self._jobq = queue
	self._file = files
	self._remote = remote_dir
        threading.Thread.__init__(self)
    def run(self):
        while self.isAlive():
            try: 
                print MySQL(self._jobq.get(block=False,timeout=5),self._file,self._remote)
                self._jobq.task_done()
            except Exception as e:
                sys.exit(1)
                break
            
if __name__ == '__main__':
    ips = sys.argv[1].split(',')
    if len(ips) == 1:
        print MySQL(''.join(ips),sys.argv[2],sys.argv[3])
    else:
        q = Queue.Queue()
        l = len(ips)
        for i in ips:
            q.put(i)
        for i in range(int(l)):
            t = MyThread(q,sys.argv[2],sys.argv[3])
            t.setDaemon(True)
            t.start()
        q.join()
