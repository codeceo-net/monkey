# coding=utf-8
import time
import os
import unittest


# 一个monkey测试任务
class MonkeyTestCase(unittest.TestCase):

    def __init__(self, methodName='runTest', monkeycmd=None, deviceid=None, story=None, screen_save_path=None,
                 reports_path=None, monkey_path=None, logText=None):
        super(MonkeyTestCase, self).__init__(methodName)
        self.monkeycmd = monkeycmd
        self.deviceid = deviceid
        self.story = story
        self.testcmd = None
        self.screen_save_path = screen_save_path
        self.reports_path = reports_path
        self.monkey_path = monkey_path
        self.logText = logText

    @staticmethod
    def loadtestcase(testcase_klass, monkeycmd=None, deviceid=None, story=None, screen_save_path=None,
                     reports_path=None, monkey_path=None, logText=None):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'.
        """
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, monkeycmd=monkeycmd, deviceid=deviceid, story=story\
                                         , screen_save_path=screen_save_path,\
                                         reports_path=reports_path,\
                                         monkey_path=monkey_path,\
                                         logText=logText))
        return suite
