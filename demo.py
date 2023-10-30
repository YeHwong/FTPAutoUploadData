#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2023-10-30 11:52
# @File: demo.py
# @Author: YeHwong
# @Email: 598318610@qq.com
# @Version ：1.0.0
"""
FTP批量下载数据
"""
import os, time, ftplib
from ftplib import FTP

class FtpDownloadCls:

    def __init__(self, ftpserver, port, usrname, pwd):
        self.ftpserver = ftpserver
        self.port = port
        self.usrname = usrname
        self.pwd = pwd
        self.ftp = self.ftpConnect()

    def ftpConnect(self):
        ftp = FTP()
        try:
            ftp.connect(self.ftpserver, self.port)
            ftp.login(self.usrname, self.pwd)
            ftp.encoding = 'gbk'
        except IOError as e:
            try:
                raise IOError('{}\n FTP login failed!!!'.format(e))
            finally:
                e = None
                del e

        else:
            print(ftp.getwelcome())
            print('\n+------- FTP connection successful!!! --------+\n')
            return ftp

    def downloadFile(self, ftpfile, localfile):
        print('{}  开始下载:{}'.format(time.strftime('%Y-%m-%d %H:%M:%S'), ftpfile))
        bufSize = 1024
        if os.path.exists(localfile):
            if ftpfile == 'FTP推送.exe':
                localfile = localfile[0:-4] + '(1).exe'
        with open(localfile, 'wb') as (fd):
            total = self.ftp.size(ftpfile)
            with tqdm(total=total, desc=ftpfile, unit=' bytes', unit_scale=True) as (pbar):

                def callback_(data):
                    l = len(data)
                    pbar.update(l)
                    fd.write(data)

                self.ftp.retrbinary('RETR {}'.format(ftpfile), callback_)
        print('{}  {}  下载完成'.format(time.strftime('%Y-%m-%d %H:%M:%S'), ftpfile))
        time.sleep(0.01)
        return True

    def downloadFiles(self, ftpath, localpath):
        print('FTP PATH: {0}'.format(ftpath))
        if not os.path.exists(localpath):
            os.makedirs(localpath)
        self.ftp.cwd(ftpath)
        for i, file in enumerate(self.ftp.nlst()):
            local = os.path.join(localpath, file)
            diff = self.checkFileDir(file)
            if diff == 'Dir':
                if not os.path.exists(local):
                    os.makedirs(local)
                self.downloadFiles(file, local)
            elif diff == 'File':
                self.downloadFile(file, local)
            else:
                break

        self.ftp.cwd('..')
        return True

    def checkFileDir(self, file_name):
        """
        判断当前目录下的文件与文件夹
        :param ftp: 实例化的FTP对象
        :param file_name: 文件名/文件夹名
        :return:返回字符串“File”为文件，“Dir”问文件夹，“Unknow”为无法识别
        """
        rec = ''
        try:
            try:
                rec = self.ftp.cwd(file_name)
                self.ftp.cwd('..')
                return 'Dir'
            except ftplib.error_perm as fe:
                try:
                    rec = fe
                finally:
                    fe = None
                    del fe

        finally:
            if '550' in str(rec):
                return 'File'
            if 'Current directory is' in str(rec):
                return 'Dir'

    def auto_create_path(FilePath):
        if os.path.exists(FilePath):
            print('dir exists')
        else:
            print('dir not exists')
            os.makedirs(FilePath)

    def ftpDisConnect(self):
        self.ftp.quit()


if __name__ == '__main__':
    ftpserver = '192.168.20.135'
    port = 21
    usrname = 'TestData'
    pwd = 'rs@123456'
    ftpath = '\\FTP推送'
    localpath = 'D:/FTP推送/'
    Ftp = FtpDownloadCls(ftpserver, port, usrname, pwd)
    Ftp.downloadFiles(ftpath, localpath)
    Ftp.ftpDisConnect()
    print('\n+-------- OK!!! --------+\n')
    os.system('pause')