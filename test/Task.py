import tkinter
import unittest
from datetime import datetime

from test import HTMLTestRunner
from test.DeviceCtrl import DeviceCtrl
from test.TestMonkey import TestMonkey
from test.monkeytestcase import MonkeyTestCase
import tkinter as tk  # 装载tkinter模块,用于Python3

class Task():
    def __init__(self, deviceid, apkversion, modulename ,testPerson ,screen_save_path,reports_path ,monkey_path, commandStr, logText):
        self.deviceid = deviceid
        self.devctrl = DeviceCtrl(deviceid)
        self.apkversion = apkversion
        self.modulename = modulename
        self.testPerson = testPerson
        self.screen_save_path = screen_save_path
        self.reports_path = reports_path
        self.monkey_path = monkey_path
        self.report_title =  modulename +  apkversion + ',Android版本 Monkey测试报告'
        self.reportfile =  reports_path +  deviceid + '_' + datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '.html'
        self.commandStr = commandStr
        self.logText = logText

    def wake(self):
        '''点亮并解锁'''
        # 自动化点亮并滑动解锁
        self.devctrl.wakeup()

    def start(self):
        '''开始测试'''

        suite = unittest.TestSuite()
        print('开始加载测试用例')
        self.logText.insert(tk.END, "\n开始加载测试用例")
        self.logText.see(tk.END)


        self.report_des = '详细信息: android版本：' +  self.devctrl.getversion()+',项目名称：' +  self.modulename +  self.apkversion  + ' \n命令:' + self.commandStr

        suite.addTest(
            MonkeyTestCase.loadtestcase(TestMonkey, monkeycmd=self.commandStr, deviceid=self.deviceid, story='monkey测试',\
                                        screen_save_path = self.screen_save_path,\
                                        reports_path = self.reports_path,\
                                        monkey_path = self.monkey_path, \
                                        logText = self.logText
                ))


        # 唤醒
        self.wake()
        print('monkey参数配置: ' + self.commandStr)
        self.logText.insert(tk.END, "\nmonkey参数配置:"+self.commandStr)
        self.logText.see(tk.END)
        print('请等待执行完成......')
        self.logText.insert(tk.END, "\n请等待执行完成:")
        self.logText.see(tk.END)
        # 开始执行
        with open(self.reportfile, 'wb') as f:
            return HTMLTestRunner.HTMLTestRunner(stream=f, title=self.report_title,
                                                 description=self.report_des, verbosity=2).run(suite)





