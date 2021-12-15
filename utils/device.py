import os
import re

'''android device类'''
'''teky'''


class Device():

    def __init__(self):
        self.__deviceids = []
        pass

    def get_deviceid_list(self, adbPath=""):
        '''返回一个当前deviceid list'''
        if adbPath == '':
            print('缺少adb环境')
            return False

        rt = os.popen(adbPath + ' version').read()

        if rt == '':
            print('缺少adb环境')
            return False
        else:
            print(rt)

        rt = os.popen(adbPath + ' devices').readlines()
        if len(rt) > 2:
            # if not rt.findall('error') >= 0 or not rt.findall('offline') >= 0
            # and rt.findall('unauthorized')
            for devicestr in rt:
                if devicestr.find('\tdevice') >= 0:
                    deviceid = devicestr.split('\t')[0]
                    self.__deviceids.append(deviceid)

        return self.__deviceids

    # 获取运行的进程
    def getPid(self, adbPath="", filter="monkey"):
        '''返回一个当前deviceid list'''
        if adbPath == '':
            print('缺少adb环境')
            return False

        rt = os.popen(adbPath + ' shell ps').readlines()
        #print(rt)
        #print(len(rt))
        if len(rt) > 1:
            # if not rt.findall('error') >= 0 or not rt.findall('offline') >= 0
            # and rt.findall('unauthorized')
            for devicestr in rt:
                if devicestr.find(filter) >= 0:
                    devicestrs = re.sub(' +', ' ', devicestr).split(' ')
                    #print(devicestrs[1])
                    os.popen(adbPath + ' shell kill ' + devicestrs[1])
        return True
